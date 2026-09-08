# Cadrage — pourquoi BrainKit existe

**Ce document dit le POURQUOI.** Le COMMENT est dans
[02-architecture.md](02-architecture.md) ; la route d'installation est dans
[03-installation.md](03-installation.md).

Rien ici n'est une intention : chaque affirmation renvoie au rapport de lot qui
l'a mesurée, sous `../design/`.

---

## 1. Le problème d'origine

Un vault Obsidian de **765 pages** existait — un brain de développement
logiciel, construit sur trois versions successives. Il fonctionnait, et il
portait deux défauts qui n'étaient pas des défauts de contenu :

| Défaut observé | Ce qu'il coûtait |
|---|---|
| la **forme** du vault (les rôles, les dossiers, les règles) était mélangée à son **sujet** (les technos, les concepts de dev) | rien n'était réutilisable sur un autre sujet sans tout relire |
| **deux fichiers décrivaient le même gabarit** — le dossier `Templates/` et le fichier de contexte de l'agent | `Templates/` avait pris **trois lots de retard** sur ses 337 pages, sans que personne ne le voie |

Le second défaut est le plus instructif : ce n'est pas une négligence, c'est une
conséquence mécanique de la duplication. Deux sources qui décrivent la même
chose divergent — la question n'est pas « si », elle est « quand ».

---

## 2. L'objectif, en une phrase

Extraire de ce vault **la forme sans le sujet**, et la rendre exécutable : un
paquet qui crée, valide et entretient un second brain sur **n'importe quel
sujet**, en ne lisant qu'un seul fichier de description.

Ce fichier est `brain.yml`, appelé le **manifeste**. Il porte les mots du sujet,
ses axes de rangement, ses natures de page, ses règles et leur sévérité. Le kit
ne sait rien d'autre du brain que ce fichier.

---

## 3. Les cinq principes, et ce qui les a imposés

Ce ne sont pas des préférences de style. Chacun est né d'une mesure.

### 3.1 Une seule source

La taxonomie, les vocabulaires, les gabarits, la table de couleurs, les skills,
la table de propagation, les guides d'une instance : **tous générés** depuis
`brain.yml`. Rien de tout cela ne s'écrit à la main.

> **Problème** : deux fichiers décrivaient le même gabarit, et ils avaient
> divergé de trois lots. **Options** : (a) une discipline de relecture,
> (b) un contrôle de concordance, (c) une seule source et une génération.
> **Retenu** : (c), **plutôt que** (a) parce qu'une discipline ne se vérifie
> pas, et **plutôt que** (b) seul parce qu'un contrôle qui trouve un écart
> laisse quand même l'écart à réparer à la main. **Limite** : ce qui est généré
> ne se personnalise pas sur place — il faut modifier le manifeste, ce qui est
> exactement l'effet voulu.

Corollaire vérifiable : chaque générateur a un mode `--check` qui n'écrit rien
et **sort en code 2** s'il reste un écart. C'est la forme mécanique de « ce qui
est généré n'est jamais édité à la main ».

### 3.2 Aucune sévérité n'est héritée

Une règle du kit arrive dans une instance neuve en `a_mesurer`, jamais en
`dure`. On ne durcit qu'après avoir **compté** les violations sur le corpus
réel ; on n'assouplit qu'en **écrivant le motif** — le kit refuse un
`severite: avertissement` sans champ `motif:`.

`brainkit mesurer` est l'outil de ce comptage, et il **refuse** de proposer un
durcissement sous **30 pages** : en dessous, zéro violation ne prouve rien.

Deux exceptions, écrites et bornées : la cohérence chemin/catégorie et la
concordance des zones générées. Là, une violation n'est pas un manque de
contenu, c'est une incohérence de **structure**.

### 3.3 On réécrit la règle plutôt que d'ajouter une exception

Deux des dix règles ont été **réécrites** parce que la mesure a montré que leur
formulation d'origine était inatteignable. Le détail est dans
`../design/08-mesure.md`.

### 3.4 Rien ne se devine

Ni un axe, ni une sévérité, ni une identité git, ni un chemin de kit, ni le
libellé d'un dossier promu. **Un champ vide est une question ouverte ; une
valeur inventée est une faute.**

L'entretien porte **treize refus de deviner** en liste fermée. Le premier —
l'identité git — a **trois** garde-fous, parce qu'un seul avait déjà lâché : une
identité devinée entre dans l'historique du dépôt et n'en sort plus sans
réécriture.

### 3.5 Une ligne sans objet se déclare sans objet

Un silence se lit comme un oubli ; une ligne qui dit « sans objet ici, parce que
ceci » se lit comme une décision. C'est de cette règle que sort la phrase qui
résume le kit :

> **Une fiche vide honnêtement vaut mieux qu'une fiche remplie au jugé.**

---

## 4. Le périmètre — ce qui est dedans

| Capacité | Commande | Chapitre |
|---|---|---|
| écrire un manifeste par entretien | `entretien` | [05-premier-brain.md](05-premier-brain.md) |
| créer un vault vierge | `semer` | [05-premier-brain.md](05-premier-brain.md) |
| valider un vault contre son manifeste | `valider` | [06-manuel.md](06-manuel.md) |
| régénérer les artefacts dérivés | `generer` | [06-manuel.md](06-manuel.md) |
| mesurer le coût d'une règle avant de la durcir | `mesurer` | [06-manuel.md](06-manuel.md) |
| sonder l'amont d'une unité (fraîcheur) | `sonder` | [06-manuel.md](06-manuel.md) |
| changer le seuil de promotion d'un sous-dossier | `re-seuiller` | [06-manuel.md](06-manuel.md) |
| couper la dépendance au kit, pour une livraison hors ligne | `freeze` | [07-livrer-une-instance.md](07-livrer-une-instance.md) |

---

## 5. Hors périmètre — et pourquoi

Ce sont des **limites écrites**, pas des oublis. Le motif compte plus que la
limite.

| Ce que le kit ne fait pas | Pourquoi |
|---|---|
| **une autre langue que le français** | le pont existe — la prose sort de gabarits, un gabarit se duplique par langue — mais aucun engagement avant que deux instances françaises tournent |
| **hériter une sévérité** | `dure` et `avertissement` sont des **résultats de mesure** sur un corpus, pas des propriétés de règle (cf. 3.2) |
| **générer les vues filtrées** | un filtre est un arbitrage éditorial, un par vue. Mesuré : sur le vault d'origine, les 47 vues ont représenté **un tiers** du travail de migration |
| **rendre une vue en tableau markdown en profil `nu`** | ce serait un cinquième générateur, donc un mécanisme de plus |
| **importer un corpus existant** | c'est le vrai chantier d'amorçage : il dépend entièrement du sujet et mérite son propre cadrage |
| **une interface graphique pour l'entretien** | l'entretien est conversationnel par nature ; un formulaire ramènerait les listes à cocher que les treize refus interdisent |
| **évaluer une condition de section** | `existe_si:` est du français (« au moins une entrée datée »). Ni le validateur ni le semis ne peuvent l'évaluer ; `mesurer` compte à la place l'**usage réel** de la section |
| **confronter `kit.mode` au disque** | une instance qui se déclare branchée avec un kit copié dedans passerait inaperçue. Remontée ouverte |
| **fabriquer les captures d'écran** | une capture inventée montrerait une interface qui n'existe pas. Le protocole de prise est dans `../design/12-captures.md` |

---

## 6. Les hypothèses de travail

Elles ne sont pas démontrées ; elles sont **assumées**, et il faut les connaître
avant de bâtir dessus.

| Hypothèse | État |
|---|---|
| un brain ne rend service qu'à **plusieurs centaines de pages** | observé sur le vault d'origine, jamais mesuré ailleurs. Un brain à 20 pages ne sert à rien |
| le **seuil de promotion** d'un sous-dossier se dérive d'une loi | calibrée sur **deux points** (765 pages → 5, 600 pages → 12). Deux points ne font pas une loi : la troisième instance réelle dira si elle tient |
| un agent de code est le **lecteur principal** du brain | c'est ce que le profil `nu` teste : un vault `nu` passe les mêmes validateurs, sans Obsidian |
| l'ontologie d'un brain construit pour un tiers est **signante** | un arbre de décision décrit une organisation. Ce point n'est **pas tranché** et appartient au propriétaire du dépôt |

---

## 7. Ce qui n'est pas tranché, et n'a pas à l'être ici

Deux décisions appartiennent au propriétaire du dépôt, et aucun document ne les
tranche à sa place :

1. **La licence.** [`../LICENSE`](../LICENSE) porte *tous droits réservés*, et
   le fichier écrit pourquoi : ce n'est pas une décision, c'est l'absence de
   décision posée dans la forme la plus **réversible** qui soit.
2. **La propriété de la taxonomie d'un brain construit pour quelqu'un d'autre.**
   Le `brain.yml` d'un tel brain contient l'ontologie d'un métier. C'est un
   livrable, et c'est en même temps la description d'une organisation.

Aucun document de ce dépôt ne porte de valeur monétaire, de proposition
commerciale, d'argumentaire de vente ni de nom de tiers. Un contrôle du jeu
d'épreuve le vérifie, fichier par fichier.

---

## 8. Où lire la suite

| Question | Document |
|---|---|
| comment c'est construit | [02-architecture.md](02-architecture.md) |
| comment j'installe | [03-installation.md](03-installation.md) |
| chaque arbitrage, avec sa mesure | `../design/`, un fichier par lot |
| l'état du chantier, ce qui reste ouvert | `../design/etat-final.md` |
