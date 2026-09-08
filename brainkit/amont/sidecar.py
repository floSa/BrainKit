"""sidecar.py — ou vit la donnee sondee, et pourquoi ce n est PAS le frontmatter.

C est l arbitrage central du lot, et il tient en trois raisons.

  1. **Cette donnee se perime toute seule.** Un frontmatter dit ce que l auteur
     a decide ; une date de release dit ce que le monde a fait pendant qu il ne
     regardait pas. Les melanger, c est promettre a l auteur qu il est
     responsable d une valeur qu il n a pas ecrite et qu il ne peut pas tenir.
  2. **Un sondage produirait autant de diffs que d unites.** Sur le vault
     d origine, 337 fiches — donc 337 lignes de `git log` a chaque passage,
     dont aucune ne dirait quoi que ce soit sur le travail de la semaine. Le
     side-car en produit UN.
  3. **Le side-car se jette.** Le supprimer ne perd rien qu un sondage ne
     refasse ; supprimer un champ de frontmatter perd une decision. La
     reversibilite n est pas la meme, et elle doit se voir dans l endroit ou la
     donnee est rangee.

Ce que le side-car garde en plus des faits : l ETAT derive et sa DATE, calcules
au sondage. Cf. `etat.py` — un artefact genere ne doit pas dependre du jour ou
on le lit.

# La cle est un CHEMIN, et c est un defaut connu

Une page n a pas d identifiant stable : la cle du side-car est donc son chemin,
et un `git mv` la casse. Le vault d origine en a fait l experience — 101 entrees
devenues orphelines apres un lot de deplacement, et un mecanisme de reprise mort
en silence pendant tout un lot. On ne peut pas y remedier ici (inventer un
identifiant de page serait un autre lot, et un champ de plus dans 337 pages),
mais on peut **refuser de se taire** : `orphelines()` les nomme, et le rapport
de sondage les imprime.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import etat as _etat
from .declaration import Amont


def chemin_du_side_car(amont: Amont, racine: Path) -> Path | None:
    return (racine / amont.side_car) if amont.declare and amont.side_car else None


def lit_side_car(amont: Amont, racine: Path) -> dict:
    f = chemin_du_side_car(amont, racine)
    if f is None or not f.is_file():
        return {}
    try:
        brut = json.loads(f.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return brut if isinstance(brut, dict) else {}


def ecrit_side_car(amont: Amont, racine: Path, contenu: dict) -> Path:
    """Ecrit le side-car, trie et stable. SEULE ecriture de tout le paquet."""
    f = chemin_du_side_car(amont, racine)
    if f is None:
        raise ValueError("`amont.side_car` non déclaré — rien à écrire")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(dict(sorted(contenu.items())), ensure_ascii=False,
                            indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return f


def orphelines(contenu: dict, chemins_connus: set[str]) -> list[str]:
    """Les entrees qui ne visent plus aucune page — renommee, deplacee, supprimee."""
    return sorted(set(contenu) - chemins_connus)


def charge_faits(mo, racine: Path) -> dict[str, dict[str, str]]:
    """{chemin de page : {nom du fait : valeur}} — ce que le bandeau consomme.

    Rend un dictionnaire VIDE quand le manifeste ne declare pas d amont : c est
    ce qui fait qu un brain sans amont n affiche aucune colonne de fraicheur
    sans qu une seule ligne de condition soit ecrite ailleurs.

    Une page du role concerne qui n a AUCUNE entree recoit quand meme ses faits,
    a l etat `jamais_sonde`. Une cellule vide dirait « champ absent du
    frontmatter », ce qui serait faux : le champ n existe pas, c est le sondage
    qui n a pas eu lieu, et les deux ne se reparent pas de la meme facon.
    """
    from .declaration import declaration

    amont = declaration(mo)
    if not amont.declare or not amont.fait_etat:
        return {}
    contenu = lit_side_car(amont, racine)
    out: dict[str, dict[str, str]] = {}
    for chemin, rec in contenu.items():
        e = str(rec.get("etat") or "")
        if e not in _etat.ETATS:
            e, _d = _etat.derive(rec, amont)
        faits = {amont.fait_etat: e}
        if amont.fait_date:
            faits[amont.fait_date] = str(rec.get("date") or "")
        out[chemin] = faits
    return out


def faits_par_defaut(mo) -> dict[str, str]:
    """Les faits d une page que le side-car ne connait pas."""
    from .declaration import declaration

    amont = declaration(mo)
    if not amont.declare or not amont.fait_etat:
        return {}
    faits = {amont.fait_etat: "jamais_sonde"}
    if amont.fait_date:
        faits[amont.fait_date] = ""
    return faits
