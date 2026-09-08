"""etat.py — de ce qu on a SONDE a ce qu on AFFICHE. Cinq etats, fermes par le kit.

Le side-car garde les faits bruts — une date de release, une date de commit, un
drapeau d archivage. L etat en est derive, et c est lui que le bandeau montre et
que la regle confronte. Deux choses valent d etre dites sur ce decoupage.

**Les faits et l etat ne vieillissent pas de la meme facon.** Un fait est vrai
pour toujours : « la derniere release est datee du 2 septembre 2026 » restera
vrai dans dix ans. L etat, lui, est relatif a un seuil et a une date. Les garder
separes permet de rejouer la derivation quand le seuil change, sans redemander
au reseau ce qu on sait deja.

**Les cinq etats ne se confondent pas, et surtout pas les deux silences.**
`jamais_sonde` dit que le side-car ne connait pas la page ; `sans_amont` dit
qu on a regarde et qu il n y a rien a atteindre. Les fondre donnerait un
compteur unique ou « je n ai pas encore travaille » ressemblerait a « il n y a
rien a savoir » — c est la meme faute que « une regle absente ressemble a une
regle satisfaite », transposee a un rapport.

# L ordre des tests EST la regle

  1. jamais sonde       — rien dans le side-car : on ne sait pas, et on le dit ;
  2. archive            — le proprietaire a ferme. Cela prime sur toute date :
                          une release recente d un depot archive ne dit pas que
                          le projet vit, elle date sa derniere respiration ;
  3. une release datee  — c est la trace la plus forte, quelle que soit sa
                          provenance ; la plus RECENTE gagne, parce qu un projet
                          publie parfois sur un registre sans taguer son depot ;
  4. un commit date     — plus faible, et son seuil est donc DISTINCT : un
                          projet stable peut ne pas publier pendant deux ans en
                          recevant des correctifs, l inverse n existe pas ;
  5. sinon              — sans amont atteignable.
"""

from __future__ import annotations

import datetime

# Fermes par le kit. Le manifeste leur donne un LIBELLE (la `table:` de la
# colonne de bandeau) ; il n en ajoute ni n en retire.
ETATS = ("recente", "ancienne", "archive", "sans_amont", "jamais_sonde")

# Les faits datables d un enregistrement, du plus fort au plus faible. Le nom de
# la cle est une convention du side-car, pas un mot de sujet : `release` est ce
# qu une source publie, `commit` ce qu elle bouge.
DATES_DE_PUBLICATION = ("release_le", "registre_le")
DATE_DE_MOUVEMENT = "commit_le"


def _jour(v) -> datetime.date | None:
    try:
        return datetime.date.fromisoformat(str(v)[:10])
    except (TypeError, ValueError):
        return None


def derive(rec: dict | None, amont, aujourdhui: datetime.date | None = None
           ) -> tuple[str, str]:
    """(etat, date affichee) d un enregistrement du side-car.

    La date rendue est celle qui a SERVI a decider — jamais une autre. Afficher
    « à jour » a cote d une date qui n a pas ete comparee au seuil serait une
    cellule qui ment sans mentir.
    """
    aujourdhui = aujourdhui or datetime.date.today()
    if not rec or not rec.get("sonde_le"):
        return "jamais_sonde", ""
    if rec.get("archive"):
        d = (_jour(rec.get("archive_le")) or _jour(rec.get(DATE_DE_MOUVEMENT)))
        return "archive", d.isoformat() if d else ""

    publications = [j for j in (_jour(rec.get(c)) for c in DATES_DE_PUBLICATION) if j]
    if publications:
        d, seuil = max(publications), amont.seuil("release_ancienne_jours")
    else:
        d = _jour(rec.get(DATE_DE_MOUVEMENT))
        seuil = amont.seuil("commit_ancien_jours")
    if d is None:
        return "sans_amont", ""
    age = (aujourdhui - d).days
    return ("ancienne" if age > seuil else "recente"), d.isoformat()


def age_en_jours(rec: dict | None, aujourdhui: datetime.date | None = None
                 ) -> int | None:
    """L age, en jours, de la date qui a decide l etat. None si aucune."""
    aujourdhui = aujourdhui or datetime.date.today()
    d = _jour((rec or {}).get("date"))
    return (aujourdhui - d).days if d else None
