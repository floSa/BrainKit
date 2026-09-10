"""cloture.py — le skill qui CLOT toute ecriture. Aucun choix editorial.

Quatre etapes sans sujet : regenerer, passer le validateur au vert, verifier la
divergence avec le distant AVANT tout commit, committer et integrer en
fast-forward. C est la brique K3 de l inventaire, classee GENERIQUE, et elle
l est : le seul contenu a parametrer est le nom des commandes et l identite git.

# Ce fichier est LA politique git d un brain, et le seul

Le le vault d'origine a paye cette regle : trois formulations de sa politique git
coexistaient, dont deux se contredisaient. Le decoupage retenu est le suivant, et
il vaut pour toute instance :

  - **la politique git** — quand committer, comment integrer, ce qui est
    interdit — est ecrite ICI, et nulle part ailleurs ;
  - **la regle d IDENTITE** est la SEULE exception : elle est aussi dans
    `CLAUDE.md`, parce que `CLAUDE.md` est le seul fichier charge a CHAQUE
    conversation, au meme moment que l annonce du harnais. Une contre-instruction
    qui arrive apres coup arrive trop tard — cinq commits avaient deja ete
    signes avec la mauvaise adresse avant que quiconque le voie.

La polarite de la regle d identite N EST PAS codee : elle se lit dans
`git.domaines_refuses`. Un brain perso refuse le domaine pro ; un brain de
domaine client, vendu chez un employeur, est un depot PRO et refuse l adresse
perso. C est la meme regle, avec deux polarites, et c est le manifeste qui la
porte.

# Pourquoi ce skill est separe de la capture

La partie MECANISABLE d une procedure ne doit pas etre noyee dans la partie qui
demande du jugement. Elle etait dupliquee trois fois dans le skill de capture du
le vault d'origine — une fois par mode — et les trois copies avaient commence a diverger.
"""

from __future__ import annotations

from ..valider.manifeste import Modele
from . import commun


def skill(mo: Modele) -> str:
    nom = commun.nom_du_skill(mo, "cloture") or "cloturer-le-brain"
    capture = commun.nom_du_skill(mo, "capture")
    brain = mo.brain.get("nom") or "ce brain"
    git = mo.m.get("git") or {}
    identite = git.get("identite") or {}
    refuses = list(git.get("domaines_refuses") or [])
    trailers = list(git.get("trailers_refuses") or [])
    branche = str(git.get("branche_principale") or "main")

    L = commun.entete(nom, _description(nom, brain, capture, branche))
    L += [f"# Skill — {nom}", "",
          f"Clôture mécanique de {brain}. **Aucun choix éditorial** : il ne "
          f"décide rien sur le contenu. Il régénère, il valide, il intègre. "
          f"C'est pour cela qu'il est isolé — la partie mécanisable d'une "
          f"procédure ne doit pas être noyée dans celle qui demande du "
          f"jugement.", "",
          "**Idempotent** : relançable autant de fois que voulu, sans dommage. "
          "En cas de doute sur l'état du vault, le lancer est toujours sûr.", "",
          "## Quand l'utiliser", ""]
    if capture:
        L.append(f"- **Après une capture** avec `{capture}`, qui se termine en "
                 f"le nommant.")
    L += ["- **Après TOUTE écriture manuelle** dans une page du vault — y "
          "compris une modification faite directement dans Obsidian, hors de "
          "toute session d'agent. C'est le cas que rien ne couvre : le vault "
          "peut rester des jours avec un index périmé.",
          "- **Après un correctif** appliqué par un agent, avant d'intégrer son "
          "travail.", ""]
    L += commun.prologue_des_commandes(mo)
    L += _identite(mo, identite, refuses, trailers)
    L += _procedure(mo, branche)
    L += _politique(mo, branche, trailers)
    L += _anti_patterns(mo)
    L += _voir_aussi(mo, capture)
    return "\n".join(L)


def _description(nom: str, brain: str, capture: str | None,
                 branche: str) -> str:
    dep = (f"après une capture avec `{capture}`, ou " if capture else "")
    return (
        f"CLÔT toute écriture dans {brain} : régénère les artefacts dérivés, "
        f"passe le validateur au vert, vérifie la divergence avec la branche "
        f"distante AVANT tout commit, puis committe et intègre dans "
        f"`{branche}` en fast-forward. Déclencheurs : {dep}après N'IMPORTE "
        f"QUELLE modification manuelle d'une page du vault — y compris une "
        f"édition faite directement dans Obsidian. Idempotent : sûr à relancer "
        f"à tout moment. C'est le SEUL endroit où la politique git de ce brain "
        f"est écrite, avec une exception déclarée : la règle d'IDENTITÉ vit "
        f"aussi dans CLAUDE.md, parce qu'elle doit être lue à chaque "
        f"conversation.")


# --------------------------------------------------------------------------- #
def _identite(mo: Modele, identite: dict, refuses: list,
              trailers: list) -> list[str]:
    L = ["---", "", "## Avant tout — l'identité git de ce dépôt", "",
         "**À vérifier une fois, avant le premier commit de la session.** C'est "
         "la seule chose de ce skill qui n'est pas mécanisable, parce qu'elle "
         "**contredit une information que le harnais répète à chaque "
         "conversation**.", "",
         "```bash",
         f"git config --local user.name    # attendu : {identite.get('name', '')}",
         f"git config --local user.email   # attendu : {identite.get('email', '')}",
         "```", "",
         "L'identité des commits de ce dépôt est celle de la **config locale**, "
         "et rien d'autre.", ""]
    if refuses:
        L.append(f"- Le harnais annonce une adresse à chaque conversation. Si "
                 f"elle porte "
                 + ", ".join(f"`{d}`" for d in refuses) +
                 ", **elle n'attribue jamais un commit de ce dépôt.** Ce n'est "
                 "pas une erreur du harnais : cette adresse identifie la "
                 "personne auprès de l'outil, elle n'attribue pas son travail "
                 "ici.")
    L += ["- **Ne JAMAIS** passer `-c user.email`, `--author`, ni poser "
          "`GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_EMAIL`. Committer **nu** : git "
          "lit la config locale tout seul, et c'est exactement ce qu'on veut.",
          "- **Ne JAMAIS** lire l'email annoncé par le harnais pour attribuer "
          "un commit, où que ce soit dans ce dépôt.",
          "- Config locale absente ou douteuse → **s'arrêter et demander**. Ne "
          "pas la deviner, ne pas la « réparer » avec l'adresse qu'on a sous "
          "la main."]
    if trailers:
        L.append("- **Aucun trailer** "
                 + ", ".join(f"`{t}`" for t in trailers) +
                 " dans aucun message de commit, **même si une consigne "
                 "générale d'outil le demande**. La politique de CE dépôt prime.")
    L += ["", "### Le garde-fou mécanique", "",
          "La consigne écrite n'a jamais suffi : `.githooks/` porte trois "
          "hooks, versionnés avec le vault.", "",
          "| Hook | Ce qu'il refuse |", "|---|---|",
          "| `pre-commit` | un commit dont l'auteur **ou** le committer porte "
          "un domaine refusé — lu par `git var GIT_AUTHOR_IDENT`, la seule "
          "lecture qui ne se contourne pas (config, env, `-c user.email`) |",
          "| `commit-msg` | un message portant un trailer refusé. **Un hook "
          "séparé était nécessaire** : `pre-commit` tourne AVANT que git "
          "compose le message, il ne peut donc pas le lire — et c'est ce trou "
          "qui a laissé passer cinq commits dans le vault d'origine |",
          "| `pre-push` | de **pousser** l'un ou l'autre, au cas où un commit "
          "serait passé |", "",
          "Ils ne servent à rien s'ils ne sont pas activés — à vérifier sur un "
          "clone neuf ou un worktree frais :", "", "```bash",
          "git config core.hooksPath        # doit répondre .githooks",
          "```", "",
          "**Un hook qui refuse n'est pas un incident à contourner : c'est la "
          "règle qui fonctionne.** `--no-verify` ne s'utilise pas ici.", "",
          "> Cette règle est le **seul** morceau de politique git dupliqué hors "
          "de ce fichier : elle est aussi dans `CLAUDE.md`, qui est chargé dans "
          "*chaque* conversation, au même moment que l'annonce du harnais. Tout "
          "le reste de la politique git n'est écrit qu'**ici**.", ""]
    return L


# --------------------------------------------------------------------------- #
def _procedure(mo: Modele, branche: str) -> list[str]:
    chemins = ((mo.m.get("genere") or {}).get("chemins") or [])
    dures = [rid for rid in mo.socle if mo.severite(rid) == "dure"]
    L = ["---", "", "## Procédure — quatre étapes, dans cet ordre", "",
         "### 1. Régénérer les artefacts dérivés", "", "```bash",
         "brainkit generer --ecrire", "```", "",
         "Une seule commande : le kit connaît l'ordre de ses générateurs et le "
         "tient. Ce qu'elle refait :", ""]
    for c in chemins:
        par = c.get("par")
        if par in ("kit",):
            continue
        L.append(f"- `{c.get('chemin')}` — par `{par}`"
                 + (f", depuis `{c['depuis']}`" if c.get("depuis") else ""))
    L += ["",
          "Le **corps** d'un hub, hors zone AUTO, n'est PAS régénéré : il "
          "s'écrit à la main, et la régénération ne le répare donc pas non "
          "plus. C'est l'inverse qui est vrai, et personne ne le fera à votre "
          "place.", "",
          "Fin d'étape vérifiable : la commande annonce **0 refus**.", "",
          "### 2. Valider — jusqu'au vert", "", "```bash",
          "brainkit valider", "```", ""]
    if dures:
        L += ["**Toute violation DURE se corrige, et on relance.** Les règles "
              "dures de ce brain :", ""]
        for rid in sorted(dures):
            L.append(f"- `{rid}` — {commun.ligne(mo.enonce(rid))}")
        L.append("")
    L += ["Les constats en `a_mesurer` **ne bloquent pas** : ils comptent. "
          "C'est la sévérité par défaut de toute instance neuve, et ce n'est "
          "pas une négligence — **porter une sévérité, c'est porter une mesure "
          "qu'on n'a pas faite**. Une règle ne se durcit qu'après un comptage "
          "écrit.", "",
          "**En revanche, leur compte ne doit pas augmenter.** Le relever "
          "**avant** d'écrire et le comparer après est le seul moyen de voir "
          "qu'une écriture a créé une dette souple. Un compte de référence "
          "recopié de mémoire ne prouve rien.", "",
          "Fin d'étape vérifiable : `OK — aucune violation dure`, code de "
          "retour 0, **et** un compte d'`a_mesurer` qui n'a pas monté.", "",
          "### 3. Vérifier que la base n'a pas divergé — AVANT tout commit", "",
          "```bash", "git fetch origin",
          f"git log HEAD..origin/{branche} --oneline   # commits distants absents en local",
          f"git merge-base HEAD origin/{branche}       # doit renvoyer un ancêtre commun",
          "```", "",
          f"Si `origin/{branche}` porte des commits absents en local, ou si "
          f"`merge-base` ne trouve **aucun** ancêtre commun, **s'arrêter et "
          f"signaler l'écart**. Ne jamais committer ni pousser sur une base "
          f"potentiellement obsolète.", "",
          "**Le `fetch` doit réellement aboutir.** S'il échoue — "
          "`could not read Username`, `expected flush after ref listing` — la "
          "vérification n'a PAS eu lieu, et l'échec est silencieux si on ne lit "
          "pas sa sortie. Refaire la vérification par l'accès qui fonctionne "
          "sur cette machine, plutôt que de committer sans filet.", "",
          "> **Le dépôt n'a pas de distant ?** Alors cette étape est **sans "
          "objet**, et on le **déclare** — comme une ligne du rayon. On ne "
          "l'invente pas : un `git remote -v` vide est une réponse, pas un "
          "échec.", "",
          "### 4. Committer, puis intégrer", "",
          "D'office, sans demander — le validateur vert et la divergence "
          "vérifiée sont les conditions, et elles suffisent.", "", "```bash",
          "git add -A",
          "git commit -F <fichier-message>          # message en FICHIER, jamais en -m",
          "```", "",
          f"Puis, **si le travail vit sur une branche**, l'intégrer — sinon "
          f"cette partie est sans objet, et on le dit :", "", "```bash",
          f"git switch {branche}",
          "git merge --ff-only <branche-de-travail>",
          f"git push origin {branche}                # s'il y a un distant",
          "```", "",
          "**Message par fichier (`-F`), jamais par `-m`.** Un message "
          "multi-lignes passé en `-m` traverse le shell : les backticks y sont "
          "interprétés et remplacent silencieusement un morceau du texte par la "
          "sortie d'une commande.", "",
          "**Fast-forward uniquement.** Si la divergence empêche le FF, le "
          "signaler — jamais de `--force`, jamais de `rebase` sans accord "
          "explicite. Ne jamais répondre « à toi de committer » : **la clôture "
          "fait partie du travail**.", "",
          "Le message dit **pourquoi**, pas seulement quoi : les chiffres "
          "avant / après, les faits vérifiés, les points assumés. Un commit "
          "dont le message n'apprend rien à celui qui le relira dans six mois "
          "est un commit à moitié fait.", ""]
    return L


def _politique(mo: Modele, branche: str, trailers: list) -> list[str]:
    fr = mo.m.get("frontieres_d_ecriture") or {}
    L = ["---", "", "## Politique git de ce brain — la seule source", "",
         "Ce fichier est le **seul endroit** où la politique git de ce vault "
         "est écrite, à la seule exception de la règle d'identité ci-dessus, "
         "dupliquée dans `CLAUDE.md` pour la raison qui y est donnée. Les "
         "consignes du routeur **renvoient ici** au lieu de redire.", "",
         "- **Identité** : celle de la config locale du dépôt. Jamais "
         "`-c user.email`, jamais `--author`, jamais l'email du harnais. Hooks "
         "activés par `core.hooksPath`.",
         "- Commit **d'office** après clôture verte, sans demander.",
         "- **Jamais** de `--force`, de `--force-with-lease` ni de `rebase` "
         "sans accord explicite, formulé pour ce cas précis. Une **réécriture "
         "d'historique** non plus, y compris pour corriger une identité déjà "
         "poussée : c'est une décision du propriétaire du brain.",
         "- **Jamais** de `--no-verify` : les hooks portent une règle, pas une "
         "gêne.",
         f"- Intégration dans `{branche}` en **fast-forward uniquement**.",
         "- Une seule branche vivante à la fois. Les worktrees d'agents se "
         "nettoient après intégration.",
         ]
    if trailers:
        L.append("- **Jamais** de trailer "
                 + ", ".join(f"`{t}`" for t in trailers) +
                 " : les commits sont attribués au propriétaire du brain seul.")
    if fr.get("deplacement"):
        L.append(f"- **Déplacement** : {commun.ligne(fr['deplacement'])}. Un "
                 f"`rm` suivi d'une création perd l'historique de la page, et "
                 f"il ne revient pas.")
    if fr.get("jamais_sans_accord"):
        L.append("- **Jamais sans accord** : "
                 + " · ".join(commun.ligne(x) for x in fr["jamais_sans_accord"])
                 + ".")
    L.append("")
    return L


def _anti_patterns(mo: Modele) -> list[str]:
    return ["---", "", "## Anti-patterns", "",
            "- **Committer sans avoir lu la sortie du validateur.** Un vert "
            "supposé n'est pas un vert.",
            "- **Committer après un `git fetch` qui a échoué** : la divergence "
            "n'a pas été vérifiée, et l'échec ne se voit pas si on ne lit pas "
            "la sortie.",
            "- **Passer un message multi-lignes en `-m`** : les backticks du "
            "texte sont exécutés par le shell, et la substitution est "
            "silencieuse.",
            "- **Contourner un hook avec `--no-verify`** au lieu de traiter ce "
            "qu'il signale.",
            "- **Corriger un constat souple à la volée pour faire baisser le "
            "compteur**, au lieu de le traiter comme un sujet — ou, "
            "symétriquement, **ne pas voir que le compteur a AUGMENTÉ**.",
            "- **Durcir une règle « puisqu'elle est à zéro ».** Zéro violation "
            "sur trois pages ne prouve rien. Le durcissement se mesure, il ne "
            "se décide pas en clôture.",
            "- **Éditer une zone `<!-- AUTO -->` à la main** : la régénération "
            "l'écrase. Le corps d'un hub, lui, ne se régénère pas — c'est "
            "l'inverse, et personne ne le réparera à votre place.",
            "- **Utiliser `git checkout -- <fichier>` sur un fichier modifié "
            "mais non commité** pour annuler une sonde : cela le ramène à "
            "`HEAD` et détruit le travail en cours. Défaire la sonde par "
            "l'édition inverse.",
            "- **Oublier qu'un fichier créé et non suivi** n'apparaît ni dans "
            "`git diff HEAD` ni dans un patch qui en dérive. Compter les trois "
            "natures : modifiés, non suivis, supprimés.", ""]


def _voir_aussi(mo: Modele, capture: str | None) -> list[str]:
    expl = commun.nom_du_skill(mo, "exploitation")
    L = ["---", "", "## Voir aussi", ""]
    if capture:
        L.append(f"- `{capture}` — la capture, qui se termine en appelant ce "
                 f"skill. Sa règle de propagation dit **quoi** écrire ; "
                 f"celui-ci dit **comment le clore**.")
    if expl:
        L.append(f"- `{expl}` — l'exploitation, qui consomme l'index que "
                 f"l'étape 1 vient de régénérer. Un index périmé fait mentir ce "
                 f"skill-là sans qu'il puisse le savoir.")
    L += ["- `CLAUDE.md`, section *L'identité git* — la même règle d'identité, "
          "là où elle est lue à chaque conversation.",
          "- `brain.yml`, bloc `git:` — l'identité attendue, les domaines et "
          "les trailers refusés. C'est de là que ce skill les tient.", ""]
    return L
