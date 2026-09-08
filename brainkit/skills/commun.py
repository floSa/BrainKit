"""commun.py — ce que les trois skills partagent, ecrit UNE fois.

Un skill genere est un document, pas du code : il n a ni test unitaire ni
compilateur pour rattraper une phrase fausse. La seule protection est qu une
phrase vraie ne soit ecrite qu a un endroit — c est la meme discipline que le
manifeste applique aux valeurs, appliquee ici aux phrases.

# Le prologue de commande, et pourquoi il existe

Le kit se lance par `brainkit <sous-commande>`, et c est ce que le `CLAUDE.md`
seme ecrit. Sur une instance `kit.mode: branche` fraichement semee, cette
commande n est PAS sur le PATH tant que le kit n a pas ete installe : ni
`brainkit` ni `uv run brainkit` ne resolvent depuis le dossier du vault. Un
skill qui donnerait une commande qui ne tourne pas serait pire qu un skill qui
n en donne aucune — il ferait perdre du temps AVANT d etre corrige.

Les skills donnent donc la commande courte, et une ligne de repli. Le manque de
fond — l instance ne sait pas OU vit le kit — est une remontee du lot 7, pas un
correctif du lot 7.
"""

from __future__ import annotations

from ..generer.prose import champ_du_role
from ..valider.manifeste import Modele


def entete(nom: str, description: str) -> list[str]:
    """Le frontmatter d un SKILL.md. `name` et `description`, et rien d autre."""
    return ["---", f"name: {nom}",
            "description: |"] + [f"  {ligne}" for ligne in _plie(description)] + \
           ["---", ""]


def _plie(texte: str, largeur: int = 76) -> list[str]:
    mots = " ".join(str(texte).split()).split(" ")
    lignes: list[str] = []
    courante = ""
    for mot in mots:
        if courante and len(courante) + 1 + len(mot) > largeur:
            lignes.append(courante)
            courante = mot
        else:
            courante = f"{courante} {mot}".strip()
    if courante:
        lignes.append(courante)
    return lignes


def ligne(v) -> str:
    return " ".join(str(v or "—").split())


def nom_du_skill(mo: Modele, cle: str) -> str | None:
    s = ((mo.m.get("skills") or {}).get(cle) or {})
    nom = s.get("nom")
    return str(nom) if nom else None


def prologue_des_commandes(mo: Modele) -> list[str]:
    """Le bloc « comment lancer le kit », identique dans les trois skills."""
    mode = str((mo.m.get("kit") or {}).get("mode") or "branche")
    L = ["## Lancer le kit", "",
         "Toutes les commandes de ce skill se lancent **depuis la racine du "
         "vault**. Elles résolvent `./brain.yml` toutes seules : pas besoin de "
         "`--manifeste`.", "",
         "```bash",
         "brainkit valider                 # les règles, une par une",
         "brainkit generer                 # `--check` par défaut : n'écrit rien",
         "brainkit generer --ecrire        # régénère les artefacts dérivés",
         "```", ""]
    if mode == "branche":
        scripts = str(((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
        L += [f"> **Si `brainkit` n'est pas sur le PATH**, cette instance est en "
              f"`kit.mode: branche` : le kit vit ailleurs et n'est pas copié "
              f"ici. Deux issues, et aucune n'est une devinette :", "",
              f"> - `export BRAINKIT_RACINE=<racine du dépôt BrainKit>` — c'est "
              f"la première piste que `{scripts}/scripts/_pont_kit.py` essaie, "
              f"et il est posé dans cette instance par le semis ;",
              f"> - `uv run --project <racine du kit> brainkit …` — le kit "
              f"lancé depuis son dépôt.", "",
              f"> Si aucun kit n'est atteignable, le résolveur **sort en 2 et "
              f"imprime les trois pistes** qu'il a essayées. Il ne devine pas : "
              f"un kit deviné est un verdict rendu par un code qu'on n'a pas "
              f"choisi.", ""]
    else:
        L += ["> Cette instance est **figée** (`kit.mode: fige`) : le kit a été "
              "copié dans `AI/scripts/`. Les commandes s'y lancent, et cette "
              "instance ne reçoit plus de correctif du kit.", ""]
    return L


def bloc_frontieres(mo: Modele) -> list[str]:
    """Les frontieres d ecriture, telles que le manifeste les declare."""
    fr = mo.m.get("frontieres_d_ecriture") or {}
    cr = champ_du_role(mo)
    proteges = [rid for rid in sorted(mo.roles) if mo.roles[rid].get("protege")]
    L = ["## Les frontières d'écriture", ""]
    for cle, titre in (("libre", "Libre"),
                       ("sur_confirmation", "Sur confirmation"),
                       ("sur_demande_explicite", "Sur demande EXPLICITE"),
                       ("jamais_a_la_main", "Jamais à la main"),
                       ("jamais_sans_accord", "Jamais sans accord")):
        lot = fr.get(cle) or []
        if lot:
            L.append(f"- **{titre}** — " + " · ".join(ligne(x) for x in lot))
    if fr.get("deplacement"):
        L.append(f"- **Déplacement** — {ligne(fr['deplacement'])}")
    L.append("")
    if proteges:
        L += [f"**La frontière se lit sur le champ `{cr}:`, jamais sur un "
              f"chemin.** " + ", ".join(f"`{cr}: {r}`" for r in proteges) +
              " — création libre dès qu'une capture en a besoin ; "
              "**modification d'une page qui existe déjà sur demande "
              "explicite** seulement. Une page voisine, dans le même dossier, "
              "sous le même hub, peut être protégée : **lire le frontmatter "
              "avant d'écrire.**", ""]
    return L


def mot(mo: Modele, cle: str, nombre: str = "s") -> str:
    return mo.mot(cle, nombre)


def libelle_role(mo: Modele, rid: str, nombre: str = "s") -> str:
    r = mo.roles.get(rid) or {}
    return str((r.get("libelle") or {}).get(nombre) or rid)


def dossier_exemple(mo: Modele) -> str:
    prefixes = mo.rangement.get("prefixes") or []
    return str(prefixes[0].get("dossier")) if prefixes else "<dossier>"


def valeur_exemple(mo: Modele) -> str:
    """Une valeur d axe LEGALE, prise dans le manifeste — jamais inventee."""
    prefixes = mo.rangement.get("prefixes") or []
    if not prefixes:
        return "<valeur>"
    p = prefixes[0]
    sous = list((p.get("sous") or {}))
    if sous:
        return f"{p['cle']}/{sous[0]}"
    return str(p["cle"]) if mo.valeur_courte else f"{p['cle']}/<sous-valeur>"
