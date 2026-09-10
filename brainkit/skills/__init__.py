"""brainkit.skills — les trois skills d une instance, INSTANCIES depuis le manifeste.

    capture      ecrit dans le brain      -> porte la regle de propagation
    cloture      clot toute ecriture      -> porte la politique git, et elle seule
    exploitation consomme, n ecrit rien   -> porte le livrable declare

Le decoupage est STRUCTUREL, pas thematique — c est la brique K1 de l inventaire
de separation : un skill qui ecrit, un skill qui clot, un skill qui consomme.
Tout brain a besoin des trois, quel que soit son sujet.

# Ce que ce paquet garantit, et qui est verifiable

**Aucune valeur d instance n est ecrite ici.** Pas un nom de role, pas un titre
de section, pas un nom de champ, pas une valeur d axe. Ce que ces modules
portent est de la LANGUE et une STRUCTURE ; tout le reste vient de `brain.yml` —
et la table de propagation, elle, est DERIVEE (`propagation.py`), pas recopiee.

Le controle est une commande :

    uv run tests/skills.py --generique

Il seme deux brains sans un mot commun et verifie que chaque mot de vocabulaire
du premier est absent des skills du second. Une table identique sur deux brains differents serait la preuve qu elle
est recopiee.

# Le troisieme skill peut ne pas exister, et c est une reponse

`skills.exploitation` n est pas requis par le schema : la passe 10 de l entretien
porte un REFUS DE DEVINER, et un utilisateur peut ne pas savoir encore ce qu il
produira. Dans ce cas le skill n est PAS ecrit, et le README des skills dit
pourquoi. Un skill creux serait charge a chaque conversation et mentirait.
"""

from __future__ import annotations

from ..valider.manifeste import Modele
from . import capture, cloture, commun, exploitation, propagation

__all__ = ["capture", "cloture", "exploitation", "propagation", "commun",
           "rendus", "chemin_du_skill"]


def chemin_du_skill(nom: str) -> str:
    return f".claude/skills/{nom}/SKILL.md"


def rendus(mo: Modele) -> dict[str, str]:
    """{chemin relatif : contenu} — les skills que CE manifeste produit.

    Un dictionnaire plutot qu une ecriture : le semis a un plan unique
    (`semer/plan.py`), et un module qui ecrirait directement le contournerait.
    Les tests, eux, lisent ce dictionnaire sans toucher un disque.
    """
    out: dict[str, str] = {}
    nom = commun.nom_du_skill(mo, "capture")
    if nom:
        out[chemin_du_skill(nom)] = capture.skill(mo)
    nom = commun.nom_du_skill(mo, "cloture")
    if nom:
        out[chemin_du_skill(nom)] = cloture.skill(mo)
    if exploitation.declare(mo):
        nom = commun.nom_du_skill(mo, "exploitation")
        out[chemin_du_skill(str(nom))] = exploitation.skill(mo)
    return out
