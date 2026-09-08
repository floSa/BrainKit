# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""generation.py — le jeu d epreuve des GENERATEURS (lot 4).

    uv run tests/generation.py
    uv run tests/generation.py --vault-devbrain ../DevBrain

Sept scenarios. Les quatre premiers opposent deux vaults JUMEAUX —
`tests/genere-vert/` et `tests/genere-rouge/` — qui ne different que par les huit
defauts que le rouge porte volontairement. Un jeu d epreuve qui n aurait qu un
vault perime prouverait qu un generateur CRIE ; il ne prouverait jamais qu il se
taise quand il faut, et c est la moitie qui compte pour un `--check`.

  1. VERT      — les trois formes de zone AUTO et les DEUX axes transverses,
                 tous conformes : zero ecart, zero refus, et la forme de chacune
                 des trois verifiee sur son contenu. Plus le cas qui passe pour
                 une valeur d axe DECLAREE et portee par aucune page : aucun hub
                 ne doit naitre pour elle.
  2. ROUGE     — huit defauts : SIX ecarts voulus (un par forme, un par axe, un
                 bandeau, un index), un SEPTIEME ecart derive qu il faut avoir
                 prevu, et DEUX refus. Les ensembles sont EXACTS : un constat de
                 plus ou de moins fait echouer le scenario.
  3. UN AXE    — le second axe transverse retire EN MEMOIRE. Ses deux hubs
                 cessent d etre poses, les deux autres restent. C est la preuve
                 que la boucle porte sur `axes.transverses[]` et non sur une
                 constante (rupture 4 du test a blanc).
  4. ZERO AXE  — les deux axes retires EN MEMOIRE. Aucun hub transverse pose, et
                 aucun dossier cree. « Zero axe transverse est legal » n est pas
                 une phrase du cadrage, c est un comportement.
  5. REPARATION — le vault rouge, copie hors du depot, repare par `--ecrire` :
                 il devient identique au vert page par page, SAUF les deux pages
                 que le generateur refuse de deviner. Relance : zero octet
                 ecrit. C est l idempotence, mesuree et pas affirmee.
  6. LOT 3     — le vault vert du lot 3 reste vert APRES generation, et
                 `--check` y est silencieux. Plus le cas negatif du perimetre :
                 son manifeste ne declare ni index, ni carte des liens, ni
                 bandeau, et les trois REFUSENT au lieu d inventer un chemin.
  7. DEVBRAIN  — facultatif : le critere d acceptation du lot, sur le vrai
                 vault. Saute si le vault n est pas la.

Les mutations des scenarios 3 et 4 ne touchent AUCUN fichier : elles modifient le
dictionnaire charge, une cle chacune, et le disent.
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit.generer import charge_corpus, genere_tout            # noqa: E402
from brainkit.generer.index import catalogue                       # noqa: E402
from brainkit.generer.sortie import CHECK, ECRIRE                  # noqa: E402
from brainkit.valider import valide                                # noqa: E402
from brainkit.valider.manifeste import Modele                      # noqa: E402

MANIFESTE = RACINE_KIT / "tests" / "generation.brain.yml"
VERT = RACINE_KIT / "tests" / "genere-vert"
ROUGE = RACINE_KIT / "tests" / "genere-rouge"
MANIFESTE_LOT3 = RACINE_KIT / "tests" / "epreuve.brain.yml"
VERT_LOT3 = RACINE_KIT / "tests" / "vert"

# --------------------------------------------------------------------------- #
# Le vault VERT : 16 artefacts, et les quatre hubs transverses attendus.
# --------------------------------------------------------------------------- #
VERT_ARTEFACTS = 16
HUBS_TRANSVERSES = {
    "Thèmes/Pouvoir et institutions.md",
    "Thèmes/Guerres et armées.md",
    "Espaces/Méditerranée.md",
    "Espaces/Europe.md",
}
HUBS_DU_SECOND_AXE = {"Espaces/Méditerranée.md", "Espaces/Europe.md"}
# `religieux` est DECLAREE dans le manifeste et portee par aucune page : aucun
# hub ne doit naitre pour elle. Un hub vide dans un graphe est un noeud de plus
# qui ne rassemble rien.
HUB_INTERDIT = "Thèmes/Croyances et religions.md"

# --------------------------------------------------------------------------- #
# Le vault ROUGE : sept ecarts, et il faut savoir lequel des sept n a pas ete
# pose a la main.
# --------------------------------------------------------------------------- #
ROUGE_ECARTS = {
    # 1 — forme ARBRE : la sous-section des vues a disparu de la zone
    "Antiquité/Rome/Rome.md",
    # 2 — forme RALLIEMENT : groupe par le sous-dossier au lieu du premier segment
    "Chronologies/Chronologies.md",
    # 3 — forme TRANSVERSE, axe 1 (`themes`) : un compte faux
    "Thèmes/Guerres et armées.md",
    # 4 — forme TRANSVERSE, axe 2 (`espaces`) : une puce manquante
    "Espaces/Europe.md",
    # 5 — BANDEAU : une cellule qui ne derive plus du frontmatter
    "XXe siècle/Kennan - Le long telegramme.md",
    # 6 — INDEX humain : une entree retiree
    "AI/index/brain-index.md",
    # 7 — DERIVE, et c est le seul interessant : personne ne l a pose a la main.
    #     Le defaut 1 a retire un WIKILINK d une zone AUTO, donc les liens
    #     sortants du hub « Rome » ont change, donc la carte des liens est
    #     perimee — sans qu on y ait touche. C est exactement la raison pour
    #     laquelle l orchestration tourne jusqu a un POINT FIXE en ecriture : une
    #     zone AUTO porte des liens, et la carte des liens les compte.
    "AI/index/liens.md",
}
ROUGE_REFUS = {
    # 8 — un hub SANS zone AUTO : un REFUS, pas un ecart. La zone ne s invente
    #     pas dans un hub qui n en declare pas.
    "Transversal/Transversal.md",
    # 9 — une page SANS titre de niveau 1 : un REFUS. La place d une zone dans
    #     une page sans titre n est pas devinable, et l inventer casse la page.
    "Antiquité/Herodote - Histoires.md",
}
# Les deux pages que le generateur REFUSE de reparer : le scenario 5 les exclut
# de sa comparaison, et c est le comportement voulu.
NON_REPARABLES = ROUGE_REFUS


def charge_dict(chemin: Path = MANIFESTE) -> dict:
    with chemin.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def poses(s) -> set[str]:
    return {p.chemin for p in s.poses}


def ecarts(s) -> set[str]:
    return {p.chemin for p in s.ecarts()}


def _forme(s, forme: str) -> set[str]:
    return {p.chemin for p in s.poses if p.forme == forme}


def refus_pages(s) -> set[str]:
    """Les chemins nommes par les refus. Un refus est une phrase, pas un objet.

    Volontairement lu par prefixe : le message d un refus est destine a un
    humain, et le figer dans le test en ferait un contrat de formulation.
    """
    return {r.split(" : ", 1)[0] for r in s.refus if " : " in r}


class Journal:
    def __init__(self) -> None:
        self.echecs: list[str] = []

    def verifie(self, nom: str, ok: bool, detail: str = "") -> None:
        print(f"  {'OK    ' if ok else 'ÉCHEC '} {nom}")
        if not ok:
            self.echecs.append(nom)
            for ligne in detail.splitlines():
                print(f"         {ligne}")


def _ensemble(nom: str, reel: set[str], attendu: set[str], j: Journal) -> None:
    detail = ""
    if attendu - reel:
        detail += "attendus et absents :\n" + "\n".join(
            f"  {x}" for x in sorted(attendu - reel)) + "\n"
    if reel - attendu:
        detail += "trouvés et non attendus :\n" + "\n".join(
            f"  {x}" for x in sorted(reel - attendu))
    j.verifie(nom, reel == attendu, detail)


# --------------------------------------------------------------------------- #
def scenario_vert(j: Journal) -> None:
    print("\n1. VERT — les trois formes et les deux axes, tous conformes")
    mo = Modele(charge_dict(), MANIFESTE)
    s = genere_tout(mo, VERT, mode=CHECK)
    j.verifie(f"les {VERT_ARTEFACTS} artefacts concordent, zéro écart",
              not s.ecarts() and len(s.poses) == VERT_ARTEFACTS,
              f"{len(s.poses)} posé(s), écarts : {sorted(ecarts(s))}")
    j.verifie("zéro refus — aucun hub sans zone, aucune page sans titre",
              not s.refus, "\n".join(s.refus))

    p = poses(s)
    _ensemble("les 4 hubs transverses, deux par axe", _forme(s, "transverse"),
              HUBS_TRANSVERSES, j)
    j.verifie("une valeur d'axe déclarée et non portée ne crée AUCUN hub",
              HUB_INTERDIT not in p and not (VERT / HUB_INTERDIT).exists())

    # Les trois FORMES, verifiees sur leur contenu et non sur leur seul compte :
    # une forme qui regresserait en une autre concorderait encore avec elle-meme.
    arbre = (VERT / "Antiquité/Rome/Rome.md").read_text(encoding="utf-8")
    j.verifie("forme ARBRE : les sous-sections déclarées, dans l'ordre déclaré",
              arbre.index("### Notions") < arbre.index("### Sources")
              < arbre.index("### Chronologies"))
    ralliement = (VERT / "Chronologies/Chronologies.md").read_text(encoding="utf-8")
    j.verifie("forme RALLIEMENT : groupée par le PREMIER segment du chemin",
              "### Antiquité" in ralliement and "### Rome" not in ralliement)
    transverse = (VERT / "Thèmes/Pouvoir et institutions.md").read_text(
        encoding="utf-8")
    j.verifie("forme TRANSVERSE : une phrase d'intro, puis une puce par groupe",
              "Axe thème **Pouvoir et institutions** (`politique`)" in transverse
              and "— 3 page(s)" in transverse
              and "###" not in transverse.split("<!-- AUTO:START -->")[1])

    v = valide(mo, VERT)
    j.verifie("le vault généré est VERT pour le validateur", not v.dures,
              "\n".join(sorted(f"{c.regle} — {c.page}" for c in v.dures)))


def scenario_rouge(j: Journal) -> None:
    print("\n2. ROUGE — sept écarts et deux refus, exactement")
    mo = Modele(charge_dict(), MANIFESTE)
    s = genere_tout(mo, ROUGE, mode=CHECK)
    _ensemble(f"les {len(ROUGE_ECARTS)} écarts, et eux seuls", ecarts(s),
              ROUGE_ECARTS, j)
    _ensemble(f"les {len(ROUGE_REFUS)} refus, et eux seuls", refus_pages(s),
              ROUGE_REFUS, j)
    # Un refus n est PAS un ecart : melanger les deux ferait passer un
    # generateur qui n a pas tourne pour un generateur qui n a rien trouve.
    j.verifie("un refus n'est jamais compté comme un écart",
              not (refus_pages(s) & ecarts(s)),
              f"les deux : {sorted(refus_pages(s) & ecarts(s))}")


def scenario_un_axe(j: Journal) -> None:
    print("\n3. UN AXE — le second axe transverse retiré en mémoire")
    brut = charge_dict()
    retire = brut["axes"]["transverses"].pop()          # LA mutation, une clé
    j.verifie("c'est bien le second axe qui est retiré", retire["champ"] == "espaces")
    s = genere_tout(Modele(brut, MANIFESTE), VERT, mode=CHECK)
    # Le test porte sur la FORME de la pose, pas sur sa presence : les deux pages
    # existent toujours sur le disque, et l axe retire, elles retombent dans la
    # forme ARBRE comme les hubs de n importe quel dossier. C est le
    # comportement voulu, et c est ce que `Pose.forme` permet de distinguer.
    j.verifie("les 2 hubs du second axe ne sont plus posés EN FORME TRANSVERSE",
              not (_forme(s, "transverse") & HUBS_DU_SECOND_AXE),
              f"encore transverses : {sorted(_forme(s, 'transverse') & HUBS_DU_SECOND_AXE)}")
    j.verifie("les 2 hubs du premier axe le sont toujours",
              (HUBS_TRANSVERSES - HUBS_DU_SECOND_AXE) <= _forme(s, "transverse"))


def scenario_zero_axe(j: Journal) -> None:
    print("\n4. ZÉRO AXE — les deux axes retirés en mémoire")
    brut = charge_dict()
    brut["axes"]["transverses"] = []                    # LA mutation, une clé
    s = genere_tout(Modele(brut, MANIFESTE), VERT, mode=CHECK)
    j.verifie("aucune pose en forme transverse, et aucun dossier créé",
              not _forme(s, "transverse"),
              f"posés : {sorted(_forme(s, 'transverse'))}")
    j.verifie("les 12 autres artefacts concordent — seuls les 4 hubs retombent "
              "en forme arbre",
              ecarts(s) == HUBS_TRANSVERSES, f"écarts : {sorted(ecarts(s))}")


def scenario_reparation(j: Journal) -> None:
    print("\n5. RÉPARATION — le rouge réparé hors du dépôt, puis relancé")
    mo = Modele(charge_dict(), MANIFESTE)
    base = Path(tempfile.mkdtemp(prefix="bk4-"))
    travail = base / "rouge"
    shutil.copytree(ROUGE, travail)
    try:
        s1 = genere_tout(mo, travail, mode=ECRIRE)
        j.verifie("la réparation écrit, et atteint son point fixe",
                  s1.passes >= 1 and not s1.ecarts(),
                  f"{s1.passes} passe(s), écarts restants : {sorted(ecarts(s1))}")

        differents = []
        for p in sorted(VERT.rglob("*")):
            if not p.is_file():
                continue
            rel = p.relative_to(VERT).as_posix()
            if rel in NON_REPARABLES:
                continue
            autre = travail / rel
            if not autre.is_file() or not filecmp.cmp(p, autre, shallow=False):
                differents.append(rel)
        j.verifie("le vault réparé est identique au vert, page par page",
                  not differents, "\n".join(differents))
        j.verifie("sauf les 2 pages que le générateur REFUSE de deviner",
                  all((travail / r).is_file() for r in NON_REPARABLES))

        s2 = genere_tout(mo, travail, mode=ECRIRE)
        ecrits = [p.chemin for p in s2.poses if p.etat != "identique"]
        j.verifie("relancé sur un vault à jour : ZÉRO octet écrit", not ecrits,
                  "\n".join(ecrits))
    finally:
        shutil.rmtree(base, ignore_errors=True)


def scenario_lot3(j: Journal) -> None:
    print("\n6. LOT 3 — le vault vert du lot 3, et le périmètre par la négative")
    mo = Modele(charge_dict(MANIFESTE_LOT3), MANIFESTE_LOT3)
    s = genere_tout(mo, VERT_LOT3, mode=CHECK, quoi=("hubs",))
    j.verifie("`--check` est SILENCIEUX sur les 4 hubs du vault vert du lot 3",
              not s.ecarts() and not s.refus,
              f"écarts : {sorted(ecarts(s))} · refus : {s.refus}")
    v = valide(mo, VERT_LOT3)
    j.verifie("et il reste vert : zéro dure, zéro avertissement",
              not v.dures and not v.avertissements,
              "\n".join(sorted(c.rendu() for c in v.dures + v.avertissements)))

    # Le cas NEGATIF du perimetre : ce manifeste ne declare ni index, ni carte
    # des liens, ni bandeau. Les trois doivent REFUSER, pas inventer un chemin.
    s2 = genere_tout(mo, VERT_LOT3, mode=CHECK)
    j.verifie("les 3 artefacts NON déclarés refusent au lieu d'inventer un chemin",
              len(s2.refus) == 3,
              f"{len(s2.refus)} refus : " + " | ".join(s2.refus))
    j.verifie("et zéro axe transverse déclaré ne crée aucun dossier",
              not any(p.chemin.startswith(("Thèmes/", "Métiers/"))
                      for p in s2.poses))


def scenario_devbrain(j: Journal, vault: Path) -> None:
    print(f"\n7. DEVBRAIN — le critère d'acceptation, sur `{vault.name}`")
    chemin = RACINE_KIT / "exemples" / "devbrain.brain.yml"
    mo = Modele(yaml.safe_load(chemin.read_text(encoding="utf-8")), chemin)
    s = genere_tout(mo, vault, mode=CHECK)
    par = s.par_artefact()
    j.verifie("les 337 bandeaux concordent", par.get("bandeau", (0, 1, 0))[1] == 0,
              str(par.get("bandeau")))
    j.verifie("les 74 zones AUTO de hub concordent",
              par.get("hubs", (0, 1, 0))[1] == 0, str(par.get("hubs")))
    j.verifie("la carte des liens concorde", par.get("liens", (0, 1, 0))[1] == 0,
              str(par.get("liens")))
    j.verifie("le document humain de l'index concorde",
              "AI/index/brain-index.md" not in ecarts(s), str(sorted(ecarts(s))))
    j.verifie("zéro refus sur 765 pages", not s.refus, "\n".join(s.refus))

    # Au plus UN ecart, et sa preuve — la verification tient AVANT et APRES le
    # lot 9, parce que c est le meme fait qu elle regarde des deux cotes.
    #
    #   AVANT  le catalogue committe annonce 26 dossiers balayes, dont deux qui
    #          ne portent aucune page : `.githooks`, et un dossier de sauvegarde
    #          qui n existe meme plus sur le disque. L ecart vaut 2 lignes.
    #   APRES  le lot 9 a regenere le catalogue avec la cle corrigee, et l ecart
    #          est nul.
    #
    # Dans les deux cas, la difference tient ENTIEREMENT a ces deux noms : les
    # reinjecter en memoire rend l octet du fichier committe. C est ce que la
    # seconde verification etablit, et c est ce qui prouve que le generateur
    # n a change que la cle `scanned`.
    j.verifie("au plus un écart : le catalogue machine",
              ecarts(s) <= {"AI/index/brain-index.json"}, str(sorted(ecarts(s))))
    c = charge_corpus(mo, vault)
    reel = (vault / "AI" / "index" / "brain-index.json").read_text(encoding="utf-8")
    j.verifie("et il tient aux SEULS dossiers sans page de `scanned`",
              catalogue(c) == reel
              or _avec_sans_page(c, catalogue, reel,
                                 [".githooks", "obsidian_outer_backup_20260907"]))


def _avec_sans_page(corpus, fabrique, reel: str, noms: list[str]) -> bool:
    corpus.scannes = sorted(set(corpus.scannes) | set(noms))
    return fabrique(corpus) == reel


# --------------------------------------------------------------------------- #
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(description="Le jeu d'épreuve des générateurs.")
    ap.add_argument("--vault-devbrain", type=Path,
                    default=RACINE_KIT.parent / "DevBrain")
    ns = ap.parse_args()

    print("épreuve — les générateurs de BrainKit, lot 4")
    j = Journal()
    scenario_vert(j)
    scenario_rouge(j)
    scenario_un_axe(j)
    scenario_zero_axe(j)
    scenario_reparation(j)
    scenario_lot3(j)
    if ns.vault_devbrain.is_dir():
        scenario_devbrain(j, ns.vault_devbrain.resolve())
    else:
        print(f"\n7. DEVBRAIN — sauté : `{ns.vault_devbrain}` introuvable")

    print()
    if j.echecs:
        print(f"{len(j.echecs)} vérification(s) en échec :")
        for e in j.echecs:
            print(f"  - {e}")
        return 1
    print("OK — le jeu d'épreuve des générateurs passe en entier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
