"""conditions.py — les conditions du manifeste, evaluees sur un frontmatter.

Le manifeste ecrit ses conditions en francais court. Ce module lit EXACTEMENT
les trois formes ci-dessous et rien de plus, parce qu une condition illisible
doit se REMONTER, jamais se deviner : traitee comme vraie, elle expliquerait une
violation par une supposition.

    <champ> in [a, b, c]
    <champ> == v     ·     <champ> != v
    <champ> renseigne          (accents tolerés : « renseigné »)

Conjonction par « et » / « and ». Rien d autre : ni « ou », ni parentheses, ni
negation. Le jour ou un manifeste en aura besoin, la forme s ajoute ici et la
regle qui la consomme le dit.
"""

from __future__ import annotations

import re

from . import vault

RE_IN = re.compile(r"^([a-z_][a-z0-9_]*)\s+in\s*\[(.*?)\]$", re.I)
RE_EQ = re.compile(r"^([a-z_][a-z0-9_]*)\s*(==|!=)\s*(.+)$", re.I)
RE_RENSEIGNE = re.compile(r"^([a-z_][a-z0-9_]*)\s+renseign[ée]e?$", re.I)


def evalue_atome(cond: str, fm: dict) -> bool | None:
    m = RE_IN.match(cond)
    if m:
        champ, brut = m.group(1), m.group(2)
        legales = [v.strip().strip("\"'") for v in brut.split(",") if v.strip()]
        portees = vault.valeurs(fm.get(champ))
        return any(v in legales for v in portees)
    m = RE_RENSEIGNE.match(cond)
    if m:
        return vault.non_vide(fm.get(m.group(1)))
    m = RE_EQ.match(cond)
    if m:
        champ, op, val = m.group(1), m.group(2), m.group(3).strip().strip("\"'")
        egal = str(fm.get(champ) or "") == val
        return egal if op == "==" else not egal
    return None


def evalue(cond: str, fm: dict) -> bool | None:
    """La condition, ou None si elle sort des formes lues."""
    if not cond:
        return None
    sortie = True
    for atome in re.split(r"\s+(?:et|and)\s+", cond.strip()):
        v = evalue_atome(atome.strip(), fm)
        if v is None:
            return None
        sortie = sortie and v
    return sortie
