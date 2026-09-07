# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Le semis d instance de BrainKit, en ligne de commande.

    uv run brainkit/semer/__main__.py --manifeste exemples/histobrain.brain.yml \\
                                      --dans /chemin/vers/histobrain
    uv run brainkit/semer/__main__.py --manifeste … --dans … --ecrire

# Le mode par defaut n ecrit rien, et ce n est pas negociable

Un semis CREE un vault. Le lancer pour voir ce qu il ferait est le premier
usage de la commande, et il ne doit rien coûter. `--ecrire` se demande.

Sortie : **0** si tout va bien, **1** sur un manque de manifeste ou un refus.
Un manque de manifeste n est pas une erreur d execution : c est le contrat qui
dit non, et il le dit AVANT d avoir ecrit un octet.

Trois commandes vivent dans ce module, parce qu elles partagent le meme plan
d ecriture et les memes garde-fous :

    brainkit semer         # de `brain.yml` a un vault vierge
    brainkit re-seuiller   # changer le seuil de promotion — une MIGRATION
    brainkit freeze        # copier le kit DANS l instance (livraison on-prem)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[2]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit.semer import figer, reseuiller, semis          # noqa: E402
from brainkit.valider import charge                          # noqa: E402


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass


def _manifeste(chemin: Path | None, vault: Path) -> Path | None:
    """Le manifeste donne, ou celui de l instance. Jamais un defaut du kit.

    Un defaut du kit — `exemples/devbrain.brain.yml`, comme pour `valider` et
    `generer` — serait ici un piege : semer ou re-seuiller avec le manifeste
    d un AUTRE brain reformerait l arbre selon des valeurs qui ne sont pas
    celles du vault.
    """
    if chemin is not None:
        return chemin
    candidat = vault / "brain.yml"
    return candidat if candidat.is_file() else None


# --------------------------------------------------------------------------- #
def main() -> int:
    _utf8()
    ap = argparse.ArgumentParser(
        description="Sème une instance vierge depuis un manifeste `brain.yml`.")
    ap.add_argument("--manifeste", type=Path, required=True)
    ap.add_argument("--dans", type=Path, required=True,
                    help="le dossier de l'instance — vide ou inexistant")
    ap.add_argument("--ecrire", action="store_true",
                    help="écrire pour de bon (le défaut n'écrit rien)")
    ap.add_argument("--sans-git", action="store_true",
                    help="ne pas créer le dépôt ni poser l'identité locale")
    ap.add_argument("--message", default=None,
                    help="le message du commit initial")
    ap.add_argument("--detail", type=int, default=0,
                    help="nombre de fichiers listés dans le rapport")
    ns = ap.parse_args()

    if not ns.manifeste.exists():
        print(f"manifeste introuvable : {ns.manifeste}")
        return 2
    mo = charge(ns.manifeste)
    s = semis.seme(mo, ns.dans, ecrire=ns.ecrire, avec_git=not ns.sans_git,
                   message=ns.message)
    return semis.imprime(s, mo, ns.dans.resolve(), detail=ns.detail)


# --------------------------------------------------------------------------- #
def main_reseuiller() -> int:
    _utf8()
    ap = argparse.ArgumentParser(
        description="Change le seuil de promotion d'un sous-dossier. C'est une "
                    "MIGRATION : elle déplace des pages, par `git mv`.")
    ap.add_argument("--manifeste", type=Path, default=None)
    ap.add_argument("--vault", type=Path, required=True)
    ap.add_argument("--seuil", type=int, required=True,
                    help="le seuil visé")
    ap.add_argument("--appliquer", action="store_true",
                    help="exécuter les `git mv` (le défaut n'écrit rien)")
    ap.add_argument("--detail", type=int, default=20)
    ns = ap.parse_args()

    vault = ns.vault.resolve()
    if not vault.is_dir():
        print(f"vault introuvable : {vault}")
        return 2
    chemin = _manifeste(ns.manifeste, vault)
    if chemin is None or not chemin.exists():
        print(f"manifeste introuvable : ni `--manifeste`, ni `{vault}/brain.yml`")
        return 2

    mo = charge(chemin)
    r = reseuiller.calcule(mo, vault, ns.seuil)
    if ns.appliquer and not r.refus:
        r = reseuiller.applique(mo, vault, r)
    return reseuiller.imprime(r, vault, detail=ns.detail)


# --------------------------------------------------------------------------- #
def main_freeze() -> int:
    _utf8()
    ap = argparse.ArgumentParser(
        description="Copie le kit DANS l'instance et coupe la dépendance. "
                    "Une instance figée ne reçoit plus de correctif.")
    ap.add_argument("--manifeste", type=Path, default=None)
    ap.add_argument("--vault", type=Path, required=True)
    ap.add_argument("--ecrire", action="store_true",
                    help="écrire pour de bon (le défaut n'écrit rien)")
    ns = ap.parse_args()

    vault = ns.vault.resolve()
    if not vault.is_dir():
        print(f"vault introuvable : {vault}")
        return 2
    chemin = _manifeste(ns.manifeste, vault)
    if chemin is None or not chemin.exists():
        print(f"manifeste introuvable : ni `--manifeste`, ni `{vault}/brain.yml`")
        return 2

    mo = charge(chemin)
    f = figer.fige(mo, vault, ecrire=ns.ecrire)
    return figer.imprime(f)


if __name__ == "__main__":
    raise SystemExit(main())
