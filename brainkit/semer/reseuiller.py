"""reseuiller.py — changer le seuil de promotion est une MIGRATION, pas un reglage.

# Pourquoi cette operation existe (rupture 5 du test a blanc)

`SEUIL = 5` du DevBrain est calibre sur ~700 pages en 20 domaines, soit ~35 par
domaine. Sur 3 000 pages en 8 periodes — ~375 par periode — le meme seuil
produirait quarante sous-dossiers par periode, ce qui n est plus un arbre mais
une liste. A l inverse, un brain client de 40 pages en 6 paquets ne promouvrait
jamais rien.

Le seuil se derive donc du volume cible, et le calcul s ecrit dans `motif_seuil`.
Mais un brain qui grandit plus que prevu devra le CHANGER, et **changer le seuil
reforme l arbre** : des pages changent de dossier. Le DevBrain s en est passe
parce qu il a fixe son seuil une fois, avec 700 pages deja ecrites sous les yeux.

# Trois regles, et aucune n est negociable

1. **`git mv`, jamais suppression + creation.** Un deplacement par `rm` + `add`
   perd l historique de la page, et l historique est ce qui distingue un vault
   d un dossier de fichiers.
2. **Le mode par defaut n ecrit rien.** `re-seuiller` se lance d abord pour VOIR
   ce qu il ferait — sur un arbre de 700 pages, la reponse tient rarement dans
   ce qu on imaginait.
3. **Une depromotion ne SUPPRIME rien.** Un sous-dossier qui retombe sous le
   seuil rend ses pages au parent, et son hub devient orphelin. Le hub n est pas
   efface : il est SIGNALE. « Jamais sans accord » vaut pour toute suppression de
   page, et une migration automatique n est pas un accord.

# Ce que l operation cree quand meme

Le hub d un dossier NOUVELLEMENT promu. Sans lui, `hub_par_niveau` — regle DURE —
serait viole des la fin de la migration, et l operation livrerait un vault rouge.
Creer ce hub n est pas une exception a la regle 3 : on ne supprime rien, on pose
la page que la structure exige.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass, field
from pathlib import Path

from ..valider import chemins, vault
from ..valider.manifeste import Modele
from . import depot as _depot
from . import pages as _pages
from .plan import Plan
from .prose import ProseSemis


@dataclass
class Mouvement:
    depuis: str
    vers: str
    valeur: str


@dataclass
class Reseuillage:
    seuil_actuel: int
    seuil_vise: int
    promus_avant: dict[str, str] = field(default_factory=dict)
    promus_apres: dict[str, str] = field(default_factory=dict)
    mouvements: list[Mouvement] = field(default_factory=list)
    hubs_a_creer: list[tuple[str, str, str]] = field(default_factory=list)
    hubs_orphelins: list[str] = field(default_factory=list)
    sans_libelle: list[str] = field(default_factory=list)
    refus: list[str] = field(default_factory=list)
    applique: bool = False

    @property
    def promotions(self) -> list[str]:
        return sorted(set(self.promus_apres) - set(self.promus_avant))

    @property
    def depromotions(self) -> list[str]:
        return sorted(set(self.promus_avant) - set(self.promus_apres))

    @property
    def sans_effet(self) -> bool:
        return not self.mouvements and not self.hubs_a_creer


def _avec_seuil(mo: Modele, seuil: int) -> Modele:
    """Le MEME manifeste, lu avec un autre seuil. Aucun fichier n est touche."""
    import copy
    m = copy.deepcopy(mo.m)
    m["axes"]["rangement"]["seuil_promotion"] = int(seuil)
    return Modele(m, mo.chemin)


def calcule(mo: Modele, racine: Path, seuil_vise: int) -> Reseuillage:
    """Ce que le changement de seuil ferait. N ECRIT RIEN, jamais."""
    r = Reseuillage(seuil_actuel=mo.seuil, seuil_vise=int(seuil_vise))
    if seuil_vise < 1:
        r.refus.append(f"seuil visé `{seuil_vise}` — un seuil est un entier ≥ 1")
        return r

    pages = [p for p in vault.lire_vault(racine, mo.non_pages) if p.illisible is None]
    mo_apres = _avec_seuil(mo, seuil_vise)
    r.promus_avant, avant_sans = chemins.promotions(pages, mo)
    r.promus_apres, apres_sans = chemins.promotions(pages, mo_apres)
    r.sans_libelle = sorted(set(avant_sans) | set(apres_sans))

    # --- les pages qui changent de dossier -------------------------------- #
    peuple: collections.Counter = collections.Counter()
    for p in pages:
        if p.role not in mo.roles or not mo.porte_l_axe_de_rangement(p.role):
            continue
        valeur = chemins.valeur_dominante(p.fm, p.dossier, mo)
        if not valeur:
            continue
        cible = chemins.dossier_attendu(valeur, r.promus_apres, mo)
        if cible is None:
            r.refus.append(f"{p.chemin} : `{valeur}` n'a aucun dossier dérivable")
            continue
        if cible != p.dossier:
            r.mouvements.append(
                Mouvement(p.chemin, f"{cible}/{p.absolu.name}", valeur))
        peuple[cible] += 1

    # --- les hubs a creer, et ceux qui restent sans dossier --------------- #
    existants = {p.dossier for p in pages if p.role == mo.role_hub}
    for valeur in r.promotions:
        dossier = chemins.dossier_attendu(valeur, r.promus_apres, mo)
        if dossier and dossier not in existants:
            libelle = (mo.sous_valeurs.get(valeur) or {})
            apport = str(libelle.get("frontiere") or libelle.get("portee") or "")
            r.hubs_a_creer.append((dossier, dossier.rsplit("/", 1)[-1],
                                   " ".join(apport.split())))
    for valeur in r.depromotions:
        dossier = chemins.dossier_attendu(valeur, r.promus_avant, mo)
        if dossier and dossier in existants:
            r.hubs_orphelins.append(chemins.hub_du_dossier(dossier))
    return r


def applique(mo: Modele, racine: Path, r: Reseuillage) -> Reseuillage:
    """Les `git mv`, puis les hubs des dossiers nouvellement promus.

    Refuse sur un arbre SALE : un `git mv` melange a des modifications non
    committees rend le retour en arriere illisible, et une migration dont on ne
    peut pas sortir n est pas une migration.
    """
    propre, sortie = _depot.etat(racine)
    if not propre:
        r.refus.append("l'arbre de travail n'est pas propre — `re-seuiller` "
                       "déplace des fichiers, et un déplacement mêlé à des "
                       "modifications non committées ne se défait pas :\n"
                       + "\n".join(f"    {l}" for l in sortie.splitlines()[:10]))
        return r
    if r.refus:
        return r

    for m in r.mouvements:
        (racine / m.vers).parent.mkdir(parents=True, exist_ok=True)
        code, out = _depot._git(racine, "mv", m.depuis, m.vers)
        if code != 0:
            r.refus.append(f"`git mv {m.depuis} {m.vers}` a échoué :\n{out}")
            return r

    prose = ProseSemis(mo)
    # Le plan de semis refuse un dossier non vide, et c est sa raison d etre.
    # Ici on ecrit DANS un vault existant : on desactive le controle de CIBLE,
    # jamais celui d ecriture unique.
    plan = Plan(racine=racine, ecrire=True, controle_la_cible=False)
    for dossier, titre, apport in r.hubs_a_creer:
        texte = _pages.hub(mo, prose, titre,
                           apport or prose.ligne("semis.hub.apport_arbre",
                                                 libelle=titre,
                                                 axe_rangement=mo.libelle_rangement
                                                 .get("s") or ""))
        plan.pose(chemins.hub_du_dossier(dossier), texte, "reseuillage")
    r.refus += plan.refus
    r.applique = not r.refus
    return r


# --------------------------------------------------------------------------- #
def imprime(r: Reseuillage, racine: Path, detail: int = 20) -> int:
    print(f"re-seuiller — vault `{racine.name}` : seuil {r.seuil_actuel} → "
          f"{r.seuil_vise}"
          + ("  [APPLIQUÉ]" if r.applique else "  [simulation, rien n'est écrit]"))
    print(f"  sous-valeurs promues   avant : {len(r.promus_avant):3d}   "
          f"après : {len(r.promus_apres):3d}")
    if r.promotions:
        print(f"  {len(r.promotions)} promotion(s) : "
              + ", ".join(f"`{v}`" for v in r.promotions[:detail]))
    if r.depromotions:
        print(f"  {len(r.depromotions)} dépromotion(s) : "
              + ", ".join(f"`{v}`" for v in r.depromotions[:detail]))

    if r.mouvements:
        print(f"\n{len(r.mouvements)} page(s) à déplacer — par `git mv`, "
              f"jamais par suppression + création :")
        for m in r.mouvements[:detail]:
            print(f"  git mv \"{m.depuis}\" \"{m.vers}\"")
        if len(r.mouvements) > detail:
            print(f"  … {len(r.mouvements) - detail} autre(s)")
    if r.hubs_a_creer:
        print(f"\n{len(r.hubs_a_creer)} hub(s) à créer — sans eux, "
              f"`hub_par_niveau` (DURE) serait violée :")
        for dossier, _titre, _ in r.hubs_a_creer[:detail]:
            print(f"  {chemins.hub_du_dossier(dossier)}")
    if r.hubs_orphelins:
        print(f"\n{len(r.hubs_orphelins)} hub(s) SANS DOSSIER après la migration. "
              f"Ils ne sont PAS supprimés — une suppression de page se demande :")
        for h in r.hubs_orphelins[:detail]:
            print(f"  {h}")
    if r.sans_libelle:
        print(f"\n{len(r.sans_libelle)} sous-valeur(s) au-dessus du seuil sans "
              f"`libelle:` déclaré — le nom d'un dossier ne se devine pas :")
        for x in r.sans_libelle[:detail]:
            print(f"  {x}")

    if r.refus:
        print(f"\n{len(r.refus)} refus :")
        for x in r.refus:
            print(f"  [REFUS] {x}")
        return 1
    if r.sans_effet:
        print("\nOK — aucun `git mv` : le changement de seuil ne reforme rien.")
        return 0
    if r.applique:
        print(f"\nOK — {len(r.mouvements)} déplacement(s) et "
              f"{len(r.hubs_a_creer)} hub(s) écrits. Régénérer puis valider avant "
              f"de committer.")
    else:
        print("\nOK — simulation. Relancer avec `--appliquer` pour exécuter, "
              "sur un arbre de travail PROPRE.")
    return 0
