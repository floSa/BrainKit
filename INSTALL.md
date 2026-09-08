# Installer — BrainKit

> **Document GÉNÉRÉ** par `brainkit.emballer.install`, kit `0.1.0`. Ne pas l'éditer à la main : sa source est le kit et le manifeste, et deux sources qui décrivent la même chose divergent. Le régénérer : `uv run outils/emballer.py --ecrire`.

Ce guide va de **rien** à un brain vert : installer le kit, écrire le manifeste par l'entretien, semer l'instance, l'ouvrir, brancher l'agent, vérifier. Le sujet du brain n'entre nulle part — c'est le point du kit.

> L'instance que tu vas semer porte **son propre** `INSTALL.md`, généré depuis son manifeste : c'est lui qui nomme son coffre, sa table de couleurs et ses skills. Celui-ci décrit la route ; celui-là décrit l'arrivée.

---

## Sommaire

1. [Ce que tu obtiens](#1-ce-que-tu-obtiens)
2. [Pré-requis](#2-pré-requis)
3. [Installer le kit — et le rendre atteignable](#3-installer-le-kit--et-le-rendre-atteignable)
4. [Écrire le manifeste : l'entretien](#4-écrire-le-manifeste--lentretien)
5. [Semer l'instance](#5-semer-linstance)
6. [Les deux profils — un brain peut vivre sans Obsidian](#6-les-deux-profils--un-brain-peut-vivre-sans-obsidian)
7. [Ouvrir le vault dans Obsidian](#7-ouvrir-le-vault-dans-obsidian)
8. [Autoriser les modules complémentaires](#8-autoriser-les-modules-complémentaires)
9. [Installer les plugins](#9-installer-les-plugins)
10. [Pointer Templater sur les gabarits](#10-pointer-templater-sur-les-gabarits)
11. [Masquer ce qui n'est pas une page](#11-masquer-ce-qui-nest-pas-une-page)
12. [Colorer le graphe par rôle](#12-colorer-le-graphe-par-rôle)
13. [Brancher l'agent](#13-brancher-lagent)
14. [Vérifier que tout marche](#14-vérifier-que-tout-marche)
15. [Livrer une instance autonome — `freeze`](#15-livrer-une-instance-autonome--freeze)
16. [Dépannage](#16-dépannage)
17. [Le manifeste d'images](#17-le-manifeste-dimages)

---

## 1. Ce que tu obtiens

Un **second brain** : un dossier de fichiers markdown, ouvrable dans Obsidian, versionné dans git, et surtout **contrôlable** — deux validateurs disent à tout moment si le vault est cohérent, et quatre générateurs réécrivent ce qui se dérive.

La forme ne dépend pas du sujet, et c'est tout l'objet du kit :

- **un dossier par valeur de l'axe de rangement**, à la racine, et rien à côté. Personne ne choisit un chemin : il se **dérive** du champ de rangement de la page ;
- **un sous-dossier quand une sous-valeur grossit**, jamais avant. Le seuil est déclaré, et le changer est une migration outillée (`brainkit re-seuiller`), pas une décision de rangement ;
- **une page par dossier**, dite hub, dont une zone est générée depuis le contenu du dossier ;
- **un champ qui dit ce qu'une page est** — une unité, une notion, une vue, une prescription. C'est lui, et pas le chemin, qui décide du gabarit que le validateur applique ;
- **un manifeste**, `brain.yml`, à la racine. Il porte les mots du sujet, ses axes, ses gabarits, ses règles et leur sévérité. Le kit ne sait rien d'autre du brain que ce fichier.

Le sujet, lui, est libre : le kit a été extrait d'un brain de développement logiciel, éprouvé sur un brain d'histoire et sur un brain de montagne. Aucun de ses mécanismes ne nomme un sujet.

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

## 3. Installer le kit — et le rendre atteignable

Le kit est un **paquet Python**, pas un dépôt-gabarit qu'on clone puis qu'on vide. La distinction commande tout le reste : une instance ne contient **pas de code**, donc une correction du validateur atteint toutes les instances le jour où elle est faite. Un gabarit cloné, lui, fourche le jour du clone.

```bash
git clone <url du dépôt BrainKit> ~/BrainKit
cd ~/BrainKit
```

> **Et s'il n'y a pas d'URL ?** C'est le cas normal, pas une exception : ce dépôt peut n'avoir aucun remote, et une livraison hors ligne n'en a jamais. Le kit arrive alors sous une autre forme, et les trois se valent :

> - **un dossier copié** — `cp -r`, une clé, un partage réseau. L'historique git vient avec s'il est dans le dossier ;
> - **un `git bundle`** — un fichier unique qui se clone comme une URL : `git clone brainkit.bundle ~/BrainKit`. C'est la forme à préférer, parce qu'elle garde l'historique **et** se vérifie ;
> - **une archive** — `.zip`, `.tar.gz`. L'historique est perdu, donc `git log` ne dira plus de quelle version le kit vient : la seule trace restante est `__version__` dans `brainkit/__init__.py`.

> Dans les trois cas, la suite de ce guide est identique — rien ci-dessous ne suppose un remote.

Deux façons de le lancer, et il faut choisir **maintenant** — c'est le pas qu'on oublie, et un outillage qu'on ne sait pas lancer est un outillage qui ne tourne pas :

**a. depuis le dépôt du kit** — rien à installer, `uv` s'occupe des dépendances :

```bash
uv run brainkit                 # doit afficher les sept sous-commandes
```

**b. sur le PATH** — la commande devient disponible partout, y compris depuis le dossier d'une instance :

```bash
uv tool install --editable ~/BrainKit
brainkit                        # doit afficher les sept sous-commandes
```

Si `brainkit` n'est pas trouvé juste après, c'est que le dossier des outils `uv` n'est pas sur le PATH. `uv tool update-shell` l'y ajoute, puis il faut **rouvrir le terminal**.

> **Pourquoi ce pas mérite une section.** Une instance sait qu'elle est branchée sur un kit, elle ne sait pas **où** ce kit vit. C'est un trou mesuré, et il a deux bouchons : mettre `brainkit` sur le PATH (ici), ou laisser l'instance le chercher elle-même — le semis pose pour cela un résolveur dans l'espace de l'agent, qui essaie la variable `BRAINKIT_RACINE`, puis le kit copié dans l'instance, puis un `BrainKit/` voisin. Les deux bouchons sont bons, aucun n'est facultatif : sans l'un ou l'autre, les commandes de ce guide ne tournent pas depuis le vault.

---

## 4. Écrire le manifeste : l'entretien

Un brain neuf commence par **son manifeste**, et le manifeste s'obtient par un **entretien** — onze passes, quarante-neuf questions, menées en conversation avec l'agent :

```bash
brainkit entretien --questions      # les 49 questions, et ce que chacune produit
brainkit entretien --refus          # les 13 choses qu'il REFUSE de deviner
```

L'entretien n'est pas un formulaire, et ce n'est pas une coquetterie : il **induit** l'axe de rangement à partir de vingt titres réels que l'on cite, au lieu de demander « quels sont tes domaines ? ». Une liste de domaines donnée à froid décrit ce qu'on croit ranger ; vingt titres décrivent ce qu'on a vraiment.

Il **refuse de deviner** treize choses — l'identité git en premier, parce qu'une identité devinée entre dans l'historique du dépôt et n'en sort plus. Un refus nomme le champ et rend la question ; il ne pose pas une valeur plausible.

**Qui pose les questions.** L'entretien est une conversation, et c'est un **skill** qui la mène : `skills/entretien/SKILL.md`, dans ce dépôt. On le charge dans l'agent, depuis le dépôt du kit, et on répond. La commande ci-dessous est ce que le skill appelle — elle tient le brouillon, applique les refus, compose, puis sème. On peut aussi s'en servir à la main, et c'est ce que la suite décrit.

L'entretien écrit un **brouillon** au fil des passes, puis compose le manifeste. Six commandes, dans cet ordre :

```bash
# 1. où on en est — c'est le mode par défaut, il ne touche rien
brainkit entretien --brouillon mon-brain.entretien.yml

# 2. répondre, une question à la fois. La valeur est lue en YAML :
#    une chaîne, une liste, un dictionnaire — selon ce que la question attend.
brainkit entretien --brouillon mon-brain.entretien.yml \
    --repondre '0.2=MonBrain' --repondre '0.3=perso'

# 3. ou par lot : un fichier YAML `reponses: {<id>: <valeur>}`
brainkit entretien --brouillon mon-brain.entretien.yml --reponses lot.yml

# 4. relire ce qui a déjà été dit, avant de reprendre
brainkit entretien --brouillon mon-brain.entretien.yml --rappel

# 5. passer les treize refus sur l'état courant
brainkit entretien --brouillon mon-brain.entretien.yml --verifier

# 6. composer le manifeste — REFUSÉ s'il reste un grief
brainkit entretien --brouillon mon-brain.entretien.yml --composer mon-brain.brain.yml
```

Puis semer, soit avec la commande de la section suivante, soit directement depuis le brouillon :

```bash
brainkit entretien --brouillon mon-brain.entretien.yml --semer ~/MonBrain
brainkit entretien --brouillon mon-brain.entretien.yml --semer ~/MonBrain --ecrire
```

Une question rouverte se rejoue : `--oublier 2.2` efface la réponse et la repose. C'est la bonne façon de changer d'avis — écraser une réponse par une autre laisserait le brouillon en dire deux choses.

> **À quoi ressemble un fichier de réponses.** Deux exemples complets sont dans `tests/` : `cimebrain.reponses.yml` (un brain de montagne) et `blanc.reponses.yml` (un brain de droit du travail — c'est l'entretien de l'installation à blanc qui a validé ce guide). Chacun porte, en tête, le raisonnement du sujet ; c'est la forme à copier, pas le contenu.

> **La porte de service, et ce qu'elle coûte.** `--reponses <fichier>` accepte un lot entier de réponses d'un coup, sans conversation. C'est ce qui rend le jeu d'épreuve possible — rejouer un entretien complet est la seule façon de **prouver** qu'un entretien produit un vault vert — et c'est un usage légitime pour qui sait déjà ce qu'il veut. Mais il faut savoir ce qu'on saute : les treize refus tournent toujours sur le brouillon et sur le manifeste composé, **pas** sur la conversation. Ce qu'on perd, c'est le moment où une question ouverte fait changer d'avis — et c'est là qu'est la valeur de l'entretien. Employer `--reponses` pour rejouer, pas pour se dispenser de réfléchir.

---

## 5. Semer l'instance

Le semis crée le vault : ses dossiers, un hub par dossier, un gabarit par rôle, la taxonomie et les vocabulaires générés, le routeur de l'agent, les trois skills, les trois hooks git, le dépôt et son premier commit.

```bash
brainkit semer --manifeste mon-brain.brain.yml --dans ~/MonBrain
brainkit semer --manifeste mon-brain.brain.yml --dans ~/MonBrain --ecrire
```

**Le mode par défaut n'écrit pas un octet.** Le lancer pour voir ce qu'il ferait est le premier usage de la commande, et il ne doit rien coûter. `--ecrire` se demande.

Le semis **refuse** quatre situations, et aucune n'est négociable :

| Refus | Ce qu'il évite |
|---|---|
| la cible existe et n'est pas vide | écraser un vault qu'on croyait absent |
| la cible vit sous le dépôt du kit | versionner une instance dans le kit |
| la cible vit sous un dépôt git | semer dans un dépôt qui n'est pas le sien |
| la cible vit sous un vault | semer un brain à l'intérieur d'un autre |

Il refuse aussi un **manifeste incomplet**, et il rend tous les manques d'un coup, **avant** d'avoir écrit quoi que ce soit : un vault à demi semé fait dire n'importe quoi à ses validateurs, et le premier geste de l'utilisateur serait de réparer une structure que personne n'a cassée.

Ce que le semis ne fait **pas** : écrire des pages. Un brain neuf porte un hub par dossier et **rien d'autre**. Ce que l'entretien a récolté — les vingt titres de la passe d'induction — est posé dans la page de capture, en cases à cocher : du travail identifié, pas du contenu de démonstration.

---

## 6. Les deux profils — un brain peut vivre sans Obsidian

Le manifeste déclare `brain.profil`, et il n'a que deux valeurs :

| Profil | Ce que le vault porte | Pour qui |
|---|---|---|
| `obsidian` | tout : les vues natives embarquées, les couleurs du graphe, le jeton de gabarit résolu par Templater | un brain qu'on lit et qu'on explore |
| `nu` | markdown, frontmatter, validateurs, générateurs, skills, hooks, **et le bandeau** | un brain lu par un agent, un dépôt de documentation, un poste où l'on n'installera rien |

Ce que `nu` **perd**, nommément :

- **les vues vivantes.** Un rôle de fonction `vue` embarque, en profil `obsidian`, un fichier de requête que le lecteur évalue. En `nu` il n'y a pas de moteur pour l'évaluer : la page de vue reste une page, sa section écrite à la main reste la partie qui a de la valeur, et la table se tient à la main si on la veut.
- **les couleurs du graphe**, donc le graphe comme outil de lecture. La table reste dans le manifeste, elle n'est simplement pas posée.
- **le jeton de gabarit** : un gabarit `nu` porte `<titre de la page>` là où un gabarit `obsidian` porte le jeton que Templater résout.
- **le confort** : masquer un dossier, replier un frontmatter, chercher par nom au clavier. Rien de tout cela n'est un mécanisme du kit ; tout cela manque quand même.

Ce que `nu` **ne** perd **pas** : la dérivation des chemins, la propagation, les dix règles, la mesure, le semis, le figeage, et la validité. Un vault `nu` passe les mêmes validateurs qu'un vault `obsidian` — c'est la preuve que le profil n'est pas une amputation du modèle, seulement de son lecteur.

---

## 7. Ouvrir le vault dans Obsidian

Obsidian n'importe rien et ne convertit rien : un coffre **est** un dossier de fichiers. Ouvrir le vault ne le modifie pas.

À l'écran d'accueil, **Ouvrir un dossier comme coffre** *(Open folder as vault)*, puis choisir la racine de `ton brain` — celle qui porte `brain.yml`.

> **Capture attendue** — `docs/install/img/01-obsidian-selecteur-de-coffre.png` (du kit, réutilisable) : l'écran d'accueil d'Obsidian, bouton « Ouvrir un dossier comme coffre » (Open folder as vault).

> **Capture attendue** — `docs/install/img/02-obsidian-reglages-general.png` (du kit, réutilisable) : le panneau Paramètres → Général, pour situer la barre de gauche.

> **Capture attendue** — `docs/install/img/18-selecteur-dossier-du-vault.png` (DE CETTE INSTANCE) : le sélecteur de dossier pointé sur CE vault — c'est son nom qui est montré, donc la capture ne se réutilise pas.

---

## 8. Autoriser les modules complémentaires

Un coffre neuf est en **mode restreint** : aucun plugin tiers ne tourne. Paramètres (`Ctrl + ,`) → **Modules complémentaires** *(Community plugins)* → **Activer les modules complémentaires**.

Le réglage est **par coffre** : les autres coffres ne sont pas touchés.

> **Capture attendue** — `docs/install/img/03-obsidian-mode-restreint.png` (du kit, réutilisable) : Modules complémentaires (Community plugins) avec le mode restreint ACTIF — l'état de départ d'un coffre neuf.

> **Capture attendue** — `docs/install/img/04-obsidian-modules-actives.png` (du kit, réutilisable) : le même panneau après « Activer les modules complémentaires » : le bouton Parcourir devient cliquable.

---

## 9. Installer les plugins

**Parcourir** *(Browse)*, puis pour chacun : chercher son nom, ouvrir sa carte, **Installer** puis **Activer**. 2 sont requis, 2 sont du confort — et la colonne qui compte est la dernière : *ce qui le rend nécessaire*. Un plugin dont on ne sait pas dire quel mécanisme l'exige est un plugin qu'on n'installe pas.

| Plugin | Auteur | Rôle | Ce qui le rend nécessaire |
|---|---|---|---|
| **Local REST API & MCP Server** | `coddingtonbear` | expose le coffre en HTTPS sur la boucle locale, et parle MCP | l'agent lit le vault VIVANT — frontmatter résolu, vues évaluées — et pas seulement les fichiers du dépôt. Sans lui, un agent voit le markdown mais pas ce qu'Obsidian en fait |
| **Templater** | `SilentVoid13` | remplit une page neuve depuis un gabarit de `Templates/` | les gabarits générés portent le jeton `<% tp.file.title %>` quand le profil est `obsidian` — c'est le kit qui l'écrit, donc c'est le kit qui exige le moteur qui le résout |
| **File Hider** *(confort)* | `eldritch-oliver` | masque un dossier de la barre latérale, sans le supprimer | l'espace de l'agent, les gabarits et la gouvernance sont dans le vault mais ne sont pas des pages : les voir en permanence coûte de l'attention à chaque recherche |
| **Dataview** *(confort)* | `blacksmithgu` | requêtes type SQL sur le frontmatter, en ligne dans une page | rien dans le kit ne l'exige. Il sert de repli quand une version d'Obsidian trop ancienne ne rend pas les vues natives, et pour une requête jetable qu'on ne veut pas figer en page de vue |

> **Vérifier l'auteur avant d'installer.** Plusieurs de ces noms ont des homonymes dans le catalogue, et un homonyme ne fait pas la même chose. La colonne *Auteur* est là pour ça.

> **Capture attendue** — `docs/install/img/05-obsidian-catalogue.png` (du kit, réutilisable) : le navigateur de plugins ouvert, barre de recherche vide.

> **Capture attendue** — `docs/install/img/06-plugin-rest-api-recherche.png` (du kit, réutilisable) : la recherche du plugin de pont agent, avec les résultats voisins visibles — c'est ce qui permet de ne pas se tromper de carte.

> **Capture attendue** — `docs/install/img/07-plugin-rest-api-active.png` (du kit, réutilisable) : la carte du plugin de pont agent après Installer puis Activer.

> **Capture attendue** — `docs/install/img/10-plugins-tous-actives.png` (du kit, réutilisable) : la liste des modules complémentaires, tous les plugins requis activés — l'état final attendu de l'étape.

---

## 10. Pointer Templater sur les gabarits

Réglages → **Templater** → *Template folder location* → `Templates`.

Sans ce réglage, Templater ne trouve rien et une page neuve naît vide. Les gabarits de ce dossier sont **générés** depuis le manifeste, un par rôle : ne pas les éditer à la main, ils se régénèrent — et deux sources qui décrivent le même gabarit divergent.

> **Capture attendue** — `docs/install/img/11-templater-reglages.png` (du kit, réutilisable) : les réglages de Templater, champ « Template folder location » vide.

> **Capture attendue** — `docs/install/img/12-templater-dossier-pose.png` (du kit, réutilisable) : le même champ renseigné avec le dossier de gabarits du vault.

---

## 11. Masquer ce qui n'est pas une page

Le vault porte des dossiers qui ne sont pas des pages : `AI/` (l'espace de l'agent), `Templates/`, `Documentation/`. Les voir en permanence coûte de l'attention à chaque recherche.

Clic droit sur le dossier dans l'explorateur → **Hide folder**. Les fichiers restent là, git les suit, l'agent les lit : seule la barre latérale change.

> **Capture attendue** — `docs/install/img/13-file-hider-options.png` (du kit, réutilisable) : les options de File Hider, liste des chemins cachés vide.

> **Capture attendue** — `docs/install/img/14-file-hider-menu-contextuel.png` (du kit, réutilisable) : le menu du clic droit dans l'explorateur, entrée « Hide folder ».

> **Capture attendue** — `docs/install/img/15-file-hider-apres.png` (du kit, réutilisable) : l'explorateur après masquage : l'espace de l'agent a disparu de la barre latérale.

---

## 12. Colorer le graphe par rôle

Une couleur par rôle, dans le panneau du graphe → **Groupes**. La table vit dans le manifeste de l'instance, et l'`INSTALL.md` de l'instance la donne ligne par ligne.

Deux faits qui valent pour tout brain, et qu'on ne retrouve pas en réessayant :

- **l'ordre des requêtes compte.** Une règle qui cible un chemin doit passer **avant** une règle qui cible un rôle, sinon un hub spécial prend la couleur des hubs ordinaires.
- **un fichier de vue ne se colore pas.** Il n'a pas de frontmatter, donc pas de rôle. Ce n'est pas un réglage à trouver, c'est une limite à connaître.

La cible de ces réglages n'est en général **pas versionnée** : la table du manifeste est la seule source, et elle se réapplique à la main sur chaque poste. C'est une étape d'installation, pas un fichier.

---

## 13. Brancher l'agent

Le semis a écrit, à la racine de l'instance, le routeur de l'agent (`CLAUDE.md` et son contexte de mode) et, sous `.claude/skills/`, les skills du brain. Il n'y a rien à écrire : tout sort du manifeste.

Trois skills, et le découpage est **structurel**, pas thématique — un skill qui **écrit** dans le brain, un skill qui **clôt** toute écriture, un skill qui **consomme** le brain sans y écrire. Tout brain a besoin des trois ; le troisième peut légitimement ne pas exister, et son absence est alors écrite plutôt que remplie par un skill creux.

La première section de `CLAUDE.md` est la **règle d'identité git**, et ce n'est pas un choix de mise en page : c'est le seul fichier chargé dans **chaque** conversation, au même moment que l'annonce de l'outil. Une contre-instruction qui arrive après coup arrive trop tard.

Pour que l'agent lise le vault **vivant** et pas seulement ses fichiers, brancher le plugin de pont : ses options donnent l'URL locale, la clé d'API et le bloc de configuration MCP à coller côté agent.

> La clé donne un accès complet en lecture et en écriture au coffre. Elle se traite comme un mot de passe, et elle ne se committe **jamais**.

> **Capture attendue** — `docs/install/img/08-plugin-rest-api-options.png` (du kit, réutilisable) : les options du plugin de pont : URL locale et clé d'API, **la clé masquée** — une clé n'a pas sa place dans un dépôt.

> **Capture attendue** — `docs/install/img/09-plugin-rest-api-mcp.png` (du kit, réutilisable) : la section « How to access via MCP » du plugin, qui donne le bloc de configuration à coller côté agent.

> **Capture attendue** — `docs/install/img/28-agent-connecte.png` (DE CETTE INSTANCE) : l'agent listant les pages du vault, preuve que le pont répond.

---

## 14. Vérifier que tout marche

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

Sur une instance **fraîchement semée**, les trois répondent : zéro violation dure, **zéro avertissement**, zéro écart, arbre propre. Le zéro avertissement est plus fort qu'il n'y paraît : sur un vault à zéro page d'unité, tout avertissement porterait sur une page que personne n'a écrite — il signalerait donc un défaut du **kit**.

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
```

> **Capture attendue** — `docs/install/img/26-verdict-valider.png` (DE CETTE INSTANCE) : le terminal, sortie de la commande de validation sur ce vault.

> **Capture attendue** — `docs/install/img/27-verdict-generer-check.png` (DE CETTE INSTANCE) : le terminal, sortie du contrôle des artefacts dérivés — code 0.

---

## 15. Livrer une instance autonome — `freeze`

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

## 16. Dépannage

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

## 17. Le manifeste d'images

Les captures se rangent sous `docs/install/img/`.

Ce guide appelle **28 captures** et n'en embarque aucune. Elles se rangent en deux tas, et la coupure décide qui les refait :

- **17 captures du kit** — elles montrent l'interface d'Obsidian et rien du contenu. Prises une fois, elles valent pour toutes les instances.
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
| `17-snippet-css-actif.png` | kit | Apparence → Extraits CSS, l'extrait des rôles activé |
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
