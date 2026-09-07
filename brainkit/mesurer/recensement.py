"""recensement.py — la forme de l arbre, d un coup d oeil. Remontee 8 du lot 3.

`check_arbo.py` imprimait, avant son verdict, « 681 page(s) migree(s) dans 20
domaine(s) — 10 rangee(s) par `role:` » puis une ligne par domaine avec son
compte. Le lot 3 l a ECARTE, et il avait raison : ce n est pas une regle, ca ne
rend aucun verdict, et un validateur qui imprime des mesures finit par noyer les
siennes.

Mais il l a ecarte en le NOMMANT une perte : *« la sortie de `check_arbo` etait
le seul endroit du vault ou l on voyait la forme de l arbre d un coup d oeil.
Elle appartient a la passe de mesure, qui est le lot 8 du kit, et c est la qu il
faut la remettre — avec les comptes de promotion, qui sont deja calcules par
`chemins.promotions()`. »*

C est fait ici, et avec les promotions. Deux choses de plus que l original, et
elles ne sont pas gratuites :

  - le compte se donne PAR ROLE dans chaque dossier, pas seulement en total. Le
    total d un domaine melange les unites, les notions et les vues, et c est
    justement ce melange qui rend l arbre v3 lisible — le voir, c est voir
    pourquoi le voisinage d une page est `ls` de son dossier ;
  - la DISTANCE AU SEUIL de chaque valeur non promue. Une valeur a quatre pages
    sur un seuil de cinq est l information qu on cherche quand on se demande de
    quoi l arbre va changer de forme au prochain ajout.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass, field

from ..valider import chemins
from ..valider.contexte import Contexte


@dataclass
class Domaine:
    dossier: str
    pages: int = 0                       # rangees par l AXE — la maille de `check_arbo`
    hubs: int = 0
    par_role: collections.Counter = field(default_factory=collections.Counter)
    sous_dossiers: list[str] = field(default_factory=list)


@dataclass
class Recensement:
    par_axe: list[Domaine] = field(default_factory=list)
    par_role: list[Domaine] = field(default_factory=list)
    total_axe: int = 0
    total_role: int = 0
    total_hubs: int = 0
    hors_arbre: int = 0
    promus: dict[str, str] = field(default_factory=dict)
    proches_du_seuil: list[tuple[str, int, int]] = field(default_factory=list)
    seuil: int = 0
    roles_par_role: list[str] = field(default_factory=list)


def recense(ctx: Contexte) -> Recensement:
    """La forme de l arbre : les dossiers de l axe, ceux des roles, les promotions.

    La MAILLE est celle de `check_arbo`, et il faut la dire : une page compte
    dans le total « rangee par l axe » quand son role PORTE l axe. Un hub n en
    porte pas — il ne se range pas, il EST le rangement —, donc il ne compte pas
    dans ce total, et il est compte a part. C est exactement le decoupage qui
    donnait « 681 page(s) dans 20 domaine(s) — 10 rangee(s) par `role:` », et
    reproduire ce chiffre est la preuve que le recensement est le meme.
    """
    mo = ctx.mo
    rec = Recensement(promus=dict(ctx.promus), seuil=mo.seuil,
                      roles_par_role=sorted(mo.roles_ranges_par_role()))

    par_role_ids = set(mo.roles_ranges_par_role())
    rid_hub = mo.role_hub

    par_tete: dict[str, Domaine] = {}
    for p in ctx.lisibles:
        if not p.dossier:
            rec.hors_arbre += 1
            continue
        tete = p.dossier.split("/")[0]
        d = par_tete.setdefault(tete, Domaine(tete))
        d.par_role[p.role] += 1
        if p.role == rid_hub:
            d.hubs += 1
            rec.total_hubs += 1
        elif p.role in par_role_ids:
            rec.total_role += 1
        elif p.role in mo.roles and mo.porte_l_axe_de_rangement(p.role):
            d.pages += 1
            rec.total_axe += 1
        if "/" in p.dossier and p.dossier not in d.sous_dossiers:
            d.sous_dossiers.append(p.dossier)

    for tete in sorted(par_tete):
        d = par_tete[tete]
        d.sous_dossiers.sort()
        (rec.par_role if d.pages == 0 else rec.par_axe).append(d)

    # La distance au seuil : ce qui va changer la forme de l arbre au prochain
    # ajout. Une valeur deja promue n y figure pas — elle a son dossier.
    poids = chemins.poids_du_seuil(ctx.lisibles, mo)
    for valeur, n in sorted(poids.items()):
        if "/" not in valeur or valeur in ctx.promus or not mo.seuil:
            continue
        if n >= mo.seuil:
            continue                    # non promue pour une autre raison (plafond)
        if mo.seuil - n <= 2:
            rec.proches_du_seuil.append((valeur, n, mo.seuil - n))
    return rec
