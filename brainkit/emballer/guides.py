"""guides.py — les trois guides d une instance, GENERES depuis `brain.yml`.

    docs/manuel.md      lire le brain      — ce qu on a sous les yeux
    docs/enrichir.md    ecrire dedans      — et ce que ca declenche autour
    docs/exploiter.md   s en servir        — depuis un projet, sans y ecrire

Le decoupage est celui des trois skills, et pour la meme raison : il est
STRUCTUREL, pas thematique. Un lecteur, un auteur, un consommateur — tout brain
a ces trois-la, quel que soit son sujet. Les guides du DevBrain ont servi de
reference de ce qui marche ; ce qu ils portaient de dev est ici remplace par ce
que le manifeste declare.

# La regle de ce module, verifiable

**Aucune valeur d instance n est ecrite ici.** Pas un role, pas un titre de
section, pas un nom de champ, pas une valeur d axe, pas un seuil. Ce que ce
module porte est de la LANGUE et une STRUCTURE. Le controle est celui du lot 7,
etendu a ces trois documents : semer deux brains sans rien de commun, et
verifier que chaque mot de sujet du premier est absent des guides du second.

# Ce qui est derive, et pourquoi ca compte plus que le reste

La table de propagation du guide d enrichissement et la table des effets de bord
du mode mise a jour ne sont pas recopiees d un autre vault : elles sortent des
roles, des axes et des champs reciproques que `brain.yml` declare
(`brainkit.skills.propagation`). C est la MEME derivation que celle du skill de
capture — pas une seconde table qui lui ressemblerait. Deux tables issues de
deux sources auraient fait, dans les deux documents les plus lus du vault,
exactement le defaut que le manifeste existe pour supprimer.
"""

from __future__ import annotations

from ..skills import commun, exploitation, propagation
from ..generer.prose import champ_du_role
from ..valider.manifeste import (GENRE_AUTO, GENRE_BANDEAU, GENRE_DECISION,
                                 GENRE_ETIQUETEE, GENRE_LISTE, GENRE_PROSE,
                                 Modele)

MANUEL, ENRICHIR, EXPLOITER = "manuel.md", "enrichir.md", "exploiter.md"

# Les six fonctions de role sont FERMEES par le kit (contrat §1) : ce sont les
# seuls mots sur lesquels le kit raisonne. La phrase qui les explique est donc
# du kit, pas du manifeste — et c est ce qui permet a un guide de dire ce QU EST
# une page sans qu aucun manifeste n ait a le reecrire. `roles[].libelle` donne
# le mot du sujet ; cette table donne le sens.
FONCTIONS: dict[str, str] = {
    "unite": "ce qu'on vient chercher dans le brain",
    "notion": "ce qu'il faut comprendre",
    "hub": "la page d'aiguillage d'un dossier — elle n'explique rien, elle oriente",
    "vue": "ce qui départage plusieurs pages d'un même thème",
    "prescription": "un objet transverse par construction, qui ne dépend "
                    "d'aucune valeur de l'axe de rangement",
    "transverse": "le hub d'une valeur d'un axe transverse — généré, jamais écrit",
}


def _l(v) -> str:
    return " ".join(str(v or "—").split())


def _entete(mo: Modele, titre: str, quoi: str, voisins: list[str]) -> list[str]:
    from .. import __version__
    L = [f"# {mo.brain.get('nom')} — {titre}", "",
         f"> **Document GÉNÉRÉ** depuis `brain.yml` par BrainKit "
         f"`{__version__}`. Ne pas l'éditer à la main : il se régénère.", "",
         quoi, ""]
    if voisins:
        L += ["Voir aussi : " + " · ".join(voisins), ""]
    return L


def _pluriel(mo: Modele, rid: str) -> str:
    return str(((mo.roles.get(rid) or {}).get("libelle") or {}).get("p") or rid)


def _singulier(mo: Modele, rid: str) -> str:
    return str(((mo.roles.get(rid) or {}).get("libelle") or {}).get("s") or rid)


def _profil(mo: Modele) -> str:
    return str(mo.brain.get("profil") or "obsidian")


def _est_une_place(titre: str) -> bool:
    """Un titre `<...>` est une PLACE, pas une section : le gabarit l efface."""
    return titre.startswith("<") and titre.endswith(">")


def _sections_ecrites(mo: Modele, rid: str) -> list[str]:
    """Les titres des sections qu un humain remplit — les seules a citer.

    Ecartees : les zones generees, le haut de page, et les places `<...>` que
    le gabarit remplace par un jeton. Citer l une des trois enverrait le
    lecteur vers un endroit ou il n a rien a lire ni a ecrire.
    """
    return [mo.titre(s) for s in mo.corps(rid)
            if str(s.get("genre") or "") not in (GENRE_AUTO, GENRE_BANDEAU)
            and not _est_une_place(mo.titre(s))]


# --------------------------------------------------------------------------- #
#  1 — LE MANUEL : lire le brain
# --------------------------------------------------------------------------- #
def manuel(mo: Modele) -> str:
    cr = champ_du_role(mo)
    mot_s = mo.libelle_rangement.get("s") or ""
    mot_p = mo.libelle_rangement.get("p") or ""
    unite = mo.role_unite or ""
    profil = _profil(mo)

    L = _entete(mo, "Manuel d'utilisateur",
                f"Ce document dit **ce qu'on a sous les yeux** en ouvrant le "
                f"vault, et comment y retrouver quelque chose.",
                [f"[{ENRICHIR}]({ENRICHIR}) pour écrire dedans",
                 f"[{EXPLOITER}]({EXPLOITER}) pour s'en servir",
                 "`../INSTALL.md` pour l'installer"])

    # --- 1. le vault en une phrase ----------------------------------------
    L += ["---", "", "## 1. Le vault en une phrase", "",
          f"**Un dossier par {mot_s} à la racine, et une page qui dit ce "
          f"qu'elle est.**", "",
          f"Il n'y a rien d'autre à comprendre. Pas de hiérarchie parallèle, "
          f"pas de dossier d'attente, pas de galaxie. Le dossier porte la "
          f"valeur de `{mo.champ_rangement}:` ; le champ `{cr}:` porte ce que "
          f"la page **est**. Les deux axes ne se recouvrent pas, et c'est ce "
          f"qui permet à deux pages de nature différente de vivre dans le même "
          f"dossier sans que rien ne soit ambigu.", ""]

    # --- 2. les natures de page -------------------------------------------
    L += ["---", "", f"## 2. Les {len(mo.roles)} natures de page", "",
          f"C'est le champ `{cr}:` du frontmatter qui porte la nature d'une "
          f"page. **Il ne se devine pas depuis le chemin** : deux pages de "
          f"nature différente et de même {mot_s} vivent dans le même dossier, "
          f"et un `ls` ne les distingue pas.", "",
          f"| `{cr}:` | Ce que c'est | Rangée par | Protégée |",
          "|---|---|---|---|"]
    for rid, decl in sorted(mo.roles.items()):
        range_par = decl.get("range_par")
        ou = (f"`{mo.champ_rangement}:`" if range_par == "axe"
              else f"son rôle → `{decl.get('dossier')}/`")
        if decl.get("porte_categorie") is False:
            ou = "elle **est** le rangement"
        L.append(f"| `{rid}` | "
                 f"{_l(FONCTIONS.get(str(decl.get('fonction')), _singulier(mo, rid)))} "
                 f"| {ou} | {'**oui**' if decl.get('protege') else 'non'} |")
    L += ["", f"La colonne du milieu n'est pas une paraphrase du mot : c'est la "
          f"**fonction** que le rôle déclare, prise dans une liste fermée de "
          f"six. Le vault se lit dans les mots de son sujet ; le kit, lui, ne "
          f"raisonne que sur ces six-là. Un seul endroit fait le pont, et c'est "
          f"`brain.yml`.", ""]
    proteges = [rid for rid in sorted(mo.roles) if mo.roles[rid].get("protege")]
    if proteges:
        L += ["Une page **protégée** est la mémoire personnelle du "
              "propriétaire du brain. On y ajoute volontiers ; on n'y réécrit "
              "pas sans qu'il l'ait demandé. La frontière se lit dans le "
              f"frontmatter, page par page — jamais sur un chemin.", ""]
    if profil == "obsidian" and (mo.m.get("graphe") or {}).get("ordre"):
        L += [f"Les couleurs du graphe sont ce même axe, en visuel : une "
              f"couleur par `{cr}:`. La table est dans "
              f"`../Documentation/graphe.md`.", ""]

    # --- 3. ou vit une page ------------------------------------------------
    L += ["---", "", "## 3. Où vit une page", "",
          f"**Personne ne choisit un dossier.** Le chemin se dérive du champ "
          f"`{mo.champ_rangement}:`"
          + (f" — {len(mo.dossier_de_prefixe)} valeurs de premier niveau"
             if mo.dossier_de_prefixe else "") + ", et le validateur le "
          "vérifie page par page : une page hors de son dossier dérivé est une "
          "violation, pas un rangement personnel.", "",
          f"Un sous-dossier apparaît quand une sous-valeur atteint **{mo.seuil}** "
          f"page(s)"
          + (", sauf s'il ne laisserait aucune page au niveau du parent — un "
             "dossier fils qui redouble son parent n'apporte rien."
             if mo.plafond else ".") + " Changer ce seuil est une **migration** "
          "outillée, pas un réglage : elle déplace des pages, par `git mv`.", ""]
    if not mo.exclusif:
        L += [f"L'axe n'est **pas exclusif** : une page peut porter plusieurs "
              f"valeurs de `{mo.champ_rangement}:`. Son dossier est alors celui "
              f"de la valeur dominante"
              + (f" — {_l(mo.rangement.get('definition_de_la_majorite'))}"
                 if mo.rangement.get("definition_de_la_majorite") else "")
              + (f", et le préfixe `{mo.prefixe_transversal}` est réservé aux "
                 f"pages qu'aucune valeur ne rassemble."
                 if mo.prefixe_transversal else "."), ""]
    L += [f"| {mot_s.capitalize()} | Dossier | Portée |", "|---|---|---|"]
    for p in mo.rangement.get("prefixes") or []:
        L.append(f"| `{p['cle']}` | `{p.get('dossier','')}/` | "
                 f"{_l(p.get('portee'))} |")
    L.append("")
    ratt = mo.rangement.get("rattachements") or {}
    if ratt:
        L += ["Et les **rattachements** — des exceptions nommées, avec leur "
              "motif :", "", "| Valeur | Dossier | Motif |", "|---|---|---|"]
        for cle, d in sorted(ratt.items()):
            L.append(f"| `{cle}` | `{(d or {}).get('dossier','')}/` | "
                     f"{_l((d or {}).get('motif'))} |")
        L.append("")
    for t in mo.transverses:
        L += [f"**L'axe transverse `{t['champ']}:`** traverse l'arbre : un hub "
              f"par valeur **portée**, dans `{t['dossier']}/`. Un hub y naît "
              f"quand une page porte la valeur, pas avant — une page vide dans "
              f"un graphe est un nœud de plus qui ne rassemble rien.", ""]

    # --- 4. lire une page d unite ------------------------------------------
    if unite:
        L += ["---", "", f"## 4. Lire une page `{cr}: {unite}`", "",
              f"Une {_singulier(mo, unite)} suit toujours le même gabarit. De "
              f"haut en bas :", "",
              "| Section | Ce qu'elle contient | Ce qu'elle ne contient pas |",
              "|---|---|---|"]
        for s in mo.corps(unite):
            genre = str(s.get("genre") or "libre")
            if genre == "conditionnelle":       # listées à part, juste après
                continue
            titre = mo.titre(s)
            quoi = _l(s.get("forme") or s.get("doctrine"))
            pas = "—"
            if genre == GENRE_BANDEAU:
                quoi = ("les colonnes du haut de page, composées depuis le "
                        "frontmatter")
                pas = "**rien d'écrit à la main** — la zone est générée"
            elif genre == GENRE_PROSE:
                quoi = quoi if quoi != "—" else "de la prose"
                pas = "ce que le haut de page dit déjà"
            elif genre == GENRE_DECISION:
                pos = s.get("colonne_positive") or "positive"
                neg = s.get("colonne_negative") or "négative"
                quoi = f"un tableau à deux colonnes : *{pos}* et *{neg}*"
                pas = "de la prose"
            elif genre == GENRE_ETIQUETEE:
                etiq = (s.get("obligatoires") or []) or (s.get("permises") or [])
                ferme = "obligatoires" if s.get("obligatoires") else "permises"
                quoi = (f"{len(etiq)} étiquette(s) {ferme} : "
                        + ", ".join(f"`{e}`" for e in etiq)) if etiq else quoi
                pas = "de la prose, et aucune étiquette hors de la liste"
            elif genre == GENRE_LISTE:
                quoi = (f"une puce par cible, adossée à `{s['champ']}:`"
                        if s.get("champ") else "une puce par lien interne")
                pas = "un lien cité au milieu d'une phrase — ça ne LISTE pas"
            elif genre == GENRE_AUTO:
                quoi = quoi if quoi != "—" else "une zone générée"
                pas = "**rien d'écrit à la main**"
            elif genre == "libre":
                quoi = quoi if quoi != "—" else "des puces, une idée par puce"
            L.append(f"| `{titre}` | {quoi} | {pas} |")
        L += ["", "**Une ligne, une étiquette, une idée.** La prose ne vit que "
              "dans la section qui la déclare ; partout ailleurs, des puces.",
              ""]
        cond = [s for s in mo.corps(unite) if s.get("genre") == "conditionnelle"]
        if cond:
            L += ["Et les sections **conditionnelles** — elles n'existent que "
                  "si elles se remplissent. Une section conditionnelle vide se "
                  "**supprime** :", ""]
            for s in cond:
                L.append(f"- `{mo.titre(s)}` — n'existe que si "
                         f"{_l(s.get('existe_si'))}.")
            L.append("")
        if mo.bandeau.get("colonnes"):
            L += [f"### Le haut de page", "",
                  "| Colonne | Composée depuis |", "|---|---|"]
            for c in mo.bandeau["colonnes"]:
                src = c.get("source") or "—"
                L.append(f"| {c.get('titre', src)} | `{src}`"
                         + (f", qualifié par `{c['qualifie_par']}`"
                            if c.get("qualifie_par") else "") + " |")
            L += ["", "**Une cellule vide est un fait, pas un oubli.** Une "
                  "cellule sans source dans le frontmatter affiche un tiret "
                  "cadratin, jamais une valeur plausible — une fiche vide "
                  "honnêtement vaut mieux qu'une fiche remplie au jugé.", ""]

    # --- 5. lire une page de vue -------------------------------------------
    rid_vue = mo.role_de_fonction("vue")
    if rid_vue:
        vue = mo.roles[rid_vue].get("vue_embarquee") or {}
        L += ["---", "", f"## 5. Lire une page `{cr}: {rid_vue}`", ""]
        if profil == "obsidian":
            L += [f"Deux fichiers portent le même nom : la **page** `.md` et la "
                  f"**vue** `{vue.get('extension','')}`.", "",
                  f"- La vue est une **requête**, rendue par `{vue.get('moteur','')}`. "
                  f"Elle liste les pages qui remplissent son filtre et affiche "
                  f"leur frontmatter en tableau. Elle se remplit toute seule : "
                  f"une page ajoutée y entre sans que personne n'y touche.",
                  f"- La page **embarque** ce tableau, et ajoute ce que le "
                  f"tableau ne peut pas dire.", ""]
        else:
            L += [f"Ce brain est en profil **`nu`** : il n'y a pas de moteur "
                  f"pour évaluer une requête. Une page `{rid_vue}` est donc une "
                  f"page ordinaire — sa valeur est entièrement dans la section "
                  f"écrite à la main, et la table, si on la veut, se tient à la "
                  f"main.", ""]
        ecrites = _sections_ecrites(mo, rid_vue)
        if ecrites:
            L += ["**C'est là qu'est la valeur** : "
                  + ", ".join(f"`{t}`" for t in ecrites)
                  + ". Un tableau dit que deux pages portent la même valeur — "
                  "c'est vrai et ça n'apprend rien. La section écrite dit ce "
                  "qui les distingue.", ""]
        ralliement = (mo.roles[rid_vue].get("hub_de_ralliement") or {})
        if ralliement.get("dossier"):
            L += [f"Toutes les pages `{rid_vue}` sont réunies par le hub de "
                  f"`{ralliement['dossier']}/`, où qu'elles vivent dans "
                  f"l'arbre. **C'est le lien retour qui fait la grappe** : un "
                  f"hub qui cite N pages sans qu'aucune le cite ajoute un nœud "
                  f"et ne rassemble rien.", ""]

    # --- 6. trouver quelque chose ------------------------------------------
    L += ["---", "", "## 6. Trouver quelque chose", "",
          "Par ordre d'efficacité :", ""]
    n = 1
    if profil == "obsidian":
        L.append(f"{n}. **Tu sais quoi chercher** → ouvrir par le nom "
                 f"(`Ctrl+O`). Les liens du vault sont **nus** : le nom de "
                 f"fichier suffit, quel que soit le dossier.")
        n += 1
    else:
        L.append(f"{n}. **Tu sais quoi chercher** → chercher le nom du "
                 f"fichier. Les liens du vault sont **nus** : le nom suffit, "
                 f"quel que soit le dossier.")
        n += 1
    if rid_vue:
        L.append(f"{n}. **Tu hésites entre deux pages** → la page `{rid_vue}` "
                 f"du dossier, et directement sa section écrite à la main.")
        n += 1
    L.append(f"{n}. **Tu explores** → le hub du dossier. Sa zone générée liste "
             f"tout ce que le dossier contient ; son corps, écrit à la main, "
             f"dit ce qui départage les sous-dossiers.")
    n += 1
    for t in mo.transverses:
        L.append(f"{n}. **Tu pars d'un axe transverse** → `{t['dossier']}/`, un "
                 f"hub par valeur de `{t['champ']}:`.")
        n += 1
    L.append(f"{n}. **Tu veux le catalogue entier** → "
             f"`../{str(((mo.m.get('agent') or {}).get('racine') or 'AI/')).strip('/')}"
             f"/index/` : le catalogue machine, le document humain et la carte "
             f"des liens, tous trois **générés**.")
    n += 1
    if profil == "obsidian" and (mo.m.get("graphe") or {}).get("ordre"):
        L.append(f"{n}. **Tu veux voir les liens** → le graphe, coloré par "
                 f"`{cr}:`.")
    L.append("")

    # --- 7. ce qui est genere ----------------------------------------------
    L += ["---", "", "## 7. Ce qui est généré, et qu'on ne touche pas", "",
          "| Quoi | Généré par |", "|---|---|"]
    for c in ((mo.m.get("genere") or {}).get("chemins") or []):
        L.append(f"| `{c.get('chemin')}` | {_l(c.get('par'))}"
                 + (f", depuis `{c['depuis']}`" if c.get("depuis") else "") + " |")
    L += ["", "Éditer l'un de ces blocs à la main, c'est écrire quelque chose "
          "que la prochaine régénération effacera. Le **corps** d'un hub, lui, "
          "s'écrit à la main — c'est la zone générée qui est intouchable, pas "
          "la page.", "",
          "Le contrôle est une commande, et elle sort en 2 s'il reste un "
          "écart :", "", "```bash", "brainkit generer            # --check", "```", ""]
    return "\n".join(L).rstrip("\n") + "\n"


# --------------------------------------------------------------------------- #
#  2 — ENRICHIR : écrire dans le brain
# --------------------------------------------------------------------------- #
def enrichir(mo: Modele) -> str:
    cr = champ_du_role(mo)
    mot_s = mo.libelle_rangement.get("s") or ""
    unite = mo.role_unite or ""
    capture = commun.nom_du_skill(mo, "capture")
    cloture = commun.nom_du_skill(mo, "cloture")
    lignes = propagation.derive(mo)
    prop = mo.m.get("propagation") or {}
    taxonomie = str(((mo.vocabulaires or {}).get("taxonomie") or {})
                    .get("fichier") or "Documentation/taxonomie.md")

    L = _entete(mo, "Enrichir le brain",
                f"Comment ajouter une page, et **ce que ça déclenche autour**.",
                [f"[{MANUEL}]({MANUEL}) pour lire le vault",
                 f"[{EXPLOITER}]({EXPLOITER}) pour s'en servir"])

    L += ["---", "", "## 1. Tu ne crées pas une page, tu déclenches une "
          "propagation", ""]
    if prop.get("enonce"):
        L += [f"**{_l(prop['enonce'])}**", ""]
    L += [f"C'est le point à avoir en tête avant tout le reste : **une page ne "
          f"s'ajoute jamais seule.** Une page nouvelle change au moins "
          f"{len(lignes)} autres choses, et si on ne les change pas le vault "
          f"ment.", ""]
    if prop.get("clause"):
        L += [f"> {_l(prop['clause'])}", ""]
    if capture:
        L += [f"Le skill **`{capture}`** porte cette règle. On l'appelle en "
              f"langage naturel, depuis un agent lancé **dans le dossier du "
              f"vault**.", ""]
        decl = (mo.m.get("skills") or {}).get("capture") or {}
        if decl.get("mode_lot"):
            L += ["Il a un **mode lot** : capturer plusieurs pages d'un même "
                  "dossier en une conversation, en n'appliquant la propagation "
                  "qu'une fois à la fin. Sans lui, l'amorçage d'un brain neuf "
                  "coûte une conversation par page, et personne ne le fait.",
                  ""]

    # --- 2. le rayon, DERIVE -----------------------------------------------
    L += ["---", "", "## 2. Le rayon — ce que le skill fait, et que tu n'as "
          "pas à faire", "",
          "| # | Cible | Trouvée par | Par | Sans objet si |",
          "|---|---|---|---|---|"]
    for li in lignes:
        L.append(f"| {li.n} | {_l(li.cible)} | {_l(li.trouve_par)} | "
                 f"{_l(li.par)} | {_l(li.sans_objet_si) if li.sans_objet_si else '—'} |")
    L += ["", f"Cette table est **dérivée** de `roles`, `axes` et `champs` du "
          f"manifeste — pas écrite à la main, et pas recopiée d'un autre brain. "
          f"Un manifeste différent donne une table différente ; une table "
          f"identique sur deux brains différents serait la preuve qu'elle est "
          f"recopiée.", "",
          "**Une ligne sans objet se déclare sans objet, elle ne se tait pas.** "
          "Un silence se lit comme un oubli ; une ligne qui dit « sans objet "
          "ici, parce que ceci » se lit comme une décision.", ""]

    # --- 3. les valeurs qu on ne devine pas --------------------------------
    L += ["---", "", "## 3. Les valeurs que tu ne devines jamais", "",
          f"- **`{mo.champ_rangement}:`** — l'axe qui **range** ({mot_s}) : "
          f"*où ça se range*. C'est lui, et lui seul, qui décide du chemin."]
    if mo.champ_nature:
        mot_n = (mo.libelles.get("axe_nature") or {}).get("s") or mo.champ_nature
        L.append(f"- **`{mo.champ_nature}:`** — l'axe qui **qualifie** "
                 f"({mot_n}) : *ce que c'est*"
                 + (f", {len(mo.valeurs_nature)} valeurs fermées."
                    if mo.valeurs_nature else "."))
    L += ["", f"`{taxonomie}` porte un **arbre de décision déterministe** : "
          f"questions **fermées**, en **ordre strict**, la première réponse "
          f"positive gagne. On le déroule, on ne tranche pas au jugé — et "
          f"l'ordre des questions **est** la décision de conception, prise une "
          f"fois, valable pour toutes les pages.", "",
          "**Si aucune question ne tranche : laisser le champ vide et "
          "demander.** Un champ vide est une question ouverte ; une valeur "
          "inventée est une faute, et elle range la page au mauvais endroit "
          "pour toujours.", ""]
    if mo.champ_nature and not mo.nature_vide_autorise:
        L += [f"> Sur ce brain, `{mo.champ_nature}:` **n'accepte pas** le vide : "
              f"il faut trancher, ou demander.", ""]
    L += [f"Un troisième champ, **`{cr}:`**, dit ce que la page *est* — voir le "
          f"manuel. Les deux axes ne se recouvrent pas.", ""]

    # --- 4. les frontieres --------------------------------------------------
    L += ["---", "", "## 4. Les frontières d'écriture", ""]
    L += commun.bloc_frontieres(mo)[1:]

    # --- 5. mettre a jour ---------------------------------------------------
    # Les champs SANS consommateur declare sont ecartes du guide, et gardes par
    # le skill. Le skill est une liste de controle exhaustive : y voir « ce
    # champ ne se lit nulle part » est une information. Un guide, lui, se lit
    # en entier — vingt lignes qui disent « rien a faire » y noient les dix qui
    # disent quoi faire.
    effets = [e for e in propagation.effets_de_bord(mo)
              if e.consommateurs
              and not all("aucun consommateur déclaré" in c
                          for c in e.consommateurs)]
    L += ["---", "", "## 5. Mettre à jour une page qui existe", "",
          "Jamais un patch improvisé. **Une page qu'on crée n'a pas de "
          "consommateurs ; une page qui existe en a.** C'est toute la "
          "différence entre créer et mettre à jour, et c'est pour ça que le "
          "skill a deux modes.", "",
          "| Champ modifié | Qui le lit | Comment on vérifie |",
          "|---|---|---|"]
    for e in effets:
        L.append(f"| `{e.champ}` | " + " · ".join(_l(c) for c in e.consommateurs)
                 + f" | {_l(e.verification)} |")
    L += ["", "Cette table est **dérivée** elle aussi : du bandeau, des vues, "
          "des champs réciproques, des conditionnels et des champs indexés. "
          "Elle est la même que celle du skill de capture — pas une seconde "
          "table qui lui ressemblerait.", "",
          "Les champs qu'elle **ne** montre **pas** sont ceux dont aucun "
          "consommateur n'est déclaré : ni indexés, ni au haut de page, ni "
          "réciproques, ni adossés à un vocabulaire. Le skill les garde, parce "
          "qu'une liste de contrôle exhaustive a besoin de dire « rien à faire "
          "ici » ; un guide se lit en entier, et ces lignes-là y noieraient les "
          "autres.", ""]

    # --- 6. cloturer --------------------------------------------------------
    L += ["---", "", "## 6. Clôturer — la seule étape qu'on ne saute pas", ""]
    if cloture:
        L += [f"**Toute** écriture dans une page du brain se clôt par le skill "
              f"**`{cloture}`**.", ""]
    etapes = ((mo.m.get("skills") or {}).get("cloture") or {}).get("etapes") or []
    if etapes:
        for e in etapes:
            L.append(f"1. {_l(e)}")
        L.append("")
    L += ["```bash", "brainkit generer --ecrire", "brainkit valider", "```", "",
          "C'est le **seul** endroit où la politique git du vault est écrite — "
          "à une exception, et elle est délibérée : la **règle d'identité git** "
          "vit aussi dans `CLAUDE.md`, parce que c'est le seul fichier chargé "
          "dans chaque conversation, au même moment que l'annonce de l'outil. "
          "Une contre-instruction qui arrive après coup arrive trop tard.", "",
          "Trois hooks versionnés doublent la consigne, parce que la consigne "
          "seule n'a jamais suffi. **Un hook qui refuse n'est pas un incident à "
          "contourner : c'est la règle qui fonctionne.**", ""]

    # --- 7. ce qu on n ecrit pas -------------------------------------------
    L += ["---", "", "## 7. Ce qu'on n'écrit pas", "",
          "- **Rien qui ne soit sourcé.** Une cellule sans source reste vide et "
          "se signale. Des pages remplies de plausible sont pires que des pages "
          "vides : on ne sait plus lesquelles croire.",
          f"- **Aucune valeur d'axe hors du vocabulaire.** Une famille nouvelle "
          f"se pose dans `{taxonomie}` — donc dans `brain.yml`, qui le génère — "
          f"pas dans l'arborescence.",
          "- **Aucune sévérité durcie sans mesure.** `brainkit mesurer` compte "
          "ce qu'une règle coûterait **avant** qu'on la durcisse. Porter une "
          "sévérité qu'on n'a pas mesurée, c'est porter la mesure d'un autre "
          "corpus.",
          "- **Aucun `rm` improvisé.** Un déplacement se fait par `git mv`, "
          "sans quoi l'historique de la page est perdu — et l'historique est ce "
          "qui distingue un vault d'un dossier de fichiers.", ""]
    return "\n".join(L).rstrip("\n") + "\n"


# --------------------------------------------------------------------------- #
#  3 — EXPLOITER : s'en servir sans y écrire
# --------------------------------------------------------------------------- #
def exploiter(mo: Modele) -> str:
    cr = champ_du_role(mo)
    unite = mo.role_unite or ""
    agent = str(((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    expl = commun.nom_du_skill(mo, "exploitation")
    capture = commun.nom_du_skill(mo, "capture")
    decl = (mo.m.get("skills") or {}).get("exploitation") or {}

    L = _entete(mo, "S'en servir",
                f"Le brain n'est pas fait pour être lu de bout en bout : il est "
                f"fait pour **contraindre le travail en aval**. Ce document dit "
                f"comment le consommer sans y écrire.",
                [f"[{MANUEL}]({MANUEL}) pour lire le vault",
                 f"[{ENRICHIR}]({ENRICHIR}) pour écrire dedans"])

    L += ["---", "", "## 1. La règle qui commande tout : on ne travaille pas "
          "dans le vault", "",
          "Le travail se fait dans **son propre dossier**, avec l'agent lancé "
          "là-bas — jamais dans le vault. Le vault est une **source**, pas un "
          "plan de travail.", "",
          "Depuis un consommateur, le brain se **lit** et ne s'**écrit** pas. "
          "Ce n'est pas une politesse : une écriture faite hors du mode "
          "d'enrichissement saute la propagation, et une page insérée sans son "
          "rayon laisse le vault incohérent sans que personne ne le sache "
          "avant la prochaine validation.", ""]

    L += ["---", "", "## 2. Ce que le brain apporte au démarrage", "",
          "Sans lui, un agent à qui on demande un plan propose ce qu'il a vu le "
          "plus souvent. Avec lui, il propose **ce que tu as déjà évalué**, "
          "avec le fait qui t'avait fait choisir — et il pointe la page qui le "
          "justifie.", ""]
    if expl:
        L += [f"C'est le rôle du skill **`{expl}`**, appelé depuis le dossier "
              f"du travail :", ""]
        if decl.get("livrable"):
            L += [f"Il produit **{_l(decl['livrable'])}**. C'est ce livrable "
                  f"qui contraint l'aval, et c'est là qu'est le gain — pas "
                  f"dans la lecture du vault.", ""]
        if decl.get("etapes"):
            for e in decl["etapes"]:
                L.append(f"1. {_l(e)}")
            L.append("")
    else:
        L += ["**Ce brain n'a pas de skill d'exploitation, et c'est une "
              "réponse, pas un oubli.**", "", exploitation.absence(mo), ""]

    # --- 3. interroger l index ---------------------------------------------
    idx = (mo.m.get("genere") or {}).get("index") or {}
    L += ["---", "", "## 3. Interroger l'index", "",
          f"Le catalogue machine est dans `{agent}/index/`. Il est **généré** : "
          f"il ne s'édite pas, il se régénère.", ""]
    if idx.get("champs"):
        L += ["Champs indexés, donc filtrables :", "",
              " · ".join(f"`{c}`" for c in idx["champs"]), ""]
    L += ["Deux réserves qui valent d'être connues avant de filtrer :", "",
          "- un champ d'énumération **ouverte** ne se filtre pas par égalité "
          "exacte sans rater des pages qui portent une valeur composée ;",
          "- un champ vide n'est pas une valeur : c'est une question ouverte, "
          "et une page au champ vide ne doit pas être éliminée comme si elle "
          "avait répondu.", ""]
    elim = exploitation.eliminatoires(mo)
    if elim:
        L += ["Les champs qui **éliminent** légitimement, et leurs valeurs :", ""]
        for champ, valeurs in elim:
            L.append(f"- `{champ}` — " + ", ".join(f"`{v}`" for v in valeurs))
        L += ["", "> Une valeur d'élimination n'est pas un jugement de "
              "qualité : elle dit ce que la page **est**, pas ce qu'elle "
              "vaut.", ""]

    # --- 4. le chemin de lecture -------------------------------------------
    L += ["---", "", "## 4. Le chemin de lecture, quand tu cherches toi-même",
          "", "| Tu veux | Va voir |", "|---|---|"]
    rid_vue = mo.role_de_fonction("vue")
    if rid_vue:
        ecrite = next(iter(_sections_ecrites(mo, rid_vue)), None)
        L.append(f"| choisir entre deux pages | la page `{cr}: {rid_vue}` du "
                 f"dossier" + (f", section `{ecrite}`" if ecrite else "") + " |")
    if unite:
        for s in mo.corps(unite):
            genre = str(s.get("genre") or "")
            if genre == GENRE_ETIQUETEE:
                L.append(f"| les conditions pratiques, étiquette par étiquette "
                         f"| la page, `{mo.titre(s)}` |")
            elif genre == GENRE_DECISION:
                neg = s.get("colonne_negative")
                L.append(f"| savoir pourquoi écarter | la page, "
                         f"`{mo.titre(s)}`"
                         + (f", colonne *{neg}*" if neg else "") + " |")
    rid_notion = mo.role_de_fonction("notion")
    if rid_notion:
        L.append(f"| comprendre le fond | la page `{cr}: {rid_notion}` du même "
                 f"dossier |")
    for rid in sorted(mo.roles_de_fonction("prescription")):
        L.append(f"| ce que les {_pluriel(mo, rid)} du brain prescrivent | "
                 f"`{mo.dossier_de_role(rid)}/` |")
    for axe in mo.transverses:
        L.append(f"| partir de `{axe['champ']}:` | `{axe['dossier']}/` |")
    L.append("")

    # --- 5. ce qui remonte --------------------------------------------------
    L += ["---", "", "## 5. Ce qui remonte vers le brain", "",
          "Un travail produit deux choses qui méritent de revenir :", ""]
    dates: list[str] = []
    if unite:
        for s in mo.corps(unite):
            if str(s.get("genre") or "") == "conditionnelle":
                dates.append(f"`{mo.titre(s)}` — n'existe que si "
                             f"{_l(s.get('existe_si'))}"
                             + (f", au format `{s['format']}`"
                                if s.get("format") else ""))
    if dates:
        L += ["- **Un retour daté.** Il s'écrit dans la section conditionnelle "
              "de la page concernée :", ""]
        for d in dates:
            L.append(f"  - {d}")
        L += ["", "  La **date** est ce qui distingue le vécu du piège "
              "documenté. Sans date, ce n'est pas un retour : c'est une borne, "
              "et une borne va dans la section qui porte les bornes.", ""]
    if capture:
        L += [f"- **Une page découverte.** Elle se capture avec `{capture}`, "
              f"**depuis le vault**, pas depuis le dossier de travail — c'est "
              f"la propagation qui l'exige, pas une convention.", ""]
    L += ["> Un incident né entre deux pages s'inscrit **sous celle qui a porté "
          "le correctif**, une seule fois, les autres nommées en clair dans la "
          "ligne. Une entrée dupliquée serait une seconde chose à "
          "synchroniser.", ""]
    return "\n".join(L).rstrip("\n") + "\n"


def rendus(mo: Modele) -> dict[str, str]:
    """{nom de fichier : contenu} — les trois guides de CE manifeste."""
    return {MANUEL: manuel(mo), ENRICHIR: enrichir(mo), EXPLOITER: exploiter(mo)}
