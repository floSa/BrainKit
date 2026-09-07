# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""brainkit — la porte d entree unique du kit.

    brainkit valider [...]
    brainkit generer [...]
    brainkit semer [...]
    brainkit re-seuiller [...]
    brainkit freeze [...]

Sans sous-commande, la commande dit ce qu elle sait faire et sort en 2. Elle ne
choisit PAS de defaut : valider ne lit rien, generer peut ecrire, semer cree un
vault, et deviner laquelle l utilisateur voulait serait exactement le genre de
defaut qui finit par ecrire quelque part.

Les trois dernieres partagent un module (`brainkit.semer`) et donc un plan
d ecriture unique : c est ce qui rend leurs garde-fous impossibles a contourner
par une commande qui les oublierait.
"""

from __future__ import annotations

import sys
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

# {nom : (module, fonction, aide)}. La fonction est nommee parce que trois
# commandes vivent dans le meme module : elles partagent le plan d ecriture du
# semis, et un module par commande dupliquerait ses garde-fous.
SOUS_COMMANDES = {
    "entretien": ("brainkit.entretien.__main__", "main",
                  "mène l'entretien qui produit un `brain.yml`, puis sème"),
    "valider": ("brainkit.valider.__main__", "main",
                "valide un vault contre son manifeste"),
    "generer": ("brainkit.generer.__main__", "main",
                "régénère les artefacts dérivés (mode `--check` par défaut)"),
    "semer": ("brainkit.semer.__main__", "main",
              "sème une instance vierge (mode lecture par défaut)"),
    "re-seuiller": ("brainkit.semer.__main__", "main_reseuiller",
                    "change le seuil de promotion — une MIGRATION, par `git mv`"),
    "freeze": ("brainkit.semer.__main__", "main_freeze",
               "copie le kit DANS l'instance (livraison on-prem)"),
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
        for nom, (_mod, _fn, aide) in SOUS_COMMANDES.items():
            print(f"  {nom:12s} {aide}")
        return 2
    import importlib
    mod, fonction, _aide = SOUS_COMMANDES[argv[0]]
    module = importlib.import_module(mod)
    sys.argv = [f"brainkit {argv[0]}"] + argv[1:]
    return getattr(module, fonction)()


if __name__ == "__main__":
    raise SystemExit(main())
