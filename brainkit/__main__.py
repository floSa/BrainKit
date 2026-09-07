# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""brainkit — la porte d entree unique du kit.

    brainkit valider [...]
    brainkit generer [...]

Sans sous-commande, la commande dit ce qu elle sait faire et sort en 2. Elle ne
choisit PAS de defaut : valider ne lit rien, generer peut ecrire, et deviner
laquelle des deux l utilisateur voulait serait exactement le genre de defaut qui
finit par ecrire dans un vault.
"""

from __future__ import annotations

import sys
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

SOUS_COMMANDES = {
    "valider": ("brainkit.valider.__main__", "valide un vault contre son manifeste"),
    "generer": ("brainkit.generer.__main__", "régénère les artefacts dérivés "
                                             "(mode `--check` par défaut)"),
}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help") or argv[0] not in SOUS_COMMANDES:
        if argv and argv[0] not in ("-h", "--help"):
            print(f"sous-commande inconnue : {argv[0]}")
        print("usage : brainkit <sous-commande> [options]\n")
        for nom, (_mod, aide) in SOUS_COMMANDES.items():
            print(f"  {nom:9s} {aide}")
        return 2
    import importlib
    module = importlib.import_module(SOUS_COMMANDES[argv[0]][0])
    sys.argv = [f"brainkit {argv[0]}"] + argv[1:]
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
