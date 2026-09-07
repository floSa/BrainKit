"""index.py — le catalogue machine et le document humain. Remplace `build_index.py`.

Deux sorties, une source. Le JSON est lu par les skills, le Markdown par floSa.
Ils ne divergent pas parce qu ils sont composes du meme jeu d entrees, dans le
meme ordre.

# Ce qui rend le `diff` vide possible : ordre stable, aucun horodatage

`genere.index.tri: stable` et `horodatage: false` ne sont pas des options de
confort. Deux regenerations d un vault inchange doivent produire le MEME octet,
sans quoi le critere d acceptation du lot — un `diff` vide contre les artefacts
du vault — serait inatteignable, et la regle « ce qui est genere se verifie »
n aurait aucun sens.

L ordre est donc : les entrees par CHEMIN, les groupes du document humain dans
l ordre declare, et a l interieur d un groupe par valeur d axe puis par nom en
minuscules.

# Ce qui a ete jete

`is_active_v2()` et `V1_MARKERS` — treize noms de champs de la v1 du DevBrain,
qui servaient a ecarter de l index un « reservoir » de pages vivant sous un
dossier `Wiki/` supprime au lot 4 de sa migration. Le filtre rend `True` pour
toute page depuis ce jour, et le compte qu il alimentait sort a zero. Porter ce
code dans le kit aurait porte la dette du DevBrain dans TOUTES les instances
(§5.10). La seule trace qui reste est une ligne d en-tete que le manifeste
declare, parce qu elle est dans le fichier du vault : cf. `prose.py`.
"""

from __future__ import annotations

import json

from . import corpus as _corpus
from .prose import Prose
from .sortie import Sortie

ARTEFACT = "index"


def _decl(corpus: _corpus.Corpus) -> dict:
    return (corpus.mo.m.get("genere") or {}).get("index") or {}


def _fichiers(corpus: _corpus.Corpus) -> tuple[str | None, str | None]:
    """(le JSON, le Markdown) — reconnus par leur EXTENSION, pas par leur rang.

    `genere.index.fichiers` est une liste ; se fier a l ordre ferait dependre le
    catalogue machine d une virgule.
    """
    js = md = None
    for f in _decl(corpus).get("fichiers") or []:
        if f.endswith(".json"):
            js = f
        elif f.endswith(".md"):
            md = f
    return js, md


# --------------------------------------------------------------------------- #
#  Le catalogue machine
# --------------------------------------------------------------------------- #
def index_des_mots_cles(corpus: _corpus.Corpus) -> dict[str, list[str]]:
    """{mot-cle : les pages qui le portent}, trie, sans doublon."""
    if not corpus.champ_tags:
        return {}
    ti: dict[str, list[str]] = {}
    for e in corpus.entrees:
        for t in e.get(corpus.champ_tags) or []:
            ti.setdefault(str(t), []).append(corpus.nom(e))
    return {t: sorted(set(v)) for t, v in sorted(ti.items())}


def catalogue(corpus: _corpus.Corpus) -> str:
    decl = _decl(corpus)
    doc: dict = {"generated_by": str(decl.get("signature") or "")}
    doc["scanned"] = corpus.scannes
    portee = decl.get("portee")
    if portee:
        # Emise seulement si le manifeste la declare. Un brain neuf n a aucune
        # reserve de perimetre a annoncer, et une cle vide en inventerait une.
        doc["scope"] = str(portee)
    doc["count"] = len(corpus.entrees)
    doc["tags_index"] = index_des_mots_cles(corpus)
    doc["pages"] = [corpus.colonnes_publiees(e) for e in corpus.entrees]
    return json.dumps(doc, ensure_ascii=False, indent=2) + "\n"


# --------------------------------------------------------------------------- #
#  Le document humain
# --------------------------------------------------------------------------- #
def groupes(corpus: _corpus.Corpus) -> tuple[list[str], dict[str, str]]:
    """(l ordre des roles, leur titre) — declares, puis les autres par ordre alphabetique.

    Un role que `genere.index.groupes` ne nomme pas n est pas ecarte : il sort
    APRES les declares, sous son propre identifiant. Une page hors des groupes
    prevus doit se voir — c est ce qui fait apparaitre les 74 hubs sous un
    `## hub` sans titre redige, et c est un fait du vault, pas un oubli du
    generateur.
    """
    ordre: list[str] = []
    titres: dict[str, str] = {}
    for g in _decl(corpus).get("groupes") or []:
        ordre.append(g["role"])
        titres[g["role"]] = g.get("titre") or g["role"]
    return ordre, titres


def document(corpus: _corpus.Corpus, prose: Prose, signature: str) -> str:
    ordre, titres = groupes(corpus)
    lignes = [f"# {prose.ligne('index.titre')}", ""]
    lignes += [f"> {l}" for l in prose.lignes("index.entete",
                                              signature=signature,
                                              pages=len(corpus.entrees))]
    lignes.append("")

    par_role: dict[str, list[dict]] = {}
    for e in corpus.entrees:
        par_role.setdefault(str(e.get(corpus.champ_role) or "?"), []).append(e)

    champ_axe = corpus.mo.champ_rangement
    sans = prose.ligne("index.sans_valeur")
    vide = prose.ligne("index.vide")
    for role in sorted(par_role, key=lambda r: (ordre.index(r) if r in ordre
                                                else len(ordre) + 1, r)):
        lignes += [f"## {titres.get(role, role)}", ""]
        par_axe: dict[str, list[dict]] = {}
        for e in par_role[role]:
            par_axe.setdefault(str(e.get(champ_axe) or sans), []).append(e)
        for valeur in sorted(par_axe):
            lignes.append(f"### {valeur}")
            for e in sorted(par_axe[valeur], key=lambda x: corpus.nom(x).lower()):
                desc = corpus.descripteur(e, avec_alias=True, vide=vide)
                lignes.append(f"- **{corpus.nom(e)}** — {desc}")
            lignes.append("")
    return "\n".join(lignes).rstrip() + "\n"


# --------------------------------------------------------------------------- #
def genere(corpus: _corpus.Corpus, prose: Prose, s: Sortie) -> None:
    js, md = _fichiers(corpus)
    signature = str(_decl(corpus).get("signature") or "")
    if not js and not md:
        s.refuse("`genere.index.fichiers` ne déclare ni JSON ni Markdown — "
                 "rien à générer")
        return
    if js:
        s.pose(js, catalogue(corpus), ARTEFACT)
    if md:
        s.pose(md, document(corpus, prose, signature), ARTEFACT)
