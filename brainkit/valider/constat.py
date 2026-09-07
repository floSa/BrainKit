"""constat.py — ce qu une regle rapporte, et l inventaire qui rend le silence lisible.

Trois idees, et une seule est evidente.

1. **Un constat porte sa regle, pas seulement son message.** Le critere du lot
   est « meme verdict, REGLE PAR REGLE » : un compte global ne le prouverait
   pas. Chaque constat porte donc l `id` de la regle du manifeste, le code de
   l ancien validateur (pour la correspondance), la severite LUE et la page.

2. **La severite se lit, elle ne se decide pas.** Trois valeurs :
   `dure` (le verdict echoue), `avertissement` (il signale), `a_mesurer` (il
   compte, sans juger — c est la valeur par defaut de toute instance neuve, et
   la seule que l entretien sait ecrire).

3. **Une regle qui n a rien trouve n est pas une regle qui n a pas tourne.**
   L inventaire imprime, nommement, les regles qui ont tourne sans rien trouver,
   celles que le manifeste desactive, celles qu il ne declare pas et celles qui
   sont deleguees ailleurs. Sans cette liste, une regle verte et une regle morte
   se ressemblent — c est exactement ce que l absence de `completude_du_hub` a
   coute au DevBrain : « une regle absente ne ressemble pas a une regle souple,
   elle ressemble a une regle satisfaite. »

4. **Zero violation ne veut rien dire sans son denominateur.** AJOUTE AU LOT 8.
   Chaque regle declare, en plus de ses constats, la POPULATION qu elle a
   REELLEMENT mesuree : le nombre de pages sur lesquelles elle avait quelque
   chose a controler. Pas le nombre de pages du vault, pas le nombre de pages de
   son role — le nombre de pages ou une violation etait POSSIBLE.

   La nuance n est pas cosmetique, c est tout le lot 8 : une regle a zero sur
   trois pages qui portent le champ n a rien prouve, et elle est indiscernable
   d une regle a zero sur trois cents si le seul chiffre imprime est zero. Le
   denominateur est donc DECLARE PAR LA REGLE ELLE-MEME, au moment ou elle
   tourne — jamais recalcule ailleurs, sans quoi la mesure et le controle
   diveregeraient en silence, ce qui est exactement le constat E4.

   Une regle qui ne compte pas des pages (les cellules d une colonne, les noms
   de fichier, les champs d un manifeste) declare EN PLUS son objet et son
   compte : c est ce qui permet de dire « 1 violation sur 1 388 cellules » sans
   pretendre que 1 388 est un nombre de pages.
"""

from __future__ import annotations

from dataclasses import dataclass, field

DURE = "dure"
AVERTISSEMENT = "avertissement"
A_MESURER = "a_mesurer"

# Les quatre raisons pour lesquelles une regle n a rien rapporte. Elles ne se
# confondent pas.
TOURNEE = "tournée, aucun constat"
INACTIVE = "désactivée par le manifeste (`active: false`)"
NON_DECLAREE = "non déclarée par ce manifeste"
DELEGUEE = "déléguée — portée par un autre outil que le validateur"
NON_APPLICABLE = "sans objet sur ce vault"


@dataclass(frozen=True)
class Constat:
    regle: str                 # l `id` de la regle du manifeste
    severite: str
    message: str
    page: str = ""             # chemin relatif, vide si le constat est global
    cle: str = ""              # la section, pour une severite par section
    codes: tuple[str, ...] = ()   # les codes de l ancien validateur

    def rendu(self) -> str:
        ou = f"{self.page} : " if self.page else ""
        return f"{ou}{self.message}"


@dataclass(frozen=True)
class Population:
    """Ce qu une regle a REELLEMENT mesure — son denominateur.

    `pages` est le nombre de pages sur lesquelles une violation etait possible.
    `objets` / `objet` portent l unite reelle quand la regle ne compte pas des
    pages : des cellules, des couples, des noms de fichier, des champs du
    manifeste. `sur_le_manifeste` marque les regles verifiables SANS lire une
    page — leur denominateur n est pas un volume de corpus, et le plancher de
    pages ne s y applique donc pas.
    """

    pages: int
    objets: int | None = None
    objet: str = ""
    sur_le_manifeste: bool = False


@dataclass
class Rapport:
    constats: list[Constat] = field(default_factory=list)
    etats: dict[str, str] = field(default_factory=dict)   # regle -> raison du silence
    notes: list[str] = field(default_factory=list)
    populations: dict[tuple[str, str], Population] = field(default_factory=dict)

    # ------------------------------------------------------------------ #
    def ajoute(self, regle: str, severite: str, message: str,
               page: str = "", cle: str = "", codes: tuple[str, ...] = ()) -> None:
        self.constats.append(Constat(regle, severite, message, page, cle, codes))

    def population(self, regle: str, pages: int, cle: str = "",
                   objets: int | None = None, objet: str = "",
                   sur_le_manifeste: bool = False) -> None:
        """Declare le denominateur d une regle. Appele PAR la regle, une fois."""
        self.populations[(regle, cle)] = Population(pages, objets, objet,
                                                    sur_le_manifeste)

    def population_de(self, regle: str, cle: str = "") -> Population | None:
        return self.populations.get((regle, cle)) or self.populations.get((regle, ""))

    def etat(self, regle: str, raison: str) -> None:
        """Declare pourquoi une regle n a rien rapporte."""
        self.etats[regle] = raison

    def note(self, texte: str) -> None:
        self.notes.append(texte)

    # ------------------------------------------------------------------ #
    def par_severite(self, severite: str) -> list[Constat]:
        return [c for c in self.constats if c.severite == severite]

    def regles_touchees(self) -> list[str]:
        vus: list[str] = []
        for c in self.constats:
            if c.regle not in vus:
                vus.append(c.regle)
        return vus

    def compte(self, regle: str, severite: str | None = None) -> int:
        return sum(1 for c in self.constats
                   if c.regle == regle and (severite is None or c.severite == severite))

    def compte_par_regle(self) -> dict[tuple[str, str, str], int]:
        """{(regle, cle, severite) : nombre}. La cle porte la section, s il y en a une."""
        out: dict[tuple[str, str, str], int] = {}
        for c in self.constats:
            k = (c.regle, c.cle, c.severite)
            out[k] = out.get(k, 0) + 1
        return out
