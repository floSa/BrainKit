"""depot.py — le depot git de l instance : identite LOCALE, trois hooks, premier commit.

# L identite ne se devine JAMAIS, et surtout pas ici

C est le refus n° 1 de l entretien (§3.5), et c est le seul endroit du kit qui
puisse le violer. Trois interdits, tenus par construction :

  - la commande de commit est NUE — pas de `-c user.email`, pas de `--author` ;
  - l environnement n est pas touche — ni `GIT_AUTHOR_EMAIL`, ni
    `GIT_COMMITTER_EMAIL` ;
  - l identite vient de `git.identite` du MANIFESTE, jamais d une config globale,
    jamais d une variable d environnement, jamais de ce que l outil qui lance le
    kit croit savoir de l utilisateur.

Verifiable :

    grep -rnE "GIT_AUTHOR|GIT_COMMITTER|--author|-c user\\." brainkit/semer/
    # -> uniquement les mentions de ce docstring et les hooks generes

# `core.hooksPath` est pose par le semis, pas laisse a l installation

Les hooks du DevBrain sont versionnes mais leur activation est manuelle
(`INSTALL.md` §3.5), et le lot 6 de sa migration a mesure ce que ca coûte : cinq
commits passes parce que rien ne cherchait. Une instance neuve n a aucune raison
de naitre avec ses garde-fous eteints — le semis les allume, et le premier commit
les traverse. Ce commit EST le test.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from ..valider.manifeste import Modele
from . import hooks as _hooks
from .plan import Plan

GITIGNORE = """\
# Le poste de travail Obsidian, pas le brain.
.obsidian/workspace*.json
.obsidian/cache
.trash/

# Bytecode Python — une instance figee porte du code, et il ne se versionne pas.
__pycache__/
*.py[cod]

# Arbres de travail des generateurs : la piece a conviction d une execution,
# jamais un livrable.
travail/
"""

GITATTRIBUTES = """\
# Les hooks sont interpretes par /bin/sh : jamais de CRLF, il casse le shebang.
.githooks/* text eol=lf
"""


@dataclass
class Depot:
    """Ce que le semis a fait — ou aurait fait — au depot de l instance."""

    etapes: list[str] = field(default_factory=list)
    echecs: list[str] = field(default_factory=list)
    commit: str | None = None

    @property
    def ok(self) -> bool:
        return not self.echecs


def seme_les_hooks(mo: Modele, plan: Plan) -> None:
    """Les trois hooks, plus `.gitignore` et `.gitattributes`."""
    git = mo.m.get("git") or {}
    identite = git.get("identite") or {}
    rendus = _hooks.rendus(
        brain=str(mo.brain.get("nom") or ""),
        nom=str(identite.get("name") or ""),
        email=str(identite.get("email") or ""),
        domaines=[str(d) for d in (git.get("domaines_refuses") or [])],
        trailers=[str(t) for t in (git.get("trailers_refuses") or [])],
    )
    for fichier, texte in sorted(rendus.items()):
        plan.pose(f".githooks/{fichier}", texte, "hooks")
    plan.pose(".gitignore", GITIGNORE, "hooks")
    plan.pose(".gitattributes", GITATTRIBUTES, "hooks")


# --------------------------------------------------------------------------- #
def _git(racine: Path, *args: str, entree: str | None = None) -> tuple[int, str]:
    p = subprocess.run(["git", "-C", str(racine), *args],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", input=entree)
    return p.returncode, (p.stdout + p.stderr).strip()


def initialise(mo: Modele, racine: Path, message: str | None = None,
               ecrire: bool = False) -> Depot:
    """`git init`, identite LOCALE, `core.hooksPath`, premier commit.

    En mode lecture (`ecrire=False`), rend la liste des commandes SANS en lancer
    une seule — un semis qu on lance pour voir ne doit pas creer de depot.
    """
    d = Depot()
    git = mo.m.get("git") or {}
    identite = git.get("identite") or {}
    branche = str(git.get("branche_principale") or "main")
    nom = str(identite.get("name") or "")
    email = str(identite.get("email") or "")
    if not nom or not email:
        d.echecs.append("`git.identite` incomplète — le dépôt ne sera pas créé. "
                        "L'identité ne se devine jamais.")
        return d

    message = message or (f"semis : {mo.brain.get('nom')} — l'instance vierge, "
                          f"un hub par dossier")

    commandes: list[list[str]] = [
        ["init", "-b", branche],
        # LOCAL, et rien d autre. Une identite globale ne suffit pas : elle
        # change avec la machine, et c est exactement ce qu on refuse.
        ["config", "--local", "user.name", nom],
        ["config", "--local", "user.email", email],
        ["config", "--local", "core.hooksPath", ".githooks"],
        ["add", "-A"],
        # Commit NU : git lit la config locale tout seul, c est ce qu on veut.
        ["commit", "-m", message],
    ]
    d.etapes = ["git " + " ".join(c) for c in commandes]
    if not ecrire:
        return d

    for c in commandes:
        code, sortie = _git(racine, *c)
        if code == 0:
            continue
        if c[0] == "init" and "-b" in c:
            # git < 2.28 ne connait pas `init -b`. Repli explicite, jamais
            # silencieux : la branche se pose ensuite.
            code, sortie = _git(racine, "init")
            if code == 0:
                _git(racine, "symbolic-ref", "HEAD", f"refs/heads/{branche}")
                continue
        d.echecs.append(f"`git {' '.join(c)}` a échoué :\n{sortie}")
        return d

    code, sortie = _git(racine, "rev-parse", "--short", "HEAD")
    d.commit = sortie if code == 0 else None
    return d


def etat(racine: Path) -> tuple[bool, str]:
    """(l arbre est propre, la sortie de `git status --porcelain`)."""
    code, sortie = _git(racine, "status", "--porcelain")
    if code != 0:
        return False, sortie
    return (sortie == ""), sortie
