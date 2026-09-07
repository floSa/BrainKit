"""rendu.py — le rapport de mesure, en texte et en Markdown.

Une seule regle de rendu, et elle vaut pour les deux formes : **ce qu on ne sait
pas encore se dit aussi fort que ce qu on sait.** Un rapport de mesure qui
n imprimerait que les regles a zero serait un rapport qui ment par omission —
c est le meme defaut que « une regle absente ressemble a une regle satisfaite »,
transpose a la mesure.

Le rapport repond donc a trois questions, dans cet ordre, et la troisieme est
celle que le lot 8 doit rendre :

  1. **ce qu on sait** — les regles mesurees, leur compte, leur denominateur ;
  2. **ce qu on ne sait pas encore** — les regles refusees, et POURQUOI ;
  3. **a partir de combien de pages on saura** — le manque, chiffre, par regle
     et pour l instance.
"""

from __future__ import annotations

from . import gardes
from .regles import Ligne, Mesure

ETIQUETTE = {
    gardes.PROPOSEE: "PROPOSE",
    gardes.DEJA_DURE: "déjà dure",
    gardes.A_REPARER: "à réparer",
    gardes.REFUS_INSTANCE: "REFUS",
    gardes.REFUS_POPULATION: "REFUS",
    gardes.STRUCTURELLE: "structurelle",
    gardes.NON_MESUREE: "non mesurée",
}


def _denominateur(li: Ligne) -> str:
    p = li.population
    if p is None:
        return "—"
    if p.sur_le_manifeste:
        return f"{p.objets} {p.objet} (sur le manifeste)"
    s = f"{p.pages} page(s)"
    if p.objets is not None and p.objet:
        s += f" · {p.objets} {p.objet}"
    return s


def _pourquoi(li: Ligne, m: Mesure) -> str:
    if li.verdict == gardes.NON_MESUREE:
        return li.etat or ("désactivée par le manifeste" if not li.active
                           else "aucun denominateur déclaré")
    if li.verdict == gardes.DEJA_DURE:
        return "rien à durcir"
    if li.verdict == gardes.A_REPARER:
        return (f"{li.violations} violation(s) à réparer d'abord — un durcissement "
                f"ne se propose pas sur un passif")
    if li.verdict == gardes.STRUCTURELLE:
        return ("garde-fou 3 — hors du régime de la mesure : sa dureté ne "
                "s'obtient pas en comptant des violations")
    if li.verdict == gardes.REFUS_INSTANCE:
        return (f"garde-fou 1 — le vault porte {m.pages_de_l_unite} page(s) de "
                f"`{m.role_unite}`, il en faut {gardes.PLANCHER_PAGES} "
                f"(il en manque {gardes.manque_au_plancher(m.pages_de_l_unite)})")
    if li.verdict == gardes.REFUS_POPULATION:
        return (f"garde-fou 1 — la règle n'a mesuré que {li.pages} page(s) ; "
                f"zéro sur {li.pages} ne prouve rien (il en manque {li.manque})")
    return "0 violation sur une population suffisante"


# --------------------------------------------------------------------------- #
def texte(m: Mesure, rec, occupations, bl) -> list[str]:
    """Le rapport sur la sortie standard."""
    L: list[str] = []
    a = L.append

    a(f"mesurer : vault `{m.vault}`, manifeste `{m.manifeste}`, "
      f"mesuré le {m.date}")
    a(f"  {m.pages_totales} page(s) · unité `{m.role_unite}` : "
      f"{m.pages_de_l_unite} page(s) · plancher de durcissement : "
      f"{gardes.PLANCHER_PAGES}")
    if not m.plancher_tenu:
        a(f"  REFUS GLOBAL — sous le plancher, AUCUN durcissement n'est proposé. "
          f"Il manque {gardes.manque_au_plancher(m.pages_de_l_unite)} page(s) de "
          f"`{m.role_unite}`.")
    a("")

    # ---- 1. le recensement ---------------------------------------------- #
    a(f"recensement : {rec.total_axe} page(s) rangée(s) par l'axe dans "
      f"{len(rec.par_axe)} dossier(s) — {rec.total_role} rangée(s) par `role:` "
      f"({', '.join(rec.roles_par_role) or 'aucun'}) — {rec.total_hubs} hub(s)")
    for d in rec.par_axe:
        detail = " · ".join(f"{r} {n}" for r, n in sorted(d.par_role.items()))
        a(f"  {d.dossier + '/':38s} {d.pages:4d} page(s)   {detail}")
        for sd in d.sous_dossiers:
            a(f"      {sd}/")
    for d in rec.par_role:
        detail = " · ".join(f"{r} {n}" for r, n in sorted(d.par_role.items()))
        a(f"  {d.dossier + '/':38s} {'—':>4s}             {detail}")
    if rec.hors_arbre:
        a(f"  (racine) {rec.hors_arbre} page(s) hors de tout dossier")
    a(f"  promotions : {len(rec.promus)} sous-valeur(s) promue(s) "
      f"(seuil {rec.seuil})")
    for valeur, n, manque in rec.proches_du_seuil:
        a(f"  proche du seuil : `{valeur}` — {n} page(s), il en manque {manque}")
    a("")

    # ---- 2. la mesure, regle par regle ----------------------------------- #
    a("mesure, règle par règle :")
    a(f"  {'règle':36s} {'sévérité':14s} {'viol.':>6s}  population mesurée")
    for li in m.lignes:
        a(f"  {li.id_affiche:36s} {li.severite:14s} {li.violations:6d}  "
          f"{_denominateur(li)}")
        a(f"      {ETIQUETTE[li.verdict]} — {_pourquoi(li, m)}")
        for cle, n, pop in li.details:
            détail = f"{pop.pages} page(s)" if pop else "—"
            if pop and pop.objets is not None and pop.objet:
                détail += f" · {pop.objets} {pop.objet}"
            a(f"        · {cle:28s} {n:4d}  {détail}")
        if li.severite_divergente:
            a(f"      ATTENTION — sévérité déclarée `{li.severite}`, sévérité "
              f"APPLIQUÉE {list(li.severites_vues)} : elle ne vit pas dans la "
              f"règle. Le moteur lit la bonne source ; la déclaration ment au "
              f"lecteur.")
        if li.declaree:
            a(f"      déclaré au manifeste : {li.declaree}")
    a("")

    # ---- 3. les propositions --------------------------------------------- #
    if m.propositions:
        a(f"propositions de durcissement : {len(m.propositions)}")
        a("  Chacune se colle dans `regles[]` — et le `motif:` sort VIDE : le kit")
        a("  sait mesurer, il ne sait pas écrire pourquoi (garde-fou 2).")
        for li in m.propositions:
            a("")
            for ligne in li.bloc_a_coller(m.date):
                a(f"  {ligne}")
    else:
        a("propositions de durcissement : AUCUNE.")
        for li in m.par_verdict(gardes.REFUS_INSTANCE):
            pass
        n_ref = len(m.par_verdict(gardes.REFUS_INSTANCE)) + len(
            m.par_verdict(gardes.REFUS_POPULATION))
        if n_ref:
            a(f"  {n_ref} règle(s) refusée(s) par le plancher — voir ci-dessus.")
    a("")

    # ---- 4. garde-fou 2 --------------------------------------------------- #
    if m.sans_motif:
        a(f"REFUS — garde-fou 2 : {len(m.sans_motif)} sévérité(s) "
          f"`avertissement` sans `motif:` écrit.")
        a("  Une règle qui reste souple doit dire pourquoi. Le kit refuse.")
        for li in m.sans_motif:
            a(f"  - `{li.id_affiche}` : `severite: avertissement`, aucun `motif:`")
    else:
        a("garde-fou 2 : toute sévérité `avertissement` porte son motif écrit.")
    if m.contradictions:
        a("")
        a(f"garde-fou 3 : {len(m.contradictions)} contradiction(s) de manifeste.")
        for c in m.contradictions:
            a(f"  - {c}")
    a("")

    # ---- 5. le gabarit ---------------------------------------------------- #
    mortes = [o for o in occupations if o.morte and o.population]
    a(f"occupation du gabarit : {len(occupations)} section(s) déclarée(s), "
      f"{len(mortes)} remplie(s) sur AUCUNE page")
    for o in sorted(occupations, key=lambda o: (o.role, o.titre)):
        if not o.population:
            continue
        drapeau = ""
        if o.morte:
            drapeau = "  <- MORTE"
        elif o.conditionnelle and o.universelle:
            drapeau = "  <- conditionnelle et pourtant universelle"
        a(f"  {o.role + '.' + o.titre:56s} présente {o.presentes:4d}/"
          f"{o.population:<4d} remplie {o.remplies:4d}{drapeau}")
    if not m.plancher_tenu:
        a(f"  (sous le plancher : ces taux se lisent, ils ne se concluent pas — "
          f"il faut {gardes.PLANCHER_PAGES} pages de l'unité pour trancher.)")
    a("")

    # ---- 6. le backlog ---------------------------------------------------- #
    groupes = bl.par_code()
    a(f"backlog : {len(bl.entrees)} entrée(s) — une liste de TRAVAIL, pas un verdict")
    from .backlog import CODES
    for code in sorted(groupes):
        a(f"  [{code}] {CODES.get(code, '')}")
        for e in groupes[code]:
            a(f"      · {e.sujet} — {e.quoi}")
    return L


# --------------------------------------------------------------------------- #
def markdown(m: Mesure, rec, occupations, bl) -> list[str]:
    """Le meme rapport, en Markdown, pour etre depose dans une instance."""
    L: list[str] = []
    a = L.append
    a(f"# Rapport de mesure — {m.vault}")
    a("")
    a(f"> Produit par `brainkit mesurer` le {m.date}, contre "
      f"`{m.manifeste}`. **Rien n'a été écrit dans le vault** : la mesure est en "
      f"lecture seule, et le durcissement est une décision, pas un effet de bord.")
    a("")

    a("## Ce qu'on sait")
    a("")
    a(f"- {m.pages_totales} page(s) contrôlées.")
    a(f"- Unité `{m.role_unite}` : **{m.pages_de_l_unite} page(s)**.")
    a(f"- Plancher de durcissement (§5.6) : **{gardes.PLANCHER_PAGES} pages de "
      f"l'unité**.")
    mesurees = [x for x in m.lignes if x.verdict != gardes.NON_MESUREE]
    a(f"- {len(mesurees)} règle(s) ont réellement mesuré quelque chose, "
      f"{len(m.lignes) - len(mesurees)} n'ont rien mesuré (désactivées, "
      f"déléguées ou sans objet).")
    a("")
    a("| règle | sévérité | violations | population mesurée | verdict |")
    a("|---|---|---:|---|---|")
    for li in m.lignes:
        a(f"| `{li.id_affiche}` | {li.severite} | {li.violations} | "
          f"{_denominateur(li)} | {ETIQUETTE[li.verdict]} |")
        for cle, n, pop in li.details:
            d = f"{pop.pages} page(s)" if pop else "—"
            if pop and pop.objets is not None and pop.objet:
                d += f" · {pop.objets} {pop.objet}"
            a(f"| &nbsp;&nbsp;· `{cle}` | — | {n} | {d} | (détail) |")
    a("")

    a("## Ce qu'on ne sait pas encore")
    a("")
    if m.plancher_tenu:
        a("Le plancher d'instance est tenu.")
    else:
        a(f"**Le plancher n'est pas tenu.** Le vault porte "
          f"{m.pages_de_l_unite} page(s) de `{m.role_unite}` ; le plancher est à "
          f"{gardes.PLANCHER_PAGES}. Sous ce seuil, une règle à zéro violation "
          f"n'a rien prouvé — elle n'a rien vu. **Aucun durcissement n'est donc "
          f"proposé, pour aucune règle.**")
    a("")
    a("Ce que chaque règle a mesuré malgré tout — le chiffre est vrai, c'est sa "
      "portée qui ne l'est pas encore :")
    a("")
    for li in m.lignes:
        if li.verdict == gardes.REFUS_INSTANCE:
            a(f"- `{li.id_affiche}` — {li.violations} violation(s) sur "
              f"{_denominateur(li)}.")
        elif li.verdict == gardes.REFUS_POPULATION:
            a(f"- `{li.id_affiche}` — {li.violations} violation(s) sur "
              f"{_denominateur(li)} : la règle elle-même n'a vu que {li.pages} "
              f"page(s), il lui en manque {li.manque}.")
    a("")

    a("## À partir de combien de pages on saura")
    a("")
    manque = gardes.manque_au_plancher(m.pages_de_l_unite)
    if manque:
        a(f"**{manque} page(s) de `{m.role_unite}`** — c'est le seul chiffre qui "
          f"débloque quoi que ce soit. Tant qu'il n'est pas atteint, le nombre de "
          f"pages qu'une règle particulière a mesurées ne change rien : le "
          f"plancher d'instance passe avant.")
        a("")
        a("Une fois le plancher d'instance franchi, chaque règle doit encore "
          "avoir mesuré 30 pages POUR ELLE — une règle ne voit que les pages où "
          "une violation était possible. L'état d'aujourd'hui :")
        a("")
        a("| règle | pages mesurées aujourd'hui | il en manque |")
        a("|---|---:|---:|")
        for li in m.lignes:
            if li.verdict == gardes.NON_MESUREE or li.sur_le_manifeste:
                continue
            a(f"| `{li.id_affiche}` | {li.pages} | "
              f"{gardes.manque_au_plancher(li.pages)} |")
    else:
        a("Le plancher d'instance est franchi. Ce qui reste à savoir se lit "
          "règle par règle, dans le tableau ci-dessus.")
    a("")

    a("## Propositions de durcissement")
    a("")
    if m.propositions:
        a("Chaque bloc se colle dans `regles[]`. Le `motif:` sort **vide** : "
          "garde-fou 2, et le kit ne sait pas l'écrire.")
        a("")
        a("```yaml")
        for li in m.propositions:
            for ligne in li.bloc_a_coller(m.date):
                a(ligne)
        a("```")
    else:
        a("**Aucune.** Et c'est le résultat attendu, pas une panne : voir "
          "ci-dessus.")
    a("")

    a("## Les trois garde-fous")
    a("")
    a(f"1. **Plancher** — {gardes.PLANCHER_PAGES} pages de l'unité. "
      + ("tenu." if m.plancher_tenu else
         f"**NON tenu** ({m.pages_de_l_unite}). Aucune proposition émise."))
    if m.sans_motif:
        a(f"2. **Motif obligatoire** — **REFUS** : {len(m.sans_motif)} "
          f"sévérité(s) `avertissement` sans `motif:` écrit — "
          + ", ".join(f"`{li.id_affiche}`" for li in m.sans_motif) + ".")
    else:
        a("2. **Motif obligatoire** — toute sévérité `avertissement` porte son "
          "motif écrit.")
    if m.contradictions:
        a("3. **Structurellement dures** — contradiction(s) :")
        for c in m.contradictions:
            a(f"   - {c}")
    else:
        a("3. **Structurellement dures** — `chemin_categorie` et "
          "`bandeau_a_jour` : rien à signaler.")
    a("")

    a("## Le recensement")
    a("")
    a(f"{rec.total_axe} page(s) rangée(s) par l'axe dans {len(rec.par_axe)} "
      f"dossier(s), {rec.total_role} rangée(s) par `role:` "
      f"({', '.join(rec.roles_par_role) or 'aucun'}), {rec.total_hubs} hub(s).")
    a("")
    a("| dossier | rangées par l'axe | par rôle |")
    a("|---|---:|---|")
    for d in rec.par_axe + rec.par_role:
        a(f"| `{d.dossier}/` | {d.pages or '—'} | "
          f"{' · '.join(f'{r} {n}' for r, n in sorted(d.par_role.items()))} |")
    a("")
    if rec.proches_du_seuil:
        a(f"Proches du seuil de promotion ({rec.seuil}) :")
        for valeur, n, mq in rec.proches_du_seuil:
            a(f"- `{valeur}` : {n} page(s), il en manque {mq}.")
        a("")

    a("## L'occupation du gabarit")
    a("")
    a("La forme mesurable d'`existe_si` : on n'évalue pas la condition, on "
      "mesure son résultat. Une section **présente et vide partout** vaut le "
      "même diagnostic qu'une section absente partout.")
    a("")
    a("| rôle . section | conditionnelle | présente | remplie |")
    a("|---|---|---:|---:|")
    for o in sorted(occupations, key=lambda o: (o.role, o.titre)):
        if not o.population:
            continue
        a(f"| `{o.role}` . {o.titre} | {'oui' if o.conditionnelle else 'non'} | "
          f"{o.presentes}/{o.population} | {o.remplies}/{o.population} |")
    a("")

    a("## Le backlog")
    a("")
    a("Une liste de **travail**, pas un verdict. Rien ici n'est une violation.")
    a("")
    from .backlog import CODES
    groupes = bl.par_code()
    for code in sorted(groupes):
        a(f"### `{code}` — {CODES.get(code, '')}")
        a("")
        for e in groupes[code]:
            a(f"- `{e.sujet}` — {e.quoi}")
        a("")
    if not groupes:
        a("Vide.")
        a("")
    return L
