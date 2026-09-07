"""brainkit.mesurer — ce qu une regle COUTE, avant qu on la durcisse.

C est le lot qui rend une severite MESUREE au lieu d etre decretee. §5.6 du
cadrage nomme le risque en une phrase — *« la tentation sera forte de livrer les
sept regles dures du DevBrain puisqu elles marchent »* — et ce paquet est la
reponse : par regle, le compte de violations, la POPULATION reellement mesuree,
la date, et une proposition de durcissement pour celles qui sont a zero. Avec
trois garde-fous qui ne se negocient pas (`gardes.py`).

    from pathlib import Path
    from brainkit.valider import charge, valide
    from brainkit.mesurer import mesure

    mo = charge(Path("exemples/devbrain.brain.yml"))
    m = mesure(mo, Path("../DevBrain"))
    print(m.pages_de_l_unite, len(m.propositions))

LECTURE SEULE, comme le validateur, et pour la meme raison : mesurer un vault ne
doit jamais le changer. Le seul chemin d ecriture du paquet est l option
`--rapport`, qui depose un fichier a un chemin que l utilisateur DONNE.

    grep -rnE 'write_text|write_bytes|mkdir|unlink|rmtree|rename' brainkit/mesurer/
    # -> les deux lignes de `--rapport`, dans __main__.py, et cette phrase

# Ce que `mesurer` ne fait pas, et c est le lot

Il ne durcit rien. Il ne recrit aucun manifeste. Sa sortie est une LISTE DE
TRAVAIL et non un verdict — la seule exception est le garde-fou 2, qui REFUSE
une severite `avertissement` sans motif ecrit, et qui le fait dans le code de
sortie parce qu un refus qu on n entend pas n est pas un refus.
"""

from .gardes import PLANCHER_PAGES, STRUCTURELLEMENT_DURES
from .regles import Ligne, Mesure

__all__ = ["mesure", "Mesure", "Ligne", "PLANCHER_PAGES",
           "STRUCTURELLEMENT_DURES"]


def mesure(mo, racine, date: str = ""):
    """La passe complete : valide, mesure, recense, occupe le gabarit, backlog.

    Rend `(mesure, recensement, occupations, backlog)`. La validation est
    refaite ici plutot que recue en parametre : la mesure a besoin du CONTEXTE
    du validateur (les promotions, les hubs, les pages du role de l unite), et
    le recalculer ailleurs serait la seconde source qu on passe le lot a
    supprimer.
    """
    from pathlib import Path

    from ..skills import propagation as _prop
    from ..valider import valide as _valide
    from . import backlog as _backlog
    from . import gabarit as _gabarit
    from . import recensement as _recensement
    from .regles import mesure_les_regles

    racine = Path(racine)
    v = _valide(mo, racine)
    m = mesure_les_regles(mo, v, racine.name, date=date)
    rec = _recensement.recense(v.contexte)
    occ = _gabarit.occupation(mo, v.contexte)
    derivees = len(_prop.derive(mo, mo.role_unite)) if mo.role_unite else None
    bl = _backlog.construis(mo, v.contexte, occupations=occ,
                            lignes_derivees=derivees)
    return m, rec, occ, bl
