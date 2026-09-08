"""sondes.py — les deux sondes que le kit sait faire, et rien d autre.

Une sonde prend une CIBLE (un slug de depot, un nom de paquet) et rend des FAITS
DATES. Elle ne juge rien, elle ne derive aucun etat, elle ne lit pas le vault.
La liste est fermee par le kit (`declaration.SONDES`) : le manifeste dit quel
hote se sonde par quelle sonde, il n en invente pas.

# Aucun jeton, et c est une decision de conception

L API REST de GitHub donne tout ce qu on veut en un appel — et **60 appels par
heure** sans jeton. Sur les 316 depots du vault d origine, une passe complete
prendrait plus de cinq heures, ou exigerait un jeton. Un jeton dans un vault
versionne est un secret publie ; un jeton dans l environnement est une etape
d installation qu on oublie, donc un outillage qui, un jour, ne tourne plus.

Les trois URL ci-dessous sont celles qu un navigateur charge, sans compte et
sans quota d API :

  - `releases.atom` — le flux des versions publiees. Le premier `<entry>` est la
    derniere, avec sa date et son etiquette ;
  - `commits.atom`  — le flux de la branche par defaut. Meme lecture ;
  - la page du depot — le seul endroit ou l archivage se lit sans jeton. Le
    marqueur est un drapeau JSON embarque, `"isArchived": true|false`, double
    d une phrase qui porte la DATE de l archivage.

La derniere est la plus chere, et sa lecture est donc **bornee** : on s arrete
des que le marqueur est vu, ou au plafond declare. On telecharge un quart de
megaoctet la ou l API en rendait deux kilos — c est le prix de l absence de
jeton, et il est paye en octets plutot qu en secret.

# Ce qu une sonde qui echoue rend

Un dictionnaire portant `http:` et rien d autre. Jamais une exception qui
remonte, jamais un fait invente : une sonde muette laisse la page en
`sans_amont`, ce qui est exactement ce qu on sait d elle.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from urllib.parse import urlsplit

UA = ("brainkit-amont/1 (sondage de fraicheur, lecture seule, sans jeton)")
PLAFOND_PAGE = 400_000          # octets lus au plus sur une page HTML
DELAI = 25

RE_ENTREE = re.compile(r"<entry>(.*?)</entry>", re.S)
RE_MAJ = re.compile(r"<updated>([^<]+)</updated>")
RE_TITRE = re.compile(r"<title>([^<]*)</title>")
RE_ARCHIVE = re.compile(r'"isArchived":\s*(true|false)')
RE_ARCHIVE_LE = re.compile(
    r"This repository was archived by the owner on ([A-Z][a-z]{2} \d{1,2}, \d{4})")
MOIS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], start=1)}

# `github.com/<proprietaire>/<depot>/...` — on garde les DEUX premiers segments
# et on ignore la suite. Une URL qui vise un sous-arbre (`/tree/master/xxx`)
# designe quand meme un depot : on le sonde, et le rapport dit que ses dates
# decrivent le depot entier, pas le sous-arbre.
RE_SLUG = re.compile(r"^/([^/\s]+)/([^/\s?#]+?)(?:\.git)?(?:/.*)?$")


# --------------------------------------------------------------------------- #
#  Le transport
# --------------------------------------------------------------------------- #
def _lit(url: str, plafond: int | None = None,
         arret: re.Pattern | None = None) -> tuple[int, str]:
    """(code HTTP, texte lu). Lecture BORNEE, et interrompue des que `arret` mord."""
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept-Encoding": "identity"})
    try:
        with urllib.request.urlopen(req, timeout=DELAI) as r:
            if plafond is None:
                return r.status, r.read().decode("utf-8", "replace")
            buf, lu = "", 0
            while lu < plafond:
                bloc = r.read(65536)
                if not bloc:
                    break
                lu += len(bloc)
                buf += bloc.decode("utf-8", "replace")
                if arret is not None and arret.search(buf):
                    break
            return r.status, buf
    except urllib.error.HTTPError as e:
        return e.code, ""
    except OSError:
        return 0, ""


def _premiere_entree(flux: str) -> tuple[str, str]:
    """(date ISO, titre) de la premiere entree d un flux Atom. ('', '') si aucune."""
    m = RE_ENTREE.search(flux)
    if not m:
        return "", ""
    bloc = m.group(1)
    d = RE_MAJ.search(bloc)
    t = RE_TITRE.search(bloc)
    return (d.group(1)[:10] if d else ""), (t.group(1).strip() if t else "")


def _date_anglaise(brut: str) -> str:
    m = re.match(r"([A-Z][a-z]{2}) (\d{1,2}), (\d{4})", brut.strip())
    if not m or m.group(1) not in MOIS:
        return ""
    return f"{m.group(3)}-{MOIS[m.group(1)]:02d}-{int(m.group(2)):02d}"


# --------------------------------------------------------------------------- #
#  Les cibles
# --------------------------------------------------------------------------- #
def cible_de_l_url(url: str) -> str | None:
    """Le slug `<proprietaire>/<depot>` d une URL de depot, ou None."""
    m = RE_SLUG.match(urlsplit(url.strip()).path or "")
    return f"{m.group(1)}/{m.group(2)}" if m else None


def sous_arbre(url: str) -> bool:
    """L URL vise-t-elle un sous-arbre plutot que la racine du depot ?"""
    parts = [p for p in (urlsplit(url.strip()).path or "").split("/") if p]
    return len(parts) > 2


# --------------------------------------------------------------------------- #
#  Les sondes
# --------------------------------------------------------------------------- #
def github(cible: str) -> dict:
    """Derniere version publiee, dernier mouvement, archivage. Trois requetes."""
    base = f"https://github.com/{cible}"
    rec: dict = {"amont": f"github:{cible}"}

    code, flux = _lit(f"{base}/releases.atom")
    rec["http"] = code
    if code == 200:
        d, titre = _premiere_entree(flux)
        if d:
            rec["release_le"] = d
            if titre:
                rec["release_tag"] = titre
    elif code in (404, 451):
        return rec                      # depot disparu ou retire : inutile d insister

    code, flux = _lit(f"{base}/commits.atom")
    if code == 200:
        d, _t = _premiere_entree(flux)
        if d:
            rec["commit_le"] = d

    code, page = _lit(base, plafond=PLAFOND_PAGE, arret=RE_ARCHIVE)
    if code == 200:
        m = RE_ARCHIVE.search(page)
        if m:
            rec["archive"] = m.group(1) == "true"
            q = RE_ARCHIVE_LE.search(page)
            if rec["archive"] and q:
                d = _date_anglaise(q.group(1))
                if d:
                    rec["archive_le"] = d
        else:
            # Le marqueur n a pas ete vu sous le plafond. On ne conclut PAS
            # « non archive » : on ne sait pas, et le dire est le travail.
            rec["archive_inconnu"] = True
    elif code:
        rec["http_page"] = code
    return rec


def pypi(cible: str) -> dict:
    """Derniere version publiee sur le registre, et sa date. Une requete."""
    code, brut = _lit(f"https://pypi.org/pypi/{cible}/json")
    if code != 200 or not brut:
        return {"http_registre": code}
    try:
        data = json.loads(brut)
    except json.JSONDecodeError:
        return {"http_registre": 0}
    info = data.get("info") or {}
    version = str(info.get("version") or "")
    rec: dict = {"registre": cible}
    if version:
        rec["registre_version"] = version
    fichiers = data.get("urls") or []
    if not fichiers and version:
        fichiers = (data.get("releases") or {}).get(version) or []
    dates = sorted(str(f.get("upload_time") or "")[:10] for f in fichiers
                   if f.get("upload_time"))
    if dates:
        rec["registre_le"] = dates[-1]
    return rec


IMPLEMENTEES = {"github": github, "pypi": pypi}
