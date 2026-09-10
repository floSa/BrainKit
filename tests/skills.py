# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""skills.py — le jeu d epreuve des TROIS SKILLS (lot 7).

    uv run tests/skills.py
    uv run tests/skills.py --garder

Sept scenarios. Aucun n ecrit hors d un dossier temporaire, et aucun ne touche
une instance d essai.

  1. DERIVATION   — la table de propagation d BrainRef, ligne par ligne. Ce
                    n est pas un compte : c est la composition qui est le
                    livrable, et chaque ligne est verifiee sur son GENRE, son
                    role vise et sa condition de « sans objet ».
  2. GENERICITE   — la table de BrainDeux confrontee a celle du manifeste de reference. Deux
                    manifestes sans un mot commun doivent donner deux tables
                    dont AUCUNE cellule ne coincide. Une table identique serait
                    la preuve qu elle est recopiee. Plus le controle des mots :
                    aucun mot de sujet de l un n apparait dans les skills de
                    l autre.
  3. EFFETS       — la table des effets de bord : un champ = une ligne, et le
                    branchement de chaque famille de consommateur est verifie
                    sur le champ qui la declare, jamais sur son nom.
  4. RAYON TENU   — le cas POSITIF du controle : une capture complete, chaque
                    ligne honoree ou sans objet, code 0.
  5. RAYON TU     — le cas NEGATIF, celui qui donne sa valeur au lot : une
                    capture qui laisse une ligne du rayon TUE est REFUSEE, la
                    ligne est nommee, et le code de retour est 1.
  6. EXPLOITATION — un manifeste SANS `skills.exploitation` ne produit PAS de
                    troisieme skill, et le README des skills dit pourquoi.
                    L absence declaree vaut mieux qu une presence creuse.
  7. SEMIS        — une instance semee porte les trois `SKILL.md`, reste verte
                    aux deux controles, et son `CLAUDE.md` porte la MEME table
                    que le skill de capture : une seule source, pas deux.
"""

from __future__ import annotations

import argparse
import copy
import io
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit import skills                                        # noqa: E402
from brainkit.entretien import brouillon as _brouillon             # noqa: E402
from brainkit.entretien import composer                            # noqa: E402
from brainkit.generer import genere_tout                           # noqa: E402
from brainkit.generer.sortie import CHECK                          # noqa: E402
from brainkit.semer import semis                                   # noqa: E402
from brainkit.skills import controle as ctrl                       # noqa: E402
from brainkit.skills import propagation as P                       # noqa: E402
from brainkit.valider import valide                                # noqa: E402
from brainkit.valider.manifeste import Modele                      # noqa: E402

REFERENCE = RACINE_KIT / "gabarit" / "brain.yml"
# BrainDeux n est PAS copie ici : il se COMPOSE depuis les reponses d entretien
# que le lot 6 a enregistrees. Une copie serait une seconde source du meme
# manifeste, c est-a-dire le defaut que le manifeste existe pour supprimer.
REPONSES_DEUX = RACINE_KIT / "tests" / "deuxieme.reponses.yml"

# La table du manifeste de reference, attendue LIGNE PAR LIGNE : (genre, role visé, la ligne
# a-t-elle toujours un objet ?, demande-t-elle un travail humain ?).
TABLE_REFERENCE = [
    ("P1", P.G_HUB,         "hub",         True,  False),
    ("P2", P.G_PARENTS,     "hub",         False, False),
    ("P3", P.G_VOISIN,      "sequence",    False, True),
    ("P4", P.G_VOISIN,      "notion",      False, True),
    ("P5", P.G_PAIRS,       "unite",       False, True),
    ("P6", P.G_RESUMES,     None,          False, True),
    ("P7", P.G_RALLIEMENT,  "sequence",    False, True),
    ("P8", P.G_TRANSVERSE,  None,          False, False),
    ("P9", P.G_TRANSVERSE,  None,          False, False),
]

# Les mots de SUJET de chaque brain. Aucun ne doit apparaitre dans les skills de
# l autre : c est le controle qui distingue une derivation d une recopie.
#
# Les jetons portent leur PONCTUATION — `contredit:` et non « contredit ». Le
# premier jeu d essai n en portait pas, et il a signale deux faux positifs :
# « une cellule sans source » et « elle contredit une information que le
# harnais repete » sont du francais ordinaire, pas une fuite de vocabulaire.
# Un controle de genericite qui teste des mots courants mesure la langue, pas
# la derivation.
MOTS_REFERENCE = ["role: unite", "role: sequence", "Marqueur 1", "Secteur 1",
                  "Segment B1", "prolonge_par", "contredit:", "fiabilite",
                  "BrainRef"]
MOTS_DEUX = ["role: element", "role: selection", "Croisements", "matiere",
             "Phase 1", "enchaine_avec", "variante_de", "BrainDeux"]


class Journal:
    def __init__(self) -> None:
        self.echecs: list[str] = []

    def verifie(self, nom: str, ok: bool, detail: str = "") -> None:
        print(f"  {'OK    ' if ok else 'ÉCHEC '} {nom}")
        if not ok:
            self.echecs.append(nom)
            for ligne in str(detail).splitlines():
                print(f"         {ligne}")


def charge(chemin: Path) -> Modele:
    with chemin.open(encoding="utf-8") as f:
        return Modele(yaml.safe_load(f), chemin)


def compose_deuxieme(dossier: Path) -> Modele:
    """BrainDeux, recompose depuis ses reponses d entretien. Jamais copie."""
    with REPONSES_DEUX.open(encoding="utf-8") as f:
        reponses = (yaml.safe_load(f) or {}).get("reponses") or {}
    b = _brouillon.charge(dossier / "entretien.yml")
    for qid, val in reponses.items():
        b.repond(str(qid), val)
    m, griefs = composer.compose(b)
    if m is None:
        raise SystemExit("BrainDeux ne se compose pas : " + " · ".join(griefs))
    return Modele(m, dossier / "brain.yml")


# --------------------------------------------------------------------------- #
def scenario_derivation(j: Journal, mo: Modele) -> list[P.Ligne]:
    print("\n1. DÉRIVATION — la table de référence, ligne par ligne")
    lignes = P.derive(mo)
    j.verifie(f"{len(TABLE_REFERENCE)} lignes dérivées",
              len(lignes) == len(TABLE_REFERENCE),
              f"{len(lignes)} obtenues : "
              + " · ".join(f"{li.n} {li.genre}" for li in lignes))
    if len(lignes) != len(TABLE_REFERENCE):
        return lignes
    for li, (n, genre, role, toujours, ecrire) in zip(lignes, TABLE_REFERENCE):
        j.verifie(f"{n} — genre `{genre}`, rôle `{role}`",
                  li.n == n and li.genre == genre and li.role == role,
                  f"obtenu : {li.n} genre `{li.genre}` rôle `{li.role}`")
        j.verifie(f"{n} — {'toujours un objet' if toujours else 'sans objet DÉCLARÉ'}",
                  li.toujours_un_objet == toujours,
                  f"`sans_objet_si` = {li.sans_objet_si!r}")
        j.verifie(f"{n} — {'à écrire' if ecrire else 'délégué au générateur'}",
                  li.a_ecrire == ecrire, f"`par` = {li.par!r}")

    # Chaque ligne dit CE QUI la produit. Une origine vide serait une ligne
    # qu on ne pourrait ni contester ni retirer en changeant le manifeste.
    j.verifie("chaque ligne porte son `origine` dans le manifeste",
              all(li.origine and "`" in li.origine for li in lignes),
              " · ".join(f"{li.n}={li.origine!r}" for li in lignes
                         if not li.origine))
    # La paire ORIENTEE, le mecanisme que le DevBrain n a jamais eu.
    paires = P.paires_inverses(mo)
    j.verifie("la paire inverse `prolonge` / `prolonge_par` est vue UNE fois",
              paires == [("prolonge", "prolonge_par")], str(paires))
    ligne_pairs = next(li for li in lignes if li.genre == P.G_PAIRS)
    j.verifie("la ligne des pairs nomme les DEUX modes de réciprocité",
              "symétrique" in ligne_pairs.par and "inverse" in ligne_pairs.par,
              ligne_pairs.par)
    return lignes


def scenario_genericite(j: Journal, mo_h: Modele, mo_c: Modele,
                        lignes_h: list[P.Ligne]) -> None:
    print("\n2. GÉNÉRICITÉ — deux manifestes, deux tables, aucune cellule commune")
    lignes_c = P.derive(mo_c)
    j.verifie("BrainDeux obtient 8 lignes, BrainRef 9 — un axe transverse "
              "de moins",
              len(lignes_c) == 8 and len(lignes_h) == 9,
              f"BrainDeux {len(lignes_c)}, BrainRef {len(lignes_h)}")

    # Le controle central : deux tables differentes sur deux brains differents.
    cellules_h = {(li.cible, li.trouve_par, li.par) for li in lignes_h}
    cellules_c = {(li.cible, li.trouve_par, li.par) for li in lignes_c}
    communes = cellules_h & cellules_c
    # DEUX lignes sont legitimement identiques, et ce sont exactement celles qui
    # ne citent AUCUNE valeur d instance : le hub du dossier et les hubs
    # parents. Elles ne parlent que de la structure de l arbre, qui est la meme
    # partout — c est le fait dont toute la regle de propagation depend. Toutes
    # les autres doivent differer, mot pour mot.
    attendu = {(li.cible, li.trouve_par, li.par) for li in lignes_h
               if li.genre in (P.G_HUB, P.G_PARENTS)}
    j.verifie("seules les deux lignes de hub sont communes — elles ne citent "
              "aucune valeur d'instance",
              communes == attendu,
              "communes en trop : "
              + " · ".join(str(c) for c in sorted(communes - attendu))
              + " · manquantes : "
              + " · ".join(str(c) for c in sorted(attendu - communes)))

    # Le controle des MOTS : la preuve qu aucun vocabulaire ne fuit.
    rendus_h = "\n".join(skills.rendus(mo_h).values())
    rendus_c = "\n".join(skills.rendus(mo_c).values())
    for mot in MOTS_DEUX:
        j.verifie(f"« {mot} » (BrainDeux) absent des skills de BrainRef",
                  mot.lower() not in rendus_h.lower())
    for mot in MOTS_REFERENCE:
        j.verifie(f"« {mot} » (BrainRef) absent des skills de BrainDeux",
                  mot.lower() not in rendus_c.lower())

    # Le NOM des skills vient du manifeste, jamais du kit.
    chemins_h, chemins_c = set(skills.rendus(mo_h)), set(skills.rendus(mo_c))
    j.verifie("les six skills portent six noms distincts, tous du manifeste",
              len(chemins_h | chemins_c) == 6 and not (chemins_h & chemins_c),
              str(sorted(chemins_h | chemins_c)))


def scenario_effets(j: Journal, mo: Modele) -> None:
    print("\n3. EFFETS DE BORD — un champ, une ligne, un branchement déclaré")
    effets = {e.champ: e for e in P.effets_de_bord(mo)}
    j.verifie("un effet par champ déclaré, sans exception",
              set(effets) == set(mo.champs),
              f"manquants : {sorted(set(mo.champs) - set(effets))} · "
              f"en trop : {sorted(set(effets) - set(mo.champs))}")

    # Chaque famille de consommateur est branchee sur ce qui la DECLARE, jamais
    # sur le nom du champ : c est la discipline de resolution du moteur.
    attendus = [
        ("nom", "unicite_du_nom_de_fichier", "`fonction: identite`"),
        ("apport", "reinjection_du_resume", "`fonction: resume_court`"),
        ("domaine", "chemin_categorie", "`source: axes.rangement`"),
        ("nature", "gabarit_par_role", "les conditionnels qu'il commande"),
        ("marqueurs", "generer --check", "un axe transverse"),
        ("tags", "vocabulaire_ferme", "un vocabulaire en fichier"),
        ("prolonge", "reciprocite", "`reciproque: inverse`"),
        ("contredit", "reciprocite", "`reciproque: symetrique`"),
    ]
    for champ, attendu, pourquoi in attendus:
        e = effets.get(champ)
        texte = (e.verification + " " + " ".join(e.consommateurs)) if e else ""
        j.verifie(f"`{champ}:` → {attendu} ({pourquoi})",
                  attendu in texte, texte[:200])

    j.verifie("`domaine:` est le SEUL champ qui change de rayon",
              [c for c, e in effets.items() if "CHANGE de rayon" in e.rayon]
              == ["domaine"],
              str([c for c, e in effets.items() if "CHANGE" in e.rayon]))
    j.verifie("`variante:` n'a aucun consommateur, et le DIT",
              "aucun consommateur déclaré" in
              " ".join(effets["variante"].consommateurs))
    hors = {e.champ for e in P.effets_hors_champ(mo)}
    j.verifie("le renommage et la suppression ont leur ligne, hors des champs",
              len(hors) == 2 and all("**" in h for h in hors), str(hors))


# --------------------------------------------------------------------------- #
def _vault_d_essai(racine: Path, mo: Modele, avec_liens: bool) -> str:
    """Un dossier, un hub, une notion, un pair, et la page qu on capture.

    `avec_liens=False` produit exactement le defaut que le lot controle : la
    page est ecrite, ses voisins ne sont pas touches, et RIEN dans le vault ne
    le dit. C est le cas negatif.
    """
    dossier = racine / "Domaine B"
    dossier.mkdir(parents=True, exist_ok=True)
    ecrit = []

    def pose(nom: str, texte: str) -> str:
        (dossier / f"{nom}.md").write_text(texte, encoding="utf-8", newline="\n")
        ecrit.append(f"Domaine B/{nom}.md")
        return f"Domaine B/{nom}.md"

    pose("Domaine B", "---\nrole: hub\nnom: Domaine B\napport: \"x\"\n---\n\n"
                      "# Domaine B\n")
    pose("Notion d'essai", "---\nrole: notion\nnom: Notion d'essai\n"
                           "domaine: domaine-b/b1\nmarqueurs: [m1]\n---\n\n"
                           "# Notion d'essai\n")
    pose("Pair d'essai", "---\nrole: unite\nnom: Pair d'essai\n"
                         "apport: \"Le pair déjà en place.\"\n"
                         "domaine: domaine-b/b1\n---\n\n# Pair d'essai\n")
    liens = ("contredit: [Pair d'essai]\n" if avec_liens else "")
    page = pose("Page capturée",
                "---\nrole: unite\nnom: Page capturée\n"
                "apport: \"La page qu'on vient d'écrire.\"\n"
                f"domaine: domaine-b/b1\n{liens}---\n\n# Page capturée\n")
    return page


def scenario_rayon_tenu(j: Journal, mo: Modele, tmp: Path) -> None:
    print("\n4. RAYON TENU — le cas positif : tout est touché, code 0")
    racine = tmp / "tenu"
    page = _vault_d_essai(racine, mo, avec_liens=True)
    touches = {f"Domaine B/{p.name}" for p in (racine / "Domaine B").iterdir()}
    r = ctrl.controle(mo, racine, page, touches)
    j.verifie("aucune ligne tue", not r.tues,
              " · ".join(c.ligne.n for c in r.tues))
    j.verifie("code de retour 0", r.code == 0)
    etats = {c.ligne.n: c.etat for c in r.constats}
    j.verifie("la notion et le pair sont HONORÉS",
              etats.get("P4") == ctrl.HONOREE and etats.get("P5") == ctrl.HONOREE,
              str(etats))
    j.verifie("la séquence absente est SANS OBJET, pas tue",
              etats.get("P3") == ctrl.SANS_OBJET, str(etats))
    j.verifie("les hubs sont DÉLÉGUÉS aux générateurs, pas exigés ici",
              etats.get("P1") == ctrl.DELEGUEE and etats.get("P2") == ctrl.DELEGUEE,
              str(etats))
    # La condition de « sans objet » est ECRITE, pas sous-entendue.
    sans = next(c for c in r.constats if c.ligne.n == "P3")
    j.verifie("une ligne sans objet porte la RAISON, en clair",
              bool(sans.detail) and "aucune page" in sans.detail, sans.detail)


def scenario_rayon_tu(j: Journal, mo: Modele, tmp: Path) -> None:
    print("\n5. RAYON TU — le cas NÉGATIF : une ligne tue est REFUSÉE")
    racine = tmp / "tu"
    page = _vault_d_essai(racine, mo, avec_liens=False)
    # On ne touche QUE la page capturée : le pair et la notion restent en place,
    # intacts. C est exactement « écrire la page et s'arrêter là ».
    r = ctrl.controle(mo, racine, page, {page})
    j.verifie("le contrôle REFUSE — code de retour 1", r.code == 1)
    tues = {c.ligne.n for c in r.tues}
    j.verifie("la notion du dossier (P4) est déclarée TUE", "P4" in tues, str(tues))
    j.verifie("le pair du dossier (P5) est déclaré TUE", "P5" in tues, str(tues))
    j.verifie("les lignes tues NOMMENT leurs objets",
              all(c.objets for c in r.tues),
              str([(c.ligne.n, c.objets) for c in r.tues]))

    sortie = io.StringIO()
    with redirect_stdout(sortie):
        code = ctrl.imprime(r)
    texte = sortie.getvalue()
    j.verifie("l'impression sort en 1 et nomme les lignes tues",
              code == 1 and "TUE" in texte and "Notion d'essai" in texte,
              texte)
    j.verifie("le message rappelle la clause : une ligne sans objet se DÉCLARE",
              "sans objet se DÉCLARE" in texte, texte[-300:])

    # Et le contre-controle : le validateur, lui, ne voit RIEN. C est la raison
    # d etre de ce controle-la, et il faut que le jeu d epreuve le prouve.
    v = valide(mo, racine)
    j.verifie("le validateur, lui, ne signale AUCUNE violation dure — c'est "
              "pourquoi ce contrôle existe",
              not v.dures, " · ".join(str(d) for d in v.dures[:3]))


def scenario_exploitation(j: Journal, mo: Modele) -> None:
    print("\n6. EXPLOITATION — non déclarée = pas écrite, et on le DIT")
    muet = Modele(copy.deepcopy(mo.m), mo.chemin)
    muet.m["skills"].pop("exploitation")
    j.verifie("`skills.exploitation` absent → deux skills, pas trois",
              len(skills.rendus(muet)) == 2, str(sorted(skills.rendus(muet))))
    from brainkit.skills import exploitation as expl
    j.verifie("l'absence est déclarée, avec la question qui la répare",
              "10.1" in expl.absence(muet)
              and "fiction" in expl.absence(muet), expl.absence(muet))
    j.verifie("les deux skills restants ne citent plus le troisième",
              "preparer-un-livrable" not in "\n".join(skills.rendus(muet).values()))
    j.verifie("déclaré, il est écrit", len(skills.rendus(mo)) == 3,
              str(sorted(skills.rendus(mo))))
    # Le filtre eliminatoire : VIDE par defaut, et le skill l ecrit en clair.
    j.verifie("aucun champ éliminatoire dans BrainRef, et le skill le DIT",
              not expl.eliminatoires(mo)
              and "Rien ne disqualifie" in skills.rendus(mo)[
                  ".claude/skills/preparer-un-livrable/SKILL.md"])


def scenario_semis(j: Journal, mo: Modele, tmp: Path) -> None:
    print("\n7. SEMIS — les trois skills posés, et UNE seule table")
    racine = tmp / "semis"
    s = semis.seme(mo, racine, ecrire=True, avec_git=False)
    j.verifie("le semis n'est pas refusé", not s.refuse, " · ".join(s.plan.refus))
    poses = {f.chemin for f in s.plan.fichiers}
    for nom in ("enrichir-brainref", "cloturer-brainref",
                "preparer-un-livrable"):
        j.verifie(f"`.claude/skills/{nom}/SKILL.md` posé",
                  f".claude/skills/{nom}/SKILL.md" in poses)
    j.verifie("aucun `.gitkeep` ne subsiste dans un dossier de skill écrit",
              not [c for c in poses
                   if c.startswith(".claude/skills/") and c.endswith(".gitkeep")],
              str([c for c in poses if c.endswith(".gitkeep")]))

    dures, souples, ecarts = semis.verifie(mo, racine)
    j.verifie("l'instance semée reste verte", dures == 0, f"{dures} dure(s)")
    j.verifie("`generer --check` reste silencieux", ecarts == 0,
              f"{ecarts} écart(s)")
    _ = souples

    # UNE table, pas deux : le routeur et le skill de capture disent la meme
    # chose parce qu ils la derivent du meme endroit. C est le constat E4,
    # applique aux deux fichiers les plus lus du vault.
    routeur = (racine / "CLAUDE.md").read_text(encoding="utf-8")
    capture = (racine / ".claude/skills/enrichir-brainref/SKILL.md").read_text(
        encoding="utf-8")
    for li in P.derive(mo):
        j.verifie(f"{li.n} — même cible dans `CLAUDE.md` et dans la capture",
                  li.cible in routeur and li.cible in capture,
                  f"routeur={li.cible in routeur} capture={li.cible in capture}")
    j.verifie("le README des skills montre l'origine de chaque ligne",
              all(li.origine in (racine / ".claude/skills/README.md").read_text(
                  encoding="utf-8") for li in P.derive(mo)))

    g = genere_tout(mo, racine, mode=CHECK)
    j.verifie("les artefacts dérivés concordent après le semis",
              not g.ecarts(), str(g.ecarts()[:3]))


# --------------------------------------------------------------------------- #
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(description="Le jeu d'épreuve des trois skills.")
    ap.add_argument("--garder", action="store_true")
    ns = ap.parse_args()

    print("épreuve — les trois skills de BrainKit, lot 7")
    j = Journal()
    tmp = Path(tempfile.mkdtemp(prefix="bk7-"))
    mo_h = charge(REFERENCE)
    mo_c = compose_deuxieme(tmp / "deux")
    try:
        lignes = scenario_derivation(j, mo_h)
        scenario_genericite(j, mo_h, mo_c, lignes)
        scenario_effets(j, mo_h)
        scenario_rayon_tenu(j, mo_h, tmp)
        scenario_rayon_tu(j, mo_h, tmp)
        scenario_exploitation(j, mo_h)
        scenario_semis(j, mo_h, tmp)
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
    print("OK — le jeu d'épreuve des skills passe en entier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
