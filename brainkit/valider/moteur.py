"""moteur.py — l orchestration : quelles regles tournent, dans quel ordre, et le verdict.

Trois choix de conception, et ils sont le lot :

1. **Les dix d abord, dans l ordre du kit ; le socle ensuite, dans l ordre du
   manifeste.** L ordre de sortie est donc stable d une execution a l autre et
   d une instance a l autre, ce qui rend deux verdicts comparables.

2. **Une regle que le manifeste ne branche pas ne tourne pas.** Pas de valeur
   par defaut, pas de « au cas ou » : c est le manifeste qui decide, et
   l inventaire nomme celles qui n ont pas tourne, avec la raison.

3. **Le verdict se rend REGLE PAR REGLE.** Un compte global ne prouve rien : le
   critere d equivalence avec l ancien validateur porte sur chaque regle et
   chaque section. La table de comptes est donc imprimee a chaque execution,
   pas derriere une option.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import constat, dix, socle, vault, vocabulaires, vues
from .constat import Rapport
from .contexte import Contexte
from .manifeste import LES_DIX, Modele

IMPLEMENTEES = {**dix.IMPLEMENTEES, **socle.IMPLEMENTEES, **vues.IMPLEMENTEES}


@dataclass
class Verdict:
    rapport: Rapport
    contexte: Contexte

    @property
    def dures(self) -> list[constat.Constat]:
        return self.rapport.par_severite(constat.DURE)

    @property
    def avertissements(self) -> list[constat.Constat]:
        return self.rapport.par_severite(constat.AVERTISSEMENT)

    @property
    def a_mesurer(self) -> list[constat.Constat]:
        return self.rapport.par_severite(constat.A_MESURER)

    @property
    def code(self) -> int:
        return 1 if self.dures else 0


def valide(mo: Modele, racine: Path) -> Verdict:
    pages = vault.lire_vault(racine, mo.non_pages)
    ctx = Contexte(mo=mo, racine=racine, pages=pages,
                   vocabulaires=vocabulaires.charge_tous(mo.vocabulaires, racine))
    ctx.prepare()
    r = Rapport()

    lancees: list[str] = []
    for rid in LES_DIX:
        if rid not in mo.regles:
            r.etat(rid, "absente de `regles[]` — le manifeste ne la branche pas")
            continue
        IMPLEMENTEES[rid](ctx, r)
        lancees.append(rid)

    for rid in mo.socle:
        fn = IMPLEMENTEES.get(rid)
        if fn is None:
            r.etat(rid, "déclarée par le manifeste, NON implémentée par le moteur")
            continue
        fn(ctx, r)
        lancees.append(rid)

    for rid in IMPLEMENTEES:
        if rid not in mo.regles and rid not in mo.socle:
            r.etat(rid, constat.NON_DECLAREE)

    touchees = set(r.regles_touchees())
    for rid in lancees:
        if rid not in touchees and rid not in r.etats:
            r.etat(rid, constat.TOURNEE)

    return Verdict(r, ctx)


# --------------------------------------------------------------------------- #
#  Impression
# --------------------------------------------------------------------------- #
_ETIQUETTE = {constat.DURE: "FAIL", constat.AVERTISSEMENT: "WARN",
              constat.A_MESURER: "MESURE"}


def _ligne(c: constat.Constat) -> str:
    quoi = c.regle if not c.cle else f"{c.regle}/{c.cle}"
    codes = f" [{'·'.join(c.codes)}]" if c.codes else ""
    return f"  [{_ETIQUETTE[c.severite]}] {quoi}{codes} — {c.rendu()}"


def imprime(v: Verdict, mo: Modele, racine: Path, regle: str | None = None,
            tout: bool = False) -> int:
    r = v.rapport
    lisibles = len(v.contexte.lisibles)
    illisibles = len(v.contexte.pages) - lisibles
    suffixe = f" ({illisibles} illisible(s))" if illisibles else ""
    print(f"valider : {len(v.contexte.pages)} page(s) contrôlée(s){suffixe} — "
          f"vault `{racine.name}`, manifeste "
          f"`{mo.chemin.name if mo.chemin else '(inconnu)'}`")

    def garde(c: constat.Constat) -> bool:
        return regle is None or c.regle == regle

    for c in sorted(v.avertissements, key=lambda c: (c.regle, c.cle, c.page)):
        if garde(c):
            print(_ligne(c))
    for c in sorted(v.a_mesurer, key=lambda c: (c.regle, c.cle, c.page)):
        if garde(c):
            print(_ligne(c))

    # ---- la table du verdict, regle par regle -------------------------- #
    print("\nverdict, règle par règle :")
    comptes = r.compte_par_regle()
    vus: set[str] = set()
    for rid in list(LES_DIX) + list(mo.socle) + sorted(IMPLEMENTEES):
        if rid in vus:
            continue
        vus.add(rid)
        lignes = sorted((k, n) for k, n in comptes.items() if k[0] == rid)
        if not lignes:
            print(f"  {rid:34s} · 0 — {r.etats.get(rid, constat.TOURNEE)}")
            continue
        for (_rid, cle, sev), n in lignes:
            ou = f"/{cle}" if cle else ""
            print(f"  {rid + ou:34s} · {n} {sev}")

    if r.notes and tout:
        print("\nnotes :")
        for n in r.notes:
            print(f"  - {n}")
    elif r.notes:
        print(f"\n{len(r.notes)} note(s) — `--tout` pour les lire")

    dures = [c for c in v.dures if garde(c)]
    if dures:
        print(f"\n{len(dures)} violation(s) DURE(s) :")
        for c in sorted(dures, key=lambda c: (c.regle, c.cle, c.page)):
            print(_ligne(c))
        return 1
    n_w = len([c for c in v.avertissements if garde(c)])
    n_m = len([c for c in v.a_mesurer if garde(c)])
    queue = []
    if n_w:
        queue.append(f"{n_w} avertissement(s)")
    if n_m:
        queue.append(f"{n_m} à mesurer")
    print("\nOK — aucune violation dure."
          + (f" ({', '.join(queue)})" if queue else ""))
    return 0
