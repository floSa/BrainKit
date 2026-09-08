"""exigences.py — ce que le semis EXIGE du manifeste, verifie AVANT d ecrire.

# Pourquoi cette passe existe, et pourquoi elle est separee

Le contrat du lot 1 (`schema/brain.schema.json`) dit si un manifeste est BIEN
FORME. Il ne dit pas s il est SEMABLE. Les deux ne se recouvrent pas : un
manifeste peut satisfaire le schema et ne pas declarer le dossier d un role
`range_par: role` — le schema le tolere parce qu un manifeste peut n en avoir
aucun, le semis ne le peut pas parce qu il devrait alors inventer un nom de
dossier.

L interdiction du lot est explicite : **un manifeste incomplet doit etre refuse,
pas seme a moitie.** Un semis qui pose douze dossiers puis s arrete sur le
treizieme laisse un vault a demi ecrit, dont les deux validateurs diront
n importe quoi. Cette passe rend donc TOUS ses refus d un coup, avant que le
plan d ecriture existe.

# Les refus ne sont pas des regles de validation

Aucun de ces controles n est une regle du validateur, et aucun n en change une.
Ce sont des PRE-CONDITIONS de generation : « pour poser ce fichier, il me faut
cette declaration ». Un manifeste refuse ici reste un manifeste valide au sens
du lot 1 — il est simplement incomplet pour ce que le lot 5 doit produire.
"""

from __future__ import annotations

from ..valider.manifeste import GENRE_AUTO, Modele
from ..valider.vocabulaires import _lecture_connue

# Les dossiers que le semis ecrit et qui ne portent PAS de page d unite. Le
# validateur enumere son perimetre par la negative (`genere.non_pages`) : si l un
# d eux manque a cette liste, ses fichiers seront lus comme des pages, et un
# gabarit de `Templates/` — qui porte volontairement des valeurs a trous — sera
# compte comme une page fautive.
# `docs` a rejoint la liste au lot 10, parce que le semis y ecrit desormais les
# trois guides. Ce n est pas un ajout de confort : un guide n a ni role ni
# valeur d axe, donc lu comme une page il violerait le gabarit de tous les
# roles a la fois.
DOSSIERS_HORS_PAGES = ("Templates", "Documentation", "docs")


def controle(mo: Modele) -> list[str]:
    """Tous les manques, d un coup. Liste vide = le manifeste est semable."""
    r: list[str] = []
    r += _identite(mo)
    r += _roles(mo)
    r += _rangement(mo)
    r += _transverses(mo)
    r += _racine(mo)
    r += _gouvernance(mo)
    r += _ponts(mo)
    return r


def _ponts(mo: Modele) -> list[str]:
    """Les alias de `agent.ponts` visent-ils une cible que le kit sait ponter ?

    Un pont vers une cible inventee serait un fichier qui ne tourne pas, pose
    dans l espace de l agent, nomme par un skill. Le refuser AVANT d ecrire est
    la seule facon de ne pas livrer ca.
    """
    from . import ponts as _p
    return _p.manques(mo)


# --------------------------------------------------------------------------- #
def _identite(mo: Modele) -> list[str]:
    r: list[str] = []
    if mo.version != 1:
        r.append(f"`manifeste: {mo.version}` — le kit ne sait semer que la version 1")
    if not (mo.brain.get("nom") or "").strip():
        r.append("`brain.nom` manquant — c'est le nom du vault et de son dépôt")
    if not (mo.brain.get("langue") or "").strip():
        r.append("`brain.langue` manquant")

    git = mo.m.get("git") or {}
    identite = git.get("identite") or {}
    for cle in ("name", "email"):
        if not str(identite.get(cle) or "").strip():
            r.append(f"`git.identite.{cle}` manquant — l'identité d'un dépôt ne "
                     f"se devine JAMAIS, et surtout pas depuis l'adresse annoncée "
                     f"par le harnais (refus n° 1 de l'entretien, §3.5)")
    if not git.get("branche_principale"):
        r.append("`git.branche_principale` manquant — le dépôt de l'instance "
                 "naîtrait sur la branche par défaut de la machine")
    return r


def _roles(mo: Modele) -> list[str]:
    r: list[str] = []
    rid_hub = mo.role_hub
    if rid_hub is None:
        r.append("aucun rôle `fonction: hub` — un vault sans hub n'a pas d'aiguillage, "
                 "et le semis n'a rien à poser dans ses dossiers")
        return r

    section = mo.section_de_genre(rid_hub, GENRE_AUTO)
    if section is None:
        r.append(f"le rôle `{rid_hub}` ne déclare aucune section `genre: auto` — "
                 f"les hubs semés n'auraient pas de zone régénérable, et le "
                 f"générateur les REFUSERAIT à la première clôture")
    else:
        bal = section.get("balises")
        if not bal or len(bal) != 2:
            r.append(f"la section `genre: auto` du rôle `{rid_hub}` ne déclare pas "
                     f"ses deux balises")

    # Le semis remplit un hub avec trois choses, et trois seulement : son role,
    # son identite, son resume court. Un champ REQUIS hors de ces trois ne peut
    # etre ni devine ni laisse vide — `gabarit_par_role` refuserait la page.
    connus = {mo.champ_de_fonction("identite"), mo.champ_de_fonction("resume_court")}
    for champ in mo.requis(rid_hub):
        d = mo.champ(champ)
        if str(d.get("source") or "").strip() == "roles[].id":
            continue
        if champ in connus:
            continue
        r.append(f"le rôle `{rid_hub}` exige `{champ}:`, qu'aucune `fonction:` du "
                 f"dictionnaire de champs ne désigne — le semis devrait l'inventer, "
                 f"et une valeur inventée dans un hub est exactement ce que la "
                 f"règle du tiret cadratin interdit")

    for rid in mo.roles_ranges_par_role():
        if not mo.dossier_de_role(rid):
            r.append(f"le rôle `{rid}` est `range_par: role` sans `dossier:` — "
                     f"son chemin se lit sur son rôle, encore faut-il le nommer")
    for rid, decl in sorted(mo.roles.items()):
        ral = decl.get("hub_de_ralliement")
        if ral is not None and not ral.get("dossier"):
            r.append(f"le rôle `{rid}` déclare un `hub_de_ralliement` sans `dossier:`")
    return r


def _rangement(mo: Modele) -> list[str]:
    r: list[str] = []
    if not mo.champ_rangement:
        r.append("`axes.rangement.champ` manquant")
    prefixes = mo.rangement.get("prefixes") or []
    if not prefixes:
        r.append("`axes.rangement.prefixes` vide — le semis n'a aucun dossier à poser")
    for i, p in enumerate(prefixes):
        if not (p or {}).get("cle"):
            r.append(f"`axes.rangement.prefixes[{i}].cle` manquant")
        if not (p or {}).get("dossier"):
            r.append(f"`axes.rangement.prefixes[{i}].dossier` manquant — le dossier "
                     f"d'accueil ne se dérive pas d'une clé, il se déclare")
    if not mo.seuil:
        r.append("`axes.rangement.seuil_promotion` manquant ou nul — `re-seuiller` "
                 "n'aurait aucune valeur de départ")
    if not mo.exclusif and not mo.prefixe_transversal:
        r.append("`axes.rangement.exclusif: false` sans `prefixe_transversal:` — "
                 "une page sans centre de gravité n'aurait nulle part où aller "
                 "(rupture 3 du test à blanc)")
    return r


def _transverses(mo: Modele) -> list[str]:
    """Zero axe transverse est LEGAL. Un axe mal declare ne l est pas."""
    r: list[str] = []
    dossiers: dict[str, str] = {}
    for i, t in enumerate(mo.transverses):
        champ = (t or {}).get("champ")
        dossier = (t or {}).get("dossier")
        if not champ:
            r.append(f"`axes.transverses[{i}].champ` manquant")
        if not dossier:
            r.append(f"`axes.transverses[{i}].dossier` manquant")
            continue
        if dossier in dossiers:
            r.append(f"deux axes transverses partagent le dossier `{dossier}` "
                     f"(`{dossiers[dossier]}` et `{champ}`)")
        dossiers[dossier] = str(champ)
    # La contrainte de nommage de la rupture 4, rendue mecanique : aucun dossier
    # d axe transverse ne peut porter le nom d un dossier de l arbre. Le DevBrain
    # a nomme `Métiers/` plutot que `Domaines/` pour cette raison exacte.
    arbre = set(mo.dossier_de_prefixe.values())
    for dossier, champ in sorted(dossiers.items()):
        if dossier in arbre:
            r.append(f"l'axe transverse `{champ}` veut le dossier `{dossier}`, "
                     f"déjà porté par l'arbre de rangement")
    return r


def _racine(mo: Modele) -> list[str]:
    """La porte d entree — arbitrage 1 du lot 5, cf. `design/05-semis.md`."""
    r: list[str] = []
    bloc = mo.m.get("racine")
    if not bloc:
        r.append("bloc `racine:` absent — le semis ne sait pas quelle page est la "
                 "porte d'entrée du vault, et c'est elle qui cite les hubs de "
                 "premier niveau (remontée 3 du lot 4, tranchée au lot 5)")
        return r
    porte = str(bloc.get("porte_d_entree") or "").strip()
    pages = bloc.get("pages") or []
    fichiers = [str((p or {}).get("fichier") or "") for p in pages]
    if not porte:
        r.append("`racine.porte_d_entree` manquant")
    elif porte not in fichiers:
        r.append(f"`racine.porte_d_entree: {porte}` n'est pas dans `racine.pages[]`")
    for i, p in enumerate(pages):
        p = p or {}
        if not p.get("fichier"):
            r.append(f"`racine.pages[{i}].fichier` manquant")
        elif not str(p["fichier"]).endswith(".md"):
            r.append(f"`racine.pages[{i}].fichier` n'est pas un `.md`")
        if not p.get("titre"):
            r.append(f"`racine.pages[{i}].titre` manquant")
    # Les dossiers d ATELIER (lot 6) : declares, vides, et HORS du perimetre du
    # validateur. Sans la seconde condition, le contenu d un carnet de notes
    # serait lu comme des pages fautives — un dossier d atelier ne porte ni
    # role ni categorie, par definition.
    for i, d in enumerate(bloc.get("dossiers") or []):
        chemin = str((d or {}).get("chemin") or "").strip("/")
        if not chemin:
            r.append(f"`racine.dossiers[{i}].chemin` manquant")
            continue
        tete = chemin.split("/")[0]
        if tete not in mo.non_pages:
            r.append(f"`racine.dossiers[{i}]` déclare `{chemin}/` sans que "
                     f"`{tete}` soit dans `genere.non_pages` — le validateur "
                     f"lirait son contenu comme des pages, et un dossier "
                     f"d'atelier ne porte ni rôle ni catégorie")

    if porte and not any((p or {}).get("aiguille") for p in pages):
        r.append("aucune page de `racine.pages[]` ne porte `aiguille: true` — les "
                 "hubs de premier niveau ne seraient cités par personne")
    return r


def _gouvernance(mo: Modele) -> list[str]:
    r: list[str] = []
    racine_agent = str(((mo.m.get("agent") or {}).get("racine") or "")).strip("/")
    if not racine_agent:
        r.append("`agent.racine` manquant — le semis ne sait pas où poser l'espace "
                 "de l'agent (design, migration, index, sessions, scripts)")
    attendus = set(DOSSIERS_HORS_PAGES) | ({racine_agent} if racine_agent else set())
    for nom in sorted(attendus):
        if nom not in mo.non_pages:
            r.append(f"`{nom}` est écrit par le semis mais absent de "
                     f"`genere.non_pages` — le validateur le lirait comme un "
                     f"dossier de pages, et les gabarits à trous compteraient "
                     f"comme des pages fautives")

    for nom, decl in sorted((mo.vocabulaires or {}).items()):
        decl = decl or {}
        if decl.get("genere"):
            continue
        if not decl.get("fichier"):
            r.append(f"`vocabulaires.{nom}.fichier` manquant — le semis ne sait pas "
                     f"où poser ce vocabulaire")
        if decl.get("mode") == "ferme" and not _lecture_connue(str(decl.get("lecture") or "")):
            r.append(f"`vocabulaires.{nom}` est `ferme` sans `lecture:` que le "
                     f"moteur sache appliquer — le fichier semé serait ILLISIBLE, "
                     f"et `vocabulaire_ferme` le dirait dès la première validation")

    graphe = mo.m.get("graphe") or {}
    if not graphe.get("ordre"):
        r.append("`graphe.ordre` manquant — la table de couleurs est la SEULE "
                 "source de vérité du graphe (le fichier cible est gitignoré), "
                 "donc le semis doit l'écrire dans l'étape d'installation")
    return r
