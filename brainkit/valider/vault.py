"""vault.py — la lecture du vault, et RIEN de plus.

Ce module ne porte aucune regle. Il porte les conventions de FORMAT que les
regles consomment : ce qu est un frontmatter, ce qu est une section, ce qu est
un wikilink, ce qu une puce LISTE, ce qu une cellule de tableau contient.

Toutes ces conventions sont celles de Markdown et d Obsidian, donc communes a
tout brain. Aucune n est une valeur du DevBrain : les TITRES des sections, les
NOMS des colonnes, les VOCABULAIRES d etiquettes viennent du manifeste et sont
passes en argument.

Fidelite a l ancien code : les expressions regulieres et la decoupe en sections
sont reprises a l identique de `AI/scripts/check_brain.py`. Ce n est pas de la
paresse, c est le critere d acceptation du lot — un `sections()` qui sauterait
les blocs de code (ce que fait `outils/fidelite.py`) donnerait un autre compte,
et le lot n a pas le droit d ameliorer une regle au passage.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# --------------------------------------------------------------------------- #
# Conventions de format. Reprises mot pour mot de check_brain.py — cf. docstring.
# --------------------------------------------------------------------------- #
RE_TITRE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
LIEN_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
LIEN_PAIRE_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
PUCE_LIEN_RE = re.compile(r"\s*-\s*\[\[([^\]|]+)(?:\|([^\]]+))?\]\]\s*[—-]\s*(.+)")
# Liens d ENTREE d une puce : ce avec quoi la puce COMMENCE, eventuellement
# plusieurs enchaines. C est la definition de « liste » — un lien cite au milieu
# d une phrase n est pas une entree de liste.
PUCE_ENTREE_RE = re.compile(r"^\s*-\s*((?:\[\[[^\]]+\]\]\s*(?:·|,|/)?\s*)+)")
PUCE_ETIQ_RE = re.compile(r"^\s*-\s+(.+?)\s+—\s")
SEPARATEUR_RE = re.compile(r":?-{2,}:?")
# Caracteres interdits dans un nom de fichier (Windows compris) : un champ
# d identite qui en porte un ne PEUT pas etre le nom de son fichier.
FS_ILLEGAL = set('/\\:*?"<>|')

# Dossiers de la racine ecartes du balayage QUEL QUE SOIT le manifeste : un
# worktree git vit sous `.claude/` et est une copie complete du vault, le
# balayer doublerait tout.
HORS_VAULT = {".git", ".claude"}


@dataclass
class Page:
    """Une page lue. `illisible` et `fm` s excluent."""

    chemin: str                       # relatif a la racine, en posix
    fm: dict
    corps: str
    absolu: Path
    illisible: str | None = None
    _sections: dict[str, str] | None = field(default=None, repr=False)

    @property
    def role(self) -> str | None:
        r = self.fm.get("role")
        return None if r is None else str(r)

    @property
    def dossier(self) -> str:
        return self.chemin.rsplit("/", 1)[0] if "/" in self.chemin else ""

    @property
    def stem(self) -> str:
        return Path(self.chemin).stem

    @property
    def sections(self) -> dict[str, str]:
        """{titre : contenu} pour tous les `##` et `###` du corps.

        Un seul niveau de dictionnaire, sans hierarchie : les titres d un
        gabarit sont uniques sur une page, et une section `###` s arrete au
        titre suivant quel que soit son niveau.
        """
        if self._sections is None:
            out: dict[str, str] = {}
            cur: str | None = None
            buf: list[str] = []
            for ligne in self.corps.splitlines():
                m = RE_TITRE.match(ligne)
                if m:
                    if cur is not None:
                        out[cur] = "\n".join(buf)
                    cur, buf = m.group(2), []
                elif cur is not None:
                    buf.append(ligne)
            if cur is not None:
                out[cur] = "\n".join(buf)
            self._sections = out
        return self._sections

    def titres(self) -> list[tuple[int, str]]:
        out: list[tuple[int, str]] = []
        for ligne in self.corps.splitlines():
            m = RE_TITRE.match(ligne)
            if m:
                out.append((len(m.group(1)), m.group(2)))
        return out

    def liens_du_corps(self) -> list[str]:
        return LIEN_RE.findall(self.corps)

    def liens_du_frontmatter(self) -> list[tuple[str, str]]:
        """Wikilinks portes par le FRONTMATTER, avec le champ qui les porte.

        Un renommage ou une suppression laissait un lien mort en frontmatter
        sans que rien ne le dise : le corps seul ne suffit pas.
        """
        out: list[tuple[str, str]] = []
        for cle, val in self.fm.items():
            for item in (val if isinstance(val, list) else [val]):
                if isinstance(item, str):
                    out.extend((str(cle), t) for t in LIEN_RE.findall(item))
        return out


def parse_page(md: Path, racine: Path) -> Page:
    """Une page lue. Les QUATRE motifs d illisibilite sont distingues.

    Le motif est retourne, jamais avale. Une page qui ne parse pas est une
    ERREUR, jamais une absence : avalee, elle sortait du total, echappait a
    toutes les autres regles et ses liens n etaient pas resolus — le vault
    restait vert.
    """
    rel = md.relative_to(racine).as_posix()
    txt = md.read_text(encoding="utf-8")
    if not txt.startswith("---"):
        return Page(rel, {}, "", md,
                    illisible="aucun frontmatter (le fichier ne commence pas par `---`)")
    parts = txt.split("---", 2)
    if len(parts) < 3:
        return Page(rel, {}, "", md,
                    illisible="frontmatter non refermé (pas de second `---`)")
    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        detail = str(e).splitlines()[0].strip()
        return Page(rel, {}, parts[2], md,
                    illisible=f"YAML invalide — {detail}. Cause la plus fréquente : "
                              f"une valeur non quotée contenant « : »")
    if not isinstance(fm, dict):
        return Page(rel, {}, parts[2], md,
                    illisible=f"frontmatter lu comme {type(fm).__name__}, pas comme "
                              f"un dictionnaire de champs")
    return Page(rel, fm, parts[2], md)


def lire_vault(racine: Path, non_pages: set[str]) -> list[Page]:
    """Les pages de l arbre. Le perimetre s enumere PAR LA NEGATIVE.

    Tout dossier de la racine qui n est pas de l outillage porte des pages, et
    la liste de l outillage est celle du manifeste (`genere.non_pages`) — aucune
    table de domaines a tenir a jour.
    """
    pages: list[Page] = []
    for d in sorted(racine.iterdir()):
        if not d.is_dir() or d.name in non_pages or d.name in HORS_VAULT:
            continue
        for md in sorted(d.rglob("*.md")):
            pages.append(parse_page(md, racine))
    return pages


def fichiers_du_vault(racine: Path, extensions: list[str]) -> set[str]:
    """Noms resolvables par un wikilink : le stem ET le nom complet, en minuscules.

    Deux cles par fichier. La seconde sert les liens d embed qui portent une
    extension (`![[X.base]]`), seule syntaxe qui vise un fichier non-`.md` — le
    stem seul faisait declarer ce lien MORT. Porter les deux cles garde le test
    exact : un lien vers `X.base` ne resout que si `X.base` existe, jamais par
    repli sur un `X.md` de meme stem.

    Le balayage porte sur TOUT le vault, gouvernance et gabarits compris : un
    lien vers un document de gouvernance est un lien vivant.
    """
    noms: set[str] = set()
    for ext in extensions:
        for p in racine.rglob(f"*{ext}"):
            try:
                parts = p.relative_to(racine).parts
            except ValueError:
                continue
            if parts and parts[0] in HORS_VAULT:
                continue
            noms.add(p.stem.lower())
            noms.add(p.name.lower())
    return noms


def cible_resolue(cible: str, noms: set[str], racine: Path,
                  extensions: list[str]) -> bool:
    cible = cible.strip()
    if "/" in cible:                      # lien qualifie par chemin
        return any((racine / (cible + e)).exists() for e in extensions)
    return cible.lower() in noms


def cibles_du_champ(fm: dict, champ: str) -> set[str]:
    """Cibles d un champ de liste de liens du frontmatter.

    Le pipe d un wikilink ne porte qu un texte affiche : c est lui qui nomme la
    cible quand il est present, sinon le lien nu. Le dernier segment de chemin
    est retenu, la convention du vault etant le lien NU.
    """
    out: set[str] = set()
    for a in fm.get(champ) or []:
        if not isinstance(a, str):
            continue
        m = re.search(r"\|([^\]]+)\]\]", a) or re.search(r"\[\[([^\]]+)\]\]", a)
        out.add((m.group(1) if m else a).split("/")[-1])
    return out


def cibles_de_la_section(sec: str | None) -> set[str]:
    return {(b or a).split("/")[-1]
            for a, b in LIEN_PAIRE_RE.findall(sec or "")}


def entrees_de_puces(sec: str | None) -> list[str]:
    """Cibles LISTEES par une section de liste de liens.

    Une cible est « listee » quand elle est l ENTREE d une puce, eventuellement
    enchainee a d autres. Sans cette distinction, la regle de citation unique
    punirait la forme recommandee pour une section vide (« Aucune outillee dans
    le brain : l approche concurrente est [[X]] »), ou le lien EXPLIQUE au lieu
    de LISTER.
    """
    out: list[str] = []
    for ligne in (sec or "").splitlines():
        m = PUCE_ENTREE_RE.match(ligne)
        if not m:
            continue
        for a, b in LIEN_PAIRE_RE.findall(m.group(1)):
            out.append((b or a).split("/")[-1].strip())
    return out


def etiquettes(sec: str | None) -> list[str]:
    """Etiquettes des puces `- <Etiquette> — …` d une section.

    Une puce SANS etiquette est rendue telle quelle, prefixee, pour que le
    message montre la ligne fautive au lieu de la taire.
    """
    out: list[str] = []
    for ligne in (sec or "").splitlines():
        m = PUCE_ETIQ_RE.match(ligne)
        if m:
            out.append(m.group(1).strip().replace("**", ""))
        elif ligne.strip().startswith("- "):
            out.append("(sans étiquette) " + ligne.strip()[2:][:60])
    return out


def cellules_de_colonne(sec: str | None, titre_positif: str,
                        titre_negatif: str) -> list[str]:
    """Cellules d une colonne d un tableau a deux colonnes.

    L index de la colonne se LIT dans la ligne d en-tete, il n est pas suppose.
    A defaut d en-tete reconnaissable, la colonne negative est la seconde — le
    genre `decision` du manifeste declare exactement deux colonnes, l une
    positive et l autre negative.
    """
    if sec is None:
        return []
    idx = 1
    out: list[str] = []
    for ligne in sec.splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("|"):
            continue
        cols = [c.strip() for c in ligne.strip("|").split("|")]
        if len(cols) < 2:
            continue
        if SEPARATEUR_RE.fullmatch(cols[0]):
            continue
        if cols[0].lower().startswith(titre_positif.lower()):
            for i, c in enumerate(cols):          # l en-tete donne l index
                if c.lower().startswith(titre_negatif.lower()):
                    idx = i
            continue
        if idx < len(cols) and cols[idx]:
            out.append(cols[idx])
    return out


def normalise_resume(s: str) -> str:
    """Normalisation de comparaison d un resume : gras et espaces seulement."""
    return re.sub(r"\s+", " ", re.sub(r"\*\*", "", s or "")).strip().rstrip(".")


def non_vide(v) -> bool:
    if v is None:
        return False
    if isinstance(v, (list, dict, str)):
        return len(v) > 0
    return True


def valeurs(v) -> list[str]:
    """Un champ lu comme une LISTE de valeurs, qu il porte un scalaire ou une liste."""
    if v is None:
        return []
    if isinstance(v, list):
        return [str(x) for x in v if x is not None and str(x) != ""]
    return [str(v)] if str(v) != "" else []
