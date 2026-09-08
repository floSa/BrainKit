"""chemins.py — la derivation `valeur d axe` -> `dossier`, ecrite UNE fois.

Personne ne choisit un dossier : le chemin d une page se DERIVE de sa valeur de
l axe de rangement, du seuil de promotion, de son plafond et des libelles
declares. Le validateur applique la meme derivation qu un generateur, sans quoi
le vault et son validateur divergent en silence.

# L axe non exclusif — la rupture 3, portee ici

Le DevBrain n a jamais le cas : une brique a exactement un domaine, toujours.
Un brain d histoire l a des la vingtieme page — « Histoire de la France des
origines a nos jours » ne tombe dans aucune periode unique. Trois mecanismes
declares par le manifeste, et ce module les porte tous les trois :

  - `exclusif: false` — le champ peut porter PLUSIEURS valeurs, ou AUCUNE ;
  - `regle_de_majorite: true` — la valeur qui range la page est celle qui « en
    rassemble le plus ». C est une phrase EDITORIALE, et aucune machine ne la
    calcule : ce que le validateur peut verifier, et ce qu il verifie, c est que
    le dossier de la page se derive d une valeur qu elle PORTE VRAIMENT. La
    regle de majorite choisit laquelle ; le validateur refuse un dossier qui ne
    correspond a aucune.
  - `prefixe_transversal: <cle>` — le prefixe reserve a ce qui n a AUCUN centre
    de gravite. Il l emporte sur les autres valeurs : une page qui le porte vit
    dans SON dossier, pas dans celui d une periode qu elle traverse.

Et l axe ABSENT : une page dont le role ne porte pas l axe (`porte_categorie:
false`), ou dont le champ est vide sur un role qui ne l exige pas, n a pas de
chemin a deriver. Elle est ECARTEE de la regle et COMPTEE comme telle — jamais
ecartee en silence.
"""

from __future__ import annotations

import collections

from . import vault
from .manifeste import Modele


def valeurs_d_axe(fm: dict, mo: Modele) -> list[str]:
    """Les valeurs de l axe de rangement portees par une page."""
    return vault.valeurs(fm.get(mo.champ_rangement))


def est_transversale(valeur: str, mo: Modele) -> bool:
    return (mo.prefixe_transversal is not None
            and valeur.split("/")[0] == mo.prefixe_transversal)


def dossier_attendu(valeur: str, promus: dict[str, str], mo: Modele) -> str | None:
    """Le dossier d accueil d une valeur, relatif a la racine. None si indérivable.

    `promus` : {valeur complete : libelle du sous-dossier} — les sous-valeurs
    qui ont franchi le seuil, calculees sur la population reelle.
    """
    prefixe = valeur.split("/")[0]
    dossier = mo.dossier_de_prefixe.get(prefixe)
    if dossier is None:
        return None
    sous = promus.get(valeur)
    return f"{dossier}/{sous}" if sous else dossier


def valeur_dominante(fm: dict, dossier: str, mo: Modele) -> str | None:
    """La valeur qui RANGE la page, quand elle en porte plusieurs.

    L ordre de resolution ne depend PAS du seuil — sans quoi le calcul du seuil,
    qui a besoin de cette attribution, tournerait en rond :

      1. une seule valeur : c est elle ;
      2. le prefixe transversal, s il est porte : il l emporte ;
      3. la valeur dont le dossier de PREFIXE est celui ou la page vit — c est
         la lecture machine de la regle de majorite : on ne devine pas laquelle
         « rassemble le plus », on lit celle que le rangement a retenue ;
      4. a defaut, la premiere declaree.
    """
    vals = valeurs_d_axe(fm, mo)
    if not vals:
        return None
    if len(vals) == 1:
        return vals[0]
    for v in vals:
        if est_transversale(v, mo):
            return v
    tete = dossier.split("/")[0]
    for v in vals:
        if mo.dossier_de_prefixe.get(v.split("/")[0]) == tete:
            return v
    return vals[0]


def poids_du_seuil(pages, mo: Modele) -> collections.Counter:
    """Le compte des pages qui PESENT sur le seuil, par valeur de l axe.

    Un role `pese_sur_le_seuil: false` est verifie comme les autres mais ne
    compte pas : « une vue n est pas un membre de la vue ». Sans cette
    exception, convertir un fichier en page ferait franchir le seuil a une
    sous-valeur, et l arbre changerait de forme sans qu aucune unite soit
    arrivee.

    Une page compte UNE FOIS, pour sa valeur dominante — un axe non exclusif ne
    doit pas gonfler trois sous-valeurs avec une seule page.
    """
    c: collections.Counter = collections.Counter()
    for p in pages:
        if p.illisible or p.role not in mo.roles:
            continue
        if not mo.porte_l_axe_de_rangement(p.role):
            continue
        if not mo.pese_sur_le_seuil(p.role):
            continue
        v = valeur_dominante(p.fm, p.dossier, mo)
        if v:
            c[v] += 1
    return c


def promotions(pages, mo: Modele) -> tuple[dict[str, str], list[str]]:
    """Les sous-valeurs promues en dossier. Rend (promus, valeurs sans libelle).

    Le seuil se compte PAR PREFIXE, jamais sur le total. Son plafond ecarte le
    fils qui redoublerait son parent : `n == total du prefixe`, pas « fils
    unique » — deux sous-valeurs de cinq pages qui se partagent un prefixe de
    dix se promeuvent toutes les deux, elles separent quelque chose.

    Une sous-valeur qui franchit le seuil SANS libelle declare fait echouer la
    derivation plutot qu inventer un nom de dossier. C est le comportement
    voulu : le libelle se lit dans le manifeste, il ne se devine pas.
    """
    par_prefixe: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter)
    for valeur, n in poids_du_seuil(pages, mo).items():
        dossier = mo.dossier_de_prefixe.get(valeur.split("/")[0])
        if dossier:
            par_prefixe[dossier][valeur] += n

    promus: dict[str, str] = {}
    sans_libelle: list[str] = []
    for dossier in sorted(par_prefixe):
        compte = par_prefixe[dossier]
        total = sum(compte.values())
        for valeur, n in sorted(compte.items()):
            if n < mo.seuil or "/" not in valeur:
                continue
            if mo.plafond and n == total:
                continue
            libelle = (mo.sous_valeurs.get(valeur) or {}).get("libelle")
            if not libelle:
                sans_libelle.append(f"`{valeur}` atteint {n} page(s) (seuil "
                                    f"{mo.seuil}) sans `libelle` déclaré")
                continue
            promus[valeur] = libelle
    return promus, sans_libelle


class _PageDeSeuil:
    """Le MINIMUM que `poids_du_seuil` lit d une page. Pas une `Page` du vault.

    Quatre attributs, et c est tout ce que la derivation du seuil consulte :
    le frontmatter (pour la valeur d axe), le role (pour savoir s il pese), le
    dossier (pour resoudre la valeur dominante) et la lisibilite.
    """

    __slots__ = ("fm", "role", "dossier", "illisible")

    def __init__(self, fm: dict, role: str | None, dossier: str = "") -> None:
        self.fm, self.role, self.dossier, self.illisible = fm, role, dossier, None


def promotions_depuis_valeurs(valeurs, mo: Modele) -> tuple[dict[str, str], list[str]]:
    """`promotions()`, pour un appelant qui n a que des VALEURS d axe.

    # Pourquoi cette porte existe — remontee 2 du lot 9

    `promotions(pages, mo)` prend des pages, et elle a raison : elle doit
    pouvoir ecarter un role hors seuil (`pese_sur_le_seuil: false`) et resoudre
    la valeur dominante d un axe non exclusif. Mais un appelant qui lit l index
    plutot que le vault — un skill de capture, un pont d instance — n a que des
    chaines. Le lot 9 lui a fait fabriquer huit lignes de pages factices, dans
    l instance ; la prochaine instance les aurait reecrites.

    Elles sont donc ici, une fois, a la bonne place. Chaque valeur devient une
    page du role d UNITE — celui qui pese — ce qui n invente rien : compter des
    valeurs d axe, c est exactement compter des unites.

    Ce n est pas une correction du calcul : c est la reconnaissance que le kit a
    une **API**, et pas seulement une ligne de commande.
    """
    unite = mo.role_de_fonction("unite")
    champ = mo.champ_rangement
    pages = [_PageDeSeuil(fm={champ: v}, role=unite,
                          dossier=mo.dossier_de_prefixe.get(
                              str(v).split("/")[0]) or "")
             for v in valeurs]
    return promotions(pages, mo)


def hub_du_dossier(dossier: str) -> str:
    """Le chemin du hub qui porte un dossier : le dossier porte une page a son nom."""
    return f"{dossier}/{dossier.rsplit('/', 1)[-1]}.md"


def niveaux(dossier: str) -> list[str]:
    parts = dossier.split("/")
    return ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
