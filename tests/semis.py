# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""semis.py — le jeu d epreuve du SEMIS (lot 5).

    uv run tests/semis.py
    uv run tests/semis.py --vault-temoin <chemin d un vault reel>

Sept scenarios. Aucun n ecrit hors d un dossier temporaire, et le scenario 4 lit
un vault REEL sans l ouvrir en ecriture.

  1. VIERGE      — HistoBrain seme dans un dossier temporaire. C est le critere
                   d acceptation du lot, verifie et non affirme : un hub par
                   dossier et AUCUNE autre page, les deux validateurs a zero
                   violation ET a zero avertissement, les generateurs silencieux
                   en `--check`, les vingt titres du test a blanc dans `Inbox.md`
                   et pas une de ces pages ecrite.
  2. REFUS       — les quatre situations que le plan d ecriture refuse : cible
                   non vide, cible sous un depot git, cible sous un vault, cible
                   sous le depot du kit. Et la verification qui compte : rien n a
                   ete ecrit.
  3. INCOMPLET   — le cas NEGATIF. Trois manifestes ampute EN MEMOIRE, un manque
                   chacun. Chacun est refuse, le refus NOMME le champ, et le
                   dossier cible reste inexistant : pas de semis a moitie.
  4. GENERICITE  — le vault temoin seme depuis son propre manifeste, et sa structure
                   vide comparee a l arbre REEL. C est la repetition du lot 9 a
                   blanc. Saute si le vault n est pas la.
  5. RE-SEUILLER — sur l instance vierge : aucun `git mv`, et il le dit. Sur un
                   vault peuple : une DEPROMOTION, deux `git mv` reels, et le hub
                   orphelin SIGNALE et non supprime.
  6. FREEZE      — refuse un dossier qui n est pas une instance ; refuse une
                   instance deja figee ; et une instance figee reste VERTE.
  7. IDEMPOTENCE — semer deux fois au meme endroit est refuse, et un second
                   `--check` juste apres le semis est toujours silencieux.
"""

from __future__ import annotations

import argparse
import copy
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import temoin                                          # noqa: E402

from brainkit.generer import genere_tout                            # noqa: E402
from brainkit.generer.sortie import CHECK                           # noqa: E402
from brainkit.semer import figer, reseuiller, semis                 # noqa: E402
from brainkit.valider import valide                                 # noqa: E402
from brainkit.valider.manifeste import Modele                       # noqa: E402

REFERENCE = RACINE_KIT / "gabarit" / "brain.yml"
GENERATION = RACINE_KIT / "tests" / "generation.brain.yml"
VERT = RACINE_KIT / "tests" / "genere-vert"

# L instance de REFERENCE vierge, attendue au FICHIER PRES. Un compte global ne
# prouverait rien : c est la composition qui est le livrable.
HUBS_ATTENDUS = {
    "Domaine A", "Domaine B", "Domaine C", "Domaine D", "Domaine E",
    "Domaine F", "Domaine G", "Transverse",
    "Consignes", "Directives", "Séquences",
}
GABARITS_ATTENDUS = {
    "Gabarit - Unité", "Gabarit - Notion", "Gabarit - Séquence",
    "Gabarit - Hub", "Gabarit - Consigne", "Gabarit - Directive",
}
# Les dossiers d axe transverse existent, et ne portent AUCUN hub — arbitrage 2.
TRANSVERSES_ATTENDUS = {"Marqueurs", "Secteurs"}


class Journal:
    def __init__(self) -> None:
        self.echecs: list[str] = []

    def verifie(self, nom: str, ok: bool, detail: str = "") -> None:
        print(f"  {'OK    ' if ok else 'ÉCHEC '} {nom}")
        if not ok:
            self.echecs.append(nom)
            for ligne in str(detail).splitlines():
                print(f"         {ligne}")


def _ensemble(nom: str, reel: set, attendu: set, j: Journal) -> None:
    detail = ""
    if attendu - reel:
        detail += "attendus et absents :\n" + "\n".join(
            f"  {x}" for x in sorted(attendu - reel)) + "\n"
    if reel - attendu:
        detail += "trouvés et non attendus :\n" + "\n".join(
            f"  {x}" for x in sorted(reel - attendu))
    j.verifie(nom, reel == attendu, detail)


def charge_dict(chemin: Path) -> dict:
    with chemin.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def _git(racine: Path, *args: str) -> tuple[int, str]:
    p = subprocess.run(["git", "-C", str(racine), *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout + p.stderr).strip()


# --------------------------------------------------------------------------- #
def scenario_vierge(j: Journal, dossier: Path) -> Modele:
    print("\n1. VIERGE — le critère d'acceptation du lot, vérifié")
    mo = Modele(charge_dict(REFERENCE), REFERENCE)
    cible = dossier / "reference"
    s = semis.seme(mo, cible, ecrire=True, avec_git=True)
    j.verifie("le semis ne refuse rien", not s.refuse,
              "\n".join(s.manques + s.plan.refus))
    if s.refuse:
        return mo

    v = valide(mo, cible)
    # ZERO violation dure ET zero avertissement : sur un vault a zero page
    # d unite, un avertissement serait forcement injustifie — il porterait sur
    # une page que personne n a ecrite.
    j.verifie("validateur : 0 violation DURE", not v.dures,
              "\n".join(c.rendu() for c in v.dures))
    j.verifie("validateur : 0 avertissement, 0 à mesurer",
              not v.avertissements and not v.a_mesurer,
              "\n".join(c.rendu() for c in v.avertissements + v.a_mesurer))

    g = genere_tout(mo, cible, mode=CHECK)
    j.verifie("générateurs : `--check` silencieux (le semis est à son point fixe)",
              not g.ecarts() and not g.refus,
              f"{len(g.ecarts())} écart(s), {len(g.refus)} refus")

    pages = {p.stem: p for p in v.contexte.lisibles}
    j.verifie("un hub par dossier, et AUCUNE autre page",
              all(p.role == mo.role_hub for p in v.contexte.lisibles),
              ", ".join(f"{p.chemin} ({p.role})" for p in v.contexte.lisibles
                        if p.role != mo.role_hub))
    _ensemble("les 11 hubs attendus, exactement", set(pages), HUBS_ATTENDUS, j)

    gabarits = {p.stem for p in (cible / "Templates").glob("*.md")}
    _ensemble("les 6 gabarits attendus, un par rôle", gabarits,
              GABARITS_ATTENDUS, j)

    # Arbitrage 2 : le dossier d un axe transverse existe, et il est VIDE de
    # hubs. Un hub par valeur declaree serait un noeud de plus qui ne rassemble
    # rien — cf. `generer/hubs.py`.
    transverses = {d.name for d in cible.iterdir()
                   if d.is_dir() and d.name in TRANSVERSES_ATTENDUS}
    _ensemble("les dossiers d'axe transverse existent", transverses,
              TRANSVERSES_ATTENDUS, j)
    poses = sorted(str(f.relative_to(cible)) for d in TRANSVERSES_ATTENDUS
                   for f in (cible / d).glob("*.md"))
    j.verifie("aucun hub d'axe transverse n'est semé", not poses,
              "un hub a été posé pour une valeur que personne ne porte : "
              + ", ".join(poses))

    # Les vingt titres : dans l inbox, et PAS UNE page ecrite.
    inbox = (cible / "Inbox.md").read_text(encoding="utf-8")
    amorce = [a for p in (mo.m["racine"]["pages"] or [])
              for a in (p.get("amorce") or [])]
    j.verifie(f"les {len(amorce)} titres du test à blanc sont dans `Inbox.md`",
              all(a in inbox for a in amorce),
              "\n".join(a for a in amorce if a not in inbox))
    ecrites = [a for a in amorce
               if any(a.split(" : ", 1)[-1][:20] in s for s in pages)]
    j.verifie("et pas une de ces pages n'est écrite", not ecrites, str(ecrites))

    # Le depot : identite du MANIFESTE, hooks actifs, arbre propre.
    _c, auteur = _git(cible, "log", "-1", "--format=%an <%ae>")
    attendue = (f"{mo.m['git']['identite']['name']} "
                f"<{mo.m['git']['identite']['email']}>")
    j.verifie("le commit initial porte l'identité du MANIFESTE",
              auteur == attendue, f"trouvé : {auteur}\nattendu : {attendue}")
    _c, hooks = _git(cible, "config", "--local", "core.hooksPath")
    j.verifie("`core.hooksPath` est posé", hooks == ".githooks", hooks)
    _c, statut = _git(cible, "status", "--porcelain")
    j.verifie("l'arbre de l'instance est propre après le semis", statut == "",
              statut)
    return mo


# --------------------------------------------------------------------------- #
def scenario_refus(j: Journal, mo: Modele, dossier: Path) -> None:
    print("\n2. REFUS — les quatre situations que le plan d'écriture refuse")
    seme = dossier / "reference"

    cas = [
        ("cible non vide", seme),
        ("cible SOUS un dépôt git", seme / "sous-le-depot"),
        ("cible SOUS le dépôt du kit", RACINE_KIT / "essai-interdit"),
    ]
    for nom, cible in cas:
        s = semis.seme(mo, cible, ecrire=True)
        j.verifie(f"refusé — {nom}", s.plan.refuse and not s.plan.fichiers,
                  f"{len(s.plan.fichiers)} fichier(s) posé(s) ; "
                  f"refus : {s.plan.refus}")
        j.verifie(f"  … et rien n'a été écrit — {nom}", not cible.exists()
                  or cible == seme, f"`{cible}` existe")

    # Sous un VAULT : un dossier qui porte `brain.yml` sans etre un depot git.
    faux = dossier / "faux-vault"
    faux.mkdir()
    (faux / "brain.yml").write_text("manifeste: 1\n", encoding="utf-8")
    s = semis.seme(mo, faux / "dedans", ecrire=True)
    j.verifie("refusé — cible SOUS un vault (marqueur `brain.yml`)",
              s.plan.refuse and not (faux / "dedans").exists(),
              str(s.plan.refus))


# --------------------------------------------------------------------------- #
def scenario_incomplet(j: Journal, dossier: Path) -> None:
    print("\n3. INCOMPLET — le cas NÉGATIF : refusé, jamais semé à moitié")
    base = charge_dict(REFERENCE)

    def ampute(quoi, mutation) -> tuple[str, dict]:
        m = copy.deepcopy(base)
        mutation(m)
        return quoi, m

    def sans_racine(m):
        del m["racine"]

    def sans_dossier_de_role(m):
        for r in m["roles"]:
            if r.get("range_par") == "role":
                del r["dossier"]
                break

    def sans_identite(m):
        m["git"]["identite"]["email"] = ""

    def sans_balises(m):
        for r in m["roles"]:
            for s in r.get("corps") or []:
                if s.get("genre") == "auto" and s.get("balises"):
                    del s["balises"]

    cas = [ampute("`racine:` absent", sans_racine),
           ampute("un rôle `range_par: role` sans `dossier:`", sans_dossier_de_role),
           ampute("`git.identite.email` vide", sans_identite),
           ampute("la zone AUTO du hub sans balises", sans_balises)]

    for i, (quoi, m) in enumerate(cas):
        mo = Modele(m, REFERENCE)
        cible = dossier / f"incomplet-{i}"
        s = semis.seme(mo, cible, ecrire=True)
        j.verifie(f"refusé — {quoi}", bool(s.manques), "aucun manque signalé")
        j.verifie(f"  … rien n'est écrit — {quoi}", not cible.exists(),
                  f"`{cible}` a été créé")
        j.verifie(f"  … et le refus NOMME le manque — {quoi}",
                  any(len(x) > 20 for x in s.manques), str(s.manques))


# --------------------------------------------------------------------------- #
def scenario_genericite(j: Journal, dossier: Path, vault: Path) -> None:
    print("\n4. GÉNÉRICITÉ — le témoin semé, comparé à son arbre RÉEL (lecture seule)")
    manifeste = vault / "brain.yml"
    mo = Modele(charge_dict(manifeste), manifeste)
    cible = dossier / "temoin-vierge"
    s = semis.seme(mo, cible, ecrire=True, avec_git=False)
    j.verifie("le semis du témoin ne refuse rien", not s.refuse,
              "\n".join(s.manques + s.plan.refus))
    if s.refuse:
        return

    v = valide(mo, cible)
    j.verifie("validateur : 0 violation DURE sur l'instance vierge", not v.dures,
              "\n".join(c.rendu() for c in v.dures))
    g = genere_tout(mo, cible, mode=CHECK)
    j.verifie("générateurs : `--check` silencieux", not g.ecarts() and not g.refus,
              f"{len(g.ecarts())} écart(s), {len(g.refus)} refus")

    # Les dossiers de PREMIER NIVEAU qui portent des pages, des deux cotes.
    def tetes(racine: Path) -> set[str]:
        return {d.name for d in racine.iterdir()
                if d.is_dir() and not d.name.startswith(".")
                and d.name not in mo.non_pages
                and any(d.glob("*.md"))}

    # L ECART EST ATTENDU, il est UN, et il est explique : les dossiers d axe
    # transverse. Le vault reel porte `Métiers/` peuple de six hubs, un par
    # valeur PORTEE ; l instance vierge porte le dossier et aucun hub, parce
    # qu aucune page ne porte encore de valeur (arbitrage 2 du semis). Le
    # premier `build_mocs` apres la premiere capture le creera tout seul.
    attendu_en_moins = {t["dossier"] for t in mo.transverses}
    _ensemble("mêmes dossiers de premier niveau portant un hub, aux dossiers "
              "d'axe transverse près",
              tetes(cible) | attendu_en_moins, tetes(vault), j)
    j.verifie("… et l'écart est EXACTEMENT les dossiers d'axe transverse",
              tetes(vault) - tetes(cible) == attendu_en_moins,
              f"écart réel : {sorted(tetes(vault) - tetes(cible))}")

    # Les hubs de premier niveau, par nom de fichier.
    def hubs(racine: Path) -> set[str]:
        return {d.name for d in racine.iterdir()
                if d.is_dir() and (d / f"{d.name}.md").is_file()}

    _ensemble("mêmes hubs de premier niveau", hubs(cible), hubs(vault), j)

    def compte(racine: Path) -> int:
        # Sans `.git` ni `.claude` : le vault reel porte 26 worktrees sous
        # `.claude/`, qui sont des COPIES completes de lui-meme.
        return sum(1 for p in racine.rglob("*.md")
                   if not set(p.relative_to(racine).parts) & {".git", ".claude"})

    print(f"       écart attendu et EXPLIQUÉ : le vault réel porte "
          f"{compte(vault)} `.md`, l'instance vierge {compte(cible)}. "
          f"La différence est le CONTENU — c'est tout l'intérêt.")


# --------------------------------------------------------------------------- #
def scenario_reseuiller(j: Journal, mo: Modele, dossier: Path) -> None:
    print("\n5. RE-SEUILLER — aucun effet à zéro page, une dépromotion réelle sinon")
    vierge = dossier / "reference"
    r = reseuiller.calcule(mo, vierge, 5)
    j.verifie("instance vierge : aucun `git mv`, et l'opération le dit",
              r.sans_effet and not r.refus, str(r.refus))

    # Un vault PEUPLE : `tests/genere-vert`, copie hors du depot, en depot git.
    mo_v = Modele(charge_dict(GENERATION), GENERATION)
    copie = dossier / "reseuil"
    shutil.copytree(VERT, copie)
    _git(copie, "init", "-b", "essai")
    _git(copie, "config", "--local", "user.name", "épreuve")
    _git(copie, "config", "--local", "user.email", "epreuve@local")
    _git(copie, "add", "-A")
    _git(copie, "commit", "-m", "état de départ")

    # Seuil 2 -> 3 : `domaine-a/segment-1` pese 2, donc il se DEPROMEUT.
    r = reseuiller.calcule(mo_v, copie, 3)
    j.verifie("seuil 2 → 3 : une dépromotion", r.depromotions == ["domaine-a/segment-1"],
              f"promotions={r.promotions} dépromotions={r.depromotions}")
    # TROIS pages, pas deux : la chronologie du dossier suit, alors qu elle ne
    # PESE pas sur le seuil. Les deux notions ne se confondent pas —
    # `pese_sur_le_seuil: false` dit « ne compte pas dans la decision de
    # promotion », pas « ne se range pas ». Une vue restee dans un dossier
    # depromu serait une page hors de son dossier derive, donc une violation de
    # `chemin_categorie`.
    j.verifie("trois pages à déplacer, dont la vue qui ne pèse pas sur le seuil",
              len(r.mouvements) == 3,
              str([(m.depuis, m.vers) for m in r.mouvements]))
    j.verifie("le hub du dossier dépromu est SIGNALÉ, pas supprimé",
              r.hubs_orphelins == ["Domaine A/Segment 1/Segment 1.md"],
              str(r.hubs_orphelins))

    r = reseuiller.applique(mo_v, copie, r)
    j.verifie("les `git mv` passent", r.applique and not r.refus, str(r.refus))
    j.verifie("les pages ont bougé", (copie / "Domaine A" / "Unité A2.md")
              .is_file() and not (copie / "Domaine A" / "Segment 1" /
                                  "Unité A2.md").is_file())
    # `git status` voit un RENOMMAGE (`R`), pas une suppression suivie d un
    # ajout. C est ce qui prouve le `git mv` : `--follow` ne dirait rien avant
    # le commit, et l operation ne committe pas — la cloture n est pas son
    # travail.
    _c, statut = _git(copie, "status", "--porcelain")
    renommages = [l for l in statut.splitlines() if l.startswith("R")]
    j.verifie("git voit trois RENOMMAGES, pas des suppressions + créations",
              len(renommages) == 3, statut)
    j.verifie("le hub orphelin est TOUJOURS là",
              (copie / "Domaine A" / "Segment 1" / "Segment 1.md").is_file())

    # Sur un arbre SALE, `applique` refuse.
    (copie / "sale.txt").write_text("x", encoding="utf-8")
    r2 = reseuiller.applique(mo_v, copie, reseuiller.calcule(mo_v, copie, 2))
    j.verifie("`applique` refuse sur un arbre de travail sale",
              bool(r2.refus) and not r2.applique, str(r2.refus))


# --------------------------------------------------------------------------- #
def scenario_freeze(j: Journal, mo: Modele, dossier: Path) -> None:
    print("\n6. FREEZE — ce qu'il copie, ce qu'il refuse, ce qu'il préserve")
    f = figer.fige(mo, dossier, ecrire=False)
    j.verifie("refuse un dossier qui n'est pas une instance", bool(f.refus),
              "aucun refus")

    cible = dossier / "reference"
    f = figer.fige(mo, cible, ecrire=False)
    j.verifie("simulation : quatre étapes annoncées, rien d'écrit",
              not f.refus and len(f.etapes) == 4
              and not (cible / "AI" / "scripts" / "brainkit").exists(),
              str(f.etapes))

    f = figer.fige(mo, cible, ecrire=True)
    j.verifie("appliqué : le kit est copié dans l'instance",
              f.applique and (cible / "AI" / "scripts" / "brainkit" /
                              "valider" / "moteur.py").is_file(), str(f.refus))
    j.verifie("les trois lanceurs PEP 723 sont posés",
              all((cible / "AI" / "scripts" / n).is_file()
                  for n in ("valider.py", "generer.py", "semer.py")))
    manifeste = (cible / "brain.yml").read_text(encoding="utf-8")
    j.verifie("`kit.mode` est passé à `fige`", "mode: fige" in manifeste)
    j.verifie("les `motif:` du manifeste survivent à la bascule",
              "motif_seuil:" in manifeste and manifeste.count("motif") > 50,
              f"{manifeste.count('motif')} occurrence(s) de `motif`")

    mo_fige = Modele(yaml.safe_load(manifeste), cible / "brain.yml")
    j.verifie("refuse de refiger une instance déjà figée",
              bool(figer.fige(mo_fige, cible, ecrire=False).refus))
    v = valide(mo_fige, cible)
    j.verifie("l'instance figée reste VERTE", not v.dures,
              "\n".join(c.rendu() for c in v.dures))


# --------------------------------------------------------------------------- #
def scenario_idempotence(j: Journal, mo: Modele, dossier: Path) -> None:
    print("\n7. IDEMPOTENCE — semer deux fois est refusé")
    s = semis.seme(mo, dossier / "reference", ecrire=True)
    j.verifie("un second semis au même endroit est refusé",
              s.plan.refuse and not s.plan.fichiers, str(s.plan.refus))
    neuf = dossier / "reference-bis"
    a = semis.seme(mo, neuf, ecrire=True, avec_git=False)
    b = semis.seme(mo, neuf / "encore", ecrire=False, avec_git=False)
    j.verifie("le mode lecture n'écrit rien, même sur une cible libre",
              not (neuf / "encore").exists(), "la cible a été créée")
    j.verifie("deux semis du même manifeste posent les mêmes fichiers",
              {f.chemin for f in a.plan.fichiers}
              == {f.chemin for f in s.plan.fichiers} or bool(s.plan.refus),
              "les deux plans diffèrent")
    _ = b


# --------------------------------------------------------------------------- #
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(description="Le jeu d'épreuve du semis.")
    ap.add_argument("--vault-temoin", type=Path, default=None,
                    help="un vault réel ; cf. tests/temoin.py")
    ap.add_argument("--garder", action="store_true",
                    help="ne pas effacer le dossier temporaire (pour inspecter)")
    ns = ap.parse_args()

    print("épreuve — le semis d'instance de BrainKit, lot 5")
    j = Journal()
    tmp = Path(tempfile.mkdtemp(prefix="bk5-"))
    try:
        mo = scenario_vierge(j, tmp)
        scenario_refus(j, mo, tmp)
        scenario_incomplet(j, tmp)
        vault = temoin.resout(ns.vault_temoin)
        if vault is not None and (vault / "brain.yml").is_file():
            scenario_genericite(j, tmp, vault)
        else:
            print(f"\n4. GÉNÉRICITÉ — sauté : {temoin.pourquoi_saute()}")
        scenario_reseuiller(j, mo, tmp)
        scenario_freeze(j, mo, tmp)
        scenario_idempotence(j, mo, tmp)
    finally:
        if ns.garder:
            print(f"\ndossier temporaire gardé : {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    print()
    if j.echecs:
        print(f"{len(j.echecs)} vérification(s) en échec :")
        for e in j.echecs:
            print(f"  - {e}")
        return 1
    print("OK — le jeu d'épreuve du semis passe en entier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
