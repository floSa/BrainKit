"""gardes.py — les TROIS garde-fous de §5.6, et rien d autre.

Ils ne sont pas des options de la mesure : ils sont ce qui distingue une mesure
d une superstition. Le risque que §5.6 nomme est precis — *« la tentation sera
forte de livrer les sept regles dures du vault d'origine puisqu elles marchent »* — et
la reponse tient en une phrase : **une severite est un resultat de mesure sur un
corpus, pas une propriete de regle.** Elle ne se porte donc pas d un brain a
l autre, et un brain neuf nait en `a_mesurer`.

# Garde-fou 1 — le plancher

    Une regle ne se durcit pas sous 30 pages de l unite.

Trente est ecrit dans le cadrage, et le chiffre importe moins que ce qu il
protege : sous le plancher, zero violation ne dit pas « la regle est
respectee », il dit « la regle n a rien vu ». BrainRef, avec dix pages de son
unite, est le controle negatif de ce lot — et il est aussi important que le
positif : un outil qui durcirait un brain de dix pages transformerait chaque
regle en superstition.

Le plancher se lit DEUX fois, et la seconde est un arbitrage de ce lot :

  - **plancher d instance** — le vault porte-t-il 30 pages du role
    `fonction: unite` ? Si non, AUCUNE proposition n est emise, pour aucune
    regle. C est le garde-fou tel que §5.6 l ecrit.
  - **plancher de regle** — la regle a-t-elle REELLEMENT mesure 30 pages ? Le
    cadrage exprime son plancher en « pages de l unite » parce que c est la
    population de la plupart des regles ; une regle dont la population reelle
    est plus petite n est pas couverte par ce raisonnement. Sur le vault d'origine, qui
    passe largement le plancher d instance, cette seconde lecture ne change
    RIEN — c est ce qui rend l ajout sans risque : il ne se paie pas.

Une regle dont le denominateur n est pas un volume de corpus — verifiable sur le
MANIFESTE, sans lire une page — echappe au plancher, et c est le seul cas.
`paire_inverse_bien_declaree` est de celles-la : elle est dure d emblee dans
BrainRef, et ce n est pas une entorse, c est un trou qu on refuse d ouvrir.

# Garde-fou 2 — le motif obligatoire

    Une regle qui reste en avertissement doit porter un `motif:` ECRIT ; le kit
    REFUSE un `severite: avertissement` sans motif.

« Refuse » est pris au mot : c est le seul endroit de `mesurer` qui change le
code de sortie. Un refus qui ne se voit pas dans le code de sortie est un refus
que personne ne lit — meme raisonnement que « une regle absente ne ressemble pas
a une regle souple, elle ressemble a une regle satisfaite ».

Corollaire, et c est un arbitrage de ce lot : **toute proposition de
durcissement emise ici porte un emplacement `motif:` vide et OBLIGATOIRE.** Le
kit sait mesurer, il ne sait pas ecrire pourquoi — et une severite dont personne
n a ecrit la raison est exactement la severite heritee que §5.6 interdit.

# Garde-fou 3 — les deux regles structurellement dures

    `chemin_categorie` et `bandeau_a_jour` sont dures des le depart : une
    violation y est une INCOHERENCE DE STRUCTURE, pas un defaut de redaction.

La liste est FERMEE PAR LE KIT, comme celle des dix. Elle ne se lit pas dans le
manifeste, et c est le point : un garde-fou qu une instance peut desactiver en
ecrivant `structurellement_dure: false` n est pas un garde-fou. Le manifeste
du manifeste de reference ecrit precisement cela — il porte la recommandation de §5.6 sans
l appliquer, parce que le point n etait pas tranche quand il a ete ecrit. Il
l est ici, dans le sens que §5.6 recommandait, et `mesurer` SIGNALE la
contradiction au lieu de la resoudre en silence.

Ce que garde-fou 3 ne fait PAS : proposer un durcissement. Ces deux regles ne
relevent pas du regime de la mesure — leur durete ne s obtient pas en comptant
des violations —, donc elles se decident quand le manifeste s ecrit, pas quand
on mesure. Sur un vault sous le plancher, `mesurer` ne propose donc toujours
RIEN, y compris pour elles.
"""

from __future__ import annotations

import re

#: §5.6, ecrit tel quel. Le nombre de pages du role `fonction: unite` sous
#: lequel aucun durcissement n est propose.
PLANCHER_PAGES = 30

#: Fermee par le kit. Cf. l en-tete : une liste qu une instance peut contredire
#: n est pas un garde-fou.
STRUCTURELLEMENT_DURES = ("chemin_categorie", "bandeau_a_jour")

#: La convention d annotation du manifeste (propriete 2) : `motif`,
#: `motif_<x>` ou `note_<x>`. Un motif ECRIT est n importe laquelle des trois.
RE_MOTIF = re.compile(r"^(motif|note)(_[a-z0-9_]+)?$")

# Les verdicts d une regle, fermes. Ils ne se melangent pas : « rien a proposer
# parce que la regle est deja dure » et « rien a proposer parce que le vault est
# trop petit » sont deux silences differents.
DEJA_DURE = "deja_dure"
A_REPARER = "a_reparer"
PROPOSEE = "proposee"
REFUS_INSTANCE = "refus_instance"
REFUS_POPULATION = "refus_population"
STRUCTURELLE = "structurelle"
NON_MESUREE = "non_mesuree"


def motif_ecrit(decl: dict) -> str:
    """Le motif ECRIT d une declaration de regle, ou la chaine vide.

    N importe quelle annotation de la propriete 2 compte : ce qui est exige est
    qu une phrase existe, pas qu elle porte un nom precis.
    """
    for cle, valeur in (decl or {}).items():
        if RE_MOTIF.match(str(cle)) and str(valeur).strip():
            return str(valeur).strip()
    return ""


def plancher_tenu(pages_de_l_unite: int) -> bool:
    return pages_de_l_unite >= PLANCHER_PAGES


def manque_au_plancher(n: int) -> int:
    return max(0, PLANCHER_PAGES - n)
