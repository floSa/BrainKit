# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6", "jsonschema>=4.21"]
# ///
"""amont.py — le jeu d epreuve de la fraicheur (lot 11).

    uv run tests/amont.py

Six scenarios, et **aucun n appelle le reseau**. C est une contrainte de
conception du lot, pas une commodite : un jeu d epreuve qui sonde GitHub echoue
le jour ou GitHub tousse, et un test qui echoue pour une raison etrangere a ce
qu il teste est un test qu on finit par ignorer. Les faits sont donc SYNTHETIQUES
et la derivation, le rendu et la regle se verifient dessus.

  1. DERIVATION  — les cinq etats depuis des faits bruts, bornes comprises. Le
                   jour du seuil est `recente`, le lendemain `ancienne` : une
                   inegalite mal ecrite ne se voit qu au bord.
  2. BANDEAU     — la colonne `externe:` rend les cinq libelles et accole la
                   date avec le separateur declare.
  3. NEGATIF     — LE scenario du lot. Le MEME manifeste sans son bloc `amont:`
                   ne sonde rien, ne signale rien, et rend un bandeau prive de
                   sa colonne. Un mecanisme declaratif se prouve par son absence.
  4. REGLE       — `amont_concorde` sur un vault reel et un side-car synthetique :
                   les trois sous-cles, et surtout les TROIS SILENCES (page deja
                   declaree morte, page sans amont, page jamais sondee).
  5. CONTRAT     — C11 refuse les quatre declarations mal formees.
  6. REFUS       — le paquet n ecrit que dans le side-car, et ne connait aucun
                   jeton. Verifie par lecture du code, pas par promesse.
"""

from __future__ import annotations

import ast
import copy
import datetime
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit.amont import declaration, derive                  # noqa: E402
from brainkit.amont.declaration import Amont                    # noqa: E402
from brainkit.amont.etat import ETATS                           # noqa: E402
from brainkit.amont.passe import cibles_de_la_page, normalise    # noqa: E402
from brainkit.amont.sidecar import charge_faits                 # noqa: E402
from brainkit.generer import bandeau                            # noqa: E402
from brainkit.valider import valide                             # noqa: E402
from brainkit.valider.manifeste import Modele                   # noqa: E402

MANIFESTE = RACINE_KIT / "tests" / "epreuve.brain.yml"
VERT = RACINE_KIT / "tests" / "vert"
PAQUET = RACINE_KIT / "brainkit" / "amont"

AUJOURDHUI = datetime.date(2026, 9, 8)

# Le bloc `amont:` injete EN MEMOIRE dans le manifeste du jeu d epreuve. Il ne
# nomme ni depot ni paquet : `nature` est l axe de nature d un brain d histoire,
# et c est le point — le mecanisme ne connait pas le sujet.
AMONT_INJECTE = {
    "porte_par": ["source"],
    "champ_url": "cote",
    "champ_confronte": "nature",
    "side_car": "sidecar.json",
    "faits": {"etat": "fraicheur", "date": "fraicheur_date"},
    "sondes": [{"hote": "github.com", "sonde": "github"}],
    "seuils": {"release_ancienne_jours": 730, "commit_ancien_jours": 365},
}
COLONNE = {
    "titre": "Fraîcheur",
    "source": "fraicheur",
    "externe": "amont",
    "qualifie_par": "fraicheur_date",
    "separateur": " · ",
    "table": {"recente": "à jour", "ancienne": "amont ancien",
              "archive": "dépôt archivé", "sans_amont": "aucun amont fiché",
              "jamais_sonde": "amont non sondé"},
}
BANDEAU_INJECTE = {
    "porte_par": ["source"],
    "vide": "—",
    "balises": ["<!-- AUTO:BANDEAU:START -->", "<!-- AUTO:BANDEAU:END -->"],
    "colonnes": [
        {"titre": "Nature", "source": "nature"},
        COLONNE,
    ],
}


class Journal:
    def __init__(self) -> None:
        self.echecs: list[str] = []

    def verifie(self, nom: str, ok: bool, detail: str = "") -> None:
        print(f"   {'OK  ' if ok else 'ÉCHEC'}  {nom}")
        if not ok:
            self.echecs.append(nom + (f" — {detail}" if detail else ""))
            if detail:
                for ligne in detail.splitlines():
                    print(f"          {ligne}")


def charge_dict() -> dict:
    return yaml.safe_load(MANIFESTE.read_text(encoding="utf-8"))


def _amont(seuil_release: int = 730, seuil_commit: int = 365) -> Amont:
    m = copy.deepcopy(AMONT_INJECTE)
    m["seuils"] = {"release_ancienne_jours": seuil_release,
                   "commit_ancien_jours": seuil_commit}
    return declaration(Modele({"amont": m}))


# --------------------------------------------------------------------------- #
def scenario_derivation(j: Journal) -> None:
    print("\n1. DÉRIVATION — les cinq états, bornes comprises")
    a = _amont()
    jour = AUJOURDHUI.isoformat()
    veille = (AUJOURDHUI - datetime.timedelta(days=730)).isoformat()
    lendemain = (AUJOURDHUI - datetime.timedelta(days=731)).isoformat()

    cas = [
        ("jamais_sonde", None, ("jamais_sonde", "")),
        ("jamais_sonde sur un enregistrement vide", {}, ("jamais_sonde", "")),
        ("sans_amont : sondée, rien trouvé",
         {"sonde_le": jour}, ("sans_amont", "")),
        ("recente : une release du jour",
         {"sonde_le": jour, "release_le": jour}, ("recente", jour)),
        ("recente : PILE au seuil (730 j)",
         {"sonde_le": jour, "release_le": veille}, ("recente", veille)),
        ("ancienne : un jour de plus (731 j)",
         {"sonde_le": jour, "release_le": lendemain}, ("ancienne", lendemain)),
        ("archive PRIME sur une release récente",
         {"sonde_le": jour, "release_le": jour, "archive": True,
          "archive_le": "2025-08-07"}, ("archive", "2025-08-07")),
        ("le registre compte comme une release, et la PLUS RÉCENTE gagne",
         {"sonde_le": jour, "release_le": lendemain, "registre_le": jour},
         ("recente", jour)),
        ("sans release, c'est le commit — et son seuil à lui",
         {"sonde_le": jour,
          "commit_le": (AUJOURDHUI - datetime.timedelta(days=400)).isoformat()},
         ("ancienne", (AUJOURDHUI - datetime.timedelta(days=400)).isoformat())),
    ]
    for nom, rec, attendu in cas:
        reel = derive(rec, a, AUJOURDHUI)
        j.verifie(nom, reel == attendu, f"{reel} au lieu de {attendu}")

    j.verifie("les cinq états sont bien cinq, et fermés",
              set(ETATS) == {"recente", "ancienne", "archive", "sans_amont",
                             "jamais_sonde"}, str(ETATS))
    j.verifie("un seuil non déclaré retombe sur le défaut du kit, et le DIT",
              not declaration(Modele({"amont": {**AMONT_INJECTE,
                                                "seuils": {}}})).seuil_declare)


# --------------------------------------------------------------------------- #
def scenario_bandeau(j: Journal) -> None:
    print("\n2. BANDEAU — la colonne `externe:` rend les cinq états")
    mo = Modele({"bandeau": BANDEAU_INJECTE, "amont": AMONT_INJECTE})
    fm = {"nature": "ouvrage"}
    attendus = {
        "recente": "à jour · 2026-09-02",
        "ancienne": "amont ancien · 2019-04-01",
        "archive": "dépôt archivé · 2025-08-07",
        "sans_amont": "aucun amont fiché",
        "jamais_sonde": "amont non sondé",
    }
    dates = {"recente": "2026-09-02", "ancienne": "2019-04-01",
             "archive": "2025-08-07", "sans_amont": "", "jamais_sonde": ""}
    for e, attendu in attendus.items():
        cells = bandeau.cellules(mo, fm,
                                 {"fraicheur": e, "fraicheur_date": dates[e]})
        j.verifie(f"état `{e}` → « {attendu} »", cells[1] == attendu,
                  f"« {cells[1]} »")
    j.verifie("la colonne ordinaire lit toujours le frontmatter",
              bandeau.cellules(mo, fm, {"fraicheur": "recente"})[0] == "ouvrage")
    j.verifie("un état inconnu rend le caractère vide, il n'est pas absorbé",
              bandeau.cellules(mo, fm, {"fraicheur": "tiède"})[1] == "—")
    j.verifie("sans le moindre fait, la cellule est vide — pas plausible",
              bandeau.cellules(mo, fm, {})[1] == "—")
    j.verifie("le séparateur déclaré est employé, pas une espace",
              " · " in bandeau.cellules(
                  mo, fm, {"fraicheur": "recente",
                           "fraicheur_date": "2026-09-02"})[1])


# --------------------------------------------------------------------------- #
def scenario_negatif(j: Journal) -> None:
    print("\n3. NÉGATIF — le même manifeste SANS bloc `amont:`")
    nu = Modele({"bandeau": {**BANDEAU_INJECTE,
                             "colonnes": [{"titre": "Nature", "source": "nature"}]}})
    a = declaration(nu)
    j.verifie("`amont:` absent → déclaration non déclarée", not a.declare)
    j.verifie("aucun fait chargé, et aucune lecture de fichier",
              charge_faits(nu, VERT) == {})
    j.verifie("le bandeau rend UNE colonne, pas deux",
              len(bandeau.cellules(nu, {"nature": "ouvrage"})) == 1)

    m = charge_dict()
    mo = Modele(m, MANIFESTE)
    v = valide(mo, VERT)
    j.verifie("la règle `amont_concorde` ne tourne pas et l'inventaire le dit",
              v.rapport.etats.get("amont_concorde") == "non déclarée par ce manifeste",
              str(v.rapport.etats.get("amont_concorde")))
    j.verifie("zéro constat de fraîcheur",
              not [c for c in v.rapport.constats if c.regle == "amont_concorde"])


# --------------------------------------------------------------------------- #
SIDE_CAR = {
    # ouvrage (non éliminatoire) + archivé → sous-clé `archive`
    "Antiquité/Rome/Suetone - Vies des Cesars.md": {
        "sonde_le": "2026-09-08", "etat": "archive", "date": "2025-08-07"},
    # ouvrage + au-delà du seuil → sous-clé `ancien`
    "Transversal/Histoire de France.md": {
        "sonde_le": "2026-09-08", "etat": "ancienne", "date": "2019-04-01"},
    # source-primaire (ÉLIMINATOIRE) + amont vivant → sous-clé `contredit`
    "Antiquité/Herodote - Histoires.md": {
        "sonde_le": "2026-09-08", "etat": "recente", "date": "2026-09-02"},
    # source-primaire + archivé → RIEN : la page le dit déjà
    "Antiquité/Rome/Tacite - Annales.md": {
        "sonde_le": "2026-09-08", "etat": "archive", "date": "2024-01-01"},
    # sondée, rien à atteindre → RIEN, mais DANS la population
    "XXe siècle/Fonds Moscou.md": {
        "sonde_le": "2026-09-08", "etat": "sans_amont", "date": ""},
    # « Kennan » est absente : jamais sondée, donc HORS population
}


def scenario_regle(j: Journal) -> None:
    print("\n4. RÈGLE — `amont_concorde` sur un side-car synthétique")
    m = charge_dict()
    m["amont"] = copy.deepcopy(AMONT_INJECTE)
    m["champs"]["nature"]["eliminatoire"] = ["source-primaire"]
    m["regles_de_socle"].append({
        "id": "amont_concorde", "severite": "avertissement",
        "enonce": "L'amont sondé ne contredit pas ce que la page déclare.",
        "motif": "Jamais dure : le désaccord est avec un tiers, pas une faute de rédaction."})

    tmp = Path(tempfile.mkdtemp(prefix="brainkit-amont-"))
    vault = tmp / "vert"
    shutil.copytree(VERT, vault)
    (vault / "sidecar.json").write_text(
        json.dumps(SIDE_CAR, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        v = valide(Modele(m, MANIFESTE), vault)
        constats = [c for c in v.rapport.constats if c.regle == "amont_concorde"]
        par_cle = {}
        for c in constats:
            par_cle.setdefault(c.cle, []).append(c.page)
        attendu = {
            "archive": ["Antiquité/Rome/Suetone - Vies des Cesars.md"],
            "ancien": ["Transversal/Histoire de France.md"],
            "contredit": ["Antiquité/Herodote - Histoires.md"],
        }
        j.verifie("les trois sous-clés, et elles seules",
                  {k: sorted(v_) for k, v_ in par_cle.items()} == attendu,
                  f"{ {k: sorted(x) for k, x in par_cle.items()} }")
        j.verifie("une page déjà déclarée morte ne produit RIEN",
                  "Antiquité/Rome/Tacite - Annales.md"
                  not in [c.page for c in constats])
        j.verifie("une page sans amont atteignable ne produit RIEN",
                  "XXe siècle/Fonds Moscou.md" not in [c.page for c in constats])
        j.verifie("aucun constat n'est DUR",
                  all(c.severite == "avertissement" for c in constats),
                  str({c.severite for c in constats}))
        pop = v.rapport.population_de("amont_concorde")
        j.verifie("la population est le nombre de pages SONDÉES (5), pas de pages (6)",
                  pop is not None and pop.pages == 5,
                  str(pop))
        j.verifie("la page jamais sondée est nommée dans une note",
                  any("jamais sondée" in n for n in v.rapport.notes),
                  str(v.rapport.notes))
        j.verifie("le vault reste vert : zéro violation dure", not v.dures,
                  "\n".join(c.rendu() for c in v.dures))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------- #
def scenario_contrat(j: Journal) -> None:
    print("\n5. CONTRAT — C11 refuse les déclarations mal formées")
    sys.path.insert(0, str(RACINE_KIT / "schema"))
    from valider import coherence                              # noqa: PLC0415

    def codes(m: dict) -> list[str]:
        return [f"{ou} : {msg}" for ou, msg in coherence(m)
                if msg.startswith("C11")]

    base = charge_dict()

    sans_bloc = copy.deepcopy(base)
    sans_bloc["bandeau"] = {**BANDEAU_INJECTE}
    j.verifie("colonne `externe: amont` sans bloc `amont:` → refusée",
              len(codes(sans_bloc)) == 1, str(codes(sans_bloc)))

    champ_inconnu = copy.deepcopy(base)
    champ_inconnu["amont"] = {**AMONT_INJECTE, "champ_url": "url_inexistante"}
    j.verifie("`amont.champ_url` non défini dans `champs:` → refusé",
              any("champ_url" in c for c in codes(champ_inconnu)),
              str(codes(champ_inconnu)))

    role_inconnu = copy.deepcopy(base)
    role_inconnu["amont"] = {**AMONT_INJECTE, "porte_par": ["fantome"]}
    j.verifie("`amont.porte_par` sur un rôle inconnu → refusé",
              any("porte_par" in c for c in codes(role_inconnu)),
              str(codes(role_inconnu)))

    table_trouee = copy.deepcopy(base)
    table_trouee["amont"] = copy.deepcopy(AMONT_INJECTE)
    col = copy.deepcopy(COLONNE)
    del col["table"]["archive"]
    col["table"]["tiède"] = "tiède"
    table_trouee["bandeau"] = {**BANDEAU_INJECTE,
                               "colonnes": [{"titre": "Nature", "source": "nature"},
                                            col]}
    dits = codes(table_trouee)
    j.verifie("un état sans libellé est signalé (cellule vide sur un fait connu)",
              any("archive" in c and "sans libelle" in c for c in dits), str(dits))
    j.verifie("un état hors de la liste fermée est signalé",
              any("tiède" in c for c in dits), str(dits))

    bon = copy.deepcopy(base)
    bon["amont"] = copy.deepcopy(AMONT_INJECTE)
    bon["amont"]["champ_url"] = "cote"
    bon["bandeau"] = copy.deepcopy(BANDEAU_INJECTE)
    j.verifie("la déclaration bien formée passe C11 sans un mot",
              codes(bon) == [], str(codes(bon)))


# --------------------------------------------------------------------------- #
ECRITURE = re.compile(r"^(write_text|write_bytes|mkdir|unlink|rmtree|rename)$")
JETON = re.compile(r"token|authorization|bearer|api[-_]?key|--fix", re.I)


def code_effectif(fichier: Path) -> list[tuple[int, str]]:
    """(ligne, symbole ou chaine) de tout ce que le fichier EXECUTE.

    Les docstrings sont ecartees, et il le faut : ce module explique en toutes
    lettres qu il n emploie ni jeton ni `--fix`, et une lecture au grep prendrait
    l explication pour la chose. Ce qu on veut prouver, c est qu aucun CHEMIN
    D EXECUTION ne les nomme — donc on lit l arbre, pas le texte.
    """
    arbre = ast.parse(fichier.read_text(encoding="utf-8"))
    docstrings: set[int] = set()
    for n in ast.walk(arbre):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                          ast.ClassDef)):
            corps = getattr(n, "body", [])
            if corps and isinstance(corps[0], ast.Expr) \
                    and isinstance(corps[0].value, ast.Constant) \
                    and isinstance(corps[0].value.value, str):
                docstrings.add(id(corps[0].value))
    out: list[tuple[int, str]] = []
    for n in ast.walk(arbre):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) \
                and id(n) not in docstrings:
            out.append((n.lineno, n.value))
        elif isinstance(n, ast.Name):
            out.append((n.lineno, n.id))
        elif isinstance(n, ast.Attribute):
            out.append((n.lineno, n.attr))
        elif isinstance(n, ast.keyword) and n.arg:
            out.append((getattr(n.value, "lineno", 0), n.arg))
        elif isinstance(n, ast.arg):
            out.append((n.lineno, n.arg))
    return out


def scenario_refus(j: Journal) -> None:
    print("\n6. REFUS — ce que le paquet ne fait pas, vérifié dans le code")
    fichiers = sorted(PAQUET.glob("*.py"))
    j.verifie("le paquet a bien été lu", len(fichiers) >= 5, str(fichiers))

    ecritures: list[str] = []
    jetons: list[str] = []
    for f in fichiers:
        for n, mot in code_effectif(f):
            if ECRITURE.match(mot):
                ecritures.append(f"{f.name}:{n} {mot}")
            if JETON.search(mot):
                jetons.append(f"{f.name}:{n} {mot}")

    # Les seules ecritures legitimes : le side-car, et le `--rapport` qu on
    # demande explicitement. Toute autre est une porte ouverte sur les pages.
    permises = [e for e in ecritures
                if e.startswith("sidecar.py:") or e.startswith("__main__.py:")]
    j.verifie("aucune écriture hors du side-car et de `--rapport`",
              len(permises) == len(ecritures),
              "\n".join(e for e in ecritures if e not in permises))
    j.verifie("le side-car est bien écrit quelque part", bool(permises))
    j.verifie("aucun jeton d'API ni `--fix` sur un chemin d'exécution",
              not jetons, "\n".join(jetons))

    # La normalisation de nom de paquet, et la lecture d une URL de depot :
    # deux fonctions pures, sans reseau, qui decident CE QU ON VA SONDER.
    j.verifie("un nom de paquet se normalise (PEP 503)",
              normalise("Scikit_Learn.Extra") == "scikit-learn-extra",
              normalise("Scikit_Learn.Extra"))
    a = _amont()
    depot, registre, url = cibles_de_la_page(
        {"cote": "https://github.com/pola-rs/polars", "nature": "ouvrage"}, a)
    j.verifie("une URL de dépôt donne son slug",
              depot == ("github", "pola-rs/polars"), str(depot))
    depot, _r, _u = cibles_de_la_page(
        {"cote": "https://git.deuxfleurs.fr/x/y", "nature": "ouvrage"}, a)
    j.verifie("un hôte non déclaré ne se devine pas : aucune cible",
              depot is None, str(depot))
    j.verifie("aucun registre déclaré ici → aucune cible de registre",
              registre is None, str(registre))


# --------------------------------------------------------------------------- #
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    print("épreuve — l'amont et la fraîcheur, lot 11 (aucun appel réseau)")
    j = Journal()
    scenario_derivation(j)
    scenario_bandeau(j)
    scenario_negatif(j)
    scenario_regle(j)
    scenario_contrat(j)
    scenario_refus(j)

    print()
    if j.echecs:
        print(f"{len(j.echecs)} vérification(s) en échec :")
        for e in j.echecs:
            print(f"  - {e}")
        return 1
    print("OK — le jeu d'épreuve de l'amont passe en entier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
