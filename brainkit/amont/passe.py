"""passe.py — une passe de sondage : quelles pages, quelles cibles, quel rapport.

Trois choix, et ils sont le lot.

1. **La reprise est le mode normal, pas une option de secours.** Une passe saute
   ce qui a ete sonde depuis moins de `--age-max-jours`, et `--limit` borne le
   reste. Deux consequences : une passe interrompue ne perd rien, et un vault
   qu on ne veut sonder que par morceaux se sonde par morceaux. Le mecanisme
   n existe pas parce que le reseau est lent, il existe parce qu un sondage
   complet est un geste rare et qu on ne doit jamais avoir peur de le lancer.

2. **Le rapport separe ce qu on sait de ce qu on ne sait pas.** Trois lignes
   distinctes : les pages a release datee, celles dont l amont n est pas
   atteignable, celles qui n ont jamais ete sondees. Un compteur unique
   melangerait « il n y a rien a savoir » et « je n ai pas encore regarde ».

3. **Le sondage NE JUGE PAS la page.** Il derive un etat et l ecrit dans le
   side-car. Confronter cet etat a ce que la page declare est le travail du
   validateur, et la separation est deliberee : un rapport qui juge finit par
   proposer de corriger, et corriger un champ que l auteur a ecrit n appartient
   pas a un outil.
"""

from __future__ import annotations

import datetime
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

from ..valider import conditions, vault as _vault
from . import etat as _etat
from . import sidecar, sondes
from .declaration import Amont, declaration

# PEP 503, et generalisable : un nom de paquet se normalise avant d etre demande
# a un registre. Le kit ne connait qu une normalisation, et c est assez : les
# registres qui comptent l ont tous adoptee.
RE_NORMALISE = re.compile(r"[-_.]+")


def normalise(nom: str) -> str:
    return RE_NORMALISE.sub("-", str(nom).strip().replace(" ", "-")).lower()


@dataclass
class Rapport:
    pages: int = 0
    sondees: int = 0
    fraiches: int = 0                        # sautees par la reprise
    hors_limite: int = 0                     # laissees a la passe suivante
    requetes: int = 0
    orphelines: list[str] = field(default_factory=list)
    sans_cible: list[str] = field(default_factory=list)
    sous_arbres: list[str] = field(default_factory=list)
    archivage_inconnu: list[str] = field(default_factory=list)
    par_etat: dict[str, int] = field(default_factory=dict)
    avec_release: int = 0
    avec_registre: int = 0
    avec_commit_seul: int = 0
    seuil_declare: bool = True
    lignes: list[tuple[str, str, str]] = field(default_factory=list)


def cibles_de_la_page(fm: dict, amont: Amont) -> tuple[tuple[str, str] | None,
                                                       tuple[str, str] | None,
                                                       str]:
    """((sonde de depot, cible), (sonde de registre, cible), l URL declaree).

    Les deux sont independantes : un paquet publie sur un registre sans depot
    declare se sonde quand meme, et un depot sans paquet aussi.
    """
    url = str(fm.get(amont.champ_url) or "").strip() if amont.champ_url else ""
    depot = None
    if url.startswith("http"):
        from urllib.parse import urlsplit
        nom_sonde = amont.sonde_de_l_hote(urlsplit(url).netloc)
        if nom_sonde:
            cible = sondes.cible_de_l_url(url)
            if cible:
                depot = (nom_sonde, cible)

    registre = None
    decl = amont.registre
    if decl and decl.get("sonde"):
        si = str(decl.get("si") or "")
        tient = conditions.evalue(si, fm) if si else True
        if tient:
            for champ in decl.get("champs") or []:
                brut = fm.get(champ)
                candidats = brut if isinstance(brut, list) else [brut]
                for c in candidats:
                    n = normalise(c or "")
                    if n:
                        registre = (str(decl["sonde"]), n)
                        break
                if registre:
                    break
    return depot, registre, url


def _frais(rec: dict | None, aujourdhui: datetime.date, age_max: int) -> bool:
    d = (rec or {}).get("sonde_le")
    if not d:
        return False
    try:
        return (aujourdhui - datetime.date.fromisoformat(str(d))).days < age_max
    except ValueError:
        return False


def sonde_une_page(fm: dict, amont: Amont, rap: Rapport, chemin: str,
                   pause: float = 0.0) -> dict:
    """Les faits bruts d une page. Aucune derivation, aucun jugement."""
    depot, registre, url = cibles_de_la_page(fm, amont)
    rec: dict = {}
    if depot is not None:
        fn = sondes.IMPLEMENTEES.get(depot[0])
        if fn is not None:
            rec |= fn(depot[1])
            rap.requetes += 3 if depot[0] == "github" else 1
            if sondes.sous_arbre(url):
                rap.sous_arbres.append(f"{chemin} — {url}")
            if rec.pop("archive_inconnu", False):
                rap.archivage_inconnu.append(chemin)
    if registre is not None:
        fn = sondes.IMPLEMENTEES.get(registre[0])
        if fn is not None:
            avant = dict(rec)
            rec |= fn(registre[1])
            rap.requetes += 1
            # Un registre qui ne connait pas le nom ne doit pas effacer ce que
            # le depot a rendu : on ne garde son echec que s il n ecrase rien.
            if "registre" not in rec and avant:
                rec.pop("http_registre", None)
                rec |= avant
    if not depot and not registre:
        rap.sans_cible.append(chemin)
    if pause:
        time.sleep(pause)
    return rec


def passe(mo, racine: Path, limite: int | None = None, age_max: int = 7,
          recalculer: bool = False, pause: float = 0.0,
          aujourdhui: datetime.date | None = None) -> tuple[dict, Rapport, Amont]:
    """Une passe complete. Rend (le side-car a ecrire, le rapport, la declaration)."""
    amont = declaration(mo)
    rap = Rapport()
    if not amont.declare:
        return {}, rap, amont
    rap.seuil_declare = amont.seuil_declare
    aujourdhui = aujourdhui or datetime.date.today()

    pages = [p for p in _vault.lire_vault(racine, mo.non_pages)
             if p.illisible is None and p.role in amont.porte_par]
    rap.pages = len(pages)
    ancien = sidecar.lit_side_car(amont, racine)
    rap.orphelines = sidecar.orphelines(ancien, {p.chemin for p in pages})

    a_sonder: list = []
    for p in pages:
        if recalculer:
            continue
        if _frais(ancien.get(p.chemin), aujourdhui, age_max):
            rap.fraiches += 1
            continue
        a_sonder.append(p)
    if limite is not None and len(a_sonder) > limite:
        rap.hors_limite = len(a_sonder) - limite
        a_sonder = a_sonder[:limite]
    prevu = {p.chemin for p in a_sonder}

    neuf: dict = {}
    for p in pages:
        rec = dict(ancien.get(p.chemin) or {})
        if p.chemin in prevu:
            rec = sonde_une_page(p.fm, amont, rap, p.chemin, pause=pause)
            rec["sonde_le"] = aujourdhui.isoformat()
            rap.sondees += 1
        elif recalculer and not rec:
            continue
        e, d = _etat.derive(rec, amont, aujourdhui)
        if rec:
            rec["etat"], rec["date"] = e, d
            neuf[p.chemin] = rec
        rap.par_etat[e] = rap.par_etat.get(e, 0) + 1
        if rec.get("release_le"):
            rap.avec_release += 1
        if rec.get("registre_le"):
            rap.avec_registre += 1
        if rec.get("commit_le") and not rec.get("release_le") \
                and not rec.get("registre_le"):
            rap.avec_commit_seul += 1
        if e in ("archive", "ancienne"):
            rap.lignes.append((p.chemin, e, d))
    return neuf, rap, amont
