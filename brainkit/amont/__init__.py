"""brainkit.amont — l AMONT d une unite : la source vivante dont elle parle.

Une unite de brain decrit quelque chose qui existe ailleurs, et cet ailleurs a
sa propre vie. Une brique de developpement a un depot : il publie des versions,
il recoit des commits, et un jour son proprietaire l archive. L unite d un
autre brain n a rien de tel — un texte publie une fois ne sortira pas de
version 2.

C est pour cela que ce paquet est **entierement declaratif**. Le bloc `amont:`
du manifeste est FACULTATIF : un brain qui ne le declare pas ne sonde rien, ne
signale rien, et n affiche aucune colonne de fraicheur. Rien dans le code ne
suppose qu une unite ait un amont, et aucun mot de ce paquet ne nomme un depot,
un paquet Python ou une licence.

# Ce que ce paquet ne fait pas, et c est le lot

  - **Il n ecrit JAMAIS dans une page.** Sa seule sortie est le side-car
    declare par `amont.side_car`. Le champ que l amont contredit reste ce que
    l auteur du brain a ecrit : un desaccord se SIGNALE, il ne se corrige pas.
  - **Il n a pas de `--fix`**, et il n en aura pas. Le seul geste qu il
    pourrait automatiser — reecrire une valeur declaree parce que l amont dit
    autre chose — est precisement celui qui appartient a l auteur.
  - **Il n exige aucun jeton d API**, il n en lit aucun, il n en ecrit aucun.
    Les trois sondes tapent sur des URL publiques anonymes. Un jeton dans un
    vault versionne est un secret publie ; l absence de jeton n est donc pas une
    limitation subie, c est une contrainte de conception.
  - **Il ne rend jamais un code d erreur sur un CONSTAT.** Un depot tiers en
    panne, un amont injoignable, une licence changee : ce sont des faits du
    monde, pas des fautes du vault. Bloquer une cloture dessus rendrait le brain
    otage de l amont. La regle heritee de `verifier_fraicheur.py`, et elle
    tient.

# Les trois etats du savoir, et ils ne se confondent pas

`jamais_sonde` (le side-car ne connait pas la page), `sans_amont` (on a
regarde, il n y a rien a atteindre) et une date. Un compteur a zero n est pas
une bonne nouvelle : les trois se lisent separement dans le rapport, exactement
comme l inventaire du validateur distingue « tournee, aucun constat » de « non
declaree ».

# Ou l etat est CALCULE, et pourquoi la que et nulle part ailleurs

L etat (`recente`, `ancienne`, `archive`…) est derive **au moment du sondage**
et ECRIT dans le side-car. Il n est pas recalcule a la generation du bandeau, et
ce n est pas une optimisation : un etat calcule a la lecture dependrait de la
date du jour, donc la zone AUTO d une page changerait toute seule, sans qu aucun
sondage ait eu lieu et sans que rien le dise. Un artefact genere doit etre une
fonction de ce qui est ecrit, pas de quand on le lit. `sonder --recalculer`
rejoue la derivation sur les faits deja sondes, sans un seul appel reseau, quand
un seuil du manifeste change.
"""

from .declaration import Amont, declaration
from .etat import ETATS, derive
from .sidecar import (charge_faits, ecrit_side_car, faits_par_defaut,
                      lit_side_car)

__all__ = ["Amont", "declaration", "ETATS", "derive", "charge_faits",
           "faits_par_defaut", "lit_side_car", "ecrit_side_car"]
