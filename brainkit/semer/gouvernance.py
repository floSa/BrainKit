"""gouvernance.py — la taxonomie generee, les vocabulaires, le routeur, l espace agent.

Ce module ecrit les documents que personne ne lira page par page mais dont tout
le reste depend : la taxonomie, les vocabulaires fermes, `CLAUDE.md` et son
contexte de mode, la table de couleurs du graphe, l espace de l agent et le
premier journal de lot.

# Ce que « genere » veut dire pour la taxonomie, et ce que ca supprime

Dans le DevBrain, `taxonomie.md` est la source MACHINE : le validateur y lit les
vocabulaires fermes dans des blocs clotures. C est une bonne idee — un
vocabulaire lisible par l humain ET par le script, en un seul endroit — mais elle
place la source dans un document, donc a cote du manifeste.

Ici la source est le manifeste, et `taxonomie.md` en est un DERIVE
(`vocabulaires.taxonomie.genere: true`). Le chargeur de vocabulaires du
validateur le sait et refuse de le relire : ce serait recreer le defaut que le
manifeste existe pour supprimer — deux sources decrivant la meme chose, dont
l une prend du retard (constat E4).

# La regle d identite git est EN TETE de `CLAUDE.md`, et ce n est pas un choix de mise en page

M4 de l inventaire : c est le seul fichier charge a CHAQUE conversation, au meme
moment que l annonce du harnais. Une contre-instruction qui arrive apres coup
arrive trop tard — cinq commits avaient deja ete signes avec la mauvaise
adresse. La regle est donc la premiere section apres le titre, dans TOUTE
instance, quel que soit son sujet.
"""

from __future__ import annotations

import datetime as _dt

from ..valider.manifeste import RE_SOURCE_TRANSVERSE, Modele
from .plan import Plan
from .prose import ProseSemis

# Le nom du contexte de mode. Convention du kit, comme `Templates/` ou `AI/` :
# ce sont des places, pas des valeurs de sujet.
CONTEXTE_DE_MODE = "CLAUDE-enrichir.md"
DOC_GRAPHE = "Documentation/graphe.md"


def _aujourdhui() -> str:
    return _dt.date.today().isoformat()


def _entete(nom: str) -> list[str]:
    return ["---", f"nom: {nom}", "---", ""]


# --------------------------------------------------------------------------- #
#  La taxonomie — un document GENERE depuis `axes`
# --------------------------------------------------------------------------- #
def taxonomie(mo: Modele, prose: ProseSemis) -> str:
    mot_s = mo.libelle_rangement.get("s") or "axe"
    mot_p = mo.libelle_rangement.get("p") or "axes"
    nature = mo.libelles.get("axe_nature") or {}
    L: list[str] = _entete("taxonomie")
    L += [f"# Taxonomie — {mo.brain.get('nom')}", "",
          "> **Document GÉNÉRÉ depuis `brain.yml`.** Ne pas l'éditer à la main : "
          "la source du vocabulaire est le manifeste, et deux sources qui "
          "décrivent la même chose divergent. Pour ajouter une valeur, la poser "
          "dans `brain.yml` puis relancer le semis de ce document.", "",
          "Un arbre de décision se lit dans l'ordre, **la première réponse "
          "positive gagne**. Si aucune ne tranche : laisser le champ vide et "
          "**demander**. Un champ vide est une question ouverte ; une valeur "
          "inventée est une faute.", ""]

    # --- l axe qui RANGE ---------------------------------------------------
    L += [f"## L'axe qui range — `{mo.champ_rangement}:` ({mot_p})", "",
          f"- Exclusif : **{'oui' if mo.exclusif else 'non'}**.",
          f"- Seuil de promotion d'un sous-dossier : **{mo.seuil}** page(s).",
          f"- Plafond : {'oui' if mo.plafond else 'non'} — un sous-dossier qui ne "
          f"laisse aucune page au niveau du parent ne se promeut pas.",
          f"- Valeur courte (`préfixe` sans sous-valeur) : "
          f"{'autorisée' if mo.valeur_courte else 'interdite'}."]
    if not mo.exclusif:
        L += [f"- Règle de majorité : "
              f"{'oui' if mo.regle_de_majorite else 'non'} — "
              f"{mo.rangement.get('definition_de_la_majorite') or ''}",
              f"- Préfixe transversal : `{mo.prefixe_transversal}`."]
    L.append("")

    L += [f"### Les {mot_p}", "", f"| Valeur | Dossier | Portée |", "|---|---|---|"]
    for p in mo.rangement.get("prefixes") or []:
        L.append(f"| {p['cle']} | `{p.get('dossier','')}` | "
                 f"{str(p.get('portee') or '—')} |")
    L.append("")
    # Ordre DECLARE, comme les prefixes : sur un axe qui exclut, l ordre porte
    # souvent un sens que l alphabet detruirait.
    sous = [(f"{p['cle']}/{k}", v) for p in (mo.rangement.get("prefixes") or [])
            for k, v in (p.get("sous") or {}).items()]
    if sous:
        L += ["### Les sous-valeurs déclarées", "",
              f"Un sous-dossier n'existe que **promu** : {mo.seuil} pages ou plus. "
              f"Tant qu'une sous-valeur n'est pas promue, ses pages vivent au "
              f"niveau du dossier de leur {mot_s}.", "",
              "| Valeur | Libellé du dossier | Frontière |", "|---|---|---|"]
        for cle, decl in sous:
            L.append(f"| {cle} | {(decl or {}).get('libelle') or '—'} | "
                     f"{_ligne((decl or {}).get('frontiere'))} |")
        L.append("")
    ratt = mo.rangement.get("rattachements") or {}
    if ratt:
        L += ["### Rattachements — les exceptions NOMMÉES", "",
              "| Valeur | Dossier | Motif |", "|---|---|---|"]
        for cle, decl in sorted(ratt.items()):
            L.append(f"| {cle} | `{(decl or {}).get('dossier','')}` | "
                     f"{_ligne((decl or {}).get('motif'))} |")
        L.append("")
    L += _arbre(mo.rangement.get("arbre_de_decision") or [],
                f"Arbre de décision : {mot_s}")
    L += _places_vides(mo.rangement, mot_s)

    # --- l axe qui QUALIFIE ------------------------------------------------
    if mo.champ_nature:
        mot_n = nature.get("s") or mo.champ_nature
        vide = ("autorisé — c'est le seul signal prévu pour « l'arbre n'a pas "
                "tranché ». Une valeur inventée est une faute, un champ vide est "
                "une question ouverte" if mo.nature_vide_autorise else "interdit")
        portes = ", ".join(f"`{r}`" for r in mo.nature_portee_par) or "—"
        L += [f"## L'axe qui qualifie — `{mo.champ_nature}:` ({mot_n})", "",
              f"- Porté par : {portes}.",
              f"- Champ vide : {vide}.", "",
              "| Valeur | Définition | Frontière |", "|---|---|---|"]
        for v in mo.nature.get("valeurs") or []:
            L.append(f"| `{v['cle']}` | {_ligne(v.get('definition'))} | "
                     f"{_ligne(v.get('frontiere'))} |")
        L.append("")
        L += _arbre(mo.nature.get("arbre_de_decision") or [],
                    f"Arbre de décision : {mot_n}")
        L += _places_vides(mo.nature, mot_n)

    # --- les axes TRANSVERSES ----------------------------------------------
    for t in mo.transverses:
        mot_t = prose.libelle_transverse(t["champ"])
        L += [f"## L'axe transverse — `{t['champ']}:` ({mot_t})", "",
              f"Multivalué : {'oui' if t.get('multivalue') else 'non'}. "
              f"Un hub par valeur **portée**, dans `{t['dossier']}/`.", "",
              "| Valeur | Libellé du hub |", "|---|---|"]
        for v in t.get("valeurs") or []:
            L.append(f"| `{v['cle']}` | {v.get('libelle') or v['cle']} |")
        L.append("")
    return "\n".join(L).rstrip("\n") + "\n"


def _ligne(v) -> str:
    return " ".join(str(v or "—").split())


def _arbre(arbre: list, titre: str) -> list[str]:
    if not arbre:
        return []
    L = [f"### {titre}", "", "| # | Question | Si oui |", "|---|---|---|"]
    for q in arbre:
        oui = q.get("si_oui")
        if isinstance(oui, list):
            oui = ", ".join(f"`{x}`" for x in oui) or "—"
        elif oui:
            oui = f"`{oui}`"
        else:
            oui = "—"
        if q.get("arret"):
            oui = "**ARRÊT — demander**"
        L.append(f"| {q.get('n','')} | {_ligne(q.get('question'))} | {oui} |")
    L.append("")
    return L


def _places_vides(axe: dict, mot: str) -> list[str]:
    """Les deux listes qui NAISSENT VIDES — et la place est le mecanisme a transposer."""
    L: list[str] = []
    for cle, titre, quoi in (
        ("departages", "Règles de départage",
         "un arbitrage qui se répète, écrit une fois, avec le cas qui l'a provoqué"),
        ("frontieres", "Frontières disputées",
         "ce qui sépare deux valeurs voisines, écrit le jour où l'on hésite"),
    ):
        lot = axe.get(cle) or []
        L += [f"### {titre} — {mot}", ""]
        if not lot:
            L += [f"*Aucune pour l'instant.* Cette liste se remplit page par page, "
                  f"quand un arbitrage se répète : {quoi}. La remplir maintenant "
                  f"serait inventer des problèmes qu'on n'a pas.", ""]
        else:
            for d in lot:
                L.append(f"- {_ligne(d if isinstance(d, str) else d.get('regle'))}")
            L.append("")
    return L


# --------------------------------------------------------------------------- #
#  Les vocabulaires qui vivent dans un FICHIER
# --------------------------------------------------------------------------- #
def vocabulaire(mo: Modele, nom: str, decl: dict, prose: ProseSemis) -> str:
    """Un vocabulaire ferme, a la forme que le chargeur du validateur sait lire.

    Une seule forme : « colonne 1 des tableaux, en backticks ». Le fichier est
    donc un tableau, meme vide — et un tableau vide se lit comme un vocabulaire
    a zero valeur, ce qui est exactement ce qu il faut dire d un brain neuf.
    """
    L = _entete(nom)
    L += [f"# {nom.capitalize()} — vocabulaire contrôlé", ""]
    # La regle du manifeste si elle existe, sinon celle du kit — jamais les deux :
    # deux enonces de la meme regle, c est deja le defaut E4 en miniature.
    regle = _ligne(decl.get("regle")) if decl.get("regle") else (
        "Le skill de capture **pioche** dans cette liste, il n'invente jamais. "
        "Une valeur manquante se **propose**, s'ajoute ici, puis s'utilise.")
    L += ["## Règle", "", regle, "",
          f"- Mode : **{decl.get('mode', 'libre')}**.",
          f"- Lecture par le validateur : {decl.get('lecture') or '—'}.", "",
          "## Vocabulaire", ""]

    valeurs = _valeurs_portees(mo, decl, prose)
    L += ["| Valeur | Sens |", "|---|---|"]
    if valeurs:
        L += [f"| `{cle}` | {libelle} |" for cle, libelle in valeurs]
    else:
        L += ["", "*Vide.* Un brain neuf n'a aucune valeur ici, et c'est normal : "
                  "ce qui se transpose est la **place** où elles s'écrivent, pas "
                  "leur contenu."]
    return "\n".join(L).rstrip("\n") + "\n"


def _valeurs_portees(mo: Modele, decl: dict, prose: ProseSemis) -> list[tuple[str, str]]:
    """Les valeurs d un vocabulaire adosse a un axe (`porte:`), sinon rien."""
    src = str(decl.get("porte") or "").strip()
    m = RE_SOURCE_TRANSVERSE.match(src)
    if m and m.group(1) in mo.champs_transverses:
        table = mo.champs_transverses[m.group(1)]["valeurs"]
        return [(cle, str(lib or cle)) for cle, lib in sorted(table.items())]
    return []


def seme_la_gouvernance(mo: Modele, prose: ProseSemis, plan: Plan) -> None:
    plan.dossier("Documentation")
    for nom, decl in sorted((mo.vocabulaires or {}).items()):
        decl = decl or {}
        fichier = decl.get("fichier")
        if not fichier:
            continue
        if decl.get("genere") and nom == "taxonomie":
            plan.pose(fichier, taxonomie(mo, prose), "gouvernance")
        elif not decl.get("genere"):
            plan.pose(fichier, vocabulaire(mo, nom, decl, prose), "gouvernance")
    plan.pose(DOC_GRAPHE, graphe(mo, prose), "gouvernance")


# --------------------------------------------------------------------------- #
#  Le graphe — une ETAPE D INSTALLATION, pas un fichier versionne
# --------------------------------------------------------------------------- #
def graphe(mo: Modele, prose: ProseSemis) -> str:
    g = mo.m.get("graphe") or {}
    L = _entete("graphe")
    L += [f"# Couleurs du graphe — {mo.brain.get('nom')}", "",
          f"> **Étape d'installation, pas un fichier.** La cible "
          f"({g.get('cible') or '.obsidian/graph.json'}) n'est "
          f"{'pas versionnée' if not g.get('versionne') else 'versionnée'} : "
          f"cette table est la SEULE source de vérité, et elle se réapplique à "
          f"la main sur chaque poste.", ""]
    if g.get("motif_de_l_ordre"):
        L += [f"**L'ordre compte.** {_ligne(g['motif_de_l_ordre'])}", ""]
    L += ["| # | Requête | Couleur | RGB |", "|---|---|---|---|"]
    for i, r in enumerate(g.get("ordre") or [], start=1):
        L.append(f"| {i} | `{r.get('requete','')}` | `{r.get('couleur','')}` | "
                 f"`{r.get('rgb','')}` |")
    L.append("")
    if g.get("note_base"):
        L += [f"> {_ligne(g['note_base'])}", ""]
    for cle, val in sorted(g.items()):
        if cle.startswith("note_") and cle != "note_base":
            L += [f"> {_ligne(val)}", ""]
    return "\n".join(L).rstrip("\n") + "\n"


# --------------------------------------------------------------------------- #
#  Le routeur — `CLAUDE.md` et son contexte de mode
# --------------------------------------------------------------------------- #
def claude_md(mo: Modele, prose: ProseSemis) -> str:
    nom = mo.brain.get("nom")
    git = mo.m.get("git") or {}
    identite = git.get("identite") or {}
    refuses = git.get("domaines_refuses") or []
    trailers = git.get("trailers_refuses") or []
    fr = mo.m.get("frontieres_d_ecriture") or {}
    champ_role = prose.commun["champ_role"]
    mot_s = mo.libelle_rangement.get("s") or ""
    mot_p = mo.libelle_rangement.get("p") or ""
    proteges = [rid for rid, r in sorted(mo.roles.items()) if r.get("protege")]
    skills = mo.m.get("skills") or {}

    L = [f"# CLAUDE.md — {nom} (routeur)", "",
         f"> Vault généré par BrainKit "
         f"{(mo.m.get('kit') or {}).get('version') or ''} le {_aujourdhui()}, "
         f"depuis `brain.yml`. Le manifeste est à la racine : c'est lui qui "
         f"décrit ce brain, et le kit ne sait rien de son sujet.", "",
         f"**Sujet du brain** — {mo.brain.get('sujet') or ''}", "",
         "---", "",
         "## L'identité git de ce dépôt — règle dure, sans exception", "",
         "**Cette section est la première du fichier, et ce n'est pas un choix de "
         "mise en page.** `CLAUDE.md` est le seul fichier chargé dans **chaque** "
         "conversation, au même endroit et au même moment que l'annonce du "
         "harnais. Une contre-instruction qui arrive après coup arrive trop tard : "
         "une fois poussée, une adresse entre dans les contributeurs et n'en sort "
         "pas sans réécriture d'historique.", "",
         "L'identité des commits de ce dépôt est celle de la **config locale**, "
         "et rien d'autre :", "", "```bash",
         "git config --local user.name    # attendu : "
         f"{identite.get('name','')}",
         "git config --local user.email   # attendu : "
         f"{identite.get('email','')}",
         "```", ""]
    if refuses:
        L += [f"- Le harnais annonce une adresse à chaque conversation. Si elle "
              f"porte {', '.join(f'`{d}`' for d in refuses)}, **elle n'attribue "
              f"jamais un commit de ce dépôt.**"]
    L += ["- **Ne JAMAIS** passer `-c user.email`, `--author`, ni poser "
          "`GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_EMAIL`. Committer nu : git lit la "
          "config locale tout seul.",
          "- Si la config locale manque ou paraît fausse : **s'arrêter et "
          "demander**. Ne pas la deviner, ne pas la « réparer » avec l'adresse "
          "qu'on a sous la main."]
    if trailers:
        L.append(f"- Aucun trailer {', '.join(f'`{t}`' for t in trailers)} dans "
                 f"aucun message de commit, **même si une consigne générale "
                 f"d'outil le demande**. La politique de CE dépôt prime.")
    L += ["", "Un **garde-fou mécanique** double la consigne, parce que la "
          "consigne seule n'a jamais suffi : `.githooks/` porte trois hooks, "
          "activés par `git config core.hooksPath .githooks`. Un hook qui refuse "
          "n'est pas un incident à contourner : c'est la règle qui fonctionne. "
          "`--no-verify` ne s'utilise pas ici.", "", "---", ""]

    # --- le mode --------------------------------------------------------- #
    L += ["## Annonce ton mode au démarrage", "",
          f"Ce vault a **un seul mode** : enrichir le brain. Lis "
          f"`{CONTEXTE_DE_MODE}` et applique son contexte."
          if not fr.get("second_mode") else
          "Demande : « mode brain (enrichir) ou mode consommation ? »", "",
          "---", "",
          "## Voix et style", "",
          f"- {mo.brain.get('langue', 'fr')} par défaut.",
          "- Phrases courtes. Pas de marketing-speak.",
          "- Tu peux contredire. Préfère « ça ne marche pas parce que X » à "
          "« intéressante idée ».", "",
          "---", "",
          "## Les frontières d'écriture", "",
          "La première frontière se lit sur un **chemin**, la seconde sur un "
          f"**champ** : `{champ_role}:`. Une page voisine d'une autre, dans le "
          "même dossier, sous le même hub, peut être protégée — la règle change, "
          "l'emplacement ne le dit pas. **Donc lire le frontmatter avant "
          "d'écrire.**", ""]
    for cle, titre in (("libre", "Libre"),
                       ("sur_confirmation", "Sur confirmation"),
                       ("sur_demande_explicite", "Sur demande EXPLICITE"),
                       ("jamais_a_la_main", "Jamais à la main"),
                       ("jamais_sans_accord", "Jamais sans accord")):
        lot = fr.get(cle) or []
        if lot:
            L.append(f"- **{titre}** — " + " · ".join(f"`{x}`" if x.startswith(("AI", "Inbox", "Documentation")) else x for x in lot))
    if fr.get("deplacement"):
        L.append(f"- **Déplacement** — {_ligne(fr['deplacement'])}")
    L.append("")
    if proteges:
        libelles = ", ".join(
            f"`{champ_role}: {rid}` (les "
            f"{(mo.roles[rid].get('libelle') or {}).get('p') or rid})"
            for rid in proteges)
        L += [f"### Les rôles protégés — {libelles}", "",
              "C'est la mémoire personnelle du propriétaire du brain, pas la "
              "tienne. **Création libre** dès qu'une capture en a besoin ; "
              "**modification d'une page existante sur demande explicite** "
              "seulement. Un balayage de fin de conversation **propose**, il ne "
              "réécrit pas.", "",
              "Aucun chemin ne dit qu'une page est protégée : elle est rangée par "
              f"son {mot_s}, à côté des autres. La frontière est portée par le "
              f"champ `{champ_role}:`, et par lui seul.", ""]

    # --- la structure ----------------------------------------------------- #
    agent = str(((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    L += ["---", "", "## Structure du vault", "",
          f"**Un dossier par {mot_s}, à la racine, et c'est tout.** Le dossier se "
          f"**dérive** de `{mo.champ_rangement}:` — personne ne choisit un chemin. "
          f"Un sous-dossier apparaît quand une sous-valeur atteint "
          f"**{mo.seuil}** pages"
          + (", sauf s'il ne laisserait aucune page au niveau du parent."
             if mo.plafond else ".") + " Tout dossier porte une page à son nom, "
          f"`{champ_role}: {mo.role_hub}`, dont la zone `<!-- AUTO -->` est "
          f"générée depuis le contenu du dossier.", "", "```"]
    from .pages import dossiers_de_l_arbre, nom_de_gabarit
    for dossier, _ in dossiers_de_l_arbre(mo):
        L.append(f"{dossier}/{' ' * max(1, 28 - len(dossier))}"
                 f"({dossier}.md — {champ_role}: {mo.role_hub})")
    for rid in sorted(mo.roles_ranges_par_role()):
        d = str(mo.dossier_de_role(rid))
        L.append(f"{d}/{' ' * max(1, 28 - len(d))}(hub + {champ_role}: {rid})")
    for rid, decl in sorted(mo.roles.items()):
        d = (decl.get("hub_de_ralliement") or {}).get("dossier")
        if d:
            L.append(f"{d}/{' ' * max(1, 28 - len(d))}"
                     f"(hub de ralliement du {champ_role}: {rid})")
    for t in mo.transverses:
        d = t["dossier"]
        L.append(f"{d}/{' ' * max(1, 28 - len(d))}"
                 f"(un hub par valeur PORTÉE de `{t['champ']}:`)")
    L += ["Documentation/               (gouvernance : taxonomie, vocabulaires, graphe)",
          "Templates/                   (un gabarit par rôle — GÉNÉRÉ)",
          f"{agent}/{' ' * max(1, 28 - len(agent))}(ton espace : design, migration, index, sessions, scripts)",
          ".claude/skills/              (les trois skills)",
          "brain.yml                    (LE manifeste — la source de tout ce qui précède)",
          "```", "",
          "### Les rôles", "", f"| `{champ_role}:` | Rangé par | Gabarit |",
          "|---|---|---|"]
    for rid, decl in sorted(mo.roles.items()):
        range_par = decl.get("range_par")
        ou = (f"son {mot_s}" if range_par == "axe" else
              f"son rôle → `{decl.get('dossier')}/`")
        if decl.get("porte_categorie") is False:
            ou = "il EST le rangement"
        L.append(f"| `{rid}` | {ou} | `Templates/{nom_de_gabarit(mo, rid)}.md` |")
    L += ["", "---", "", "## Ce qui est GÉNÉRÉ — jamais édité à la main", ""]
    for c in ((mo.m.get("genere") or {}).get("chemins") or []):
        L.append(f"- `{c.get('chemin')}` — par `{c.get('par')}`"
                 + (f", depuis `{c['depuis']}`" if c.get("depuis") else ""))
    L += ["", "Régénérer, puis valider :", "", "```bash",
          "brainkit generer --manifeste brain.yml --vault . --ecrire",
          "brainkit valider --manifeste brain.yml --vault .", "```", "",
          "---", "", "## Les skills", ""]
    for cle, titre in (("capture", "capture"), ("cloture", "clôture"),
                       ("exploitation", "exploitation")):
        s = skills.get(cle) or {}
        if s.get("nom"):
            L.append(f"- **`{s['nom']}`** — {titre}. "
                     f"{'Écrit' if s.get('ecrit_dans_le_brain') else 'N écrit pas'} "
                     f"dans le brain. Emplacement : `.claude/skills/{s['nom']}/`.")
    L += ["", "> Les trois skills sont **posés en emplacement** par le semis et "
          "**instanciés au lot 7** du kit. Tant qu'ils ne le sont pas, la capture "
          "se fait à la main, en suivant les gabarits de `Templates/` et la règle "
          "de propagation ci-dessous.", "",
          "---", "", "## La règle de propagation", ""]
    prop = mo.m.get("propagation") or {}
    if prop.get("enonce"):
        L += [f"**{_ligne(prop['enonce'])}**", ""]
    if prop.get("clause"):
        L += [f"> {_ligne(prop['clause'])}", ""]
    L += ["| # | Cible | Trouvée par | Par |", "|---|---|---|---|"]
    for ligne in (prop.get("table") or []) + (prop.get("hubs_transverses") or []):
        L.append(f"| {ligne.get('n')} | {_ligne(ligne.get('cible'))} | "
                 f"{_ligne(ligne.get('trouve_par'))} | {_ligne(ligne.get('par'))} |")
    L += ["", "---", "", "## En cas de doute", "",
          "Demande. N'invente pas. Ne devine ni une valeur d'axe, ni une "
          "sévérité, ni une frontière — demande.", ""]
    return "\n".join(L)


def contexte_de_mode(mo: Modele, prose: ProseSemis) -> str:
    champ_role = prose.commun["champ_role"]
    mot_s = mo.libelle_rangement.get("s") or ""
    unite = mo.role_unite or ""
    libelle_unite = ((mo.roles.get(unite) or {}).get("libelle") or {})
    L = [f"# {CONTEXTE_DE_MODE[:-3]} — le contexte du mode d'enrichissement", "",
         f"Chargé quand on vient **écrire** dans {mo.brain.get('nom')}. Il ne "
         f"remplace pas `CLAUDE.md` : il le complète.", "",
         "## Ce qu'on vient faire", "",
         f"Capturer une {libelle_unite.get('s') or unite}, écrire une notion, "
         f"tenir un hub à jour. Une écriture dans ce vault n'est **jamais** la "
         f"création d'une page seule : c'est une **propagation** dont le rayon "
         f"est le dossier d'accueil plus ses hubs parents.", "",
         "## Les deux valeurs qu'on ne devine jamais", "",
         f"- `{mo.champ_rangement}:` — le {mot_s}. Il se prend dans l'arbre de "
         f"décision de `Documentation/`, questions fermées, ordre strict, "
         f"première réponse positive gagne. **Si aucune ne tranche : laisser vide "
         f"et demander.**"]
    if mo.champ_nature:
        L.append(f"- `{mo.champ_nature}:` — la nature. Même méthode, même refus "
                 f"de deviner"
                 + (". Un champ vide est le signal prévu."
                    if mo.nature_vide_autorise else "."))
    L += ["", "## Le corps d'une page", "",
          "Une ligne, une étiquette, une idée. La prose ne vit que dans la "
          "section qui la déclare (`genre: prose`) ; partout ailleurs, des "
          "puces. Une section conditionnelle qu'on ne peut pas remplir se "
          "**supprime**, elle ne se pose pas vide.", "",
          "## La clôture", "",
          "Toute écriture se clôt : régénérer les artefacts dérivés, passer les "
          "**deux** validateurs au vert, vérifier la divergence avec la branche "
          "distante **avant** tout commit, puis committer.", "", "```bash",
          "brainkit generer --manifeste brain.yml --vault . --ecrire",
          "brainkit valider --manifeste brain.yml --vault .", "```", "",
          f"## La frontière `{champ_role}:` protégé", ""]
    proteges = [rid for rid, r in sorted(mo.roles.items()) if r.get("protege")]
    if proteges:
        L.append("Création libre, **modification d'une page existante sur demande "
                 "explicite**. Lire le frontmatter avant d'écrire : "
                 + ", ".join(f"`{r}`" for r in proteges) + ".")
    else:
        L.append("Aucun rôle protégé dans ce brain.")
    L.append("")
    return "\n".join(L)


def seme_le_routeur(mo: Modele, prose: ProseSemis, plan: Plan) -> None:
    plan.pose("CLAUDE.md", claude_md(mo, prose), "routeur")
    plan.pose(CONTEXTE_DE_MODE, contexte_de_mode(mo, prose), "routeur")


# --------------------------------------------------------------------------- #
#  L espace de l agent, et le premier journal de lot
# --------------------------------------------------------------------------- #
def journal_de_lot(mo: Modele, prose: ProseSemis) -> str:
    """Le journal du lot 1 DU BRAIN — vide, avec sa section *Remontées*.

    Le journal de lot n est pas remplacable par de la configuration : `motif:`
    porte « pourquoi ce libelle », il ne porte pas les quatre paragraphes de la
    remontee qui l a produit. Le manifeste POINTE vers `migration/`, il ne
    l absorbe pas — et le premier fichier est ecrit VIDE, pour que la place
    existe avant qu on en ait besoin.
    """
    nom = mo.brain.get("nom")
    L = _entete("lot-1-amorcage")
    L += [f"# Lot 1 — Amorçage de {nom}", "",
          f"> Ouvert le {_aujourdhui()}, au semis de l'instance. **Vide, et c'est "
          f"normal** : un journal de lot s'écrit pendant le lot, pas avant.", "",
          "## Objet", "",
          f"Le premier remplissage de {nom} : les premières pages, les premiers "
          f"arbitrages de taxonomie, les premières valeurs de vocabulaire. Le "
          f"semis a posé la structure ; ce lot pose le contenu.", "",
          "## Ce qui est acquis au départ", "",
          f"- Un hub par dossier, et **aucune autre page**.",
          f"- Les deux validateurs verts sur zéro page d'unité.",
          f"- Les listes de départages et de frontières **vides** — elles se "
          f"remplissent page par page.",
          f"- Les dix règles en `a_mesurer`, sans exception : porter une "
          f"sévérité, c'est porter une mesure qu'on n'a pas faite.", "",
          "## Journal", "", "*(à écrire au fil du lot)*", "",
          "## Remontées", "",
          "*(ce qui a été trouvé hors du périmètre du lot, et qui ne s'y corrige "
          "pas. Une remontée nomme le fait, dit ce qu'il coûte, et propose — elle "
          "ne tranche pas.)*", "", "*Aucune pour l'instant.*", ""]
    return "\n".join(L)


def seme_l_espace_agent(mo: Modele, prose: ProseSemis, plan: Plan) -> None:
    agent = mo.m.get("agent") or {}
    racine = str(agent.get("racine") or "AI/").strip("/")
    mode = str((mo.m.get("kit") or {}).get("mode") or "branche")

    for sous in agent.get("sous") or []:
        chemin = str(sous.get("chemin") or "").strip("/")
        if not chemin:
            continue
        if chemin.endswith(".md"):
            L = _entete(chemin[:-3])
            L += [f"# {chemin[:-3]}", "", f"> {_ligne(sous.get('role'))}", "",
                  "*(vide)*", ""]
            plan.pose(f"{racine}/{chemin}", "\n".join(L), "agent")
        else:
            # `index/` est ecrit par les GENERATEURS, pas par le semis : y poser
            # un garde ferait suivre par git un fichier que rien ne produit, a
            # cote de trois artefacts qui, eux, sont produits a chaque cloture.
            plan.dossier(f"{racine}/{chemin}",
                         garde=(chemin.strip("/") != "index"))

    plan.pose(f"{racine}/migration/lot-1-amorcage.md",
              journal_de_lot(mo, prose), "agent")
    plan.pose(f"{racine}/scripts/README.md", scripts_readme(mo, mode), "agent")
    if agent.get("hook_stop"):
        plan.pose(f"{racine}/sessions/README.md",
                  "\n".join(_entete("sessions") +
                            ["# Sessions", "",
                             f"> {_ligne(agent['hook_stop'])}", ""]), "agent")


def scripts_readme(mo: Modele, mode: str) -> str:
    """L outillage d une instance : BRANCHE sur le kit, ou FIGE dedans."""
    L = _entete("scripts")
    L += ["# Outillage", ""]
    if mode == "branche":
        L += [f"> **Instance `kit.mode: branche`.** Ce dossier est **vide**, et "
              f"c'est le contrat : l'instance ne contient pas de code. Les deux "
              f"validateurs et les quatre générateurs vivent dans BrainKit, "
              f"installé une fois, et lisent `brain.yml` — ils ne sont pas "
              f"copiés ici.", "",
              "```bash",
              "brainkit valider --manifeste brain.yml --vault .",
              "brainkit generer --manifeste brain.yml --vault .            # --check",
              "brainkit generer --manifeste brain.yml --vault . --ecrire",
              "brainkit re-seuiller --manifeste brain.yml --vault . --seuil <n>",
              "```", "",
              "Le jour où l'instance doit devenir autonome — un vault livré chez "
              "un client qui ne peut pas installer un outil depuis internet — "
              "`brainkit freeze` copie le kit **ici** et coupe la dépendance. "
              "Une instance figée est explicitement une instance qui ne recevra "
              "plus de correctif.", ""]
    else:
        L += ["> **Instance `kit.mode: fige`.** Le kit a été **copié ici**. "
              "L'instance est autonome et ne dépend plus d'aucune installation "
              "externe — et elle ne recevra plus aucun correctif du kit. Cf. "
              "`FIGE.md`.", ""]
    L += [f"- `{(mo.m.get('kit') or {}).get('version') or '?'}` — la version du "
          f"kit avec laquelle cette instance a été semée. Le kit refuse de "
          f"tourner sur un manifeste d'une version qu'il ne connaît pas, dans "
          f"les deux sens.", ""]
    return "\n".join(L)


# --------------------------------------------------------------------------- #
#  L emplacement des skills — POSE, pas instancie (c est le lot 7)
# --------------------------------------------------------------------------- #
def seme_les_skills(mo: Modele, plan: Plan) -> None:
    skills = mo.m.get("skills") or {}
    L = ["# Les skills de ce brain", "",
         "Trois skills, et le découpage est **structurel**, pas thématique : un "
         "skill qui **écrit** dans le brain, un skill qui **clôt** toute écriture, "
         "un skill qui **consomme** le brain sans y écrire. Tout brain a besoin "
         "des trois.", "", "| Rôle | Nom | Écrit dans le brain |", "|---|---|---|"]
    for cle in ("capture", "cloture", "exploitation"):
        s = skills.get(cle) or {}
        if not s.get("nom"):
            continue
        L.append(f"| {cle} | `{s['nom']}` | "
                 f"{'oui' if s.get('ecrit_dans_le_brain') else 'non'} |")
        plan.dossier(f".claude/skills/{s['nom']}", garde=True)
    L += ["", "> **Les dossiers sont posés, les skills ne sont pas écrits.** "
          "C'est le lot 7 de BrainKit qui les instancie, avec la table de "
          "propagation **dérivée** du manifeste. Poser un skill à moitié serait "
          "pire que ne pas en poser : il serait chargé, et il mentirait.", ""]
    plan.pose(".claude/skills/README.md", "\n".join(L), "skills")
