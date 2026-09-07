# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""Le validateur de vault de BrainKit, en ligne de commande.

    uv run brainkit/valider/__main__.py
    uv run brainkit/valider/__main__.py --manifeste <brain.yml> --vault <dossier>
    uv run brainkit/valider/__main__.py --regle voisinage_declare
    uv run brainkit/valider/__main__.py --tout

Sort en 1 si une regle DURE est violee, en 0 sinon. Une regle en
`avertissement` signale ; une regle en `a_mesurer` compte, sans juger — c est la
severite par defaut de toute instance neuve.

LECTURE SEULE. Le validateur n a aucun chemin d ecriture :

    grep -rnE 'write_text|write_bytes|mkdir|unlink|rmtree|rename' brainkit/valider/
    # -> une seule ligne : cette phrase

Le perimetre de la promesse a ete RESTREINT au lot 4, et il faut le dire :
`brainkit/generer/` ecrit, par construction, et son unique chemin d ecriture vit
dans `brainkit/generer/sortie.py`. Une promesse « le paquet n ecrit nulle part »
serait devenue fausse en silence le jour ou le generateur est arrive.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[2]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit import defauts                          # noqa: E402
from brainkit.valider import charge, imprime, valide  # noqa: E402


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(description="Valide un vault contre son manifeste.")
    ap.add_argument("--manifeste", type=Path, default=None,
                    help="défaut : le `brain.yml` du vault visé")
    ap.add_argument("--vault", type=Path, default=None,
                    help="défaut : le dossier courant s'il porte un `brain.yml`")
    ap.add_argument("--regle", default=None,
                    help="n'imprimer que les constats d'une règle")
    ap.add_argument("--tout", action="store_true",
                    help="imprimer aussi les notes (conditions non évaluables, "
                         "pages écartées d'une dérivation)")
    ns = ap.parse_args()

    vault = ns.vault if ns.vault is not None else defauts.vault_par_defaut()
    if not vault.is_dir():
        return print(f"vault introuvable : {vault}") or 2
    manifeste, dits = defauts.resout(ns.manifeste, vault)
    for ligne in dits:
        print(ligne)
    if manifeste is None:
        return 2
    if not manifeste.exists():
        return print(f"manifeste introuvable : {manifeste}") or 2
    if dits:
        print()
    ns = argparse.Namespace(**{**vars(ns), "manifeste": manifeste,
                               "vault": vault})

    mo = charge(ns.manifeste)
    v = valide(mo, ns.vault.resolve())
    return imprime(v, mo, ns.vault.resolve(), regle=ns.regle, tout=ns.tout)


if __name__ == "__main__":
    raise SystemExit(main())
