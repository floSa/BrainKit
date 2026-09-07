"""vues.py — la couverture des VUES, et le seul endroit du moteur qui dépend d Obsidian.

Une vue est un fichier de requete pose a cote de la page qui l embarque. Le
manifeste declare son extension et son MOTEUR (`vue_embarquee.moteur`) ; le
langage de filtre appartient a ce moteur, pas au kit. Ce module implemente
`obsidian-bases`, et refuse de compter quand le moteur est autre — un decompte
faux serait pire qu un decompte absent.

Quatre constats, tous SOUPLES par declaration du manifeste : creer une vue est
une decision EDITORIALE, pas technique.

  (a) une valeur d axe assez peuplee qu aucune vue ne reunit ;
  (b) une vue a moins de membres que le seuil — une vue sans comparaison ;
  (c) une vue que plus aucune page ne cite ;
  (d) un filtre par LISTE DE NOMS codee en dur : une page qui entre dans le
      theme n entrera jamais dans la vue ;
  (e) une page hors de TOUTE vue alors qu une vue retient ses pairs — c est l
      angle mort de (a) : (a) verifie qu une valeur a sa vue, jamais que ses
      pages y entrent.
"""

from __future__ import annotations

import collections
import re
from pathlib import Path

import yaml

from . import chemins, constat, vault
from .constat import Rapport
from .contexte import Contexte

MOTEUR_CONNU = "obsidian-bases"
STR = r'"([^"]*)"'


def filtre_match(expr, chemin: str, fm: dict) -> bool | None:
    """Une clause de filtre `obsidian-bases`, evaluee sur une page. None = forme inconnue.

    Couvre les formes que les vues d un vault reel emploient ; toute forme
    nouvelle rend la vue NON EVALUABLE et se signale comme telle, plutot que de
    produire un decompte faux.
    """
    if isinstance(expr, dict):
        for op, agg in (("and", all), ("or", any)):
            if op in expr:
                res = [filtre_match(e, chemin, fm) for e in expr[op]]
                return None if None in res else agg(res)
        if "not" in expr:
            v = filtre_match(expr["not"], chemin, fm)
            return None if v is None else not v
        return None
    s = str(expr).strip()
    m = re.fullmatch(rf"file\.path\.startsWith\({STR}\)", s)
    if m:
        return chemin.startswith(m.group(1))
    m = re.fullmatch(rf"file\.name\s*==\s*{STR}", s)
    if m:
        return Path(chemin).stem == m.group(1)
    m = re.fullmatch(rf"(?:file\.hasTag|tags\.contains)\({STR}\)", s)
    if m:
        return m.group(1) in (fm.get("tags") or [])
    m = re.fullmatch(rf"([a-z_]+)\.startsWith\({STR}\)", s)
    if m:
        return str(fm.get(m.group(1)) or "").startswith(m.group(2))
    m = re.fullmatch(rf"([a-z_]+)\s*(==|!=)\s*(?:{STR}|null)", s)
    if m:
        champ, op, val = m.group(1), m.group(2), m.group(3)
        cur = fm.get(champ)
        egal = (cur in (None, "", [], {})) if val is None else (cur == val)
        return egal if op == "==" else not egal
    return None


def couverture_des_vues(ctx: Contexte, r: Rapport) -> None:
    rid = "couverture_des_vues"
    mo = ctx.mo
    ext = mo.extension_de_vue()
    rid_unite = mo.role_unite
    if not ext or rid_unite is None:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    moteur = mo.moteur_de_vue()
    if moteur != MOTEUR_CONNU:
        r.etat(rid, f"moteur de vue `{moteur}` non implémenté — filtres non "
                    f"évaluables, aucun décompte produit")
        return

    sev = mo.severite(rid)
    seuil_valeur = int(mo.seuils.get("vue_min_valeurs_axe") or 0)
    seuil_membres = int(mo.seuils.get("vue_min_membres") or 0)

    fm_par_chemin = {p.chemin: p.fm for p in ctx.lisibles}
    membres: dict[str, list[str] | None] = {}

    for fichier in sorted(ctx.racine.rglob(f"*{ext}")):
        parts = fichier.relative_to(ctx.racine).parts
        if parts and parts[0] in vault.HORS_VAULT:
            continue
        nom = fichier.relative_to(ctx.racine).as_posix()
        txt = fichier.read_text(encoding="utf-8")
        try:
            doc = yaml.safe_load(txt) or {}
        except yaml.YAMLError:
            r.ajoute(rid, sev, "YAML illisible", nom, codes=("R8",))
            continue

        # (d) — une liste de noms codee en dur dans le filtre de base, pas dans
        #       les vues secondaires : celles-la sont du confort de lecture.
        durs = len(re.findall(r'file\.name\s*==\s*"', txt.split("views:")[0]))
        if durs >= 2:
            r.ajoute(rid, sev,
                     f"filtre par liste de {durs} noms codée en dur (une page qui "
                     f"entre dans le thème n'entrera jamais dans la vue)",
                     nom, cle="d", codes=("R8d",))

        filt = doc.get("filters")
        if filt is None:
            r.ajoute(rid, sev, "aucun bloc `filters:` — membres indéterminables",
                     nom, codes=("R8",))
            membres[nom] = None
            continue

        sel: list[str] | None = []
        for chemin, fm in fm_par_chemin.items():
            v = filtre_match(filt, chemin, fm)
            if v is None:
                r.ajoute(rid, sev, "filtre non évaluable hors ligne — non compté",
                         nom, codes=("R8",))
                sel = None
                break
            if v:
                sel.append(chemin)
        membres[nom] = sel

        if sel is not None and len(sel) < seuil_membres:
            r.ajoute(rid, sev,
                     f"{len(sel)} membre(s) (< {seuil_membres}) — vue sans comparaison",
                     nom, cle="b", codes=("R8b",))

        # (c) — citee par au moins une page
        if fichier.stem.lower() not in ctx.cibles_citees:
            r.ajoute(rid, sev, "citée par aucune page", nom, cle="c", codes=("R8c",))

    # (a) — une valeur d axe assez peuplee sans vue qui en reunisse le seuil
    compte = collections.Counter()
    for p in ctx.pages_du_role(rid_unite):
        v = chemins.valeur_dominante(p.fm, p.dossier, mo)
        if v:
            compte[v] += 1
    # Les quatre sous-constats n ont PAS le meme denominateur, et les melanger
    # rendrait chacun illisible : (a) se mesure en valeurs d axe assez peuplees,
    # (b) et (d) en fichiers de vue, (e) en pages de l unite.
    r.population(rid, len(ctx.pages_du_role(rid_unite)),
                 objets=len(membres), objet="fichier de vue")
    r.population(rid, len(ctx.pages_du_role(rid_unite)), cle="e")
    r.population(rid, len(membres), cle="b", objets=len(membres),
                 objet="fichier de vue")
    r.population(rid, len(membres), cle="d", objets=len(membres),
                 objet="fichier de vue")
    r.population(rid, len(membres), cle="c", objets=len(membres),
                 objet="fichier de vue")
    assez_peuplees = sum(1 for _v, n in compte.items() if n >= seuil_valeur)
    r.population(rid, len(ctx.pages_du_role(rid_unite)), cle="a",
                 objets=assez_peuplees,
                 objet=f"valeur d'axe à au moins {seuil_valeur} membres")
    for valeur, n in sorted(compte.items()):
        if n < seuil_valeur:
            continue
        couverte = any(
            sel is not None
            and sum(1 for c in sel
                    if chemins.valeur_dominante(fm_par_chemin[c], c.rsplit("/", 1)[0],
                                                mo) == valeur) >= seuil_membres
            for sel in membres.values())
        if not couverte:
            r.ajoute(rid, sev,
                     f"`{valeur}` : {n} {mo.mot('unite', 'p')}, aucune "
                     f"{mo.mot('vue', 's')} ne les réunit", cle="a", codes=("R8a",))

    # (e) — l angle mort de (a) : une page hors de toute vue alors qu une vue
    #       retient ses pairs. La formulation la plus etroite qui attrape le
    #       defaut, et la seule qui soit REPARABLE — elargir un filtre.
    retenues: set[str] = set()
    for sel in membres.values():
        if sel:
            retenues |= set(sel)
    valeurs_en_vue = {chemins.valeur_dominante(fm_par_chemin[c],
                                               c.rsplit("/", 1)[0], mo)
                      for c in retenues
                      if fm_par_chemin[c].get("role") == rid_unite}
    for p in ctx.pages_du_role(rid_unite):
        if p.chemin in retenues:
            continue
        v = chemins.valeur_dominante(p.fm, p.dossier, mo)
        if v in valeurs_en_vue:
            r.ajoute(rid, sev,
                     f"hors de toutes les vues, alors qu'une vue retient d'autres "
                     f"pages de `{v}` — le filtre de la vue l'a laissée dehors",
                     p.chemin, cle="e", codes=("R8e",))


IMPLEMENTEES = {"couverture_des_vues": couverture_des_vues}
