"""contexte.py — ce que les regles partagent, calcule UNE fois.

Chaque index de ce module existe parce qu une regle le consomme, et parce que le
recalculer par page serait quadratique : la regle de redirection confronte chaque
cellule de tableau aux noms et alias de toutes les unites du vault.

Aucun index n est nomme d apres un mot du sujet. `champ_identite`,
`champ_resume`, `champ_alias` sont RESOLUS par la `fonction:` que le manifeste
declare dans son dictionnaire de champs — jamais par le nom du champ. C est la
discipline qui rend l homonymie « domaine » inoffensive : le moteur ne reconnait
jamais un champ a son nom.
"""

from __future__ import annotations

import collections
from dataclasses import dataclass, field
from pathlib import Path

from . import chemins, vault
from .manifeste import Modele
from .vault import Page
from .vocabulaires import Vocabulaire


@dataclass
class Contexte:
    mo: Modele
    racine: Path
    pages: list[Page]                       # toutes, illisibles comprises
    vocabulaires: dict[str, Vocabulaire] = field(default_factory=dict)

    # --- calcules ------------------------------------------------------- #
    lisibles: list[Page] = field(default_factory=list)
    champ_identite: str | None = None
    champ_resume: str | None = None
    champ_alias: str | None = None
    par_identite: dict[str, dict] = field(default_factory=dict)
    resumes: dict[str, str] = field(default_factory=dict)
    extensions: list[str] = field(default_factory=list)
    noms_resolvables: set[str] = field(default_factory=set)
    promus: dict[str, str] = field(default_factory=dict)
    promus_sans_libelle: list[str] = field(default_factory=list)
    hubs: dict[str, Page] = field(default_factory=dict)      # dossier -> la page hub
    cibles_des_hubs: dict[str, set[str]] = field(default_factory=dict)
    index_des_unites: dict[str, str] = field(default_factory=dict)
    pages_par_dossier_et_role: collections.Counter = field(
        default_factory=collections.Counter)
    stems_a_comprendre: set[str] = field(default_factory=set)
    cibles_citees: set[str] = field(default_factory=set)

    # ------------------------------------------------------------------ #
    def prepare(self) -> None:
        mo = self.mo
        self.lisibles = [p for p in self.pages if p.illisible is None]

        self.champ_identite = mo.champ_de_fonction("identite")
        self.champ_resume = mo.champ_de_fonction("resume_court")
        self.champ_alias = mo.champ_de_fonction("alias")

        # L extension d une vue embarquee est resolvable par un wikilink : c est
        # la seule syntaxe qui vise un fichier non-`.md`.
        self.extensions = [".md"]
        ext = mo.extension_de_vue()
        if ext and ext not in self.extensions:
            self.extensions.append(ext)
        self.noms_resolvables = vault.fichiers_du_vault(self.racine, self.extensions)

        if self.champ_identite:
            for p in self.lisibles:
                nom = p.fm.get(self.champ_identite)
                if nom is not None:
                    self.par_identite[str(nom)] = p.fm
        if self.champ_identite and self.champ_resume:
            for p in self.lisibles:
                nom = p.fm.get(self.champ_identite)
                if nom is not None:
                    self.resumes[str(nom)] = str(p.fm.get(self.champ_resume) or "")

        self.promus, self.promus_sans_libelle = chemins.promotions(self.lisibles, mo)

        rid_hub = mo.role_hub
        for p in self.lisibles:
            if p.role == rid_hub:
                self.hubs[p.dossier] = p
                self.cibles_des_hubs[p.chemin] = {
                    (b or a).split("/")[-1].strip()
                    for a, b in vault.LIEN_PAIRE_RE.findall(p.corps)}

        # {nom ou alias : nom canonique} des unites — la regle de redirection
        # sourcee confronte chaque cellule negative a cet index. Un alias de
        # moins de trois caracteres est ECARTE : il produirait des
        # correspondances de hasard dans de la prose.
        rid_unite = mo.role_unite
        if rid_unite and self.champ_identite:
            for p in self.lisibles:
                if p.role != rid_unite:
                    continue
                nom = p.fm.get(self.champ_identite)
                if not nom:
                    continue
                self.index_des_unites[str(nom).lower()] = str(nom)
                if self.champ_alias:
                    for a in p.fm.get(self.champ_alias) or []:
                        if len(str(a)) >= 3:
                            self.index_des_unites.setdefault(str(a).lower(), str(nom))

        self.pages_par_dossier_et_role = collections.Counter(
            (p.dossier, p.role) for p in self.lisibles)

        # Les pages « a comprendre » : celles dont la fonction est d expliquer.
        a_comprendre = set(mo.roles_de_fonction("notion")) | set(
            mo.roles_de_fonction("hub"))
        self.stems_a_comprendre = {p.stem.lower() for p in self.lisibles
                                   if p.role in a_comprendre}

        # Tout ce que le corps d une page cite, en minuscules. Un lien d embed
        # portant l extension d une vue compte AUSSI sans son extension.
        for p in self.lisibles:
            for t in p.liens_du_corps():
                cible = t.strip().split("/")[-1].lower()
                self.cibles_citees.add(cible)
                if ext and cible.endswith(ext):
                    self.cibles_citees.add(cible[: -len(ext)])

    # ------------------------------------------------------------------ #
    def pages_du_role(self, rid: str) -> list[Page]:
        return [p for p in self.lisibles if p.role == rid]

    def resume(self, nom: str) -> str:
        return self.resumes.get(nom, "")
