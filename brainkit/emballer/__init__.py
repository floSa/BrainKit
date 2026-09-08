"""brainkit.emballer — les DOCUMENTS d une instance, generes depuis `brain.yml`.

    INSTALL.md          installer ce brain sur une machine neuve
    docs/manuel.md      lire le brain
    docs/enrichir.md    ecrire dedans, et ce que ca declenche autour
    docs/exploiter.md   s en servir depuis un travail, sans y ecrire

# Pourquoi un paquet, et pas quatre fichiers ecrits a la main

Propriete 1 du manifeste : *il est la seule source*. Ces quatre documents
nomment le dossier des gabarits, la table de couleurs, les trois skills, le
seuil de promotion, les titres de section et les champs indexes — une vingtaine
de valeurs qui vivent AUSSI dans `brain.yml`. Ecrits a la main, ils prennent du
retard : c est le constat E4, et il est mesure dans le DevBrain, dont
`Templates/` a pris trois lots de retard sur ses 337 pages.

# La frontiere avec `brainkit.skills`

Un skill s adresse a un AGENT : il porte une procedure, des refus, des
anti-patterns. Un guide s adresse a un HUMAIN : il porte ce qu il faut
comprendre pour ne pas se tromper. Les deux disent des choses vraies du meme
brain, et les DERIVATIONS sont partagees — la table de propagation et la table
des effets de bord sortent de `skills.propagation`, une seule fois, pour les
deux. Deux derivations qui se ressembleraient auraient ete deux choses a tenir
a jour.

# Ou ces documents atterrissent

`rendus(mo)` rend un dictionnaire {chemin relatif : contenu}, et c est le SEMIS
qui les pose — par son plan d ecriture unique (`semer/plan.py`). Ce module
n ecrit pas un octet : un module qui ecrirait directement contournerait le plan,
donc ses quatre refus.

`docs/` doit etre dans `genere.non_pages` du manifeste, et le semis l exige :
sans ca, le validateur lirait ces guides comme des pages, et un guide n a ni
role ni valeur d axe.
"""

from __future__ import annotations

from ..valider.manifeste import Modele
from . import guides, images, install

__all__ = ["install", "guides", "images", "rendus",
           "CHEMIN_INSTALL", "DOSSIER_GUIDES"]

CHEMIN_INSTALL = "INSTALL.md"
DOSSIER_GUIDES = "docs"


def rendus(mo: Modele) -> dict[str, str]:
    """{chemin relatif : contenu} — les documents que CE manifeste produit."""
    out = {CHEMIN_INSTALL: install.document(mo)}
    for nom, texte in guides.rendus(mo).items():
        out[f"{DOSSIER_GUIDES}/{nom}"] = texte
    return out


# Il y avait ici un `rendus_du_kit()` : le meme generateur, appele avec un
# manifeste VIDE, pour produire l `INSTALL.md` du DEPOT DU KIT. Il est retire,
# et le motif vaut d etre garde.
#
# Ce document ne lisait AUCUNE valeur de manifeste — la preuve etant qu il se
# rendait sans en avoir un. Ce n etait donc pas de la generation, c etait de la
# prose ecrite en Python : plus dure a modifier qu un fichier markdown, et
# surtout incapable de porter une image, puisque `images.appel()` interdit
# (a raison) toute balise `![]()` dans un document genere.
#
# La doc du kit est desormais ecrite a la main, dans `docs/`, et elle porte ses
# captures. Ce module ne s adresse plus qu a UNE INSTANCE, ce qui est le seul
# lecteur pour lequel la propriete 1 du manifeste ait quelque chose a dire.
#
# `install.document()` accepte encore `None` : ce chemin n a plus d appelant.
# Son retrait est un refactor de ~250 lignes du generateur, hors du perimetre
# d un lot de documentation — il est ecrit en remontee dans
# `design/12-captures.md`.
