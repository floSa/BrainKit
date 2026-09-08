"""images.py — le MANIFESTE D IMAGES, et pourquoi le kit n embarque aucune capture.

# Le constat N3 de l inventaire, applique

L `INSTALL.md` du DevBrain porte 28 captures. L inventaire de separation les a
comptees en deux tas, et la coupure n est pas esthetique :

  - **17 montrent l interface d Obsidian** — panneaux de reglages, navigateur de
    plugins, options de plugin. Elles ne montrent rien du DevBrain, donc elles
    valent pour n importe quelle instance : ce sont des captures DU KIT (N2).
    Le kit en declare **16** : celle de l extrait CSS est tombee, parce
    qu aucun mecanisme du kit ne produit d extrait CSS — demander la capture
    d une chose qui n existe pas serait le bruit que ce module doit eviter ;
  - **11 montrent du contenu de dev** — l arbre du vault, une fiche, deux
    comparatifs, le graphe colore. Elles sont fausses des la deuxieme instance :
    ce sont des captures D INSTANCE (N3).

Et la conclusion que N3 tire, qui est la raison d etre de ce module :

  > la doc generee doit **REFERENCER** ses captures par un manifeste d images,
  > pas les embarquer en dur.

# Ce que ce module fait, et ce qu il ne fait surtout pas

Il declare, pour chaque capture, son fichier, l endroit du document ou elle
va, ce qu elle doit montrer, et sa portee (kit ou instance). Le generateur pose
a cet endroit un appel de figure — pas une image. **Aucune capture n est
fabriquee**, et c est explicite : une capture inventee montrerait une interface
qui n existe pas, ce qui est strictement pire qu un trou nomme. Le lot 10 a
recu l interdiction en toutes lettres, et elle est bonne.

Une capture manquante se lit donc dans le document comme un trou NOMME, avec ce
qu il faudrait photographier. C est le meme raisonnement que la regle dure du
lot 6 sur les bandeaux : *une fiche vide honnetement vaut mieux qu une fiche
remplie au juge*.

# Le nommage

`img/NN-slug.png`, numerote dans l ordre de lecture du document, sous le dossier
`docs/install/` de l instance (ou du depot du kit pour les captures de portee
`kit`). Les numeros ne sont pas jointifs et n ont pas a l etre : ils disent
l ordre, pas un compte.
"""

from __future__ import annotations

from dataclasses import dataclass

KIT, INSTANCE = "kit", "instance"


@dataclass(frozen=True)
class Capture:
    """Une capture ATTENDUE. `ancre` dit a quelle section du document elle va."""

    fichier: str
    ancre: str
    montre: str
    portee: str
    profil: str = "obsidian"        # `obsidian`, `nu`, ou `tous`


# L ordre de cette liste est l ordre de lecture du document. Les `ancre:` sont
# des identifiants de section, resolus par `install.py` — pas des titres, qui
# eux dependent du manifeste et changeraient les appels de figure.
CAPTURES: tuple[Capture, ...] = (
    # --- portee KIT : l interface d Obsidian, vraie pour toute instance ------
    Capture("01-obsidian-selecteur-de-coffre.png", "obsidian.ouvrir",
            "l'écran d'accueil d'Obsidian, bouton « Ouvrir un dossier comme "
            "coffre » (Open folder as vault)", KIT),
    Capture("02-obsidian-reglages-general.png", "obsidian.ouvrir",
            "le panneau Paramètres → Général, pour situer la barre de gauche",
            KIT),
    Capture("03-obsidian-mode-restreint.png", "obsidian.modules",
            "Modules complémentaires (Community plugins) avec le mode restreint "
            "ACTIF — l'état de départ d'un coffre neuf", KIT),
    Capture("04-obsidian-modules-actives.png", "obsidian.modules",
            "le même panneau après « Activer les modules complémentaires » : "
            "le bouton Parcourir devient cliquable", KIT),
    Capture("05-obsidian-catalogue.png", "obsidian.plugins",
            "le navigateur de plugins ouvert, barre de recherche vide", KIT),
    Capture("06-plugin-rest-api-recherche.png", "obsidian.plugins",
            "la recherche du plugin de pont agent, avec les résultats "
            "voisins visibles — c'est ce qui permet de ne pas se tromper de "
            "carte", KIT),
    Capture("07-plugin-rest-api-active.png", "obsidian.plugins",
            "la carte du plugin de pont agent après Installer puis Activer",
            KIT),
    Capture("08-plugin-rest-api-options.png", "obsidian.agent",
            "les options du plugin de pont : URL locale et clé d'API, **la clé "
            "masquée** — une clé n'a pas sa place dans un dépôt", KIT),
    Capture("09-plugin-rest-api-mcp.png", "obsidian.agent",
            "la section « How to access via MCP » du plugin, qui donne le bloc "
            "de configuration à coller côté agent", KIT),
    Capture("10-plugins-tous-actives.png", "obsidian.plugins",
            "la liste des modules complémentaires, tous les plugins requis "
            "activés — l'état final attendu de l'étape", KIT),
    Capture("11-templater-reglages.png", "obsidian.gabarits",
            "les réglages de Templater, champ « Template folder location » "
            "vide", KIT),
    Capture("12-templater-dossier-pose.png", "obsidian.gabarits",
            "le même champ renseigné avec le dossier de gabarits du vault", KIT),
    Capture("13-file-hider-options.png", "obsidian.cacher",
            "les options de File Hider, liste des chemins cachés vide", KIT),
    Capture("14-file-hider-menu-contextuel.png", "obsidian.cacher",
            "le menu du clic droit dans l'explorateur, entrée « Hide folder »",
            KIT),
    Capture("15-file-hider-apres.png", "obsidian.cacher",
            "l'explorateur après masquage : l'espace de l'agent a disparu de "
            "la barre latérale", KIT),
    Capture("16-graphe-groupes-reglages.png", "obsidian.couleurs",
            "le panneau du graphe, section Groupes, une requête et sa couleur "
            "en cours de saisie", KIT),
    # Pas de capture d extrait CSS, et c est un retrait du lot 10 : le
    # DevBrain en a un (`.obsidian/snippets/roles.css`, ecrit a la main), mais
    # AUCUN mecanisme du kit ne produit un extrait CSS. Demander la capture
    # d une chose que le kit ne cree pas serait exactement le bruit que ce
    # manifeste existe pour eviter.

    # --- portee INSTANCE : le contenu, faux des la deuxieme instance ---------
    Capture("18-selecteur-dossier-du-vault.png", "obsidian.ouvrir",
            "le sélecteur de dossier pointé sur CE vault — c'est son nom qui "
            "est montré, donc la capture ne se réutilise pas", INSTANCE),
    Capture("19-arbre-du-vault.png", "apercu",
            "la barre latérale, l'arbre des dossiers de l'axe de rangement "
            "déplié sur un niveau", INSTANCE),
    Capture("20-porte-d-entree.png", "apercu",
            "la porte d'entrée du vault ouverte à côté de l'arbre", INSTANCE),
    Capture("21-page-d-unite-proprietes.png", "apercu",
            "une page d'unité en mode lecture, frontmatter déplié — c'est "
            "cette capture qui montre à quoi sert le manifeste", INSTANCE),
    Capture("22-bandeau-genere.png", "apercu",
            "le haut d'une page d'unité, bandeau généré visible, dont une "
            "cellule vide — la règle « un tiret cadratin, jamais une valeur "
            "plausible » se voit là", INSTANCE),
    Capture("23-page-de-vue.png", "apercu",
            "une page de vue : la table filtrée embarquée, et la section "
            "écrite à la main juste en dessous", INSTANCE),
    Capture("24-hub-zone-auto.png", "apercu",
            "un hub, zone générée et corps écrit à la main dans le même "
            "écran", INSTANCE),
    Capture("25-graphe-colore.png", "obsidian.couleurs",
            "le graphe du vault, une couleur par rôle, après application de "
            "la table", INSTANCE),
    Capture("26-verdict-valider.png", "verifier",
            "le terminal, sortie de la commande de validation sur ce vault",
            INSTANCE, profil="tous"),
    Capture("27-verdict-generer-check.png", "verifier",
            "le terminal, sortie du contrôle des artefacts dérivés — code 0",
            INSTANCE, profil="tous"),
    Capture("28-agent-connecte.png", "obsidian.agent",
            "l'agent listant les pages du vault, preuve que le pont répond",
            INSTANCE),
)


def pour(ancre: str, profil: str, portee: str | None = None) -> list[Capture]:
    """Les captures attendues a un endroit du document, pour ce profil."""
    return [c for c in CAPTURES
            if c.ancre == ancre
            and (c.profil == "tous" or c.profil == profil)
            and (portee is None or c.portee == portee)]


def appel(c: Capture, dossier: str) -> list[str]:
    """L appel de figure pose dans le document. Un TROU NOMME, jamais une image.

    Aucune balise `![](...)` : un lien vers un fichier absent afficherait une
    image cassee, ce qui se lit comme un defaut du document plutot que comme un
    travail a faire.
    """
    return [f"> **Capture attendue** — `{dossier}/{c.fichier}` "
            f"({'du kit, réutilisable' if c.portee == KIT else 'DE CETTE INSTANCE'}) : "
            f"{c.montre}.", ""]


def table(profil: str) -> list[str]:
    """Le recapitulatif : ce qu il faudrait photographier, et une seule fois."""
    lot = [c for c in CAPTURES if c.profil in ("tous", profil)]
    kit = [c for c in lot if c.portee == KIT]
    inst = [c for c in lot if c.portee == INSTANCE]
    L = [f"Ce guide appelle **{len(lot)} captures** et n'en embarque aucune. "
         f"Elles se rangent en deux tas, et la coupure décide qui les refait :",
         "",
         f"- **{len(kit)} captures du kit** — elles montrent l'interface "
         f"d'Obsidian et rien du contenu. Prises une fois, elles valent pour "
         f"toutes les instances.",
         f"- **{len(inst)} captures de l'instance** — elles montrent le vault "
         f"lui-même. Elles sont fausses dès la deuxième instance, donc elles se "
         f"reprennent à chaque brain.", "",
         "| Fichier | Portée | Ce qu'elle doit montrer |", "|---|---|---|"]
    for c in lot:
        L.append(f"| `{c.fichier}` | {c.portee} | {c.montre} |")
    L += ["", "**Aucune n'est fabriquée, et c'est délibéré.** Une capture "
          "inventée montrerait une interface qui n'existe pas — strictement "
          "pire qu'un trou nommé. C'est le même raisonnement que la règle du "
          "bandeau : une cellule vide honnêtement vaut mieux qu'une cellule "
          "remplie au jugé.", ""]
    return L
