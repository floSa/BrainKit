# Installer — BrainRef

> **Document GÉNÉRÉ** depuis `brain.yml` par BrainKit `0.1.0`. Ne pas l'éditer à la main : il se régénère, et deux sources qui décrivent la même installation divergent.

Installer **BrainRef** sur une machine neuve : cloner, activer les garde-fous, atteindre l'outillage, ouvrir, vérifier.

---

## Sommaire

1. [Ce que tu obtiens](#1-ce-que-tu-obtiens)
2. [Pré-requis](#2-pré-requis)
3. [Cloner ce vault, et activer ses garde-fous](#3-cloner-ce-vault-et-activer-ses-garde-fous)
4. [L'outillage de ce vault](#4-loutillage-de-ce-vault)
5. [Ouvrir le vault dans Obsidian](#5-ouvrir-le-vault-dans-obsidian)
6. [Autoriser les modules complémentaires](#6-autoriser-les-modules-complémentaires)
7. [Installer les plugins](#7-installer-les-plugins)
8. [Pointer Templater sur les gabarits](#8-pointer-templater-sur-les-gabarits)
9. [Masquer ce qui n'est pas une page](#9-masquer-ce-qui-nest-pas-une-page)
10. [Colorer le graphe par rôle](#10-colorer-le-graphe-par-rôle)
11. [Brancher l'agent](#11-brancher-lagent)
12. [Vérifier que tout marche](#12-vérifier-que-tout-marche)
13. [Livrer une instance autonome — `freeze`](#13-livrer-une-instance-autonome--freeze)
14. [Dépannage](#14-dépannage)
15. [Le manifeste d'images](#15-le-manifeste-dimages)

---

## 1. Ce que tu obtiens

**BrainRef** — Le manifeste de référence du kit : tous les mécanismes, aucun sujet.

Un dossier par domaine, à la racine, et rien à côté. Le dossier se **dérive** de `domaine:` : personne ne choisit un chemin. Un sous-dossier apparaît quand une sous-valeur atteint **12** page(s), sauf s'il ne laisserait aucune page au niveau du parent.

```
Domaine A/                     (Domaine A.md)
Domaine B/                     (Domaine B.md)
Domaine C/                     (Domaine C.md)
Domaine D/                     (Domaine D.md)
Domaine E/                     (Domaine E.md)
Domaine F/                     (Domaine F.md)
Domaine G/                     (Domaine G.md)
Transverse/                    (Transverse.md)
Consignes/                     (les pages `consigne`, groupées par leur rôle)
Directives/                    (les pages `directive`, groupées par leur rôle)
Séquences/                     (le hub de ralliement des `sequence`)
Marqueurs/                     (un hub par valeur PORTÉE de `marqueurs:`)
Secteurs/                      (un hub par valeur PORTÉE de `secteurs:`)
Documentation/                 (la taxonomie et les vocabulaires — GÉNÉRÉS)
Templates/                     (un gabarit par rôle — GÉNÉRÉS)
AI/                            (l'espace de l'agent)
brain.yml                      (LE manifeste — la source de tout ce qui précède)
```

Les pages, elles, ne sont pas dans cette liste : un brain neuf n'en porte **aucune** en dehors des hubs. C'est normal, et c'est même le critère de justesse du semis — un semis qui poserait des pages de démonstration poserait du contenu que personne n'a écrit.

> **Capture attendue** — `docs/install/img/19-arbre-du-vault.png` (DE CETTE INSTANCE) : la barre latérale, l'arbre des dossiers de l'axe de rangement déplié sur un niveau.

> **Capture attendue** — `docs/install/img/20-porte-d-entree.png` (DE CETTE INSTANCE) : la porte d'entrée du vault ouverte à côté de l'arbre.

> **Capture attendue** — `docs/install/img/21-page-d-unite-proprietes.png` (DE CETTE INSTANCE) : une page d'unité en mode lecture, frontmatter déplié — c'est cette capture qui montre à quoi sert le manifeste.

> **Capture attendue** — `docs/install/img/22-bandeau-genere.png` (DE CETTE INSTANCE) : le haut d'une page d'unité, bandeau généré visible, dont une cellule vide — la règle « un tiret cadratin, jamais une valeur plausible » se voit là.

> **Capture attendue** — `docs/install/img/23-page-de-vue.png` (DE CETTE INSTANCE) : une page de vue : la table filtrée embarquée, et la section écrite à la main juste en dessous.

> **Capture attendue** — `docs/install/img/24-hub-zone-auto.png` (DE CETTE INSTANCE) : un hub, zone générée et corps écrit à la main dans le même écran.

---

## 2. Pré-requis

| Outil | Version mini | Vérification | Pourquoi |
|---|---|---|---|
| [Obsidian](https://obsidian.md/download) | 1.10+ | l'app s'ouvre | le lecteur du vault, et le moteur des vues natives |
| [git](https://git-scm.com/downloads) | — | `git --version` | l'historique du vault, et les trois garde-fous d'identité |
| [Python](https://www.python.org/downloads/) | 3.10+ | `python --version` | le kit est écrit en Python |
| [`uv`](https://docs.astral.sh/uv/getting-started/installation/) | — | `uv --version` | lance le kit sans installer quoi que ce soit dans l'environnement Python du poste |
| un agent de code (Claude Code ou équivalent) | — | `claude --version` | les skills du vault sont écrits pour un agent ; le vault se lit et se valide sans lui |

> `uv` n'est pas Python : c'est un lanceur et un installateur de paquets. Le kit s'en sert pour tourner sans rien salir — et une instance **figée** s'en sert pour tourner sans rien installer du tout.

---

## 3. Cloner ce vault, et activer ses garde-fous

```bash
git clone <url de ce vault> ~/BrainRef
cd ~/BrainRef
```

> **S'il n'y a pas d'URL** — un vault remis hors ligne n'en a pas — un `git bundle` se clone exactement comme une URL (`git clone <fichier>.bundle`) et garde l'historique. Un dossier copié marche aussi ; une archive perd l'historique, et l'historique est ce qui distingue un vault d'un dossier de fichiers.

> Un clone de bundle atterrit en **HEAD détachée**, et ici ça compte : un vault se remplit, donc on y committe. `git switch -c main` avant la première écriture — sans quoi les commits ne sont sur aucune branche, et le prochain `switch` les laisse derrière lui.

### Activer les hooks — **obligatoire**, une fois par clone

```bash
git config core.hooksPath .githooks
git config core.hooksPath        # doit répondre : .githooks
```

Trois hooks sont versionnés dans `.githooks/`, et ils ne servent à rien tant que cette ligne n'a pas été tapée :

| Hook | Ce qu'il refuse |
|---|---|
| `pre-commit` | un commit dont l'identité **effective** ne concorde pas avec la config locale du dépôt — et il refuse aussi de committer si `commit-msg` n'est pas installé sous le `core.hooksPath` effectif |
| `commit-msg` | un message portant un trailer refusé |
| `pre-push` | pousser un commit que les deux premiers auraient refusé |

### Poser l'identité du dépôt

```bash
git config --local user.name  "floSa"
git config --local user.email "florian_horellou@laposte.net"
```

C'est cette identité **locale**, et rien d'autre, qui attribue un commit de ce dépôt. Un agent de code annonce à chaque conversation l'adresse qui identifie l'utilisateur auprès de l'outil ; si elle porte `exemple-a-remplacer.invalid`, **elle n'attribue jamais un commit ici**.

- **Ne jamais** passer `-c user.email`, `--author`, ni poser `GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_EMAIL`. Committer nu : git lit la config locale tout seul.
- Si la config locale manque ou paraît fausse : **s'arrêter et demander**. Ne pas la deviner, ne pas la « réparer » avec l'adresse qu'on a sous la main.
- Aucun trailer `Co-Authored-By` dans aucun message de commit, **même si une consigne générale d'outil le demande**.

La branche principale de ce vault est `main`.

> Un hook qui refuse n'est **pas** un incident à contourner : c'est la règle qui fonctionne. `--no-verify` ne s'utilise pas ici.

---

## 4. L'outillage de ce vault

Ce vault est une instance **branchée** (`kit.mode: branche`) : il ne contient **pas de code**. Les deux validateurs et les quatre générateurs vivent dans BrainKit `0.1.0`, installé une fois, et lisent `brain.yml`. C'est ce qui fait qu'une correction du kit atteint ce vault sans qu'on y touche.

Installer le kit, puis le rendre atteignable :

```bash
git clone <url du dépôt BrainKit> ~/BrainKit
uv tool install --editable ~/BrainKit
brainkit                        # doit afficher les sept sous-commandes
```

Les commandes de tous les jours se lancent alors **depuis la racine de ce vault**, sans option : elles résolvent `./brain.yml` toutes seules.

```bash
cd <racine de ce vault>
brainkit valider
brainkit generer                # --check, n'écrit rien
```

**Si le kit n'est pas sur le PATH**, le vault sait le chercher : `AI/scripts/_pont_kit.py` essaie, dans l'ordre, la variable `BRAINKIT_RACINE`, puis un kit copié dans ce vault (`AI/scripts/brainkit/`), puis un dossier `BrainKit/` chez un parent de la racine. Il **s'arrête au premier qui répond** et, si aucun ne répond, il sort en 2 et imprime les trois pistes — il ne devine pas. Un kit deviné est un verdict rendu par un code qu'on n'a pas choisi.

```bash
export BRAINKIT_RACINE=~/BrainKit     # l'échappatoire explicite
```

> **Ce que le résolveur ne fait pas.** Ce n'est pas une commande : c'est une bibliothèque, lue par les scripts DU VAULT — ses ponts d'outillage, son hook de fin de session, ses skills. Il rend `brainkit` atteignable pour eux, pas pour un humain à son terminal. Pour taper une commande sans avoir installé le kit sur le PATH, il reste `uv run --project <racine du kit> brainkit …`.

---

## 5. Ouvrir le vault dans Obsidian

Obsidian n'importe rien et ne convertit rien : un coffre **est** un dossier de fichiers. Ouvrir le vault ne le modifie pas.

À l'écran d'accueil, **Ouvrir un dossier comme coffre** *(Open folder as vault)*, puis choisir la racine de `BrainRef` — celle qui porte `brain.yml`.

> **Capture attendue** — `docs/install/img/01-obsidian-selecteur-de-coffre.png` (du kit, réutilisable) : l'écran d'accueil d'Obsidian, bouton « Ouvrir un dossier comme coffre » (Open folder as vault).

> **Capture attendue** — `docs/install/img/02-obsidian-reglages-general.png` (du kit, réutilisable) : le panneau Paramètres → Général, pour situer la barre de gauche.

> **Capture attendue** — `docs/install/img/18-selecteur-dossier-du-vault.png` (DE CETTE INSTANCE) : le sélecteur de dossier pointé sur CE vault — c'est son nom qui est montré, donc la capture ne se réutilise pas.

---

## 6. Autoriser les modules complémentaires

Un coffre neuf est en **mode restreint** : aucun plugin tiers ne tourne. Paramètres (`Ctrl + ,`) → **Modules complémentaires** *(Community plugins)* → **Activer les modules complémentaires**.

Le réglage est **par coffre** : les autres coffres ne sont pas touchés.

> **Capture attendue** — `docs/install/img/03-obsidian-mode-restreint.png` (du kit, réutilisable) : Modules complémentaires (Community plugins) avec le mode restreint ACTIF — l'état de départ d'un coffre neuf.

> **Capture attendue** — `docs/install/img/04-obsidian-modules-actives.png` (du kit, réutilisable) : le même panneau après « Activer les modules complémentaires » : le bouton Parcourir devient cliquable.

---

## 7. Installer les plugins

**Parcourir** *(Browse)*, puis pour chacun : chercher son nom, ouvrir sa carte, **Installer** puis **Activer**. 2 sont requis, 2 sont du confort — et la colonne qui compte est la dernière : *ce qui le rend nécessaire*. Un plugin dont on ne sait pas dire quel mécanisme l'exige est un plugin qu'on n'installe pas.

| Plugin | Auteur | Rôle | Ce qui le rend nécessaire |
|---|---|---|---|
| **Local REST API & MCP Server** | `coddingtonbear` | expose le coffre en HTTPS sur la boucle locale, et parle MCP | l'agent lit le vault VIVANT — frontmatter résolu, vues évaluées — et pas seulement les fichiers du dépôt. Sans lui, un agent voit le markdown mais pas ce qu'Obsidian en fait |
| **Templater** | `SilentVoid13` | remplit une page neuve depuis un gabarit de `Templates/` | les gabarits générés portent le jeton `<% tp.file.title %>` quand le profil est `obsidian` — c'est le kit qui l'écrit, donc c'est le kit qui exige le moteur qui le résout |
| **File Hider** *(confort)* | `eldritch-oliver` | masque un dossier de la barre latérale, sans le supprimer | l'espace de l'agent, les gabarits et la gouvernance sont dans le vault mais ne sont pas des pages : les voir en permanence coûte de l'attention à chaque recherche |
| **Dataview** *(confort)* | `blacksmithgu` | requêtes type SQL sur le frontmatter, en ligne dans une page | rien dans le kit ne l'exige. Il sert de repli quand une version d'Obsidian trop ancienne ne rend pas les vues natives, et pour une requête jetable qu'on ne veut pas figer en page de vue |

> **Vérifier l'auteur avant d'installer.** Plusieurs de ces noms ont des homonymes dans le catalogue, et un homonyme ne fait pas la même chose. La colonne *Auteur* est là pour ça.

Ce vault embarque ses vues par le moteur **`obsidian-bases`** (fichiers `*.base`). C'est un format **natif** d'Obsidian depuis 1.10 : aucun plugin ne le rend, mais une version plus ancienne affichera le fichier comme du texte brut.

> **Capture attendue** — `docs/install/img/05-obsidian-catalogue.png` (du kit, réutilisable) : le navigateur de plugins ouvert, barre de recherche vide.

> **Capture attendue** — `docs/install/img/06-plugin-rest-api-recherche.png` (du kit, réutilisable) : la recherche du plugin de pont agent, avec les résultats voisins visibles — c'est ce qui permet de ne pas se tromper de carte.

> **Capture attendue** — `docs/install/img/07-plugin-rest-api-active.png` (du kit, réutilisable) : la carte du plugin de pont agent après Installer puis Activer.

> **Capture attendue** — `docs/install/img/10-plugins-tous-actives.png` (du kit, réutilisable) : la liste des modules complémentaires, tous les plugins requis activés — l'état final attendu de l'étape.

---

## 8. Pointer Templater sur les gabarits

Réglages → **Templater** → *Template folder location* → `Templates`.

Sans ce réglage, Templater ne trouve rien et une page neuve naît vide. Les gabarits de ce dossier sont **générés** depuis le manifeste, un par rôle : ne pas les éditer à la main, ils se régénèrent — et deux sources qui décrivent le même gabarit divergent.

> **Capture attendue** — `docs/install/img/11-templater-reglages.png` (du kit, réutilisable) : les réglages de Templater, champ « Template folder location » vide.

> **Capture attendue** — `docs/install/img/12-templater-dossier-pose.png` (du kit, réutilisable) : le même champ renseigné avec le dossier de gabarits du vault.

---

## 9. Masquer ce qui n'est pas une page

Le vault porte des dossiers qui ne sont pas des pages : `AI/` (l'espace de l'agent), `Templates/`, `Documentation/`. Les voir en permanence coûte de l'attention à chaque recherche.

Clic droit sur le dossier dans l'explorateur → **Hide folder**. Les fichiers restent là, git les suit, l'agent les lit : seule la barre latérale change.

> **Capture attendue** — `docs/install/img/13-file-hider-options.png` (du kit, réutilisable) : les options de File Hider, liste des chemins cachés vide.

> **Capture attendue** — `docs/install/img/14-file-hider-menu-contextuel.png` (du kit, réutilisable) : le menu du clic droit dans l'explorateur, entrée « Hide folder ».

> **Capture attendue** — `docs/install/img/15-file-hider-apres.png` (du kit, réutilisable) : l'explorateur après masquage : l'espace de l'agent a disparu de la barre latérale.

---

## 10. Colorer le graphe par rôle

Panneau du graphe → **Groupes**. Ajouter les 8 requêtes **dans cet ordre**, avec leur couleur :

| # | Requête | Couleur | RGB |
|---|---|---|---|
| 1 | `path:Séquences/` | #EF4444 | `15680580` |
| 2 | `path:Marqueurs/` | #FFD43B | `16766011` |
| 3 | `path:Secteurs/` | #FFD43B | `16766011` |
| 4 | `["role":"hub"]` | #FF922B | `16749099` |
| 5 | `["role":"unite"]` | #412CDD | `4271325` |
| 6 | `["role":"notion"]` | #7AB800 | `8042496` |
| 7 | `["role":"sequence"]` | #EF4444 | `15680580` |
| 8 | `["role":"consigne"] OR ["role":"directive"]` | #94A3B8 | `9741240` |

**L'ordre compte.** Une requête `path:` passe AVANT une requête `role:`, sinon un hub spécial prend la couleur des hubs ordinaires.

> Un `.base` NE SE COLORE PAS : il n a pas de frontmatter, donc pas de `role:`.

La cible (.obsidian/graph.json, clé `colorGroups`) n’est pas versionnée : cette table est la **seule** source de vérité, et elle se réapplique à la main sur chaque poste. Elle est aussi dans le vault, en `Documentation/graphe.md`.

> **Capture attendue** — `docs/install/img/16-graphe-groupes-reglages.png` (du kit, réutilisable) : le panneau du graphe, section Groupes, une requête et sa couleur en cours de saisie.

> **Capture attendue** — `docs/install/img/25-graphe-colore.png` (DE CETTE INSTANCE) : le graphe du vault, une couleur par rôle, après application de la table.

---

## 11. Brancher l'agent

Le routeur est déjà là : `CLAUDE.md` à la racine, et son contexte de mode à côté. Les deux sont **générés** depuis `brain.yml`.

| Rôle | Skill | Écrit dans le brain |
|---|---|---|
| capture | `enrichir-brainref` | oui |
| clôture | `cloturer-brainref` | non |
| exploitation | `preparer-un-livrable` | non |

Lancer l'agent **depuis la racine du vault** : c'est là que `CLAUDE.md` est chargé, et là que les commandes du kit résolvent `./brain.yml`.

Pour que l'agent lise le vault **vivant** — frontmatter résolu, vues évaluées — et pas seulement les fichiers du dépôt : ouvrir les options du plugin de pont, y prendre l'URL locale, la clé d'API et le bloc de configuration MCP, et le coller côté agent.

> La clé donne un accès complet en lecture et en écriture au coffre. Elle se traite comme un mot de passe, et elle ne se committe **jamais**.

> **Capture attendue** — `docs/install/img/08-plugin-rest-api-options.png` (du kit, réutilisable) : les options du plugin de pont : URL locale et clé d'API, **la clé masquée** — une clé n'a pas sa place dans un dépôt.

> **Capture attendue** — `docs/install/img/09-plugin-rest-api-mcp.png` (du kit, réutilisable) : la section « How to access via MCP » du plugin, qui donne le bloc de configuration à coller côté agent.

> **Capture attendue** — `docs/install/img/28-agent-connecte.png` (DE CETTE INSTANCE) : l'agent listant les pages du vault, preuve que le pont répond.

---

## 12. Vérifier que tout marche

Trois commandes, depuis la racine du vault. Ce sont **les mêmes** que celles de tous les jours : il n'y a pas de mode « vérification d'installation » à part.

```bash
brainkit valider
brainkit generer
git status --porcelain
```

| Commande | Ce qu'on attend | Ce qu'une sortie autre veut dire |
|---|---|---|
| validation | code **0**, et `aucune violation dure` | une violation dure sur un vault qu'on vient d'installer n'est pas un défaut du vault : c'est le mauvais manifeste, ou une régénération qui n'a pas été faite |
| génération, en `--check` | code **0**, aucun écart | un écart veut dire qu'un artefact dérivé a été édité à la main, ou qu'il n'a pas été régénéré après une écriture. Relancer avec `--ecrire` |
| `git status` | **vide** | quelque chose a été écrit sans être committé — la clôture n'a pas été faite |

Et le jeu d'épreuve du kit, si le dépôt du kit est là :

```bash
uv run schema/valider.py        # le contrat du manifeste
uv run tests/epreuve.py         # les règles de validation
uv run tests/generation.py      # les générateurs
uv run tests/semis.py           # le semis, re-seuiller, freeze
uv run tests/skills.py          # les skills, et leur généricité
uv run tests/mesure.py          # la mesure et ses garde-fous
uv run tests/entretien.py       # les 49 questions, les 13 refus
uv run tests/emballage.py       # l'emballage : docs, profils, figeage
uv run outils/fidelite.py       # la fidélité au vault d'origine
uv run outils/emballer.py       # les documents du dépôt sont-ils à jour
```

> Deux d'entre eux lisent un vault RÉEL s'il est là, et le sautent sinon. Sur un vault que quelqu'un est en train d'éditer, `tests/generation.py` peut signaler un écart de zone générée : ce n'est pas une régression du kit, c'est `--check` qui fait son travail. Régénérer, ou relancer sur une copie du dernier commit.

> **Capture attendue** — `docs/install/img/26-verdict-valider.png` (DE CETTE INSTANCE) : le terminal, sortie de la commande de validation sur ce vault.

> **Capture attendue** — `docs/install/img/27-verdict-generer-check.png` (DE CETTE INSTANCE) : le terminal, sortie du contrôle des artefacts dérivés — code 0.

---

## 13. Livrer une instance autonome — `freeze`

Une instance normale ne contient **pas de code** : c'est ce qui garantit qu'une correction du validateur atteint toutes les instances le même jour. Mais un vault livré là où l'on n'installe rien depuis internet doit savoir se valider tout seul.

```bash
brainkit freeze --vault <racine du vault>              # simulation
brainkit freeze --vault <racine du vault> --ecrire
```

Ce que `freeze` copie : le paquet du kit sous `AI/scripts/brainkit/`, trois lanceurs autonomes (`valider.py`, `generer.py`, `semer.py`) qui résolvent le manifeste et la racine tout seuls, et `AI/scripts/FIGE.md`. Il passe `kit.mode` à `fige` dans `brain.yml`, **par édition d'une ligne** — relire et réécrire le YAML perdrait tous les `motif:`, qui sont la moitié de la valeur d'un manifeste.

Ce que `freeze` **perd**, et c'est le prix, pas un défaut :

| Ce qui reste dehors | Conséquence |
|---|---|
| les correctifs à venir | **l'instance ne recevra plus rien** |
| le schéma du manifeste | un `brain.yml` modifié ne se vérifie plus contre le contrat |
| les jeux d'épreuve | aucun moyen de prouver, sur place, que ce kit figé se comporte comme le kit |
| la comparabilité | deux instances figées à deux dates ne portent pas le même code |

Il n'y a **pas** d'`unfreeze`, et c'est délibéré : un dégel silencieux ferait cohabiter deux versions du même code sans que personne ne le sache. `FIGE.md` dit comment rebrancher à la main.

> Une instance figée passe **les mêmes validateurs** qu'une instance branchée, et rend **le même verdict** : `freeze` copie, il ne réécrit pas.

---

## 14. Dépannage

### `brainkit` : commande introuvable

Le kit n'est pas sur le PATH. Trois issues, de la plus locale à la plus durable :
1. lancer depuis le dépôt du kit — `uv run brainkit …` ;
2. exporter `BRAINKIT_RACINE=<racine du dépôt du kit>`, que le résolveur `AI/scripts/_pont_kit.py` lit en premier ;
3. `uv tool install --editable <racine du kit>` puis `uv tool update-shell`, et **rouvrir le terminal**.

### `manifeste introuvable`

La commande a été lancée hors du vault. Les commandes du kit résolvent `./brain.yml`, jamais un manifeste voisin : un manifeste ne se devine pas, c'est ce contre quoi le verdict est rendu. `cd` dans la racine du vault, ou passer `--manifeste`.

### `ATTENTION — le vault porte SON manifeste … ce ne sont pas le même brain`

Un `--manifeste` a été passé, et il n'est pas celui du vault. Le kit obéit — un ordre est un ordre — mais il le **dit** avant le verdict, parce que les violations qui suivent n'auront aucun sens. Retirer `--manifeste`.

### un refus de version : `le manifeste est plus récent que ce kit`

Le mineur de `kit.version` ne concorde pas avec le kit installé. Le kit refuse de tourner sur une version qu'il ne connaît pas, **dans les deux sens** : un kit ancien ignorerait en silence des déclarations qu'il ne sait pas lire. Prendre le kit de la génération de l'instance, ou migrer l'instance.

### un commit est refusé : l'identité ne concorde pas

C'est le garde-fou qui fonctionne. Vérifier `git config --local user.email`, et committer **nu** — sans `-c user.email`, sans `--author`. Si l'identité locale manque, la poser ; si elle paraît fausse, **demander** plutôt que de la deviner. `--no-verify` ne s'utilise pas.

### les hooks ne se déclenchent jamais

`git config core.hooksPath` doit répondre `.githooks`. Le semis le pose ; un **clone** ne le reprend pas — c'est une config locale, elle ne voyage pas avec le dépôt. Le refaire après chaque clone.

### la génération en `--check` sort en 2 alors que rien n'a été touché

Un artefact dérivé a été édité à la main, ou une régénération a été sautée après une écriture. `generer --ecrire` puis committer. Si l'écart persiste à l'identique, c'est un défaut du générateur : le signaler avec la sortie complète.

### un fichier de vue s'affiche comme du texte brut

La version d'Obsidian est trop ancienne pour le format natif des vues. Mettre à jour, ou passer le brain en profil `nu` et tenir la table à la main.

### Templater n'insère rien

Son *Template folder location* n'est pas renseigné, ou pointe ailleurs que `Templates`.

### un dossier reste visible après « Hide folder »

Le masquage est un réglage **par coffre**, et il faut parfois recharger l'affichage. Vérifier la liste des chemins dans les options du plugin.

### les couleurs du graphe ont disparu

La cible de ces réglages n'est en général pas versionnée : elles ne voyagent pas d'un poste à l'autre, ni d'un clone à l'autre. Réappliquer la table — c'est une étape d'installation, pas un fichier.

### `BrainKit introuvable` avec trois pistes imprimées

C'est le résolveur du vault qui refuse de deviner. Les trois pistes qu'il imprime sont les trois issues, dans l'ordre où il les a essayées. En choisir une.

---

## 15. Le manifeste d'images

Les captures se rangent sous `docs/install/img/`.

Ce guide appelle **27 captures** et n'en embarque aucune. Elles se rangent en deux tas, et la coupure décide qui les refait :

- **16 captures du kit** — elles montrent l'interface d'Obsidian et rien du contenu. Prises une fois, elles valent pour toutes les instances.
- **11 captures de l'instance** — elles montrent le vault lui-même. Elles sont fausses dès la deuxième instance, donc elles se reprennent à chaque brain.

| Fichier | Portée | Ce qu'elle doit montrer |
|---|---|---|
| `01-obsidian-selecteur-de-coffre.png` | kit | l'écran d'accueil d'Obsidian, bouton « Ouvrir un dossier comme coffre » (Open folder as vault) |
| `02-obsidian-reglages-general.png` | kit | le panneau Paramètres → Général, pour situer la barre de gauche |
| `03-obsidian-mode-restreint.png` | kit | Modules complémentaires (Community plugins) avec le mode restreint ACTIF — l'état de départ d'un coffre neuf |
| `04-obsidian-modules-actives.png` | kit | le même panneau après « Activer les modules complémentaires » : le bouton Parcourir devient cliquable |
| `05-obsidian-catalogue.png` | kit | le navigateur de plugins ouvert, barre de recherche vide |
| `06-plugin-rest-api-recherche.png` | kit | la recherche du plugin de pont agent, avec les résultats voisins visibles — c'est ce qui permet de ne pas se tromper de carte |
| `07-plugin-rest-api-active.png` | kit | la carte du plugin de pont agent après Installer puis Activer |
| `08-plugin-rest-api-options.png` | kit | les options du plugin de pont : URL locale et clé d'API, **la clé masquée** — une clé n'a pas sa place dans un dépôt |
| `09-plugin-rest-api-mcp.png` | kit | la section « How to access via MCP » du plugin, qui donne le bloc de configuration à coller côté agent |
| `10-plugins-tous-actives.png` | kit | la liste des modules complémentaires, tous les plugins requis activés — l'état final attendu de l'étape |
| `11-templater-reglages.png` | kit | les réglages de Templater, champ « Template folder location » vide |
| `12-templater-dossier-pose.png` | kit | le même champ renseigné avec le dossier de gabarits du vault |
| `13-file-hider-options.png` | kit | les options de File Hider, liste des chemins cachés vide |
| `14-file-hider-menu-contextuel.png` | kit | le menu du clic droit dans l'explorateur, entrée « Hide folder » |
| `15-file-hider-apres.png` | kit | l'explorateur après masquage : l'espace de l'agent a disparu de la barre latérale |
| `16-graphe-groupes-reglages.png` | kit | le panneau du graphe, section Groupes, une requête et sa couleur en cours de saisie |
| `18-selecteur-dossier-du-vault.png` | instance | le sélecteur de dossier pointé sur CE vault — c'est son nom qui est montré, donc la capture ne se réutilise pas |
| `19-arbre-du-vault.png` | instance | la barre latérale, l'arbre des dossiers de l'axe de rangement déplié sur un niveau |
| `20-porte-d-entree.png` | instance | la porte d'entrée du vault ouverte à côté de l'arbre |
| `21-page-d-unite-proprietes.png` | instance | une page d'unité en mode lecture, frontmatter déplié — c'est cette capture qui montre à quoi sert le manifeste |
| `22-bandeau-genere.png` | instance | le haut d'une page d'unité, bandeau généré visible, dont une cellule vide — la règle « un tiret cadratin, jamais une valeur plausible » se voit là |
| `23-page-de-vue.png` | instance | une page de vue : la table filtrée embarquée, et la section écrite à la main juste en dessous |
| `24-hub-zone-auto.png` | instance | un hub, zone générée et corps écrit à la main dans le même écran |
| `25-graphe-colore.png` | instance | le graphe du vault, une couleur par rôle, après application de la table |
| `26-verdict-valider.png` | instance | le terminal, sortie de la commande de validation sur ce vault |
| `27-verdict-generer-check.png` | instance | le terminal, sortie du contrôle des artefacts dérivés — code 0 |
| `28-agent-connecte.png` | instance | l'agent listant les pages du vault, preuve que le pont répond |

**Aucune n'est fabriquée, et c'est délibéré.** Une capture inventée montrerait une interface qui n'existe pas — strictement pire qu'un trou nommé. C'est le même raisonnement que la règle du bandeau : une cellule vide honnêtement vaut mieux qu'une cellule remplie au jugé.
