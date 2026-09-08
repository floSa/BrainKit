"""contrat.py — QUELLE version du contrat, QUELLE version du kit. Dans les deux sens.

# Le trou que ce module ferme

Remontee 6 du lot 5, renvoyee ici : *« le semis lit `kit.version` pour l ecrire
dans `AI/scripts/README.md`, mais il ne la COMPARE a rien »*. Le cadrage, lui,
l ecrit noir sur blanc (§5.1) :

  > `brain.yml` porte la version du kit avec laquelle l instance a ete generee.
  > Le kit refuse de tourner sur un manifeste d une version qu il ne connait
  > pas, **dans les deux sens**.

« Dans les deux sens » est le point : un kit ancien devant un manifeste neuf est
aussi dangereux qu un kit neuf devant un manifeste ancien. Le premier ignore en
silence des declarations qu il ne sait pas lire ; le second applique des defauts
a des champs qui ont change de sens. Aucun des deux ne se signale tout seul.

# Deux versions, et elles ne disent pas la meme chose

| Ce qui est compare | A quoi | Ce qu une divergence veut dire |
|---|---|---|
| `manifeste:` | `CONTRAT` | le FORMAT du fichier a change — les champs ne sont plus les memes |
| `kit.version` | `__version__` du paquet | le CODE a change — les memes champs, un autre comportement |

La premiere est une rupture de contrat : on refuse, sans nuance. La seconde se
gradue, et la graduation est celle du versionnement semantique tel que le kit le
pratique en `0.x` — c est le MINEUR qui porte la rupture, le correctif ne la
porte jamais :

  - majeur ou mineur different  -> **REFUS**. Le code et le manifeste ne se
    comprennent pas, et un verdict rendu par un code qu on n a pas choisi est
    pire qu une absence de verdict (meme raisonnement que `defauts.py`) ;
  - correctif different         -> on le **DIT**, et on tourne. Un correctif ne
    change ni le format ni le sens ; se taire ferait perdre la seule trace de
    « cette instance a ete semee par un kit plus ancien » ;
  - bloc `kit:` absent          -> **rien**. Le bloc est facultatif au contrat
    (§2.2), et un manifeste ecrit a la main a le droit de ne pas l avoir. Se
    plaindre d une declaration facultative serait exiger ce que le schema
    n exige pas.

# Pourquoi ce controle vit dans `charge()`, et nulle part ailleurs

`brainkit.valider.charge()` est le seul entonnoir : les sept sous-commandes en
passent par lui, les ponts d instance aussi. Poser le controle dans chaque
`__main__` aurait donne sept endroits a tenir a jour, donc six oublis en
puissance — c est le constat E4 du cadrage applique a un controle plutot qu a un
gabarit.

Le refus prend la forme d un `SystemExit(2)`. C est brutal pour une fonction de
chargement, et c est voulu : une version inconnue n est pas une donnee douteuse
dont on pourrait faire quelque chose, c est un contrat absent. La seule reponse
juste est de ne pas tourner. `charge(..., controle=False)` existe pour le jeu
d epreuve, qui doit pouvoir observer le refus sans le subir.
"""

from __future__ import annotations

import re

RE_SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

# La version du CONTRAT que ce kit sait lire. Le schema la fixe a `const: 1` ;
# elle est reprise ici parce que le schema n est pas embarque dans une instance
# figee (`freeze` ne copie pas `schema/`), et qu un controle qui ne tourne que
# la ou le schema est present ne tourne pas la ou il sert le plus.
CONTRAT = 1


def _triplet(v: str) -> tuple[int, int, int] | None:
    m = RE_SEMVER.match(str(v).strip())
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None


def controle(m: dict) -> tuple[list[str], bool]:
    """(ce qu il faut DIRE, faut-il REFUSER de tourner).

    `m` est le manifeste brut, pas un `Modele` : le controle doit pouvoir se
    rendre AVANT que le modele existe, puisqu il decide si le modele a un sens.
    """
    from . import __version__

    dits: list[str] = []
    version_du_kit = _triplet(__version__)

    # --- le contrat -------------------------------------------------------
    brut = m.get("manifeste")
    if brut is None:
        return ([f"refus — le manifeste ne declare pas sa version. "
                 f"`manifeste: {CONTRAT}` est le premier champ du contrat : "
                 f"sans lui, rien ne dit quel format ce fichier suit."], True)
    try:
        pose = int(brut)
    except (TypeError, ValueError):
        return ([f"refus — `manifeste: {brut!r}` n'est pas un entier. "
                 f"Ce kit lit le contrat `{CONTRAT}`."], True)
    if pose != CONTRAT:
        sens = ("plus RÉCENT que ce kit — des déclarations qu'il ne sait pas "
                "lire seraient ignorées en silence" if pose > CONTRAT else
                "plus ANCIEN que ce kit — des champs ont changé de sens depuis")
        return ([f"refus — `manifeste: {pose}`, et ce kit lit le contrat "
                 f"`{CONTRAT}`. Le manifeste est {sens}.",
                 "    Un contrat ne se devine pas : mettre le manifeste à jour, "
                 "ou prendre le kit de sa génération."], True)

    # --- le kit -----------------------------------------------------------
    kit = m.get("kit") or {}
    declaree = kit.get("version")
    if not declaree:
        return (dits, False)                # bloc facultatif : rien a dire
    pose_kit = _triplet(str(declaree))
    if pose_kit is None:
        return ([f"refus — `kit.version: {declaree!r}` n'est pas une version "
                 f"sémantique `<majeur>.<mineur>.<correctif>`."], True)
    if version_du_kit is None:              # pragma: no cover — garde de dev
        return ([f"refus — la version du paquet (`{__version__}`) n'est pas "
                 f"sémantique. C'est un défaut du kit, pas du manifeste."], True)

    if pose_kit[:2] != version_du_kit[:2]:
        quoi = ("plus RÉCENT que ce kit" if pose_kit[:2] > version_du_kit[:2]
                else "plus ANCIEN que ce kit")
        mode = str(kit.get("mode") or "branche")
        L = [f"refus — l'instance déclare `kit.version: {declaree}` et ce kit "
             f"est `{__version__}` : le manifeste est {quoi}, sur le chiffre "
             f"qui porte les ruptures (le mineur).",
             "    Le kit refuse de tourner sur une version qu'il ne connaît "
             "pas, dans les deux sens : un verdict rendu par un code qu'on n'a "
             "pas choisi est pire qu'une absence de verdict."]
        if mode == "fige":
            L.append("    Cette instance est FIGÉE : son code est dans "
                     "`AI/scripts/brainkit/`, et c'est celui-là qu'il faut "
                     "lancer (`uv run AI/scripts/valider.py`). Cf. "
                     "`AI/scripts/FIGE.md`.")
        else:
            L.append("    Deux issues : prendre le kit de la génération de "
                     "l'instance, ou migrer l'instance — et une migration de "
                     "manifeste se lit dans les notes de version du kit, elle "
                     "ne s'improvise pas.")
        return (L, True)

    if pose_kit != version_du_kit:
        dits.append(
            f"note — l'instance a été semée par BrainKit `{declaree}` et ce kit "
            f"est `{__version__}`. Même mineur, donc même contrat et même "
            f"comportement : la différence est un correctif, et elle est dite "
            f"plutôt que passée sous silence.")
    return (dits, False)
