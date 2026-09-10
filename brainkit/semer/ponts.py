"""ponts.py — la COUCHE D ADAPTATION d une instance, posee par le semis.

# Le trou que ce module ferme — remontee 1 du lot 9

Le lot 9 a fait du vault d'origine une instance du kit. Il n a PAS supprime ses sept
scripts : il les a reduits a des **ponts** de vingt lignes qui resolvent le kit,
chargent `brain.yml` et l appellent. Deux motifs, tous deux mesures :

  - **un contrat.** Le skill de capture, le skill de cloture, la configuration
    de l agent et son hook de fin de session nommaient tous
    `AI/scripts/<script>.py`. Ce sont les fichiers qui pilotent l ecriture dans
    le vault, et ils sont lus a chaque session. Remplacer l outillage en
    cassant ce qui ecrit les pages aurait ete une victoire de comptable ;
  - **un octet.** `genere.index.signature` porte le nom du fichier qu un humain
    lance, et cette chaine est DANS l artefact versionne. Tant que le fichier
    lance porte ce nom, la signature reste exacte et l artefact ne bouge pas.

Et le constat que le lot 9 en a tire, qui est la raison de ce module : **ces
553 lignes etaient du code d instance.** Dans aucun paquet, teste par aucun jeu
d epreuve, et la prochaine instance les aurait reecrites. Or ce n est pas une
singularite du vault d'origine : TOUTE instance qui a des habitudes — un hook, un
skill, une commande dans un README — preferera garder ses noms.

# Ce que le semis pose, et selon quoi

| Quoi | Quand | Depuis |
|---|---|---|
| `<agent>/scripts/_pont_kit.py` | **toujours** | rien a declarer : la resolution est integralement generique |
| `<agent>/scripts/<nom>.py` | si `agent.ponts` le declare | `{nom: cible}` |

Le resolveur est pose **meme sans alias declare**, et meme sur une instance
figee. C est la reponse a l autre moitie de la remontee 5 du lot 7 : une
instance branchee sait qu elle depend d un kit, elle ne sait pas OU il vit. Le
PATH est l autre bouchon, et il est une **etape d installation** — donc quelque
chose qu on oublie. Les deux valent mieux qu un seul.

# Les cibles sont FERMEES, et c est deliberé

`agent.ponts` associe un nom de fichier a une cible prise dans une liste de
huit. Ce n est pas de la parcimonie : un pont dont la cible serait une chaine
libre serait un mini-langage de commande dans un manifeste, donc une seconde
facon de lancer le kit — et deux facons de lancer le meme code divergent. Les
huit cibles couvrent exactement les sept ponts que le lot 9 a ecrits a la main,
plus la validation complete.
"""

from __future__ import annotations

from ..valider.manifeste import Modele
from .plan import Plan

QUOI = "ponts"
RESOLVEUR = "_pont_kit.py"

# {cible : (ce que le pont fait, le gabarit a rendre)}. Ferme par le kit.
CIBLES: dict[str, str] = {
    "valider": "le verdict entier — les règles de contenu et de structure",
    "structure": "les seules règles de STRUCTURE, sans le bruit du contenu",
    "generer": "les quatre artefacts dérivés, `--check` par défaut",
    "index": "le catalogue machine et le document humain",
    "hubs": "les zones générées des hubs, et les hubs d'axe transverse",
    "liens": "la carte des liens, et les liens non résolus",
    "bandeau": "le haut de page de chaque page qui en porte un",
    "chemins": "une BIBLIOTHÈQUE, pas une commande : la dérivation "
               "valeur d'axe → dossier, importable",
}

# Les regles que le kit tient pour des regles de STRUCTURE. Fermee, et pour un
# motif ecrit : une regle de CONTENU qui entrerait ici rendrait les deux entrees
# de validation redondantes, et la distinction que le pont existe pour tenir
# deviendrait decorative.
STRUCTURE = ("chemin_categorie", "hub_par_niveau", "frontmatter_lisible")

_ENTETE = '''# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
'''


def dossier_des_scripts(mo: Modele) -> str:
    racine = str(((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    return f"{racine}/scripts"


def _profondeur(mo: Modele) -> int:
    """De combien de niveaux `_pont_kit.py` est-il sous la racine du vault ?

    `<agent>/scripts/_pont_kit.py` : autant de segments que le chemin en porte.
    Se calculer plutot que se coder en dur, parce que `agent.racine` est
    declaree — le vault d'origine dit `AI/`, un autre brain dira `agent/interne/`.
    """
    return len(dossier_des_scripts(mo).split("/"))


def declares(mo: Modele) -> dict[str, str]:
    """{nom de fichier sans `.py` : cible}, tels que le manifeste les declare."""
    brut = ((mo.m.get("agent") or {}).get("ponts") or {})
    return {str(k): str(v) for k, v in brut.items()}


def manques(mo: Modele) -> list[str]:
    """Les cibles inconnues. Un pont vers une cible inventee ne se pose pas."""
    return [f"`agent.ponts.{nom}: {cible}` — cible inconnue. Les cibles sont "
            f"fermées : {', '.join(sorted(CIBLES))}"
            for nom, cible in declares(mo).items() if cible not in CIBLES]


# --------------------------------------------------------------------------- #
#  Le resolveur — la seule piece integralement generique de la couche
# --------------------------------------------------------------------------- #
def resolveur(mo: Modele) -> str:
    scripts = dossier_des_scripts(mo)
    n = _profondeur(mo)
    mode = str((mo.m.get("kit") or {}).get("mode") or "branche")
    version = (mo.m.get("kit") or {}).get("version") or "?"
    return _ENTETE + f'''"""{RESOLVEUR} — COMMENT CE VAULT ATTEINT BRAINKIT.

Écrit une fois par `brainkit semer`, lu par tous les ponts de `{scripts}/`.

Ce vault est une **instance** de BrainKit `{version}` (`kit.mode: {mode}`) : il
ne porte pas les règles, il les lit. Les deux validateurs et les quatre
générateurs vivent dans le kit et lisent `brain.yml` — aucune ligne du kit n'est
copiée ici tant que `brainkit freeze` n'a pas été lancé. Une copie forkerait le
jour où elle est faite, et c'est exactement le défaut que `brain.yml` existe
pour supprimer.

# La résolution : trois pistes, dans cet ordre, arrêt à la première qui répond

`kit.mode: branche` dit que le code vit ailleurs, sans dire **où**. Deux
bouchons existent, et ils ne s'excluent pas : mettre `brainkit` sur le PATH est
une étape d'installation — donc quelque chose qu'on oublie — et ce fichier est
ce qui rattrape l'oubli.

  1. `$BRAINKIT_RACINE` — l'échappatoire explicite, pour un kit rangé ailleurs ;
  2. `{scripts}/brainkit/` — une instance **FIGÉE**, où `brainkit freeze` a
     copié le kit dans le vault. Ce cas passe **avant** la recherche par
     voisinage : une instance figée est une instance qui ne doit plus jamais
     lire un kit du dehors, c'est toute sa raison d'être. Une résolution qui
     trouverait le kit voisin d'abord annulerait `freeze` en silence ;
  3. le **voisinage**, en remontant depuis la racine du vault : `<parent>/BrainKit`
     à chaque niveau, et pas seulement au premier. Le cas nominal — les deux
     dépôts côte à côte — répond tout de suite ; un arbre de travail d'agent,
     qui vit plusieurs niveaux plus bas, répond plus haut. Ne regarder que le
     premier parent rendrait le pont inutilisable là où on en a le plus besoin.

Si aucune ne répond, ce module **s'arrête et dit les trois pistes**. Il ne
devine pas : un kit deviné est un verdict rendu par un code qu'on n'a pas
choisi.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# La racine du vault : ce fichier vit dans `<vault>/{scripts}/`.
VAULT = Path(__file__).resolve().parents[{n}]
MANIFESTE = VAULT / "brain.yml"

_MARQUEUR = Path("brainkit") / "__init__.py"
_SCRIPTS = VAULT / "{scripts}"


def _porte_le_kit(racine: Path) -> bool:
    return (racine / _MARQUEUR).is_file()


def racine_du_kit() -> Path:
    """Où vit BrainKit. S'arrête si personne ne répond — jamais de devinette."""
    pistes: list[str] = []

    env = os.environ.get("BRAINKIT_RACINE")
    if env:
        p = Path(env).expanduser()
        if _porte_le_kit(p):
            return p.resolve()
        pistes.append(f"$BRAINKIT_RACINE = `{{env}}` — ne porte pas "
                      f"`brainkit/__init__.py`")

    if _porte_le_kit(_SCRIPTS):
        return _SCRIPTS.resolve()

    for parent in [VAULT, *VAULT.parents]:
        candidat = parent / "BrainKit"
        if _porte_le_kit(candidat):
            return candidat.resolve()
    pistes.append(f"aucun `BrainKit/` en remontant depuis `{{VAULT}}`")

    print("BrainKit introuvable — ce vault est une INSTANCE : son outillage "
          "vit dans le kit.", file=sys.stderr)
    for p in pistes:
        print(f"  - {{p}}", file=sys.stderr)
    print("\\n  Trois façons de le dire, de la plus locale à la plus durable :\\n"
          "    1. poser le dépôt BrainKit à côté du vault ;\\n"
          "    2. exporter BRAINKIT_RACINE=<racine du dépôt BrainKit> ;\\n"
          "    3. `brainkit freeze --vault .` depuis le kit, qui le copie DANS "
          "le vault et coupe la dépendance (livraison on-prem).", file=sys.stderr)
    raise SystemExit(2)


def branche() -> Path:
    """Met le kit sur `sys.path` et rend sa racine. Idempotent."""
    racine = racine_du_kit()
    if str(racine) not in sys.path:
        sys.path.insert(0, str(racine))
    return racine


def manifeste() -> Path:
    if not MANIFESTE.is_file():
        print(f"manifeste introuvable : {{MANIFESTE}}\\n"
              "  Un manifeste ne se devine pas : c'est ce contre quoi le "
              "verdict est rendu.", file=sys.stderr)
        raise SystemExit(2)
    return MANIFESTE


def modele():
    """Le manifeste du vault, chargé par le kit — version comprise."""
    branche()
    from brainkit.valider import charge          # noqa: PLC0415 — après branche()
    return charge(manifeste())


def sortie_utf8() -> None:
    """Une console peut être en page de code locale ; le vault est accentué."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
'''


# --------------------------------------------------------------------------- #
#  Les ponts d alias
# --------------------------------------------------------------------------- #
_PROLOGUE = '''from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pont_kit                                            # noqa: E402
'''


def _docstring(nom: str, cible: str, quoi: str) -> str:
    return (f'"""{nom}.py — PONT vers le kit : {quoi}.\n\n'
            f'    uv run <ce fichier>\n\n'
            f'Ce fichier ne porte aucune règle : il résout le kit, charge\n'
            f'`brain.yml` et appelle `{cible}`. Il existe parce que les skills,\n'
            f'les hooks et la configuration de l\'agent nomment CE chemin — un\n'
            f'contrat de travail lu à chaque session, qu\'un changement\n'
            f'd\'outillage n\'a aucune raison de casser.\n\n'
            f'Généré par `brainkit semer` depuis `agent.ponts` du manifeste.\n'
            f'Ne pas l\'éditer à la main : il se régénère.\n\n'
            f'Où vit le kit : `{RESOLVEUR}`.\n"""\n')


def pont(mo: Modele, nom: str, cible: str) -> str:
    quoi = CIBLES[cible]
    tete = _ENTETE + _docstring(nom, cible, quoi) + "\n" + _PROLOGUE

    if cible == "valider":
        return tete + '''

def main() -> int:
    _pont_kit.sortie_utf8()
    _pont_kit.branche()
    from brainkit.valider import charge, imprime, valide     # noqa: PLC0415
    import argparse                                          # noqa: PLC0415

    ap = argparse.ArgumentParser(description="Valide ce vault contre `brain.yml`.")
    ap.add_argument("--regle", default=None)
    ap.add_argument("--tout", action="store_true")
    ns = ap.parse_args()

    mo = charge(_pont_kit.manifeste())
    v = valide(mo, _pont_kit.VAULT)
    return imprime(v, mo, _pont_kit.VAULT, regle=ns.regle, tout=ns.tout)


if __name__ == "__main__":
    raise SystemExit(main())
'''

    if cible == "structure":
        return tete + f'''
# Les regles que le kit tient pour des regles de STRUCTURE. Fermee : une regle
# de CONTENU qui entrerait ici rendrait les deux entrees redondantes.
STRUCTURE = {STRUCTURE!r}


def main() -> int:
    _pont_kit.sortie_utf8()
    _pont_kit.branche()
    from brainkit.valider import charge, valide              # noqa: PLC0415
    from brainkit.valider import constat                     # noqa: PLC0415

    mo = charge(_pont_kit.manifeste())
    v = valide(mo, _pont_kit.VAULT)
    tenus = [c for c in v.rapport.constats if c.regle in STRUCTURE]
    dures = [c for c in tenus if c.severite == constat.DURE]
    autres = [c for c in tenus if c.severite != constat.DURE]

    par_tete: dict[str, int] = {{}}
    for p in v.contexte.pages:
        if "/" in p.chemin:
            tete = p.chemin.split("/", 1)[0]
            par_tete[tete] = par_tete.get(tete, 0) + 1

    print(f"structure : {{len(v.contexte.pages)}} page(s) dans "
          f"{{len(par_tete)}} dossier(s) de premier niveau — "
          f"{{', '.join(STRUCTURE)}}")
    for tete, n in sorted(par_tete.items()):
        print(f"  {{tete}}/ — {{n}} page(s)")
    for c in sorted(autres, key=lambda c: (c.regle, c.page)):
        print(f"  [WARN] {{c.regle}} — {{c.rendu()}}")
    if dures:
        print(f"\\n{{len(dures)}} écart(s) :")
        for c in sorted(dures, key=lambda c: (c.regle, c.page)):
            print(f"  [FAIL] {{c.regle}} — {{c.rendu()}}")
        return 1
    print("\\nOK — chemin et dossier dérivé concordent partout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

    if cible in ("generer", "index", "hubs", "liens", "bandeau"):
        quoi_opt = ("" if cible == "generer"
                    else f'"--quoi", {cible!r}, ')
        return tete + f'''

def main() -> int:
    _pont_kit.sortie_utf8()
    _pont_kit.branche()
    from brainkit.generer.__main__ import main as generer    # noqa: PLC0415

    # ATTENTION, et c est deliberé : ce pont ECRIT par defaut, la ou
    # `brainkit generer` ne fait que verifier. Ce n est pas une distraction —
    # c est la seule raison d etre d un pont. Un fichier nomme « construis
    # ceci » est appele par un hook et par un skill pour CONSTRUIRE ; en faire
    # un verificateur silencieux casserait exactement l habitude que le pont
    # existe pour menager. `--check` reste disponible, et sort en 2 sur ecart.
    reste = [a for a in sys.argv[1:] if a != "--check"]
    mode = ["--check"] if "--check" in sys.argv[1:] else ["--ecrire"]
    sys.argv = ["brainkit generer", "--vault", str(_pont_kit.VAULT),
                {quoi_opt}*mode, *reste]
    return generer()


if __name__ == "__main__":
    raise SystemExit(main())
'''

    # `chemins` : une BIBLIOTHEQUE. Pas de `main()`, pas de sortie — un module
    # qu on IMPORTE, parce que c est comme ca que le skill de capture s en sert.
    return _ENTETE + _docstring(nom, cible, quoi) + '''
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _pont_kit                                            # noqa: E402

_pont_kit.branche()

from brainkit.valider import chemins as _chemins            # noqa: E402
from brainkit.valider import charge                         # noqa: E402

MO = charge(_pont_kit.manifeste())

#: Le seuil de promotion d un sous-dossier, tel que le manifeste le declare.
SEUIL: int = MO.seuil

#: Les roles qui n ont AUCUN chemin a deriver — ils ne portent pas l axe.
ROLES_SANS_AXE = {r for r in MO.roles if not MO.porte_l_axe_de_rangement(r)}

#: Les roles qui ne PESENT pas sur le seuil — « une vue n est pas un membre de
#: la vue ». C est `pese_sur_le_seuil: false` du manifeste. A ne pas confondre
#: avec le precedent : ne pas peser n est pas ne pas se ranger.
ROLES_HORS_SEUIL = {r for r in MO.roles if not MO.pese_sur_le_seuil(r)}


def tete(valeur: str) -> str | None:
    """Le dossier de premier niveau d une valeur d axe. None si le prefixe est inconnu."""
    return MO.dossier_de_prefixe.get(str(valeur).split("/")[0])


def promotions(valeurs: list[str]) -> dict[str, str]:
    """Les sous-valeurs promues en dossier, sur la population donnee.

    Leve `KeyError` si une sous-valeur franchit le seuil sans libelle declare :
    le libelle se LIT dans `brain.yml`, il ne se devine pas.
    """
    promus, sans_libelle = _chemins.promotions_depuis_valeurs(valeurs, MO)
    if sans_libelle:
        raise KeyError("; ".join(sans_libelle)
                       + " — le libellé s'ajoute dans `brain.yml`, sous "
                         "`axes.rangement.prefixes[].sous`.")
    return promus


def dossier_attendu(valeur: str, promus: dict[str, str]) -> str | None:
    """Le dossier d accueil, relatif a la racine du vault. None si inderivable."""
    return _chemins.dossier_attendu(str(valeur), promus, MO)
'''


def seme_les_ponts(mo: Modele, plan: Plan) -> None:
    """Le resolveur, toujours ; les alias, si le manifeste en declare."""
    scripts = dossier_des_scripts(mo)
    plan.pose(f"{scripts}/{RESOLVEUR}", resolveur(mo), QUOI)
    for nom, cible in sorted(declares(mo).items()):
        if cible not in CIBLES:                 # refuse en amont par `exigences`
            continue
        plan.pose(f"{scripts}/{nom}.py", pont(mo, nom, cible), QUOI)
