"""corpus.py — ce que les quatre generateurs lisent, calcule UNE fois.

Le DevBrain balayait son vault QUATRE fois : `build_index.py`, `build_mocs.py`
(qui relisait en plus le JSON produit par le premier), `build_links.py` et
`build_bandeau.py` avaient chacun leur `NON_PAGES`, leur `parse_frontmatter()`
et leur boucle `rglob`. Quatre copies de la meme chose, dont trois pouvaient
prendre du retard sur la quatrieme — et c est arrive : la boucle transverse de
`build_mocs.py` est restee sur le perimetre de la v2 pendant tout un lot, et
« ne PAS le faire erode ces 5 pages a chaque lot de domaine, en silence » est
ecrit dans son propre commentaire.

Ici, un seul balayage, un seul perimetre — celui du manifeste
(`genere.non_pages`) — et un seul jeu d entrees d index que les quatre
consomment. Le chainage par fichier disparait : plus besoin de lancer l index
avant les hubs.

Aucun champ n est reconnu par son NOM. `champ_identite`, `champ_resume`,
`champ_alias`, `champ_tags`, `champ_role` sont resolus par leur `fonction:` ou
leur `source:`, exactement comme dans le validateur — c est ce qui rend
inoffensive l homonymie « domaine » du DevBrain.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ..valider import vault
from ..valider.manifeste import Modele
from ..valider.vault import Page

# Les colonnes CALCULEES que `genere.index.plus` peut nommer. Vocabulaire ferme
# par le kit : une colonne calculee est du code, pas une donnee.
CALCULEES = ("path",)


@dataclass
class Corpus:
    mo: Modele
    racine: Path
    pages: list[Page] = field(default_factory=list)
    lisibles: list[Page] = field(default_factory=list)
    illisibles: list[Page] = field(default_factory=list)
    entrees: list[dict] = field(default_factory=list)
    scannes: list[str] = field(default_factory=list)
    par_chemin: dict[str, Page] = field(default_factory=dict)

    champ_identite: str = ""
    champ_resume: str = ""
    champ_alias: str = ""
    champ_role: str = "role"
    champ_tags: str = ""
    champs_transverses: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------ #
    def prepare(self) -> None:
        mo = self.mo
        self.champ_identite = mo.champ_de_fonction("identite") or ""
        self.champ_resume = mo.champ_de_fonction("resume_court") or ""
        self.champ_alias = mo.champ_de_fonction("alias") or ""
        self.champ_role = _champ_par_source(mo, "roles[].id") or "role"
        self.champ_tags = _premier_champ_de_vocabulaire(mo)
        self.champs_transverses = list(mo.champs_transverses)

        # Le perimetre s enumere PAR LA NEGATIVE : tout dossier de la racine qui
        # n est pas de l outillage porte des pages. `scannes` est la liste TELLE
        # QUELLE, sans le filtre technique des worktrees — c est elle que l index
        # publie, et elle doit dire ce qui a ete parcouru.
        self.scannes = sorted(d.name for d in self.racine.iterdir()
                              if d.is_dir() and d.name not in mo.non_pages)

        self.pages = vault.lire_vault(self.racine, mo.non_pages)
        self.pages.sort(key=lambda p: p.chemin)
        self.lisibles = [p for p in self.pages if p.illisible is None]
        self.illisibles = [p for p in self.pages if p.illisible is not None]
        self.par_chemin = {p.chemin: p for p in self.lisibles}
        self.entrees = [self._entree(p) for p in self.lisibles]

    # ------------------------------------------------------------------ #
    def _entree(self, p: Page) -> dict:
        """Une page, lue comme une ligne : son chemin, puis TOUT son frontmatter.

        L entree n est PAS la ligne de l index. Elle porte tout ce que la page
        declare, et c est le generateur d index qui PROJETTE les colonnes que le
        manifeste publie. La difference n est pas cosmetique : `genere.index`
        decide de ce qui sort dans le catalogue, pas de ce que les generateurs
        ont le droit de lire. Un manifeste qui ne declare aucun index — celui
        d un jeu d epreuve de validation, par exemple — laisserait sinon les
        hubs sans un nom a citer.

        `path` est la seule cle CALCULEE, et elle est toujours la : c est
        l identite d une entree a l interieur du kit.
        """
        e: dict = {"path": p.chemin}
        e.update(p.fm)
        # Le champ d identite retombe sur le nom de fichier : le vault a des
        # roles qui n en portent pas (une prescription n a ni identite ni valeur
        # d axe), et une entree sans nom ne se cite pas.
        if self.champ_identite and not e.get(self.champ_identite):
            e[self.champ_identite] = p.stem
        return e

    def colonnes_publiees(self, e: dict) -> dict:
        """La ligne d index PUBLIEE : les colonnes declarees, dans leur ordre.

        Un champ que la page ne porte pas sort a `null` et n est PAS omis : un
        consommateur machine qui filtre sur le catalogue doit voir la case vide,
        sans quoi il ne distingue pas « pas renseigne » de « pas indexe ».
        """
        decl = (self.mo.m.get("genere") or {}).get("index") or {}
        out: dict = {}
        for nom in decl.get("plus") or []:
            if nom in CALCULEES:
                out[nom] = e.get(nom)
        for nom in decl.get("champs") or []:
            out[nom] = e.get(nom)
        return out

    # ------------------------------------------------------------------ #
    def nom(self, e: dict) -> str:
        return str(e.get(self.champ_identite) or Path(e["path"]).stem)

    def resume(self, e: dict) -> str:
        return str(e.get(self.champ_resume) or "") if self.champ_resume else ""

    def stem(self, e: dict) -> str:
        return Path(e["path"]).stem

    def lien(self, e: dict) -> str:
        """Le wikilink NU vers une entree — jamais qualifie par un chemin.

        Un lien qualifie porte le chemin, donc casse au premier `git mv` : le
        lot 3 du DevBrain a deplace 682 fichiers sans toucher un lien. Le pipe
        ne sert qu a changer le texte affiche, quand le nom de la page differe
        de son nom de fichier.
        """
        stem, nom = self.stem(e), self.nom(e)
        return f"[[{stem}]]" if stem == nom else f"[[{stem}|{nom}]]"

    def valeurs_transverses(self, e: dict) -> list[tuple[str, list[str]]]:
        return [(c, [str(v) for v in (e.get(c) or [])])
                for c in self.champs_transverses]

    def descripteur(self, e: dict, avec_alias: bool = False,
                    vide: str = "") -> str:
        """Ce qui suit le lien d une puce : le resume, sinon ce qui reste.

        Deux formes, et la difference est mesuree sur le DevBrain : le hub d un
        dossier retombe sur les seuls axes transverses et n affiche RIEN quand il
        n y en a pas ; l index humain retombe en plus sur les alias, et affiche
        un tiret quand il ne reste rien. Les deux sont conservees telles quelles.
        """
        r = self.resume(e)
        if r:
            return r
        bouts: list[str] = []
        for champ, vals in self.valeurs_transverses(e):
            if vals:
                bouts.append(f"{champ} : " + ", ".join(vals))
        if avec_alias and self.champ_alias:
            al = [str(a) for a in (e.get(self.champ_alias) or [])]
            if al:
                bouts.append(f"{self.champ_alias} : " + ", ".join(al))
        return " · ".join(bouts) if bouts else vide


# --------------------------------------------------------------------------- #
def _champ_par_source(mo: Modele, source: str) -> str | None:
    for nom, d in mo.champs.items():
        if str(d.get("source") or "").strip() == source:
            return nom
    return None


def _premier_champ_de_vocabulaire(mo: Modele) -> str:
    """Le champ de mots-cles transverses : celui dont le vocabulaire vit dans un FICHIER.

    C est la seule sorte de champ enumere dont la source n est ni un axe ni une
    liste en dur — donc le seul candidat pour l index de mots-cles. Le kit en
    lit UN : un brain qui en aurait deux verrait le second absent de la carte des
    liens, et c est une remontee, pas un comportement.
    """
    for nom, d in mo.champs.items():
        if str(d.get("source") or "").startswith("vocabulaires."):
            return nom
    return ""


def charge_corpus(mo: Modele, racine: Path) -> Corpus:
    c = Corpus(mo=mo, racine=racine.resolve())
    c.prepare()
    return c
