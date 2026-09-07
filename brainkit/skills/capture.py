"""capture.py — le skill qui ECRIT dans le brain, instancie depuis le manifeste.

C est le seul des trois qui ecrit, et le seul dont le contenu soit presque
entierement DERIVE : la table de propagation sort de `propagation.derive()`, la
table des effets de bord de `propagation.effets_de_bord()`, les gabarits de
`roles[]`, les vocabulaires de `axes`. Ce module met en page ; il ne decide
rien.

# Les trois modes, et pourquoi le troisieme n est pas un luxe

| mode | declencheur | ce qui le distingue |
|---|---|---|
| **cible** | « ajoute X » | une page, un rayon, une cloture |
| **lot** | « ajoute ces quinze titres » | N pages d UN dossier, le rayon applique UNE fois a la fin |
| **mise a jour** | « le resume de X a change », un renommage | la page EXISTE, donc elle a des CONSOMMATEURS |

Le mode LOT est la reponse au risque §5.9 du cadrage : a la fin de l entretien,
le vault contient des hubs et zero page ; personne ne remplit trois cents pages
une conversation a la fois. Sans ce mode, l amorcage ne se fait pas — et un
brain qui ne s amorce pas ne rend aucun service.

Le mode MISE A JOUR est celui qui manque toujours et qui coute le plus cher :
une page qu on cree n a aucun consommateur, une page qui existe en a. C est la
difference entre les deux procedures, et c est toute la raison de la table des
effets de bord.
"""

from __future__ import annotations

from ..generer.prose import champ_du_role
from ..valider.manifeste import Modele
from . import commun, propagation


def skill(mo: Modele) -> str:
    nom = commun.nom_du_skill(mo, "capture") or "enrichir-le-brain"
    decl = ((mo.m.get("skills") or {}).get("capture") or {})
    brain = mo.brain.get("nom") or "ce brain"
    cr = champ_du_role(mo)
    rid = mo.role_unite
    unite = commun.mot(mo, "unite", "s")
    unites = commun.mot(mo, "unite", "p")
    axe_s = mo.libelle_rangement.get("s") or "domaine"
    axe_p = mo.libelle_rangement.get("p") or "domaines"
    dossier = commun.dossier_exemple(mo)
    lignes = propagation.derive(mo, rid)
    mode_lot = bool(decl.get("mode_lot"))
    cloture = commun.nom_du_skill(mo, "cloture")

    L: list[str] = commun.entete(nom, _description(mo, nom, brain, unite,
                                                   unites, axe_s, mode_lot))
    L += [f"# Skill — {nom}", "",
          f"Skill de **capture** de {brain}. Il écrit dans le brain — c'est le "
          f"seul des trois. Ce qu'il porte, et que rien d'autre ne porte : la "
          f"**règle de propagation**, qui dit qu'une écriture n'est jamais la "
          f"création d'une page seule.", "",
          f"> **{brain}** — {commun.ligne(mo.brain.get('sujet'))}", "",
          f"Généré depuis `brain.yml` par BrainKit. La table de propagation "
          f"ci-dessous n'est pas recopiée d'un autre brain : elle est "
          f"**dérivée** des rôles, des axes et des champs réciproques que ce "
          f"manifeste déclare. Un autre manifeste donnerait une autre table.",
          ""]

    L += _quand_l_utiliser(mo, nom, cloture, mode_lot)
    L += commun.prologue_des_commandes(mo)
    L += _la_regle(mo, lignes, axe_s, dossier)
    L += _trouver_le_dossier(mo, axe_s, axe_p, dossier)
    L += _lister_le_rayon(mo, lignes, dossier)
    L += _conventions(mo)
    L += _mode_cible(mo, lignes, rid, unite, dossier, cloture)
    if mode_lot:
        L += _mode_lot(mo, lignes, unites, axe_s, cloture, decl)
    L += _mode_mise_a_jour(mo, cloture)
    L += _anti_patterns(mo, lignes, cr)
    L += _voir_aussi(mo, cloture)
    return "\n".join(L)


# --------------------------------------------------------------------------- #
def _description(mo: Modele, nom: str, brain: str, unite: str, unites: str,
                 axe_s: str, mode_lot: bool) -> str:
    lot = (f" Mode LOT : capturer dix à vingt {unites} d'un même dossier en une "
           f"conversation, le rayon appliqué UNE fois à la fin — c'est ce mode "
           f"qui rend l'amorçage d'un brain neuf possible."
           if mode_lot else "")
    return (
        f"Capture une {unite} ou une notion dans {brain}. Déclencheurs : "
        f"« ajoute <X> au brain », « documente <X> », « fiche-moi <X> », ou en "
        f"fin de conversation « enrichis le brain » (mode balayage). Porte la "
        f"RÈGLE DE PROPAGATION : le rayon d'une insertion est le dossier "
        f"d'accueil plus ses hubs parents, et le voisinage d'une page est `ls` "
        f"de son dossier — jamais une intuition. Crée la page demandée ET met à "
        f"jour tout son rayon, dans les deux sens.{lot} Porte aussi le mode "
        f"MISE À JOUR — « le résumé de X a changé », un reclassement, un "
        f"renommage — avec sa table des effets de bord : une page qui existe a "
        f"des consommateurs. NE CLÔT PAS : régénérer, valider et committer "
        f"appartiennent au skill de clôture.")


def _quand_l_utiliser(mo: Modele, nom: str, cloture: str | None,
                      mode_lot: bool) -> list[str]:
    unite = commun.mot(mo, "unite", "s")
    unites = commun.mot(mo, "unite", "p")
    expl = commun.nom_du_skill(mo, "exploitation")
    L = ["## Quand l'utiliser", "",
         f"- **Mode ciblé** — ajouter une {unite} ou une page précise. "
         f"« ajoute <X> », « documente <X> ».",
         f"- **Mode balayage** — en fin de conversation : repérer tout ce qui "
         f"mérite une page, présenter le plan, attendre le GO, puis dérouler."]
    if mode_lot:
        L.append(f"- **Mode lot** — amorcer : dix à vingt {unites} d'un même "
                 f"dossier, en une conversation. C'est le mode qui rend un "
                 f"brain neuf utilisable.")
    L += [f"- **Mode mise à jour** — une page existe déjà et un champ change. "
          f"C'est le cas le plus dangereux : elle a des **consommateurs**.", "",
          "Distinct de :"]
    if cloture:
        L.append(f"- `{cloture}` — la **clôture** : régénérer, valider, "
                 f"committer. Ce skill-ci ne commite pas, et n'a pas le droit "
                 f"de clore à sa place.")
    if expl:
        L.append(f"- `{expl}` — l'**exploitation** : il consomme le brain et "
                 f"n'y écrit rien.")
    L.append("")
    return L


# --------------------------------------------------------------------------- #
def _la_regle(mo: Modele, lignes: list[propagation.Ligne], axe_s: str,
              dossier: str) -> list[str]:
    prop = mo.m.get("propagation") or {}
    enonce = commun.ligne(prop.get("enonce")) if prop.get("enonce") else (
        "Le rayon de propagation d'une insertion est le DOSSIER D'ACCUEIL, plus "
        "ses HUBS PARENTS. Le voisinage d'une page est `ls` de son dossier.")
    clause = commun.ligne(prop.get("clause")) if prop.get("clause") else (
        "Une ligne sans objet se DÉCLARE sans objet, elle ne se tait pas.")

    L = ["---", "", "## La règle de propagation — le cœur de ce skill", "",
         f"> **{enonce}**", "",
         f"Le voisinage d'une page cesse d'être une intuition : c'est `ls` de "
         f"son dossier. Ça ne tient qu'à un fait de structure — **le dossier "
         f"porte la valeur de `{mo.champ_rangement}:`** — et c'est pour cela "
         f"que la règle ne dépend d'aucun sujet.", "",
         f"> **{clause}**", "",
         "C'est cette clause, et elle seule, qui distingue « j'ai propagé » de "
         "« j'ai écrit une page ». Une ligne dont on ne dit rien est un oubli, "
         "pas un choix.", "",
         f"### La table — {len(lignes)} lignes, dérivées de ce manifeste", "",
         "| # | À mettre à jour | Comment on la trouve | Qui le fait |",
         "|---|---|---|---|"]
    for li in lignes:
        L.append(f"| **{li.n}** | {li.cible} | {li.trouve_par} | {li.par} |")
    L += ["", f"### D'où sort chaque ligne, et quand elle est **sans objet**", "",
          "La première colonne est ce qui, **dans `brain.yml`**, fait exister la "
          "ligne. La seconde est la seule façon légitime de ne rien écrire pour "
          "elle — et elle se **déclare**.", "",
          "| # | Ce qui la produit dans le manifeste | Sans objet quand… |",
          "|---|---|---|"]
    for li in lignes:
        L.append(f"| **{li.n}** | {li.origine} | "
                 f"{li.sans_objet_si or '**jamais** — cette ligne a toujours un objet'} |")
    L.append("")
    hors = [r for r in sorted(mo.roles_ranges_par_role())]
    if hors:
        L += [f"> **Une page d'un rôle rangé par son rôle n'a pas ce rayon-là.** "
              + ", ".join(
                  f"`{champ_du_role(mo)}: {r}` vit dans `{mo.dossier_de_role(r)}/`"
                  for r in hors)
              + ". Son dossier d'accueil est ce dossier, son rayon est ce "
                "dossier plus son hub, et les lignes d'axe sont sans objet — "
                "à déclarer comme telles, comme toutes les autres.", ""]
    return L


def _trouver_le_dossier(mo: Modele, axe_s: str, axe_p: str,
                        dossier: str) -> list[str]:
    voc = (mo.vocabulaires or {}).get("taxonomie") or {}
    fichier = voc.get("fichier") or "Documentation/taxonomie.md"
    arbre = mo.rangement.get("arbre_de_decision") or []
    n_arbre = len(arbre)
    L = ["---", "",
         f"## Trouver le dossier d'accueil — une DÉRIVATION, pas une décision",
         "",
         f"Personne ne choisit un dossier. Il se dérive de `{mo.champ_rangement}:`, "
         f"qui se dérive elle-même de l'arbre de décision de `{fichier}` — "
         f"{n_arbre} questions fermées, **ordre strict, première réponse "
         f"positive gagne**.", "",
         f"1. Dérouler l'arbre de `{mo.champ_rangement}:` — jamais à "
         f"l'intuition, jamais en sautant une question.",
         ]
    if mo.champ_nature:
        n_nat = len(mo.nature.get("arbre_de_decision") or [])
        vide = (" Aucune ne tranche → **laisser le champ vide** : c'est le "
                "signal prévu pour « l'arbre n'a pas tranché ». Une valeur "
                "inventée est une faute, un champ vide est une question ouverte."
                if mo.nature_vide_autorise else
                " Aucune ne tranche → **demander**.")
        L.append(f"2. Dérouler l'arbre de `{mo.champ_nature}:` — {n_nat} "
                 f"questions, même méthode.{vide}")
    L += [f"{3 if mo.champ_nature else 2}. **Le dossier est la conséquence**, "
          f"jamais le point de départ.", ""]

    if not mo.exclusif:
        L += [f"### L'axe n'est PAS exclusif — deux mécanismes, et ils sont "
              f"déclarés", "",
              f"Une page peut porter **plusieurs** valeurs de "
              f"`{mo.champ_rangement}:`, ou aucune. Deux mécanismes rangent "
              f"quand même, et aucun n'est une échappatoire :", ""]
        if mo.regle_de_majorite:
            L.append(f"- **la règle de majorité** — "
                     f"{commun.ligne(mo.rangement.get('definition_de_la_majorite'))}. "
                     f"Le dossier se dérive de cette valeur-là ; le validateur "
                     f"vérifie seulement qu'il correspond à une valeur que la "
                     f"page porte **vraiment**.")
        if mo.prefixe_transversal:
            L.append(f"- **le préfixe `{mo.prefixe_transversal}`** — réservé à "
                     f"ce qui n'a **aucun** centre de gravité. Il l'emporte sur "
                     f"tout le reste. Une page qui a un centre de gravité, même "
                     f"si elle en déborde, prend la règle de majorité : le "
                     f"préfixe transversal n'est pas la case « je ne sais pas ».")
        L.append("")

    L += [f"### Le seuil — une insertion peut PROMOUVOIR un sous-dossier", "",
          f"Un sous-dossier apparaît quand une sous-valeur atteint **{mo.seuil}** "
          f"pages"
          + (", sauf s'il ne laisse aucune page au niveau du parent."
             if mo.plafond else ".")
          + f" **La page qu'on insère COMPTE dans ce seuil** : la dérivation "
            f"doit la voir avant l'écriture.", "",
          "```bash",
          f'V="{commun.valeur_exemple(mo)}"'.ljust(34)
          + "# la valeur dont on veut la population",
          (f'grep -rn "^{mo.champ_rangement}:" --include="*.md" . '
           f'| grep -c "$V"').ljust(34) + "# + 1 pour la page à insérer",
          "```", "",
          f"Si le compte franchit **{mo.seuil}**, ce n'est plus une insertion, "
          f"c'est une **réorganisation** : le dossier se crée, ses pages y "
          f"descendent par `git mv`, il prend un hub à son nom. **Le signaler "
          f"avant de le faire**, et passer par `brainkit re-seuiller` plutôt "
          f"que de déplacer à la main.", ""]
    return L


def _lister_le_rayon(mo: Modele, lignes: list[propagation.Ligne],
                     dossier: str) -> list[str]:
    cr = champ_du_role(mo)
    return ["---", "", "## Lister le rayon — une commande, une liste FERMÉE", "",
            "```bash",
            f'D="{dossier}"'.ljust(34) + "# le dossier dérivé, pas deviné",
            'ls -1 "$D"'.ljust(34) + "# tout le voisinage, en clair",
            'dirname "$D"'.ljust(34) + "# le parent ; remonter jusqu'à la racine",
            f'grep -H "^{cr}:" "$D"/*.md'.ljust(34) + "# ce que chaque voisin EST",
            "```", "",
            f"Ce que `ls` rend, ligne par ligne : le hub du dossier "
            f"(`<Dossier>.md`), les pages des autres rôles, et les pairs. "
            f"**Rien ne se lit dans un chemin** : deux pages du même dossier "
            f"peuvent avoir deux rôles et deux règles — d'où le `grep` sur "
            f"`{cr}:`.", "",
            "**« Les pages connexes » n'est pas une liste. La sortie de "
            "`ls -1` en est une.**", ""]


def _conventions(mo: Modele) -> list[str]:
    cr = champ_du_role(mo)
    ident = mo.champ_de_fonction("identite") or "nom"
    resume = propagation.champ_resume(mo)
    L = ["---", "", "## Conventions non négociables", "",
         f"- **Le dossier se dérive, il ne se choisit pas.** Une page posée "
         f"« là où ça semble logique » fait sortir un constat "
         f"`chemin_categorie`, et il sort après coup.",
         f"- **Wikilinks NUS, toujours** : `[[Nom]]`, jamais "
         f"`[[Dossier/Sous/Nom|Nom]]`. Le pipe ne sert qu'à changer le texte "
         f"affiché. Un lien qui porte un chemin casse au premier `git mv` — et "
         f"il y en aura, au premier re-seuillage.",
         f"- **Contrepartie du lien nu : le nom de fichier d'une page nouvelle "
         f"est UNIQUE dans tout le vault**, à la casse près. À vérifier "
         f"**avant** de créer, y compris pour un hub à créer :",
         "",
         "  ```bash",
         '  find . -iname "<Nom>.md" -not -path "./.git/*"   # doit être vide',
         "  ```", "",
         f"- **Frontmatter EXACT** selon le gabarit du rôle : ni plus, ni "
         f"moins. C'est `{cr}:` qui choisit le gabarit, et tout champ hors de "
         f"`autorises` fait échouer la page. Les gabarits sont dans "
         f"`Templates/`, **générés** : ne pas les éditer à la main.",
         f"- **`{ident}:` est le nom du fichier**, à l'identique.",
         ]
    if resume:
        L.append(f"- **`{resume}:` s'écrit UNE fois, sur sa page, et se COPIE "
                 f"partout ailleurs.** Jamais retapé, jamais reformulé : une "
                 f"phrase retapée diverge, et rien ne le dit.")
    L += [f"- **La prose ne vit que dans une section `genre: prose`.** Partout "
          f"ailleurs : des puces, une ligne une idée.",
          f"- **Une section conditionnelle qu'on ne peut pas remplir se "
          f"SUPPRIME**, elle ne se pose pas vide. Le gabarit le dit en "
          f"commentaire, section par section.",
          f"- **Un vocabulaire fermé se pioche, il ne s'invente pas.** Une "
          f"valeur manquante se **propose**, s'ajoute dans son fichier de "
          f"vocabulaire, PUIS s'utilise.",
          f"- **Une zone `<!-- AUTO -->` ne s'édite jamais à la main** : elle "
          f"est régénérée à la clôture, et l'édition sera écrasée.",
          f"- **En cas de doute : demander.** Ne pas deviner une valeur d'axe, "
          f"une date, un auteur. Un champ vide est honnête ; un champ rempli "
          f"au juge ne se distingue plus d'un champ vrai.", ""]
    return L


# --------------------------------------------------------------------------- #
def _mode_cible(mo: Modele, lignes: list[propagation.Ligne], rid: str | None,
                unite: str, dossier: str, cloture: str | None) -> list[str]:
    cr = champ_du_role(mo)
    ident = mo.champ_de_fonction("identite") or "nom"
    L = ["---", "", "## Procédure — mode ciblé", "",
         "Chaque étape a une **fin vérifiable**. Une étape dont on ne peut pas "
         "montrer la sortie n'a pas eu lieu.", "",
         f"1. **Vérifier que la page n'existe pas déjà** — par son `{ident}:` "
         f"et par ses alias.", "",
         "   ```bash",
         '   grep -rn "^' + ident + ': .*<X>" --include="*.md" . | grep -v "/.git/"',
         '   find . -iname "<X>.md" -not -path "./.git/*"',
         "   ```", "",
         "   Elle existe → **basculer sur le mode mise à jour**. Ne jamais "
         "improviser un patch sur une page qui a des consommateurs.", "",
         f"2. **Dériver les valeurs d'axe, PUIS le dossier** — dans cet ordre. "
         f"Fin d'étape : un chemin de dossier écrit, pas une intuition.", "",
         f"3. **Lister le rayon** : `ls -1 \"$D\"` plus la remontée des "
         f"parents. Fin d'étape : **la table remplie NOMINATIVEMENT**, un "
         f"fichier par ligne. Le gabarit de sortie :", "",
         "   ```"]
    for li in lignes:
        L.append(f"   {li.n:3s} {_court(li.cible):42s} : …")
    L += ["   ```", "",
          f"4. **Écrire la page** depuis `Templates/`, dans `$D`. Les faits "
          f"qu'on ne connaît pas restent **vides** — jamais devinés.",
          f"5. **Dérouler la table, ligne par ligne.** C'est l'étape qui porte "
          f"tout le travail, et la seule qu'on est tenté de sauter :", ""]
    for li in lignes:
        L.append(f"   - **{li.n} — {_court(li.cible)}.** {li.par}."
                 + (f" *Sans objet si {li.sans_objet_si} — et alors on le "
                    f"DÉCLARE.*" if li.sans_objet_si else
                    " *Cette ligne a toujours un objet.*"))
    L += ["", "6. **Contrôle final — confronter ce qu'on a touché au dossier.** "
          "Étape obligatoire : c'est elle qui transforme une intention en fait "
          "vérifié.", "",
          "   ```bash",
          "   git status --porcelain          # ce qui a bougé, en fait",
          '   ls -1 "$D"                      # ce qui aurait dû être considéré',
          "   ```", "",
          "   Rendre compte des **trois** cas :", "",
          "   | Cas | Ce qu'on en fait |",
          "   |---|---|",
          "   | fichier du dossier **touché** | normal, il est dans le rayon |",
          "   | fichier du dossier **non touché** | **déclarer pourquoi**. Le "
          "silence n'est pas une réponse |",
          "   | fichier touché **hors du dossier** | légitime pour les hubs "
          "parents, les hubs transverses et un hub de ralliement ; **suspect** "
          "partout ailleurs — l'expliquer ou le défaire |", "",
          "7. **Vérifier les réciprocités et la réinjection**, avant de clore :",
          "", "   ```bash"]
    if mo.champs_a_reciprocite():
        L.append("   brainkit valider --regle reciprocite")
    if propagation.champ_resume(mo):
        L.append("   brainkit valider --regle reinjection_du_resume")
    L += ["   brainkit valider --regle completude_du_hub",
          "   ```", "",
          "   Fin d'étape : **0 constat** sur chacune."]
    if cloture:
        L += ["", f"8. **Clôturer** : invoquer `{cloture}`. La capture n'est "
              f"pas finie tant que la clôture n'a pas tourné — mais elle ne "
              f"fait pas partie de ce skill-ci.", "",
              f"**Sortie attendue de ce skill** : la table remplie ligne par "
              f"ligne, le résultat du contrôle de l'étape 6, et « la capture "
              f"est faite, `{cloture}` reste à lancer » — ou son résultat s'il "
              f"a déjà tourné. **Ne jamais laisser l'état implicite** : c'est "
              f"ainsi qu'un index périmé survit à une session.", ""]
    else:
        L += ["", "8. **Clôturer** : régénérer et valider (cf. *Lancer le "
              "kit*).", ""]
    return L


def _court(s: str) -> str:
    """Le libelle d une cible, sans son incise — pour un gabarit de sortie."""
    for sep in (" — ", " -- "):
        if sep in s:
            s = s.split(sep)[0]
    return s.strip()


# --------------------------------------------------------------------------- #
def _mode_lot(mo: Modele, lignes: list[propagation.Ligne], unites: str,
              axe_s: str, cloture: str | None, decl: dict) -> list[str]:
    inbox = _inbox(mo)
    motif = commun.ligne(decl.get("motif_mode_lot"))
    L = ["---", "", "## Procédure — mode LOT (l'amorçage)", "",
         f"Déclencheurs : « amorce le brain », « ajoute ces quinze titres », "
         f"« vide l'inbox ». C'est le mode qui rend un brain neuf utilisable : "
         f"**capturer dix à vingt {unites} d'un même dossier en une "
         f"conversation, en n'appliquant le rayon qu'UNE fois, à la fin**.", ""]
    if motif and motif != "—":
        L += [f"> {motif}", ""]
    L += ["### Ce que le mode lot change, et ce qu'il ne relâche PAS", "",
          "| Ce qui change | Ce qui ne change pas |",
          "|---|---|",
          "| le rayon s'applique **une fois pour le lot**, pas N fois | la "
          "table est remplie **ligne par ligne**, et une ligne sans objet se "
          "déclare |",
          "| une seule clôture, un commit par dossier | chaque page est écrite "
          "en entier, gabarit respecté |",
          "| les réciprocités **entre pages du lot** se posent au fil de l'eau "
          "| les réciprocités avec les pages **déjà là** se posent au rayon |",
          "| le plan passe avant l'écriture | rien ne s'écrit avant le GO |", "",
          "### Le danger propre au mode lot — le SEUIL", "",
          f"C'est le seul risque que le mode ciblé n'a pas. Dix pages posées "
          f"d'un coup peuvent faire franchir le seuil de **{mo.seuil}** à une "
          f"sous-valeur, et donc **promouvoir un sous-dossier au milieu du "
          f"lot**. Le compte se fait sur le lot **entier**, avant d'écrire la "
          f"première page — pas page par page.", "",
          f"Si le lot promeut : le dire, et traiter la promotion comme une "
          f"réorganisation (`brainkit re-seuiller`), **avant** de capturer. "
          f"Capturer d'abord et déplacer ensuite double le travail et perd des "
          f"liens.", "",
          "### Les étapes", "", ]
    n = 1
    if inbox:
        L.append(f"{n}. **Prendre la file** — `{inbox}` porte le premier "
                 f"backlog : des titres identifiés, **et pas une page écrite**. "
                 f"C'est le point de départ naturel du lot.")
        n += 1
    L += [f"{n}. **Grouper par dossier d'accueil.** C'est ce qui fait le lot : "
          f"un dossier, un rayon. Deux dossiers = deux lots, traités l'un "
          f"après l'autre.",
          f"{n+1}. **Présenter le plan et ATTENDRE LE GO.** Une ligne par page : "
          f"nom, rôle, valeurs d'axe, dossier dérivé, et si elle existe déjà. "
          f"Signaler toute promotion de sous-dossier. **Ne rien écrire avant.**",
          f"{n+2}. **Écrire les N pages**, gabarit par gabarit. Les liens "
          f"**entre pages du lot** se posent maintenant, dans les deux sens : "
          f"elles arrivent ensemble, elles se connaissent.",
          f"{n+3}. **Appliquer le rayon UNE fois**, pour le lot entier, ligne "
          f"par ligne. Les pairs à traiter sont les pages **qui étaient déjà "
          f"là** — celles du lot sont déjà câblées.",
          f"{n+4}. **Contrôle final** : `git status --porcelain` confronté à "
          f"`ls -1 \"$D\"`, comme en mode ciblé. Le diff doit contenir les N "
          f"pages, les fichiers du rayon, et rien d'autre.",
          ]
    if inbox:
        L.append(f"{n+5}. **Cocher dans `{inbox}`** — au fur et à mesure, pas à "
                 f"la fin. Une file à moitié drainée dont rien n'est coché est "
                 f"une file perdue.")
        n += 1
    if cloture:
        L.append(f"{n+5}. **Clôturer une fois** : `{cloture}`.")
    L.append("")
    return L


def _inbox(mo: Modele) -> str | None:
    for p in ((mo.m.get("racine") or {}).get("pages") or []):
        if p.get("role_editorial") == "capture":
            return str(p.get("fichier"))
    return None


# --------------------------------------------------------------------------- #
def _mode_mise_a_jour(mo: Modele, cloture: str | None) -> list[str]:
    effets = propagation.effets_de_bord(mo) + propagation.effets_hors_champ(mo)
    L = ["---", "", "## Procédure — mode mise à jour", "",
         "**Règle d'or** : une modification de champ n'est pas finie quand la "
         "page est enregistrée. Elle est finie quand ses **consommateurs** sont "
         "à jour et que la **commande de vérification** ne renvoie plus aucun "
         "écart.", "",
         "Une page qu'on crée n'a aucun consommateur ; une page qui existe en a. "
         "C'est toute la différence avec le mode ciblé.", "",
         "**Le rayon borne aussi ce travail** : un champ modifié se propage au "
         "**dossier de la page**, pas au vault entier. La colonne *Rayon* de la "
         "table dit, champ par champ, ce qui bouge. Un seul champ fait "
         f"exception et sort du dossier : `{mo.champ_rangement}:`, qui "
         f"**déplace la page** et lui fait donc changer de rayon.", "",
         "1. **Relever l'état AVANT**, avant toute écriture :", "",
         "   ```bash",
         "   sed -n '/^---$/,/^---$/p' \"<chemin>\" | tee /tmp/avant.txt",
         "   ```", "",
         "2. **Déclarer les champs qui changent**, un par un, sous la forme "
         "`champ : avant → après`. Un champ absent de cette liste n'a pas le "
         "droit de bouger.",
         "3. **Dresser la liste NOMINATIVE des consommateurs** : pour chaque "
         "champ déclaré, lire sa ligne dans la table ci-dessous et lancer sa "
         "commande d'inventaire. Fin d'étape : une liste de **chemins de "
         "fichiers**, pas une intention.",
         "4. **Patcher la page section par section** — jamais de réécriture "
         "intégrale. `git diff -- \"<chemin>\"` ne doit montrer aucun champ "
         "hors de la liste de l'étape 2.",
         "5. **Propager chaque consommateur `[M]`.** Fin d'étape : chaque "
         "fichier de la liste de l'étape 3 apparaît dans "
         "`git diff --name-only`. Un fichier de la liste absent du diff = une "
         "propagation oubliée.",
         "6. **Lancer la commande de vérification de chaque champ modifié.** "
         "**0 écart** sur chacune. Ne pas passer à la suite avec un écart "
         "restant : c'est exactement ainsi que naissent les résumés périmés.",
         "7. **Contrôle final**, identique au mode ciblé.",
         ]
    if cloture:
        L.append(f"8. **Clôturer** : `{cloture}`. Il est idempotent.")
    L += ["", "### Table des effets de bord — champ modifié → consommateurs → "
          "vérification", "",
          "Les quatre marqueurs :", "",
          f"- **{propagation.MANUEL}** propagation **manuelle** obligatoire — "
          f"rien ne la fera à votre place ;",
          f"- **{propagation.GENERATEUR}** corrigé par `brainkit generer "
          f"--ecrire` ;",
          f"- **{propagation.DECLARE}** **déclaré** — une règle du validateur le "
          f"contrôle ;",
          f"- **{propagation.SILENCIEUX}** dérive **silencieuse** : aucun "
          f"contrôle n'existe.", "",
          f"> **Ce que `{propagation.DECLARE}` veut dire sur un brain neuf.** "
          f"Les règles **comptent**, elles ne **bloquent** pas : elles sortent "
          f"toutes en `a_mesurer` tant que personne n'a mesuré. Une règle ne se "
          f"durcit qu'après un comptage écrit — c'est le travail du lot 8 du "
          f"kit, pas une case à cocher à la volée.", "",
          "| Champ modifié | Rayon | Consommateurs | Inventaire | Vérification "
          "(0 écart attendu) |", "|---|---|---|---|---|"]
    for e in effets:
        cons = " · ".join(e.consommateurs)
        inv = f"`{e.inventaire}`" if e.inventaire != "—" else "—"
        ver = e.verification or "—"
        nom = e.champ if e.champ.startswith("**") else f"`{e.champ}:`"
        L.append(f"| {nom} | {e.rayon} | {cons} | {_pipe(inv)} | {_pipe(ver)} |")
    L += ["", "### D'où sort chaque ligne de cette table", "",
          "| Champ | Ce qui la produit dans le manifeste |", "|---|---|"]
    for e in effets:
        nom = e.champ if e.champ.startswith("**") else f"`{e.champ}:`"
        L.append(f"| {nom} | {e.origine} |")
    L.append("")
    return L


def _pipe(s: str) -> str:
    return s.replace("|", "\\|")


# --------------------------------------------------------------------------- #
def _anti_patterns(mo: Modele, lignes: list[propagation.Ligne],
                   cr: str) -> list[str]:
    resume = propagation.champ_resume(mo)
    proteges = [r for r in sorted(mo.roles) if mo.roles[r].get("protege")]
    L = ["---", "", "## Anti-patterns", "",
         "- **Écrire la page et s'arrêter là.** Le rayon n'est pas optionnel : "
         "une page insérée sans lui dégrade la structure au lieu de l'enrichir.",
         "- **Sauter une ligne de la table en silence.** Une ligne sans objet "
         "se **déclare** sans objet. C'est la seule chose que ce skill contrôle "
         "et qu'aucun validateur ne peut contrôler à sa place.",
         "- **Deviner le dossier au lieu de le dériver.** Le constat sort après "
         "coup, quand la page est déjà écrite et citée.",
         "- **Sauter le contrôle final.** Confronter `git status` au `ls` du "
         "dossier est ce qui transforme une intention en fait vérifié.",
         "- **Modifier un champ d'une page existante sans dérouler la table des "
         "effets de bord.** C'est l'origine mesurée des résumés périmés.",
         "- **Poser une réciprocité d'un seul côté.** Une moitié orpheline ne "
         "se voit pas en relisant une seule page.",
         ]
    for a, b in propagation.paires_inverses(mo):
        L.append(f"- **Confondre `{a}:` et `{b}:`.** « A {a} B » implique "
                 f"« B {b} A », **pas** « B {a} A ». Écrire le même champ des "
                 f"deux côtés fabrique une relation fausse que la règle "
                 f"`reciprocite` signale, et qu'un relecteur humain ne voit pas.")
    if resume:
        L.append(f"- **Retaper un `{resume}:` au lieu de le copier.** Une "
                 f"phrase retapée diverge, et personne ne le voit avant six mois.")
    for r in proteges:
        L.append(f"- **Réécrire une page `{cr}: {r}` sans que le propriétaire "
                 f"du brain l'ait demandé.** La créer est normal ; la réécrire "
                 f"ne l'est pas. Proposer, et attendre.")
    L += ["- **Écrire un wikilink qualifié par un chemin.** Il casse au premier "
          "`git mv`, et le premier re-seuillage en fera beaucoup.",
          "- **Éditer une zone `<!-- AUTO -->` à la main.** Elle sera écrasée à "
          "la clôture.",
          "- **Inventer une valeur de vocabulaire fermé** pour éviter de "
          "demander.",
          "- **Remplir un champ au juge** parce que le laisser vide « fait "
          "négligé ». Une page vide honnêtement vaut mieux qu'une page remplie "
          "au juge : la seconde ne se distingue plus d'une page vraie.", ""]
    return L


def _voir_aussi(mo: Modele, cloture: str | None) -> list[str]:
    expl = commun.nom_du_skill(mo, "exploitation")
    voc = mo.vocabulaires or {}
    L = ["---", "", "## Voir aussi", ""]
    if cloture:
        L.append(f"- `{cloture}` — la clôture, appelée en fin de chaque "
                 f"procédure. **Seul endroit où la politique git de ce brain "
                 f"est écrite**, à l'exception de la règle d'identité, qui est "
                 f"dans `CLAUDE.md` parce qu'elle doit être lue à **chaque** "
                 f"conversation.")
    if expl:
        L.append(f"- `{expl}` — l'exploitation, qui consomme l'index produit "
                 f"par la clôture.")
    for nom, decl in sorted(voc.items()):
        if (decl or {}).get("fichier"):
            L.append(f"- `{decl['fichier']}` — le vocabulaire `{nom}` "
                     f"(`{decl.get('mode', 'libre')}`)"
                     + (", **généré** depuis `brain.yml` : ne pas l'éditer à la "
                        "main" if decl.get("genere") else ""))
    L += ["- `Templates/` — un gabarit par rôle, **généré**.",
          "- `CLAUDE.md` — le routeur, les frontières d'écriture et la règle "
          "d'identité git.",
          "- `brain.yml` — LE manifeste. Tout ce que ce skill vient de dire en "
          "sort ; rien n'y a été ajouté à la main.", ""]
    L += commun.bloc_frontieres(mo)
    return L
