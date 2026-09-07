# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""entretien.py — le jeu d epreuve de L ENTRETIEN (lot 6).

    uv run tests/entretien.py

Sept scenarios. Aucun n ecrit hors d un dossier temporaire, et deux d entre eux
ont pour but de RATER : un entretien qui ne saurait pas s arreter serait plus
dangereux qu un entretien absent.

  1. LES QUESTIONS — onze passes, la liste est fermee, l ordre est stable, les
                     treize refus sont tous portes, et chaque question hors
                     cadrage porte son motif ECRIT.
  2. IDENTITE      — le CONTROLE NEGATIF du lot, en quatre cas : sans reponse
                     l entretien s arrete et ne seme rien ; une reponse marquee
                     `harnais` est refusee a l enregistrement ; une adresse
                     portant le domaine que 0.5 vient d interdire est refusee ;
                     une adresse egale a une valeur de l ENVIRONNEMENT est
                     refusee. Et la verification qui compte : le dossier cible
                     n existe pas.
  3. INDUCTION     — ce que l entretien fait quand les reponses ne suffisent
                     pas : moins de dix titres, un titre range nulle part, un
                     titre dans deux paquets, un arbre sans rangs, un arbre qui
                     n atteint pas un paquet.
  4. REPRISE       — un entretien s arrete et repart : rien ne se redemande,
                     les questions conditionnelles se sautent toutes seules, et
                     `--oublier` est le seul moyen de rouvrir.
  5. BOUT EN BOUT  — CimeBrain, un TROISIEME sujet. Reponses -> manifeste ->
                     schema -> semis -> deux validateurs verts sur ZERO page
                     d unite, et les vingt titres dans `Inbox.md` sans qu une
                     page ait ete ecrite.
  6. LES INVARIANTS— aucune severite deduite, aucune liste remplie d avance,
                     aucun vocabulaire herite, aucun mot d un autre brain.
  7. DEFAUT DE MANIFESTE — la remontee 3 du lot 5, corrigee : le defaut est le
                     manifeste DU VAULT, et une incoherence se dit en toutes
                     lettres.
"""

from __future__ import annotations

import copy
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit import defauts                                       # noqa: E402
from brainkit.entretien import (brouillon as _brouillon,           # noqa: E402
                                composer, induction, passes, refus)
from brainkit.entretien import rendu as _rendu                     # noqa: E402
from brainkit.generer import genere_tout                           # noqa: E402
from brainkit.generer.sortie import CHECK                          # noqa: E402
from brainkit.semer import semis                                   # noqa: E402
from brainkit.valider import valide                                # noqa: E402
from brainkit.valider.manifeste import Modele                      # noqa: E402

REPONSES = RACINE_KIT / "tests" / "cimebrain.reponses.yml"
HUBS_ATTENDUS = {"Mont-Blanc", "Écrins", "Vanoise", "Vercors", "Pyrénées",
                 "Queyras-Ubaye", "Traversées", "Règles", "Sélections"}


class Journal:
    def __init__(self) -> None:
        self.echecs: list[str] = []

    def verifie(self, nom: str, ok: bool, detail: str = "") -> None:
        print(f"  {'OK    ' if ok else 'ÉCHEC '} {nom}")
        if not ok:
            self.echecs.append(nom)
            for ligne in str(detail).splitlines():
                print(f"         {ligne}")


def _charge_les_reponses() -> dict:
    with REPONSES.open(encoding="utf-8") as f:
        return (yaml.safe_load(f) or {}).get("reponses") or {}


def _brouillon_neuf(dossier: Path, reponses: dict) -> _brouillon.Brouillon:
    b = _brouillon.charge(dossier / "entretien.yml")
    for qid, val in reponses.items():
        b.repond(str(qid), val)
    return b


def _git(racine: Path, *args: str) -> tuple[int, str]:
    p = subprocess.run(["git", "-C", str(racine), *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout + p.stderr).strip()


# --------------------------------------------------------------------------- #
def scenario_questions(j: Journal) -> None:
    print("\n1. LES QUESTIONS — la liste est fermée, et elle se compte")
    j.verifie("onze passes", len(passes.PASSES) == 11,
              f"{len(passes.PASSES)} passe(s)")
    j.verifie(f"{passes.total()} questions, et pas une de plus",
              passes.total() == sum(len(p.questions) for p in passes.PASSES))
    j.verifie("les identifiants sont uniques",
              len(passes.ORDRE) == len(set(passes.ORDRE)))
    j.verifie("l'ordre des identifiants suit l'ordre des passes",
              list(passes.ORDRE) == [q.id for p in passes.PASSES
                                     for q in p.questions])
    j.verifie("chaque question dit ce qu'elle produit",
              all(q.produit for q in passes.QUESTIONS.values()),
              ", ".join(q.id for q in passes.QUESTIONS.values() if not q.produit))

    # Une question hors cadrage SANS motif ecrit serait une question inventee.
    sans_motif = [q.id for q in passes.QUESTIONS.values()
                  if q.ajoutee is not None and q.id in passes.AJOUTEES
                  and not q.ajoutee.strip()]
    j.verifie(f"les {len(passes.AJOUTEES)} questions ajoutées au cadrage portent "
              f"leur motif", not sans_motif, str(sans_motif))

    # Les treize refus : chacun est porte par une question, ou declare comme
    # invariante. Un refus qu aucune question n honore serait un refus mort.
    orphelins = []
    for r in refus.LES_TREIZE:
        cites = {x.strip() for x in r.question.replace("/", " ").split()}
        if r.question.startswith("(aucune"):
            continue
        if not any(qid in passes.QUESTIONS for qid in cites):
            orphelins.append(r.n)
    j.verifie("les treize refus sont portés par une question, ou déclarés "
              "invariants", not orphelins, str(orphelins))
    j.verifie("une seule question BLOQUANTE, et c'est l'identité git",
              passes.BLOQUANTES == ("0.4",), str(passes.BLOQUANTES))


# --------------------------------------------------------------------------- #
def scenario_identite(j: Journal, dossier: Path) -> None:
    print("\n2. IDENTITÉ — le contrôle négatif : sans réponse, rien n'est semé")
    reponses = _charge_les_reponses()

    # --- cas a : 0.4 sans reponse ---------------------------------------- #
    amputees = {k: v for k, v in reponses.items() if k != "0.4"}
    b = _brouillon_neuf(dossier / "sans-identite", amputees)
    motif = refus.arret(b.reponses)
    j.verifie("sans réponse à 0.4, l'entretien ARRÊTE", motif is not None)
    j.verifie("… et le motif nomme le harnais",
              bool(motif) and "harnais" in motif, str(motif))
    m, griefs = composer.compose(b)
    j.verifie("… et rien ne se compose", m is None and len(griefs) == 1)

    cible = dossier / "jamais-seme"
    j.verifie("… et le dossier cible n'existe pas", not cible.exists(),
              "un semis a eu lieu alors que l'identité manquait")

    # --- cas b : l adresse du harnais, PROPOSEE ---------------------------- #
    b2 = _brouillon.charge(dossier / "harnais" / "entretien.yml")
    g = b2.repond("0.4", {"name": "floSa",
                          "email": "florian.horellou@aosis.net"},
                  provenance="harnais")
    j.verifie("une réponse de provenance `harnais` est REFUSÉE", bool(g),
              "elle a été acceptée")
    j.verifie("… et rien n'est enregistré", not b2.a_repondu("0.4"))

    # --- cas c : l adresse du harnais, presentee comme une reponse --------- #
    # Elle porte le domaine que la question 0.5 vient de nommer comme interdit.
    # C est le SECOND filet, et c est celui qui attrape l accident reel.
    triche = dict(reponses)
    triche["0.4"] = {"name": "floSa", "email": "florian.horellou@aosis.net"}
    b3 = _brouillon_neuf(dossier / "domaine-refuse", triche)
    motif = refus.arret(b3.reponses)
    j.verifie("une identité portant le domaine refusé par 0.5 est REFUSÉE",
              motif is not None and "aosis.net" in str(motif), str(motif))
    m, griefs = composer.compose(b3)
    j.verifie("… et le manifeste ne se compose pas", m is None)

    # --- cas d : l adresse trouvee dans l ENVIRONNEMENT -------------------- #
    ancien = os.environ.get("GIT_AUTHOR_EMAIL")
    os.environ["GIT_AUTHOR_EMAIL"] = "florian_horellou@laposte.net"
    try:
        b4 = _brouillon_neuf(dossier / "environnement", reponses)
        motif = refus.arret(b4.reponses)
        j.verifie("une identité égale à `GIT_AUTHOR_EMAIL` est REFUSÉE",
                  motif is not None and "GIT_AUTHOR_EMAIL" in str(motif),
                  str(motif))
    finally:
        if ancien is None:
            os.environ.pop("GIT_AUTHOR_EMAIL", None)
        else:
            os.environ["GIT_AUTHOR_EMAIL"] = ancien

    # --- et le cas POSITIF : un garde-fou qui refuse tout ne prouve rien --- #
    b5 = _brouillon_neuf(dossier / "identite-juste", reponses)
    j.verifie("une identité donnée par l'utilisateur PASSE",
              refus.arret(b5.reponses) is None, str(refus.arret(b5.reponses)))


# --------------------------------------------------------------------------- #
def scenario_induction(j: Journal) -> None:
    print("\n3. INDUCTION — ce qu'elle fait quand les réponses ne suffisent pas")
    reponses = _charge_les_reponses()
    titres = list(reponses["2.1"])
    paquets = {k: list(v) for k, v in reponses["2.2"].items()}

    p = induction.induis_les_paquets(titres, paquets)
    j.verifie("les sept paquets sont lus dans le geste, dans l'ordre nommé",
              [x["dossier"] for x in p.prefixes] == list(paquets))
    j.verifie("l'axe est vu NON exclusif — deux titres débordent",
              not p.exclusif and len(p.debordent) == 2,
              f"{len(p.debordent)} : {sorted(p.debordent)}")
    j.verifie("aucun titre n'est rangé nulle part", not p.orphelins,
              str(p.orphelins))

    # moins de dix titres : l induction ne tient pas, et elle le DIT.
    court = induction.induis_les_paquets(titres[:8], {"Un": titres[:8]})
    j.verifie("sous dix titres, un diagnostic BLOQUANT",
              any(d.question == "2.1" and d.bloquant for d in court.diagnostics))

    # un titre range nulle part : on le fait ranger, on ne le jette pas.
    manque = {k: [t for t in v if t != titres[0]] for k, v in paquets.items()}
    orphelin = induction.induis_les_paquets(titres, manque)
    j.verifie("un titre rangé nulle part est BLOQUANT, et il est nommé",
              any(d.question == "2.2" and d.bloquant for d in orphelin.diagnostics)
              and titres[0] in "\n".join(d.a_dire for d in orphelin.diagnostics))

    # le seuil se DERIVE, et il retombe sur les deux points de calibration.
    j.verifie("le seuil dérivé retrouve DevBrain (700 pages / 20 paquets -> 5)",
              induction.derive_le_seuil(700, 20)[0] == 5,
              str(induction.derive_le_seuil(700, 20)[0]))
    j.verifie("… et HistoBrain (3000 / 8 -> 12)",
              induction.derive_le_seuil(3000, 8)[0] == 12,
              str(induction.derive_le_seuil(3000, 8)[0]))
    seuil, motif = induction.derive_le_seuil(600, 7)
    j.verifie("… et le calcul est ÉCRIT dans le motif",
              "600" in motif and "/ 7" in motif and str(seuil) in motif, motif)

    # l ordre de l arbre reste a l utilisateur : sans rangs, c est BLOQUANT.
    sans_rangs = [{"n": None, "question": "…", "si_oui": [x["cle"]]}
                  for x in p.prefixes] + [{"n": None, "question": "Aucun",
                                           "si_oui": [], "arret": True}]
    d = induction.verifie_l_arbre(sans_rangs, p.prefixes)
    j.verifie("un arbre proposé SANS RANGS est bloquant (refus n° 5)",
              any(x.bloquant and "ORDRE" in x.a_dire for x in d))

    # un paquet qu aucune question n atteint : la page tomberait au hasard.
    troue = [{"n": "D1", "question": "…", "si_oui": [p.prefixes[0]["cle"]]},
             {"n": "D2", "question": "Aucun", "si_oui": [], "arret": True}]
    d = induction.verifie_l_arbre(troue, p.prefixes)
    j.verifie("un paquet qu'aucune question n'atteint est bloquant",
              any(x.bloquant and "mène" in x.a_dire for x in d))

    # un dossier d axe transverse qui redouble un dossier de l arbre.
    d = induction.verifie_les_transverses(
        [{"champ": "saisons", "dossier": p.prefixes[0]["dossier"]}], p.prefixes)
    j.verifie("un axe transverse qui redouble un dossier de l'arbre est refusé",
              any(x.bloquant for x in d))


# --------------------------------------------------------------------------- #
def scenario_reprise(j: Journal, dossier: Path) -> None:
    print("\n4. REPRISE — un entretien s'arrête et repart")
    reponses = _charge_les_reponses()
    ids = list(passes.ORDRE)
    moitie = {k: reponses[k] for k in ids[:20] if k in reponses}

    chemin = dossier / "reprise" / "entretien.yml"
    b = _brouillon.charge(chemin)
    for qid, val in moitie.items():
        b.repond(qid, val)
    _brouillon.enregistre(b)
    j.verifie("le brouillon s'écrit", chemin.is_file())

    # On RECHARGE : c est la seance suivante.
    b2 = _brouillon.charge(chemin)
    j.verifie("les 20 réponses sont relues", len(b2.reponses) == len(moitie),
              f"{len(b2.reponses)} au lieu de {len(moitie)}")
    j.verifie("aucune question déjà répondue ne se redemande",
              all(not b2.prochaine() or b2.prochaine().id not in moitie
                  for _ in [0]))
    suivante = b2.prochaine()
    attendue = next(q for q in ids if q not in moitie)
    j.verifie(f"on reprend exactement à {attendue}",
              suivante is not None and suivante.id == attendue,
              f"trouvé : {suivante.id if suivante else None}")
    j.verifie("le rappel relit ce qui a déjà été dit",
              "0.1" in b2.rappel() or ids[19] in b2.rappel())

    # Les conditionnelles se sautent TOUTES SEULES.
    sans_nature = {k: v for k, v in reponses.items()
                   if k not in ("3.2", "3.3", "3.4")}
    sans_nature["3.1"] = "non"
    b3 = _brouillon_neuf(dossier / "sans-nature", sans_nature)
    j.verifie("3.1 = non : 3.2, 3.3 et 3.4 ne se posent plus",
              not [q for q in b3.restantes() if q.id in ("3.2", "3.3", "3.4")],
              str([q.id for q in b3.restantes()]))
    j.verifie("… et elles sont comptées comme SAUTÉES, pas comme oubliées",
              {q.id for q in b3.sautees()} == {"3.2", "3.3", "3.4"},
              str([q.id for q in b3.sautees()]))
    m, griefs = composer.compose(b3)
    j.verifie("… et un brain SANS axe de nature se compose quand même",
              m is not None and "nature" not in (m or {}).get("axes", {}),
              "\n".join(griefs))

    # `--oublier` est le seul moyen de rouvrir.
    b2.oublie("2.6")
    j.verifie("`--oublier` rouvre une question", not b2.a_repondu("2.6"))


# --------------------------------------------------------------------------- #
def scenario_bout_en_bout(j: Journal, dossier: Path) -> Modele | None:
    print("\n5. BOUT EN BOUT — CimeBrain, un TROISIÈME sujet, semé et vérifié")
    reponses = _charge_les_reponses()
    b = _brouillon_neuf(dossier / "cime", reponses)
    _brouillon.enregistre(b)

    m, griefs = composer.compose(b)
    j.verifie("le manifeste se compose, sans un grief", m is not None and not griefs,
              "\n".join(griefs))
    if m is None:
        return None

    fichier = dossier / "cime-manifeste" / "brain.yml"
    _rendu.ecrit(m, fichier, brouillon=str(b.chemin))
    # `uv run` et non `sys.executable` : l en-tete PEP 723 de `schema/valider.py`
    # declare `jsonschema`, que le projet ne porte qu en extra. Le lancer avec
    # l interpreteur courant echouerait a l import, et l echec ne dirait rien du
    # manifeste.
    p = subprocess.run(["uv", "run", str(RACINE_KIT / "schema" / "valider.py"),
                        str(fichier)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       cwd=str(RACINE_KIT))
    j.verifie("le manifeste passe le contrat du lot 1 (schéma + cohérence)",
              p.returncode == 0, p.stdout + p.stderr)

    mo = Modele(yaml.safe_load(fichier.read_text(encoding="utf-8")), fichier)
    cible = dossier / "cimebrain"
    s = semis.seme(mo, cible, ecrire=True, avec_git=True,
                   brouillon=b.chemin.read_text(encoding="utf-8"))
    j.verifie("le semis ne refuse rien", not s.refuse,
              "\n".join(s.manques + s.plan.refus))
    if s.refuse:
        return mo

    v = valide(mo, cible)
    j.verifie("validateur : 0 violation DURE", not v.dures,
              "\n".join(c.rendu() for c in v.dures))
    j.verifie("validateur : 0 avertissement, 0 à mesurer",
              not v.avertissements and not v.a_mesurer,
              "\n".join(c.rendu() for c in v.avertissements + v.a_mesurer))
    g = genere_tout(mo, cible, mode=CHECK)
    j.verifie("générateurs : `--check` silencieux",
              not g.ecarts() and not g.refus,
              f"{len(g.ecarts())} écart(s), {len(g.refus)} refus")

    pages = {p_.stem for p_ in v.contexte.lisibles}
    j.verifie("ZÉRO page d'unité — un hub par dossier, et rien d'autre",
              all(p_.role == mo.role_hub for p_ in v.contexte.lisibles),
              ", ".join(f"{p_.chemin} ({p_.role})" for p_ in v.contexte.lisibles
                        if p_.role != mo.role_hub))
    j.verifie(f"les {len(HUBS_ATTENDUS)} hubs attendus, exactement",
              pages == HUBS_ATTENDUS,
              f"manquants : {sorted(HUBS_ATTENDUS - pages)} ; "
              f"en trop : {sorted(pages - HUBS_ATTENDUS)}")

    inbox = (cible / "Inbox.md").read_text(encoding="utf-8")
    titres = list(reponses["2.1"])
    j.verifie(f"les {len(titres)} titres cités sont dans `Inbox.md`",
              all(t in inbox for t in titres),
              "\n".join(t for t in titres if t not in inbox))
    j.verifie("… et pas une de ces pages n'est écrite",
              not [t for t in titres if t in pages])

    # Le dossier d ATELIER demande en 9.6 existe, et il est VIDE.
    carnet = cible / "Carnet"
    j.verifie("le dossier d'atelier demandé en 9.6 existe et il est vide",
              carnet.is_dir() and not list(carnet.glob("*.md")),
              str(sorted(x.name for x in carnet.iterdir())) if carnet.is_dir()
              else "absent")

    # Le brouillon voyage AVEC l instance, et le skill de reprise est instancie.
    j.verifie("le brouillon de l'entretien est dans l'instance",
              (cible / "AI" / "entretien" / "entretien.yml").is_file())
    skill = cible / ".claude" / "skills" / "reprendre-l-entretien" / "SKILL.md"
    j.verifie("le skill de reprise est instancié", skill.is_file())
    if skill.is_file():
        texte = skill.read_text(encoding="utf-8")
        j.verifie("… et il parle la langue du brain, pas celle du kit",
                  "course" in texte and "massif" in texte
                  and "brique" not in texte)

    _c, auteur = _git(cible, "log", "-1", "--format=%an <%ae>")
    attendue = (f"{m['git']['identite']['name']} "
                f"<{m['git']['identite']['email']}>")
    j.verifie("le commit initial porte l'identité du MANIFESTE",
              auteur == attendue, f"trouvé : {auteur}\nattendu : {attendue}")
    _c, statut = _git(cible, "status", "--porcelain")
    j.verifie("`git status` est vide juste après le semis", statut == "", statut)
    return mo


# --------------------------------------------------------------------------- #
def scenario_invariants(j: Journal, dossier: Path) -> None:
    print("\n6. LES INVARIANTS — ce que l'entretien ne sait pas écrire")
    b = _brouillon_neuf(dossier / "invariants", _charge_les_reponses())
    m, _g = composer.compose(b)
    if m is None:
        j.verifie("le manifeste se compose", False)
        return

    dures = [r["id"] for r in m["regles"] if r["severite"] != "a_mesurer"
             and r.get("active", True)]
    j.verifie("les dix règles ACTIVES sortent toutes en `a_mesurer`", not dures,
              str(dures))
    j.verifie("il y en a exactement dix", len(m["regles"]) == 10,
              str(len(m["regles"])))
    j.verifie("départages et frontières naissent VIDES",
              not m["axes"]["rangement"]["departages"]
              and not m["axes"]["rangement"]["frontieres"]
              and not m["axes"]["nature"]["departages"])
    j.verifie("le vocabulaire de tags naît vide",
              m["vocabulaires"]["tags"].get("vide") is True)
    j.verifie("`vide_autorise` est vrai sur l'axe de nature",
              m["axes"]["nature"]["vide_autorise"] is True)
    j.verifie("les rattachements naissent vides",
              not m["axes"]["rangement"]["rattachements"])

    # Aucun mot d un autre brain. Le controle porte sur le VOCABULAIRE VISIBLE,
    # pas sur les `motif:` — un motif a le droit de citer le DevBrain pour
    # expliquer d ou vient un mecanisme, c est meme sa fonction.
    vocabulaire = {k: v for k, v in m["libelles"].items()
                   if not k.startswith(("motif", "note"))}
    visibles = yaml.safe_dump(vocabulaire, allow_unicode=True) + \
        yaml.safe_dump([{"id": r["id"], "libelle": r["libelle"]}
                        for r in m["roles"]], allow_unicode=True)
    intrus = [mot for mot in refus.LEXIQUE_DU_DEV if mot in visibles.lower()]
    j.verifie("aucun mot du DevBrain dans le vocabulaire visible", not intrus,
              str(intrus))

    # Une severite deduite est refusee, meme si elle « parait evidente ».
    triche = copy.deepcopy(m)
    triche["regles"][1]["severite"] = "dure"
    griefs = refus.controle(b.reponses, triche)
    j.verifie("une sévérité `dure` glissée après coup est REFUSÉE",
              any(n == 6 for n, _ in griefs), str(griefs))

    # Une colonne de bandeau sans source est refusee.
    triche = copy.deepcopy(m)
    triche["bandeau"]["colonnes"].append({"titre": "Ambiance", "source": ""})
    griefs = refus.controle(b.reponses, triche)
    j.verifie("une colonne de bandeau sans champ source est REFUSÉE",
              any(n == 12 for n, _ in griefs), str(griefs))


# --------------------------------------------------------------------------- #
def scenario_defaut_de_manifeste(j: Journal, dossier: Path, mo: Modele | None) -> None:
    print("\n7. DÉFAUT DE MANIFESTE — remontée 3 du lot 5, corrigée")
    cible = dossier / "cimebrain"
    if not (cible / "brain.yml").is_file():
        j.verifie("l'instance du scénario 5 est là", False)
        return

    resolu, dits = defauts.resout(None, cible)
    j.verifie("sans `--manifeste`, c'est le `brain.yml` DU VAULT qui est pris",
              resolu is not None and resolu.resolve() == (cible / "brain.yml").resolve(),
              str(resolu))
    j.verifie("… et rien n'est dit, parce qu'il n'y a rien à dire", not dits,
              "\n".join(dits))

    autre = RACINE_KIT / "exemples" / "histobrain.brain.yml"
    resolu, dits = defauts.resout(autre, cible)
    j.verifie("un `--manifeste` donné l'emporte toujours",
              resolu is not None and resolu.resolve() == autre.resolve())
    j.verifie("… mais l'incohérence est DITE, et elle nomme les deux brains",
              any("CimeBrain" in d and "HistoBrain" in d for d in dits)
              or (any("CimeBrain" in d for d in dits)
                  and any("HistoBrain" in d for d in dits)),
              "\n".join(dits))

    vide = dossier / "pas-un-vault"
    vide.mkdir(parents=True, exist_ok=True)
    resolu, dits = defauts.resout(None, vide)
    j.verifie("un dossier sans `brain.yml` ne se devine PAS un manifeste",
              resolu is None and any("ne se devine pas" in d for d in dits),
              "\n".join(dits))


# --------------------------------------------------------------------------- #
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    j = Journal()
    print("jeu d'épreuve de l'entretien — lot 6")
    with tempfile.TemporaryDirectory(prefix="brainkit-entretien-") as tmp:
        dossier = Path(tmp)
        scenario_questions(j)
        scenario_identite(j, dossier)
        scenario_induction(j)
        scenario_reprise(j, dossier)
        mo = scenario_bout_en_bout(j, dossier)
        scenario_invariants(j, dossier)
        scenario_defaut_de_manifeste(j, dossier, mo)

    print()
    if j.echecs:
        print(f"ÉCHEC — {len(j.echecs)} vérification(s) :")
        for e in j.echecs:
            print(f"  · {e}")
        return 1
    print("OK — le jeu d'épreuve de l'entretien passe en entier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
