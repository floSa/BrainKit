"""brainkit.semer — LE generateur d instance : de `brain.yml` a un vault vierge.

C est le livrable central du projet, et il tient en une phrase : **le kit ne
sait rien du sujet du brain qu il seme.** Tout ce qu il pose — l arbre, les
hubs, les gabarits, la taxonomie, le routeur, les hooks — se derive du
manifeste. Aucun mot de sujet, aucun titre de section code en dur.

    from pathlib import Path
    from brainkit.semer import seme, imprime
    from brainkit.valider import charge

    mo = charge(Path("gabarit/brain.yml"))
    s = seme(mo, Path("/tmp/mon-brain"))          # ne pose pas un octet
    imprime(s, mo, Path("/tmp/mon-brain"))

Le mode par defaut n ecrit rien. `plan.py` est le seul module du paquet capable
d ecrire, et il refuse quatre situations avant tout : une cible non vide, une
cible sous le depot du kit, une cible sous un depot git, une cible sous un vault.

Trois operations :

  - `seme()`        — le semis ;
  - `calcule()` / `applique()` de `reseuiller` — changer le seuil de promotion,
    qui est une MIGRATION et non un reglage (rupture 5 du test a blanc) ;
  - `fige()`        — copier le kit dans l instance, pour une livraison on-prem
    (§5.1 du cadrage : ce mode n est pas optionnel).
"""

from .figer import fige
from .plan import Plan
from .reseuiller import applique as applique_le_seuil
from .reseuiller import calcule as calcule_le_seuil
from .semis import Semis, imprime, seme, verifie

__all__ = ["seme", "imprime", "verifie", "Semis", "Plan",
           "calcule_le_seuil", "applique_le_seuil", "fige"]
