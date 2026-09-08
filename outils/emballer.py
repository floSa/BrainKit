# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""emballer.py — regenere les documents DU DEPOT DU KIT, et verifie qu ils sont a jour.

    uv run outils/emballer.py              # --check : n ecrit rien, sort en 2 sur ecart
    uv run outils/emballer.py --ecrire

# Pourquoi un outil de depot, et pas une sous-commande

`brainkit <sous-commande>` s adresse a une INSTANCE : valider la sienne, semer
la prochaine, mesurer ses regles. Regenerer les documents du depot du kit
lui-meme n est pas un usage d instance, c est un geste de developpement du kit —
comme `outils/fidelite.py` ou `schema/valider.py`. Le mettre dans la CLI aurait
ajoute une huitieme sous-commande a un lot dont l interdiction est explicite :
*aucun mecanisme nouveau*.

# Ce qu il pose

| Fichier | Genere depuis | Lecteur |
|---|---|---|
| `INSTALL.md` | le kit, sans instance | celui qui n a **aucun** brain |
| `docs/README.md` | ce que `docs/` contient | celui qui ouvre le dossier |
| `docs/histobrain/*` | `exemples/histobrain.brain.yml` | celui qui veut VOIR ce que le semis pose |

Le troisieme tas demande un mot. Les quatre documents d instance sont poses par
le SEMIS, dans l instance — ils n ont rien a faire dans le depot du kit. Sauf
qu un depot qui annonce « le semis pose un INSTALL.md et trois guides » sans
qu on puisse les lire demande de le croire sur parole. Ils sont donc rendus une
fois, depuis le manifeste de demonstration, et clairement etiquetes comme tels :
c est le meme choix que `exemples/histobrain.brain.yml`, pour la meme raison.

# `--check` sort en 2, comme les generateurs

C est la forme verifiable de « ce qui est genere n est jamais edite a la main ».
Le jeu d epreuve du lot 10 l appelle, et un document du depot qui aurait ete
retouche a la main fait echouer le lot — pas une relecture humaine.
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

#: Le manifeste de demonstration dont les guides sont rendus dans `docs/`.
#: HistoBrain et pas DevBrain, et ce n est pas un hasard : le kit doit se
#: montrer sur le sujet le plus ELOIGNE de celui dont il est extrait.
DEMONSTRATION = "histobrain"
SOUS_DOSSIER = f"docs/{DEMONSTRATION}"


def _readme_des_docs(nom_demo: str, fichiers: list[str]) -> str:
    return "\n".join([
        "# `docs/` — les documents générés du kit", "",
        "> **Dossier GÉNÉRÉ** par `uv run outils/emballer.py --ecrire`. Ne rien "
        "éditer à la main ici : tout se régénère depuis le code du kit et depuis "
        "un manifeste.", "",
        "## Ce que tu cherches probablement", "",
        "| Tu veux | Va voir |", "|---|---|",
        "| installer le kit et créer un brain | `../INSTALL.md`, à la racine du dépôt |",
        f"| **voir** ce que le semis pose dans une instance | `{DEMONSTRATION}/` |",
        "| comprendre les décisions de conception | `../design/`, lot par lot |", "",
        f"## `{DEMONSTRATION}/` — les documents d'une instance, rendus une fois",
        "",
        f"Une instance porte **ses** documents, écrits par `brainkit semer` "
        f"depuis **son** manifeste. Ils n'ont donc rien à faire dans le dépôt du "
        f"kit — sauf qu'un dépôt qui annonce « le semis pose un guide "
        f"d'installation et trois guides d'usage » sans qu'on puisse les lire "
        f"demande de le croire sur parole.", "",
        f"Ceux-ci sont rendus depuis `exemples/{DEMONSTRATION}.brain.yml`, le "
        f"manifeste de démonstration — un brain d'**histoire**, choisi parce "
        f"que c'est le sujet le plus éloigné de celui dont le kit a été "
        f"extrait. Un brain de développement logiciel aurait laissé planer le "
        f"doute.", "",
        "| Fichier | Ce que c'est |", "|---|---|"] + [
        f"| `{DEMONSTRATION}/{f}` | " + {
            "INSTALL.md": "installer **cette instance** sur une machine neuve",
            "manuel.md": "lire le brain — ce qu'on a sous les yeux",
            "enrichir.md": "écrire dedans, et ce que ça déclenche autour",
            "exploiter.md": "s'en servir depuis un travail, sans y écrire",
        }.get(Path(f).name, "—") + " |"
        for f in fichiers] + [
        "", "> Ce sont des documents d'**exemple**. Ton instance porte les "
        "siens, avec tes mots, tes axes et tes règles — et si les deux se "
        "ressemblent quelque part, c'est que cet endroit-là est vraiment "
        "générique.", ""])


def documents() -> dict[str, str]:
    """{chemin relatif au depot : contenu} — tout ce que cet outil pose."""
    out: dict[str, str] = dict(emballer.rendus_du_kit())
    mo = charge(RACINE_KIT / "exemples" / f"{DEMONSTRATION}.brain.yml")
    rendus = emballer.rendus(mo)
    for chemin, texte in rendus.items():
        out[f"{SOUS_DOSSIER}/{Path(chemin).name}"] = texte
    out["docs/README.md"] = _readme_des_docs(
        DEMONSTRATION, sorted(Path(c).name for c in rendus))
    return out


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(
        description="Régénère les documents du dépôt du kit depuis le manifeste.")
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
        print(f"{len(ecarts)} écart(s) — les documents du dépôt ne sont plus "
              f"ceux que le kit génère :")
        for e in ecarts:
            print(f"  [ÉCART] {e}")
        print("\nRelancer avec `--ecrire`. Un document généré ne s'édite pas à "
              "la main : deux sources qui décrivent la même chose divergent.")
        return 2
    print(f"OK — les {len(lot)} documents du dépôt concordent avec ce que le "
          f"kit génère.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
