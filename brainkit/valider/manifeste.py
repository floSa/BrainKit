"""manifeste.py — le modele que le vault doit satisfaire, lu dans `brain.yml`.

AUCUNE valeur d instance n est ecrite ici. Ni prefixe, ni categorie, ni famille,
ni role, ni titre de section, ni seuil de promotion, ni severite. Les seules
constantes de ce module sont des conventions de FORMAT du manifeste lui-meme
(le nom du champ `fonction:`, les six fonctions fermees par le kit, les dix
identifiants de regle fermes par le kit).

# L homonymie « domaine » — trois choses, trois noms distincts

C est la remontee 7 du lot 1 et la remontee 5 du lot 2, tranchees ici. Dans le
le vault d'origine, trois choses s ecrivent « domaine », et un validateur qui les
confondrait rangerait une prescription par un champ libre :

| Ce que c est                              | Ou ca vit                        | Nom dans ce moteur      |
|---|---|---|
| le DOSSIER de l arbre                     | `axes.rangement.prefixes[].dossier` | `dossier_de_prefixe`  |
| le CHAMP de l axe de rangement            | `axes.rangement.champ`           | `champ_rangement`       |
| le MOT que la prose emploie               | `libelles.axe_rangement.{s,p}`   | `libelle_rangement`     |
| le CHAMP d une prescription, chaine libre | `champs.domaine`                 | rien — un champ ordinaire |
| le CHAMP d un axe transverse              | `champs.domaines`                | `champs_transverses`    |

La regle qui rend la confusion impossible n est pas un nommage, c est une
DISCIPLINE DE RESOLUTION : **le moteur ne reconnait jamais un champ par son
nom.** Il le reconnait par sa `source:` (quel axe il lit), par sa `fonction:`
(identite, alias, resume court) ou par son `reciproque:`. `champs.domaine` ne
declare aucune des trois : c est donc, pour le moteur, une `ligne` comme une
autre — et c est exactement ce qu elle est.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

# Les six fonctions de role, fermees par le kit (contrat §1).
FONCTIONS = ("unite", "notion", "hub", "vue", "prescription", "transverse")

# Les dix regles de §10, fermees par le kit (contrat §2.12). Le manifeste les
# BRANCHE, il ne les decrit pas.
LES_DIX = ("reciprocite", "chemin_categorie", "completude_du_hub",
           "voisinage_declare", "redirection_sourcee", "reinjection_du_resume",
           "etiquettes_fermees", "citation_unique", "bandeau_a_jour",
           "anti_repetition")

# Genres de section qui portent une liste de liens, une zone a balises, un
# tableau de decision, un vocabulaire ferme. Conventions du manifeste.
GENRE_LISTE = "liste_liens"
GENRE_DECISION = "decision"
GENRE_ETIQUETEE = "etiquetee"
GENRE_PROSE = "prose"
GENRE_BANDEAU = "bandeau"
GENRE_AUTO = "auto"

RE_SOURCE_TRANSVERSE = re.compile(r"axes\.transverses\[(.+?)\]$")


class Modele:
    """Le manifeste, mis en forme pour etre confronte a un vault."""

    def __init__(self, m: dict, chemin: Path | None = None):
        self.m = m
        self.chemin = chemin
        self.version = m.get("manifeste")
        self.brain = m.get("brain") or {}
        self.libelles = m.get("libelles") or {}
        self.roles: dict[str, dict] = {r["id"]: r for r in (m.get("roles") or [])}
        self.champs: dict[str, dict] = m.get("champs") or {}

        axes = m.get("axes") or {}
        self.rangement = axes.get("rangement") or {}
        self.nature = axes.get("nature") or {}
        self.transverses = axes.get("transverses") or []

        self.bandeau = m.get("bandeau") or {}
        self.seuils = m.get("seuils") or {}
        self.vocabulaires = m.get("vocabulaires") or {}
        genere = m.get("genere") or {}
        self.non_pages: set[str] = set(genere.get("non_pages") or [])

        # ---- l axe qui RANGE ---------------------------------------------
        self.champ_rangement: str = str(self.rangement.get("champ") or "")
        self.exclusif: bool = bool(self.rangement.get("exclusif"))
        self.regle_de_majorite: bool = bool(self.rangement.get("regle_de_majorite"))
        self.prefixe_transversal: str | None = self.rangement.get("prefixe_transversal")
        self.seuil: int = int(self.rangement.get("seuil_promotion") or 0)
        self.plafond: bool = bool(self.rangement.get("plafond_promotion"))
        self.valeur_courte: bool = bool(self.rangement.get("valeur_courte_autorisee"))

        self.dossier_de_prefixe: dict[str, str] = {}
        self.prefixes_rattaches: set[str] = set()
        self.sous_valeurs: dict[str, dict] = {}     # "pfx/sub" -> declaration
        for p in self.rangement.get("prefixes") or []:
            self.dossier_de_prefixe[p["cle"]] = p["dossier"]
            for sub, decl in (p.get("sous") or {}).items():
                self.sous_valeurs[f"{p['cle']}/{sub}"] = decl or {}
        for cle, decl in (self.rangement.get("rattachements") or {}).items():
            self.dossier_de_prefixe[cle] = decl["dossier"]
            self.prefixes_rattaches.add(cle)
            for sub, sdecl in (decl.get("sous") or {}).items():
                self.sous_valeurs[f"{cle}/{sub}"] = sdecl or {}

        self.valeurs_rangement: set[str] = set(self.sous_valeurs)
        if self.valeur_courte:
            self.valeurs_rangement |= set(self.dossier_de_prefixe)

        # ---- l axe qui QUALIFIE ------------------------------------------
        self.champ_nature: str = str(self.nature.get("champ") or "")
        self.valeurs_nature: list[str] = [v["cle"] for v in
                                          (self.nature.get("valeurs") or [])]
        self.nature_portee_par: list[str] = list(self.nature.get("porte_par") or [])
        self.nature_interdite_sur: list[str] = list(self.nature.get("interdit_sur") or [])
        self.nature_vide_autorise: bool = bool(self.nature.get("vide_autorise"))

        # ---- les axes TRANSVERSES ----------------------------------------
        self.champs_transverses: dict[str, dict] = {}
        for t in self.transverses:
            self.champs_transverses[t["champ"]] = {
                "dossier": t["dossier"],
                "multivalue": bool(t.get("multivalue")),
                "hub_par_valeur": t.get("hub_par_valeur", True),
                "valeurs": {v["cle"]: v.get("libelle") for v in (t.get("valeurs") or [])},
            }

        # ---- les regles ---------------------------------------------------
        self.regles: dict[str, dict] = {r["id"]: r for r in (m.get("regles") or [])}
        self.socle: dict[str, dict] = {r["id"]: r for r in
                                       (m.get("regles_de_socle") or [])}

    # ------------------------------------------------------------------ #
    #  Le vocabulaire visible
    # ------------------------------------------------------------------ #
    @property
    def libelle_rangement(self) -> dict:
        """Le MOT que la prose emploie pour l axe de rangement.

        Distinct du champ (`champ_rangement`) et des dossiers
        (`dossier_de_prefixe`). Il ne sert QUE les messages.
        """
        return self.libelles.get("axe_rangement") or {"s": "", "p": ""}

    def mot(self, cle: str, nombre: str = "s") -> str:
        return (self.libelles.get(cle) or {}).get(nombre) or cle

    # ------------------------------------------------------------------ #
    #  Les roles, par fonction
    # ------------------------------------------------------------------ #
    def roles_de_fonction(self, fonction: str) -> list[str]:
        return [rid for rid, r in self.roles.items() if r.get("fonction") == fonction]

    def role_de_fonction(self, fonction: str) -> str | None:
        lot = self.roles_de_fonction(fonction)
        return lot[0] if lot else None

    @property
    def role_unite(self) -> str | None:
        return self.role_de_fonction("unite")

    @property
    def role_hub(self) -> str | None:
        return self.role_de_fonction("hub")

    def roles_ranges_par_axe(self) -> list[str]:
        return [rid for rid, r in self.roles.items() if r.get("range_par") == "axe"]

    def roles_ranges_par_role(self) -> list[str]:
        return [rid for rid, r in self.roles.items() if r.get("range_par") == "role"]

    def porte_l_axe_de_rangement(self, rid: str) -> bool:
        """Un role qui ne PORTE pas la categorie n a pas de chemin a deriver.

        `porte_categorie: false` sur un hub : il ne se range pas, il EST le
        rangement — son dossier est son chemin.
        """
        r = self.roles.get(rid) or {}
        return r.get("range_par") == "axe" and r.get("porte_categorie", True)

    def pese_sur_le_seuil(self, rid: str) -> bool:
        return bool((self.roles.get(rid) or {}).get("pese_sur_le_seuil", True))

    def apparait_dans_le_hub(self, rid: str) -> bool:
        return bool((self.roles.get(rid) or {}).get("apparait_dans_le_hub", True))

    def dossier_de_role(self, rid: str) -> str | None:
        return (self.roles.get(rid) or {}).get("dossier")

    def dossiers_de_ralliement(self) -> set[str]:
        return {(r.get("hub_de_ralliement") or {}).get("dossier")
                for r in self.roles.values() if r.get("hub_de_ralliement")} - {None}

    # ------------------------------------------------------------------ #
    #  Le gabarit de frontmatter
    # ------------------------------------------------------------------ #
    def gabarit(self, rid: str) -> dict:
        return (self.roles.get(rid) or {}).get("champs") or {}

    def requis(self, rid: str) -> list[str]:
        return list(self.gabarit(rid).get("requis") or [])

    def autorises(self, rid: str) -> set[str]:
        return set(self.gabarit(rid).get("autorises") or [])

    def conditionnels(self, rid: str) -> list[dict]:
        """Les champs conditionnels d un role, chacun avec son SENS.

        `sens: permet` (defaut) — le champ n existe QUE si la condition tient.
        `sens: exige`           — le champ est REQUIS quand la condition tient.

        Le defaut est `permet`, et c est une mesure, pas un gout : lu comme une
        obligation, `si: "famille in [...]"` produisait 42 fausses violations
        sur un vault que ses deux validateurs declarent vert. Cf.
        `design/03-validation.md`, arbitrage 1.
        """
        out: list[dict] = []
        for c in self.gabarit(rid).get("conditionnels") or []:
            out.append({"champ": c["champ"], "si": c["si"],
                        "sens": c.get("sens", "permet")})
        return out

    def deprecies(self, rid: str) -> set[str]:
        return set(self.gabarit(rid).get("deprecies") or [])

    def roles_qui_portent(self, champ: str) -> list[str]:
        """Les roles dont le gabarit autorise ce champ.

        Sert a brancher une regle qui nomme un CHAMP sans nommer de role : le
        perimetre est alors l ensemble des roles qui peuvent le porter.
        """
        return sorted(rid for rid in self.roles if champ in self.autorises(rid))

    # ------------------------------------------------------------------ #
    #  Le dictionnaire de champs — resolution PAR SOURCE, jamais par nom
    # ------------------------------------------------------------------ #
    def champ(self, nom: str) -> dict:
        return self.champs.get(nom) or {}

    def champ_de_fonction(self, fonction: str) -> str | None:
        for nom, d in self.champs.items():
            if d.get("fonction") == fonction:
                return nom
        return None

    def vocabulaire(self, nom: str) -> set[str] | None:
        """Le vocabulaire ferme d un champ enumere, ou None.

        None a deux causes distinctes, et elles ne se confondent pas dans le
        message : le champ n est pas enumere, ou son vocabulaire vit dans un
        FICHIER (`vocabulaires.<x>`) que ce module ne lit pas — c est
        `vocabulaires.py` qui s en charge.
        """
        d = self.champ(nom)
        if d.get("type") not in ("enum", "liste_enum"):
            return None
        if d.get("valeurs"):
            return {str(v) for v in d["valeurs"]}
        src = str(d.get("source") or "").strip()
        if src == "roles[].id":
            return set(self.roles)
        if src in ("axes.rangement", self.champ_rangement):
            return set(self.valeurs_rangement)
        if src in ("axes.nature", self.champ_nature):
            return set(self.valeurs_nature)
        m = RE_SOURCE_TRANSVERSE.match(src)
        if m and m.group(1) in self.champs_transverses:
            return set(self.champs_transverses[m.group(1)]["valeurs"])
        return None

    def source_de_vocabulaire(self, nom: str) -> str | None:
        """Le fichier de vocabulaire d un champ enumere, s il en a un."""
        d = self.champ(nom)
        if d.get("type") not in ("enum", "liste_enum"):
            return None
        src = str(d.get("source") or "").strip()
        if src.startswith("vocabulaires."):
            return src.split(".", 1)[1]
        return None

    def champs_a_reciprocite(self) -> dict[str, dict]:
        """{champ : sa declaration `reciproque:`}, les deux modes confondus."""
        return {nom: d["reciproque"] for nom, d in self.champs.items()
                if isinstance(d.get("reciproque"), dict)}

    def champs_supprimes(self) -> set[str]:
        """Les champs que le contrat ne connait PLUS : `deprecated: true`, autorises nulle part.

        La distinction avec `roles[].champs.deprecies` est celle du contrat
        §2.10 : `deprecies` est un vestige TOLERE par un role (autorise, absent
        du gabarit genere) ; `champs.<x>.deprecated` marque un champ vestigial
        PARTOUT. Un champ vestigial partout et qu aucun `autorises` ne cite est
        un champ SUPPRIME — c est cette conjonction, et elle seule, qui branche
        la regle.
        """
        autorises_partout: set[str] = set()
        for rid in self.roles:
            autorises_partout |= self.autorises(rid)
        return {nom for nom, d in self.champs.items()
                if d.get("deprecated") and nom not in autorises_partout}

    # ------------------------------------------------------------------ #
    #  Le gabarit de corps
    # ------------------------------------------------------------------ #
    def corps(self, rid: str) -> list[dict]:
        return list((self.roles.get(rid) or {}).get("corps") or [])

    @staticmethod
    def titre(s: dict) -> str:
        """Le titre REND[U] d une section — celui qu une page porte."""
        return s.get("titre_rendu") or s["titre"]

    def section_de_genre(self, rid: str, genre: str) -> dict | None:
        for s in self.corps(rid):
            if s.get("genre") == genre:
                return s
        return None

    def sections_de_genre(self, rid: str, genre: str) -> list[dict]:
        return [s for s in self.corps(rid) if s.get("genre") == genre]

    def section_par_titre(self, rid: str, titre: str) -> dict | None:
        for s in self.corps(rid):
            if self.titre(s) == titre or s["titre"] == titre:
                return s
        return None

    def sections_adossees(self, rid: str) -> list[tuple[str, str]]:
        """(titre rendu, champ) des sections de liste de liens adossees a un champ."""
        return [(self.titre(s), s["champ"])
                for s in self.corps(rid)
                if s.get("genre") == GENRE_LISTE and s.get("champ")]

    # ------------------------------------------------------------------ #
    #  Les regles
    # ------------------------------------------------------------------ #
    def regle(self, rid: str) -> dict:
        return self.regles.get(rid) or {}

    def regle_active(self, rid: str) -> bool:
        r = self.regles.get(rid)
        return bool(r and r.get("active"))

    def severite(self, rid: str, cle: str | None = None) -> str:
        """La severite d une regle, scalaire ou par section.

        Une severite n est JAMAIS portable : `dure` et `avertissement` sont des
        resultats de mesure sur un corpus, pas des proprietes de regle. Le
        moteur les LIT, il n en propose aucune.
        """
        r = self.regles.get(rid) or self.socle.get(rid) or {}
        s = r.get("severite")
        if isinstance(s, dict):
            if cle is not None and cle in s:
                return str(s[cle])
            return "a_mesurer"
        return str(s or "a_mesurer")

    def codes(self, rid: str) -> list[str]:
        """La PROVENANCE d une regle : les identifiants de l ancien validateur.

        `code:` ne dit que d ou la regle vient. Ce qui la TIENT aujourd hui, quand
        ce n est pas le validateur, se lit dans `porte_par()`.
        """
        r = self.regles.get(rid) or self.socle.get(rid) or {}
        return [str(c) for c in (r.get("code") or [])]

    def porte_par(self, rid: str) -> str | None:
        """L outil qui TIENT la regle, quand le validateur la delegue. None sinon.

        Tranche au lot 4 (remontee 10 du lot 3). `code:` portait tantot un
        identifiant de regle (`R21`, `R8e`), tantot un nom de script
        (`check_arbo`), tantot une COMMANDE (`build_bandeau --check`) : le moteur
        devait deviner par convention laquelle des trois il lisait, et annoncer
        une delegation sur cette devinette. Les deux premieres sont de la
        provenance, la troisieme une delegation — et une delegation qui se
        devine est une delegation qui, un jour, ne se voit plus.
        """
        r = self.regles.get(rid) or self.socle.get(rid) or {}
        v = r.get("porte_par")
        return str(v) if v else None

    def enonce(self, rid: str) -> str:
        r = self.regles.get(rid) or self.socle.get(rid) or {}
        return str(r.get("enonce") or "").strip()

    def socle_declaree(self, rid: str) -> bool:
        return rid in self.socle

    def extension_de_vue(self) -> str | None:
        rid = self.role_de_fonction("vue")
        if rid is None:
            return None
        return ((self.roles[rid].get("vue_embarquee") or {}).get("extension"))

    def moteur_de_vue(self) -> str | None:
        rid = self.role_de_fonction("vue")
        if rid is None:
            return None
        return ((self.roles[rid].get("vue_embarquee") or {}).get("moteur"))


def charge(chemin: Path, controle: bool = True) -> Modele:
    """Le manifeste, charge et CONFRONTE A SA VERSION.

    C est le seul entonnoir de chargement du kit — les sept sous-commandes et
    les ponts d une instance en passent tous par lui — donc c est ici, et
    nulle part ailleurs, que se controle « ce kit sait-il lire ce manifeste ».
    Poser le controle dans chaque `__main__` aurait donne sept endroits a tenir
    a jour, donc six oublis en puissance.

    Un refus sort en **2** immediatement : une version inconnue n est pas une
    donnee douteuse dont on pourrait faire quelque chose, c est un contrat
    absent, et un verdict rendu par un code qu on n a pas choisi est pire
    qu une absence de verdict. `controle=False` existe pour le jeu d epreuve,
    qui doit pouvoir observer le refus sans le subir.
    """
    with chemin.open(encoding="utf-8") as f:
        brut = yaml.safe_load(f)
    if controle:
        from ..contrat import controle as _controle
        dits, refuse = _controle(brut or {})
        for ligne in dits:
            print(ligne)
        if refuse:
            raise SystemExit(2)
    return Modele(brut, chemin)
