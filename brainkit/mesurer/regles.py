"""regles.py — la mesure, regle par regle, et la proposition de durcissement.

Une ligne de mesure porte quatre choses, et pas une de moins :

  - le COMPTE de violations, tel que le validateur le rend ;
  - la POPULATION reellement mesuree, telle que la regle la declare ;
  - la DATE de la mesure ;
  - le VERDICT — et un verdict n est jamais « rien a dire ». Il dit POURQUOI il
    n y a rien a proposer, et les six raisons ne se confondent pas.

C est cette derniere exigence qui fait la difference entre un rapport de mesure
et un tableau de zeros. Une regle deja dure, une regle a reparer, une regle qui
attend vingt pages de plus et une regle que le manifeste desactive produisent
toutes les quatre « aucune proposition » — et ce sont quatre situations sans
rapport.

# Ce que ce module ne fait PAS

Il ne durcit rien. Il ne recrit aucun manifeste, il ne touche aucun vault. Sa
sortie est une LISTE DE TRAVAIL, pas un verdict — c est la distinction que le
lot 3 avait posee en renvoyant `A1`/`A3` ici (cf. `backlog.py`), et elle vaut
d abord pour les propositions de durcissement elles-memes : le durcissement est
une decision, la mesure est ce qui permet de la prendre.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field

from ..valider.constat import Population, Rapport
from ..valider.manifeste import LES_DIX, Modele
from ..valider.moteur import Verdict
from . import gardes


@dataclass
class Ligne:
    """La mesure d UNE regle — ou d une section, quand la severite est par section."""

    regle: str
    cle: str = ""
    severite: str = "a_mesurer"
    active: bool = True
    violations: int = 0
    population: Population | None = None
    declaree: dict | None = None          # le bloc `mesure:` du manifeste, s il existe
    etat: str = ""                        # la raison du silence, telle que le moteur la dit
    verdict: str = gardes.NON_MESUREE
    motif: str = ""
    structurelle: bool = False
    manque: int = 0                       # pages qui manquent au plancher
    details: list[tuple[str, int, Population | None]] = field(default_factory=list)
    severites_vues: tuple[str, ...] = ()

    @property
    def severite_divergente(self) -> bool:
        """La severite APPLIQUEE differe de celle qui est declaree.

        Le cas existe et il est connu : `vocabulaire_ferme` declare
        `severite: dure` et porte `R14b`, dont la severite ne vit pas dans la
        regle mais dans `axes.nature.vide_autorise`. Le moteur lit la bonne
        source ; la declaration, elle, reste trompeuse pour un lecteur humain —
        c est la remontee 2 du lot 3, et elle se VOIT ici pour la premiere fois.
        """
        return bool(self.severites_vues) and set(self.severites_vues) != {self.severite}

    @property
    def id_affiche(self) -> str:
        return f"{self.regle}/{self.cle}" if self.cle else self.regle

    @property
    def pages(self) -> int:
        return self.population.pages if self.population else 0

    @property
    def sur_le_manifeste(self) -> bool:
        return bool(self.population and self.population.sur_le_manifeste)

    def bloc_a_coller(self, date: str) -> list[str]:
        """Le YAML a coller dans `regles[]` si la proposition est retenue.

        Le `motif:` sort VIDE et en majuscules : garde-fou 2, corollaire. Le kit
        sait mesurer, il ne sait pas ecrire pourquoi.
        """
        pop = (f"population: {self.pages}" if not self.sur_le_manifeste
               else f"population: {self.population.objets} "
                    f"# {self.population.objet}")
        return [f"  - id: {self.regle}",
                "    severite: dure",
                '    motif: "À ÉCRIRE — le kit refuse une sévérité sans motif"',
                f'    mesure: {{ date: "{date}", {pop}, violations: 0 }}']


@dataclass
class Mesure:
    """Tout ce qu une passe de mesure produit sur un vault."""

    date: str
    vault: str
    manifeste: str
    role_unite: str | None
    pages_de_l_unite: int
    pages_totales: int
    lignes: list[Ligne] = field(default_factory=list)
    sans_motif: list[Ligne] = field(default_factory=list)
    contradictions: list[str] = field(default_factory=list)

    @property
    def plancher_tenu(self) -> bool:
        return gardes.plancher_tenu(self.pages_de_l_unite)

    @property
    def propositions(self) -> list[Ligne]:
        return [x for x in self.lignes if x.verdict == gardes.PROPOSEE]

    def par_verdict(self, verdict: str) -> list[Ligne]:
        return [x for x in self.lignes if x.verdict == verdict]


# --------------------------------------------------------------------------- #
def _sous_cles(rid: str, r: Rapport) -> list[str]:
    """Toutes les cles qu une regle a produites — populations et constats confondus."""
    cles = [c for (x, c) in r.populations if x == rid and c]
    cles += [c.cle for c in r.constats if c.regle == rid and c.cle]
    return sorted(set(cles))


def _unites_de_decision(mo: Modele, rid: str) -> list[str]:
    """Les cles sur lesquelles une severite se DECIDE — pas celles qu on affiche.

    Une severite declaree PAR SECTION se decide par section : `Mise en œuvre` a
    zero violation et `Ressources` en a cinq, et fondre les deux rendrait la
    premiere indurcissable et la seconde invisible.

    Une severite SCALAIRE se decide au niveau de la regle, meme quand la regle
    produit plusieurs sous-constats. C est le cas de `couverture_des_vues`,
    dont les cinq sous-constats partagent une seule severite : proposer de
    durcir `c` parce qu il est a zero, quand `a` en a treize, proposerait une
    chose qui ne s ecrit pas. Les sous-comptes restent AFFICHES, en detail — ce
    sont eux que le critere d acceptation du lot 3 confronte.
    """
    sev = (mo.regles.get(rid) or mo.socle.get(rid) or {}).get("severite")
    return sorted(str(k) for k in sev) if isinstance(sev, dict) else [""]


def _verdict(li: Ligne, plancher_instance: bool) -> None:
    """Le verdict d une ligne, et le manque de pages quand il y en a un.

    L ordre des tests EST la regle, et il se lit de haut en bas :

      1. une regle qui n a pas tourne n a rien mesure — pas de verdict de mesure ;
      2. les deux structurellement dures sortent du regime de la mesure ;
      3. une regle deja dure n a rien a durcir ;
      4. des violations : il y a du travail avant, pas un durcissement ;
      5. le plancher d instance : sous 30 pages, on ne propose RIEN ;
      6. le plancher de regle : zero sur trois pages n a rien prouve.
    """
    if not li.active or li.etat:
        li.verdict = gardes.NON_MESUREE
        return
    if li.structurelle:
        li.verdict = gardes.STRUCTURELLE
        return
    if li.severite == "dure":
        li.verdict = gardes.DEJA_DURE
        return
    if li.violations:
        li.verdict = gardes.A_REPARER
        return
    if not plancher_instance:
        li.verdict = gardes.REFUS_INSTANCE
        return
    if li.sur_le_manifeste:
        li.verdict = gardes.PROPOSEE      # son denominateur n est pas un corpus
        return
    if not gardes.plancher_tenu(li.pages):
        li.verdict = gardes.REFUS_POPULATION
        li.manque = gardes.manque_au_plancher(li.pages)
        return
    li.verdict = gardes.PROPOSEE


def mesure_les_regles(mo: Modele, v: Verdict, vault: str, date: str = "") -> Mesure:
    """Confronte le verdict du validateur aux trois garde-fous de §5.6."""
    date = date or datetime.date.today().isoformat()
    r = v.rapport
    rid_unite = mo.role_unite
    n_unite = len(v.contexte.pages_du_role(rid_unite)) if rid_unite else 0

    m = Mesure(date=date, vault=vault,
               manifeste=mo.chemin.name if mo.chemin else "(inconnu)",
               role_unite=rid_unite, pages_de_l_unite=n_unite,
               pages_totales=len(v.contexte.pages))

    ordre = list(LES_DIX) + [x for x in mo.regles if x not in LES_DIX] + list(mo.socle)
    vus: set[str] = set()
    for rid in ordre:
        if rid in vus:
            continue
        vus.add(rid)
        decl = mo.regles.get(rid) or mo.socle.get(rid) or {}
        # Une regle de socle n a pas de `active:` — elle est branchee par sa
        # presence. Une des dix, si.
        active = mo.regle_active(rid) if rid in mo.regles else True
        etat = r.etats.get(rid, "")
        if etat in ("tournée, aucun constat",):
            etat = ""
        sous = _sous_cles(rid, r)
        for cle in _unites_de_decision(mo, rid):
            vise = [c for c in r.constats
                    if c.regle == rid and (not cle or c.cle == cle)]
            li = Ligne(
                regle=rid, cle=cle,
                severite=mo.severite(rid, cle or None),
                active=active,
                violations=len(vise),
                population=r.population_de(rid, cle),
                declaree=(decl.get("mesure") or {}).get(cle) if (
                    cle and isinstance(decl.get("mesure"), dict)
                    and cle in (decl.get("mesure") or {})) else decl.get("mesure"),
                etat=etat,
                motif=gardes.motif_ecrit(decl),
                structurelle=rid in gardes.STRUCTURELLEMENT_DURES,
                severites_vues=tuple(sorted({c.severite for c in vise})),
                details=[] if cle else
                        [(k, sum(1 for c in r.constats
                                 if c.regle == rid and c.cle == k),
                          r.populations.get((rid, k))) for k in sous],
            )
            # Une regle dont la severite est SCALAIRE mais qui n a declare
            # sa population que par sous-cle : on prend la plus large de ses
            # sous-populations. Imprimer « — » la ou la regle a mesure dix
            # pages effacerait la seule chose que le lot 8 ajoute.
            if li.population is None and li.details:
                candidates = [pop for _k, _n, pop in li.details if pop]
                if candidates:
                    li.population = max(candidates, key=lambda x: x.pages)
            _verdict(li, m.plancher_tenu)
            m.lignes.append(li)

            # Garde-fou 2 : le kit REFUSE un avertissement sans motif ecrit.
            if li.severite == "avertissement" and not li.motif and active:
                m.sans_motif.append(li)

            # Garde-fou 3 : la liste est fermee par le kit. Un manifeste qui la
            # contredit est SIGNALE, jamais suivi en silence.
            if li.structurelle and li.severite != "dure" and active and not cle:
                dit = decl.get("structurellement_dure")
                m.contradictions.append(
                    f"`{rid}` est structurellement dure (garde-fou 3, liste fermée "
                    f"par le kit) et le manifeste la déclare `severite: "
                    f"{li.severite}`"
                    + (f" avec `structurellement_dure: {dit}`" if dit is not None
                       else "")
                    + " — une violation y est une incohérence de STRUCTURE, pas un "
                      "défaut de rédaction : elle se décide quand le manifeste "
                      "s'écrit, pas quand on mesure.")
    return m
