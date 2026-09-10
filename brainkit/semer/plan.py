"""plan.py — LE plan d ecriture du semis, et le seul du paquet.

Aucun autre module de `brainkit.semer` n appelle `write_text`, `mkdir` ou
`shutil.copy`. Tout passe par `Plan.pose()` et `Plan.dossier()`, et c est
verifiable en une commande :

    grep -rnE 'write_text|write_bytes|mkdir|copytree|copy2' brainkit/semer/
    # -> plan.py, plus figer.py qui copie le kit (et le declare)

C est la meme discipline que `generer/sortie.py`, pour la meme raison, et avec
une exigence de plus : un semis ne rafraichit pas un vault, il en CREE un. Il
n a donc aucune raison d ecrire dans un arbre qui existe deja, et le refuser est
la seule protection qui ne depende pas de l attention de l appelant.

# Les quatre refus, et pourquoi aucun n est negociable

| refus | ce qu il evite |
|---|---|
| la cible existe et n est pas vide | ecraser un vault qu on croyait absent |
| la cible vit sous le depot du kit | versionner une instance d essai dans BrainKit |
| la cible vit sous un depot git     | semer DANS le vault d'origine, ou dans n importe quel dépôt |
| la cible vit sous un vault         | semer un brain a l interieur d un autre |

Les deux derniers sont volontairement formules SANS nommer le vault d'origine. Un garde-fou
qui interdit un chemin par son nom protege un chemin ; un garde-fou qui interdit
une SITUATION protege tous les chemins qui s y trouveront un jour. « Sous un
depot git » couvre le vault d'origine, BrainKit, et le depot d un client qu on n a pas
encore rencontre.

# Le defaut n ecrit rien

`Plan(racine)` construit le plan et ne pose pas un octet. `Plan(racine,
ecrire=True)` ecrit. Un semis qu on lance pour voir ce qu il ferait est le
premier usage de la commande, et il ne doit rien coûter.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# Meme contournement que `generer/sortie.py` : Windows plafonne un chemin a 260
# caracteres sauf prefixe `\\?\`, et un vault d essai pose sous « Documents/
# BrainKit-essais/ » en consomme deja la moitie.
_LIMITE_WINDOWS = 240


def _long(p: Path) -> Path:
    if os.name != "nt":
        return p
    brut = str(p)
    if len(brut) < _LIMITE_WINDOWS or brut.startswith("\\\\?\\"):
        return p
    return Path("\\\\?\\" + brut)


# Ce qui, dans un dossier parent, dit « il y a deja un brain ici ».
MARQUEURS_DE_VAULT = ("brain.yml", ".obsidian")


@dataclass
class Fichier:
    chemin: str            # relatif a la racine de l instance, en posix
    octets: int
    quoi: str = ""         # quelle partie du semis l a pose


@dataclass
class Plan:
    """Ce que le semis ECRIRA, et rien de plus tant qu on ne le demande pas."""

    racine: Path
    ecrire: bool = False
    fichiers: list[Fichier] = field(default_factory=list)
    dossiers: list[str] = field(default_factory=list)
    refus: list[str] = field(default_factory=list)
    racine_du_kit: Path | None = None
    # Les quatre refus ci-dessus valent pour un SEMIS — la creation d un vault.
    # `re-seuiller` ecrit dans un vault qui existe deja et qui n est evidemment
    # pas vide : il desactive le controle de CIBLE, jamais celui d ecriture
    # unique. La distinction est declaree ici plutot que contournee ailleurs.
    controle_la_cible: bool = True

    # ------------------------------------------------------------------ #
    def __post_init__(self) -> None:
        self.racine = self.racine.resolve()
        if self.racine_du_kit is not None:
            self.racine_du_kit = self.racine_du_kit.resolve()
        if self.controle_la_cible:
            self._controle_la_cible()

    def _controle_la_cible(self) -> None:
        cible = self.racine
        if cible.exists():
            if not cible.is_dir():
                self.refus.append(f"`{cible}` existe et n'est pas un dossier")
                return
            contenu = sorted(x.name for x in cible.iterdir())
            if contenu:
                self.refus.append(
                    f"`{cible}` n'est pas vide ({len(contenu)} entrée(s) : "
                    f"{', '.join(contenu[:6])}"
                    f"{'…' if len(contenu) > 6 else ''}) — un semis crée un vault, "
                    f"il n'en répare pas un. Choisir un dossier vide ou inexistant.")

        parents = [cible] + list(cible.parents)
        if self.racine_du_kit is not None:
            if cible == self.racine_du_kit or self.racine_du_kit in cible.parents:
                self.refus.append(
                    f"`{cible}` vit SOUS le dépôt du kit `{self.racine_du_kit}` — "
                    f"refusé : une instance ne se versionne pas dans BrainKit.")
        for p in parents:
            if (p / ".git").exists() and p != cible:
                self.refus.append(
                    f"`{cible}` vit SOUS le dépôt git `{p}` — refusé : une "
                    f"instance porte SON dépôt, elle n'entre pas dans celui d'un "
                    f"autre. C'est ce refus qui interdit de semer dans un vault "
                    f"existant sans avoir à le nommer.")
                break
        for p in parents:
            if p == cible:
                continue
            for marqueur in MARQUEURS_DE_VAULT:
                if (p / marqueur).exists():
                    self.refus.append(
                        f"`{cible}` vit SOUS le vault `{p}` (il porte "
                        f"`{marqueur}`) — refusé : un brain ne se sème pas dans "
                        f"un autre brain.")
                    return

    @property
    def refuse(self) -> bool:
        return bool(self.refus)

    # ------------------------------------------------------------------ #
    def dossier(self, rel: str, garde: bool = False) -> None:
        """Declare un dossier. `garde` y pose un `.gitkeep` — git n en suit aucun vide."""
        if self.refuse:
            return
        rel = rel.strip("/")
        if rel and rel not in self.dossiers:
            self.dossiers.append(rel)
        if self.ecrire:
            _long(self.racine / rel).mkdir(parents=True, exist_ok=True)
        if garde:
            self.pose(f"{rel}/.gitkeep" if rel else ".gitkeep", "", "dossier")

    def pose(self, rel: str, texte: str, quoi: str = "") -> None:
        """Pose un fichier. Un chemin pose deux fois est un REFUS, jamais un ecrasement."""
        if self.refuse:
            return
        deja = next((f for f in self.fichiers if f.chemin == rel), None)
        if deja is not None:
            self.refus.append(
                f"{rel} : posé deux fois — par `{deja.quoi}` puis par `{quoi}`. "
                f"Le second écraserait le premier.")
            return
        self.fichiers.append(Fichier(rel, len(texte.encode("utf-8")), quoi))
        if not self.ecrire:
            return
        cible = _long(self.racine / rel)
        cible.parent.mkdir(parents=True, exist_ok=True)
        # Fins de ligne LF, toujours, et sans exception : un hook `.githooks/*`
        # dont le shebang porte un CR n est pas executable par git, et les quatre
        # premieres conversations du vault d'origine s y sont fait prendre. Ecrire tout
        # le vault en LF evite d avoir a se demander, fichier par fichier, si
        # celui-la fait partie des exceptions.
        with cible.open("w", encoding="utf-8", newline="\n") as f:
            f.write(texte)

    def refuse_avec(self, message: str) -> None:
        self.refus.append(message)

    # ------------------------------------------------------------------ #
    def par_quoi(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for f in self.fichiers:
            out[f.quoi] = out.get(f.quoi, 0) + 1
        return dict(sorted(out.items()))
