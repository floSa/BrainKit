# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""La passe de mesure de BrainKit, en ligne de commande.

    uv run brainkit/mesurer/__main__.py
    uv run brainkit/mesurer/__main__.py --vault <dossier> --manifeste <brain.yml>
    uv run brainkit/mesurer/__main__.py --rapport AI/mesure/2026-09-07-mesure.md
    uv run brainkit/mesurer/__main__.py --regle voisinage_declare

Codes de sortie :

    0 — la mesure est faite, et aucun refus ne se tient.
    1 — garde-fou 2 : au moins une severite `avertissement` sans `motif:` ecrit.
        Le kit REFUSE. C est le SEUL cas qui change le code de sortie — ni les
        violations comptees, ni le plancher non tenu ne sont des erreurs : la
        mesure a fait exactement son travail en les rapportant.
    2 — erreur d usage (vault ou manifeste introuvable).

Le refus du plancher n est donc PAS un code 1, et c est delibere : un vault de
douze pages qui refuse tout durcissement est un vault en bonne sante, pas un
vault en faute.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[2]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit import defauts                       # noqa: E402
from brainkit.mesurer import mesure                # noqa: E402
from brainkit.mesurer import rendu                 # noqa: E402
from brainkit.valider import charge                # noqa: E402


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(
        description="Mesure ce qu'une règle coûte, avant de la durcir.")
    ap.add_argument("--manifeste", type=Path, default=None,
                    help="défaut : le `brain.yml` du vault visé")
    ap.add_argument("--vault", type=Path, default=None,
                    help="défaut : le dossier courant s'il porte un `brain.yml`")
    ap.add_argument("--rapport", type=Path, default=None,
                    help="dépose le rapport en Markdown à ce chemin")
    ap.add_argument("--regle", default=None,
                    help="n'imprimer que la mesure d'une règle")
    ap.add_argument("--date", default="",
                    help="la date de la mesure (défaut : aujourd'hui)")
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

    mo = charge(manifeste)
    m, rec, occ, bl = mesure(mo, vault.resolve(), date=ns.date)

    if ns.regle:
        m.lignes = [x for x in m.lignes if x.regle == ns.regle]
        m.sans_motif = [x for x in m.sans_motif if x.regle == ns.regle]

    for ligne in rendu.texte(m, rec, occ, bl):
        print(ligne)

    if ns.rapport:
        ns.rapport.parent.mkdir(parents=True, exist_ok=True)
        ns.rapport.write_text("\n".join(rendu.markdown(m, rec, occ, bl)) + "\n",
                              encoding="utf-8")
        print(f"\nrapport écrit : {ns.rapport}")

    return 1 if m.sans_motif else 0


if __name__ == "__main__":
    raise SystemExit(main())
