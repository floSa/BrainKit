"""temoin.py — OU est le vault temoin, et pourquoi le kit ne le sait pas.

Six jeux d epreuve savent faire une chose que ni `tests/vert/` ni
`tests/genere-vert/` ne peuvent prouver : tourner sur un vault REEL, de plusieurs
centaines de pages, et rendre le meme compte a l unite pres. C est la seule
mesure qui dise qu une regle tient a l echelle.

Ce vault ne vit PAS dans le depot, et le depot ne le nomme pas. Deux raisons, et
la premiere suffit :

  1. le kit est neutre. Un chemin code en dur, meme dans un test, dirait de quel
     sujet le kit est sorti — et un lecteur en conclurait qu il en porte quelque
     chose ;
  2. ce vault appartient a quelqu un. Son emplacement est une donnee de poste,
     pas une donnee de projet.

# Ou le chercher, dans cet ordre

  1. l argument `--vault-temoin <chemin>` ;
  2. la variable d environnement `BRAINKIT_VAULT_TEMOIN` ;
  3. le fichier `.brainkit-local` a la racine du depot — NON SUIVI (gitignore),
     une ligne `vault_temoin=<chemin>` ;
  4. rien. Le scenario est alors SAUTE, et il le dit.

Un scenario saute n est pas un scenario vert : la sortie le distingue, et le
compte de verifications baisse d autant. C est voulu — un jeu d epreuve qui se
tairait sur ce qu il n a pas pu verifier mentirait.

Le manifeste, lui, ne se cherche pas : c est `<vault>/brain.yml`. Le kit
n embarque aucun manifeste d instance.
"""

from __future__ import annotations

import os
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[1]
FICHIER_LOCAL = RACINE_KIT / ".brainkit-local"
VARIABLE = "BRAINKIT_VAULT_TEMOIN"
VARIABLE_ESSAI = "BRAINKIT_VAULT_ESSAI"


def _du_fichier_local(cle_cherchee: str = "vault_temoin") -> Path | None:
    if not FICHIER_LOCAL.is_file():
        return None
    for ligne in FICHIER_LOCAL.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue
        cle, _, valeur = ligne.partition("=")
        if cle.strip() == cle_cherchee and valeur.strip():
            return Path(valeur.strip())
    return None


def resout(argument: Path | None = None) -> Path | None:
    """Le vault temoin, ou None. Jamais un chemin devine."""
    for candidat in (argument,
                     Path(os.environ[VARIABLE]) if os.environ.get(VARIABLE) else None,
                     _du_fichier_local()):
        if candidat is not None and candidat.is_dir():
            return candidat.resolve()
    return None


def resout_essai(argument: Path | None = None) -> Path | None:
    """La PETITE instance reelle — celle qui est sous le plancher de mesure.

    Deuxieme vault, et deuxieme role : le temoin prouve qu une regle tient a
    l echelle ; l essai prouve que le kit REFUSE de durcir sur un corpus trop
    court. Ce sont deux mesures opposees, donc deux vaults.
    """
    valeur = os.environ.get(VARIABLE_ESSAI)
    for candidat in (argument,
                     Path(valeur) if valeur else None,
                     _du_fichier_local("vault_essai")):
        if candidat is not None and (candidat / "brain.yml").is_file():
            return candidat.resolve()
    return None


def pourquoi_saute_essai() -> str:
    return (f"aucune petite instance d'essai — passer `--vault-essai <chemin>`, "
            f"poser `{VARIABLE_ESSAI}`, ou écrire `vault_essai=<chemin>` dans "
            f"`{FICHIER_LOCAL.name}` (non suivi).")


def pourquoi_saute() -> str:
    """La phrase a imprimer quand il n y a pas de temoin. Elle DIT quoi faire."""
    return (f"aucun vault témoin — passer `--vault-temoin <chemin>`, poser "
            f"`{VARIABLE}`, ou écrire `vault_temoin=<chemin>` dans "
            f"`{FICHIER_LOCAL.name}` (non suivi).")
