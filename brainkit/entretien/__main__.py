# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""L entretien d initialisation de BrainKit, en ligne de commande.

    uv run brainkit entretien --questions                     # les 11 passes
    uv run brainkit entretien --refus                         # les 13 refus
    uv run brainkit entretien --brouillon e.yml               # OU on en est
    uv run brainkit entretien --brouillon e.yml --repondre '0.1=…'
    uv run brainkit entretien --brouillon e.yml --reponses lot.yml
    uv run brainkit entretien --brouillon e.yml --verifier
    uv run brainkit entretien --brouillon e.yml --composer brain.yml
    uv run brainkit entretien --brouillon e.yml --semer <dossier> --ecrire

# Cette commande n est pas l entretien

L entretien est une CONVERSATION, et c est le skill qui la mene
(`skills/entretien/SKILL.md`). Cette commande est ce que le skill APPELLE : elle
tient le brouillon, elle applique les treize refus, elle compose, et elle
appelle le semis. Elle sert aussi a rejouer un entretien sans conversation —
c est ce que fait le jeu d epreuve, et c est la seule facon de PROUVER qu un
entretien produit un vault vert.

# Rien ne s ecrit sans qu on le demande

`--etat` est le defaut, et il ne touche rien. `--composer` ecrit le manifeste et
refuse tant qu il reste un grief. `--semer` sans `--ecrire` ne pose pas un octet.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[2]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit.entretien import brouillon as _brouillon        # noqa: E402
from brainkit.entretien import composer, passes, refus            # noqa: E402
from brainkit.entretien import rendu as _rendu                    # noqa: E402


def _utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass


def main() -> int:
    _utf8()
    ap = argparse.ArgumentParser(
        description="Mène (ou rejoue) l'entretien d'initialisation d'un brain.")
    ap.add_argument("--brouillon", type=Path, default=Path(_brouillon.NOM_PAR_DEFAUT),
                    help="le fichier de reprise (défaut : ./entretien.yml)")
    ap.add_argument("--questions", action="store_true",
                    help="imprimer les onze passes et leurs questions")
    ap.add_argument("--refus", action="store_true",
                    help="imprimer les treize refus de deviner")
    ap.add_argument("--repondre", action="append", default=[],
                    metavar="ID=VALEUR",
                    help="enregistrer une réponse (la valeur est lue en YAML)")
    ap.add_argument("--reponses", type=Path, default=None,
                    help="un fichier YAML {id: valeur} — un lot de réponses")
    ap.add_argument("--oublier", action="append", default=[], metavar="ID",
                    help="rouvrir une question déjà répondue")
    ap.add_argument("--provenance", default=refus.PROVENANCE_VALIDE,
                    help="la provenance des réponses de cet appel")
    ap.add_argument("--rappel", action="store_true",
                    help="relire ce qui a déjà été dit (à faire en reprenant)")
    ap.add_argument("--verifier", action="store_true",
                    help="passer les treize refus sur l'état courant")
    ap.add_argument("--composer", type=Path, default=None, metavar="SORTIE",
                    help="écrire le `brain.yml` — refusé s'il reste un grief")
    ap.add_argument("--semer", type=Path, default=None, metavar="DOSSIER",
                    help="composer PUIS semer l'instance")
    ap.add_argument("--ecrire", action="store_true",
                    help="pour `--semer` : écrire pour de bon")
    ns = ap.parse_args()

    if ns.questions:
        print(passes.rendu())
        return 0
    if ns.refus:
        print(f"Les {len(refus.LES_TREIZE)} refus de deviner — liste FERMÉE.\n")
        for r in refus.LES_TREIZE:
            print(f"{r.n:2d}. {r.objet}")
            print(f"    à la place : {r.a_la_place}")
            print(f"    question   : {r.question}"
                  f"{'   [contrôlé mécaniquement]' if r.mecanique else ''}\n")
        return 0

    try:
        b = _brouillon.charge(ns.brouillon)
    except ValueError as e:
        print(str(e))
        return 2

    touche = False
    for oubli in ns.oublier:
        b.oublie(oubli)
        touche = True
        print(f"question {oubli} rouverte")

    lots: list[tuple[str, object]] = []
    if ns.reponses is not None:
        if not ns.reponses.is_file():
            print(f"fichier de réponses introuvable : {ns.reponses}")
            return 2
        with ns.reponses.open(encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
        lots += [(str(k), v) for k, v in (d.get("reponses") or d).items()]
    for brut in ns.repondre:
        if "=" not in brut:
            print(f"réponse mal formée : `{brut}` — attendu `ID=VALEUR`")
            return 2
        qid, val = brut.split("=", 1)
        lots.append((qid.strip(), yaml.safe_load(val)))

    for qid, val in lots:
        griefs = b.repond(qid, val, provenance=ns.provenance)
        touche = True
        for g in griefs:
            print(f"[REFUSÉ] {g}")
        if griefs:
            return 1
    if touche:
        _brouillon.enregistre(b)

    if ns.rappel:
        print(b.rappel())
        print()

    if ns.composer is None and ns.semer is None and not ns.verifier:
        print(b.etat())
        return 0

    # --- composition ------------------------------------------------------ #
    m, griefs = composer.compose(b)
    if ns.verifier and not (ns.composer or ns.semer):
        print(b.etat())
        print()
        if not griefs:
            print("Les treize refus passent. Le manifeste est composable.")
            return 0
        print(f"{len(griefs)} grief(s) — rien ne se compose tant qu'il en reste "
              f"un :")
        for g in griefs:
            print(f"  [GRIEF] {g}")
        return 1
    if m is None or griefs:
        print(f"{len(griefs)} grief(s) — RIEN n'est écrit, RIEN n'est semé :")
        for g in griefs:
            print(f"  [GRIEF] {g}")
        return 1

    # OU poser le manifeste, et c est moins anodin qu il n y parait : le plan
    # d ecriture du semis REFUSE une cible qui vit sous un dossier portant un
    # `brain.yml` — « un brain ne se sème pas dans un autre brain ». Poser le
    # manifeste a cote du brouillon, puis semer dans un sous-dossier de ce
    # meme endroit, declenche donc ce refus, et le message parle d un vault
    # qui n existe pas. Le defaut de `--semer` est donc un fichier TEMPORAIRE,
    # hors de l arborescence de la cible. Le semis le copie de toute facon a la
    # racine de l instance : c est lui qui devient le manifeste du brain.
    if ns.composer is not None:
        sortie = ns.composer
    elif ns.semer is not None:
        import tempfile
        sortie = Path(tempfile.mkdtemp(prefix="brainkit-entretien-")) / "brain.yml"
    else:
        sortie = ns.brouillon.parent / "brain.yml"
    _rendu.ecrit(m, sortie, brouillon=str(ns.brouillon))
    print(f"manifeste écrit : {sortie}")

    if ns.semer is not None and sortie.parent in ns.semer.resolve().parents:
        print(f"[REFUS] le manifeste est posé dans `{sortie.parent}`, qui est un "
              f"parent de la cible `{ns.semer}`. Le semis refuserait la cible "
              f"comme vivant « sous un vault ». Poser le `--composer` ailleurs, "
              f"ou l'omettre pour laisser l'entretien choisir un temporaire.")
        return 1

    if ns.semer is None:
        return 0

    # --- semis ------------------------------------------------------------ #
    from brainkit.semer import semis                          # noqa: E402
    from brainkit.valider import charge                       # noqa: E402

    mo = charge(sortie)
    # Le brouillon part AVEC l instance : il est la seule trace de POURQUOI la
    # taxonomie est celle-la, et il se relira dans six mois.
    trace = (ns.brouillon.read_text(encoding="utf-8")
             if ns.brouillon.is_file() else None)
    s = semis.seme(mo, ns.semer, ecrire=ns.ecrire, avec_git=True, brouillon=trace)
    return semis.imprime(s, mo, ns.semer.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
