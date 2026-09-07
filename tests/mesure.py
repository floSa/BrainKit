# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""mesure.py — le jeu d epreuve de la passe de mesure (lot 8).

    uv run tests/mesure.py
    uv run tests/mesure.py --vault-devbrain ../DevBrain
    uv run tests/mesure.py --vault-histobrain <chemin>

Neuf scenarios. Le premier est le CONTROLE NEGATIF, et il est le plus important
du lot : un outil qui durcirait un brain de dix pages transformerait chaque
regle en superstition. Les scenarios 1 et 2 sont donc jumeaux — le MEME vault,
la MEME mesure, et une seule chose qui change : le plancher. Sans le second, on
prouverait que l outil ne propose rien, jamais ; avec lui, on prouve que c est
bien le plancher qui l en empeche.

  1. PLANCHER       — vault de six unites : AUCUNE proposition, et le refus dit
                      combien de pages il manque.
  2. PLANCHER BAISSE— le meme vault, `PLANCHER_PAGES` abaisse EN MEMOIRE. Les
                      propositions apparaissent : c etait bien le plancher.
  3. POPULATION     — le denominateur d une regle est le sien, pas celui du
                      vault ; et une regle a population nulle reste refusee meme
                      sous un plancher a 1. C est la seconde lecture du
                      garde-fou 1.
  4. MOTIF          — garde-fou 2 : une severite `avertissement` sans motif est
                      REFUSEE, et le refus disparait des qu un motif est ecrit.
  5. STRUCTURELLE   — garde-fou 3 : la liste est fermee par le kit. Un manifeste
                      qui declare `structurellement_dure: false` est CONTREDIT,
                      et la regle n est jamais proposee, meme plancher baisse.
  6. GABARIT        — la forme mesurable d `existe_si` : presence et
                      remplissage, sous-arbre compris, et une section CONTENEUR
                      n est pas declaree morte.
  7. LECTURE SEULE  — mesurer ne touche aucun octet du vault.
  8. DEVBRAIN       — facultatif : le recensement du lot 3 retrouve, les comptes
                      du lot 8 du DevBrain confrontes, et le refus du garde-fou 2
                      nomme ses deux regles.
  9. HISTOBRAIN     — facultatif : le controle negatif sur le vrai vault d essai.

Les mutations des scenarios 2 a 5 sont EN MEMOIRE : une cle du dictionnaire
charge, ou une constante du module de garde-fous, remise en place aussitot.
Aucun fichier n est touche.
"""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit.mesurer import gardes, mesure            # noqa: E402
from brainkit.valider.manifeste import Modele          # noqa: E402

MANIFESTE = RACINE_KIT / "tests" / "epreuve.brain.yml"
VERT = RACINE_KIT / "tests" / "vert"
DATE = "2026-09-07"

# Les comptes du lot 8 du DevBrain, tels que le lot 3 les a confrontes au vault.
# Le troisieme est DATE : le lot 8 annoncait « 11 candidats dont 2 vrais », le
# vault dit 4 depuis le 2026-09-07 — sept candidats ont disparu par reecriture
# des sections de definition. C est le vault qui a raison.
DEVBRAIN_HISTORIQUE = {
    ("voisinage_declare", ""): 62,
    ("etiquettes_fermees", "Ressources"): 5,
    ("anti_repetition", ""): 4,
}

# Les deux regles du DevBrain qui restent en avertissement sans qu aucun motif
# n ait jamais ete ecrit. Le garde-fou 2 les REFUSE, et c est la premiere fois
# qu on les voit.
DEVBRAIN_SANS_MOTIF = {"taille_avertissement", "collision_alias"}


def charge_dict() -> dict:
    with MANIFESTE.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def modele(brut: dict | None = None) -> Modele:
    return Modele(brut if brut is not None else charge_dict(), MANIFESTE)


def ligne(m, rid: str, cle: str = ""):
    for li in m.lignes:
        if li.regle == rid and li.cle == cle:
            return li
    return None


class Journal:
    def __init__(self) -> None:
        self.echecs: list[str] = []

    def verifie(self, nom: str, ok: bool, detail: str = "") -> None:
        print(f"  {'OK    ' if ok else 'ÉCHEC '} {nom}")
        if not ok:
            self.echecs.append(nom)
            for l in detail.splitlines():
                print(f"         {l}")


class PlancherBaisse:
    """Abaisse `PLANCHER_PAGES` le temps d un bloc, et le remet."""

    def __init__(self, n: int) -> None:
        self.n, self.avant = n, gardes.PLANCHER_PAGES

    def __enter__(self):
        gardes.PLANCHER_PAGES = self.n
        return self

    def __exit__(self, *_):
        gardes.PLANCHER_PAGES = self.avant
        return False


# --------------------------------------------------------------------------- #
def scenario_plancher(j: Journal) -> None:
    print("\n1. PLANCHER — le contrôle négatif")
    m, _rec, _occ, _bl = mesure(modele(), VERT, date=DATE)
    j.verifie("le vault porte 6 pages de l'unité, sous le plancher de 30",
              m.pages_de_l_unite == 6 and not m.plancher_tenu,
              f"unité `{m.role_unite}` : {m.pages_de_l_unite} page(s)")
    j.verifie("AUCUNE proposition de durcissement", not m.propositions,
              "proposé : " + ", ".join(x.id_affiche for x in m.propositions))
    refuses = m.par_verdict(gardes.REFUS_INSTANCE)
    j.verifie("des règles sont refusées, nommément, par le plancher d'instance",
              len(refuses) >= 2,
              f"refusées : {[x.id_affiche for x in refuses]}")
    j.verifie("le refus chiffre ce qui manque : 24 pages",
              gardes.manque_au_plancher(m.pages_de_l_unite) == 24)


def scenario_plancher_baisse(j: Journal) -> None:
    print("\n2. PLANCHER BAISSÉ — le même vault, le plancher abaissé en mémoire")
    with PlancherBaisse(1):
        m, _rec, _occ, _bl = mesure(modele(), VERT, date=DATE)
    proposes = {x.id_affiche for x in m.propositions}
    j.verifie("le plancher tenu, les propositions apparaissent", bool(proposes),
              "aucune proposition — le refus du scénario 1 ne venait donc pas "
              "du plancher")
    j.verifie("`taille_avertissement` est proposée — 0 violation sur 9 pages",
              "taille_avertissement" in proposes, f"proposé : {sorted(proposes)}")
    li = ligne(m, "taille_avertissement")
    bloc = "\n".join(li.bloc_a_coller(DATE))
    j.verifie("le bloc à coller porte un `motif:` VIDE — garde-fou 2, corollaire",
              "À ÉCRIRE" in bloc and "severite: dure" in bloc, bloc)
    j.verifie("le bloc porte la date et la population MESURÉE",
              f'date: "{DATE}"' in bloc and "population: 9" in bloc, bloc)


def scenario_population(j: Journal) -> None:
    print("\n3. POPULATION — le dénominateur est celui de la RÈGLE")
    m, _rec, _occ, _bl = mesure(modele(), VERT, date=DATE)
    total = m.pages_totales
    hub = ligne(m, "hub_par_niveau")
    frontmatter = ligne(m, "frontmatter_lisible")
    j.verifie("une règle qui lit toutes les pages déclare le total",
              frontmatter.pages == total, f"{frontmatter.pages} != {total}")
    j.verifie("une règle de portée étroite déclare MOINS que le total",
              0 < hub.pages < total, f"hub_par_niveau : {hub.pages} / {total}")
    paire = ligne(m, "paire_inverse_bien_declaree")
    j.verifie("une règle vérifiable sur le MANIFESTE ne compte pas des pages",
              paire.sur_le_manifeste and paire.pages == 0,
              f"pages={paire.pages} sur_le_manifeste={paire.sur_le_manifeste}")
    # La SECONDE lecture du plancher : meme sous un plancher a 1, une regle qui
    # n a rien mesure n a rien prouve.
    with PlancherBaisse(1):
        m2, _r, _o, _b = mesure(modele(), VERT, date=DATE)
    alias = ligne(m2, "collision_alias")
    j.verifie("plancher à 1 : une règle à population NULLE reste refusée",
              alias.pages == 0 and alias.verdict == gardes.REFUS_POPULATION,
              f"pages={alias.pages} verdict={alias.verdict}")


def scenario_motif(j: Journal) -> None:
    print("\n4. MOTIF — garde-fou 2, le kit REFUSE")
    brut = charge_dict()
    for r in brut["regles"]:
        if r["id"] == "etiquettes_fermees":
            r["severite"] = "avertissement"             # LA mutation, une clé
    m, _rec, _occ, _bl = mesure(modele(brut), VERT, date=DATE)
    noms = {x.regle for x in m.sans_motif}
    j.verifie("une sévérité `avertissement` sans motif est REFUSÉE",
              "etiquettes_fermees" in noms, f"refusées : {sorted(noms)}")

    brut2 = copy.deepcopy(brut)
    for r in brut2["regles"]:
        if r["id"] == "etiquettes_fermees":
            r["motif"] = ("Cinq étiquettes nommées par l'utilisateur ; ouvrir le "
                          "vocabulaire pour faire passer la règle serait ajouter "
                          "une exception, pas la respecter.")
    m2, _r, _o, _b = mesure(modele(brut2), VERT, date=DATE)
    j.verifie("le motif écrit, le refus disparaît",
              not any(x.regle == "etiquettes_fermees" for x in m2.sans_motif),
              f"refusées : {[x.id_affiche for x in m2.sans_motif]}")
    # `note_<x>` compte aussi : la propriete 2 du manifeste dit qu une valeur
    # porte son motif sous n importe laquelle de ces formes.
    brut3 = copy.deepcopy(brut)
    for r in brut3["regles"]:
        if r["id"] == "etiquettes_fermees":
            r["note_severite"] = "Souple tant que le vocabulaire n'est pas arrêté."
    m3, _r, _o, _b = mesure(modele(brut3), VERT, date=DATE)
    j.verifie("une annotation `note_<x>` vaut motif — propriété 2 du manifeste",
              not any(x.regle == "etiquettes_fermees" for x in m3.sans_motif))


def scenario_structurelle(j: Journal) -> None:
    print("\n5. STRUCTURELLE — garde-fou 3, la liste est fermée par le kit")
    brut = charge_dict()
    for r in brut["regles"]:
        if r["id"] == "chemin_categorie":
            r["severite"] = "a_mesurer"                 # LES deux mutations
            r["structurellement_dure"] = False
    m, _rec, _occ, _bl = mesure(modele(brut), VERT, date=DATE)
    j.verifie("un manifeste qui contredit le garde-fou 3 est SIGNALÉ",
              any("chemin_categorie" in c for c in m.contradictions),
              f"contradictions : {m.contradictions}")
    li = ligne(m, "chemin_categorie")
    j.verifie("elle sort du régime de la mesure",
              li.verdict == gardes.STRUCTURELLE, f"verdict={li.verdict}")
    with PlancherBaisse(1):
        m2, _r, _o, _b = mesure(modele(copy.deepcopy(brut)), VERT, date=DATE)
    j.verifie("même plancher tenu, elle n'est JAMAIS proposée",
              "chemin_categorie" not in {x.regle for x in m2.propositions},
              f"proposé : {[x.id_affiche for x in m2.propositions]}")
    j.verifie("les deux structurellement dures sont bien celles de §5.6",
              gardes.STRUCTURELLEMENT_DURES
              == ("chemin_categorie", "bandeau_a_jour"))


def scenario_gabarit(j: Journal) -> None:
    print("\n6. GABARIT — la forme mesurable d'`existe_si`")
    _m, _rec, occ, _bl = mesure(modele(), VERT, date=DATE)
    par_titre = {(o.role, o.titre): o for o in occ}
    autour = par_titre.get(("source", "Autour"))
    j.verifie("une section à sous-titres déclarés est vue CONTENEUR",
              autour is not None and autour.conteneur,
              f"{autour}")
    j.verifie("… et son sous-arbre est lu : elle n'est pas déclarée morte",
              autour is not None and not autour.morte and autour.remplies > 0,
              f"remplies={autour.remplies if autour else '—'}")
    ce_que = par_titre.get(("source", "Ce que c'est"))
    j.verifie("une section universelle est mesurée présente ET remplie partout",
              ce_que is not None and ce_que.presentes == ce_que.population
              and ce_que.remplies == ce_que.population, f"{ce_que}")
    partielle = par_titre.get(("source", "Prolonge"))
    j.verifie("une section absente de la plupart des pages est mesurée comme telle",
              partielle is not None
              and 0 < partielle.presentes < partielle.population,
              f"{partielle}")
    j.verifie("aucun marqueur de place (`niveau: 0`) n'est compté comme section",
              not any(o.titre.startswith("<") for o in occ),
              f"{[o.titre for o in occ if o.titre.startswith('<')]}")


def scenario_lecture_seule(j: Journal) -> None:
    print("\n7. LECTURE SEULE — mesurer ne touche aucun octet")
    def empreinte() -> dict:
        return {p.relative_to(VERT).as_posix(): (p.stat().st_size,
                                                 p.stat().st_mtime_ns)
                for p in sorted(VERT.rglob("*")) if p.is_file()}
    avant = empreinte()
    mesure(modele(), VERT, date=DATE)
    apres = empreinte()
    j.verifie(f"les {len(avant)} fichiers du vault sont inchangés", avant == apres,
              "\n".join(sorted(set(avant) ^ set(apres))
                        or [f"{k} : {avant[k]} -> {apres[k]}"
                            for k in avant if avant[k] != apres[k]]))


def scenario_devbrain(j: Journal, vault: Path, manifeste: Path) -> None:
    print(f"\n8. DEVBRAIN — les comptes du lot 8, confrontés au vault `{vault.name}`")
    mo = Modele(yaml.safe_load(manifeste.read_text(encoding="utf-8")), manifeste)
    m, rec, occ, bl = mesure(mo, vault, date=DATE)

    j.verifie("le plancher est LARGEMENT tenu : 337 pages de l'unité",
              m.pages_de_l_unite == 337 and m.plancher_tenu,
              f"{m.pages_de_l_unite} page(s) de `{m.role_unite}`")

    # Le recensement de `check_arbo`, ecarte par le lot 3, remis ici.
    j.verifie("le recensement retrouve « 681 pages dans 20 dossiers, 10 par rôle »",
              (rec.total_axe, len(rec.par_axe), rec.total_role) == (681, 20, 10),
              f"{rec.total_axe} / {len(rec.par_axe)} / {rec.total_role}")
    j.verifie("… et les 74 hubs, comptés à part parce qu'ils ne se rangent pas",
              rec.total_hubs == 74, f"{rec.total_hubs} hub(s)")

    for (rid, cle), attendu in sorted(DEVBRAIN_HISTORIQUE.items()):
        li = ligne(m, rid, cle)
        nom = f"{rid}/{cle}" if cle else rid
        j.verifie(f"`{nom}` : {attendu} violation(s), comme l'histoire le dit",
                  li is not None and li.violations == attendu,
                  f"mesuré : {li.violations if li else '—'}")

    red = ligne(m, "redirection_sourcee")
    j.verifie("`redirection_sourcee` mesure bien 1 388 cellules",
              red.population.objets == 1388,
              f"{red.population.objets if red.population else '—'}")

    j.verifie("garde-fou 2 : le refus nomme exactement les deux règles sans motif",
              {x.regle for x in m.sans_motif} == DEVBRAIN_SANS_MOTIF,
              f"refusées : {sorted(x.regle for x in m.sans_motif)}")

    j.verifie("aucune contradiction de garde-fou 3 — les deux sont déjà dures",
              not m.contradictions, "\n".join(m.contradictions))

    mortes = {f"{o.role}.{o.titre}" for o in occ if o.morte}
    j.verifie("`brique.Retours` est mesurée MORTE : 0/337 présente, 0 remplie",
              "brique.Retours" in mortes, f"mortes : {sorted(mortes)}")

    codes = set(bl.par_code())
    j.verifie("le backlog porte `A1` et `A3` — la place que le lot 3 leur promettait",
              {"A1", "A3"} <= codes, f"codes : {sorted(codes)}")
    a1 = [e for e in bl.entrees if e.code == "A1"]
    j.verifie("les cinq `skill/*` déclarées sans page y sont, toutes les cinq",
              len(a1) == 5 and all(e.sujet.startswith("skill/") for e in a1),
              f"{[e.sujet for e in a1]}")


def scenario_histobrain(j: Journal, vault: Path) -> None:
    print(f"\n9. HISTOBRAIN — le contrôle négatif sur `{vault.name}`")
    manifeste = vault / "brain.yml"
    mo = Modele(yaml.safe_load(manifeste.read_text(encoding="utf-8")), manifeste)
    m, _rec, _occ, _bl = mesure(mo, vault, date=DATE)
    j.verifie("l'unité `source` compte 10 pages — sous le plancher",
              m.pages_de_l_unite == 10 and not m.plancher_tenu,
              f"{m.pages_de_l_unite} page(s) de `{m.role_unite}`")
    j.verifie("AUCUNE proposition de durcissement", not m.propositions,
              f"proposé : {[x.id_affiche for x in m.propositions]}")
    j.verifie("… et 20 pages manquent, dit nommément",
              gardes.manque_au_plancher(m.pages_de_l_unite) == 20)
    j.verifie("le manifeste contredit le garde-fou 3 sur ses DEUX règles",
              len(m.contradictions) == 2, "\n".join(m.contradictions))
    atteignable = ligne(m, "page_atteignable")
    j.verifie("les 13 hubs d'axe transverse inatteignables sont mesurés",
              atteignable is not None and atteignable.violations == 13,
              f"{atteignable.violations if atteignable else '—'}")


# --------------------------------------------------------------------------- #
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(description="Jeu d'épreuve de la mesure.")
    ap.add_argument("--vault-devbrain", type=Path,
                    default=RACINE_KIT.parent / "DevBrain")
    ap.add_argument("--manifeste-devbrain", type=Path,
                    default=RACINE_KIT / "exemples" / "devbrain.brain.yml")
    ap.add_argument("--vault-histobrain", type=Path, default=None)
    ns = ap.parse_args()

    print("=" * 74)
    print("jeu d'épreuve — la passe de mesure (lot 8)")
    print("=" * 74)

    j = Journal()
    scenario_plancher(j)
    scenario_plancher_baisse(j)
    scenario_population(j)
    scenario_motif(j)
    scenario_structurelle(j)
    scenario_gabarit(j)
    scenario_lecture_seule(j)

    if ns.vault_devbrain.is_dir() and ns.manifeste_devbrain.exists():
        scenario_devbrain(j, ns.vault_devbrain.resolve(),
                          ns.manifeste_devbrain)
    else:
        print(f"\n8. DEVBRAIN — sauté : `{ns.vault_devbrain}` absent")

    histo = ns.vault_histobrain
    if histo is None:
        defaut = Path.home() / "Documents" / "BrainKit-essais" / "histobrain"
        histo = defaut if (defaut / "brain.yml").exists() else None
    if histo is not None and (histo / "brain.yml").exists():
        scenario_histobrain(j, histo.resolve())
    else:
        print("\n9. HISTOBRAIN — sauté : aucune instance d'essai trouvée "
              "(`--vault-histobrain <chemin>`)")

    print()
    if j.echecs:
        print(f"ÉCHEC — {len(j.echecs)} vérification(s) :")
        for e in j.echecs:
            print(f"  - {e}")
        return 1
    print("OK — le jeu d'épreuve de la mesure passe en entier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
