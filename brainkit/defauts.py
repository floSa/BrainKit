"""defauts.py — QUEL manifeste, pour QUEL vault, quand on ne l a pas dit.

# Le defaut qui a pris une verification en flagrant delit

`valider` et `generer` ont eu, un temps, un manifeste et un vault de DEFAUT
codes dans le kit — ceux qui servaient a le developper. Lances dans une
instance, ils rendaient des verdicts sur un AUTRE brain : des violations dures
qui n avaient aucun sens, et rien qui dise que le manifeste n etait pas le bon.

Le pire n est pas l echec, c est le SILENCE. Un vault valide contre le manifeste
d un autre sujet echoue partout, et un utilisateur qui ne connait pas le kit
conclut que son brain est casse.

Ces defauts n existent plus : le kit n embarque AUCUN manifeste d instance.

# La regle, en deux lignes, et elle vaut pour toutes les commandes

1. `--manifeste` donne     -> celui-la, et rien d autre ;
2. sinon `<vault>/brain.yml` s il existe -> le manifeste DE L INSTANCE.

Hors de ces deux cas, on s arrete. Deviner un manifeste, c est deviner contre
quoi on juge.

# L incoherence se DIT, elle ne se corrige pas

Un `--manifeste` donne l emporte toujours : c est un ordre, et le kit n a pas a
le contredire. Mais si le vault porte SON manifeste et qu il ne s agit pas du
meme brain, la commande le dit en toutes lettres AVANT le verdict — nom contre
nom. C est une ergonomie, pas une regle de validation : aucun code de sortie ne
change, aucune severite ne bouge.
"""

from __future__ import annotations

from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]


def vault_par_defaut() -> Path:
    """Le dossier courant. Un utilisateur d instance tape la commande DEDANS.

    Il n y a plus de repli : si le dossier courant ne porte pas de `brain.yml`,
    `resout()` s arrete et le dit. Un vault de defaut code dans le kit ferait
    juger un brain a la place d un autre.
    """
    return Path.cwd()


def _nom(chemin: Path) -> str:
    try:
        with chemin.open(encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
        return str((d.get("brain") or {}).get("nom") or "?")
    except Exception:                                   # pragma: no cover
        return "?"


def resout(manifeste: Path | None, vault: Path) -> tuple[Path | None, list[str]]:
    """(le manifeste a employer, ce qu il faut DIRE avant le verdict)."""
    dits: list[str] = []
    propre = vault / "brain.yml"

    if manifeste is not None:
        if propre.is_file() and propre.resolve() != manifeste.resolve():
            a, b = _nom(manifeste), _nom(propre)
            dits.append(
                f"ATTENTION — le vault porte SON manifeste (`{propre}`, brain "
                f"« {b} ») et tu valides contre `{manifeste}` (brain « {a} »).")
            if a != b:
                dits.append(
                    f"    Ce ne sont pas le même brain. Ce qui suit juge "
                    f"« {b} » contre les règles de « {a} » : les violations "
                    f"n'auront pas de sens. Retirer `--manifeste` pour prendre "
                    f"celui du vault.")
            else:
                dits.append(
                    "    Même nom de brain, deux fichiers — vérifier lequel "
                    "fait foi avant de conclure.")
        return manifeste, dits

    if propre.is_file():
        return propre, dits

    dits.append(
        f"manifeste introuvable : ni `--manifeste`, ni `{propre}`.\n"
        f"    Un manifeste ne se devine pas : c'est ce contre quoi le verdict "
        f"est rendu. Lancer la commande DANS le brain, ou passer "
        f"`--manifeste <fichier>`.")
    return None, dits
