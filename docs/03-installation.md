# Installer le kit

**La voie normale d'usage de ce kit est un agent de code, pas une clé d'API.**
Claude Code, Cursor, Antigravity, Windsurf ou un autre : on lui donne les
consignes, il pose les questions à l'humain, et il suit des recettes. Son point
d'entrée est [`../AGENTS.md`](../AGENTS.md), et les recettes sont dans
[`../recettes/`](../recettes/README.md) — du Markdown pur, sans dépendance à un
format propriétaire.

**Aucune clé, aucun jeton, aucun compte n'est requis nulle part.** Le sondage de
fraîcheur lui-même (`brainkit sonder`) tape sur des URL publiques anonymes, et
il est écrit pour ne jamais lire ni écrire un jeton : un jeton dans un vault
versionné est un secret publié.

Tout le kit s'utilise aussi **à la main**, dans un terminal, sans agent : c'est
ce que décrit ce chapitre, et les deux tiers de ce qu'il fait se vérifient
comme ça. L'agent n'est pas une couche au-dessus, c'est le lecteur pour lequel
les skills et les recettes sont écrits.

---

**Ce chapitre s'arrête quand `brainkit` répond.** Créer un premier brain est le
chapitre suivant : [05-premier-brain.md](05-premier-brain.md). Configurer
Obsidian est [04-obsidian.md](04-obsidian.md), et cela ne sert qu'une fois qu'un
vault existe.

> **Durée** : 10 minutes si `uv` est déjà là, 15 sinon.

---

## Sommaire

1. [Pré-requis](#1-pré-requis)
2. [Obtenir le kit](#2-obtenir-le-kit)
3. [Activer les hooks git](#3-activer-les-hooks-git)
4. [Lancer le kit — deux façons, et il faut choisir](#4-lancer-le-kit--deux-façons-et-il-faut-choisir)
5. [Vérifier que l'installation est bonne](#5-vérifier-que-linstallation-est-bonne)
6. [Ce qui n'est pas encore fait](#6-ce-qui-nest-pas-encore-fait)

---

## 1. Pré-requis

| Outil | Version mini | Vérification | Pourquoi |
|---|---|---|---|
| [git](https://git-scm.com/downloads) | — | `git --version` | l'historique du vault, et les trois garde-fous d'identité |
| [Python](https://www.python.org/downloads/) | 3.10+ | `python --version` | le kit est écrit en Python |
| [`uv`](https://docs.astral.sh/uv/getting-started/installation/) | — | `uv --version` | lance le kit sans rien installer dans l'environnement Python du poste |
| [Obsidian](https://obsidian.md/download) | 1.10+ | l'app s'ouvre | le lecteur du vault, et le moteur des vues natives. **Facultatif** : un brain en profil `nu` n'en a pas besoin |
| **un agent de code** (Claude Code, Cursor, Antigravity, Windsurf…) | — | la commande de l'agent choisi | **la voie normale** : les recettes et les skills d'un vault sont écrits pour lui. Aucune clé d'API. **Repli explicite** : tout se lit, se valide et se génère dans un terminal nu |

`uv` **n'est pas** Python : c'est un lanceur et un installateur de paquets. Le
kit s'en sert pour tourner sans rien salir — et une instance **figée** s'en sert
pour tourner sans rien installer du tout.

> Obsidian est marqué facultatif, et ce n'est pas une politesse : un brain en
> profil `nu` s'en passe entièrement. L'agent de code, lui, n'est pas facultatif
> au même titre — c'est la voie normale, et le terminal nu est le **repli**.
> Ce qu'on perd sans Obsidian est écrit à
> [02-architecture.md](02-architecture.md) §7.

Une seule dépendance d'exécution, **PyYAML**. `uv` l'installe tout seul au
premier lancement ; il n'y a pas de `pip install` à faire.

---

## 2. Obtenir le kit

### Si le dépôt a un remote atteignable

```bash
git clone <url du dépôt BrainKit> ~/BrainKit
cd ~/BrainKit
```

Pour connaître l'URL depuis une copie déjà présente sur la machine :

```bash
git -C <la copie existante> remote get-url origin
```

> **Attention à un piège de forme.** L'URL peut nommer un **alias SSH** plutôt
> qu'un hôte réel — par exemple `git@github.com-perso:…` au lieu de
> `git@github.com:…`. Un alias est défini dans le `~/.ssh/config` d'**une**
> machine : il ne se clone pas depuis une autre. Sur un poste neuf, remplacer
> l'alias par l'hôte réel, ou recopier l'entrée correspondante de `~/.ssh/config`.

### S'il n'y a pas d'URL utilisable

C'est un cas normal, pas une exception : une livraison hors ligne n'a jamais
d'URL. Trois formes, et elles ne se valent pas :

| Forme | Commande | Ce qu'on garde |
|---|---|---|
| **un `git bundle`** — à préférer | `git clone brainkit.bundle ~/BrainKit` | l'historique **et** la vérifiabilité |
| **un dossier copié** | `cp -r <source> ~/BrainKit` | l'historique, s'il est dans le dossier copié |
| **une archive** `.zip` / `.tar.gz` | l'extraire | rien de l'historique. La seule trace de version restante est `__version__` dans `brainkit/__init__.py` |

Un clone de bundle atterrit **parfois** en HEAD détachée : cela dépend de la
façon dont le bundle a été fabriqué. Un bundle qui porte `HEAD` et une branche
(`git bundle create … --all`) se clone sur `main` comme un dépôt normal ; un
bundle bâti sur une plage de révisions, non. Le contrôle est le même dans les
deux cas, et il est immédiat :

```bash
git -C ~/BrainKit status | head -1
```

- « On branch main » : il n'y a rien à faire ;
- « HEAD detached at … » : `git switch -c main`. Sur le kit c'est sans
  conséquence — on n'y committe pas — mais le faire tout de suite évite d'avoir
  à se le demander plus tard.

Ne pas lancer `git switch -c main` à l'aveugle : sur un clone déjà sur `main`, la
commande échoue avec `fatal: a branch named 'main' already exists`, ce qui
inquiète pour rien.

La suite de ce chapitre est **identique** dans tous les cas : rien ci-dessous ne
suppose un remote.

---

## 3. Activer les hooks git

À faire **une fois par clone**, et avant le premier commit :

```bash
git config core.hooksPath .githooks
```

Vérifier que c'est pris — la commande doit répondre `.githooks` :

```bash
git config core.hooksPath
```

**Git ne regarde pas `.githooks/` par défaut.** Sans cette commande, les hooks
sont bien dans le dépôt et ne s'exécutent pas — ce qui est pire qu'aucun
garde-fou, parce qu'on le croit actif. Un **worktree** hérite de la config du
dépôt principal ; un **clone** neuf, non.

Ce que les trois hooks tiennent :

| Hook | Ce qu'il refuse |
|---|---|
| `pre-commit` | un commit dont l'**auteur** ou le **committer** porte l'adresse professionnelle. Il lit l'identité *effective*, donc couvre aussi `-c user.email=…`, `--author=…` et les variables d'environnement |
| `commit-msg` | un message portant un trailer de co-auteur : les commits de ce dépôt sont à une seule personne |
| `pre-push` | de **pousser** un commit fautif, quelle que soit son origine — un contournement, un `rebase` qui rejoue une identité, un commit importé d'un autre clone |

**Pourquoi le message a son propre hook** : git exécute `pre-commit` **avant**
de composer le message. À cet instant, le fichier de message porte encore celui
du commit précédent — un test placé là ne verrait rien, et une règle qui ne
trouve jamais rien ressemble à une règle satisfaite. C'est ce trou qui avait
laissé passer cinq commits dans le vault d'origine.

Un hook qui refuse n'est pas un incident à contourner : c'est la règle qui
fonctionne. Le contournement de vérification ne s'utilise pas ici. Le détail
est dans [SECURITY.md](SECURITY.md) §2.

> Ce chapitre parle des hooks **du dépôt du kit**. Une instance semée reçoit ses
> propres hooks, posés par `brainkit semer`, et il faut y refaire la même
> commande — voir [05-premier-brain.md](05-premier-brain.md) §5.

---

## 4. Lancer le kit — deux façons, et il faut choisir

C'est le pas qu'on oublie, et un outillage qu'on ne sait pas lancer est un
outillage qui ne tourne pas. **Choisir maintenant**, pas au premier besoin.

### a. Depuis le dépôt du kit

Rien à installer. `uv` s'occupe des dépendances au premier appel.

```bash
cd ~/BrainKit
uv run brainkit
```

La commande doit lister les **huit** sous-commandes et sortir en code 2 — elle
ne choisit pas de défaut, et c'est voulu.

> **Au premier appel seulement**, `uv` construit le paquet et imprime deux
> lignes `Building brainkit @ …` avant la sortie utile. Ce n'est pas une erreur,
> et cela n'arrive qu'une fois par arbre. En revanche, ce premier appel a besoin
> d'atteindre un index de paquets : sur une machine réellement hors ligne, il
> échoue. Obtenir le kit hors ligne (§2) et **le lancer** hors ligne sont deux
> problèmes différents — le second se traite par un cache `uv` pré-rempli, ou
> par `brainkit freeze` côté instance
> ([07-livrer-une-instance.md](07-livrer-une-instance.md)).

**Cette voie ne suffit pas** dès qu'un vault existe : `uv run brainkit`, lancé
depuis un vault, échoue avec `Failed to spawn: brainkit — program not found`.
`uv run` cherche la commande dans le projet **courant**, et un vault n'est pas un
projet Python. Lire la voie **b**, et l'encadré qui la suit.

### b. Sur le PATH

La commande devient disponible partout, y compris depuis le dossier d'une
instance. C'est la façon à préférer dès qu'un brain existe.

```bash
uv tool install --editable ~/BrainKit
brainkit
```

Si `brainkit` n'est pas trouvé juste après, le dossier des outils `uv` n'est pas
sur le PATH :

```bash
uv tool update-shell
```

…puis **rouvrir le terminal**. Une variable de PATH modifiée n'atteint pas un
terminal déjà ouvert.

> **Pourquoi ce choix mérite une section.** Une instance sait qu'elle est
> branchée sur un kit ; elle ne sait pas **où** ce kit vit. C'est un trou
> mesuré, et il a deux bouchons — **qui ne se valent pas** :
>
> 1. **mettre `brainkit` sur le PATH** — la façon **b** ci-dessus. C'est le seul
>    bouchon qui marche sur **tous** les brains, et c'est donc celui à prendre en
>    cas de doute ;
> 2. **laisser l'instance chercher le kit elle-même.** Le semis pose un
>    résolveur, `AI/scripts/_pont_kit.py`, qui essaie dans l'ordre la variable
>    `BRAINKIT_RACINE`, puis un kit copié dans l'instance, puis un dossier
>    `BrainKit/` voisin. **Mais ce résolveur est une bibliothèque, pas une
>    commande** : il est *importé* par les scripts de pont, et ces scripts ne
>    sont posés que si le manifeste déclare un bloc `agent.ponts`. Sur un brain
>    qui n'en déclare pas — le cas d'un brain neuf — `AI/scripts/` ne contient
>    que le résolveur et un fichier d'explication : **il n'y a rien à lancer**.
>
> Autrement dit : le bouchon 2 est un confort pour un brain qui déclare ses
> ponts, notamment un vault migré depuis des scripts existants. Le bouchon 1 est
> celui dont **tout** brain a besoin.

Vérification, depuis la racine d'un vault :

```bash
brainkit valider
```

- un verdict : le bouchon 1 est en place ;
- `brainkit : commande introuvable` : reprendre la façon **b**, puis rouvrir le
  terminal ;
- `Failed to spawn: brainkit` : la commande a été lancée avec `uv run` depuis le
  vault. Retirer `uv run`.

Pour le bouchon 2, quand le brain déclare des ponts, poser la variable une fois
pour toutes dans le profil du shell :

```bash
export BRAINKIT_RACINE=~/BrainKit
```

Sous Windows, en PowerShell, l'équivalent durable est
`[Environment]::SetEnvironmentVariable('BRAINKIT_RACINE', "$HOME\BrainKit", 'User')`,
suivi d'une réouverture du terminal.

---

## 5. Vérifier que l'installation est bonne

Trois commandes, depuis le dépôt du kit. Aucune n'écrit.

```bash
uv run brainkit                 # les huit sous-commandes, code 2
uv run schema/valider.py        # le contrat, sur les quatre manifestes du depot
uv run tests/epreuve.py         # les regles de validation
```

| Commande | Attendu | Ce qu'une autre sortie veut dire |
|---|---|---|
| `brainkit` | la liste des huit sous-commandes, **code 2** | un code 0 ou un traceback : mauvaise version de Python, ou paquet mal résolu |
| `schema/valider.py` | les trois manifestes traités, dont le **contre-exemple qui doit échouer** | `jsonschema` manque — c'est un extra, `uv run` le résout tout seul depuis l'en-tête du script |
| `tests/epreuve.py` | tous les contrôles verts | un échec sur un vault réel absent n'est pas un échec : le jeu le **saute** et le dit |

Le jeu d'épreuve complet, si l'on veut tout passer d'un coup, est listé à
[02-architecture.md](02-architecture.md) §9.

---

## 6. Ce qui n'est pas encore fait

À ce stade il n'y a **aucun brain**. Le kit est installé, il ne s'est appliqué à
rien.

| Ensuite | Où |
|---|---|
| écrire un manifeste, puis semer le premier vault | [05-premier-brain.md](05-premier-brain.md) |
| ouvrir ce vault dans Obsidian et le régler | [04-obsidian.md](04-obsidian.md) |
| l'usage de tous les jours | [06-manuel.md](06-manuel.md) |
| quelque chose ne marche pas | [08-depannage.md](08-depannage.md) |
