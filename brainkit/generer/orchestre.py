"""orchestre.py — quels generateurs tournent, dans quel ordre, et le rapport.

Trois choix, et ils sont le lot :

1. **Un seul balayage du vault pour les quatre.** Le DevBrain en faisait quatre,
   dont un qui relisait le JSON produit par un autre — donc un vault vieux d une
   execution. Le chainage disparait : `corpus.py` lit une fois, les quatre
   composent.

2. **Le rapport est chiffre, artefact par artefact, a chaque execution.** Pas
   derriere une option. Le critere d acceptation du lot est un `diff` VIDE, et un
   compte global ne le prouve pas : il faut savoir lequel des quatre s ecarte, de
   combien de lignes, et sur quelle page.

3. **Un refus n est pas un ecart.** Une page sans zone AUTO, un manifeste qui ne
   declare pas un fichier de sortie, une sortie posee sous le vault : ce sont des
   REFUS, imprimes a part et comptes a part. Melanger les deux ferait passer un
   generateur qui n a pas tourne pour un generateur qui a trouve le vault
   conforme — c est la meme leçon que « une regle absente ressemble a une regle
   satisfaite ».
"""

from __future__ import annotations

from pathlib import Path

from . import bandeau, hubs, index, liens
from .corpus import Corpus, charge_corpus
from .prose import Prose
from .sortie import CHECK, ECRIRE, IDENTIQUE, Sortie
from ..valider.manifeste import Modele

# Les quatre, dans l ordre. Ferme par le kit : un artefact est du code.
ARTEFACTS = ("index", "hubs", "liens", "bandeau")


def genere_tout(mo: Modele, racine: Path, mode: str = CHECK,
                dossier: Path | None = None,
                quoi: tuple[str, ...] = ARTEFACTS,
                corpus: Corpus | None = None) -> Sortie:
    s = Sortie(racine=racine, mode=mode, dossier=dossier)
    if s.refus:
        return s
    c = corpus if corpus is not None else charge_corpus(mo, racine)
    p = Prose(mo)
    for a in ARTEFACTS:
        if a not in quoi:
            continue
        if a == "index":
            index.genere(c, p, s)
        elif a == "hubs":
            hubs.genere(c, p, s)
        elif a == "liens":
            liens.genere(c, p, s)
        elif a == "bandeau":
            bandeau.genere(c, s, s.trous)
    s.corpus = c
    return s


# --------------------------------------------------------------------------- #
def imprime(s: Sortie, mo: Modele, racine: Path, detail: int = 12) -> int:
    """Le rapport. Sort en 2 s il reste un ecart en mode `check`, 1 sur un refus."""
    c = s.corpus
    n_pages = len(c.pages) if isinstance(c, Corpus) else 0
    print(f"générer ({s.mode}) — {n_pages} page(s) lue(s) — vault "
          f"`{racine.name}`, manifeste "
          f"`{mo.chemin.name if mo.chemin else '(inconnu)'}`")
    if s.dossier is not None:
        print(f"  sortie : {s.dossier}")

    for a, (poses, ecarts, lignes) in s.par_artefact().items():
        etat = "concorde" if not ecarts else f"{ecarts} écart(s), {lignes} ligne(s)"
        print(f"  {a or '(sans artefact)':10s} · {poses:4d} artefact(s) — {etat}")

    trous = s.trous
    if trous:
        print(f"\n  {len(trous)} bandeau(x) à cellule vide — champ absent du "
              f"frontmatter :")
        for t in trous[:detail]:
            print(f"    - {t}")
        if len(trous) > detail:
            print(f"    … {len(trous) - detail} autre(s)")

    ecarts = s.ecarts()
    if ecarts:
        print(f"\n{len(ecarts)} artefact(s) en écart :")
        for p in ecarts[:detail]:
            print(f"  [{p.etat}] {p.chemin} ({p.lignes} ligne(s) de diff)")
            for l in p.extrait.splitlines():
                print(f"      {l}")
        if len(ecarts) > detail:
            print(f"  … {len(ecarts) - detail} autre(s)")

    if s.refus:
        print(f"\n{len(s.refus)} refus :")
        for r in s.refus:
            print(f"  [REFUS] {r}")

    if s.refus:
        return 1
    if ecarts:
        # Code 2, comme le `--check` du DevBrain : « il reste quelque chose a
        # regenerer » n est pas la meme chose qu une erreur d execution.
        return 2
    n = sum(1 for p in s.poses if p.etat != IDENTIQUE)
    if s.mode == ECRIRE:
        print(f"\nOK — {n} artefact(s) écrit(s), "
              f"{len(s.poses) - n} déjà à jour.")
    else:
        print(f"\nOK — les {len(s.poses)} artefacts concordent avec le vault.")
    return 0
