"""entretien.py — ce que le semis pose DE l entretien dans l instance.

Deux choses, et elles n ont pas le meme statut.

# 1. Le BROUILLON — la trace

`AI/entretien/entretien.yml` : les quarante-neuf questions et les reponses qui
leur ont ete faites, avec leur provenance et leur horodatage.

Ce n est pas un vestige. C est la seule trace de POURQUOI la taxonomie est
celle-la, au-dela des `motif:` que le manifeste porte deja. Six mois plus tard,
« pourquoi sept paquets et pas cinq ? » se relit dans le rangement que
l utilisateur a fait de sa main, et « d ou vient l identite git ? » se verifie
sur la provenance de la reponse 0.4.

Il est pose SI ET SEULEMENT SI l entretien en a fourni un. Un manifeste ecrit a
la main n a pas de brouillon, et le semis ne fabrique pas une trace qui n existe
pas — ce serait la pire des traces.

# 2. Le SKILL de reprise — l outil

`.claude/skills/reprendre-l-entretien/SKILL.md` : instancie, pas copie.

Il ne fait pas le meme travail que le skill du kit. Celui du kit MENE un
entretien depuis rien ; celui-ci REOUVRE une question sur un brain qui existe
deja, et il connait le prix de chaque reponse qu on change — certaines coutent
une ligne, d autres une migration de tout l arbre.

C est le seul skill que le semis instancie, et la raison est nette : les trois
autres (capture, cloture, exploitation) sont le lot 7, et poser un skill a
moitie serait pire que ne pas en poser — il serait charge, et il mentirait.
Celui-ci, lui, est complet, parce que tout ce qu il dit se derive du manifeste
qu on vient d ecrire.
"""

from __future__ import annotations

from ..valider.manifeste import Modele
from .plan import Plan

QUOI = "entretien"
NOM_DU_SKILL = "reprendre-l-entretien"


def seme_l_entretien(mo: Modele, plan: Plan, brouillon: str | None = None) -> None:
    racine_agent = str(((mo.m.get("agent") or {}).get("racine") or "AI")).strip("/")
    if brouillon:
        plan.pose(f"{racine_agent}/entretien/entretien.yml", brouillon, QUOI)
    plan.pose(f".claude/skills/{NOM_DU_SKILL}/SKILL.md",
              _skill(mo, racine_agent, bool(brouillon)), QUOI)


# --------------------------------------------------------------------------- #
def _skill(mo: Modele, racine_agent: str, avec_brouillon: bool) -> str:
    nom = mo.brain.get("nom") or "ce brain"
    unite = mo.mot("unite", "s")
    unites = mo.mot("unite", "p")
    axe = mo.libelle_rangement.get("s") or "domaine"
    axes = mo.libelle_rangement.get("p") or "domaines"
    prefixes = mo.rangement.get("prefixes") or []
    seuil = mo.seuil
    proteges = [r for r in mo.roles.values() if r.get("protege")]
    chemin_brouillon = f"{racine_agent}/entretien/entretien.yml"

    L: list[str] = [
        "---",
        f"name: {NOM_DU_SKILL}",
        f"description: Rouvre une question de l'entretien qui a construit "
        f"{nom} et recompose son `brain.yml`. À utiliser quand l'utilisateur "
        f"veut changer la taxonomie de ce brain — ajouter un(e) {axe}, "
        f"renommer un rôle, changer le seuil, ajouter une relation — ou quand "
        f"il demande « pourquoi c'est rangé comme ça ? ». Il applique les "
        f"treize refus de deviner de l'entretien, et il dit le PRIX de chaque "
        f"changement avant de le faire.",
        "---",
        "",
        f"# Reprendre l'entretien de {nom}",
        "",
        f"Ce brain n'a pas été configuré à la main : il est sorti d'un entretien "
        f"de onze passes. Ce skill rouvre ce dialogue — une question à la fois, "
        f"avec le prix affiché.",
        "",
        "## Ce que ce brain est, en six lignes",
        "",
        f"- **Sujet** — {mo.brain.get('sujet') or '(non déclaré)'}",
        f"- **Unité** — la *{unite}* (pluriel : {unites})",
        f"- **Axe de rangement** — le/la *{axe}*, {len(prefixes)} "
        f"{axes} : {', '.join(str(p.get('dossier')) for p in prefixes)}",
        f"- **Seuil de promotion** — {seuil} pages, DÉRIVÉ du volume cible "
        f"({mo.brain.get('volume_cible')})",
        f"- **Rôles** — " + ", ".join(
            f"`{rid}`" for rid in sorted(mo.roles)),
        f"- **Protégés** — " + (", ".join(
            f"`{r['id']}`" for r in proteges) if proteges else
            "aucun rôle n'est protégé"),
        "",
    ]

    if avec_brouillon:
        L += [
            "## Les réponses qui l'ont produit",
            "",
            f"Elles sont dans `{chemin_brouillon}` : les quarante-neuf "
            f"questions, ce qui a été répondu, par qui et quand.",
            "",
            "**Lis-les avant de changer quoi que ce soit.** La plupart des "
            "« pourquoi c'est comme ça ? » y trouvent leur réponse sans qu'on "
            "ait à rouvrir la question — en particulier la 2.2, le rangement "
            f"que l'utilisateur a fait de sa main et d'où les {len(prefixes)} "
            f"{axes} ont été induits.",
            "",
            "```bash",
            f"uv run brainkit entretien --brouillon {chemin_brouillon} --etat",
            f"uv run brainkit entretien --brouillon {chemin_brouillon} --rappel",
            "```",
            "",
        ]
    else:
        L += [
            "## Ce brain n'a pas de brouillon d'entretien",
            "",
            "Son `brain.yml` n'est pas sorti d'un entretien — il a été écrit ou "
            "repris à la main. Ce skill fonctionne quand même, mais il ne peut "
            "pas te dire POURQUOI une valeur est celle-là : il n'y a pas de "
            "trace. Les `motif:` du manifeste sont tout ce qu'il reste.",
            "",
        ]

    L += [
        "## Rouvrir une question",
        "",
        "```bash",
        f"uv run brainkit entretien --brouillon {chemin_brouillon} --oublier 2.2",
        f"uv run brainkit entretien --brouillon {chemin_brouillon} "
        f"--repondre '2.2=…'",
        f"uv run brainkit entretien --brouillon {chemin_brouillon} --verifier",
        f"uv run brainkit entretien --brouillon {chemin_brouillon} "
        f"--composer brain.yml",
        "```",
        "",
        "**Les treize refus s'appliquent toujours.** En particulier : aucune "
        "sévérité ne se durcit ici (`a_mesurer` partout tant que personne n'a "
        "mesuré), aucun paquet ne se propose, et l'identité git ne se re-devine "
        "pas — elle est déjà en config locale, elle ne se lit nulle part "
        "ailleurs.",
        "",
        "## Le PRIX de chaque changement — à dire AVANT de le faire",
        "",
        "| Ce qu'on change | Ce que ça coûte |",
        "|---|---|",
        f"| un `motif:`, une définition, une frontière | rien — c'est du texte |",
        f"| une colonne de bandeau | `brainkit generer --ecrire` refait les "
        f"bandeaux de toutes les {unites} |",
        f"| une section du corps | le gabarit change ; les pages DÉJÀ écrites "
        f"ne bougent pas, et l'écart se voit à la relecture |",
        f"| **le seuil de promotion** | une MIGRATION : `brainkit re-seuiller` "
        f"déplace des pages par `git mv`. Jamais à la main. |",
        f"| **ajouter un(e) {axe}** | un dossier et son hub ; les pages "
        f"existantes ne bougent pas, mais l'arbre de décision doit gagner sa "
        f"branche, AU BON RANG |",
        f"| **retirer un(e) {axe}** | les pages qui le portent deviennent "
        f"orphelines. Ne jamais le faire sans les avoir déplacées d'abord. |",
        f"| **renommer un rôle** | le `role:` de chaque page concernée, le "
        f"gabarit, les hubs, l'index, la table de couleurs. Coûteux, et sans "
        f"outil : à ne faire que tôt. |",
        "",
        "## Après toute recomposition",
        "",
        "```bash",
        "uv run brainkit valider     # le manifeste du vault est pris tout seul",
        "uv run brainkit generer     # --check par défaut : n'écrit rien",
        "```",
        "",
        "Les deux commandes résolvent `./brain.yml` depuis le vault : pas "
        "besoin de `--manifeste`. Si tu en passes un qui n'est pas celui du "
        "vault, elles le disent avant le verdict — un verdict rendu contre le "
        "manifeste d'un autre brain n'aurait aucun sens, et il serait "
        "silencieux.",
        "",
        "## Ce que ce skill ne fait pas",
        "",
        f"- **Il n'écrit aucune page.** Ni {unite}, ni exemple. C'est le skill "
        f"de capture qui écrit dans le brain.",
    ]
    if proteges:
        L.append(
            "- **Il ne touche à aucune page d'un rôle protégé** — ici "
            + ", ".join(f"`{r['id']}`" for r in proteges) +
            ". La frontière est portée par le champ `role:`, pas par un "
            "chemin : lire le frontmatter avant d'écrire.")
    L += [
        "- **Il ne modifie pas ce qui est généré.** Les zones AUTO, l'index, "
        "les bandeaux et la taxonomie se régénèrent ; les éditer à la main "
        "crée un écart que `generer --check` signalera, et que la prochaine "
        "régénération effacera.",
        "",
    ]
    return "\n".join(L)
