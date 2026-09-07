"""defauts.py — QUEL manifeste, pour QUEL vault, quand on ne l a pas dit.

# Le defaut qui a pris une verification en flagrant delit

Remontee 3 du lot 5, avancee du lot 10 a ce lot-ci parce qu elle a deja piege
une verification : `valider` et `generer` prenaient pour defaut
`exemples/devbrain.brain.yml` et `../DevBrain`. Ce sont des defauts de
DEVELOPPEMENT DU KIT, pas d usage. Lances dans une instance, ils rendaient des
verdicts sur un AUTRE brain — avec des violations dures qui n avaient aucun
sens, et sans que rien ne dise que le manifeste n etait pas le bon.

Le pire n est pas l echec : c est le SILENCE. Un vault d histoire valide contre
le manifeste du dev echoue partout, et un utilisateur qui ne connait pas le kit
conclut que son brain est casse.

# La regle, en trois lignes, et elle vaut pour les cinq commandes

1. `--manifeste` donne     -> celui-la, et rien d autre ;
2. sinon `<vault>/brain.yml` s il existe -> le manifeste DE L INSTANCE ;
3. sinon, et seulement si le vault est le defaut de developpement du kit ->
   `exemples/devbrain.brain.yml`, en le DISANT.

Hors de ces trois cas, on s arrete. Deviner un manifeste, c est deviner contre
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
MANIFESTE_DE_DEVELOPPEMENT = RACINE_KIT / "exemples" / "devbrain.brain.yml"
VAULT_DE_DEVELOPPEMENT = RACINE_KIT.parent / "DevBrain"


def vault_par_defaut() -> Path:
    """Le vault courant s il porte un `brain.yml`, sinon le defaut du kit.

    Un utilisateur d instance tape `brainkit valider` DANS son brain. C est le
    cas le plus frequent, et c est celui qui n etait pas servi.
    """
    ici = Path.cwd()
    if (ici / "brain.yml").is_file():
        return ici
    return VAULT_DE_DEVELOPPEMENT


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

    if vault.resolve() == VAULT_DE_DEVELOPPEMENT.resolve() \
            and MANIFESTE_DE_DEVELOPPEMENT.is_file():
        dits.append(
            f"note — `{vault}` ne porte pas de `brain.yml` ; le kit prend son "
            f"manifeste de développement `{MANIFESTE_DE_DEVELOPPEMENT.name}`. "
            f"C'est le cas du DevBrain, qui ne deviendra une instance qu'au "
            f"lot 9.")
        return MANIFESTE_DE_DEVELOPPEMENT, dits

    dits.append(
        f"manifeste introuvable : ni `--manifeste`, ni `{propre}`.\n"
        f"    Un manifeste ne se devine pas : c'est ce contre quoi le verdict "
        f"est rendu. Lancer la commande DANS le brain, ou passer "
        f"`--manifeste <fichier>`.")
    return None, dits
