# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""captures.py — le CONTROLE DU MANIFESTE D IMAGES, dans les deux sens.

    uv run outils/captures.py              # code 0 si tout concorde, 2 sinon
    uv run outils/captures.py --liste      # imprime en plus ce qui reste a prendre

# La remontee que cet outil ferme

Le lot 10 avait releve, en remontee 8, que le manifeste d images ne se verifiait
pas :

  > Le jeu d epreuve controle qu aucune image n est embarquee. Il ne controle pas
  > l inverse : le jour ou les captures de portee kit existeront, rien ne dira
  > qu une capture declaree manque sur le disque, ni qu un fichier pose sous
  > `docs/img/` n est declare par personne.

C est exactement ce que cet outil fait, et il tourne dans les DEUX SENS parce
qu un seul sens ne suffit pas :

  - une image REFEREE qui manque sur le disque casse le rendu du document. Un
    lecteur voit une image brisee, ce qui se lit comme un defaut du document ;
  - une image POSEE que personne ne refere est un fichier mort. Elle grossit le
    depot, elle vieillit sans qu on le voie, et le jour ou on la retrouve on ne
    sait plus si elle est juste.

# Les trois etats d une capture, et pourquoi ils sont distincts

| Etat | Forme dans le document | Ce que l outil exige |
|---|---|---|
| **presente** | une balise d image `![alt](img/NN-nom.png)` | le fichier existe |
| **a prendre** | un bloc en citation `> **Capture à prendre en séance** — \\`img/NN-nom.png\\`` | le fichier n existe PAS encore |
| **orpheline** | rien | refus : le fichier existe et personne ne le nomme |

La deuxieme ligne est le coeur du dispositif, et elle vient du lot 10 : une
capture absente s ecrit comme un TROU NOMME, pas comme une balise cassee. Une
balise vers un fichier absent afficherait une image brisee ; un bloc en citation
qui dit quoi photographier se lit comme un travail a faire.

Et le controle a un troisieme effet, celui qui rattrape la DERIVE : si un fichier
« a prendre » finit par exister sur le disque, c est que la seance a eu lieu et
que personne n a converti le trou nomme en balise d image. L outil le signale.

# Le rapport avec `brainkit/emballer/images.py`

Ce module-la declare les captures d UNE INSTANCE — 27, dont 16 de portee `kit`.
La doc du kit, elle, en refere ses propres. Les deux ensembles se recoupent sans
se confondre, et l outil verifie donc aussi la troisieme direction :

  - chaque capture de portee `kit` du manifeste d instance est-elle soit presente
    dans `docs/img/`, soit nommee « a prendre » dans la doc du kit ?

Une capture de portee `instance` n a rien a faire dans ce controle : par
construction elle est refaite a chaque brain. Elle apparait dans la doc du kit
comme illustration d un vault de demonstration, ce qui est un usage legitime, pas
une declaration.

# Ce que cet outil ne fait PAS

Il ne regarde pas le CONTENU d une image. Il ne peut donc pas dire qu une cle
d API y est visible : c est une relecture humaine, et le protocole de prise
(`design/12-captures.md`) en fait sa premiere consigne.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

DOSSIER_DOC = "docs"
DOSSIER_IMG = "docs/img"
EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg")

#: Une balise d image markdown : `![texte](chemin)`. Le chemin est relatif au
#: document, et tous les documents de `docs/` sont a plat, donc `img/...`.
BALISE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")

#: Un TROU NOMME. La forme est fixee, et c est volontaire : un controle qui
#: accepterait n importe quelle phrase ne pourrait pas distinguer une capture
#: promise d une capture evoquee en passant.
TROU = re.compile(r"\*\*Captures?\s+à\s+prendre\s+en\s+séance\*\*\s*—\s*`([^`]+)`")


def _documents() -> list[Path]:
    """Les documents de la doc DU KIT — `docs/` plus le README de la racine."""
    out = sorted((RACINE_KIT / DOSSIER_DOC).rglob("*.md"))
    racine = RACINE_KIT / "README.md"
    if racine.is_file():
        out.append(racine)
    return out


def _relatif(doc: Path, cible: str) -> Path:
    return (doc.parent / cible).resolve()


def releve() -> tuple[dict[str, list[str]], dict[str, list[str]], set[Path]]:
    """(images referees, trous nommes, fichiers presents).

    Les deux premiers sont {chemin resolu POSIX : [documents qui le citent]}.
    """
    referees: dict[str, list[str]] = {}
    trous: dict[str, list[str]] = {}
    for doc in _documents():
        texte = doc.read_text(encoding="utf-8")
        nom = doc.relative_to(RACINE_KIT).as_posix()
        for cible in BALISE.findall(texte):
            if cible.startswith(("http://", "https://", "data:")):
                continue        # un badge de bandeau : hors du dossier d images
            referees.setdefault(_relatif(doc, cible).as_posix(), []).append(nom)
        for cible in TROU.findall(texte):
            trous.setdefault(_relatif(doc, cible).as_posix(), []).append(nom)
    presents = {p.resolve() for p in (RACINE_KIT / DOSSIER_IMG).iterdir()
                if p.is_file() and p.suffix.lower() in EXTENSIONS} \
        if (RACINE_KIT / DOSSIER_IMG).is_dir() else set()
    return referees, trous, presents


def declarees_du_kit() -> dict[str, str]:
    """{nom de fichier : ce qu elle doit montrer} — les captures de portee KIT.

    Lues dans `brainkit/emballer/images.py`, qui est le manifeste d images d une
    INSTANCE. On n en garde que la portee `kit` : ce sont les seules qui, par
    construction, ne dependent d aucun sujet et valent donc pour la doc du kit.
    """
    from brainkit.emballer import images
    return {c.fichier: c.montre for c in images.CAPTURES
            if c.portee == images.KIT}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(
        description="Vérifie le manifeste d'images de la doc du kit, "
                    "dans les deux sens.")
    ap.add_argument("--liste", action="store_true",
                    help="imprimer aussi ce qui reste à prendre en séance")
    ns = ap.parse_args()

    referees, trous, presents = releve()
    noms_presents = {Path(p).name for p in map(str, presents)}
    fautes: list[str] = []

    # --- sens 1 : une image REFEREE doit exister ---------------------------
    manquantes = sorted(c for c in referees if Path(c) not in presents)
    for chemin in manquantes:
        citee = ", ".join(sorted(set(referees[chemin])))
        fautes.append(f"MANQUE      {Path(chemin).name} — référée par {citee}")

    # --- sens 2 : une image POSEE doit etre referee ------------------------
    attendus = set(referees) | set(trous)
    orphelines = sorted(p.as_posix() for p in presents
                        if p.as_posix() not in attendus)
    for chemin in orphelines:
        fautes.append(f"ORPHELINE   {Path(chemin).name} — aucun document "
                      f"ne la réfère")

    # --- sens 3 : un TROU NOMME ne doit PAS encore exister -----------------
    # Si le fichier est la, la seance a eu lieu et le trou nomme n a pas ete
    # converti en balise d image. Le document dit alors « a prendre » d une
    # capture qui est prise : c est exactement la derive que ce controle attrape.
    prises = sorted(c for c in trous if Path(c) in presents)
    for chemin in prises:
        citee = ", ".join(sorted(set(trous[chemin])))
        fautes.append(f"À CONVERTIR {Path(chemin).name} — le fichier existe, "
                      f"mais {citee} l'annonce encore comme « à prendre »")

    # --- sens 4 : les captures de portee KIT du manifeste d instance -------
    declarees = declarees_du_kit()
    noms_trous = {Path(c).name for c in trous}
    ignorees = sorted(f for f in declarees
                      if f not in noms_presents and f not in noms_trous)

    print("=== la doc du kit et ses images ===")
    print(f"  {len(referees):3d} image(s) référée(s) par une balise")
    print(f"  {len(trous):3d} capture(s) nommée(s) « à prendre en séance »")
    print(f"  {len(presents):3d} fichier(s) dans {DOSSIER_IMG}/")
    print()
    print("=== les captures de portée kit du manifeste d'instance ===")
    print(f"  {len(declarees):3d} déclarée(s) dans brainkit/emballer/images.py")
    print(f"  {len(declarees) - len(ignorees):3d} couverte(s) par la doc du kit "
          f"(présente ou nommée à prendre)")
    if ignorees:
        print(f"  {len(ignorees):3d} déclarée(s) et non couverte(s) — "
              f"AVERTISSEMENT, pas une faute :")
        for f in ignorees:
            print(f"      {f} — {declarees[f]}")
        print("      Une capture déclarée pour une instance peut légitimement "
              "ne pas illustrer\n      la doc du kit. Ce qui serait une faute, "
              "c'est de l'oublier en silence.")
    print()

    if ns.liste and trous:
        print("=== à prendre en séance ===")
        for chemin in sorted(trous):
            citee = ", ".join(sorted(set(trous[chemin])))
            print(f"  {Path(chemin).name:44s} {citee}")
        print("\n  Le protocole de prise : design/12-captures.md")
        print()

    if fautes:
        print(f"{len(fautes)} écart(s) :")
        for f in fautes:
            print(f"  [ÉCART] {f}")
        print("\nRappel : une capture absente s'écrit comme un TROU NOMMÉ, "
              "jamais comme une\nbalise d'image — un lien vers un fichier "
              "absent affiche une image brisée.")
        return 2

    print("OK — aucune image référée ne manque, aucune image posée n'est "
          "orpheline.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
