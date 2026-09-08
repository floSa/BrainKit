# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""emballer.py — rend les documents D UNE INSTANCE en exemple, et verifie qu ils sont a jour.

    uv run outils/emballer.py              # --check : n ecrit rien, sort en 2 sur ecart
    uv run outils/emballer.py --ecrire

# Pourquoi un outil de depot, et pas une sous-commande

`brainkit <sous-commande>` s adresse a une INSTANCE : valider la sienne, semer
la prochaine, mesurer ses regles. Rendre en exemple les documents d une instance
de demonstration n est pas un usage d instance, c est un geste de developpement
du kit — comme `outils/fidelite.py`, `outils/captures.py` ou `schema/valider.py`.

# Ce qu il pose, et ce qu il ne pose PLUS

| Fichier | Genere depuis | Lecteur |
|---|---|---|
| `exemples/rendu-histobrain/*` | `exemples/histobrain.brain.yml` | celui qui veut VOIR ce que le semis pose |

Les quatre documents d instance sont poses par le SEMIS, dans l instance — ils
n ont rien a faire dans le depot du kit. Sauf qu un depot qui annonce « le semis
pose un INSTALL.md et trois guides » sans qu on puisse les lire demande de le
croire sur parole. Ils sont donc rendus une fois, depuis le manifeste de
demonstration, et clairement etiquetes comme tels : c est le meme choix que
`exemples/histobrain.brain.yml`, pour la meme raison.

**Ce qu il ne pose plus** : l `INSTALL.md` du DEPOT DU KIT, et le `docs/README.md`.
Les deux etaient generes, et les deux etaient de la DOC DU KIT — une nature
differente de la doc d une instance :

  - la doc d une instance nomme SES roles, SES axes, SES skills. Elle depend d un
    manifeste, donc elle se genere, et l editer a la main la ferait divergerdu
    manifeste. C est le constat E4, mesure dans le vault d origine ;
  - la doc du kit ne nomme aucun sujet et ne lit AUCUN manifeste. L `INSTALL.md`
    du depot etait donc de la prose ecrite en Python — plus dure a modifier qu un
    fichier markdown, et surtout INCAPABLE DE PORTER UNE IMAGE, puisque le
    generateur interdit (a raison) toute balise d image.

La doc du kit est desormais ecrite a la main dans `docs/`, et elle porte ses
captures. Le contrat « ce qui est genere n est jamais edite a la main » ne perd
rien : il ne portait sur ce fichier que par accident de fabrication.

# `--check` sort en 2, comme les generateurs

C est la forme verifiable du contrat. Le jeu d epreuve du lot 10 l appelle, et
un document rendu qui aurait ete retouche a la main fait echouer le lot — pas une
relecture humaine.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit import emballer                              # noqa: E402
from brainkit.valider import charge                        # noqa: E402

#: Le manifeste de demonstration dont les guides sont rendus.
#: HistoBrain et pas DevBrain, et ce n est pas un hasard : le kit doit se
#: montrer sur le sujet le plus ELOIGNE de celui dont il est extrait.
DEMONSTRATION = "histobrain"
SOUS_DOSSIER = f"exemples/rendu-{DEMONSTRATION}"


def documents() -> dict[str, str]:
    """{chemin relatif au depot : contenu} — tout ce que cet outil pose."""
    mo = charge(RACINE_KIT / "exemples" / f"{DEMONSTRATION}.brain.yml")
    return {f"{SOUS_DOSSIER}/{Path(chemin).name}": texte
            for chemin, texte in emballer.rendus(mo).items()}


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(
        description="Rend les documents d'une instance de démonstration, "
                    "et vérifie qu'ils sont à jour.")
    ap.add_argument("--ecrire", action="store_true",
                    help="écrire pour de bon (le défaut n'écrit rien)")
    ns = ap.parse_args()

    lot = documents()
    ecarts: list[str] = []
    ecrits: list[str] = []
    for chemin, texte in sorted(lot.items()):
        cible = RACINE_KIT / chemin
        actuel = cible.read_text(encoding="utf-8") if cible.is_file() else None
        etat = "identique" if actuel == texte else (
            "à poser" if actuel is None else "à rafraîchir")
        if etat != "identique":
            ecarts.append(f"{chemin} — {etat}")
            if ns.ecrire:
                cible.parent.mkdir(parents=True, exist_ok=True)
                # LF, comme partout : le depot est lu sur trois systemes.
                with cible.open("w", encoding="utf-8", newline="\n") as f:
                    f.write(texte)
                ecrits.append(chemin)
        print(f"  {etat:12s} {chemin}  ({len(texte.splitlines())} ligne(s))")

    print()
    if ns.ecrire:
        print(f"OK — {len(ecrits)} document(s) écrit(s), "
              f"{len(lot) - len(ecrits)} déjà à jour.")
        return 0
    if ecarts:
        print(f"{len(ecarts)} écart(s) — les documents rendus ne sont plus "
              f"ceux que le kit génère :")
        for e in ecarts:
            print(f"  [ÉCART] {e}")
        print("\nRelancer avec `--ecrire`. Un document généré ne s'édite pas à "
              "la main : deux sources qui décrivent la même chose divergent.")
        return 2
    print(f"OK — les {len(lot)} documents rendus concordent avec ce que le "
          f"kit génère.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
