# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""fidelite.py — le manifeste sait-il redire le vault ?

Lot 2 de BrainKit. Lit UN manifeste (`exemples/devbrain.brain.yml`) et UN vault
(DevBrain), et rapporte CHAQUE divergence entre ce que le manifeste declare et ce
que le vault est. Rien d autre :

  - LECTURE SEULE. Aucune ecriture, aucun deplacement, aucun artefact genere.
  - CE N EST PAS le validateur de vault. Les dix regles de `brain-v3.md` §10
    (reciprocite, reinjection du resume, citation unique…) sont le lot 3. Ici on
    ne compare que le MANIFESTE au VAULT : gabarits de frontmatter, vocabulaires
    d enumeration, gabarits de corps, champs conditionnels, derivation du chemin.
  - CE N EST PAS le validateur de manifeste. `schema/valider.py` (lot 1) verifie
    qu un `brain.yml` est bien forme ; ici on verifie qu il est VRAI.

Tout est pilote par le manifeste : aucune valeur de DevBrain n est ecrite dans ce
fichier. Le seuil de promotion, les 20 prefixes, les 109 valeurs d axe, les 38
sections de corps, les 4 colonnes du bandeau sont LUS. Un test qui recopierait le
vault ne testerait rien.

# Les deux boites

Chaque divergence finit dans exactement une des deux, et la table `VERDICTS`
ci-dessous porte le verdict de chaque groupe, nommement :

  1. `manifeste` — le manifeste dit faux, le vault a raison. Le manifeste est
     corrige.
  2. `vault` — le manifeste dit vrai, le vault s en ecarte. C est documente et
     NON repare, meme quand c est une vraie faute de la page.

Un groupe de divergences sans verdict sort en `INEXPLIQUEE` et l outil sort en
code 1. C est le critere du lot, tenu par du code : aucune divergence ne traine.

Usage :
    uv run outils/fidelite.py                       # les chemins par defaut
    uv run outils/fidelite.py --vault <chemin> --manifeste <chemin>
    uv run outils/fidelite.py --pages               # nomme TOUTES les pages
    uv run outils/fidelite.py --groupe C2           # un seul groupe, en entier

Sort en 0 si toute divergence porte un verdict, en 1 sinon.
"""

from __future__ import annotations

import argparse
import collections
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    sys.exit("PyYAML manquant — lancer via uv : uv run outils/fidelite.py")

RACINE = Path(__file__).resolve().parent.parent
MANIFESTE_DEFAUT = RACINE / "exemples" / "devbrain.brain.yml"
VAULT_DEFAUT = RACINE.parent / "DevBrain"

# Titres de niveau 0 du manifeste : ce ne sont pas des titres markdown mais des
# marqueurs de place (bandeau, embed, accroche, zone AUTO). Ils ne se cherchent
# donc pas parmi les `##` d une page.
NIVEAU_0 = 0

# --------------------------------------------------------------------------- #
# VERDICTS — un par groupe de divergences. `boite` vaut `manifeste` (le manifeste
# disait faux, il a ete corrige) ou `vault` (le manifeste dit vrai, le vault s en
# ecarte, on ne repare pas). Le motif est celui qui est ecrit dans
# `design/02-rapport-fidelite.md`, en une ligne.
#
# La cle est `<code>/<sujet>` — le meme couple que le rapport imprime. Un groupe
# absent de cette table sort en INEXPLIQUEE et fait echouer l outil.
# --------------------------------------------------------------------------- #
M = "manifeste"
V = "vault"

VERDICTS: dict[str, tuple[str, str]] = {

    # ------------------------------------------------ boite 1 : le manifeste
    # Cinq sections declarees INCONDITIONNELLES et qui ne sont pas universelles.
    # Le manifeste portait deja leur `mesure:` exacte — il savait donc qu elles
    # ne l etaient pas. C est la meme faute que `Les maths, simplement` avant la
    # remontee 3 du lot 1, sur cinq sections que personne n avait comptees.
    # Les cles C1/* sont celles d AVANT la correction, les cles C4/* celles d
    # APRES : les deux portent le meme verdict, pour que l outil sorte en 0 sur
    # les deux versions du manifeste et qu on puisse rejouer l avant.
    "C1/brique.Alternatives": (M, "section non universelle (324/337) declaree sans "
                                  "condition — `existe_si` ajoute au lot 2"),
    "C4/brique.Alternatives": (M, "corrige au lot 2 : `existe_si` declare, 13 pages "
                                  "sans voisine a nommer"),
    "C1/brique.Compléments": (M, "section non universelle (103/337) declaree sans "
                                 "condition — `existe_si` ajoute au lot 2"),
    "C4/brique.Compléments": (M, "corrige au lot 2 : `existe_si` declare, la section "
                                 "suit `complements:`"),
    "C1/hub.Notes": (M, "section non universelle (13/74) declaree sans condition — "
                        "`existe_si` ajoute au lot 2"),
    "C4/hub.Notes": (M, "corrige au lot 2 : `existe_si` declare, 13 hubs portent une "
                        "note manuelle"),
    "C1/hub.Ce qu'il faut comprendre": (M, "71/74 — declaree sans condition, et le "
                                           "`motif` du role nommait les mauvais trois"),
    "C4/hub.Ce qu'il faut comprendre": (M, "corrige au lot 2 : `existe_si` declare et "
                                           "les trois hubs nommes"),
    "C1/hub.Choisir": (M, "71/74 — declaree sans condition, meme cas que la section "
                          "voisine"),
    "C4/hub.Choisir": (M, "corrige au lot 2 : `existe_si` declare et les trois hubs "
                          "nommes"),
    "C14/brique.Alternatives": (M, "51 pages portent la section avec un champ vide — la "
                                   "forme que la regle 8 RECOMMANDE. Le `champ:` seul "
                                   "surdeclarait le miroir ; `existe_si` le dit"),
    "C16/hub.Comparatifs": (M, "`roles[hub].corps` ne declare qu UNE forme de zone AUTO "
                               "alors que le vault en a trois — arbre, ralliement, "
                               "transverse. Motif ajoute, forme a trancher au lot 4"),
    "F7/brique.hosted": (M, "`si:` etait ecrit comme une OBLIGATION (« quand l exiger ») "
                            "et DevBrain n en fait qu une PERMISSION — 21 briques des "
                            "trois familles ne portent pas le champ, et les 21 portent "
                            "`os:` a la place. Spec corrigee au lot 2"),
    "F7/brique.scaling": (M, "meme cas que `hosted:`, memes 21 pages — la condition "
                             "permet, elle n exige pas"),

    # ------------------------------------------------ boite 2 : le vault
    "A1/skill/code-quality": (V, "valeur declaree sans page — la regle de retrait n a "
                                 "pas ete appliquee a `skill/*` (remontee 6 bis)"),
    "A1/skill/data": (V, "idem `skill/code-quality`"),
    "A1/skill/dev-flow": (V, "idem `skill/code-quality`"),
    "A1/skill/documents": (V, "idem `skill/code-quality`"),
    "A1/skill/meta": (V, "idem `skill/code-quality`"),
    "A3/automation/no-code": (V, "libelle garde apres un plafond de promotion — le "
                                 "manifeste le declare et l explique"),
    "A3/storage/objet": (V, "idem `automation/no-code`"),
    "C1/brique.Écosystème": (V, "4 briques ne portent AUCUNE section Ecosysteme — le "
                                "manifeste le declare comme une faute du vault "
                                "(remontee 4). Non reparee : le lot 9 seul ecrit"),
    "C2/hub.Aperçu": (V, "2 hubs de domaine ont absorbe une notion chapeau et gardent "
                         "son corps de notion"),
    "C2/hub.Concepts clés": (V, "idem — corps de notion sur un hub"),
    "C2/hub.Les maths, simplement": (V, "idem — corps de notion sur un hub"),
    "C2/hub.En pratique": (V, "idem — corps de notion sur un hub"),
    "C2/hub.Approches voisines & alternatives": (V, "idem — corps de notion sur un hub"),
    "C2/hub.Pour aller plus loin": (V, "idem — corps de notion sur un hub"),
    "C2/comparatif.Pourquoi la vue liste ses membres nom par nom": (
        V, "section manuelle ajoutee a un comparatif — hors gabarit, assumee"),
    "C2/comparatif.Ce comparatif ne compare rien, et ce n'est pas la conversion qui le règle": (
        V, "meme cas — une note d arbitrage laissee dans la page"),
    "C3/brique.Modèles locaux disponibles": (V, "un `###` dans une section `etiquetee`, "
                                                "sur une page"),
    "C3/notion.Outils — données tabulaires & factices (hors LLM)": (
        V, "un `###` dans une section `liste_liens`, sur une page"),
    "C4/notion.Les maths, simplement": (V, "282/297 — 15 notions n ont pas de maths a "
                                           "expliquer et la section n a pas ete posee "
                                           "vide (remontee 3, retrouvee)"),
    "C11/brique.Ressources": (V, "4 « Site » et 1 « Poids » hors du vocabulaire declare "
                                 "— les 5 violations que le lot 8 a mesurees"),
    "F8/brique.os": (V, "champ declare vestigial et encore porte par 37 briques "
                        "(remontee 8)"),
    "F8/brique.domaines": (V, "champ declare vestigial et encore porte par 30 briques "
                              "(remontee 8)"),
    "F12/brique.famille": (V, "1 brique sans valeur d axe de nature — LEGAL, "
                              "`vide_autorise: true` : le champ vide est le signal de "
                              "« l arbre n a pas tranche »"),
    "N1/ml/hub": (V, "`ml/hub` est une sous-valeur homonyme du role `hub`, portee par "
                     "2 briques — meme famille que la remontee 7 (`domaine:`)"),
}


# ======================================================================== #
#  Lecture du vault
# ======================================================================== #
@dataclass
class Page:
    chemin: Path              # relatif a la racine du vault
    role: str | None
    fm: dict
    corps: str
    absolu: Path = Path()     # le chemin reel, pour tester un fichier voisin
    titres: list[tuple[int, str, str]] = field(default_factory=list)
    # (niveau, titre, section de niveau 2 englobante)
    illisible: str | None = None

    @property
    def dossier(self) -> str:
        return self.chemin.parent.as_posix()

    @property
    def nom_fichier(self) -> str:
        return self.chemin.stem


RE_TITRE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
RE_FENCE = re.compile(r"^\s*(```|~~~)")


def parse_page(md: Path, racine: Path) -> Page:
    """Une page lue. Les quatre motifs d illisibilite sont distingues, jamais avales."""
    rel = md.relative_to(racine)
    txt = md.read_text(encoding="utf-8")
    if not txt.startswith("---"):
        return Page(rel, None, {}, "", md, illisible="aucun frontmatter (le fichier ne commence pas par `---`)")
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return Page(rel, None, {}, "", md, illisible="frontmatter non referme (pas de second `---`)")
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        return Page(rel, None, {}, "", md, illisible=f"YAML invalide — {str(e).splitlines()[0].strip()}")
    if not isinstance(fm, dict):
        return Page(rel, None, {}, "", md, illisible=f"frontmatter lu comme {type(fm).__name__}, pas un dictionnaire")

    corps = parts[2]
    p = Page(rel, (str(fm.get("role")) if fm.get("role") is not None else None), fm, corps, md)

    dans_fence = False
    courante = ""          # derniere section de niveau 2 rencontree
    for ligne in corps.splitlines():
        if RE_FENCE.match(ligne):
            dans_fence = not dans_fence
            continue
        if dans_fence:
            continue
        m = RE_TITRE.match(ligne)
        if not m:
            continue
        niveau, titre = len(m.group(1)), m.group(2)
        if niveau == 1:
            continue           # le H1 est le nom de la page, pas une section
        if niveau == 2:
            courante = titre
        p.titres.append((niveau, titre, courante if niveau > 2 else ""))
    return p


def lire_vault(racine: Path, non_pages: set[str]) -> list[Page]:
    pages: list[Page] = []
    for d in sorted(racine.iterdir()):
        if not d.is_dir() or d.name in non_pages:
            continue
        for md in sorted(d.rglob("*.md")):
            pages.append(parse_page(md, racine))
    return pages


# ======================================================================== #
#  Lecture du manifeste — le modele que le vault doit satisfaire
# ======================================================================== #
class Modele:
    """Ce que le manifeste declare, mis en forme pour etre confronte au vault.

    Aucune valeur en dur : tout vient du fichier. Les seules constantes de ce
    module sont des conventions de FORMAT (un `##` est un titre de niveau 2), pas
    des valeurs de DevBrain.
    """

    def __init__(self, m: dict):
        self.m = m
        self.roles = {r["id"]: r for r in m.get("roles") or []}
        self.champs = m.get("champs") or {}
        axes = m.get("axes") or {}
        self.rangement = axes.get("rangement") or {}
        self.nature = axes.get("nature") or {}
        self.transverses = axes.get("transverses") or []
        self.bandeau = m.get("bandeau") or {}
        genere = m.get("genere") or {}
        self.non_pages = set(genere.get("non_pages") or [])
        self.champ_rangement = self.rangement.get("champ") or ""
        self.champ_nature = self.nature.get("champ") or ""
        self.seuil = int(self.rangement.get("seuil_promotion") or 0)
        self.plafond = bool(self.rangement.get("plafond_promotion"))
        self.valeur_courte = bool(self.rangement.get("valeur_courte_autorisee"))

        # --- prefixes de l axe de rangement, rattachements compris
        self.dossier_de_prefixe: dict[str, str] = {}
        self.sous: dict[str, dict] = {}          # "pfx/sub" -> declaration
        self.prefixe_rattache: set[str] = set()
        self.prefixes_de_l_axe: list[str] = [p["cle"] for p in
                                             (self.rangement.get("prefixes") or [])]
        for p in self.rangement.get("prefixes") or []:
            self.dossier_de_prefixe[p["cle"]] = p["dossier"]
            for sub, decl in (p.get("sous") or {}).items():
                self.sous[f"{p['cle']}/{sub}"] = decl or {}
        for cle, decl in (self.rangement.get("rattachements") or {}).items():
            self.dossier_de_prefixe[cle] = decl["dossier"]
            self.prefixe_rattache.add(cle)
            for sub, sdecl in (decl.get("sous") or {}).items():
                self.sous[f"{cle}/{sub}"] = sdecl or {}

        # valeurs declarees de l axe de rangement
        self.valeurs_rangement = set(self.sous)
        if self.valeur_courte:
            self.valeurs_rangement |= set(self.dossier_de_prefixe)

        # --- valeurs de l axe de nature
        self.valeurs_nature = [v["cle"] for v in (self.nature.get("valeurs") or [])]

        # --- axes transverses
        self.axes_transverses = {}
        for t in self.transverses:
            self.axes_transverses[t["champ"]] = {
                "dossier": t["dossier"],
                "multivalue": bool(t.get("multivalue")),
                "hub_par_valeur": t.get("hub_par_valeur", True),
                "valeurs": {v["cle"]: v.get("libelle") for v in (t.get("valeurs") or [])},
            }

    # ------------------------------------------------------------------ #
    @property
    def dossiers_de_ralliement(self) -> set[str]:
        return {(r.get("hub_de_ralliement") or {}).get("dossier")
                for r in self.roles.values() if r.get("hub_de_ralliement")} - {None}

    @property
    def etiquettes_de_groupe(self) -> set[str]:
        """Les libelles qu une zone AUTO groupee peut porter en sous-titre.

        Un `hub_de_ralliement` declare `groupe_par:` — dans DevBrain « premier
        segment du chemin (le domaine, jamais le sous-domaine) ». La REGLE de
        groupement est de la prose que l outil ne lit pas ; l ENSEMBLE des
        etiquettes possibles, lui, se derive : ce sont les dossiers de prefixe de
        l axe de rangement, plus les dossiers des roles ranges par leur role.
        """
        return (set(self.dossier_de_prefixe.values())
                | {r["dossier"] for r in self.roles.values() if r.get("dossier")})

    def role_de_fonction(self, fonction: str) -> dict | None:
        for r in self.roles.values():
            if r.get("fonction") == fonction:
                return r
        return None

    def valeurs_du_champ(self, nom: str) -> set[str] | None:
        """Le vocabulaire ferme d un champ enumere, ou None si le manifeste n en
        declare pas un (une `source:` qui pointe vers un fichier de vocabulaire,
        par exemple : ce n est pas au manifeste de le porter)."""
        d = self.champs.get(nom) or {}
        if d.get("type") not in ("enum", "liste_enum"):
            return None
        if d.get("valeurs"):
            return set(d["valeurs"])
        src = (d.get("source") or "").strip()
        if src == "roles[].id":
            return set(self.roles)
        if src in ("axes.rangement", self.champ_rangement):
            return set(self.valeurs_rangement)
        if src in ("axes.nature", self.champ_nature):
            return set(self.valeurs_nature)
        m = re.match(r"axes\.transverses\[(.+?)\]$", src)
        if m and m.group(1) in self.axes_transverses:
            return set(self.axes_transverses[m.group(1)]["valeurs"])
        return None          # `vocabulaires.tags` — fichier de contenu, hors manifeste

    def sections(self, role: str) -> list[dict]:
        return list((self.roles.get(role) or {}).get("corps") or [])

    def titre_rendu(self, s: dict) -> str:
        return s.get("titre_rendu") or s["titre"]


# ======================================================================== #
#  Divergences
# ======================================================================== #
@dataclass
class Groupe:
    code: str
    sujet: str
    libelle: str
    pages: list[str] = field(default_factory=list)
    detail: list[str] = field(default_factory=list)

    @property
    def cle(self) -> str:
        return f"{self.code}/{self.sujet}"

    @property
    def poids(self) -> int:
        return len(self.pages) or len(self.detail) or 1


class Rapport:
    def __init__(self) -> None:
        self.groupes: dict[str, Groupe] = {}
        self.mesures: list[tuple[str, str, object, object, bool]] = []

    def ajoute(self, code: str, sujet: str, libelle: str,
               page: str | None = None, detail: str | None = None) -> None:
        g = self.groupes.setdefault(f"{code}/{sujet}", Groupe(code, sujet, libelle))
        if page:
            g.pages.append(page)
        if detail:
            g.detail.append(detail)

    def mesure(self, quoi: str, ou: str, declare, reel) -> bool:
        ok = declare == reel
        self.mesures.append((quoi, ou, declare, reel, ok))
        return ok


# ------------------------------------------------------------------ conditions
RE_COND_IN = re.compile(r"^\s*(\w+)\s+in\s*\[(.*?)\]\s*$")
RE_COND_EQ = re.compile(r"^\s*(\w+)\s*(==|!=)\s*(.+?)\s*$")
RE_COND_RENSEIGNE = re.compile(r"^\s*(\w+)\s+(?:renseign[ée]|non vide)\s*$")


def evalue_atome(cond: str, fm: dict) -> bool | None:
    m = RE_COND_IN.match(cond)
    if m:
        champ, valeurs = m.group(1), [v.strip() for v in m.group(2).split(",") if v.strip()]
        return str(fm.get(champ) or "") in valeurs
    m = RE_COND_RENSEIGNE.match(cond)
    if m:
        return non_vide(fm.get(m.group(1)))
    m = RE_COND_EQ.match(cond)
    if m:
        champ, op, val = m.group(1), m.group(2), m.group(3).strip().strip("\"'")
        egal = str(fm.get(champ) or "") == val
        return egal if op == "==" else not egal
    return None


def evalue_condition(cond: str, fm: dict) -> bool | None:
    """Une condition du manifeste, evaluee sur un frontmatter.

    Trois formes d atome — `<champ> in [a, b]`, `<champ> == v` / `!= v`,
    `<champ> renseigne` — et leur conjonction par « et » / « and ». Le manifeste
    ecrit ses conditions en francais court ; cette fonction lit exactement ces
    formes et RIEN de plus.

    None quand une condition sort de ces formes : c est une limite a REMONTER,
    jamais un verdict a deviner. Une condition illisible traitee comme vraie
    ferait exactement la faute que ce lot cherche — expliquer une divergence par
    une supposition.
    """
    if not cond:
        return None
    atomes = re.split(r"\s+(?:et|and)\s+", cond.strip())
    out = True
    for a in atomes:
        v = evalue_atome(a, fm)
        if v is None:
            return None
        out = out and v
    return out


def non_vide(v) -> bool:
    if v is None:
        return False
    if isinstance(v, (list, dict, str)):
        return len(v) > 0
    return True


# ======================================================================== #
#  Les passes
# ======================================================================== #
def passe_population(mo: Modele, pages: list[Page], r: Rapport) -> None:
    """Le compte de pages, par role, contre `roles[].population`."""
    reel = collections.Counter(p.role for p in pages if p.illisible is None)
    for rid, decl in mo.roles.items():
        if "population" not in decl:
            continue
        if not r.mesure("population", rid, decl["population"], reel.get(rid, 0)):
            r.ajoute("P1", rid, f"`roles[{rid}].population` declare "
                               f"{decl['population']}, le vault en porte {reel.get(rid, 0)}")
    total_declare = sum(d.get("population", 0) for d in mo.roles.values())
    r.mesure("population", "total", total_declare, sum(reel.values()))
    for role, n in sorted(reel.items()):
        if role not in mo.roles:
            r.ajoute("F1", str(role), f"`role: {role}` inconnu du manifeste "
                                      f"({n} page(s)) — aucun gabarit ne s applique")


def passe_frontmatter(mo: Modele, pages: list[Page], r: Rapport) -> None:
    """Gabarit de frontmatter : requis, autorises, enumerations, conditionnels."""
    champs_vus: dict[str, set[str]] = collections.defaultdict(set)
    conditionnels_illisibles: set[str] = set()

    for p in pages:
        ou = p.chemin.as_posix()
        if p.illisible:
            r.ajoute("F9", "illisible", "frontmatter illisible", page=f"{ou} — {p.illisible}")
            continue
        decl = mo.roles.get(p.role or "")
        if decl is None:
            continue           # deja signale en F1
        ch = decl.get("champs") or {}
        requis = list(ch.get("requis") or [])
        autorises = set(ch.get("autorises") or [])

        for c in requis:
            if not non_vide(p.fm.get(c)):
                r.ajoute("F2", f"{p.role}.{c}",
                         f"`{c}:` est requis sur `role: {p.role}` et manque (ou est vide)",
                         page=ou)

        for c in p.fm:
            champs_vus[str(c)].add(p.role or "?")
            if c not in autorises:
                r.ajoute("F3", f"{p.role}.{c}",
                         f"`{c}:` present sur `role: {p.role}` alors que "
                         f"`autorises` ne le porte pas", page=ou)
            if c not in mo.champs:
                r.ajoute("F4", str(c),
                         f"`{c}:` n est defini nulle part dans le dictionnaire `champs:`",
                         page=ou)

        # --- enumerations
        for c, v in p.fm.items():
            legales = mo.valeurs_du_champ(str(c))
            if legales is None or not non_vide(v):
                continue
            vals = v if isinstance(v, list) else [v]
            for x in vals:
                if str(x) not in legales:
                    r.ajoute("F5", f"{c}", f"valeur hors du vocabulaire declare de `{c}:`",
                             page=ou, detail=f"{ou} — `{c}: {x}`")

        # --- champs conditionnels
        for cd in ch.get("conditionnels") or []:
            champ, cond = cd.get("champ"), cd.get("si") or ""
            verdict = evalue_condition(cond, p.fm)
            if verdict is None:
                conditionnels_illisibles.add(f"{p.role}.{champ} : `si: {cond}`")
                continue
            present = non_vide(p.fm.get(champ))
            if present and not verdict:
                r.ajoute("F6", f"{p.role}.{champ}",
                         f"`{champ}:` present alors que sa condition (`{cond}`) "
                         f"n est pas remplie", page=ou)
            if verdict and not present:
                # `si:` est une PERMISSION, pas une obligation (§2.7 du contrat,
                # corrige au lot 2) : la condition dit que le champ n existe QUE
                # si elle tient, jamais qu il est exige quand elle tient. Le cas
                # est donc LEGAL, et il se compte — c est la mesure qui a fait
                # corriger la spec.
                r.ajoute("F7", f"{p.role}.{champ}",
                         f"condition de `{champ}:` remplie (`{cond}`) et le champ "
                         f"est absent — legal, `si:` permet et n exige pas ; "
                         f"compte pour memoire", page=ou)

        # --- champs declares vestigiaux, encore portes
        for c in ch.get("deprecies") or []:
            if non_vide(p.fm.get(c)):
                r.ajoute("F8", f"{p.role}.{c}",
                         f"`{c}:` est declare `deprecies` sur `role: {p.role}` "
                         f"et reste porte", page=ou)

        # --- axe de nature interdit sur un role
        if p.role in (mo.nature.get("interdit_sur") or []) and non_vide(p.fm.get(mo.champ_nature)):
            r.ajoute("F10", f"{p.role}.{mo.champ_nature}",
                     f"`{mo.champ_nature}:` est `interdit_sur` `role: {p.role}` "
                     f"et y est porte", page=ou)
        if p.role in (mo.nature.get("porte_par") or []) and not non_vide(p.fm.get(mo.champ_nature)):
            if not mo.nature.get("vide_autorise"):
                r.ajoute("F11", f"{p.role}.{mo.champ_nature}",
                         f"`{mo.champ_nature}:` absent alors que `vide_autorise: false`",
                         page=ou)
            else:
                r.ajoute("F12", f"{p.role}.{mo.champ_nature}",
                         f"`{mo.champ_nature}:` vide — legal (`vide_autorise: true`), "
                         f"compte pour memoire", page=ou)

    for c in sorted(conditionnels_illisibles):
        r.ajoute("F13", c, f"condition d un champ conditionnel que l outil ne sait "
                           f"pas evaluer — {c}")

    # --- un champ du vault que le manifeste ne connait pas (vu globalement)
    for c in sorted(champs_vus):
        if c not in mo.champs:
            r.ajoute("F14", c, f"`{c}:` porte par {sorted(champs_vus[c])} et absent "
                               f"du dictionnaire `champs:`")


# ------------------------------------------------------------------ le corps
RE_ETIQUETTE = re.compile(r"^\s*[-*]\s+(?:\*\*)?([^—–\-\[\]*]{1,40}?)(?:\*\*)?\s*[—–]\s")
RE_BALISE = re.compile(r"<!--\s*AUTO")


def zone(txt: str, balises: list[str]) -> str | None:
    """Le contenu entre deux balises, ou None si la zone n existe pas."""
    if not balises or len(balises) != 2:
        return None
    d, f = balises
    i = txt.find(d)
    j = txt.find(f, i + len(d)) if i >= 0 else -1
    if i < 0 or j < 0:
        return None
    return txt[i + len(d):j]


def passe_corps(mo: Modele, pages: list[Page], r: Rapport) -> None:
    """Gabarit de corps : sections declarees, sections en trop, etiquettes, zones AUTO."""
    par_role: dict[str, list[Page]] = collections.defaultdict(list)
    for p in pages:
        if p.illisible is None and p.role in mo.roles:
            par_role[p.role].append(p)

    for rid, sections in ((k, mo.sections(k)) for k in mo.roles):
        lot = par_role.get(rid, [])
        if not lot:
            continue
        declarees_2 = {mo.titre_rendu(s) for s in sections if s.get("niveau") == 2}
        declarees_3 = {mo.titre_rendu(s) for s in sections if s.get("niveau") == 3}
        # sections de niveau 2 dont le contenu n est PAS controle : leurs
        # sous-titres sont libres par declaration (`genre: libre`, `genre: auto`)
        libres = {mo.titre_rendu(s) for s in sections
                  if s.get("niveau") == 2 and s.get("genre") in ("libre", "auto")}
        # sous-sections d une zone AUTO : declarees, mais en niveau 3 dans la page
        auto = [s for s in sections if s.get("genre") == "auto" and s.get("sections")]
        for s in auto:
            declarees_3 |= {sub["titre"] for sub in s["sections"]}

        for s in sections:
            niveau = s.get("niveau")
            titre = mo.titre_rendu(s)
            if niveau == NIVEAU_0:
                passe_section_niveau_0(mo, rid, s, lot, r)
                continue
            porteuses = [p for p in lot if any(n == niveau and t == titre for n, t, _ in p.titres)]
            reel = len(porteuses)
            if "mesure" in s:
                if not r.mesure(f"corps/{rid}", titre, s["mesure"], reel):
                    r.ajoute("C10", f"{rid}.{titre}",
                             f"`mesure: {s['mesure']}` declaree pour `{'#' * niveau} {titre}` "
                             f"et {reel} page(s) la portent")
            manquantes = [p.chemin.as_posix() for p in lot if p not in porteuses]
            if s.get("existe_si"):
                # Une section qui declare `existe_si` a le DROIT de manquer — quel
                # que soit son `genre`. `conditionnelle` est le genre d une section
                # que sa condition DEFINIT ; `existe_si` sur un autre genre dit
                # seulement qu elle n est pas universelle. Ce qui se rapporte alors
                # est sa COUVERTURE : le cote minoritaire, nomme. Une section a 0 %
                # (la place existe, personne ne l a alimentee) et une section a
                # 100 % ne divergent de rien — les deux bornes sont exactement ce
                # que `existe_si` prevoit.
                minorite = ([p.chemin.as_posix() for p in porteuses]
                            if reel * 2 < len(lot) else manquantes)
                for ou in minorite:
                    r.ajoute("C4", f"{rid}.{titre}",
                             f"section a condition declaree `{'#' * niveau} {titre}` : "
                             f"{reel}/{len(lot)} page(s) de `role: {rid}` la portent "
                             f"— `existe_si: {s['existe_si']}`", page=ou)
            elif manquantes:
                for ou in manquantes:
                    r.ajoute("C1", f"{rid}.{titre}",
                             f"section declaree `{'#' * niveau} {titre}` absente "
                             f"({len(manquantes)}/{len(lot)} page(s) de `role: {rid}`)",
                             page=ou)
            # etiquettes fermees
            if s.get("genre") == "etiquetee":
                passe_etiquettes(rid, s, titre, niveau, lot, r)
            # section adossee a un champ : elle existe si et seulement si le champ
            # est non vide — c est le conditionnel du corps
            if s.get("genre") == "liste_liens" and s.get("champ"):
                passe_section_champ(rid, s, titre, niveau, lot, r)
            # zone AUTO nommee (`genre: auto` de niveau > 0)
            if s.get("genre") == "auto" and s.get("balises"):
                passe_zone_auto(mo, rid, s, lot, r)

        # --- titres presents dans les pages et non declares
        for p in lot:
            for niveau, titre, parent in p.titres:
                if niveau == 2 and titre not in declarees_2:
                    r.ajoute("C2", f"{rid}.{titre}",
                             f"`## {titre}` present sur `role: {rid}` et absent du "
                             f"gabarit declare", page=p.chemin.as_posix())
                elif niveau == 3 and titre not in declarees_3:
                    if parent in libres or parent not in declarees_2:
                        continue      # sous-titre d une section non controlee
                    r.ajoute("C3", f"{rid}.{titre}",
                             f"`### {titre}` present sous `## {parent}` et absent du "
                             f"gabarit declare", page=p.chemin.as_posix())
                elif niveau > 3:
                    r.ajoute("C5", f"{rid}.h{niveau}",
                             f"titre de niveau {niveau} — le manifeste ne declare que "
                             f"les niveaux 0, 2 et 3", page=p.chemin.as_posix())

        # --- zone AUTO declaree par un `genre: auto` de niveau 0
        for s in sections:
            if s.get("genre") == "auto" and s.get("balises") and s.get("niveau") == NIVEAU_0:
                passe_zone_auto(mo, rid, s, lot, r)


def passe_section_niveau_0(mo: Modele, rid: str, s: dict, lot: list[Page], r: Rapport) -> None:
    """Les marqueurs de place : bandeau, embed d une vue, accroche."""
    genre, titre = s.get("genre"), s["titre"]
    if genre == "bandeau":
        bal = mo.bandeau.get("balises") or []
        porteuses = [p for p in lot if zone(p.corps, bal) is not None]
        if "mesure" in s and not r.mesure(f"corps/{rid}", titre, s["mesure"], len(porteuses)):
            r.ajoute("C10", f"{rid}.{titre}",
                     f"`mesure: {s['mesure']}` declaree pour le bandeau et "
                     f"{len(porteuses)} page(s) le portent")
        for p in lot:
            if zone(p.corps, bal) is None:
                r.ajoute("C6", f"{rid}.bandeau",
                         f"zone `{bal[0] if bal else '?'}` absente alors que "
                         f"`bandeau.porte_par` porte `{rid}`", page=p.chemin.as_posix())
    elif genre == "auto":
        # l embed d une vue : `vue_embarquee.embed`
        ve = (mo.roles.get(rid) or {}).get("vue_embarquee") or {}
        ext = ve.get("extension")
        if not ext:
            return
        for p in lot:
            attendu = f"![[{p.nom_fichier}{ext}]]"
            if attendu not in p.corps:
                r.ajoute("C7", f"{rid}.embed",
                         f"l embed declare `{ve.get('embed', '?')}` est absent "
                         f"(attendu : `{attendu}`)", page=p.chemin.as_posix())
            if not (p.absolu.parent / f"{p.nom_fichier}{ext}").exists():
                r.ajoute("C8", f"{rid}.vue",
                         f"le fichier de vue `{p.nom_fichier}{ext}` n existe pas "
                         f"a cote de la page", page=p.chemin.as_posix())
    elif genre == "prose" and s.get("forme"):
        # une accroche : sa forme est declaree, on verifie qu il y a bien du texte
        # avant la premiere section de niveau 2
        for p in lot:
            avant = p.corps.split("\n## ", 1)[0]
            lignes = [l for l in avant.splitlines()
                      if l.strip() and not l.startswith("#") and not RE_BALISE.search(l)]
            if not lignes:
                r.ajoute("C9", f"{rid}.{titre}",
                         f"aucune accroche avant la premiere section "
                         f"(forme declaree : `{s['forme']}`)", page=p.chemin.as_posix())


def passe_etiquettes(rid: str, s: dict, titre: str, niveau: int,
                     lot: list[Page], r: Rapport) -> None:
    """Une section `genre: etiquetee` a un vocabulaire FERME."""
    permises = set(s.get("permises") or [])
    obligatoires = list(s.get("obligatoires") or [])
    if not permises and not obligatoires:
        return
    for p in lot:
        bloc = extrait_section(p.corps, niveau, titre)
        if bloc is None:
            continue
        vues = []
        for ligne in bloc.splitlines():
            m = RE_ETIQUETTE.match(ligne)
            if m:
                vues.append(m.group(1).strip())
        for e in vues:
            if permises and e not in permises:
                r.ajoute("C11", f"{rid}.{titre}",
                         f"etiquette hors du vocabulaire declare de `{titre}`",
                         page=p.chemin.as_posix(), detail=f"{p.chemin.as_posix()} — « {e} »")
        for e in obligatoires:
            if e not in vues:
                r.ajoute("C12", f"{rid}.{titre}.{e}",
                         f"etiquette obligatoire « {e} » absente de `{titre}`",
                         page=p.chemin.as_posix())


def passe_section_champ(rid: str, s: dict, titre: str, niveau: int,
                        lot: list[Page], r: Rapport) -> None:
    """Une section de liste de liens adossee a un champ existe si le champ est non vide."""
    champ = s["champ"]
    for p in lot:
        presente = any(n == niveau and t == titre for n, t, _ in p.titres)
        rempli = non_vide(p.fm.get(champ))
        if rempli and not presente:
            r.ajoute("C13", f"{rid}.{titre}",
                     f"`{champ}:` est renseigne et la section `{titre}` est absente",
                     page=p.chemin.as_posix())
        # Une section qui declare `existe_si` n est pas le miroir strict de son
        # champ : sa condition est ecrite, et elle peut couvrir le cas « le champ
        # est vide ET la section dit en clair qu il n y a rien ».
        if presente and not rempli and not s.get("existe_si"):
            r.ajoute("C14", f"{rid}.{titre}",
                     f"la section `{titre}` existe et `{champ}:` est vide",
                     page=p.chemin.as_posix())


def passe_zone_auto(mo: Modele, rid: str, s: dict, lot: list[Page], r: Rapport) -> None:
    """Les balises d une zone AUTO, et ses sous-sections declarees."""
    bal = s.get("balises") or []
    declarees = {sub["titre"]: sub for sub in (s.get("sections") or [])}
    groupes = mo.etiquettes_de_groupe
    for p in lot:
        z = zone(p.corps, bal)
        if z is None:
            r.ajoute("C15", f"{rid}.{s['titre']}",
                     f"zone AUTO `{bal[0] if bal else '?'}` absente", page=p.chemin.as_posix())
            continue
        inconnues = [m.group(2) for ligne in z.splitlines()
                     if (m := RE_TITRE.match(ligne)) and len(m.group(1)) == 3
                     and m.group(2) not in declarees]
        etiquettes = [t for t in inconnues if t in groupes]
        autres = [t for t in inconnues if t not in groupes]
        if etiquettes:
            # la zone AUTO de cette page est GROUPEE : ses sous-titres sont des
            # etiquettes de groupe, pas des sections du gabarit. Le manifeste
            # declare le groupement (`hub_de_ralliement.groupe_par`) mais son
            # `roles[hub].corps` ne declare qu UNE forme de zone AUTO.
            r.ajoute("C16", f"{rid}.{p.nom_fichier}",
                     f"zone AUTO groupee : {len(etiquettes)} sous-titre(s) qui sont des "
                     f"etiquettes de groupe et non des `sections[]` du gabarit",
                     page=p.chemin.as_posix(),
                     detail=f"{p.chemin.as_posix()} — " + " · ".join(etiquettes))
        for t in autres:
            r.ajoute("C17", f"{rid}.{t}",
                     f"sous-section `### {t}` de la zone AUTO absente des "
                     f"`sections[]` declarees et hors des etiquettes de groupe",
                     page=p.chemin.as_posix(), detail=f"{p.chemin.as_posix()} — « {t} »")
    for titre, sub in declarees.items():
        porteuses = [p for p in lot
                     if (z := zone(p.corps, bal)) is not None
                     and re.search(rf"^### {re.escape(titre)}\s*$", z, re.M)]
        if "mesure" in sub and not r.mesure(f"auto/{rid}", titre, sub["mesure"], len(porteuses)):
            r.ajoute("C10", f"{rid}.AUTO.{titre}",
                     f"`mesure: {sub['mesure']}` declaree pour la sous-section "
                     f"`### {titre}` et {len(porteuses)} page(s) la portent")


def extrait_section(corps: str, niveau: int, titre: str) -> str | None:
    """Le contenu d une section, borne au titre suivant de meme niveau ou plus haut."""
    marque = "#" * niveau
    m = re.search(rf"^{marque} {re.escape(titre)}\s*$", corps, re.M)
    if not m:
        return None
    reste = corps[m.end():]
    borne = re.search(rf"^#{{1,{niveau}}} ", reste, re.M)
    return reste[:borne.start()] if borne else reste


# ------------------------------------------------------------------ le bandeau
def passe_bandeau(mo: Modele, pages: list[Page], r: Rapport) -> None:
    """Les colonnes du bandeau, rendues depuis le frontmatter selon les tables declarees."""
    b = mo.bandeau
    if not b:
        return
    porte_par = set(b.get("porte_par") or [])
    bal = b.get("balises") or []
    vide = b.get("vide") or ""
    colonnes = b.get("colonnes") or []
    titres = [c["titre"] for c in colonnes]

    for p in pages:
        if p.illisible or p.role not in porte_par:
            if p.illisible is None and zone(p.corps, bal) is not None:
                r.ajoute("B1", str(p.role),
                         f"zone de bandeau presente sur `role: {p.role}`, hors de "
                         f"`bandeau.porte_par`", page=p.chemin.as_posix())
            continue
        z = zone(p.corps, bal)
        if z is None:
            continue          # deja signale en C6
        lignes = [l.strip() for l in z.splitlines() if l.strip().startswith("|")]
        if len(lignes) < 3:
            r.ajoute("B2", "forme", f"la zone de bandeau ne porte pas un tableau de "
                                    f"trois lignes", page=p.chemin.as_posix())
            continue
        entete = [c.strip() for c in lignes[0].strip("|").split("|")]
        if entete != titres:
            r.ajoute("B3", "entete",
                     f"en-tete du bandeau {entete} contre {titres} declares",
                     page=p.chemin.as_posix())
        cellules = [c.strip() for c in lignes[2].strip("|").split("|")]
        if len(cellules) != len(colonnes):
            r.ajoute("B4", "colonnes",
                     f"{len(cellules)} cellule(s) contre {len(colonnes)} colonne(s) "
                     f"declarees", page=p.chemin.as_posix())
            continue
        if bool(b.get("porte_le_resume")):
            champ_resume = next((c for c, d in mo.champs.items()
                                 if (d or {}).get("fonction") == "resume_court"), None)
            attendu = f"> {p.fm.get(champ_resume)}" if champ_resume else None
            if attendu and attendu not in z:
                r.ajoute("B5", "resume",
                         f"`porte_le_resume: true` et la zone ne rend pas "
                         f"`{champ_resume}:` en citation", page=p.chemin.as_posix())
        for col, cell in zip(colonnes, cellules):
            attendu = rend_colonne(mo, col, p.fm, vide)
            if attendu is None:
                r.ajoute("B6", col["titre"],
                         f"colonne `{col['titre']}` que l outil ne sait pas rendre "
                         f"depuis le manifeste", page=p.chemin.as_posix())
                continue
            if cell != attendu:
                r.ajoute("B7", col["titre"],
                         f"cellule `{col['titre']}` rendue differemment de ce que le "
                         f"manifeste derive", page=p.chemin.as_posix(),
                         detail=f"{p.chemin.as_posix()} — « {cell} » contre « {attendu} »")


def rend_colonne(mo: Modele, col: dict, fm: dict, vide: str) -> str | None:
    """La cellule qu une colonne de bandeau doit porter, derivee du manifeste seul."""
    src = col.get("source")
    val = fm.get(src)
    table = col.get("table") or {}
    dep = col.get("depend_de") or {}

    if not non_vide(val):
        return vide
    val = str(val)

    if val in table:
        rendu = table[val]
        q = col.get("qualifie_par")
        if q:
            exc = col.get("exception_qualification") or {}
            excl = evalue_condition(exc.get("si", ""), fm) if exc.get("si") else False
            if not excl and non_vide(fm.get(q)):
                rendu = f"{rendu} {fm[q]}"
        return rendu

    # la valeur n est pas dans la table : la colonne depend d autres champs
    if dep and val in (dep.get("familles") or []):
        morceaux = []
        th = dep.get("table_hosted") or {}
        ts = dep.get("table_scaling") or {}
        h = fm.get("hosted")
        if non_vide(h):
            cle = "[" + ", ".join(sorted(str(x) for x in h)) + "]"
            morceaux.append(th.get(cle, cle))
        s = fm.get("scaling")
        if non_vide(s) and str(s) in ts:
            morceaux.append(ts[str(s)])
        if morceaux:
            return " · ".join(morceaux)
        # le repli ne s applique QUE si sa condition est remplie. Une condition
        # illisible ne vaut pas « vrai » : elle interdit de rendre la cellule.
        repli = dep.get("repli") or {}
        if repli.get("source"):
            verdict = evalue_condition(repli.get("si") or "", fm)
            if verdict is None:
                return None
            if verdict:
                return str(fm[repli["source"]])
        return vide
    if not table and not dep:
        return val            # une colonne sans table rend la valeur telle quelle
    return None


# ------------------------------------------------------- l axe et les chemins
def passe_axes(mo: Modele, pages: list[Page], r: Rapport) -> None:
    """Vocabulaires d axe : valeurs declarees sans page, valeurs portees sans declaration."""
    portees: collections.Counter = collections.Counter()
    for p in pages:
        if p.illisible:
            continue
        v = p.fm.get(mo.champ_rangement)
        if non_vide(v):
            portees[str(v)] += 1

    r.mesure("axe de rangement", "valeurs declarees",
             (mo.rangement.get("mesure") or {}).get("valeurs_declarees"),
             len(mo.valeurs_rangement))
    r.mesure("axe de rangement", "valeurs portees",
             (mo.rangement.get("mesure") or {}).get("valeurs_portees"), len(portees))
    # `mesure.prefixes` compte les prefixes de l AXE ; les rattachements sont une
    # exception declaree a cote, et se comptent a part.
    r.mesure("axe de rangement", "prefixes",
             (mo.rangement.get("mesure") or {}).get("prefixes"), len(mo.prefixes_de_l_axe))

    for v in sorted(mo.valeurs_rangement - set(portees)):
        r.ajoute("A1", v, f"`{mo.champ_rangement}: {v}` declaree et portee par AUCUNE page")
    for v in sorted(set(portees) - mo.valeurs_rangement):
        r.ajoute("A2", v, f"`{mo.champ_rangement}: {v}` portee par {portees[v]} page(s) "
                          f"et absente de la declaration de l axe")

    # --- sous-libelles : declares, promus, plafonnes
    declares = {c for c, d in mo.sous.items() if d.get("libelle")}
    r.mesure("axe de rangement", "sous-libelles declares",
             (mo.rangement.get("mesure") or {}).get("sous_libelles_declares"), len(declares))
    promus = promotions(mo, pages, r)
    r.mesure("axe de rangement", "sous-domaines promus",
             (mo.rangement.get("mesure") or {}).get("sous_domaines_promus"), len(promus))
    pesant = poids_du_seuil(mo, pages)
    for c in sorted(declares - set(promus)):
        n = pesant.get(c, 0)
        r.ajoute("A3", c, f"`libelle` declare pour `{c}` ({n} page(s) au seuil, "
                          f"{portees.get(c, 0)} au total) sans que la valeur soit "
                          f"promue en dossier")

    # une valeur d axe homonyme d un `roles[].id` : le vault ecrit alors le meme
    # mot dans deux champs qui ne parlent pas de la meme chose
    for c in sorted(mo.sous):
        if c.split("/")[-1] in mo.roles and portees.get(c):
            r.ajoute("N1", c, f"la sous-valeur `{c}` est homonyme du role "
                              f"`{c.split('/')[-1]}` et {portees[c]} page(s) la portent")

    # --- axe de nature
    nature = collections.Counter()
    for p in pages:
        if p.illisible:
            continue
        v = p.fm.get(mo.champ_nature)
        if non_vide(v):
            nature[str(v)] += 1
    r.mesure("axe de nature", "valeurs",
             (mo.nature.get("mesure") or {}).get("valeurs"), len(mo.valeurs_nature))
    for v in sorted(set(mo.valeurs_nature) - set(nature)):
        r.ajoute("A4", v, f"`{mo.champ_nature}: {v}` declaree et portee par AUCUNE page")

    # --- axes transverses
    for champ, ax in mo.axes_transverses.items():
        vus = collections.Counter()
        for p in pages:
            if p.illisible:
                continue
            v = p.fm.get(champ)
            for x in (v if isinstance(v, list) else [v] if non_vide(v) else []):
                vus[str(x)] += 1
        for v in sorted(set(ax["valeurs"]) - set(vus)):
            r.ajoute("A5", v, f"`{champ}: {v}` declaree et portee par AUCUNE page")
        for v in sorted(set(vus) - set(ax["valeurs"])):
            r.ajoute("A6", v, f"`{champ}: {v}` portee par {vus[v]} page(s) et absente "
                              f"de la declaration de l axe transverse")


def poids_du_seuil(mo: Modele, pages: list[Page]) -> collections.Counter:
    """Le compte de pages qui PESENT sur le seuil, par valeur de l axe."""
    c: collections.Counter = collections.Counter()
    for p in pages:
        if p.illisible or p.role not in mo.roles:
            continue
        if not mo.roles[p.role].get("pese_sur_le_seuil", True):
            continue
        v = p.fm.get(mo.champ_rangement)
        if non_vide(v):
            c[str(v)] += 1
    return c


def promotions(mo: Modele, pages: list[Page], r: Rapport) -> dict[str, str]:
    """Les sous-valeurs promues en dossier, calculees depuis le manifeste SEUL.

    Le seuil, son plafond et les libelles sont lus ; la population est comptee sur
    les pages des roles qui `pese_sur_le_seuil`.
    """
    par_dom: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for cat, n in poids_du_seuil(mo, pages).items():
        dom = mo.dossier_de_prefixe.get(cat.split("/")[0])
        if dom:
            par_dom[dom][cat] += n

    promus: dict[str, str] = {}
    for dom in sorted(par_dom):
        compte = par_dom[dom]
        total = sum(compte.values())
        for cat, n in sorted(compte.items()):
            if n < mo.seuil or "/" not in cat:
                continue
            if mo.plafond and n == total:
                continue
            lib = (mo.sous.get(cat) or {}).get("libelle")
            if not lib:
                r.ajoute("A7", cat, f"`{cat}` atteint {n} page(s) (seuil {mo.seuil}) "
                                    f"sans `libelle` declare — le dossier n est pas "
                                    f"derivable")
                continue
            promus[cat] = lib
    return promus


def passe_chemins(mo: Modele, pages: list[Page], r: Rapport) -> None:
    """Le chemin de chaque page, contre la derivation du manifeste."""
    promus = promotions(mo, pages, r)
    hubs = {p.dossier for p in pages if p.role == (mo.role_de_fonction("hub") or {}).get("id")}
    dossiers_transverses = {ax["dossier"] for ax in mo.axes_transverses.values()}
    libelles_transverses = {lib for ax in mo.axes_transverses.values()
                            for lib in ax["valeurs"].values()}
    dossiers_de_role = {rd["dossier"] for rd in mo.roles.values() if rd.get("dossier")}
    ralliements = {(rd.get("hub_de_ralliement") or {}).get("dossier")
                   for rd in mo.roles.values() if rd.get("hub_de_ralliement")}
    ralliements.discard(None)

    for p in pages:
        if p.illisible or p.role not in mo.roles:
            continue
        decl = mo.roles[p.role]
        ou = p.chemin.as_posix()

        # prefixe de nom
        pref = decl.get("prefixe_nom")
        if pref and not p.nom_fichier.startswith(pref):
            r.ajoute("A8", p.role, f"nom de fichier sans le `prefixe_nom: \"{pref}\"` "
                                   f"declare", page=ou)

        if decl.get("fonction") == "hub":
            # un hub ne se range pas : il EST le rangement. Son chemin est donc le
            # dossier qu il nomme — ou, pour un hub d axe transverse, le dossier de
            # l axe avec le libelle de la valeur pour nom.
            if p.chemin.parent.name == p.nom_fichier:
                continue
            if p.dossier in dossiers_transverses and p.nom_fichier in libelles_transverses:
                continue
            r.ajoute("A9", "hub", f"hub `{p.nom_fichier}` dans `{p.dossier}/` : ni le "
                                  f"dossier qu il nomme, ni un hub d axe transverse "
                                  f"declare", page=ou)
            continue

        if decl.get("range_par") == "role":
            attendu = decl.get("dossier")
            if attendu and p.dossier != attendu:
                r.ajoute("A10", p.role, f"`range_par: role` attend `{attendu}/`", page=ou)
            continue

        cat = str(p.fm.get(mo.champ_rangement) or "")
        pfx = cat.split("/")[0]
        dom = mo.dossier_de_prefixe.get(pfx)
        if dom is None:
            r.ajoute("A11", cat or "(vide)",
                     f"`{mo.champ_rangement}: {cat or '(vide)'}` — prefixe hors des "
                     f"{len(mo.dossier_de_prefixe)} declares, dossier inderivable", page=ou)
            continue
        sub = promus.get(cat)
        attendu = f"{dom}/{sub}" if sub else dom
        if p.dossier != attendu:
            r.ajoute("A12", cat, f"`{mo.champ_rangement}: {cat}` derive `{attendu}/` "
                                 f"et la page vit dans `{p.dossier}/`", page=ou)

    # --- tout dossier de l arbre porte-t-il son hub ?
    hub_id = (mo.role_de_fonction("hub") or {}).get("id")
    dossiers = {p.dossier for p in pages
                if p.illisible is None and p.role in mo.roles and p.role != hub_id}
    for d in sorted(dossiers):
        parts = d.split("/")
        for i in range(1, len(parts) + 1):
            niveau = "/".join(parts[:i])
            if niveau not in hubs:
                r.ajoute("A13", niveau, f"`{niveau}/` ne porte aucune page "
                                        f"`role: {hub_id}` a son nom")
    # Un dossier peut legitimement ne porter AUCUNE page a son niveau : ses pages
    # sont toutes descendues dans des sous-dossiers promus. Un hub y reste donc
    # justifie. Ce qui ne l est pas, c est un hub sur un dossier qui ne porte de
    # page ni a son niveau ni au-dessous.
    ancetres = {d.rsplit("/", 1)[0] for d in dossiers if "/" in d}
    inconnus = (hubs - dossiers - ancetres - dossiers_de_role - ralliements
                - dossiers_transverses)
    for d in sorted(inconnus):
        r.ajoute("A14", d, f"`{d}/` porte un hub et aucune page, ni a son niveau "
                           f"ni au-dessous")

    # --- un hub par valeur d axe transverse, quand `hub_par_valeur` le declare
    noms_de_hub = {(p.dossier, p.nom_fichier) for p in pages if p.role == hub_id}
    for champ, ax in mo.axes_transverses.items():
        if not ax["hub_par_valeur"]:
            continue
        for cle, lib in sorted(ax["valeurs"].items()):
            if (ax["dossier"], lib) not in noms_de_hub:
                r.ajoute("A15", f"{champ}/{cle}",
                         f"`hub_par_valeur: true` et aucun hub `{lib}` dans "
                         f"`{ax['dossier']}/`")

    # --- le lien retour d un hub de ralliement : c est LUI qui fait la grappe
    for rid, decl in mo.roles.items():
        hr = decl.get("hub_de_ralliement") or {}
        if not hr.get("lien_retour"):
            continue
        cible = hr["dossier"].rstrip("/").split("/")[-1]
        for p in pages:
            if p.role != rid or p.illisible:
                continue
            bloc = extrait_section(p.corps, 2, hr["lien_retour"])
            if bloc is None or f"[[{cible}" not in bloc:
                r.ajoute("A16", rid, f"`## {hr['lien_retour']}` ne porte pas le lien "
                                     f"retour `[[{cible}]]` vers le hub de ralliement",
                         page=p.chemin.as_posix())


# ======================================================================== #
#  Sortie
# ======================================================================== #
def imprime(mo: Modele, pages: list[Page], r: Rapport, ns) -> int:
    lisibles = [p for p in pages if p.illisible is None]
    print("=" * 78)
    print("fidelite — le manifeste contre le vault")
    print("=" * 78)
    print(f"manifeste : {ns.manifeste}")
    print(f"vault     : {ns.vault}")
    print(f"perimetre : la racine moins `genere.non_pages` "
          f"({len(mo.non_pages)} dossiers ecartes : {', '.join(sorted(mo.non_pages))})")
    print()

    reel = collections.Counter(p.role for p in lisibles)
    print(f"{len(pages)} page(s) lue(s), {len(lisibles)} au frontmatter lisible")
    print(f"{'role':14s} {'declare':>8s} {'mesure':>8s}")
    for rid, decl in mo.roles.items():
        print(f"  {rid:12s} {decl.get('population', '—'):>8} {reel.get(rid, 0):>8}"
              + ("" if decl.get("population") == reel.get(rid, 0) else "   <- ECART"))
    for role in sorted(set(reel) - set(mo.roles)):
        print(f"  {str(role):12s} {'—':>8} {reel[role]:>8}   <- ROLE INCONNU")
    print(f"  {'TOTAL':12s} {sum(d.get('population', 0) for d in mo.roles.values()):>8} "
          f"{sum(reel.values()):>8}")
    print()

    groupes = sorted(r.groupes.values(), key=lambda g: (g.code, -g.poids, g.sujet))
    if ns.groupe:
        groupes = [g for g in groupes if g.code == ns.groupe or g.cle.startswith(ns.groupe)]

    inexpliquees = [g for g in groupes if g.cle not in VERDICTS]
    par_boite = collections.Counter(VERDICTS[g.cle][0] for g in groupes if g.cle in VERDICTS)

    print("-" * 78)
    print(f"{len(groupes)} groupe(s) de divergences, "
          f"{sum(g.poids for g in groupes)} occurrence(s)")
    print(f"  boite 1 — erreur du manifeste : {par_boite.get('manifeste', 0)} groupe(s)")
    print(f"  boite 2 — fait connu du vault : {par_boite.get('vault', 0)} groupe(s)")
    print(f"  INEXPLIQUEE                   : {len(inexpliquees)} groupe(s)")
    print("-" * 78)
    print()

    code_courant = None
    for g in groupes:
        if g.code != code_courant:
            code_courant = g.code
            print(f"\n### {g.code}")
        boite, motif = VERDICTS.get(g.cle, ("INEXPLIQUEE", ""))
        etiquette = {"manifeste": "[boite 1]", "vault": "[boite 2]"}.get(boite, "[!! INEXPLIQUEE]")
        print(f"  {etiquette} {g.sujet} — {g.libelle}  ({g.poids})")
        if motif:
            print(f"             verdict : {motif}")
        lignes = g.detail or g.pages
        cap = len(lignes) if (ns.pages or ns.groupe) else 6
        for x in lignes[:cap]:
            print(f"             · {x}")
        if len(lignes) > cap:
            print(f"             · … + {len(lignes) - cap} autre(s)")

    ecarts = [m for m in r.mesures if not m[4]]
    print()
    print("-" * 78)
    print(f"mesures confrontees : {len(r.mesures)}, dont {len(ecarts)} en ecart")
    for quoi, ou, decl, reel_, _ in ecarts:
        print(f"  [ECART] {quoi} · {ou} : declare {decl!r}, mesure {reel_!r}")
    print("-" * 78)

    if inexpliquees:
        print(f"\n{len(inexpliquees)} groupe(s) sans verdict — a ranger dans une boite "
              f"ou a remonter :")
        for g in inexpliquees:
            print(f"  {g.cle}")
        return 1
    print("\nOK — toute divergence porte un verdict.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Confronte un brain.yml a son vault.")
    ap.add_argument("--manifeste", type=Path, default=MANIFESTE_DEFAUT)
    ap.add_argument("--vault", type=Path, default=VAULT_DEFAUT)
    ap.add_argument("--pages", action="store_true", help="nomme toutes les pages de chaque groupe")
    ap.add_argument("--groupe", help="n imprime qu un code (C2) ou un groupe (C2/notion.Variantes)")
    ns = ap.parse_args()

    if not ns.manifeste.exists():
        return print(f"manifeste introuvable : {ns.manifeste}") or 1
    if not ns.vault.is_dir():
        return print(f"vault introuvable : {ns.vault}") or 1

    m = yaml.safe_load(ns.manifeste.read_text(encoding="utf-8"))
    mo = Modele(m)
    pages = lire_vault(ns.vault, mo.non_pages)

    r = Rapport()
    passe_population(mo, pages, r)
    passe_frontmatter(mo, pages, r)
    passe_corps(mo, pages, r)
    passe_bandeau(mo, pages, r)
    passe_axes(mo, pages, r)
    passe_chemins(mo, pages, r)
    return imprime(mo, pages, r, ns)


if __name__ == "__main__":
    raise SystemExit(main())
