"""bandeau.py — le haut de page, DERIVE du frontmatter. Remplace `build_bandeau.py`.

C est la brique la plus nettement separee de tout le kit, et le test a blanc du
cadrage l a prouvee : le bandeau du DevBrain est
`Nature | Licence | Execution | Maturite`, celui d un brain d histoire
`Nature | Auteur et date | Langue | Fiabilite`. Quatre colonnes, chacune derivee
d un champ, chacune avec sa table de rendu. **Le moteur ne change pas d une
ligne** — c est ce qui rend I4 (generique) et I5 (a reecrire) deux briques
distinctes et non une seule.

# La regle dure, et elle porte tout le reste

**Une cellule sans source dans le frontmatter affiche le caractere vide, JAMAIS
une valeur plausible.** Une fiche vide honnetement vaut mieux qu une fiche
remplie au juge. Le test porte sur les CELLULES et jamais sur la zone rendue :
le tiret cadratin est aussi un signe de ponctuation courant, et douze resumes du
DevBrain en portent un — chercher le caractere vide dans le TEXTE du bandeau
signalait onze trous inexistants au premier essai.

# La regle 9, portee ici et nulle part ailleurs

`bandeau_a_jour` est la seule des dix regles que le validateur delegue : la
verifier, c est regenerer la zone et comparer les octets, donc posseder le
generateur. Le mode `--check` de ce module EST la regle, et le manifeste le dit
desormais par une declaration (`regles[].porte_par`) et non par convention — cf.
`design/04-generation.md`, arbitrage 2.

# Ce qu une colonne sait faire, et ce qu elle ne devine pas

Une colonne declare une `source:` (un champ), une `table:` (le rendu d une
valeur), un `qualifie_par:` (un second champ accole), une
`exception_qualification:` (une condition ou l on N accole PAS) et un
`depend_de:` (le cas ou la valeur de la source ne suffit pas et ou il faut lire
deux autres champs). Cinq mecanismes, aucun mot de sujet. Une valeur de source
hors de la table rend le caractere vide : elle n est pas absorbee en silence,
parce qu une valeur inconnue est un defaut de vocabulaire et se voit dans le
rapport de trous.
"""

from __future__ import annotations

from . import corpus as _corpus
from . import zone
from ..valider import conditions, vault
from ..valider.manifeste import Modele
from .sortie import Sortie

ARTEFACT = "bandeau"

# La cle de composition d une valeur qui depend de deux champs. Ferme par le kit,
# comme les six fonctions de role : la composition est du code.
CLE_COMPOSITION = "composition"
JETON_PRINCIPAL = "<hosted>"
JETON_SECOND = "<scaling>"


def _decl(mo: Modele) -> dict:
    return mo.bandeau or {}


def balises(mo: Modele) -> list[str] | None:
    b = _decl(mo).get("balises")
    return list(b) if b and len(b) == 2 else None


def vide(mo: Modele) -> str:
    return str(_decl(mo).get("vide") or "—")


# --------------------------------------------------------------------------- #
#  Une cellule
# --------------------------------------------------------------------------- #
def cellule(valeur: str | None, mo: Modele) -> str:
    """Une cellule vide se VOIT. `|` est echappe : il couperait la ligne du tableau."""
    v = (valeur or "").strip()
    return v.replace("|", r"\|") if v else vide(mo)


def rendu_de_colonne(colonne: dict, fm: dict, mo: Modele) -> str:
    """La valeur affichee d une colonne, avant echappement. Chaine vide = pas de source."""
    brut = str(fm.get(colonne["source"]) or "").strip()
    if not brut:
        return ""
    table = colonne.get("table") or {}
    if table:
        if brut in table:
            base = str(table[brut])
        else:
            base = _valeur_dependante(colonne, fm, brut)
            if not base:
                return ""
    else:
        base = brut
    return _qualifie(colonne, fm, base)


def _valeur_dependante(colonne: dict, fm: dict, brut: str) -> str:
    """Le cas ou la valeur de la source ne suffit pas : deux autres champs la disent.

    Dans le DevBrain, trois familles s hebergent et six non : pour les six, la
    reponse est dans la famille elle-meme (la `table:`) ; pour les trois, elle
    est dans `hosted:` puis `scaling:`. C est exactement ce que la regle des
    champs conditionnels a acte en supprimant `hosted:` des 177 paquets qui le
    portaient sans raison.
    """
    dep = colonne.get("depend_de") or {}
    if brut not in (dep.get("familles") or []):
        return ""
    champs = list(dep.get("champs") or [])
    principal = champs[0] if champs else None
    second = champs[1] if len(champs) > 1 else None

    table_p = dep.get("table_hosted") or {}
    valeurs = sorted(vault.valeurs(fm.get(principal))) if principal else []
    base = table_p.get("[" + ", ".join(valeurs) + "]") if valeurs else None
    if base:
        table_s = dict(dep.get("table_scaling") or {})
        composition = table_s.pop(CLE_COMPOSITION, None)
        sec = table_s.get(str(fm.get(second) or "").strip()) if second else None
        if sec and composition:
            return (str(composition).replace(JETON_PRINCIPAL, str(base))
                    .replace(JETON_SECOND, str(sec)))
        return str(base)

    # Le repli : une valeur de source qui s heberge en principe mais dont la
    # page ne porte pas les deux champs. Il est DECLARE, jamais devine — une
    # application de bureau ne porte pas d hebergement, elle porte son systeme,
    # et « ou ca tourne » est exactement la question de la colonne.
    repli = dep.get("repli") or {}
    if repli and conditions.evalue(str(repli.get("si") or ""), fm):
        return str(fm.get(repli["source"]) or "").strip()
    return ""


def _qualifie(colonne: dict, fm: dict, base: str) -> str:
    """Le second champ accole, sauf si une exception DECLAREE l ecarte.

    Une regle qui produit une cellule inutile n est pas uniforme, elle est
    seulement inconditionnelle : pour un service qu on n execute jamais soi-meme,
    le langage d implementation ne fait pas partie de ce que la chose EST.
    L exception est donc inscrite dans le manifeste plutot que devinee.
    """
    champ = colonne.get("qualifie_par")
    if not champ:
        return base
    exc = colonne.get("exception_qualification") or {}
    if exc and conditions.evalue(str(exc.get("si") or ""), fm) is True:
        return base
    q = str(fm.get(champ) or "").strip()
    return f"{base} {q}" if q else base


def cellules(mo: Modele, fm: dict) -> list[str]:
    return [cellule(rendu_de_colonne(c, fm, mo), mo)
            for c in _decl(mo).get("colonnes") or []]


def colonnes_vides(mo: Modele, cells: list[str]) -> list[str]:
    titres = [str(c["titre"]) for c in _decl(mo).get("colonnes") or []]
    v = vide(mo)
    return [t for t, val in zip(titres, cells) if val == v]


# --------------------------------------------------------------------------- #
#  La zone
# --------------------------------------------------------------------------- #
def zone_du_bandeau(mo: Modele, fm: dict, champ_resume: str) -> str:
    """La zone AUTO complete : le resume, puis les faits.

    Le resume est DANS la zone parce qu il vient lui aussi du frontmatter. Le
    laisser dehors aurait cree la seule chose que le manifeste supprime : une
    valeur recopiee a deux endroits, dont l un se perime sans que rien le dise.
    """
    bal = balises(mo)
    titres = [str(c["titre"]) for c in _decl(mo).get("colonnes") or []]
    lignes = [bal[0]]
    if _decl(mo).get("porte_le_resume") and champ_resume:
        resume = " ".join(str(fm.get(champ_resume) or "").split())
        if resume:
            lignes += [f"> {resume}", ""]
    lignes += ["| " + " | ".join(titres) + " |",
               "|" + "---|" * len(titres),
               "| " + " | ".join(cellules(mo, fm)) + " |",
               bal[1]]
    return "\n".join(lignes)


# --------------------------------------------------------------------------- #
def genere(corpus: _corpus.Corpus, s: Sortie,
           trous: list[str] | None = None) -> None:
    mo = corpus.mo
    bal = balises(mo)
    porte_par = list(_decl(mo).get("porte_par") or [])
    if bal is None or not porte_par:
        s.refuse("`bandeau.balises` ou `bandeau.porte_par` non déclaré — "
                 "aucun bandeau à générer")
        return
    for p in corpus.lisibles:
        if p.role not in porte_par:
            continue
        texte = p.absolu.read_text(encoding="utf-8")
        cells = cellules(mo, p.fm)
        manque = colonnes_vides(mo, cells)
        if manque and trous is not None:
            # SIGNALE, jamais comble : une cellule vide dit qu un champ manque au
            # frontmatter, et c est une information. La remplir au juge l effacerait.
            trous.append(f"{p.chemin} — {', '.join(manque)}")
        neuf, motif = zone.applique(texte, bal,
                                    zone_du_bandeau(mo, p.fm, corpus.champ_resume))
        if neuf is None:
            if motif:
                s.refuse(f"{p.chemin} : {motif} — bandeau non posé")
            else:
                s.pose(p.chemin, texte, ARTEFACT)     # deja exact
            continue
        s.pose(p.chemin, neuf, ARTEFACT)
