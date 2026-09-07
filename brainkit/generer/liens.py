"""liens.py — la carte des liens, des mots-cles et des SUJETS A CREER. Remplace `build_links.py`.

Trois sections, et c est la troisieme qui compte. Les deux premieres decrivent le
graphe tel qu il est : par page, ses mots-cles, ce qu elle cite, ce qui la cite.
La troisieme decrit ce qui MANQUE — les liens qui ne resolvent pas, et les
mots-cles qu aucune page ne definit. C est un mecanisme de backlog qui ne
suppose rien du sujet : un lien mort et un mot-cle orphelin sont des trous dans
n importe quel brain.

# Ce qu est un lien MORT, et ce qu il n est pas

Une cible est resolue si elle nomme une page indexee (par son nom ou par son nom
de fichier) OU un fichier resolvable du vault. La seconde branche existe pour une
raison mesuree : la syntaxe d embed d une vue porte une EXTENSION
(`![[X.base]]`), seule syntaxe qui vise un fichier non-Markdown, et sans elle les
47 vues du DevBrain comptaient comme autant de liens morts — alors que la cloture
du vault exige zero.

Le balayage des cibles resolvables porte sur TOUT le vault, gouvernance et
gabarits compris : un lien vers un document de gouvernance est un lien vivant,
meme si le document n est pas une page indexee.

# Ce qui a ete jete

Le jeu `V1` de treize champs herites et le filtre `active()` qui s en servait
pour ecarter un « reservoir » vivant sous un dossier `Wiki/` supprime au lot 4
de la migration du DevBrain — meme dette que dans l index, meme raison de ne pas
la porter (§5.10).
"""

from __future__ import annotations

import unicodedata

from . import corpus as _corpus
from ..valider import vault
from .prose import Prose
from .sortie import Sortie

ARTEFACT = "liens"


def _decl(corpus: _corpus.Corpus) -> dict:
    return (corpus.mo.m.get("genere") or {}).get("liens") or {}


def ardoise(s: str) -> str:
    """La forme comparable d un mot-cle et d un nom de page.

    Un mot-cle est en kebab-case sans accent, un nom de page ne l est pas :
    « Séries temporelles » et `series-temporelles` designent la meme chose et
    doivent se reconnaitre. La normalisation est donc : sans diacritique, en
    minuscules, espaces et soulignes en tirets.
    """
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return s.lower().strip().replace(" ", "-").replace("_", "-")


# --------------------------------------------------------------------------- #
def document(corpus: _corpus.Corpus, prose: Prose) -> str:
    mo = corpus.mo
    signature = str(_decl(corpus).get("signature") or "")

    # --- les pages, dans l ordre du corpus (par chemin) ------------------- #
    fiches: list[dict] = []
    for p, e in zip(corpus.lisibles, corpus.entrees):
        fiches.append({
            "nom": corpus.nom(e),
            "stem": p.stem,
            "role": e.get(corpus.champ_role),
            "tags": [str(t) for t in (e.get(corpus.champ_tags) or [])]
                    if corpus.champ_tags else [],
            "alias": [str(a) for a in (e.get(corpus.champ_alias) or [])]
                     if corpus.champ_alias else [],
            "sortants": [t.strip().split("/")[-1] for t in p.liens_du_corps()],
        })

    # Deux cles par page — son nom et son nom de fichier. En cas de collision,
    # la DERNIERE dans l ordre de chemin gagne, comme dans l ancien code : le
    # vault n a plus de collision de nom depuis son lot 3, et en inventer une
    # resolution differente changerait un compte sans qu aucune faute existe.
    par_nom: dict[str, dict] = {}
    for f in fiches:
        par_nom[f["nom"].lower()] = f
        par_nom[f["stem"].lower()] = f

    extensions = [".md"]
    ext = mo.extension_de_vue()
    if ext and ext not in extensions:
        extensions.append(ext)
    resolvables = vault.fichiers_du_vault(corpus.racine, extensions)

    entrants: dict[str, set[str]] = {f["nom"]: set() for f in fiches}
    morts: list[tuple[str, str]] = []
    for f in fiches:
        res: list[str] = []
        for t in f["sortants"]:
            cle = t.lower()
            if cle in par_nom:
                nm = par_nom[cle]["nom"]
                res.append(nm)
                entrants[nm].add(f["nom"])
            elif cle in resolvables:
                res.append(t)          # cible valide non-page (une vue embarquee)
            else:
                morts.append((f["nom"], t))
        f["resolus"] = sorted(set(res))

    # --- les mots-cles ---------------------------------------------------- #
    par_tag: dict[str, list[str]] = {}
    for f in fiches:
        for t in f["tags"]:
            par_tag.setdefault(t, []).append(f["nom"])

    # Un mot-cle est COUVERT quand une page dont la fonction est d expliquer
    # porte son nom ou l un de ses alias. C est la `fonction: notion` du
    # manifeste, jamais un nom de role en dur.
    roles_a_comprendre = set(mo.roles_de_fonction("notion"))
    couverts: set[str] = set()
    for f in fiches:
        if f["role"] in roles_a_comprendre:
            couverts.add(ardoise(f["nom"]))
            couverts.update(ardoise(a) for a in f["alias"])

    # --- le document ------------------------------------------------------ #
    vide = prose.ligne("liens.vide")
    L = [f"# {prose.ligne('liens.titre')}", ""]
    L += [f"> {l}" for l in prose.lignes("liens.entete", signature=signature,
                                         pages=len(fiches))]
    L += ["", f"## {prose.ligne('liens.par_page')}", ""]
    for f in sorted(fiches, key=lambda e: (e["role"] or "", e["nom"].lower())):
        L.append(f"### {f['nom']}  ·  {f['role']}")
        L.append(f"- {prose.ligne('liens.etiquette_tags')} : "
                 + (", ".join("`" + t + "`" for t in f["tags"]) or vide))
        L.append(f"- {prose.ligne('liens.etiquette_sortants')} : "
                 + (", ".join("[[" + x + "]]" for x in f["resolus"]) or vide))
        L.append(f"- {prose.ligne('liens.etiquette_entrants')} : "
                 + (", ".join("[[" + x + "]]" for x in sorted(entrants[f["nom"]]))
                    or vide))
        L.append("")

    L += [f"## {prose.ligne('liens.tags_vers_pages')}", ""]
    for t in sorted(par_tag):
        drapeau = "" if ardoise(t) in couverts else prose.ligne("liens.sans_page")
        L.append(f"- `{t}` : {', '.join(sorted(set(par_tag[t])))}{drapeau}")

    L += ["", f"## {prose.ligne('liens.a_creer')}", "",
          prose.ligne("liens.non_resolus")]
    L += [prose.ligne("liens.non_resolu", page=a, cible=b)
          for a, b in sorted(set(morts))] or [prose.ligne("liens.aucun")]
    L += ["", prose.ligne("liens.tags_sans_page")]
    manquants = sorted(t for t in par_tag if ardoise(t) not in couverts)
    L += [prose.ligne("liens.tag_porte_par", tag=t,
                      pages=", ".join(sorted(set(par_tag[t]))))
          for t in manquants] or [prose.ligne("liens.aucun")]

    return "\n".join(L).rstrip() + "\n"


# --------------------------------------------------------------------------- #
def genere(corpus: _corpus.Corpus, prose: Prose, s: Sortie) -> None:
    fichier = _decl(corpus).get("fichier")
    if not fichier:
        s.refuse("`genere.liens.fichier` non déclaré — rien à générer")
        return
    s.pose(str(fichier), document(corpus, prose), ARTEFACT)
