# BrainKit

Le noyau générique d'un **second brain** : un vault Obsidian de fichiers markdown
qui se **valide**, se **génère** et se **propage** tout seul — sur n'importe quel
sujet. Tout ce qui est propre à un sujet vit dans un seul fichier, `brain.yml` ;
rien dans le code ne nomme un domaine.

Le kit a été **extrait** d'un brain de développement logiciel de 765 pages, puis
éprouvé sur trois autres sujets — l'histoire, la montagne, le droit du travail —
pour vérifier qu'il n'en avait rien gardé.

## Démarrer en cinq lignes

```bash
uv tool install --editable .                       # le kit sur le PATH
brainkit entretien --questions                     # les 49 questions qui écrivent le manifeste
brainkit semer --manifeste mon.brain.yml --dans ~/MonBrain --ecrire
cd ~/MonBrain && brainkit valider                  # 0 violation dure sur un brain neuf
brainkit generer                                   # `--check` : les artefacts dérivés concordent
```

Le guide complet, de rien à un brain vert : **[INSTALL.md](INSTALL.md)** — généré,
comme tout ce qui décrit un brain.

## Ce qu'il fait

| Commande | Ce qu'elle fait |
|---|---|
| `entretien` | mène les 49 questions qui produisent un `brain.yml`, et **refuse d'en deviner treize** |
| `semer` | crée le vault : dossiers, hubs, gabarits, taxonomie, skills, hooks, dépôt |
| `valider` | dix règles de contenu et de structure, chacune avec la sévérité **que le manifeste déclare** |
| `generer` | les artefacts dérivés — index, hubs, liens, hauts de page. `--check` par défaut |
| `mesurer` | ce qu'une règle **coûterait** avant de la durcir, et les garde-fous qui l'interdisent trop tôt |
| `re-seuiller` | changer le seuil de promotion d'un sous-dossier — une **migration**, par `git mv` |
| `freeze` | copier le kit **dans** l'instance et couper la dépendance (livraison hors ligne) |

## Ce qui tient l'ensemble

- **Une seule source.** La taxonomie, les gabarits, les guides, les skills, la
  table de propagation, ce guide d'installation : tous **générés** depuis
  `brain.yml`. Deux sources qui décrivent la même chose divergent — c'est mesuré,
  pas supposé.
- **Aucune sévérité n'est héritée.** Un brain neuf reçoit ses dix règles en
  `a_mesurer`. On ne durcit qu'après avoir compté ; on n'assouplit qu'en écrivant
  le motif. `brainkit mesurer` est l'outil de ce comptage.
- **Rien ne se devine.** Ni un axe, ni une sévérité, ni une identité git, ni un
  chemin de kit. Un champ vide est une question ouverte ; une valeur inventée est
  une faute.
- **Ce qui est généré n'est jamais édité à la main**, et ça se vérifie : chaque
  générateur a un `--check` qui sort en 2 s'il reste un écart.

## Le dépôt

| Dossier | Contenu |
|---|---|
| `brainkit/` | le kit — validation, génération, semis, entretien, skills, emballage |
| `schema/` | le contrat de `brain.yml`, en JSON Schema, et son validateur |
| `exemples/` | trois manifestes complets, dont un **contre-exemple** qui doit échouer |
| `tests/` | les neuf jeux d'épreuve, tous lançables par `uv run` |
| `outils/` | les outils de développement du kit (fidélité, régénération des documents) |
| `design/` | les onze rapports de lot — chaque arbitrage avec sa mesure |
| `docs/` | les documents générés, et un jeu de guides d'instance rendu en exemple |

Ce dépôt **n'a pas de remote** : il se transmet par copie de dossier ou par
`git bundle`. Il n'y a donc pas d'URL de clone, et l'`INSTALL.md` le dit.

## Licence

**Tous droits réservés** — voir [LICENSE](LICENSE). C'est un choix **réversible**
et **non tranché** : rien n'est publié, donc rien n'est irrattrapable. Le point
est ouvert dans `design/00-cadrage.md` §5.7.
