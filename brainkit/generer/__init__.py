"""brainkit.generer — LES generateurs d artefacts derives, pilotes par `brain.yml`.

Ils remplacent les quatre scripts du DevBrain — `build_index.py`,
`build_mocs.py`, `build_links.py`, `build_bandeau.py` — et ne savent rien du
dev : ni prefixe, ni valeur d axe, ni role, ni titre de section, ni colonne de
bandeau, ni libelle. Tout se lit dans le manifeste.

    from pathlib import Path
    from brainkit.generer import genere_tout
    from brainkit.valider import charge

    mo = charge(Path("<vault>/brain.yml"))
    s = genere_tout(mo, Path("../DevBrain"))     # mode `check` : n ecrit rien
    print(len(s.ecarts()), "écart(s)")

Le mode par defaut est `check` : il ne pose pas un octet. Ecrire se demande, et
`sortie.py` est le seul module du paquet qui en soit capable.
"""

from .corpus import Corpus, charge_corpus
from .orchestre import ARTEFACTS, genere_tout, imprime
from .sortie import CHECK, ECRIRE, SORTIE, Sortie

__all__ = ["Corpus", "charge_corpus", "genere_tout", "imprime", "ARTEFACTS",
           "Sortie", "CHECK", "SORTIE", "ECRIRE"]
