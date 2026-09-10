"""semis.py — l orchestration : de `brain.yml` a un vault vierge, valide et committe.

# L ordre, et les deux arbitrages qu il porte

    exigences  ->  plan  ->  pages  ->  generateurs  ->  depot

1. **Les exigences d abord, toutes d un coup.** Un manifeste incomplet est
   REFUSE, jamais seme a moitie : un vault a demi ecrit fait dire n importe quoi
   a ses deux validateurs, et le premier geste de l utilisateur serait de
   reparer une structure que personne n a cassee.

2. **Les artefacts derives sont poses par les GENERATEURS, pas par le semis.**
   C est le point le plus important du module, et il est verifiable : le semis
   n ecrit ni `AI/index/`, ni la carte des liens, ni un bandeau. Il ecrit ce qui
   s ecrit UNE FOIS, puis il appelle `generer` en mode ecriture sur le vault
   qu il vient de poser. Deux consequences :

     - il n existe pas deux codes qui composent le meme artefact — le defaut
       que le manifeste existe pour supprimer (constat E4) ;
     - le semis est **a son point fixe par construction**. Un
       `brainkit generer --check` lance juste apres est silencieux, et le
       critere du lot dit qu un semis qui ne l est pas est un semis faux.

# Arbitrage 1 — l arbre naît PLAT

Un dossier par prefixe declare, et rien en dessous. La promotion d une
sous-valeur se calcule sur une population de pages qui vaut zero le jour du
semis ; poser d avance les dossiers des sous-valeurs declarees creerait des
dossiers que `chemins.dossier_attendu()` ne rendrait pas, et que `re-seuiller`
proposerait aussitot de defaire.

# Arbitrage 2 — aucun hub d axe transverse n est seme, seulement son DOSSIER

§3.3 du cadrage annonce « les dossiers des axes transverses, avec un hub par
valeur ». Le lot 4 a mesure et ecrit le contraire, et c est lui qui a raison :
*« une valeur declaree que personne ne porte ne produit AUCUN hub : le vault
n aurait rien a y montrer, et une page vide dans un graphe est un nœud de plus
qui ne rassemble rien »* (`generer/hubs.py`, `hubs_transverses`). Semer les
quatorze hubs de BrainRef reviendrait a poser quatorze pages qu aucun
generateur ne regenererait, qu il faudrait citer depuis la porte d entree pour
qu elles soient atteignables, et qui n auraient rien a montrer.

Le dossier, lui, est seme — avec un `.gitkeep`, git ne suivant aucun dossier
vide — parce qu il dit OU ces hubs naitront. Et ils naitront tout seuls : le
generateur sait creer un hub transverse absent (`hubs._hub_neuf`), et c est
eprouve depuis le lot 4.

Le contrat du kit reste donc « le livrable le plus recent a raison », et la
divergence avec §3.3 est ecrite ici plutot que resolue en silence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..generer import genere_tout
from ..generer.sortie import CHECK, ECRIRE, Sortie
from ..valider.manifeste import Modele
from . import depot as _depot
from . import entretien as _entretien
from . import exigences, gouvernance, pages, ponts
from .plan import Plan
from .prose import ProseSemis
from ..emballer import rendus as _documents

RACINE_KIT = Path(__file__).resolve().parents[2]


@dataclass
class Semis:
    plan: Plan
    manques: list[str] = field(default_factory=list)
    generation: Sortie | None = None
    depot: _depot.Depot | None = None

    @property
    def refuse(self) -> bool:
        return bool(self.manques) or self.plan.refuse

    @property
    def code(self) -> int:
        if self.refuse:
            return 1
        if self.depot is not None and not self.depot.ok:
            return 1
        if self.generation is not None and self.generation.refus:
            return 1
        return 0


def seme(mo: Modele, racine: Path, ecrire: bool = False,
         avec_git: bool = True, message: str | None = None,
         brouillon: str | None = None) -> Semis:
    """De `brain.yml` a un vault vierge. `ecrire=False` n ecrit pas un octet.

    `brouillon` est le texte du brouillon d entretien, quand il y en a un. Le
    semis le POSE, il ne le fabrique pas : un manifeste ecrit a la main n a pas
    de trace d entretien, et en inventer une serait la pire des traces.
    """
    manques = exigences.controle(mo)
    plan = Plan(racine=racine, ecrire=ecrire and not manques,
                racine_du_kit=RACINE_KIT)
    s = Semis(plan=plan, manques=manques)
    if s.refuse:
        return s

    prose = ProseSemis(mo)

    # --- ce qui s ecrit UNE fois ----------------------------------------- #
    pages.seme_les_hubs(mo, prose, plan)
    for t in mo.transverses:
        # Le dossier, pas les hubs — cf. arbitrage 2 du docstring.
        plan.dossier(str(t["dossier"]), garde=True)
    pages.seme_les_gabarits(mo, prose, plan)
    pages.seme_la_racine(mo, prose, plan)
    gouvernance.seme_la_gouvernance(mo, prose, plan)
    gouvernance.seme_le_routeur(mo, prose, plan)
    gouvernance.seme_l_espace_agent(mo, prose, plan)
    gouvernance.seme_les_skills(mo, plan)
    ponts.seme_les_ponts(mo, plan)
    _pose_les_documents(mo, plan)
    _entretien.seme_l_entretien(mo, plan, brouillon)
    _depot.seme_les_hooks(mo, plan)
    _pose_le_manifeste(mo, plan)

    if plan.refuse or not ecrire:
        return s

    # --- ce que les GENERATEURS posent, et eux seuls ---------------------- #
    s.generation = genere_tout(mo, plan.racine, mode=ECRIRE)

    # --- le depot ---------------------------------------------------------- #
    if avec_git:
        s.depot = _depot.initialise(mo, plan.racine, message=message, ecrire=True)
    return s


def _pose_les_documents(mo: Modele, plan: Plan) -> None:
    """`INSTALL.md` et les trois guides — GENERES, comme les gabarits.

    Ce sont des artefacts de SEMIS, pas d artefacts derives : ils s ecrivent une
    fois, puis se relisent — aucun generateur ne les rafraichit a chaque
    cloture, et `generer --check` ne les regarde pas. Le motif est celui de
    `Home.md` (arbitrage 3.1 du lot 5) : un document que le proprietaire du
    brain peut vouloir completer ne se regenere pas sous ses pieds.

    Ils sont POSES ICI et pas ailleurs pour une raison de discipline : le semis
    a un plan d ecriture unique, et un module qui ecrirait directement
    contournerait ses quatre refus.
    """
    for chemin, texte in _documents(mo).items():
        plan.pose(chemin, texte, "documents")


def _pose_le_manifeste(mo: Modele, plan: Plan) -> None:
    """`brain.yml` a la racine de l instance — la source de tout le reste.

    Copie a l identique, commentaires compris. Les `motif:` d un manifeste sont
    la moitie de sa valeur : ils portent POURQUOI une valeur est celle-la, et
    une copie qui les perdrait rendrait le fichier illisible en six mois.
    """
    if mo.chemin is None or not mo.chemin.is_file():
        plan.refuse_avec("le manifeste n'a pas de fichier source — impossible de "
                         "le poser à la racine de l'instance")
        return
    plan.pose("brain.yml", mo.chemin.read_text(encoding="utf-8"), "manifeste")


# --------------------------------------------------------------------------- #
def imprime(s: Semis, mo: Modele, racine: Path, detail: int = 0) -> int:
    """Le rapport du semis. Chiffre, et par famille."""
    nom = mo.brain.get("nom") or "?"
    mode = "écriture" if s.plan.ecrire else "lecture (rien n'est écrit)"
    print(f"semer ({mode}) — `{nom}` dans `{racine}`, manifeste "
          f"`{mo.chemin.name if mo.chemin else '(inconnu)'}`")

    if s.manques:
        print(f"\n{len(s.manques)} manque(s) dans le manifeste — REFUSÉ, rien "
              f"n'a été écrit :")
        for m in s.manques:
            print(f"  [MANQUE] {m}")
        return 1
    if s.plan.refus:
        print(f"\n{len(s.plan.refus)} refus :")
        for r in s.plan.refus:
            print(f"  [REFUS] {r}")
        return 1

    for quoi, n in s.plan.par_quoi().items():
        print(f"  {quoi or '(sans famille)':14s} · {n:4d} fichier(s)")
    print(f"  {'dossiers':14s} · {len(s.plan.dossiers):4d}")
    print(f"  {'TOTAL':14s} · {len(s.plan.fichiers):4d} fichier(s)")
    if detail:
        for f in s.plan.fichiers[:detail]:
            print(f"    {f.chemin}")
        if len(s.plan.fichiers) > detail:
            print(f"    … {len(s.plan.fichiers) - detail} autre(s)")

    if s.generation is not None:
        g = s.generation
        ecrits = sum(1 for p in g.poses if p.etat != "identique")
        print(f"\ngénérateurs — {len(g.poses)} artefact(s) dérivé(s), "
              f"{ecrits} écrit(s), {g.passes} passe(s)")
        for r in g.refus:
            print(f"  [REFUS] {r}")

    if s.depot is not None:
        d = s.depot
        if d.echecs:
            print("\ndépôt — ÉCHEC :")
            for e in d.echecs:
                print(f"  {e}")
        else:
            print(f"\ndépôt — initialisé, hooks actifs, commit `{d.commit}`")

    if s.code:
        return s.code
    if not s.plan.ecrire:
        print(f"\nOK — {len(s.plan.fichiers)} fichier(s) SERAIENT écrits. "
              f"Relancer avec `--ecrire` pour semer.")
    else:
        print(f"\nOK — `{nom}` semé.")
    return 0


def verifie(mo: Modele, racine: Path) -> tuple[int, int, int]:
    """(violations dures, avertissements, écarts de génération) sur l instance semée.

    Le critere d acceptation du lot, en une fonction : les deux validateurs
    verts sur zero page d unite, et les generateurs silencieux en `--check`.
    """
    from ..valider import valide
    v = valide(mo, racine)
    g = genere_tout(mo, racine, mode=CHECK)
    return len(v.dures), len(v.avertissements) + len(v.a_mesurer), len(g.ecarts())
