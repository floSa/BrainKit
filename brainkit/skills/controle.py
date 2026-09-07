"""controle.py — le rayon, CONFRONTE a un vault reel.

La clause « une ligne sans objet se declare sans objet, elle ne se tait pas » est
la seule chose que le skill de capture porte et qu aucun validateur ne controle.
Ce module la rend MECANIQUE : pour une page capturee et un ensemble de fichiers
touches, il dit, ligne par ligne, laquelle est HONOREE, laquelle est SANS OBJET,
et laquelle est TUE.

    uv run brainkit/skills/controle.py --vault . --page "<chemin de la page>"

# Ce qu il controle, et ce qu il ne controle PAS

Il ne controle que les lignes **a ecrire**. Les lignes generees — les hubs, les
hubs transverses — sont deleguees : `brainkit generer --check` et la regle
`completude_du_hub` les tiennent deja, et exiger qu on les « touche » ferait
sortir un faux defaut a chaque capture.

Ce qu il ne peut pas controler non plus, et il le dit : la QUALITE de ce qui a
ete ecrit. Qu un pair ait ete touche ne prouve pas que la reciprocite est bonne
— c est `brainkit valider --regle reciprocite` qui le dit. Les deux se
completent : celui-ci trouve les OUBLIS, l autre trouve les ERREURS.

# Pourquoi ce n est pas une regle du validateur

Parce qu il faut savoir CE QUI VIENT D ETRE CAPTURE, et un validateur ne le sait
pas : il voit un vault, pas une session. La liste des fichiers touches vient de
`git status --porcelain` — c est-a-dire du travail en cours, pas du vault. Un
vault ou toutes les lignes ont ete tues depuis six mois est un vault avec de la
dette, pas un vault invalide.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[2]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit import defauts                                        # noqa: E402
from brainkit.valider import vault                                  # noqa: E402
from brainkit.valider.manifeste import Modele, charge               # noqa: E402
from brainkit.skills import propagation as P                        # noqa: E402

HONOREE, SANS_OBJET, TUE, DELEGUEE = "honorée", "sans objet", "TUE", "déléguée"


@dataclass
class Constat:
    ligne: P.Ligne
    etat: str
    objets: list[str] = field(default_factory=list)
    touches: list[str] = field(default_factory=list)
    detail: str = ""


@dataclass
class Rapport:
    page: str
    dossier: str
    role: str | None
    constats: list[Constat] = field(default_factory=list)

    @property
    def tues(self) -> list[Constat]:
        return [c for c in self.constats if c.etat == TUE]

    @property
    def code(self) -> int:
        return 1 if self.tues else 0


def touches_par_git(racine: Path) -> set[str]:
    """Ce que `git status --porcelain` declare modifie, ajoute ou renomme.

    C est la seule source honnete de « ce qu on vient de faire » : une liste
    tenue a la main par l agent serait exactement la liste des choses dont il se
    souvient, c est-a-dire pas celles qu il a oubliees.
    """
    # `-uall` : sans lui, git replie un dossier entier non suivi en UNE ligne,
    # et un lot de dix pages neuves devient un seul chemin de dossier — le
    # controle declarerait alors TUE tout ce qui est neuf.
    # `core.quotepath=false` : sans lui, tout chemin non-ASCII sort echappe en
    # octal (`Antiquit\303\251/`), et aucune comparaison avec le vault ne tient.
    try:
        sortie = subprocess.run(
            ["git", "-c", "core.quotepath=false", "status", "--porcelain",
             "-uall"],
            cwd=racine, capture_output=True, text=True,
            encoding="utf-8", check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return set()
    out: set[str] = set()
    for ligne in sortie.splitlines():
        chemin = ligne[3:].strip().strip('"')
        if " -> " in chemin:                    # un renommage touche les deux
            avant, apres = chemin.split(" -> ", 1)
            out.update({avant.strip('"'), apres.strip('"')})
        elif chemin:
            out.add(chemin)
    return out


# --------------------------------------------------------------------------- #
def controle(mo: Modele, racine: Path, page: str,
             touches: set[str]) -> Rapport:
    """Le rayon d une capture, confronte au vault et a ce qui a ete touche."""
    pages = vault.lire_vault(racine, mo.non_pages)
    par_chemin = {p.chemin: p for p in pages}
    cible = par_chemin.get(page)
    if cible is None:
        raise SystemExit(f"page introuvable dans le vault : {page}")
    dossier = cible.chemin.rsplit("/", 1)[0] if "/" in cible.chemin else ""
    role = cible.role
    r = Rapport(page=page, dossier=dossier, role=role)
    cr = _champ_role(mo)

    voisins = [p for p in pages
               if (p.chemin.rsplit("/", 1)[0] if "/" in p.chemin else "") == dossier
               and p.chemin != cible.chemin and not p.illisible]

    for li in P.derive(mo, role):
        if not li.a_ecrire:
            r.constats.append(Constat(li, DELEGUEE, detail=(
                "portée par `brainkit generer --check` et par la règle "
                "`completude_du_hub` — pas par ce contrôle")))
            continue
        objets, detail = _objets(mo, li, cible, voisins, cr)
        if not objets:
            r.constats.append(Constat(li, SANS_OBJET, detail=(
                li.sans_objet_si or detail)))
            continue
        vus = [o for o in objets if o in touches]
        r.constats.append(Constat(
            li, HONOREE if vus else TUE, objets=objets, touches=vus,
            detail=detail))
    return r


def _champ_role(mo: Modele) -> str:
    for nom, d in mo.champs.items():
        if str(d.get("source") or "").strip() == "roles[].id":
            return nom
    return "role"


def _objets(mo: Modele, li: P.Ligne, cible, voisins, cr: str) -> tuple[list[str], str]:
    """Les fichiers que CETTE ligne désigne, dans CE vault. Vide = sans objet."""
    if li.genre in (P.G_VOISIN, P.G_PAIRS):
        objets = [p.chemin for p in voisins if p.role == li.role]
        return objets, (f"aucune page `{cr}: {li.role}` dans le dossier"
                        if not objets else
                        f"{len(objets)} page(s) `{cr}: {li.role}` dans le dossier")

    if li.genre == P.G_RESUMES:
        # Les cibles que la page capturee cite dans ses champs a reciprocite.
        # Elles doivent avoir ete touchees : la reinjection est reciproque, donc
        # la puce se pose des DEUX cotes.
        noms: set[str] = set()
        for champ in mo.champs_a_reciprocite():
            noms |= vault.cibles_du_champ(cible.fm, champ)
        if not noms:
            return [], "la page ne cite personne dans ses champs à réciprocité"
        ident = mo.champ_de_fonction("identite") or "nom"
        objets = [p.chemin for p in voisins
                  if str(p.fm.get(ident) or "") in noms]
        return objets, f"{len(objets)} cible(s) citée(s) dans le dossier"

    if li.genre == P.G_RALLIEMENT:
        # Le hub de ralliement n est dans le rayon que si la capture CREE une
        # page du role rallie. L objet a ecrire n est pas le hub — sa zone AUTO
        # est generee — c est le LIEN RETOUR, qui vit dans la page capturee.
        if cible.role != li.role:
            return [], (f"la page capturée n'est pas une `{cr}: {li.role}` : "
                        f"le hub de ralliement n'est pas dans son rayon")
        return [cible.chemin], ("le lien retour se pose DANS la page capturée, "
                                "pas dans le hub")
    return [], "genre de ligne sans objet mécanisable"


# --------------------------------------------------------------------------- #
def imprime(r: Rapport, tout: bool = False) -> int:
    print(f"rayon — `{r.page}` (`{r.role}`), dossier `{r.dossier}`\n")
    for c in r.constats:
        if c.etat == DELEGUEE and not tout:
            continue
        marque = {HONOREE: "OK   ", SANS_OBJET: "     ",
                  TUE: "TUE  ", DELEGUEE: "  ~  "}[c.etat]
        print(f"  {marque} {c.ligne.n:3s} {c.etat:11s} {_court(c.ligne.cible)}")
        if c.objets:
            for o in c.objets:
                print(f"              {'· touché  ' if o in c.touches else '· NON touché '}{o}")
        elif c.detail:
            print(f"              {c.detail}")
    print()
    if r.tues:
        print(f"{len(r.tues)} ligne(s) TUE(S) — le rayon n'est pas honoré :")
        for c in r.tues:
            print(f"  {c.ligne.n} — {_court(c.ligne.cible)} : "
                  f"{len(c.objets)} objet(s), aucun touché")
        print("\nUne ligne sans objet se DÉCLARE sans objet. Une ligne AVEC un "
              "objet et sans travail est un oubli.")
        return 1
    print("OK — chaque ligne du rayon est honorée ou sans objet.")
    return 0


def _court(s: str) -> str:
    for sep in (" — ", " -- "):
        if sep in s:
            s = s.split(sep)[0]
    return s.strip()


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(
        description="Confronte le rayon de propagation à un vault réel.")
    ap.add_argument("--manifeste", type=Path, default=None)
    ap.add_argument("--vault", type=Path, default=None)
    ap.add_argument("--page", required=True,
                    help="le chemin de la page capturée, relatif au vault")
    ap.add_argument("--touche", action="append", default=None,
                    help="un fichier touché (répétable). Défaut : `git status`")
    ap.add_argument("--tout", action="store_true",
                    help="imprimer aussi les lignes déléguées aux générateurs")
    ns = ap.parse_args()

    vaut = ns.vault if ns.vault is not None else defauts.vault_par_defaut()
    if not vaut.is_dir():
        return print(f"vault introuvable : {vaut}") or 2
    manifeste, dits = defauts.resout(ns.manifeste, vaut)
    for ligne in dits:
        print(ligne)
    if manifeste is None or not manifeste.exists():
        return 2
    mo = charge(manifeste)
    racine = vaut.resolve()
    touches = set(ns.touche) if ns.touche else touches_par_git(racine)
    return imprime(controle(mo, racine, ns.page.replace("\\", "/"), touches),
                   tout=ns.tout)


if __name__ == "__main__":
    raise SystemExit(main())
