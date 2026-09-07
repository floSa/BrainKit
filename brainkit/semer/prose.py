"""prose.py — les gabarits de phrase du SEMIS, et la frontiere avec ceux des generateurs.

Meme arbitrage que `generer/prose.py`, meme canal de surcharge
(`genere.prose.<cle>`), et la meme discipline : aucun gabarit ci-dessous ne
porte une valeur d instance. Ce qu ils portent est la langue et des trous
nommes, remplis par le manifeste.

# Ce qui est ici, et ce qui n y est PAS

Ici : les phrases d UNE LIGNE que le semis pose dans une PAGE — le resume d un
hub, la ligne d attente d une section a ecrire, l intitule d une colonne de
tableau vide. Ce sont les phrases que l utilisateur lit dans Obsidian.

Pas ici : les DOCUMENTS de gouvernance (`CLAUDE.md`, la taxonomie, le journal de
lot). Ce sont des textes longs et structures, et les declarer dans le manifeste
serait exactement l option 2 que `generer/prose.py` refuse : un brain neuf
devrait ecrire trois pages de francais avant que son routeur existe, et
l entretien du lot 6 devrait les demander. Ils vivent donc dans le module qui
les compose, et leurs VALEURS — nom du brain, roles, frontieres, identite git —
viennent du manifeste, jamais du kit.
"""

from __future__ import annotations

from ..generer.prose import Prose

DEFAUTS_SEMIS: dict[str, str | list[str]] = {
    # --- les hubs -----------------------------------------------------------
    "semis.hub.apport_arbre": "Le point d'entrée de {libelle} : ce que ce "
                              "{axe_rangement} porte, et par où commencer.",
    "semis.hub.apport_role": "Les {libelle_p} du brain, groupées par leur rôle — "
                             "aucune valeur de l'axe de rangement ne les range.",
    "semis.hub.apport_ralliement": "Toutes les {libelle_p} du brain, où qu'elles "
                                   "vivent dans l'arbre — c'est le lien retour qui "
                                   "fait la grappe.",
    "semis.hub.a_ecrire": "<!-- à écrire à la main : « {titre} ». Cette section "
                          "n'est PAS générée — seule la zone AUTO ci-dessous "
                          "l'est. -->",
    # --- la porte d entree --------------------------------------------------
    "semis.home.arbre": "L'arbre — un dossier par {axe_rangement}, à la racine",
    "semis.home.arbre_intro": "Chaque dossier porte une page `{champ_role}: hub` à "
                              "son nom. Le dossier se DÉRIVE de `{champ_rangement}:` "
                              "— personne ne choisit un chemin.",
    "semis.home.roles": "Rangés par `{champ_role}:` — aucune valeur d'axe ne les range",
    "semis.home.ralliement": "Réunis par `{champ_role}:`",
    "semis.home.transverses": "Les axes transverses",
    "semis.home.transverse_intro": "Un dossier par axe, un hub par valeur PORTÉE. "
                                   "Les hubs naissent quand une page porte la "
                                   "valeur, pas avant.",
    "semis.home.pilotage": "Pilotage",
    "semis.home.vide": "Le brain est **vide** : un hub par dossier, et aucune "
                       "autre page. Le remplissage commence au premier appel du "
                       "skill de capture.",
    # --- l inbox ------------------------------------------------------------
    "semis.inbox.regle": "Capture rapide, une ligne par item : "
                         "`- [ ] <{axe_rangement}> : <sujet>`.",
    "semis.inbox.traitement": "Traitement : demander au skill de capture de créer "
                              "et de ranger les pages, puis cocher. Rien de cette "
                              "liste n'est une page tant qu'elle n'a pas été "
                              "capturée.",
    # --- les gabarits -------------------------------------------------------
    "semis.gabarit.entete": "Gabarit `{champ_role}: {role}` — généré depuis "
                            "`roles[{role}]` du manifeste. Ne pas l'éditer à la "
                            "main : il se régénère, et deux sources qui décrivent "
                            "le même gabarit divergent (constat E4 du cadrage).",
    "semis.gabarit.a_remplir": "<!-- {quoi} -->",
}


class ProseSemis(Prose):
    """Les gabarits du semis, puis ceux des generateurs, puis les surcharges."""

    def brut(self, cle: str, /):
        if cle in self.surcharges:
            return self.surcharges[cle]
        if cle in DEFAUTS_SEMIS:
            return DEFAUTS_SEMIS[cle]
        return super().brut(cle)
