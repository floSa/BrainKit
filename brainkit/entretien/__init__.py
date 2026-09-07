"""brainkit.entretien — le lot 6 : l entretien qui construit un brain.

C est le module que l utilisateur rencontre EN PREMIER. Sans lui, creer un
brain demande d ecrire cent kilo-octets de YAML a la main, ce que personne ne
fera. Avec lui, une conversation d une heure et demie produit un `brain.yml`
valide, et le semis en tire un vault.

    passes.py      les onze passes et leurs questions, en DONNEES
    refus.py       les treize refus de deviner, en liste FERMEE et en controles
    induction.py   de vingt titres reels a une taxonomie — le coeur difficile
    brouillon.py   le mode REPRISE : un entretien s arrete et repart
    composer.py    des reponses au manifeste ; ce qui se demande, ce qui se derive
    rendu.py       le manifeste en YAML lisible, `motif:` compris

Le skill qui CONDUIT l entretien vit ailleurs — `skills/entretien/SKILL.md` — et
c est voulu : ce paquet porte la structure et les garde-fous, le skill porte la
conduite. Une conduite en Python serait un questionnaire ; un garde-fou en prose
se dilue en trois conversations.
"""

from __future__ import annotations

from .brouillon import Brouillon, charge, enregistre
from .composer import compose
from .passes import PASSES, QUESTIONS, total
from .refus import LES_TREIZE, arret
from .rendu import ecrit, rendu as rendu_yaml

__all__ = ["Brouillon", "charge", "enregistre", "compose", "PASSES",
           "QUESTIONS", "total", "LES_TREIZE", "arret", "ecrit", "rendu_yaml"]
