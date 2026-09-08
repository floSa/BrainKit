"""install.py — `INSTALL.md`, GENERE. Deux lecteurs, un seul generateur.

# Pourquoi il est genere, et pas ecrit

Propriete 1 du manifeste : *il est la seule source*. L `INSTALL.md` du DevBrain
nomme son coffre, son dossier de gabarits, sa table de couleurs, ses trois
skills et son seuil de promotion — cinq valeurs qui vivent AUSSI dans
`brain.yml`. Ecrit a la main, il prend du retard : c est le constat E4 de
l inventaire, et il est mesure dans le DevBrain lui-meme (`Templates/` a pris
trois lots de retard sur ses 337 pages).

# Deux documents, et la coupure est celle du LECTEUR

| Lecteur | Ou il lit | Ce qu il ne sait pas encore |
|---|---|---|
| celui qui n a **aucun** brain | `INSTALL.md` du depot du kit | tout — il n a ni manifeste, ni vault |
| celui qui recoit **un** brain | `INSTALL.md` de l instance | comment ouvrir CE vault sur SA machine |

Le premier a besoin de la route entiere : installer le kit, mener l entretien,
semer, puis ouvrir. Le second a un vault et un `brain.yml` : il n a rien a
semer, mais il a des valeurs a poser — le nom du coffre, la table de couleurs,
le dossier des gabarits.

C est le meme generateur : `document(None)` rend le premier, `document(mo)` le
second. Un generateur par lecteur aurait fait deux textes a tenir a jour pour
une seule sequence d installation, et le second aurait pris du retard — encore
E4.

# Ce qu il ne contient jamais

Aucune promesse commerciale : ni prix, ni offre, ni argumentaire, ni nom de
client. §5.7 et §5.8 du cadrage ne sont pas tranches, et un depot qui les
trancherait a la place de son proprietaire trancherait mal.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..valider.manifeste import Modele
from . import images

DOSSIER_IMG = "docs/install/img"


# --------------------------------------------------------------------------- #
#  Les plugins : une connaissance DU KIT, keyee par le MECANISME qui l exige
# --------------------------------------------------------------------------- #
# Ce n est pas une valeur d instance, et c est pour ca que la table est ici : un
# plugin est exige par un MECANISME du kit (un gabarit qui porte un jeton, un
# role qui embarque une vue), jamais par le sujet d un brain. La colonne qui
# compte est la derniere : « ce qui le rend necessaire ». Un plugin dont on ne
# sait pas dire quel mecanisme l exige est un plugin qu on n installe pas.
@dataclass(frozen=True)
class Plugin:
    nom: str
    auteur: str
    role: str
    exige_par: str
    requis: bool


PLUGINS: tuple[Plugin, ...] = (
    Plugin("Local REST API & MCP Server", "coddingtonbear",
           "expose le coffre en HTTPS sur la boucle locale, et parle MCP",
           "l'agent lit le vault VIVANT — frontmatter résolu, vues évaluées — "
           "et pas seulement les fichiers du dépôt. Sans lui, un agent voit le "
           "markdown mais pas ce qu'Obsidian en fait", True),
    Plugin("Templater", "SilentVoid13",
           "remplit une page neuve depuis un gabarit de `Templates/`",
           "les gabarits générés portent le jeton `<% tp.file.title %>` quand "
           "le profil est `obsidian` — c'est le kit qui l'écrit, donc c'est le "
           "kit qui exige le moteur qui le résout", True),
    Plugin("File Hider", "eldritch-oliver",
           "masque un dossier de la barre latérale, sans le supprimer",
           "l'espace de l'agent, les gabarits et la gouvernance sont dans le "
           "vault mais ne sont pas des pages : les voir en permanence coûte "
           "de l'attention à chaque recherche", False),
    Plugin("Dataview", "blacksmithgu",
           "requêtes type SQL sur le frontmatter, en ligne dans une page",
           "rien dans le kit ne l'exige. Il sert de repli quand une version "
           "d'Obsidian trop ancienne ne rend pas les vues natives, et pour une "
           "requête jetable qu'on ne veut pas figer en page de vue", False),
)


@dataclass
class Section:
    ident: str
    titre: str
    lignes: list[str] = field(default_factory=list)


def _l(v) -> str:
    return " ".join(str(v or "—").split())


def _profil(mo: Modele | None) -> str:
    if mo is None:
        return "obsidian"
    return str(mo.brain.get("profil") or "obsidian")


def _mode(mo: Modele | None) -> str:
    if mo is None:
        return "branche"
    return str((mo.m.get("kit") or {}).get("mode") or "branche")


def _figures(ancre: str, profil: str) -> list[str]:
    out: list[str] = []
    for c in images.pour(ancre, profil):
        out += images.appel(c, DOSSIER_IMG)
    return out


# --------------------------------------------------------------------------- #
#  1 — Ce que tu obtiens
# --------------------------------------------------------------------------- #
def _apercu(mo: Modele | None) -> Section:
    profil = _profil(mo)
    s = Section("apercu", "Ce que tu obtiens")
    if mo is None:
        s.lignes += [
            "Un **second brain** : un dossier de fichiers markdown, ouvrable "
            "dans Obsidian, versionné dans git, et surtout **contrôlable** — "
            "deux validateurs disent à tout moment si le vault est cohérent, "
            "et quatre générateurs réécrivent ce qui se dérive.", "",
            "La forme ne dépend pas du sujet, et c'est tout l'objet du kit :", "",
            "- **un dossier par valeur de l'axe de rangement**, à la racine, et "
            "rien à côté. Personne ne choisit un chemin : il se **dérive** du "
            "champ de rangement de la page ;",
            "- **un sous-dossier quand une sous-valeur grossit**, jamais avant. "
            "Le seuil est déclaré, et le changer est une migration outillée "
            "(`brainkit re-seuiller`), pas une décision de rangement ;",
            "- **une page par dossier**, dite hub, dont une zone est générée "
            "depuis le contenu du dossier ;",
            "- **un champ qui dit ce qu'une page est** — une unité, une notion, "
            "une vue, une prescription. C'est lui, et pas le chemin, qui décide "
            "du gabarit que le validateur applique ;",
            "- **un manifeste**, `brain.yml`, à la racine. Il porte les mots du "
            "sujet, ses axes, ses gabarits, ses règles et leur sévérité. Le kit "
            "ne sait rien d'autre du brain que ce fichier.", "",
            "Le sujet, lui, est libre : le kit a été extrait d'un brain de "
            "développement logiciel, éprouvé sur un brain d'histoire et sur un "
            "brain de montagne. Aucun de ses mécanismes ne nomme un sujet.", ""]
        return s

    nom = mo.brain.get("nom") or "?"
    mot_s = mo.libelle_rangement.get("s") or "domaine"
    s.lignes += [
        f"**{nom}** — {_l(mo.brain.get('sujet'))}", "",
        f"Un dossier par {mot_s}, à la racine, et rien à côté. Le dossier se "
        f"**dérive** de `{mo.champ_rangement}:` : personne ne choisit un chemin. "
        f"Un sous-dossier apparaît quand une sous-valeur atteint "
        f"**{mo.seuil}** page(s)"
        + (", sauf s'il ne laisserait aucune page au niveau du parent."
           if mo.plafond else ".") + "", "", "```"]
    from ..semer.pages import dossiers_de_l_arbre
    for dossier, _p in dossiers_de_l_arbre(mo):
        s.lignes.append(f"{dossier}/{' ' * max(1, 30 - len(dossier))}"
                        f"({dossier}.md)")
    for rid in sorted(mo.roles_ranges_par_role()):
        d = str(mo.dossier_de_role(rid))
        s.lignes.append(f"{d}/{' ' * max(1, 30 - len(d))}"
                        f"(les pages `{rid}`, groupées par leur rôle)")
    for rid, decl in sorted(mo.roles.items()):
        d = (decl.get("hub_de_ralliement") or {}).get("dossier")
        if d:
            s.lignes.append(f"{d}/{' ' * max(1, 30 - len(d))}"
                            f"(le hub de ralliement des `{rid}`)")
    for t in mo.transverses:
        d = str(t["dossier"])
        s.lignes.append(f"{d}/{' ' * max(1, 30 - len(d))}"
                        f"(un hub par valeur PORTÉE de `{t['champ']}:`)")
    agent = str(((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    s.lignes += [f"Documentation/{' ' * 17}(la taxonomie et les vocabulaires — GÉNÉRÉS)",
                 f"Templates/{' ' * 21}(un gabarit par rôle — GÉNÉRÉS)",
                 f"{agent}/{' ' * max(1, 30 - len(agent))}(l'espace de l'agent)",
                 f"brain.yml{' ' * 22}(LE manifeste — la source de tout ce qui précède)",
                 "```", "",
                 f"Les pages, elles, ne sont pas dans cette liste : un brain "
                 f"neuf n'en porte **aucune** en dehors des hubs. C'est normal, "
                 f"et c'est même le critère de justesse du semis — un semis qui "
                 f"poserait des pages de démonstration poserait du contenu que "
                 f"personne n'a écrit.", ""]
    s.lignes += _figures("apercu", profil)
    return s


# --------------------------------------------------------------------------- #
#  2 — Pré-requis
# --------------------------------------------------------------------------- #
def _prerequis(mo: Modele | None) -> Section:
    profil = _profil(mo)
    mode = _mode(mo)
    s = Section("prerequis", "Pré-requis")
    s.lignes += ["| Outil | Version mini | Vérification | Pourquoi |",
                 "|---|---|---|---|"]
    if profil == "obsidian":
        s.lignes.append("| [Obsidian](https://obsidian.md/download) | 1.10+ | "
                        "l'app s'ouvre | le lecteur du vault, et le moteur des "
                        "vues natives |")
    s.lignes += [
        "| [git](https://git-scm.com/downloads) | — | `git --version` | "
        "l'historique du vault, et les trois garde-fous d'identité |",
        "| [Python](https://www.python.org/downloads/) | 3.10+ | "
        "`python --version` | le kit est écrit en Python |",
        "| [`uv`](https://docs.astral.sh/uv/getting-started/installation/) | — | "
        "`uv --version` | lance le kit sans installer quoi que ce soit dans "
        "l'environnement Python du poste |"]
    if mode == "branche":
        s.lignes.append("| un agent de code (Claude Code ou équivalent) | — | "
                        "`claude --version` | les skills du vault sont écrits "
                        "pour un agent ; le vault se lit et se valide sans lui |")
    s.lignes += ["", "> `uv` n'est pas Python : c'est un lanceur et un "
                 "installateur de paquets. Le kit s'en sert pour tourner sans "
                 "rien salir — et une instance **figée** s'en sert pour tourner "
                 "sans rien installer du tout.", ""]
    if profil == "nu":
        s.lignes += ["**Ce brain est en profil `nu`** : il n'a pas besoin "
                     "d'Obsidian. Voir la section *Le profil `nu`*.", ""]
    return s


# --------------------------------------------------------------------------- #
#  3 — Installer le kit  /  l'atteindre depuis une instance
# --------------------------------------------------------------------------- #
def _installer_le_kit(mo: Modele | None) -> Section:
    if mo is not None:
        return _atteindre_le_kit(mo)
    s = Section("kit.installer", "Installer le kit — et le rendre atteignable")
    s.lignes += [
        "Le kit est un **paquet Python**, pas un dépôt-gabarit qu'on clone puis "
        "qu'on vide. La distinction commande tout le reste : une instance ne "
        "contient **pas de code**, donc une correction du validateur atteint "
        "toutes les instances le jour où elle est faite. Un gabarit cloné, lui, "
        "fourche le jour du clone.", "", "```bash",
        "git clone <url du dépôt BrainKit> ~/BrainKit",
        "cd ~/BrainKit", "```", "",
        "Deux façons de le lancer, et il faut choisir **maintenant** — c'est le "
        "pas qu'on oublie, et un outillage qu'on ne sait pas lancer est un "
        "outillage qui ne tourne pas :", "",
        "**a. depuis le dépôt du kit** — rien à installer, `uv` s'occupe des "
        "dépendances :", "", "```bash",
        "uv run brainkit                 # doit afficher les sept sous-commandes",
        "```", "",
        "**b. sur le PATH** — la commande devient disponible partout, y compris "
        "depuis le dossier d'une instance :", "", "```bash",
        "uv tool install --editable ~/BrainKit",
        "brainkit                        # doit afficher les sept sous-commandes",
        "```", "",
        "Si `brainkit` n'est pas trouvé juste après, c'est que le dossier des "
        "outils `uv` n'est pas sur le PATH. `uv tool update-shell` l'y ajoute, "
        "puis il faut **rouvrir le terminal**.", "",
        "> **Pourquoi ce pas mérite une section.** Une instance sait qu'elle est "
        "branchée sur un kit, elle ne sait pas **où** ce kit vit. C'est un trou "
        "mesuré, et il a deux bouchons : mettre `brainkit` sur le PATH (ici), "
        "ou laisser l'instance le chercher elle-même — le semis pose pour cela "
        "un résolveur dans l'espace de l'agent, qui essaie la variable "
        "`BRAINKIT_RACINE`, puis le kit copié dans l'instance, puis un "
        "`BrainKit/` voisin. Les deux bouchons sont bons, aucun n'est "
        "facultatif : sans l'un ou l'autre, les commandes de ce guide ne "
        "tournent pas depuis le vault.", ""]
    return s


def _atteindre_le_kit(mo: Modele) -> Section:
    mode = _mode(mo)
    agent = str(((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    version = (mo.m.get("kit") or {}).get("version") or "?"
    s = Section("kit.atteindre", "L'outillage de ce vault")
    if mode == "fige":
        s.lignes += [
            f"Ce vault est une instance **figée** (`kit.mode: fige`) : le kit "
            f"`{version}` a été **copié dedans**, sous `{agent}/scripts/`. Il "
            f"est autonome — rien à installer, rien à atteindre :", "",
            "```bash",
            f"uv run {agent}/scripts/valider.py",
            f"uv run {agent}/scripts/generer.py            # --check, n'écrit rien",
            f"uv run {agent}/scripts/generer.py --ecrire",
            "```", "",
            f"**Et il ne recevra plus aucun correctif du kit.** C'est le prix "
            f"du mode, pas un défaut : `{agent}/scripts/FIGE.md` dit ce qui est "
            f"copié, ce qui est perdu, et comment rebrancher à la main.", ""]
        return s
    s.lignes += [
        f"Ce vault est une instance **branchée** (`kit.mode: branche`) : il ne "
        f"contient **pas de code**. Les deux validateurs et les quatre "
        f"générateurs vivent dans BrainKit `{version}`, installé une fois, et "
        f"lisent `brain.yml`. C'est ce qui fait qu'une correction du kit "
        f"atteint ce vault sans qu'on y touche.", "",
        "Installer le kit, puis le rendre atteignable :", "", "```bash",
        "git clone <url du dépôt BrainKit> ~/BrainKit",
        "uv tool install --editable ~/BrainKit",
        "brainkit                        # doit afficher les sept sous-commandes",
        "```", "",
        "Les commandes de tous les jours se lancent alors **depuis la racine de "
        "ce vault**, sans option : elles résolvent `./brain.yml` toutes seules.",
        "", "```bash", "cd <racine de ce vault>",
        "brainkit valider", "brainkit generer                # --check, n'écrit rien",
        "```", "",
        f"**Si le kit n'est pas sur le PATH**, le vault sait le chercher : "
        f"`{agent}/scripts/_pont_kit.py` essaie, dans l'ordre, la variable "
        f"`BRAINKIT_RACINE`, puis un kit copié dans ce vault "
        f"(`{agent}/scripts/brainkit/`), puis un dossier `BrainKit/` chez un "
        f"parent de la racine. Il **s'arrête au premier qui répond** et, si "
        f"aucun ne répond, il sort en 2 et imprime les trois pistes — il ne "
        f"devine pas. Un kit devine est un verdict rendu par un code qu'on n'a "
        f"pas choisi.", "", "```bash",
        f"export BRAINKIT_RACINE=~/BrainKit     # l'échappatoire explicite",
        "```", ""]
    return s


# --------------------------------------------------------------------------- #
#  4 — L'entretien   (document du kit seulement)
# --------------------------------------------------------------------------- #
def _entretien(mo: Modele | None) -> Section | None:
    if mo is not None:
        return None
    s = Section("kit.entretien", "Écrire le manifeste : l'entretien")
    s.lignes += [
        "Un brain neuf commence par **son manifeste**, et le manifeste s'obtient "
        "par un **entretien** — onze passes, quarante-neuf questions, menées en "
        "conversation avec l'agent :", "", "```bash",
        "brainkit entretien --questions      # les 49 questions, et ce que chacune produit",
        "brainkit entretien --refus          # les 13 choses qu'il REFUSE de deviner",
        "```", "",
        "L'entretien n'est pas un formulaire, et ce n'est pas une coquetterie : "
        "il **induit** l'axe de rangement à partir de vingt titres réels que "
        "l'on cite, au lieu de demander « quels sont tes domaines ? ». Une liste "
        "de domaines donnée à froid décrit ce qu'on croit ranger ; vingt titres "
        "décrivent ce qu'on a vraiment.", "",
        "Il **refuse de deviner** treize choses — l'identité git en premier, "
        "parce qu'une identité devinée entre dans l'historique du dépôt et n'en "
        "sort plus. Un refus nomme le champ et rend la question ; il ne pose pas "
        "une valeur plausible.", "",
        "L'entretien écrit un **brouillon** au fil des passes, puis compose le "
        "manifeste :", "", "```bash",
        "brainkit entretien --brouillon mon-brain.entretien.yml",
        "brainkit entretien --brouillon mon-brain.entretien.yml --etat",
        "brainkit entretien --brouillon mon-brain.entretien.yml --verifier",
        "brainkit entretien --brouillon mon-brain.entretien.yml --semer ~/MonBrain",
        "brainkit entretien --brouillon mon-brain.entretien.yml --semer ~/MonBrain --ecrire",
        "```", "",
        "> **La porte de service, et ce qu'elle coûte.** `--reponses <fichier>` "
        "accepte un lot entier de réponses d'un coup, sans conversation. C'est "
        "ce qui rend le jeu d'épreuve possible — rejouer un entretien complet "
        "est la seule façon de **prouver** qu'un entretien produit un vault "
        "vert — et c'est un usage légitime pour qui sait déjà ce qu'il veut. "
        "Mais il faut savoir ce qu'on saute : les treize refus tournent toujours "
        "sur le brouillon et sur le manifeste composé, **pas** sur la "
        "conversation. Ce qu'on perd, c'est le moment où une question ouverte "
        "fait changer d'avis — et c'est là qu'est la valeur de l'entretien. "
        "Employer `--reponses` pour rejouer, pas pour se dispenser de "
        "réfléchir.", ""]
    return s


# --------------------------------------------------------------------------- #
#  5 — Semer   (document du kit seulement)
# --------------------------------------------------------------------------- #
def _semer(mo: Modele | None) -> Section | None:
    if mo is not None:
        return None
    s = Section("kit.semer", "Semer l'instance")
    s.lignes += [
        "Le semis crée le vault : ses dossiers, un hub par dossier, un gabarit "
        "par rôle, la taxonomie et les vocabulaires générés, le routeur de "
        "l'agent, les trois skills, les trois hooks git, le dépôt et son "
        "premier commit.", "", "```bash",
        "brainkit semer --manifeste mon-brain.brain.yml --dans ~/MonBrain",
        "brainkit semer --manifeste mon-brain.brain.yml --dans ~/MonBrain --ecrire",
        "```", "",
        "**Le mode par défaut n'écrit pas un octet.** Le lancer pour voir ce "
        "qu'il ferait est le premier usage de la commande, et il ne doit rien "
        "coûter. `--ecrire` se demande.", "",
        "Le semis **refuse** quatre situations, et aucune n'est négociable :", "",
        "| Refus | Ce qu'il évite |", "|---|---|",
        "| la cible existe et n'est pas vide | écraser un vault qu'on croyait absent |",
        "| la cible vit sous le dépôt du kit | versionner une instance dans le kit |",
        "| la cible vit sous un dépôt git | semer dans un dépôt qui n'est pas le sien |",
        "| la cible vit sous un vault | semer un brain à l'intérieur d'un autre |", "",
        "Il refuse aussi un **manifeste incomplet**, et il rend tous les manques "
        "d'un coup, **avant** d'avoir écrit quoi que ce soit : un vault à demi "
        "semé fait dire n'importe quoi à ses validateurs, et le premier geste de "
        "l'utilisateur serait de réparer une structure que personne n'a cassée.",
        "",
        "Ce que le semis ne fait **pas** : écrire des pages. Un brain neuf porte "
        "un hub par dossier et **rien d'autre**. Ce que l'entretien a récolté — "
        "les vingt titres de la passe d'induction — est posé dans la page de "
        "capture, en cases à cocher : du travail identifié, pas du contenu de "
        "démonstration.", ""]
    return s


# --------------------------------------------------------------------------- #
#  6 — Cloner ce vault   (document d'instance seulement)
# --------------------------------------------------------------------------- #
def _cloner(mo: Modele | None) -> Section | None:
    if mo is None:
        return None
    git = mo.m.get("git") or {}
    identite = git.get("identite") or {}
    refuses = [str(d) for d in (git.get("domaines_refuses") or [])]
    trailers = [str(t) for t in (git.get("trailers_refuses") or [])]
    branche = str(git.get("branche_principale") or "main")
    s = Section("cloner", "Cloner ce vault, et activer ses garde-fous")
    s.lignes += ["```bash", f"git clone <url de ce vault> ~/{mo.brain.get('nom')}",
                 f"cd ~/{mo.brain.get('nom')}", "```", "",
                 "### Activer les hooks — **obligatoire**, une fois par clone", "",
                 "```bash", "git config core.hooksPath .githooks",
                 "git config core.hooksPath        # doit répondre : .githooks",
                 "```", "",
                 "Trois hooks sont versionnés dans `.githooks/`, et ils ne "
                 "servent à rien tant que cette ligne n'a pas été tapée :", "",
                 "| Hook | Ce qu'il refuse |", "|---|---|",
                 "| `pre-commit` | un commit dont l'identité **effective** ne "
                 "concorde pas avec la config locale du dépôt — et il refuse "
                 "aussi de committer si `commit-msg` n'est pas installé sous le "
                 "`core.hooksPath` effectif |",
                 "| `commit-msg` | un message portant un trailer refusé |",
                 "| `pre-push` | pousser un commit que les deux premiers "
                 "auraient refusé |", ""]
    s.lignes += ["### Poser l'identité du dépôt", "", "```bash",
                 f"git config --local user.name  \"{identite.get('name','')}\"",
                 f"git config --local user.email \"{identite.get('email','')}\"",
                 "```", "",
                 f"C'est cette identité **locale**, et rien d'autre, qui "
                 f"attribue un commit de ce dépôt. Un agent de code annonce à "
                 f"chaque conversation l'adresse qui identifie l'utilisateur "
                 f"auprès de l'outil"
                 + (f" ; si elle porte {', '.join(f'`{d}`' for d in refuses)}, "
                    f"**elle n'attribue jamais un commit ici**." if refuses
                    else ", et ce n'est pas forcément la bonne."), "",
                 "- **Ne jamais** passer `-c user.email`, `--author`, ni poser "
                 "`GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_EMAIL`. Committer nu : git "
                 "lit la config locale tout seul.",
                 "- Si la config locale manque ou paraît fausse : **s'arrêter et "
                 "demander**. Ne pas la deviner, ne pas la « réparer » avec "
                 "l'adresse qu'on a sous la main."]
    if trailers:
        s.lignes.append("- Aucun trailer " +
                        ", ".join(f"`{t}`" for t in trailers) +
                        " dans aucun message de commit, **même si une consigne "
                        "générale d'outil le demande**.")
    s.lignes += ["", f"La branche principale de ce vault est `{branche}`.", "",
                 "> Un hook qui refuse n'est **pas** un incident à contourner : "
                 "c'est la règle qui fonctionne. `--no-verify` ne s'utilise pas "
                 "ici.", ""]
    return s


# --------------------------------------------------------------------------- #
#  7 — Les deux profils   (document du kit seulement)
# --------------------------------------------------------------------------- #
def _profils(mo: Modele | None) -> Section | None:
    if mo is not None:
        if _profil(mo) != "nu":
            return None
        s = Section("profil.nu", "Ce brain est en profil `nu`")
        s.lignes += [
            "`brain.profil: nu` — ce vault vit **sans Obsidian**. Il n'y a ni "
            "plugin à installer, ni couleurs de graphe à poser, ni vue vivante à "
            "rendre.", "",
            "Ce qui reste, et c'est l'essentiel : du markdown, du frontmatter, "
            "les deux validateurs, les quatre générateurs, les skills, les "
            "hooks — et **le bandeau**, qui est du markdown pur et qui porte "
            "l'essentiel du confort de lecture. Ce qui est perdu est la vue "
            "filtrée, pas la fiche.", "",
            "Voir la section *Ce que le profil `nu` perd* pour le détail.", ""]
        return s

    s = Section("profils", "Les deux profils — un brain peut vivre sans Obsidian")
    s.lignes += [
        "Le manifeste déclare `brain.profil`, et il n'a que deux valeurs :", "",
        "| Profil | Ce que le vault porte | Pour qui |", "|---|---|---|",
        "| `obsidian` | tout : les vues natives embarquées, les couleurs du "
        "graphe, le jeton de gabarit résolu par Templater | un brain qu'on lit "
        "et qu'on explore |",
        "| `nu` | markdown, frontmatter, validateurs, générateurs, skills, "
        "hooks, **et le bandeau** | un brain lu par un agent, un dépôt de "
        "documentation, un poste où l'on n'installera rien |", "",
        "Ce que `nu` **perd**, nommément :", "",
        "- **les vues vivantes.** Un rôle de fonction `vue` embarque, en profil "
        "`obsidian`, un fichier de requête que le lecteur évalue. En `nu` il n'y "
        "a pas de moteur pour l'évaluer : la page de vue reste une page, sa "
        "section écrite à la main reste la partie qui a de la valeur, et la "
        "table se tient à la main si on la veut.",
        "- **les couleurs du graphe**, donc le graphe comme outil de lecture. La "
        "table reste dans le manifeste, elle n'est simplement pas posée.",
        "- **le jeton de gabarit** : un gabarit `nu` porte `<titre de la page>` "
        "là où un gabarit `obsidian` porte le jeton que Templater résout.",
        "- **le confort** : masquer un dossier, replier un frontmatter, "
        "chercher par nom au clavier. Rien de tout cela n'est un mécanisme du "
        "kit ; tout cela manque quand même.", "",
        "Ce que `nu` **ne** perd **pas** : la dérivation des chemins, la "
        "propagation, les dix règles, la mesure, le semis, le figeage, et la "
        "validité. Un vault `nu` passe les mêmes validateurs qu'un vault "
        "`obsidian` — c'est la preuve que le profil n'est pas une amputation du "
        "modèle, seulement de son lecteur.", ""]
    return s


# --------------------------------------------------------------------------- #
#  8 — Obsidian
# --------------------------------------------------------------------------- #
def _obsidian(mo: Modele | None) -> list[Section]:
    profil = _profil(mo)
    if profil != "obsidian":
        return []
    nom = (mo.brain.get("nom") if mo is not None else None) or "ton brain"
    agent = "AI" if mo is None else str(
        ((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    out: list[Section] = []

    s = Section("obsidian.ouvrir", "Ouvrir le vault dans Obsidian")
    s.lignes += [
        "Obsidian n'importe rien et ne convertit rien : un coffre **est** un "
        "dossier de fichiers. Ouvrir le vault ne le modifie pas.", "",
        "À l'écran d'accueil, **Ouvrir un dossier comme coffre** *(Open folder "
        f"as vault)*, puis choisir la racine de `{nom}` — celle qui porte "
        "`brain.yml`.", ""]
    s.lignes += _figures("obsidian.ouvrir", profil)
    out.append(s)

    s = Section("obsidian.modules", "Autoriser les modules complémentaires")
    s.lignes += [
        "Un coffre neuf est en **mode restreint** : aucun plugin tiers ne "
        "tourne. Paramètres (`Ctrl + ,`) → **Modules complémentaires** "
        "*(Community plugins)* → **Activer les modules complémentaires**.", "",
        "Le réglage est **par coffre** : les autres coffres ne sont pas "
        "touchés.", ""]
    s.lignes += _figures("obsidian.modules", profil)
    out.append(s)

    s = Section("obsidian.plugins", "Installer les plugins")
    requis = [p for p in PLUGINS if p.requis]
    s.lignes += [
        f"**Parcourir** *(Browse)*, puis pour chacun : chercher son nom, ouvrir "
        f"sa carte, **Installer** puis **Activer**. {len(requis)} sont requis, "
        f"{len(PLUGINS) - len(requis)} sont du confort — et la colonne qui "
        f"compte est la dernière : *ce qui le rend nécessaire*. Un plugin dont "
        f"on ne sait pas dire quel mécanisme l'exige est un plugin qu'on "
        f"n'installe pas.", "",
        "| Plugin | Auteur | Rôle | Ce qui le rend nécessaire |",
        "|---|---|---|---|"]
    for p in PLUGINS:
        s.lignes.append(f"| **{p.nom}**{'' if p.requis else ' *(confort)*'} | "
                        f"`{p.auteur}` | {p.role} | {p.exige_par} |")
    s.lignes += ["", "> **Vérifier l'auteur avant d'installer.** Plusieurs de "
                 "ces noms ont des homonymes dans le catalogue, et un homonyme "
                 "ne fait pas la même chose. La colonne *Auteur* est là pour ça.",
                 ""]
    if mo is not None:
        moteur = mo.moteur_de_vue()
        ext = mo.extension_de_vue()
        if moteur:
            s.lignes += [
                f"Ce vault embarque ses vues par le moteur **`{moteur}`** "
                f"(fichiers `*{ext}`). C'est un format **natif** d'Obsidian "
                f"depuis 1.10 : aucun plugin ne le rend, mais une version plus "
                f"ancienne affichera le fichier comme du texte brut.", ""]
    s.lignes += _figures("obsidian.plugins", profil)
    out.append(s)

    s = Section("obsidian.gabarits", "Pointer Templater sur les gabarits")
    s.lignes += [
        "Réglages → **Templater** → *Template folder location* → `Templates`.",
        "",
        "Sans ce réglage, Templater ne trouve rien et une page neuve naît vide. "
        "Les gabarits de ce dossier sont **générés** depuis le manifeste, un par "
        "rôle : ne pas les éditer à la main, ils se régénèrent — et deux sources "
        "qui décrivent le même gabarit divergent.", ""]
    s.lignes += _figures("obsidian.gabarits", profil)
    out.append(s)

    s = Section("obsidian.cacher", "Masquer ce qui n'est pas une page")
    s.lignes += [
        f"Le vault porte des dossiers qui ne sont pas des pages : "
        f"`{agent}/` (l'espace de l'agent), `Templates/`, `Documentation/`. Les "
        f"voir en permanence coûte de l'attention à chaque recherche.", "",
        "Clic droit sur le dossier dans l'explorateur → **Hide folder**. Les "
        "fichiers restent là, git les suit, l'agent les lit : seule la barre "
        "latérale change.", ""]
    s.lignes += _figures("obsidian.cacher", profil)
    out.append(s)

    s = _couleurs(mo)
    if s is not None:
        out.append(s)
    return out


def _couleurs(mo: Modele | None) -> Section | None:
    s = Section("obsidian.couleurs", "Colorer le graphe par rôle")
    if mo is None:
        s.lignes += [
            "Une couleur par rôle, dans le panneau du graphe → **Groupes**. La "
            "table vit dans le manifeste de l'instance, et l'`INSTALL.md` de "
            "l'instance la donne ligne par ligne.", "",
            "Deux faits qui valent pour tout brain, et qu'on ne retrouve pas en "
            "réessayant :", "",
            "- **l'ordre des requêtes compte.** Une règle qui cible un chemin "
            "doit passer **avant** une règle qui cible un rôle, sinon un hub "
            "spécial prend la couleur des hubs ordinaires.",
            "- **un fichier de vue ne se colore pas.** Il n'a pas de "
            "frontmatter, donc pas de rôle. Ce n'est pas un réglage à trouver, "
            "c'est une limite à connaître.", "",
            "La cible de ces réglages n'est en général **pas versionnée** : la "
            "table du manifeste est la seule source, et elle se réapplique à la "
            "main sur chaque poste. C'est une étape d'installation, pas un "
            "fichier.", ""]
        return s

    g = mo.m.get("graphe") or {}
    ordre = g.get("ordre") or []
    if not ordre:
        return None
    s.lignes += [
        f"Panneau du graphe → **Groupes**. Ajouter les {len(ordre)} requêtes "
        f"**dans cet ordre**, avec leur couleur :", "",
        "| # | Requête | Couleur | RGB |", "|---|---|---|---|"]
    for i, r in enumerate(ordre, start=1):
        s.lignes.append(f"| {i} | `{r.get('requete','')}` | "
                        f"{r.get('couleur','')} | `{r.get('rgb','')}` |")
    s.lignes.append("")
    if g.get("motif_de_l_ordre"):
        s.lignes += [f"**L'ordre compte.** {_l(g['motif_de_l_ordre'])}", ""]
    if g.get("note_base"):
        s.lignes += [f"> {_l(g['note_base'])}", ""]
    s.lignes += [
        f"La cible (`{g.get('cible') or '.obsidian/graph.json'}`) "
        f"{'n’est pas versionnée' if not g.get('versionne') else 'est versionnée'}"
        f" : cette table est la **seule** source de vérité, et elle se "
        f"réapplique à la main sur chaque poste. Elle est aussi dans le vault, "
        f"en `Documentation/graphe.md`.", ""]
    s.lignes += _figures("obsidian.couleurs", _profil(mo))
    return s


# --------------------------------------------------------------------------- #
#  9 — L'agent
# --------------------------------------------------------------------------- #
def _agent(mo: Modele | None) -> Section:
    profil = _profil(mo)
    s = Section("obsidian.agent", "Brancher l'agent")
    if mo is None:
        s.lignes += [
            "Le semis a écrit, à la racine de l'instance, le routeur de l'agent "
            "(`CLAUDE.md` et son contexte de mode) et, sous `.claude/skills/`, "
            "les skills du brain. Il n'y a rien à écrire : tout sort du "
            "manifeste.", "",
            "Trois skills, et le découpage est **structurel**, pas thématique — "
            "un skill qui **écrit** dans le brain, un skill qui **clôt** toute "
            "écriture, un skill qui **consomme** le brain sans y écrire. Tout "
            "brain a besoin des trois ; le troisième peut légitimement ne pas "
            "exister, et son absence est alors écrite plutôt que remplie par un "
            "skill creux.", "",
            "La première section de `CLAUDE.md` est la **règle d'identité git**, "
            "et ce n'est pas un choix de mise en page : c'est le seul fichier "
            "chargé dans **chaque** conversation, au même moment que l'annonce "
            "de l'outil. Une contre-instruction qui arrive après coup arrive "
            "trop tard.", ""]
        if profil == "obsidian":
            s.lignes += [
                "Pour que l'agent lise le vault **vivant** et pas seulement ses "
                "fichiers, brancher le plugin de pont : ses options donnent "
                "l'URL locale, la clé d'API et le bloc de configuration MCP à "
                "coller côté agent.", "",
                "> La clé donne un accès complet en lecture et en écriture au "
                "coffre. Elle se traite comme un mot de passe, et elle ne se "
                "committe **jamais**.", ""]
        s.lignes += _figures("obsidian.agent", profil)
        return s

    skills = mo.m.get("skills") or {}
    s.lignes += [
        "Le routeur est déjà là : `CLAUDE.md` à la racine, et son contexte de "
        "mode à côté. Les deux sont **générés** depuis `brain.yml`.", "",
        "| Rôle | Skill | Écrit dans le brain |", "|---|---|---|"]
    for cle, titre in (("capture", "capture"), ("cloture", "clôture"),
                       ("exploitation", "exploitation")):
        d = skills.get(cle) or {}
        if d.get("nom"):
            s.lignes.append(f"| {titre} | `{d['nom']}` | "
                            f"{'oui' if d.get('ecrit_dans_le_brain') else 'non'} |")
        else:
            s.lignes.append(f"| {titre} | *(non déclaré — l'absence est une "
                            f"réponse, cf. `.claude/skills/README.md`)* | — |")
    s.lignes += ["", "Lancer l'agent **depuis la racine du vault** : c'est là "
                 "que `CLAUDE.md` est chargé, et là que les commandes du kit "
                 "résolvent `./brain.yml`.", ""]
    if profil == "obsidian":
        s.lignes += [
            "Pour que l'agent lise le vault **vivant** — frontmatter résolu, "
            "vues évaluées — et pas seulement les fichiers du dépôt : ouvrir "
            "les options du plugin de pont, y prendre l'URL locale, la clé "
            "d'API et le bloc de configuration MCP, et le coller côté agent.",
            "", "> La clé donne un accès complet en lecture et en écriture au "
            "coffre. Elle se traite comme un mot de passe, et elle ne se "
            "committe **jamais**.", ""]
        s.lignes += _figures("obsidian.agent", profil)
    return s


# --------------------------------------------------------------------------- #
#  10 — Vérifier
# --------------------------------------------------------------------------- #
def _verifier(mo: Modele | None) -> Section:
    profil = _profil(mo)
    mode = _mode(mo)
    agent = "AI" if mo is None else str(
        ((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    prefixe = f"uv run {agent}/scripts/" if mode == "fige" else "brainkit "
    s = Section("verifier", "Vérifier que tout marche")
    cmd_v = (prefixe + "valider.py") if mode == "fige" else "brainkit valider"
    cmd_g = (prefixe + "generer.py") if mode == "fige" else "brainkit generer"
    s.lignes += [
        "Trois commandes, depuis la racine du vault. Ce sont **les mêmes** que "
        "celles de tous les jours : il n'y a pas de mode « vérification "
        "d'installation » à part.", "", "```bash",
        f"{cmd_v}", f"{cmd_g}", "git status --porcelain", "```", "",
        "| Commande | Ce qu'on attend | Ce qu'une sortie autre veut dire |",
        "|---|---|---|",
        "| validation | code **0**, et `aucune violation dure` | une violation "
        "dure sur un vault qu'on vient d'installer n'est pas un défaut du "
        "vault : c'est le mauvais manifeste, ou une régénération qui n'a pas été "
        "faite |",
        "| génération, en `--check` | code **0**, aucun écart | un écart veut "
        "dire qu'un artefact dérivé a été édité à la main, ou qu'il n'a pas été "
        "régénéré après une écriture. Relancer avec `--ecrire` |",
        "| `git status` | **vide** | quelque chose a été écrit sans être "
        "committé — la clôture n'a pas été faite |", ""]
    if mo is None:
        s.lignes += [
            "Sur une instance **fraîchement semée**, les trois répondent : zéro "
            "violation dure, **zéro avertissement**, zéro écart, arbre propre. "
            "Le zéro avertissement est plus fort qu'il n'y paraît : sur un vault "
            "à zéro page d'unité, tout avertissement porterait sur une page que "
            "personne n'a écrite — il signalerait donc un défaut du **kit**.", ""]
    s.lignes += ["Et le jeu d'épreuve du kit, si le dépôt du kit est là :", "",
                 "```bash",
                 "uv run schema/valider.py        # le contrat du manifeste",
                 "uv run tests/epreuve.py         # les règles de validation",
                 "uv run tests/generation.py      # les générateurs",
                 "uv run tests/semis.py           # le semis, re-seuiller, freeze",
                 "uv run tests/skills.py          # les skills, et leur généricité",
                 "uv run tests/mesure.py          # la mesure et ses garde-fous",
                 "uv run tests/entretien.py       # les 49 questions, les 13 refus",
                 "uv run tests/emballage.py       # l'emballage : docs, profils, figeage",
                 "```", ""]
    s.lignes += _figures("verifier", profil)
    return s


# --------------------------------------------------------------------------- #
#  11 — Livrer figé
# --------------------------------------------------------------------------- #
def _freeze(mo: Modele | None) -> Section | None:
    if _mode(mo) == "fige":
        return None
    agent = "AI" if mo is None else str(
        ((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    s = Section("freeze", "Livrer une instance autonome — `freeze`")
    s.lignes += [
        "Une instance normale ne contient **pas de code** : c'est ce qui "
        "garantit qu'une correction du validateur atteint toutes les instances "
        "le même jour. Mais un vault livré là où l'on n'installe rien depuis "
        "internet doit savoir se valider tout seul.", "", "```bash",
        "brainkit freeze --vault <racine du vault>              # simulation",
        "brainkit freeze --vault <racine du vault> --ecrire",
        "```", "",
        f"Ce que `freeze` copie : le paquet du kit sous "
        f"`{agent}/scripts/brainkit/`, trois lanceurs autonomes "
        f"(`valider.py`, `generer.py`, `semer.py`) qui résolvent le manifeste et "
        f"la racine tout seuls, et `{agent}/scripts/FIGE.md`. Il passe "
        f"`kit.mode` à `fige` dans `brain.yml`, **par édition d'une ligne** — "
        f"relire et réécrire le YAML perdrait tous les `motif:`, qui sont la "
        f"moitié de la valeur d'un manifeste.", "",
        "Ce que `freeze` **perd**, et c'est le prix, pas un défaut :", "",
        "| Ce qui reste dehors | Conséquence |", "|---|---|",
        "| les correctifs à venir | **l'instance ne recevra plus rien** |",
        "| le schéma du manifeste | un `brain.yml` modifié ne se vérifie plus "
        "contre le contrat |",
        "| les jeux d'épreuve | aucun moyen de prouver, sur place, que ce kit "
        "figé se comporte comme le kit |",
        "| la comparabilité | deux instances figées à deux dates ne portent pas "
        "le même code |", "",
        "Il n'y a **pas** d'`unfreeze`, et c'est délibéré : un dégel silencieux "
        "ferait cohabiter deux versions du même code sans que personne ne le "
        "sache. `FIGE.md` dit comment rebrancher à la main.", "",
        "> Une instance figée passe **les mêmes validateurs** qu'une instance "
        "branchée, et rend **le même verdict** : `freeze` copie, il ne réécrit "
        "pas.", ""]
    return s


# --------------------------------------------------------------------------- #
#  12 — Dépannage
# --------------------------------------------------------------------------- #
def _depannage(mo: Modele | None) -> Section:
    profil = _profil(mo)
    mode = _mode(mo)
    agent = "AI" if mo is None else str(
        ((mo.m.get("agent") or {}).get("racine") or "AI/")).strip("/")
    s = Section("depannage", "Dépannage")
    cas: list[tuple[str, list[str]]] = [
        ("`brainkit` : commande introuvable",
         ["Le kit n'est pas sur le PATH. Trois issues, de la plus locale à la "
          "plus durable :",
          "1. lancer depuis le dépôt du kit — `uv run brainkit …` ;",
          f"2. exporter `BRAINKIT_RACINE=<racine du dépôt du kit>`, que le "
          f"résolveur `{agent}/scripts/_pont_kit.py` lit en premier ;",
          "3. `uv tool install --editable <racine du kit>` puis "
          "`uv tool update-shell`, et **rouvrir le terminal**."]),
        ("`manifeste introuvable`",
         ["La commande a été lancée hors du vault. Les commandes du kit "
          "résolvent `./brain.yml`, jamais un manifeste voisin : un manifeste "
          "ne se devine pas, c'est ce contre quoi le verdict est rendu. "
          "`cd` dans la racine du vault, ou passer `--manifeste`."]),
        ("`ATTENTION — le vault porte SON manifeste … ce ne sont pas le même brain`",
         ["Un `--manifeste` a été passé, et il n'est pas celui du vault. Le kit "
          "obéit — un ordre est un ordre — mais il le **dit** avant le verdict, "
          "parce que les violations qui suivent n'auront aucun sens. Retirer "
          "`--manifeste`."]),
        ("un refus de version : `le manifeste est plus récent que ce kit`",
         ["Le mineur de `kit.version` ne concorde pas avec le kit installé. Le "
          "kit refuse de tourner sur une version qu'il ne connaît pas, **dans "
          "les deux sens** : un kit ancien ignorerait en silence des "
          "déclarations qu'il ne sait pas lire. Prendre le kit de la génération "
          "de l'instance, ou migrer l'instance."]),
        ("un commit est refusé : l'identité ne concorde pas",
         ["C'est le garde-fou qui fonctionne. Vérifier "
          "`git config --local user.email`, et committer **nu** — sans "
          "`-c user.email`, sans `--author`. Si l'identité locale manque, la "
          "poser ; si elle paraît fausse, **demander** plutôt que de la "
          "deviner. `--no-verify` ne s'utilise pas."]),
        ("les hooks ne se déclenchent jamais",
         ["`git config core.hooksPath` doit répondre `.githooks`. Le semis le "
          "pose ; un **clone** ne le reprend pas — c'est une config locale, "
          "elle ne voyage pas avec le dépôt. Le refaire après chaque clone."]),
        ("la génération en `--check` sort en 2 alors que rien n'a été touché",
         ["Un artefact dérivé a été édité à la main, ou une régénération a été "
          "sautée après une écriture. `generer --ecrire` puis committer. Si "
          "l'écart persiste à l'identique, c'est un défaut du générateur : le "
          "signaler avec la sortie complète."]),
    ]
    if profil == "obsidian":
        cas += [
            ("un fichier de vue s'affiche comme du texte brut",
             ["La version d'Obsidian est trop ancienne pour le format natif des "
              "vues. Mettre à jour, ou passer le brain en profil `nu` et tenir "
              "la table à la main."]),
            ("Templater n'insère rien",
             ["Son *Template folder location* n'est pas renseigné, ou pointe "
              "ailleurs que `Templates`."]),
            ("un dossier reste visible après « Hide folder »",
             ["Le masquage est un réglage **par coffre**, et il faut parfois "
              "recharger l'affichage. Vérifier la liste des chemins dans les "
              "options du plugin."]),
            ("les couleurs du graphe ont disparu",
             ["La cible de ces réglages n'est en général pas versionnée : elles "
              "ne voyagent pas d'un poste à l'autre, ni d'un clone à l'autre. "
              "Réappliquer la table — c'est une étape d'installation, pas un "
              "fichier."]),
        ]
    if mode == "branche":
        cas.append(("`BrainKit introuvable` avec trois pistes imprimées",
                    ["C'est le résolveur du vault qui refuse de deviner. Les "
                     "trois pistes qu'il imprime sont les trois issues, dans "
                     "l'ordre où il les a essayées. En choisir une."]))
    for titre, lignes in cas:
        s.lignes += [f"### {titre}", ""] + lignes + [""]
    return s


# --------------------------------------------------------------------------- #
#  13 — Le manifeste d'images
# --------------------------------------------------------------------------- #
def _images(mo: Modele | None) -> Section:
    s = Section("images", "Le manifeste d'images")
    s.lignes += [f"Les captures se rangent sous `{DOSSIER_IMG}/`.", ""]
    s.lignes += images.table(_profil(mo))
    return s


# --------------------------------------------------------------------------- #
#  Le document
# --------------------------------------------------------------------------- #
def sections(mo: Modele | None) -> list[Section]:
    out: list[Section | None] = [_apercu(mo), _prerequis(mo)]
    out.append(_cloner(mo))
    out.append(_installer_le_kit(mo))
    out.append(_entretien(mo))
    out.append(_semer(mo))
    out.append(_profils(mo))
    out += _obsidian(mo)
    out.append(_agent(mo))
    out.append(_verifier(mo))
    out.append(_freeze(mo))
    out.append(_depannage(mo))
    out.append(_images(mo))
    return [s for s in out if s is not None]


def _ancre(numero: int, titre: str) -> str:
    """L ancre GitHub d un titre `## N. Titre`, telle que GitHub la fabrique."""
    brut = f"{numero}-{titre}".lower()
    garde = [c for c in brut if c.isalnum() or c in " -_"]
    return "".join(garde).replace(" ", "-")


def document(mo: Modele | None) -> str:
    from .. import __version__

    lot = sections(mo)
    nom = (mo.brain.get("nom") if mo is not None else None) or "BrainKit"
    profil = _profil(mo)

    L: list[str] = [f"# Installer — {nom}", ""]
    if mo is None:
        L += [f"> **Document GÉNÉRÉ** par `brainkit.emballer.install`, kit "
              f"`{__version__}`. Ne pas l'éditer à la main : sa source est le "
              f"kit et le manifeste, et deux sources qui décrivent la même "
              f"chose divergent. Le régénérer : `uv run outils/emballer.py "
              f"--ecrire`.", "",
              "Ce guide va de **rien** à un brain vert : installer le kit, "
              "écrire le manifeste par l'entretien, semer l'instance, l'ouvrir, "
              "brancher l'agent, vérifier. Le sujet du brain n'entre nulle part "
              "— c'est le point du kit.", "",
              "> L'instance que tu vas semer porte **son propre** `INSTALL.md`, "
              "généré depuis son manifeste : c'est lui qui nomme son coffre, sa "
              "table de couleurs et ses skills. Celui-ci décrit la route ; "
              "celui-là décrit l'arrivée.", ""]
    else:
        L += [f"> **Document GÉNÉRÉ** depuis `brain.yml` par BrainKit "
              f"`{__version__}`. Ne pas l'éditer à la main : il se régénère, et "
              f"deux sources qui décrivent la même installation divergent.", "",
              f"Installer **{nom}** sur une machine neuve : cloner, activer les "
              f"garde-fous, atteindre l'outillage, ouvrir, vérifier."
              + ("" if profil == "obsidian"
                 else " Ce brain est en profil `nu` : il n'a pas besoin "
                      "d'Obsidian."), ""]

    L += ["---", "", "## Sommaire", ""]
    for i, s in enumerate(lot, start=1):
        L.append(f"{i}. [{s.titre}](#{_ancre(i, s.titre)})")
    L.append("")
    for i, s in enumerate(lot, start=1):
        L += ["---", "", f"## {i}. {s.titre}", ""] + s.lignes
    return "\n".join(L).rstrip("\n") + "\n"
