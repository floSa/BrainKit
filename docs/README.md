# Documentation de BrainKit

**Ce dossier est écrit à la main, et il parle du kit.** Il ne parle d'aucun
sujet, et il ne lit aucun manifeste.

C'est la première chose à savoir en arrivant, parce que le dépôt contient
**deux** natures de documentation et qu'on ne les corrige pas de la même façon :

| Nature | Où | Qui l'écrit | Comment on la corrige |
|---|---|---|---|
| **la doc du kit** | ici, `docs/` | à la main | on l'édite |
| **la doc d'une instance** | à la racine du vault semé | **générée** par `brainkit/emballer/` depuis `brain.yml` | on corrige le **générateur** ou le **manifeste** — jamais le fichier |

Un exemple complet de la seconde, rendu une fois depuis le manifeste de
démonstration, est lisible dans
[`../exemples/rendu-histobrain/`](../exemples/rendu-histobrain).

---

## Par où commencer

| Vous voulez | Lisez |
|---|---|
| **installer le kit** sur une machine neuve | [03-installation.md](03-installation.md) |
| **créer votre premier brain** | [05-premier-brain.md](05-premier-brain.md) |
| **régler Obsidian** sur un vault existant | [04-obsidian.md](04-obsidian.md) |
| vous en servir tous les jours | [06-manuel.md](06-manuel.md) |
| comprendre pourquoi c'est fait comme ça | [01-cadrage.md](01-cadrage.md) |
| comprendre comment c'est construit | [02-architecture.md](02-architecture.md) |
| remettre un brain sur une machine sans accès internet | [07-livrer-une-instance.md](07-livrer-une-instance.md) |
| régler un problème | [08-depannage.md](08-depannage.md) |
| les secrets, l'identité git | [SECURITY.md](SECURITY.md) |

**La route complète, de rien à un brain vert** :
[03](03-installation.md) → [05](05-premier-brain.md) → [04](04-obsidian.md) →
[06](06-manuel.md).

L'ordre peut surprendre : on installe, on sème, **puis** on règle Obsidian.
C'est délibéré — la configuration d'Obsidian ne sert à rien avant qu'un vault
existe, et plusieurs de ses étapes demandent d'avoir le vault sous les yeux.

---

## Les huit fichiers

| Fichier | Ce qu'il couvre |
|---|---|
| [01-cadrage.md](01-cadrage.md) | le **pourquoi** : le problème d'origine, les cinq principes et ce qui les a imposés, le périmètre, les hypothèses assumées, ce qui n'est pas tranché |
| [02-architecture.md](02-architecture.md) | le **comment** : kit contre instance, le manifeste comme seule source, les huit paquets, les deux modes, les deux profils, le jeu d'épreuve, les licences |
| [03-installation.md](03-installation.md) | pré-requis, obtenir le kit avec ou sans remote, les hooks git, les deux façons de le lancer, la vérification |
| [04-obsidian.md](04-obsidian.md) | ouvrir le vault, les plugins et leurs homonymes, Templater, masquer un dossier, l'exclure de la recherche, replier les propriétés, colorer le graphe, brancher l'agent |
| [05-premier-brain.md](05-premier-brain.md) | l'entretien et ses treize refus, composer le manifeste, semer, les quatre refus du semis, la première capture, clôturer |
| [06-manuel.md](06-manuel.md) | les huit commandes, la boucle de tous les jours, chercher, capturer, mettre à jour, régénérer, valider, mesurer, sonder, re-seuiller |
| [07-livrer-une-instance.md](07-livrer-une-instance.md) | `freeze` : ce qu'il copie, ce qu'il perd, pourquoi il n'y a pas de dégel, la liste avant remise |
| [08-depannage.md](08-depannage.md) | problème / cause / solution, par domaine |
| [SECURITY.md](SECURITY.md) | la clé du pont, l'identité git et ses trois garde-fous, ce qu'un dépôt de brain ne doit pas contenir |

Plus `img/`, les captures d'écran.

---

## Les captures

Cette documentation **référence** ses images, et n'en fabrique aucune.

| État | Compte | Forme dans le texte |
|---|---|---|
| présentes dans `img/` | **15** | une balise d'image normale |
| **à prendre en séance** | **16** | un bloc en citation, qui nomme le fichier, l'écran, l'action à faire avant, et la zone à cadrer |

Une image absente est donc un **trou nommé**, jamais une balise cassée : un lien
vers un fichier qui n'existe pas afficherait une image brisée, ce qui se lit
comme un défaut du document plutôt que comme un travail à faire.

Aucune n'est fabriquée, et c'est délibéré. Une capture inventée montrerait une
interface qui n'existe pas — strictement pire qu'un trou nommé. C'est le même
raisonnement que la règle du haut de page : *une cellule vide honnêtement vaut
mieux qu'une cellule remplie au jugé*.

Le protocole de prise — la liste ordonnée, avec pour chacune l'écran, l'action
et le cadrage — est dans
[`../design/12-captures.md`](../design/12-captures.md). Il est fait pour être
exécuté par quelqu'un qui pilote la machine sans avoir lu le reste.

### Le contrôle

```bash
uv run outils/captures.py
```

Il vérifie les deux sens : **aucune image référencée ne manque**, et **aucune
image du dossier n'est orpheline**. Il sort en 2 sur écart, et il liste ce qui
reste à prendre en séance sans le compter comme une faute.

---

## Ce qui n'est pas ici

| Ce que vous cherchez | Où c'est |
|---|---|
| chaque arbitrage de conception, avec sa mesure | [`../design/`](../design), un fichier par lot |
| l'état du chantier, ce qui reste ouvert | [`../design/etat-final.md`](../design/etat-final.md) |
| le contrat du manifeste | [`../schema/brain.schema.json`](../schema/brain.schema.json) |
| des manifestes complets, dont un contre-exemple | [`../exemples/`](../exemples) |
| le skill qui mène l'entretien | [`../skills/entretien/SKILL.md`](../skills/entretien/SKILL.md) |
| le manuel de **votre** brain | dans votre vault, généré par le semis |
