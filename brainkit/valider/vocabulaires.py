"""vocabulaires.py — les vocabulaires fermes qui vivent dans un FICHIER.

La plupart des vocabulaires d un brain vivent dans le manifeste : les valeurs de
l axe de rangement, celles de l axe de nature, celles de chaque axe transverse.
Le validateur les lit la, et `vocabulaires.taxonomie.genere: true` dit pourquoi —
la place du vocabulaire ferme devient le manifeste, et deux sources ne decrivent
plus la meme chose.

Il en reste qui sont du CONTENU, et que le manifeste declare sans les porter :
un fichier, un mode (`ferme`, `propose`, `libre`) et une regle de lecture. Ce
module en lit UNE forme, et une seule :

    « colonne 1 des tableaux, en backticks »

Toute autre forme de `lecture:` rend le vocabulaire ILLISIBLE, et le dit. Un
vocabulaire illisible traite comme vide ferait passer n importe quelle valeur ;
traite comme absent, il ferait echouer toutes les pages. Aucune des deux n est
acceptable en silence.
"""

from __future__ import annotations

import re
from pathlib import Path

RE_COLONNE_1 = re.compile(r"^\|\s*`([^`]+)`", re.M)

# La seule forme de `lecture:` que ce module sait appliquer. Reconnue par ses
# deux mots-cles, pour ne pas dependre de la ponctuation d une phrase.
def _lecture_connue(lecture: str) -> bool:
    l = (lecture or "").lower()
    return "colonne 1" in l and "backtick" in l


class Vocabulaire:
    def __init__(self, nom: str, decl: dict, racine: Path):
        self.nom = nom
        self.mode = str(decl.get("mode") or "libre")
        self.fichier = decl.get("fichier")
        self.lecture = str(decl.get("lecture") or "")
        self.vide_declare = bool(decl.get("vide"))
        self.genere = bool(decl.get("genere"))
        self.valeurs: set[str] | None = None
        self.illisible: str | None = None

        if self.genere:
            # `genere: true` dit que ce fichier est un DERIVE du manifeste. Le
            # relire comme une source recreerait exactement le defaut que le
            # manifeste existe pour supprimer : deux sources decrivant la meme
            # chose, dont l une prend du retard. Le vocabulaire de ce champ vit
            # dans l axe qui le declare, et le moteur va le chercher la.
            return
        if not self.fichier:
            self.illisible = "aucun `fichier:` déclaré"
            return
        p = racine / self.fichier
        if not p.exists():
            if self.vide_declare:
                self.valeurs = set()
                return
            self.illisible = f"`{self.fichier}` introuvable"
            return
        if not _lecture_connue(self.lecture):
            self.illisible = (f"`lecture: {self.lecture or '(absente)'}` — forme "
                              f"non implémentée par le moteur")
            return
        txt = p.read_text(encoding="utf-8")
        self.valeurs = set(RE_COLONNE_1.findall(txt))

    @property
    def ferme(self) -> bool:
        return self.mode == "ferme" and not self.genere


def charge_tous(decls: dict, racine: Path) -> dict[str, Vocabulaire]:
    return {nom: Vocabulaire(nom, decl or {}, racine)
            for nom, decl in (decls or {}).items()}
