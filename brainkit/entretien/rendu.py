"""rendu.py — le manifeste compose, rendu en YAML LISIBLE.

Un `brain.yml` se relit a six mois. Ce qui le rend relisable n est pas la
syntaxe, ce sont les `motif:` — et un dump par defaut les rend en une seule
ligne de trois cents caracteres, ce qui revient a les perdre.

Deux dispositions, et rien de plus :

  1. **les longues chaines sortent en bloc litteral** (`|-`), pliees a 78
     colonnes. C est la seule facon qu un `motif:` reste lisible dans un
     editeur, dans un `git diff` et dans une revue ;
  2. **un en-tete de commentaires** dit d ou vient le fichier, quelle question a
     produit quoi, et ce que l entretien a REFUSE de deviner. C est la premiere
     chose que quelqu un lira en ouvrant l instance.

L ordre des cles est celui du composeur, jamais alphabetique : il suit l ordre
des passes, donc l ordre dans lequel les reponses ont ete donnees.
"""

from __future__ import annotations

import textwrap
from typing import Any

import yaml

from .passes import PASSES, QUESTIONS
from .refus import LES_TREIZE

LARGEUR = 78


class _Vidangeur(yaml.SafeDumper):
    """Un dumper qui garde l ordre et plie les longues chaines."""


def _str(dumper: yaml.SafeDumper, data: str):
    if "\n" in data or len(data) > 88:
        plie = "\n".join(textwrap.fill(p, LARGEUR) for p in data.split("\n"))
        return dumper.represent_scalar("tag:yaml.org,2002:str", plie, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_Vidangeur.add_representer(str, _str)


def entete(m: dict, brouillon: str = "") -> str:
    """Le bandeau de commentaires en tete du `brain.yml`."""
    nom = (m.get("brain") or {}).get("nom") or "?"
    sujet = (m.get("brain") or {}).get("sujet") or ""
    L = [
        "# " + "=" * 76,
        f"# {nom}/brain.yml — le manifeste de ce brain.",
        "# " + "-" * 76,
        f"# Sujet : {sujet}",
        "#",
        "# ÉCRIT PAR L'ENTRETIEN. Ce fichier n'a pas été rempli à la main et il",
        "# n'a été copié d'aucun autre brain : il est la transcription de "
        f"{len(PASSES)}",
        f"# passes et de {len(QUESTIONS)} questions. Chaque valeur vient d'une",
        "# réponse, ou se DÉRIVE d'une réponse — rien n'y a été deviné.",
        "#",
        "# Ce que l'entretien a refusé de deviner, et qu'il a redemandé :",
    ]
    for r in LES_TREIZE:
        L.append(f"#   {r.n:2d}. {r.objet}  (question {r.question})")
    L += [
        "#",
        "# Les dix règles sortent TOUTES en `a_mesurer`, sans exception. Porter",
        "# une sévérité, c'est porter une mesure qu'on n'a pas faite ; le brain",
        "# les durcira quand il aura des pages à mesurer.",
        "#",
        "# Ce fichier se modifie à la main, mais deux choses ne se modifient pas",
        "# sans conséquence : `axes.rangement.seuil_promotion` (changer le seuil",
        "# RÉFORME l'arbre — passer par `brainkit re-seuiller`), et les valeurs",
        "# de l'axe de rangement (une valeur retirée laisse des pages orphelines).",
    ]
    if brouillon:
        L += ["#",
              f"# Les réponses qui l'ont produit : {brouillon}"]
    L += ["# " + "=" * 76, ""]
    return "\n".join(L)


def rendu(m: dict, brouillon: str = "") -> str:
    corps = yaml.dump(m, Dumper=_Vidangeur, allow_unicode=True,
                      sort_keys=False, default_flow_style=False, width=88,
                      indent=2)
    return entete(m, brouillon) + corps


def ecrit(m: dict, chemin, brouillon: str = ""):
    from pathlib import Path
    p = Path(chemin)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="\n") as f:
        f.write(rendu(m, brouillon))
    return p


def _sans_none(o: Any) -> Any:
    """Les `None` d un dict compose ne se serialisent pas en YAML utile.

    Un `champ: null` EST porteur de sens dans ce manifeste (une section de
    liste de liens qui n est adossee a aucun champ), donc on ne les supprime
    pas partout : seulement dans les listes, ou ils ne veulent rien dire.
    """
    if isinstance(o, dict):
        return {k: _sans_none(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_sans_none(x) for x in o if x is not None]
    return o
