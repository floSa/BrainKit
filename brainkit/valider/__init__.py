"""brainkit.valider — UN validateur de vault, pilote par `brain.yml`.

Il remplace les deux validateurs du DevBrain (`check_brain.py` et
`check_arbo.py`) et ne sait rien du dev : ni prefixe, ni categorie, ni famille,
ni role, ni titre de section, ni seuil de promotion, ni severite. Tout se lit
dans le manifeste.

    from pathlib import Path
    from brainkit.valider import charge, valide

    mo = charge(Path("exemples/devbrain.brain.yml"))
    v = valide(mo, Path("../DevBrain"))
    print(v.code, len(v.dures), len(v.avertissements))
"""

from .manifeste import Modele, charge
from .moteur import Verdict, imprime, valide

__all__ = ["Modele", "charge", "Verdict", "valide", "imprime"]
