"""pages.py — les pages du semis : les hubs, les gabarits, la porte d entree.

Trois familles, trois provenances, et aucune n est du contenu :

| famille            | depuis quoi                                      |
|---|---|
| les hubs de l arbre | `axes.rangement.prefixes[]`                     |
| les hubs de role    | `roles[].dossier` (`range_par: role`)           |
| les hubs de ralliement | `roles[].hub_de_ralliement.dossier`          |
| les gabarits       | `roles[].champs` et `roles[].corps`              |
| la porte d entree  | `racine.pages[]`                                 |

# Le point fixe, et pourquoi il se verifie au lieu de se croire

Un hub seme porte deja sa zone AUTO **remplie comme le generateur la remplirait
sur un dossier vide**. Ce n est pas une coquetterie : le critere d acceptation du
lot dit qu un semis qui n est pas deja a son point fixe est un semis faux. Si la
zone etait posee vide, `brainkit generer --check` sortirait en 2 sur un vault qui
vient de naitre, et le premier geste de l utilisateur serait de reparer quelque
chose que personne n a cassé.

Les deux formes possibles sur un dossier a zero page sont donc calquees sur
`generer/hubs.py`, et sur lui seul :

  - forme ARBRE      -> `hubs.dossier_vide`   (« *(dossier vide)* »)
  - forme RALLIEMENT -> `hubs.aucune_page`    (« *(aucune page `role: x`)* »)

Elles sont lues dans la MEME table de prose que celle du generateur, ce qui
interdit qu elles divergent : une surcharge `genere.prose.hubs.dossier_vide`
change les deux d un coup.

# Ce que le semis n ecrit PAS

Aucun sous-dossier. L arbre naît **plat** : un dossier par prefixe declare, et
rien en dessous. Un sous-dossier n existe que promu, et la promotion se calcule
sur une population de pages (`chemins.promotions`) qui vaut zero le jour du
semis. Poser d avance les dossiers des sous-valeurs declarees creerait des
dossiers que la derivation ne reconnaitrait pas, et que `re-seuiller` proposerait
aussitot de defaire.

Aucun hub d axe transverse non plus — cf. `semis.py`, arbitrage 2.
"""

from __future__ import annotations

from ..valider.manifeste import GENRE_AUTO, Modele
from .plan import Plan
from .prose import ProseSemis

QUOI = "pages"

# Un titre de section entre chevrons n est pas un titre : c est une PLACE. Le
# manifeste s en sert pour le bandeau, la zone AUTO, l embed d une vue et
# l accroche d une page — quatre choses qui ne portent pas de `##`.
def _est_une_place(titre: str) -> bool:
    return titre.startswith("<") and titre.endswith(">")


# Ce qui, dans une valeur, oblige a quoter un scalaire YAML. La liste est courte
# et le motif est mesure : c est un `pitch:` non quote contenant « : » qui a
# rendu une page du vault d'origine illisible, hors du total et hors de TOUTES les
# regles — sans que rien ne le signale (R17). Un semis qui poserait une page
# illisible ferait pire que le bug d origine : il le ferait en serie.
_DANGEREUX = (": ", " #", "\n", '"', "'")


def _scalaire(v: str) -> str:
    """Une valeur de frontmatter, quotee SI ET SEULEMENT SI elle en a besoin."""
    s = str(v)
    if not s:
        return '""'
    if s.endswith(":") or s[0] in "-?[]{}&*!|>%@`\"' " or s[-1] == " ":
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    for d in _DANGEREUX:
        if d in s:
            return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


# --------------------------------------------------------------------------- #
#  Les hubs
# --------------------------------------------------------------------------- #
def zone_auto_vide(mo: Modele, prose: ProseSemis, ralliement: str | None) -> list[str]:
    """Le contenu de la zone AUTO d un hub SUR UN DOSSIER VIDE, calque du générateur."""
    if ralliement is not None:
        return [prose.ligne("hubs.aucune_page", role=ralliement)]
    return [prose.ligne("hubs.dossier_vide")]


def hub(mo: Modele, prose: ProseSemis, titre: str, apport: str,
        ralliement: str | None = None) -> str:
    """Une page `fonction: hub`, avec ses sections manuelles et sa zone AUTO."""
    rid = mo.role_hub or "hub"
    champ_role = prose.commun["champ_role"]
    identite = mo.champ_de_fonction("identite")
    resume = mo.champ_de_fonction("resume_court")

    lignes = ["---", f"{champ_role}: {rid}"]
    for champ in mo.requis(rid):
        if champ == champ_role:
            continue
        if champ == identite:
            lignes.append(f"{champ}: {_scalaire(titre)}")
        elif champ == resume:
            lignes.append(f"{champ}: {_scalaire(apport)}")
    lignes += ["---", "", f"# {titre}", "", f"> {apport}", ""]

    section_auto = mo.section_de_genre(rid, GENRE_AUTO)
    for s in mo.corps(rid):
        if s.get("genre") == GENRE_AUTO:
            continue
        t = mo.titre(s)
        if _est_une_place(t):
            continue
        niveau = int(s.get("niveau") or 2)
        lignes += ["#" * niveau + f" {t}", "",
                   prose.ligne("semis.hub.a_ecrire", titre=t), ""]

    bal = (section_auto or {}).get("balises") or []
    lignes.append(bal[0])
    lignes += zone_auto_vide(mo, prose, ralliement)
    lignes += [bal[1], ""]
    return "\n".join(lignes)


def dossiers_de_l_arbre(mo: Modele) -> list[tuple[str, str]]:
    """(dossier, resume) par dossier de l arbre, DEDUPLIQUE, dans l ORDRE DECLARE.

    Deduplique parce qu un rattachement peut partager le dossier d un prefixe :
    deux valeurs d axe rangees dans le meme dossier font deux entrees, un seul
    dossier, un seul hub.

    Dans l ordre DECLARE, et pas alphabetique : l ordre des prefixes est une
    decision de l utilisateur, et sur un axe qui exclut il porte souvent un
    sens — un axe ordonne (« 1, 2, 3 ») n est pas la meme liste une fois trie
    par son libelle. Trier detruirait cette information sans rien apporter.
    """
    vus: dict[str, str] = {}
    for p in mo.rangement.get("prefixes") or []:
        dossier = str(p.get("dossier") or "")
        if dossier and dossier not in vus:
            vus[dossier] = str(p.get("portee") or "").strip()
    return list(vus.items())


def seme_les_hubs(mo: Modele, prose: ProseSemis, plan: Plan) -> None:
    """Un dossier et son hub par dossier de l arbre, de role, et de ralliement."""
    mot = mo.libelle_rangement.get("s") or ""

    for dossier, portee in dossiers_de_l_arbre(mo):
        apport = portee or prose.ligne("semis.hub.apport_arbre",
                                       libelle=dossier, axe_rangement=mot)
        plan.dossier(dossier)
        plan.pose(f"{dossier}/{dossier}.md", hub(mo, prose, dossier, apport), QUOI)

    for rid in sorted(mo.roles_ranges_par_role()):
        dossier = str(mo.dossier_de_role(rid))
        libelle = (mo.roles[rid].get("libelle") or {})
        apport = prose.ligne("semis.hub.apport_role",
                             libelle_p=libelle.get("p") or rid)
        plan.dossier(dossier)
        plan.pose(f"{dossier}/{dossier}.md", hub(mo, prose, dossier, apport), QUOI)

    for rid, decl in sorted(mo.roles.items()):
        ral = decl.get("hub_de_ralliement") or {}
        dossier = ral.get("dossier")
        if not dossier:
            continue
        libelle = (decl.get("libelle") or {})
        apport = prose.ligne("semis.hub.apport_ralliement",
                             libelle_p=libelle.get("p") or rid)
        plan.dossier(dossier)
        plan.pose(f"{dossier}/{dossier}.md",
                  hub(mo, prose, dossier, apport, ralliement=rid), QUOI)


# --------------------------------------------------------------------------- #
#  Les gabarits — un par role, depuis `champs` et `corps`
# --------------------------------------------------------------------------- #
def nom_de_gabarit(mo: Modele, rid: str) -> str:
    """`Templates/Gabarit - <libelle>.md`.

    Le prefixe existe pour une raison mesuree : un gabarit nomme d apres son
    role (« Notion.md ») porterait le nom d une page probable du vault, et la
    convention de wikilink NU ne resout plus de facon deterministe deux fichiers
    homonymes. `Templates/` est hors du perimetre du validateur, donc la
    violation ne serait pas SIGNALEE — ce qui est pire, pas mieux.
    """
    libelle = ((mo.roles.get(rid) or {}).get("libelle") or {}).get("s") or rid
    return f"Gabarit - {libelle[0].upper()}{libelle[1:]}"


def _ligne_de_gabarit(mo: Modele, champ: str, titre_token: str,
                      taxonomie: str) -> str:
    """La ligne d amorce d un champ dans un gabarit. Jamais une valeur plausible.

    Un champ enumere ne recoit PAS la liste de ses valeurs, et c est le refus
    n° 3 de l entretien applique au gabarit : *jamais de liste a cocher*. Une
    liste sous les yeux fait choisir la valeur qui ressemble le plus ; l arbre de
    decision fait repondre a des questions fermees, dans un ordre strict, et
    l ordre EST la decision de conception. Le gabarit renvoie donc a l arbre.
    """
    d = mo.champ(champ)
    typ = str(d.get("type") or "ligne")
    if d.get("fonction") == "identite":
        return f"{champ}: {titre_token}"
    if typ in ("liste", "liste_enum", "liens"):
        return f"{champ}: []"
    if typ == "enum":
        voc = mo.vocabulaire(champ)
        n = f"{len(voc)} valeurs — " if voc else ""
        return f"{champ}:       # {n}dérouler l'arbre de décision de `{taxonomie}`"
    if typ == "date":
        return f"{champ}:       # AAAA-MM-JJ"
    if typ == "url":
        return f'{champ}: ""'
    return f'{champ}: ""'


def gabarit(mo: Modele, prose: ProseSemis, rid: str) -> str:
    decl = mo.roles.get(rid) or {}
    champ_role = prose.commun["champ_role"]
    titre_token = ("<% tp.file.title %>"
                   if str(mo.brain.get("profil") or "") == "obsidian"
                   else "<titre de la page>")

    taxonomie = str(((mo.vocabulaires or {}).get("taxonomie") or {})
                    .get("fichier") or "Documentation/taxonomie.md")

    # L ordre est celui du MANIFESTE — `requis` d abord, puis le reste de
    # `autorises` tel qu il est declare. Trier alphabetiquement melangerait
    # l identite, le resume et les champs d ecosysteme, alors que l ordre du
    # gabarit est ce que l auteur lit de haut en bas quand il remplit.
    lignes = ["---", f"{champ_role}: {rid}"]
    requis = [c for c in mo.requis(rid) if c != champ_role]
    declares = list(mo.gabarit(rid).get("autorises") or [])
    autres = [c for c in declares if c != champ_role and c not in requis]
    for champ in requis + autres:
        lignes.append(_ligne_de_gabarit(mo, champ, titre_token, taxonomie))
    lignes += ["---", ""]

    prefixe = decl.get("prefixe_nom")
    entete = prose.ligne("semis.gabarit.entete", role=rid)
    lignes += [f"<!-- {entete} -->"]
    if prefixe:
        lignes.append(f"<!-- Le nom du fichier commence par « {prefixe} ». -->")
    for c in mo.conditionnels(rid):
        lignes.append(f"<!-- `{c['champ']}:` n'existe que si « {c['si']} ». -->")
    lignes += ["", f"# {titre_token}", ""]

    for s in mo.corps(rid):
        lignes += _section_de_gabarit(mo, prose, s)
    return "\n".join(lignes).rstrip("\n") + "\n"


def _section_de_gabarit(mo: Modele, prose: ProseSemis, s: dict) -> list[str]:
    titre = mo.titre(s)
    genre = str(s.get("genre") or "libre")
    niveau = int(s.get("niveau") or 2)

    if genre == GENRE_AUTO or (genre == "auto"):
        bal = s.get("balises") or []
        if len(bal) == 2:
            return [bal[0], bal[1], ""]
        # Une place `auto` sans balises est un EMBED (la vue d une page de vue) :
        # la forme est declaree par le role, pas ici.
        #
        # Sauf en `profil: nu`, ou aucun moteur n evalue une requete : poser le
        # lien d embed y donnerait un gabarit qui promet une table vivante que
        # rien ne rendra. Le gabarit dit alors ce qu il en est — c est le meme
        # arbitrage que le jeton de Templater quelques lignes plus haut, et le
        # meme que la regle du bandeau : mieux vaut un trou nomme qu une
        # promesse qui ne tient pas.
        if str(mo.brain.get("profil") or "obsidian") != "obsidian":
            return ["<!-- profil `nu` : pas de vue vivante ici. La table, si "
                    "elle est voulue, se tient à la main — et la section "
                    "écrite ci-dessous reste la partie qui a de la valeur. -->",
                    ""]
        embed = ((mo.roles.get(mo.role_de_fonction("vue") or "") or {})
                 .get("vue_embarquee") or {}).get("embed")
        return ([f"<!-- {embed} -->", ""] if embed else [])
    if genre == "bandeau":
        bal = (mo.bandeau or {}).get("balises") or []
        if len(bal) == 2:
            return [bal[0], bal[1], ""]
        return []
    if _est_une_place(titre):
        forme = s.get("forme") or s.get("doctrine") or "à écrire"
        return [f"<!-- {forme} -->", ""]

    out = ["#" * niveau + f" {titre}", ""]
    if genre == "decision":
        pos = s.get("colonne_positive") or "Pour"
        neg = s.get("colonne_negative") or "Contre"
        out += [f"| {pos} | {neg} |", "|---|---|", "|  |  |"]
    elif genre == "etiquetee":
        for e in s.get("obligatoires") or s.get("permises") or []:
            out.append(f"- **{e}** — ")
    elif genre == "liste_liens":
        champ = s.get("champ")
        out.append(f"- <!-- une puce par entrée de `{champ}:` -->" if champ
                   else "- ")
    elif genre == "prose":
        doctrine = s.get("doctrine") or s.get("forme") or ""
        out.append(f"<!-- {doctrine} -->" if doctrine else "")
    elif genre == "conditionnelle":
        out.insert(0, f"<!-- Section CONDITIONNELLE : n'existe que si "
                      f"{s.get('existe_si') or '…'}. Sinon, la SUPPRIMER. -->")
        forme = s.get("forme")
        out.append(f"- <!-- {forme} -->" if forme else "- ")
    else:
        out.append("- ")
    out.append("")
    return out


def seme_les_gabarits(mo: Modele, prose: ProseSemis, plan: Plan) -> None:
    plan.dossier("Templates")
    for rid in sorted(mo.roles):
        plan.pose(f"Templates/{nom_de_gabarit(mo, rid)}.md",
                  gabarit(mo, prose, rid), "gabarits")


# --------------------------------------------------------------------------- #
#  La porte d entree, et les autres pages de la racine
# --------------------------------------------------------------------------- #
def porte_d_entree(mo: Modele, prose: ProseSemis, fichier: str, titre: str) -> str:
    """La page qui cite les hubs de premier niveau — l aiguillage de la racine.

    Elle porte le seul aller vers les hubs qui n ont pas de parent. Sans elle,
    tout hub de premier niveau est « atteignable depuis aucun hub » : c est le
    constat que la remontee 6 du lot 3 avait mesure a QUATRE pages sur le vault
    d epreuve, et c est ce que le bloc `racine:` declare desormais.
    """
    mot = mo.libelle_rangement.get("s") or ""
    # `nom:` porte le NOM DE FICHIER, jamais le titre affiche. La racine n est
    # pas balayee par le validateur aujourd hui, donc rien ne le verifie — et
    # c est precisement pour ca qu il faut l ecrire juste : une page dont
    # l identite ment est une page qu on ne trouve plus le jour ou le perimetre
    # s elargit.
    lignes = ["---", f"nom: {_scalaire(fichier[:-3])}", "---", "",
              f"# {mo.brain.get('nom')} — {titre}",
              "", f"> {mo.brain.get('sujet') or ''}", "",
              prose.ligne("semis.home.vide"), "",
              "## " + prose.ligne("semis.home.arbre", axe_rangement=mot), "",
              prose.ligne("semis.home.arbre_intro",
                          champ_rangement=mo.champ_rangement), ""]
    for dossier, portee in dossiers_de_l_arbre(mo):
        lignes.append(f"- [[{dossier}]]" + (f" — {portee}" if portee else ""))
    lignes.append("")

    ranges = sorted(mo.roles_ranges_par_role())
    if ranges:
        lignes += ["## " + prose.ligne("semis.home.roles"), ""]
        for rid in ranges:
            d = mo.dossier_de_role(rid)
            libelle = ((mo.roles[rid].get("libelle") or {}).get("p") or rid)
            lignes.append(f"- [[{d}]] — les {libelle}")
        lignes.append("")

    ral = [(decl["hub_de_ralliement"]["dossier"], rid)
           for rid, decl in sorted(mo.roles.items())
           if (decl.get("hub_de_ralliement") or {}).get("dossier")]
    if ral:
        lignes += ["## " + prose.ligne("semis.home.ralliement"), ""]
        for d, rid in ral:
            libelle = ((mo.roles[rid].get("libelle") or {}).get("p") or rid)
            lignes.append(f"- [[{d}]] — toutes les {libelle}, où qu'elles vivent")
        lignes.append("")

    if mo.transverses:
        lignes += ["## " + prose.ligne("semis.home.transverses"), "",
                   prose.ligne("semis.home.transverse_intro"), ""]
        for t in mo.transverses:
            mot_t = prose.libelle_transverse(t["champ"])
            valeurs = ", ".join(str(v.get("libelle") or v["cle"])
                                for v in (t.get("valeurs") or []))
            lignes.append(f"- `{t['dossier']}/` — l'axe **{mot_t}** "
                          f"(`{t['champ']}:`) : {valeurs}")
        lignes.append("")

    agent = str(((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    lignes += ["## " + prose.ligne("semis.home.pilotage"), "",
               f"- `{agent}/index/` — le catalogue et la carte des liens, générés",
               f"- `Documentation/` — la gouvernance (taxonomie, vocabulaires)",
               f"- `Templates/` — un gabarit par `{prose.commun['champ_role']}:`",
               "- `CLAUDE.md` — le routeur, et la règle d'identité git en tête",
               ""]
    return "\n".join(lignes)


def page_de_racine(mo: Modele, prose: ProseSemis, decl: dict) -> str:
    """Une page de la racine qui n aiguille pas — l inbox, un backlog, un journal."""
    titre = str(decl.get("titre") or "")
    fichier = str(decl.get("fichier") or "")
    lignes = ["---", f"nom: {_scalaire(fichier[:-3])}", "---", "",
              f"# {titre}", ""]
    role = str(decl.get("role_editorial") or "")
    if role == "capture":
        mot = mo.libelle_rangement.get("s") or ""
        lignes += [prose.ligne("semis.inbox.regle", axe_rangement=mot), "",
                   prose.ligne("semis.inbox.traitement"), ""]
    if decl.get("amorce"):
        lignes += [f"- [ ] {x}" for x in decl["amorce"]] + [""]
    return "\n".join(lignes)


def seme_la_racine(mo: Modele, prose: ProseSemis, plan: Plan) -> None:
    bloc = mo.m.get("racine") or {}
    porte = str(bloc.get("porte_d_entree") or "")
    for decl in bloc.get("pages") or []:
        decl = decl or {}
        fichier = str(decl.get("fichier"))
        titre = str(decl.get("titre") or fichier[:-3])
        texte = (porte_d_entree(mo, prose, fichier, titre) if fichier == porte
                 else page_de_racine(mo, prose, decl))
        plan.pose(fichier, texte, "racine")

    # Les dossiers d ATELIER — arbitrage du lot 6, remontee 4 du lot 5. Ils
    # naissent VIDES, avec un `.gitkeep` (git ne suit aucun dossier vide), et
    # ils n existent que si l entretien les a demandes. Le defaut est ZERO :
    # un dossier vide que personne n a demande reste vide, et la mesure du
    # le vault d'origine le dit — son `Projects/` porte zero page en dix-huit mois.
    for decl in bloc.get("dossiers") or []:
        chemin = str((decl or {}).get("chemin") or "").strip("/")
        if chemin:
            plan.dossier(chemin, garde=True)
