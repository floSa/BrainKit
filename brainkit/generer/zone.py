"""zone.py — LE moteur de zone AUTO, commun aux quatre generateurs.

Une zone AUTO est un bloc de page delimite par deux balises, regenere en bloc,
et jamais edite a la main. Ce module porte le mecanisme et rien du contenu :
trouver la zone, la remplacer, l inserer si elle manque, dire quand elle manque
sans la deviner. Les LIGNES qui vont dedans sont composees par le generateur qui
sait de quoi il parle.

C est le decoupage que l inventaire du cadrage a mesure — I4 « le moteur »
GENERIQUE contre I5 « le contenu » A REECRIRE — et le test a blanc l a
confirme : le bandeau du DevBrain (`Nature | Licence | Execution | Maturite`) et
celui d un brain d histoire (`Nature | Auteur et date | Langue | Fiabilite`)
n ont pas une valeur en commun, et le moteur ne change pas d une ligne.

# Les balises sont declarees, jamais supposees

`bandeau.balises` et `roles[].corps[<AUTO>].balises` les portent. Deux zones AUTO
homonymes dans le meme vault finiraient par se marcher dessus : le DevBrain a
`<!-- AUTO:START -->` dans ses 74 hubs et `<!-- AUTO:BANDEAU:START -->` dans ses
337 fiches, et c est deliberement deux jeux distincts.

# Deux insertions, pas une

  - `remplace()` — la zone existe : remplacement en bloc, le reste de la page
    intact. C est ce qui preserve la zone MANUELLE d un hub (`## Notes`, 13 hubs
    du DevBrain la portent).
  - `applique()` — la zone n existe pas : elle s insere juste sous le titre de
    niveau 1. Une page SANS titre est laissee telle quelle et SIGNALEE. Aucun
    troisieme cas n est devine : la place d une zone dans une page qui n a pas
    de titre n est pas devinable, et l inventer coute une page cassee.

# Le nombre de remplacements n est pas le meme partout, et c est mesure

Le generateur de hubs du DevBrain remplace TOUTES les occurrences de la zone
(`AUTO_RE.sub` sans `count`), celui du bandeau la PREMIERE seulement
(`count=1`). Aucune page du vault n en porte deux, donc la difference ne se voit
pas — mais elle est reproduite telle quelle, parce que le critere du lot est le
`diff` vide et non la ressemblance du code, et parce qu une page a deux zones
est le genre de cas qu on decouvre le jour ou il arrive.
"""

from __future__ import annotations

import re

# Titre de niveau 1 d une page : la seule ancre d insertion connue.
H1_RE = re.compile(r"^# .+$", re.M)

ABSENTE = "aucune zone"
SANS_TITRE = "aucun titre de niveau 1"


def motif(balises: tuple[str, str] | list) -> re.Pattern:
    debut, fin = balises[0], balises[1]
    return re.compile(re.escape(debut) + r".*?" + re.escape(fin), re.S)


def porte_une_zone(texte: str, balises) -> bool:
    return motif(balises).search(texte) is not None


def bloc(balises, corps: str, nl: str = "\n") -> str:
    """La zone complete : la balise d ouverture, le corps, la balise de fermeture."""
    return f"{balises[0]}{nl}{corps}{nl}{balises[1]}"


def remplace(texte: str, balises, zone: str, count: int = 0) -> str | None:
    """La page avec sa zone remplacee, ou None si elle n en porte pas.

    `re.sub` avec un remplacement CALLABLE : une zone qui contient `\\1` ou `\\g`
    — un pitch, un libelle, n importe quel texte du vault — serait sinon
    interpretee comme une reference de groupe et corromprait la page.
    """
    m = motif(balises)
    if not m.search(texte):
        return None
    return m.sub(lambda _: zone, texte, count=count)


def applique(texte: str, balises, zone: str, count: int = 1) -> tuple[str | None, str]:
    """(page a jour, motif) — la page est None quand il n y a rien a faire.

    Le motif dit POURQUOI il n y a rien a faire : la zone est deja exacte (motif
    vide), ou la page n a pas de titre sous lequel l inserer (`SANS_TITRE`). Une
    page sautee est signalee par l appelant, jamais avalee.
    """
    neuf = remplace(texte, balises, zone, count=count)
    if neuf is not None:
        return (None, "") if neuf == texte else (neuf, "")
    m = H1_RE.search(texte)
    if not m:
        return None, SANS_TITRE
    fin = m.end()
    reste = texte[fin:].lstrip("\n")
    return texte[:fin] + "\n\n" + zone + "\n\n" + reste, ""
