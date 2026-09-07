"""figer.py — `freeze` : l instance devient autonome, et cesse de recevoir des correctifs.

# Pourquoi ce mode n est PAS optionnel (§5.1 du cadrage)

Le kit est un GENERATEUR, pas un depot-gabarit qu on clone : le jour du clone, le
code fourche, et avec trois instances chaque correction se reapplique trois fois
a la main — la troisieme divergera. Une instance ne contient donc que son
contenu, son `brain.yml`, ses documents generes et ses hooks. **Pas de code.**

Sauf que la specialite de floSa est l ON-PREM. Un vault livre chez un industriel
ne pourra pas installer un outil depuis internet, et une instance qui ne sait pas
se valider toute seule n est pas livrable. D ou `freeze`, et d ou le fait qu il
soit ecrit dans le meme lot que le semis : les deux chemins doivent naitre
ensemble, sinon le second n arrive jamais.

# Ce que `freeze` COPIE

Le paquet `brainkit/` — les deux validateurs, les quatre generateurs, le semis —
dans `AI/scripts/brainkit/`, plus trois lanceurs a en-tete PEP 723 qui se
lancent par `uv run` sans rien installer. Il copie, il ne reecrit pas : c est la
mitigation du risque « deux chemins de code qui se comportent differemment », et
le lot 10 ajoutera le test croise qui fait tourner les deux sur la meme instance.

# Ce que `freeze` PERD — et il faut l ecrire dans l instance elle-meme

| ce qui reste dehors | consequence |
|---|---|
| les correctifs a venir | une instance figee est une instance qui ne recevra plus rien |
| `schema/` et son validateur de manifeste | un `brain.yml` modifie ne se verifie plus contre le contrat |
| `outils/fidelite.py`, `tests/` | aucun moyen de prouver, sur place, que le kit fige se comporte comme le kit |
| la version | `kit.version` fige la date, et le kit refuse de tourner sur une version qu il ne connait pas — dans les deux sens |

Le manifeste de l instance est modifie pour le DIRE : `kit.mode` passe a `fige`.
C est la seule modification que `freeze` apporte au contenu, et elle est
volontairement visible dans un `git diff`.
"""

from __future__ import annotations

import datetime as _dt
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from ..valider.manifeste import Modele

RACINE_KIT = Path(__file__).resolve().parents[2]
PAQUET = "brainkit"

# Ce qui n est jamais copie : du bytecode et des arbres de travail.
EXCLUS = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")

LANCEUR = '''\
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""{titre} — lanceur d une instance FIGEE.

    uv run AI/scripts/{fichier}

Aucune installation : l en-tete PEP 723 ci-dessus dit a `uv` ce qu il faut, et
le paquet est a cote, dans `AI/scripts/brainkit/`. C est le chemin de lancement
d une instance `kit.mode: fige` — cf. `AI/scripts/FIGE.md`.
"""

from __future__ import annotations

import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
VAULT = ICI.parents[1]
if str(ICI) not in sys.path:
    sys.path.insert(0, str(ICI))

from brainkit.{module}.__main__ import main   # noqa: E402

if __name__ == "__main__":
    if not any(a.startswith("--manifeste") for a in sys.argv[1:]):
        sys.argv += ["--manifeste", str(VAULT / "brain.yml")]
    if not any(a.startswith("--vault") for a in sys.argv[1:]):
        sys.argv += ["--vault", str(VAULT)]
    raise SystemExit(main())
'''


@dataclass
class Figeage:
    racine: Path
    fichiers: int = 0
    etapes: list[str] = field(default_factory=list)
    refus: list[str] = field(default_factory=list)
    applique: bool = False

    @property
    def ok(self) -> bool:
        return not self.refus


def fige(mo: Modele, racine: Path, ecrire: bool = False) -> Figeage:
    """Copie le kit dans l instance et coupe la dependance. Ne le defait pas."""
    f = Figeage(racine=racine.resolve())
    if not (racine / "brain.yml").is_file():
        f.refus.append(f"`{racine}` ne porte pas de `brain.yml` — ce n'est pas "
                       f"une instance BrainKit, et figer un dossier quelconque "
                       f"n'aurait aucun sens")
        return f
    mode = str((mo.m.get("kit") or {}).get("mode") or "branche")
    if mode == "fige":
        f.refus.append("`kit.mode` vaut déjà `fige` — l'instance est déjà "
                       "autonome. Refiger la ferait diverger davantage, pas "
                       "moins.")
        return f

    source = RACINE_KIT / PAQUET
    cible = f.racine / "AI" / "scripts" / PAQUET
    fichiers = [p for p in sorted(source.rglob("*.py"))
                if "__pycache__" not in p.parts]
    f.fichiers = len(fichiers) + 3 + 1        # + trois lanceurs + FIGE.md
    f.etapes = [f"copier `{PAQUET}/` ({len(fichiers)} module(s)) vers "
                f"`AI/scripts/{PAQUET}/`",
                "écrire les trois lanceurs PEP 723 (`valider.py`, `generer.py`, "
                "`semer.py`)",
                "écrire `AI/scripts/FIGE.md` — ce qui est copié, ce qui est perdu",
                "passer `kit.mode` à `fige` dans `brain.yml`"]
    if not ecrire:
        return f

    if cible.exists():
        shutil.rmtree(cible)
    cible.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, cible, ignore=EXCLUS)

    for module, fichier, titre in (("valider", "valider.py", "valider"),
                                   ("generer", "generer.py", "générer"),
                                   ("semer", "semer.py", "semer")):
        (f.racine / "AI" / "scripts" / fichier).write_text(
            LANCEUR.format(titre=titre, fichier=fichier, module=module),
            encoding="utf-8", newline="\n")

    (f.racine / "AI" / "scripts" / "FIGE.md").write_text(
        _note(mo), encoding="utf-8", newline="\n")
    _bascule_le_mode(f.racine / "brain.yml", f)
    f.applique = not f.refus
    return f


def _bascule_le_mode(chemin: Path, f: Figeage) -> None:
    """`kit.mode: branche` -> `fige`, par EDITION DE LIGNE.

    Relire le YAML et le reecrire perdrait tous les commentaires — donc tous les
    `motif:`, qui sont la moitie de la valeur d un manifeste. Une seule ligne
    change, et un `git diff` la montre.
    """
    texte = chemin.read_text(encoding="utf-8")
    neuf, n = re.subn(r"(?m)^(\s+mode:\s*)branche\s*$",
                      r"\1fige", texte, count=1)
    if n != 1:
        f.refus.append("`kit.mode: branche` introuvable dans `brain.yml` — "
                       "le mode n'a pas été basculé, et le reste de la copie "
                       "mentirait sur son état")
        return
    marque = f"\n# Figé le {_dt.date.today().isoformat()} par `brainkit freeze`.\n"
    chemin.write_text(neuf.rstrip("\n") + "\n" + marque, encoding="utf-8",
                      newline="\n")


def _note(mo: Modele) -> str:
    version = (mo.m.get("kit") or {}).get("version") or "?"
    return f"""\
---
nom: FIGE
---

# Instance FIGÉE — ce qui est copié, ce qui est perdu

Figée le {_dt.date.today().isoformat()}, depuis BrainKit `{version}`.

## Pourquoi

Une instance normale ne contient **pas de code** : le kit vit ailleurs, installé
une fois, et lit `brain.yml`. C'est ce qui garantit qu'une correction du
validateur atteint toutes les instances le même jour.

Ce vault a été **figé** : le kit y a été copié. C'est le mode prévu pour une
livraison on-prem, où l'instance ne peut pas dépendre d'un dépôt externe.

## Ce qui est copié

- `AI/scripts/brainkit/` — les deux validateurs, les quatre générateurs, le semis.
- `AI/scripts/valider.py`, `generer.py`, `semer.py` — trois lanceurs à en-tête
  PEP 723. Ils résolvent `brain.yml` et la racine du vault tout seuls.

```bash
uv run AI/scripts/valider.py
uv run AI/scripts/generer.py            # --check
uv run AI/scripts/generer.py --ecrire
```

## Ce qui est PERDU — et c'est le prix, pas un défaut

| Ce qui reste dehors | Conséquence |
|---|---|
| Les correctifs à venir | **Cette instance ne recevra plus rien.** Un défaut corrigé dans le kit reste ici. |
| `schema/brain.schema.json` et son validateur | Un `brain.yml` modifié ne se vérifie plus contre le contrat. |
| `outils/fidelite.py` et les jeux d'épreuve | Aucun moyen de prouver, sur place, que ce kit figé se comporte comme le kit. |
| La comparabilité | Deux instances figées à deux dates ne portent pas le même code, et rien ne le dit à l'ouverture. |

## Revenir en arrière

Il n'y a pas de `unfreeze`, et c'est délibéré : un dégel silencieux ferait
cohabiter deux versions du même code sans que personne ne le sache. Pour
rebrancher l'instance : supprimer `AI/scripts/brainkit/` et les trois lanceurs,
remettre `kit.mode: branche` dans `brain.yml`, et installer le kit.
"""


def imprime(f: Figeage, detail: int = 0) -> int:
    etat = "APPLIQUÉ" if f.applique else "simulation, rien n'est écrit"
    print(f"freeze — `{f.racine.name}`  [{etat}]")
    for e in f.etapes:
        print(f"  - {e}")
    if f.refus:
        print(f"\n{len(f.refus)} refus :")
        for r in f.refus:
            print(f"  [REFUS] {r}")
        return 1
    if f.applique:
        print(f"\nOK — {f.fichiers} fichier(s). L'instance est autonome, et elle "
              f"ne recevra plus de correctif : cf. `AI/scripts/FIGE.md`.")
    else:
        print(f"\nOK — {f.fichiers} fichier(s) SERAIENT écrits. Relancer avec "
              f"`--ecrire`.")
    return 0
