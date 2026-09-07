# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6", "jsonschema>=4.21"]
# ///
"""valider.py — passe un `brain.yml` au contrat du lot 1.

C est le SEUL code executable de ce lot, et il ne fait qu une chose : verifier un
manifeste. Deux passes, dans cet ordre, et la seconde ne tourne que si la
premiere est verte :

  1. JSON SCHEMA — schema/brain.schema.json, draft 2020-12, sans extension.
     Porte cinq des six refus du critere d acceptation : une `fonction:` hors de
     la liste fermee de six, l absence d exactement un role de fonction `unite`,
     l absence d exactement un role de fonction `hub`, un champ conditionnel sans
     condition, une version de manifeste inconnue.

  2. COHERENCE — C1..C10 ci-dessous. Le sixieme refus — « une valeur d
     enumeration absente de la declaration de son axe » — est INTRA-DOCUMENT :
     il compare une valeur ecrite quelque part a une liste declaree ailleurs dans
     le MEME fichier. JSON Schema ne sait pas faire ca sans l extension `$data`,
     qui n est pas dans la norme et que la bibliotheque de reference Python n
     implemente pas. Le refus est donc porte ici, nomme, avec son motif — c est
     la meme lecon que §2.3 point 2 du cadrage : le manifeste BRANCHE les regles,
     il ne les decrit pas, et le kit garde du code par regle.

Toute violation, des deux passes, nomme LE CHAMP FAUTIF par son chemin dans le
document (`roles[2].champs.conditionnels[0].si`, `bandeau.colonnes[1].source`).

Usage :
    uv run schema/valider.py                          # les trois exemples
    uv run schema/valider.py exemples/devbrain.brain.yml
    uv run schema/valider.py --attendre-echec exemples/invalide.brain.yml

Sort en 0 si tout ce qui devait passer passe et tout ce qui devait echouer
echoue ; en 1 sinon.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

RACINE = Path(__file__).resolve().parent.parent
SCHEMA = RACINE / "schema" / "brain.schema.json"
DEFAUT = [
    (RACINE / "exemples" / "devbrain.brain.yml", True),
    (RACINE / "exemples" / "histobrain.brain.yml", True),
    (RACINE / "exemples" / "invalide.brain.yml", False),
]


# --------------------------------------------------------------------- chemins
def chemin(parts) -> str:
    """Chemin d un noeud, ecrit comme on le citerait dans le fichier."""
    out = ""
    for p in parts:
        if isinstance(p, int):
            out += f"[{p}]"
        else:
            out += f".{p}" if out else str(p)
    return out or "<racine>"


def message(e) -> str:
    """Le message d une violation, lisible.

    Deux corrections a la sortie brute de la bibliotheque, et elles comptent
    autant que le refus lui-meme : un refus qu on ne comprend pas ne sert a rien.

      - `contains` / `minContains` / `maxContains` produisent un message qui
        recrache TOUT le tableau et ne dit pas quelle contrainte a cede. Le
        `$comment` de la sous-schema le dit, lui : il est mis en tete.
      - un `instance` long est tronque. La faute est dans le CHEMIN, pas dans le
        volume de donnees qu on rejette.
    """
    sch = e.schema if isinstance(e.schema, dict) else {}
    com = sch.get("$comment")
    if e.validator in {"contains", "minContains", "maxContains"} and com:
        combien = "il n en existe aucun" if e.validator != "maxContains" else "il en existe plusieurs"
        return f"{com} | {combien}"
    brut = " ".join(str(e.message).split())
    if len(brut) > 150:
        brut = brut[:110] + " […] " + brut[-30:]
    return f"{com} | {brut}" if com else brut


# ----------------------------------------------------- passe 2 : coherence
# Chaque contrainte rend une liste de (chemin fautif, message). Elles sont
# INTRA-DOCUMENT : c est exactement ce que JSON Schema ne sait pas exprimer.

def _axes_declares(m: dict) -> dict[str, list[str]]:
    """Toutes les enumerations declarees, par leur nom de source."""
    out: dict[str, list[str]] = {}
    ax = m.get("axes") or {}

    rang = ax.get("rangement") or {}
    valeurs: list[str] = []
    courte = bool(rang.get("valeur_courte_autorisee"))
    for pfx in rang.get("prefixes") or []:
        cle = pfx.get("cle")
        sous = pfx.get("sous") or {}
        if courte and not sous:
            valeurs.append(str(cle))
        for s in sous:
            valeurs.append(f"{cle}/{s}")
    for cle, r in (rang.get("rattachements") or {}).items():
        for s in (r.get("sous") or {}):
            valeurs.append(f"{cle}/{s}")
    out["axes.rangement"] = valeurs

    nat = ax.get("nature") or {}
    if nat:
        out["axes.nature"] = [str(v.get("cle")) for v in nat.get("valeurs") or []]

    for t in ax.get("transverses") or []:
        out[f'axes.transverses[{t.get("champ")}]'] = [
            str(v.get("cle")) for v in t.get("valeurs") or []
        ]

    out["roles[].id"] = [str(r.get("id")) for r in m.get("roles") or []]
    for nom in m.get("vocabulaires") or {}:
        out[f"vocabulaires.{nom}"] = []  # vocabulaire externe : non verifiable ici
    return out


def coherence(m: dict) -> list[tuple[str, str]]:
    err: list[tuple[str, str]] = []
    roles = m.get("roles") or []
    dico = m.get("champs") or {}
    axes = _axes_declares(m)

    # C1 — tout champ requis est aussi autorise.
    for i, r in enumerate(roles):
        ch = r.get("champs") or {}
        autor = set(ch.get("autorises") or [])
        for j, f in enumerate(ch.get("requis") or []):
            if f not in autor:
                err.append((f"roles[{i}].champs.requis[{j}]",
                            f"C1 — `{f}` est requis sur le role `{r.get('id')}` "
                            f"mais absent de `autorises`"))
        for j, f in enumerate(ch.get("deprecies") or []):
            if f not in autor:
                err.append((f"roles[{i}].champs.deprecies[{j}]",
                            f"C1 — `{f}` est declare deprecie mais absent de `autorises`"))
        for j, c in enumerate(ch.get("conditionnels") or []):
            if c.get("champ") not in autor:
                err.append((f"roles[{i}].champs.conditionnels[{j}].champ",
                            f"C1 — `{c.get('champ')}` est conditionnel mais absent "
                            f"de `autorises`"))

    # C2 — tout champ nomme quelque part est defini une fois dans `champs:`.
    def exige_champ(nom, ou):
        if nom is not None and nom not in dico:
            err.append((ou, f"C2 — `{nom}` n est defini nulle part dans `champs:`"))

    for i, r in enumerate(roles):
        ch = r.get("champs") or {}
        for j, f in enumerate(ch.get("autorises") or []):
            exige_champ(f, f"roles[{i}].champs.autorises[{j}]")
        for j, s in enumerate(r.get("corps") or []):
            if s.get("genre") == "liste_liens":
                exige_champ(s.get("champ"), f"roles[{i}].corps[{j}].champ")
    for j, c in enumerate((m.get("bandeau") or {}).get("colonnes") or []):
        exige_champ(c.get("source"), f"bandeau.colonnes[{j}].source")
        exige_champ(c.get("qualifie_par"), f"bandeau.colonnes[{j}].qualifie_par")

    # C3 — la `source` d un champ enumere resout vers un axe ou un vocabulaire.
    for nom, d in dico.items():
        src = d.get("source")
        if src and src not in axes:
            err.append((f"champs.{nom}.source",
                        f"C3 — `{src}` ne designe aucun axe ni vocabulaire declare "
                        f"(connus : {', '.join(sorted(axes))})"))

    # C4 — REFUS 6 : toute valeur d enumeration ecrite dans le manifeste
    # appartient a la declaration de son axe.
    def source_de(nom_champ: str) -> list[str] | None:
        d = dico.get(nom_champ) or {}
        if d.get("valeurs"):
            return [str(v) for v in d["valeurs"]]
        src = d.get("source")
        if src in axes and axes[src]:
            return axes[src]
        return None

    for j, c in enumerate((m.get("bandeau") or {}).get("colonnes") or []):
        legales = source_de(c.get("source"))
        if legales is None:
            continue
        for k in (c.get("table") or {}):
            if str(k) not in legales:
                err.append((f'bandeau.colonnes[{j}].table.{k}',
                            f"C4 — `{k}` n est pas une valeur declaree de "
                            f"`{c.get('source')}`"))
        dep = c.get("depend_de") or {}
        for k, fam in enumerate(dep.get("familles") or []):
            if str(fam) not in legales:
                err.append((f"bandeau.colonnes[{j}].depend_de.familles[{k}]",
                            f"C4 — `{fam}` n est pas une valeur declaree de "
                            f"`{c.get('source')}`"))
    for nom, d in dico.items():
        legales = source_de(nom)
        if legales is None:
            continue
        for k, v in enumerate(d.get("eliminatoire") or []):
            if str(v) not in legales:
                err.append((f"champs.{nom}.eliminatoire[{k}]",
                            f"C4 — `{v}` n est pas une valeur declaree de ce champ"))

    # C5 — une paire `reciproque: inverse` pointe dans les DEUX sens.
    for nom, d in dico.items():
        rec = d.get("reciproque")
        if isinstance(rec, dict) and rec.get("mode") == "inverse":
            autre = rec.get("champ")
            cible = dico.get(autre) or {}
            rc = cible.get("reciproque")
            if not (isinstance(rc, dict) and rc.get("mode") == "inverse"
                    and rc.get("champ") == nom):
                err.append((f"champs.{nom}.reciproque.champ",
                            f"C5 — `{nom}` declare l inverse `{autre}`, qui ne "
                            f"declare pas `{nom}` en retour : la paire est mal "
                            f"formee et remplacerait un trou par un autre"))

    # C6 — un axe non exclusif declare un prefixe transversal qui EXISTE.
    rang = (m.get("axes") or {}).get("rangement") or {}
    if rang.get("exclusif") is False:
        pt = rang.get("prefixe_transversal")
        cles = {p.get("cle") for p in rang.get("prefixes") or []}
        if pt not in cles:
            err.append(("axes.rangement.prefixe_transversal",
                        f"C6 — `{pt}` n est pas declare dans `prefixes[]`"))

    # C7 — aucun dossier d axe transverse ne redouble un autre nom de dossier.
    pris: dict[str, str] = {}
    for r in roles:
        if r.get("dossier"):
            pris[str(r["dossier"]).casefold()] = f"roles[{r.get('id')}].dossier"
        hr = r.get("hub_de_ralliement") or {}
        if hr.get("dossier"):
            pris[str(hr["dossier"]).casefold()] = f"roles[{r.get('id')}].hub_de_ralliement"
    for p in rang.get("prefixes") or []:
        pris.setdefault(str(p.get("dossier", "")).casefold(), f"prefixes[{p.get('cle')}]")
    plur = ((m.get("libelles") or {}).get("axe_rangement") or {}).get("p", "")
    for i, t in enumerate((m.get("axes") or {}).get("transverses") or []):
        d = str(t.get("dossier", ""))
        if d.casefold() == str(plur).casefold():
            err.append((f"axes.transverses[{i}].dossier",
                        f"C7 — `{d}` redouble le libelle pluriel de l axe de "
                        f"rangement : l homonymie serait un piege"))
        if d.casefold() in pris:
            err.append((f"axes.transverses[{i}].dossier",
                        f"C7 — `{d}` est deja pris par {pris[d.casefold()]}"))
        pris[d.casefold()] = f"axes.transverses[{i}].dossier"

    # C8 — tout role nomme dans `porte_par`, `interdit_sur`, `bandeau.porte_par`
    # ou `regles[].roles` est un role declare.
    ids = {str(r.get("id")) for r in roles}

    def exige_role(v, ou):
        if v not in ids:
            err.append((ou, f"C8 — `{v}` n est pas un `roles[].id` declare"))

    nat = (m.get("axes") or {}).get("nature") or {}
    for k, v in enumerate(nat.get("porte_par") or []):
        exige_role(v, f"axes.nature.porte_par[{k}]")
    for k, v in enumerate(nat.get("interdit_sur") or []):
        exige_role(v, f"axes.nature.interdit_sur[{k}]")
    for k, v in enumerate((m.get("bandeau") or {}).get("porte_par") or []):
        exige_role(v, f"bandeau.porte_par[{k}]")
    for i, rg in enumerate(m.get("regles") or []):
        for k, v in enumerate(rg.get("roles") or []):
            exige_role(v, f"regles[{i}].roles[{k}]")

    # C9 — toute section nommee dans une regle existe dans un corps de role.
    titres = {s.get("titre") for r in roles for s in (r.get("corps") or [])}
    titres |= {s.get("titre_rendu") for r in roles for s in (r.get("corps") or [])}
    for i, rg in enumerate(m.get("regles") or []):
        for k, s in enumerate(rg.get("sections") or []):
            if s not in titres:
                err.append((f"regles[{i}].sections[{k}]",
                            f"C9 — la section « {s} » n existe dans aucun "
                            f"`roles[].corps[].titre`"))
        sev = rg.get("severite")
        if isinstance(sev, dict):
            for s in sev:
                if s not in titres:
                    err.append((f"regles[{i}].severite.{s}",
                                f"C9 — la section « {s} » n existe dans aucun "
                                f"`roles[].corps[].titre`"))

    # C10 — un champ designe `resume_court` est unique, et la regle 6 le cite.
    courts = [n for n, d in dico.items() if d.get("fonction") == "resume_court"]
    if len(courts) > 1:
        err.append(("champs", f"C10 — {len(courts)} champs se declarent "
                              f"`resume_court` ({', '.join(courts)}) : il n en faut "
                              f"qu un, ou aucun"))
    for i, rg in enumerate(m.get("regles") or []):
        if rg.get("id") == "reinjection_du_resume" and rg.get("active"):
            cr = rg.get("champ_resume")
            if cr not in courts:
                err.append((f"regles[{i}].champ_resume",
                            f"C10 — `{cr}` n est pas le champ declare "
                            f"`fonction: resume_court`"))
    return err


# ------------------------------------------------------------------------ main
def valide(f: Path, schema: dict) -> list[str]:
    """Les violations d un fichier, chemin fautif en tete de chaque ligne."""
    try:
        m = yaml.safe_load(f.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        premiere = str(e).splitlines()[0].strip()
        return [f"<yaml> : illisible — {premiere}"]
    if not isinstance(m, dict):
        return ["<racine> : le manifeste n est pas un dictionnaire de champs"]

    v = Draft202012Validator(schema)
    out = []
    for e in sorted(v.iter_errors(m), key=lambda e: [str(p) for p in e.absolute_path]):
        out.append(f"[schema]    {chemin(e.absolute_path)} : {message(e)}")
    # La passe de coherence tourne TOUJOURS, meme si le schema a deja refuse :
    # sinon le refus 6 resterait invisible sur un fichier qui viole aussi une
    # contrainte structurelle, et le contre-exemple ne pourrait pas montrer les
    # six refus a la fois.
    try:
        out += [f"[coherence] {ou} : {msg}" for ou, msg in coherence(m)]
    except Exception as exc:  # noqa: BLE001 — un manifeste trop casse pour etre parcouru
        out.append(f"[coherence] <racine> : passe interrompue — {type(exc).__name__}: {exc}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Valide un brain.yml contre le contrat du lot 1.")
    ap.add_argument("fichiers", nargs="*", help="manifestes a valider ; vide = les trois exemples")
    ap.add_argument("--attendre-echec", action="store_true",
                    help="les fichiers donnes DOIVENT echouer")
    ns = ap.parse_args()

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    print(f"schema : {SCHEMA.name} — draft 2020-12, bien forme")

    cibles = ([(Path(x), not ns.attendre_echec) for x in ns.fichiers]
              if ns.fichiers else DEFAUT)

    code = 0
    for f, doit_passer in cibles:
        viol = valide(f, schema)
        verdict = "VALIDE" if not viol else f"REFUSE ({len(viol)} violation(s))"
        attendu = "doit passer" if doit_passer else "doit echouer"
        ok = (not viol) == doit_passer
        print(f"\n{'  OK  ' if ok else ' ECHEC'} {f.name} — {verdict} [{attendu}]")
        for line in viol:
            print(f"        {line}")
        if not ok:
            code = 1
    print()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
