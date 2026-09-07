"""hubs.py — les zones AUTO des hubs, les axes transverses, les hubs de ralliement.
Remplace `build_mocs.py`.

# L arbitrage du lot : TROIS formes de zone AUTO, et AUCUN gabarit de plus

Le lot 2 a mesure trois formes dans les 74 hubs du DevBrain et laisse la question
ouverte : « un role porte-t-il plusieurs gabarits de zone AUTO, ou la forme se
derive-t-elle du perimetre ? »

**Elle se derive du perimetre, et le perimetre se lit sur le DOSSIER du hub.**

| forme       | perimetre | comment le generateur la reconnait                        | DevBrain |
|---|---|---|---|
| arbre       | `dossier` | le cas general                                            | 67 |
| transverse  | `champ`   | le dossier de tete est un `axes.transverses[].dossier`    | 6  |
| ralliement  | `role`    | le dossier de tete est un `roles[].hub_de_ralliement.dossier` | 1 |

Trois raisons de trancher ainsi, et la troisieme est la vraie :

1. **La forme n est pas une propriete du role.** Les 74 pages portent le meme
   `role: hub`. Un role qui declarerait trois gabarits obligerait chaque page a
   dire lequel s applique — donc a stocker dans le frontmatter ce que le chemin
   dit deja.
2. **Rien de neuf n est declare.** `axes.transverses[].dossier` et
   `roles[].hub_de_ralliement.dossier` existaient AVANT ce lot, parce que le
   dossier appartient a l axe ou au role qui le peuple, pas au hub qui l habite.
   La forme se deduit donc de declarations qui sont deja la, et pour une autre
   raison qu elle.
3. **Trois gabarits sur le role, ce serait la meme information a deux endroits** —
   exactement le defaut que le manifeste existe pour supprimer (constat E4 : les
   cinq gabarits de `Templates/` ont pris du retard sur les 337 pages qu ils
   decrivaient, parce que deux sources decrivaient le meme gabarit).

Ce que le role declare, lui, c est l UNIQUE gabarit de la forme arbre : ses
sous-sections, dans l ordre, chacune avec son perimetre (`depuis:`). Les deux
autres formes n ont pas de sous-sections a declarer — l une groupe par valeur
d axe, l autre par segment de chemin, et les deux tirent leurs sous-titres du
vault.

# Ce qui a ete jete

`MOC_CONCEPT`, `CONCEPT_LABEL`, `WIKI_LABEL`, `wiki_group()`, le parametre
`scope` d `upsert()` et sa branche `indexe:` — l etage `MOC/Concepts/` du
DevBrain, mort avec le dossier `Wiki/` au lot 4 de sa migration. Plus la
detection de fin de ligne `nl = "\\r\\n" if ... else "\\n"`, qui ne pouvait jamais
rendre `\\r\\n` : le texte compare est lu en fins de ligne universelles (cf.
`sortie.py`).

Et le CHAINAGE : `build_mocs.py` refusait de tourner sans le JSON produit par
`build_index.py`, et lisait donc un vault vieux d une execution. Les hubs se
composent maintenant du meme corpus que l index, dans la meme passe.
"""

from __future__ import annotations

import collections
from pathlib import Path

from . import corpus as _corpus
from . import zone
from ..valider.manifeste import GENRE_AUTO, Modele
from .prose import Prose
from .sortie import Sortie

ARTEFACT = "hubs"

# Les perimetres qu une sous-section de la forme ARBRE peut declarer. Ferme par
# le kit : un perimetre est du code, pas une donnee.
DEPUIS_SOUS_DOSSIERS = "sous_dossiers"
DEPUIS_ROLE = "role"
DEPUIS_VUES = "vues"

# Les TROIS formes de zone AUTO. Fermees par le kit : une forme est du code. Le
# manifeste ne les nomme pas — la forme se DERIVE du dossier du hub, cf. le
# docstring ci-dessus.
FORME_ARBRE = "arbre"
FORME_TRANSVERSE = "transverse"
FORME_RALLIEMENT = "ralliement"


# --------------------------------------------------------------------------- #
#  La declaration
# --------------------------------------------------------------------------- #
def section_auto(mo: Modele) -> dict | None:
    """La section `genre: auto` du role `fonction: hub` — l unique gabarit declare."""
    rid = mo.role_hub
    if rid is None:
        return None
    return mo.section_de_genre(rid, GENRE_AUTO)


def balises(mo: Modele) -> list[str] | None:
    s = section_auto(mo)
    b = (s or {}).get("balises")
    return list(b) if b and len(b) == 2 else None


def dossiers_transverses(mo: Modele) -> dict[str, dict]:
    """{dossier : l axe transverse qui le peuple}."""
    return {t["dossier"]: t for t in mo.transverses if t.get("dossier")}


def dossiers_de_ralliement(mo: Modele) -> dict[str, str]:
    """{dossier : le role dont c est le hub de ralliement}."""
    out: dict[str, str] = {}
    for rid, r in mo.roles.items():
        d = (r.get("hub_de_ralliement") or {}).get("dossier")
        if d:
            out[d] = rid
    return out


# --------------------------------------------------------------------------- #
#  Forme ARBRE — perimetre : le dossier
# --------------------------------------------------------------------------- #
def zone_arbre(corpus: _corpus.Corpus, prose: Prose, hub: str) -> list[str]:
    """Les lignes de la zone AUTO d un hub d arbre : ses sous-dossiers, puis SES pages.

    Le perimetre est le DOSSIER, pas une requete sur la valeur d axe — c est tout
    l interet de l arborescence : le voisinage d une page est `ls` de son
    dossier, il ne se devine plus. Les pages d un sous-dossier sont listees par
    le hub de ce sous-dossier, jamais deux fois.
    """
    mo = corpus.mo
    dossier = hub.rsplit("/", 1)[0] if "/" in hub else ""
    stem_du_hub = Path(hub).stem
    absolu = corpus.racine / dossier
    lignes: list[str] = []

    ici = [e for e in corpus.entrees
           if e["path"].rsplit("/", 1)[0] == dossier
           and corpus.stem(e) != stem_du_hub]

    for sec in (section_auto(mo) or {}).get("sections") or []:
        titre = sec["titre"]
        depuis = sec.get("depuis")
        if depuis == DEPUIS_SOUS_DOSSIERS:
            sous = _sous_dossiers_a_hub(corpus, dossier, absolu)
            if sous:
                sep = sec.get("separateur") or " · "
                lignes += [f"### {titre}",
                           "- " + sep.join(f"[[{s}]]" for s in sous), ""]
        elif depuis == DEPUIS_ROLE:
            rid = sec.get("role")
            membres = sorted((e for e in ici
                              if e.get(corpus.champ_role) == rid),
                             key=lambda e: corpus.nom(e).lower())
            if membres:
                lignes += [f"### {titre}"] + [_puce(corpus, e) for e in membres]
                lignes.append("")
        elif depuis == DEPUIS_VUES:
            vues = _vues_du_dossier(mo, absolu)
            if vues:
                lignes += [f"### {titre}"] + [f"- [[{v}]]" for v in vues] + [""]
        # Une sous-section sans `depuis:` n est pas remplie AU HASARD : elle est
        # ignoree, et le rapport le dit une fois pour le manifeste entier.
    return lignes or [prose.ligne("hubs.dossier_vide")]


def _sous_dossiers_a_hub(corpus: _corpus.Corpus, dossier: str,
                         absolu: Path) -> list[str]:
    """Les sous-dossiers qui portent leur propre hub, tries par nom de dossier."""
    out: list[str] = []
    if not absolu.is_dir():
        return out
    for sd in sorted(d for d in absolu.iterdir() if d.is_dir()):
        fils = f"{dossier}/{sd.name}/{sd.name}.md" if dossier else f"{sd.name}/{sd.name}.md"
        p = corpus.par_chemin.get(fils)
        if p is not None and p.role == corpus.mo.role_hub:
            out.append(sd.name)
    return out


def _vues_du_dossier(mo: Modele, absolu: Path) -> list[str]:
    """Les fichiers de vue embarquee du dossier, par leur nom sans extension.

    ANOMALIE REPRODUITE, non corrigee. Cette sous-section lit une EXTENSION de
    fichier la ou toutes les autres lisent un `role:` — la page `fonction: vue`
    existe a cote de son fichier de vue depuis le lot 5 du DevBrain, et c est
    elle qui devrait etre listee. Le lot 2 a mesure que la bijection tient
    aujourd hui (47 pages, 47 fichiers, ses controles C8 et A17 a zero), donc la
    difference ne s observe pas ; le premier des deux qui manquera la reveillera.
    Corriger ici couterait le `diff` vide du critere d acceptation, et « ne
    corrige aucun artefact qui te paraitrait mal forme » est l interdiction du
    lot. Cf. `design/04-generation.md`, Remontees.
    """
    ext = mo.extension_de_vue()
    if not ext or not absolu.is_dir():
        return []
    return sorted(f.stem for f in absolu.glob(f"*{ext}"))


def _puce(corpus: _corpus.Corpus, e: dict) -> str:
    desc = corpus.descripteur(e, avec_alias=False, vide="")
    return f"- {corpus.lien(e)}" + (f" — {desc}" if desc else "")


# --------------------------------------------------------------------------- #
#  Forme RALLIEMENT — perimetre : un role
# --------------------------------------------------------------------------- #
def zone_ralliement(corpus: _corpus.Corpus, prose: Prose, rid: str) -> list[str]:
    """Les pages d un role disperse dans l arbre, groupees par dossier de tete.

    Le defaut que ce hub repare : une page dispersee n est reliee qu a ses
    voisins, donc noyee dans la grappe de son dossier. Ce qui fait une galaxie
    dans un graphe, c est une page que tous citent et qui les cite tous — le lien
    retour est ecrit dans chaque page, cette liste est l aller.

    Le groupe est le PREMIER SEGMENT du chemin, jamais le sous-dossier : sinon ce
    hub redoublerait l arbre au lieu de le traverser, et la vingtaine de groupes
    deviendrait une cinquantaine.
    """
    par_tete: dict[str, list[dict]] = {}
    for e in corpus.entrees:
        if e.get(corpus.champ_role) != rid:
            continue
        par_tete.setdefault(e["path"].split("/")[0], []).append(e)
    lignes: list[str] = []
    for tete, membres in sorted(par_tete.items()):
        lignes.append(f"### {tete}")
        lignes += [f"- {corpus.lien(e)}"
                   for e in sorted(membres, key=lambda e: corpus.nom(e).lower())]
        lignes.append("")
    return lignes or [prose.ligne("hubs.aucune_page", role=rid)]


# --------------------------------------------------------------------------- #
#  Forme TRANSVERSE — perimetre : un champ
# --------------------------------------------------------------------------- #
def hubs_transverses(corpus: _corpus.Corpus, prose: Prose,
                     axe: dict) -> list[tuple[str, str, str, list[str]]]:
    """(chemin, titre, intro, puces) par valeur PORTEE de l axe — la boucle de la rupture 4.

    Le DevBrain n a qu un axe transverse et `build_mocs.py` le codait en dur :
    une constante de dossier, une table de libelles, une boucle. Un brain
    d histoire en veut deux (`Themes/` et `Espaces/`), un brain de domaine client
    sans doute trois. La boucle est ici, l appelant itere sur
    `axes.transverses[]`, et ZERO axe est legal — le generateur ne cree alors
    aucun dossier.

    Une valeur declaree que personne ne porte ne produit AUCUN hub : le vault
    n aurait rien a y montrer, et une page vide dans un graphe est un noeud de
    plus qui ne rassemble rien.
    """
    champ = axe["champ"]
    dossier = axe["dossier"]
    libelles = {v["cle"]: v.get("libelle") or v["cle"]
                for v in (axe.get("valeurs") or [])}
    mot = prose.libelle_transverse(champ)

    # {valeur : {dossier de tete : compte}}. Les hubs sont exclus : ils portent
    # eux aussi le champ et se compteraient eux-memes.
    groupes: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter)
    for e in corpus.entrees:
        if e.get(corpus.champ_role) == corpus.mo.role_hub:
            continue
        tete = e["path"].split("/")[0]
        for v in e.get(champ) or []:
            groupes[str(v)][tete] += 1

    out: list[tuple[str, str, str, list[str]]] = []
    for valeur in sorted(groupes):
        titre = libelles.get(valeur, valeur)
        intro = prose.ligne("transverse.intro", axe_transverse=mot,
                            libelle=titre, cle=valeur)
        puces = [prose.ligne("transverse.puce", cible=tete, n=n)
                 for tete, n in sorted(groupes[valeur].items(),
                                       key=lambda kv: (-kv[1], kv[0]))]
        out.append((f"{dossier}/{titre}.md", titre, intro, puces))
    return out


# --------------------------------------------------------------------------- #
#  L orchestration
# --------------------------------------------------------------------------- #
def genere(corpus: _corpus.Corpus, prose: Prose, s: Sortie) -> None:
    mo = corpus.mo
    bal = balises(mo)
    if bal is None:
        s.refuse("le rôle `fonction: hub` ne déclare aucune section `genre: auto` "
                 "avec ses deux balises — aucune zone AUTO à générer")
        return
    transverses = dossiers_transverses(mo)
    ralliements = dossiers_de_ralliement(mo)

    # --- les hubs de l arbre et les hubs de ralliement -------------------- #
    for p in corpus.lisibles:
        if p.role != mo.role_hub:
            continue
        tete = p.chemin.split("/")[0]
        if tete in transverses:
            continue            # rempli par la boucle transverse, pas par `ls`
        if tete in ralliements:
            forme = FORME_RALLIEMENT
            lignes = zone_ralliement(corpus, prose, ralliements[tete])
        else:
            forme = FORME_ARBRE
            lignes = zone_arbre(corpus, prose, p.chemin)
        texte = p.absolu.read_text(encoding="utf-8")
        if not zone.porte_une_zone(texte, bal):
            s.refuse(f"{p.chemin} : aucune zone {bal[0]}/{bal[1]} — hub non rempli")
            continue
        bloc = zone.bloc(bal, "\n".join(lignes).rstrip())
        s.pose(p.chemin, zone.remplace(texte, bal, bloc), ARTEFACT, forme)

    # --- un hub par valeur portee de chaque axe transverse ---------------- #
    for axe in mo.transverses:
        if not axe.get("hub_par_valeur", True):
            continue
        for rel, titre, intro, puces in hubs_transverses(corpus, prose, axe):
            # La forme transverse ne se rstrippe PAS et porte sa phrase d intro
            # suivie d une ligne vide : c est la forme du vault, reproduite.
            bloc = (f"{bal[0]}\n{intro}\n\n" + "\n".join(puces) + f"\n{bal[1]}")
            avant = s.lit(rel)
            if avant is None:
                s.pose(rel, _hub_neuf(corpus, titre, intro, bloc), ARTEFACT,
                       FORME_TRANSVERSE)
                continue
            if not zone.porte_une_zone(avant, bal):
                s.refuse(f"{rel} : aucune zone {bal[0]}/{bal[1]} — hub non rempli")
                continue
            s.pose(rel, zone.remplace(avant, bal, bloc), ARTEFACT,
                   FORME_TRANSVERSE)


def _hub_neuf(corpus: _corpus.Corpus, titre: str, intro: str, bloc: str) -> str:
    """Un hub transverse qui n existe pas encore : frontmatter minimal et sa zone.

    Les champs sont ceux que le manifeste EXIGE du role hub, et rien de plus : un
    champ hors du gabarit ferait refuser la page par le validateur, ce qui est
    arrive au DevBrain avec un `indexe:` survivant d une v2.
    """
    mo = corpus.mo
    rid = mo.role_hub or "hub"
    lignes = ["---", f"{corpus.champ_role}: {rid}"]
    for champ in mo.requis(rid):
        if champ == corpus.champ_role:
            continue
        if champ == corpus.champ_identite:
            lignes.append(f"{champ}: {titre}")
        elif champ == corpus.champ_resume:
            lignes.append(f"{champ}: {intro}")
    lignes += ["---", "", f"# {titre}", "", bloc, ""]
    return "\n".join(lignes)
