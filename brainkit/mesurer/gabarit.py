"""gabarit.py — le taux d occupation des sections. La forme mesurable d `existe_si`.

Remontee 5 du lot 5, reconduite telle quelle par la remontee 3 du lot 6 sur un
TROISIEME manifeste. Elle dit :

    `roles[].corps[].genre: conditionnelle` porte un `existe_si:` en francais
    (« au moins une entree datee », « la notion porte une controverse
    historiographique »). Ni le validateur ni le semis ne peuvent l evaluer ; le
    gabarit le rend en commentaire, et c est tout ce qu on peut en faire.

# L arbitrage de ce lot

**On n evalue pas la condition. On mesure son RESULTAT.**

C est la seule sortie qui ne demande pas d inventer un langage d expression dans
un fichier de configuration — ce que le kit refuse partout ailleurs (« le
manifeste BRANCHE les regles, il ne les decrit pas »). Une condition en francais
reste en francais ; ce qui devient mesurable, c est le fait qu elle produise ou
non une section sur les pages reelles.

Le manifeste BrainRef avait ecrit lui-meme ce qu il fallait faire :

    le kit doit MESURER l usage de ce qu il genere — une section qui n existe sur
    aucune page au bout de N pages est une section a supprimer du gabarit, pas a
    laisser « au cas ou ».

Et la mesure du vault d'origine est la meilleure illustration qu on puisse en donner :
`## Retours`, declaree conditionnelle avec `existe_si: "au moins une entree
datee"`, est ABSENTE des 337 briques — 0/337 presente, 0/337 remplie. Zero
entree en dix-huit mois, et pas meme un titre pose. La section conditionnelle
qui n a jamais eu d objet.

Le contre-exemple compte autant : `hub.Notes` est presente sur 13 hubs sur 74 et
remplie sur AUCUN. Une section presente et vide partout vaut le meme diagnostic
qu une section absente partout — et un compte de PRESENCE seul l aurait ratee.
On mesure donc les deux : la presence du titre, et le fait que quelque chose
soit ecrit dessous.

# Ce que la mesure ne dit pas

Elle ne dit pas de supprimer. Une section a 0 % sur douze pages ne prouve rien —
c est le meme raisonnement que le plancher du garde-fou 1, et le rendu applique
le meme seuil : sous le plancher, on rapporte le taux et on se tait.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..valider.contexte import Contexte
from ..valider.manifeste import Modele


@dataclass
class Occupation:
    """Une section d un gabarit de role, confrontee aux pages qui le portent."""

    role: str
    titre: str
    genre: str
    conditionnelle: bool
    existe_si: str
    population: int          # pages du role
    presentes: int           # pages ou le titre existe
    remplies: int            # pages ou quelque chose est ecrit dessous
    conteneur: bool = False  # une section qui n a de corps que dans ses filles

    @property
    def taux_presence(self) -> float:
        return self.presentes / self.population if self.population else 0.0

    @property
    def taux_remplissage(self) -> float:
        return self.remplies / self.population if self.population else 0.0

    @property
    def morte(self) -> bool:
        """Jamais remplie sur aucune page — presente ou pas.

        Une section CONTENEUR est exclue, et l exclusion n est pas une
        commodite : `## Écosystème` porte `### Alternatives` et
        `### Compléments`, donc son corps propre est vide sur les 337 briques
        par CONSTRUCTION. La compter morte dirait de supprimer la section qui
        tient les deux autres.
        """
        return self.population > 0 and self.remplies == 0 and not self.conteneur

    @property
    def universelle(self) -> bool:
        return self.population > 0 and self.presentes == self.population


def sous_arbre(page, titre: str) -> str | None:
    """Ce qui est ecrit SOUS un titre, sous-titres compris. None si le titre manque.

    `Page.sections` s arrete au titre suivant, quel que soit son niveau — c est
    ce qu il faut a une regle qui controle le corps PROPRE d une section. Ce
    n est pas ce qu il faut a une mesure d occupation : `## Concepts clés` porte
    trois `###` libres sur chacune des 297 notions, donc son corps propre est
    vide partout, et une mesure naive conclurait que la section est morte alors
    qu elle porte tout le contenu de la page.

    On lit donc le SOUS-ARBRE : du titre jusqu au prochain titre de niveau
    inferieur ou egal. C est la seule lecture qui reponde a la question posee —
    « y a-t-il quelque chose sous ce titre ? ».
    """
    from ..valider.vault import RE_TITRE

    dedans, niveau, buf = False, 0, []
    for ligne in page.corps.splitlines():
        m = RE_TITRE.match(ligne)
        if m:
            n, t = len(m.group(1)), m.group(2)
            if dedans and n <= niveau:
                break
            if not dedans and t == titre:
                dedans, niveau = True, n
                continue
        if dedans:
            buf.append(ligne)
    return "\n".join(buf) if dedans else None


def _vide(texte: str | None) -> bool:
    """Une section est vide quand elle ne porte que du blanc ou des commentaires.

    Le gabarit du semis pose un commentaire HTML sous une section conditionnelle
    (« la garder si …, sinon la SUPPRIMER »). Une page qui l a garde tel quel n a
    rien ecrit : la compter comme remplie ferait dire a la mesure exactement le
    contraire de ce qu elle mesure.
    """
    if texte is None:
        return True
    reste = []
    dans_commentaire = False
    for ligne in texte.splitlines():
        s = ligne.strip()
        if dans_commentaire:
            if "-->" in s:
                dans_commentaire = False
                s = s.split("-->", 1)[1].strip()
            else:
                continue
        while "<!--" in s:
            avant, apres = s.split("<!--", 1)
            reste.append(avant.strip())
            if "-->" in apres:
                s = apres.split("-->", 1)[1].strip()
            else:
                dans_commentaire = True
                s = ""
                break
        if s:
            reste.append(s)
    return not any(reste)


def occupation(mo: Modele, ctx: Contexte) -> list[Occupation]:
    """Le taux d occupation de CHAQUE section declaree, role par role."""
    out: list[Occupation] = []
    for rid in mo.roles:
        pages = ctx.pages_du_role(rid)
        corps = mo.corps(rid)
        for i, s in enumerate(corps):
            titre = mo.titre(s)
            brut = s.get("niveau")
            niveau = 2 if brut is None else int(brut)
            # `niveau: 0` n est pas un titre : c est un marqueur de PLACE — le
            # bandeau, l accroche, l embed d une vue, une zone AUTO. Il ne se
            # cherche pas parmi les `##` d une page, et le compter absent
            # partout inventerait 4 sections mortes par manifeste.
            if not titre or niveau == 0:
                continue
            suivant = corps[i + 1] if i + 1 < len(corps) else None
            n_suiv = None if suivant is None else suivant.get("niveau")
            conteneur = bool(suivant is not None
                             and (2 if n_suiv is None else int(n_suiv)) > niveau)
            presentes = sum(1 for p in pages if titre in p.sections)
            remplies = sum(1 for p in pages
                           if not _vide(sous_arbre(p, titre)))
            out.append(Occupation(
                role=rid, titre=titre, genre=str(s.get("genre") or ""),
                conditionnelle=bool(s.get("existe_si")
                                    or s.get("genre") == "conditionnelle"),
                existe_si=str(s.get("existe_si") or ""),
                population=len(pages), presentes=presentes, remplies=remplies,
                conteneur=conteneur))
    return out
