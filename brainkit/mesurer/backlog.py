"""backlog.py — la liste de TRAVAIL. Le seul outil du kit dont la sortie n est pas un verdict.

C est la place que le lot 3 a promise a quatre choses qui n avaient nulle part ou
aller, et qui se ressemblent toutes par un point : elles decrivent un ECART VOULU
ou un TRAVAIL A FAIRE, pas une faute a corriger. Les mettre dans un validateur
les aurait transformees en avertissements permanents — et *« un outil qui repete
sept avertissements permanents a chaque execution finit ignore »*.

# `A1` et `A3` — arbitrage 3 du lot 3, execute ici

Le lot 3 a tranche qu elles ne sont pas des regles : elles n ont jamais ete dans
les validateurs du vault d'origine, les ajouter aurait casse son critere d acceptation
(118 avertissements au lieu de 111), et surtout `A3` signale un etat **voulu** —
le manifeste garde le libelle d une valeur plafonnee pour que la promotion
reprenne d elle-meme le jour ou le domaine gagne une seconde population. Une
regle qui signale ce qu on a decide n est pas une regle, c est un rappel.

Elles restent donc dans `outils/fidelite.py`, ou le lot 2 les a mises et ou leurs
verdicts sont ecrits. Ce qui arrive ici, c est leur PLACE DE TRAVAIL : le lot 2
recommandait de les sortir des ecarts, le lot 3 a dit que le lot 8 aurait la
bonne place pour un backlog, et la voici. Les deux comptes sont recalculs ici,
sur les memes donnees, parce qu un backlog qui renverrait a la sortie d un autre
outil ne serait pas une liste de travail.

# Les champs vestigiaux — §5.11 du cadrage

*« ajouter `deprecated: true` sur un champ autorise — le validateur le tolere, le
generateur ne le met pas dans le gabarit, et `mesurer` compte combien de pages le
portent encore. Cout faible, et cela evite qu un vestige devienne une intention
par transposition. »* La phrase nomme `mesurer` : c est ici.

# La table de propagation declaree — remontee 2 du lot 7

Le lot 7 derive la table ; le manifeste en declare une seconde. Depuis
l arbitrage de ce lot, la declaration n est plus une source — mais un manifeste
ecrit avant l arbitrage en porte une, et la confronter est exactement ce qu on
sait faire d une seconde source qu on ne veut plus : la mesurer.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass, field

from ..valider import chemins
from ..valider.contexte import Contexte
from ..valider.manifeste import Modele


@dataclass
class Entree:
    code: str
    sujet: str
    quoi: str
    poids: int = 1


@dataclass
class Backlog:
    entrees: list[Entree] = field(default_factory=list)

    def ajoute(self, code: str, sujet: str, quoi: str, poids: int = 1) -> None:
        self.entrees.append(Entree(code, sujet, quoi, poids))

    def par_code(self) -> dict[str, list[Entree]]:
        out: dict[str, list[Entree]] = {}
        for e in self.entrees:
            out.setdefault(e.code, []).append(e)
        return out


CODES = {
    "A1": "valeur d'axe de rangement déclarée et portée par AUCUNE page",
    "A3": "`libelle` déclaré pour une valeur que le seuil n'a pas promue",
    "F8": "champ déclaré vestigial (`deprecies`) et encore porté",
    "G0": "section d'un gabarit que rien ne remplit sur aucune page",
    "E4": "information déclarée dans le manifeste ET dérivée par le kit",
}


def construis(mo: Modele, ctx: Contexte, occupations=None,
              lignes_derivees: int | None = None) -> Backlog:
    """Le backlog d un vault : ce qui est a faire, et qui n est pas une violation."""
    b = Backlog()

    portees = collections.Counter()
    for p in ctx.lisibles:
        if p.role in mo.roles and mo.porte_l_axe_de_rangement(p.role):
            for v in chemins.valeurs_d_axe(p.fm, mo):
                portees[v] += 1

    # A1 — declaree, portee par personne.
    for v in sorted(mo.valeurs_rangement - set(portees)):
        b.ajoute("A1", v, "déclarée dans l'axe, portée par aucune page — "
                          "soit une page manque, soit la valeur est à retirer")

    # A3 — un libelle declare pour une valeur que le seuil n a pas promue. Deux
    # causes qui ne se confondent pas : le plafond (etat VOULU, le libelle est
    # garde expres) ou le seuil (la valeur n a pas encore assez de pages).
    poids = chemins.poids_du_seuil(ctx.lisibles, mo)
    par_prefixe: dict[str, int] = collections.Counter()
    for valeur, n in poids.items():
        d = mo.dossier_de_prefixe.get(valeur.split("/")[0])
        if d:
            par_prefixe[d] += n
    for valeur, decl in sorted(mo.sous_valeurs.items()):
        if not (decl or {}).get("libelle") or valeur in ctx.promus:
            continue
        n = poids.get(valeur, 0)
        if not n:
            continue      # zero page : c est `A1` qui le dit, et une seule fois
        dossier = mo.dossier_de_prefixe.get(valeur.split("/")[0])
        total = par_prefixe.get(dossier, 0)
        if mo.plafond and n and n == total:
            cause = (f"{n} page(s) — PLAFOND de promotion : elle redoublerait son "
                     f"préfixe. État VOULU, le libellé est gardé pour que la "
                     f"promotion reprenne d'elle-même")
        elif n >= mo.seuil:
            continue
        else:
            cause = (f"{n} page(s) pour un seuil de {mo.seuil} — il en manque "
                     f"{mo.seuil - n}")
        b.ajoute("A3", valeur, cause, poids=n)

    # F8 — les champs vestigiaux encore portes (§5.11).
    for rid in sorted(mo.roles):
        for champ in sorted(mo.deprecies(rid)):
            n = sum(1 for p in ctx.pages_du_role(rid) if champ in p.fm)
            if n:
                b.ajoute("F8", f"{rid}.{champ}",
                         f"déclaré vestigial et encore porté par {n} page(s) — "
                         f"un vestige non compté devient une intention", poids=n)

    # G0 — une section que rien ne remplit, jamais. Cf. `gabarit.py`.
    for o in occupations or []:
        if o.morte and o.population:
            b.ajoute("G0", f"{o.role}.{o.titre}",
                     f"présente sur {o.presentes}/{o.population} page(s) et "
                     f"remplie sur AUCUNE"
                     + (f" — condition déclarée : « {o.existe_si} »"
                        if o.existe_si else ""),
                     poids=o.population)

    # E4 — la seconde source. Cf. la remontee 2 du lot 7, tranchee au lot 8.
    prop = mo.m.get("propagation") or {}
    # `table` et `hubs_transverses` sont DEUX listes du meme objet : la seconde
    # replie les axes transverses a part. Les compter separement ferait dire
    # « 6 contre 9 » la ou le lot 7 avait mesure « 7 contre 9 ».
    declaree = list(prop.get("table") or []) + list(prop.get("hubs_transverses") or [])
    if declaree and lignes_derivees is not None:
        b.ajoute("E4", "propagation.table",
                 f"{len(declaree)} ligne(s) déclarées dans le manifeste contre "
                 f"{lignes_derivees} dérivées par le kit — la déclaration n'est "
                 f"plus une source depuis le lot 8 : elle peut être retirée",
                 poids=len(declaree))
    return b
