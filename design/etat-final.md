# BrainKit — état final du chantier

> Clôture écrite le 2026-09-08, à la fin du lot 10, dernier du plan. **C'est le
> document à relire d'abord** : il dit ce que le kit fait, ce qu'il ne fait pas,
> et ce qui reste ouvert. Le détail de chaque décision est dans le rapport de son
> lot (`design/01-` à `design/10-`), et le cadrage d'origine dans
> `design/00-cadrage.md`.
>
> Rien ici n'est une promesse : tout ce qui est écrit sous « ce que le kit fait »
> a été **mesuré** par une commande, et la commande est nommée.
>
> **Un onzième lot a été mené après cette clôture, le 2026-09-08** : la
> *fraîcheur*, c'est-à-dire l'amont d'une unité — `design/11-fraicheur.md`. Il
> ajoute une commande (`sonder`), un bloc facultatif au manifeste (`amont:`),
> une sixième forme de colonne de bandeau et une règle de socle, et il ferme la
> remontée 1 de §4.3. Ce document a été mis à jour là où il devenait faux ; il
> reste le document à relire d'abord.

---

# 1. Ce que c'est, en cinq lignes

Un **paquet Python** qui crée, valide et entretient un second brain — un vault de
fichiers markdown, ouvrable dans Obsidian, versionné dans git. Tout ce qui est
propre à un sujet vit dans **un seul fichier**, `brain.yml` ; rien dans le code
ne nomme un domaine. Une instance ne contient **pas de code** : le kit vit
ailleurs et lit son manifeste — sauf si on la **fige**, pour une livraison hors
ligne.

Il a été **extrait** d'un brain de développement logiciel de 765 pages, puis
éprouvé sur trois autres sujets pour vérifier qu'il n'en avait rien gardé.

---

# 2. Ce que le kit fait — et par quoi c'est prouvé

| Commande | Ce qu'elle fait | Prouvé par |
|---|---|---|
| `entretien` | mène 49 questions en 11 passes, **refuse d'en deviner 13**, écrit le manifeste | `tests/entretien.py` — un entretien joué en entier sur un troisième sujet, du brouillon au vault vert |
| `semer` | crée le vault : dossiers, un hub par dossier, un gabarit par rôle, taxonomie et vocabulaires, routeur, 3 skills, 3 hooks git, la couche de ponts, `INSTALL.md` et 3 guides, le dépôt et son premier commit | `tests/semis.py` — 7 scénarios dont le cas négatif ; une instance neuve est verte et **à son point fixe** |
| `valider` | les 10 règles de contenu et de structure, plus les contrôles de socle **que le manifeste déclare** (18 sur le DevBrain), chacun avec **sa** sévérité | `tests/epreuve.py` — égalité **règle par règle** avec les deux validateurs d'origine : 0 dure, 111 avertissements |
| `generer` | 4 artefacts dérivés — index, hubs, liens, hauts de page. `--check` par défaut, code 2 sur écart | `tests/generation.py` — **413 artefacts sur 414 identiques à l'octet** sur le vault réel, le 414e étant un défaut corrigé |
| `mesurer` | ce qu'une règle **coûterait** avant de la durcir, avec trois garde-fous qui l'interdisent trop tôt | `tests/mesure.py` — dont le **contrôle négatif** du plancher de 30 pages |
| `sonder` | l'**amont** d'une unité : dernière version publiée, dernier commit, dépôt archivé. Sans jeton, avec reprise, et n'écrit que dans un side-car | `tests/amont.py` — dont le **contrôle négatif** : le même manifeste sans bloc `amont:` ne sonde rien, ne signale rien, n'affiche aucune colonne |
| `re-seuiller` | change le seuil de promotion : une **migration**, par `git mv`, refusée sur un arbre sale | `tests/semis.py` scénario 5 — 3 renommages réels, un hub orphelin **signalé** et non supprimé |
| `freeze` | copie le kit **dans** l'instance et coupe la dépendance | `tests/emballage.py` scénario 4 — l'instance figée rend le **même verdict, ligne pour ligne** |

Et deux outils de dépôt, pas de sous-commandes : `outils/fidelite.py` (la
fidélité au vault d'origine) et `outils/emballer.py` (les documents du dépôt
sont-ils ceux que le kit génère).

## 2.1 Ce qui est généré, et ne s'écrit donc jamais à la main

La taxonomie, les vocabulaires, les gabarits, la table de couleurs, les trois
skills, la table de propagation, `INSTALL.md`, les trois guides, les zones des
hubs, l'index, la carte des liens, les hauts de page. **Tout sort de
`brain.yml`.** C'est la propriété 1 du manifeste — *il est la seule source* — et
elle existe pour une raison mesurée : dans le vault d'origine, `Templates/` avait
pris **trois lots de retard** sur ses 337 pages, parce que deux fichiers
décrivaient le même gabarit.

## 2.2 Les quatre instances qui existent

| Instance | Ce qu'elle est | État |
|---|---|---|
| **DevBrain** | le vault réel, 765 pages, 337 unités, 47 vues | instance depuis le lot 9, sur une **branche non intégrée** — l'intégration appartient à floSa |
| **HistoBrain** | un brain d'histoire, banc d'essai de référence | vierge puis rempli à 62 pages |
| **CimeBrain** | un brain de montagne, né d'un entretien joué en entier | recomposé depuis ses réponses, jamais copié |
| **DroitBrain** | un brain de droit du travail | né de l'installation à blanc du lot 10 |

Les trois derniers vivent **hors de tout dépôt suivi**. Aucun n'est un livrable.

---

# 3. Ce que le kit ne fait pas

Ce sont des **limites écrites**, pas des oublis. Chacune a un motif, et le motif
compte plus que la limite.

| Ce qu'il ne fait pas | Pourquoi |
|---|---|
| **une autre langue que le français** | §5.4. Le pont existe — la prose sort de gabarits, et un gabarit se duplique par langue — mais on ne s'engage pas sur une seconde langue avant que deux instances françaises tournent. |
| **hériter une sévérité** | Principe 1 du cadrage. `dure` et `avertissement` sont des **résultats de mesure** sur un corpus, pas des propriétés de règle. Une instance neuve reçoit tout en `a_mesurer`, et `mesurer` est l'outil du durcissement. Deux exceptions, écrites : la cohérence chemin/catégorie et la concordance des zones générées, où une violation est une incohérence de **structure**. |
| **générer les vues filtrées** | Elles sont un arbitrage éditorial, un par vue. Le manifeste donne un gabarit de colonnes ; les filtres, non. Mesuré : sur le vault réel, les 47 vues sont **un tiers du travail** de migration. |
| **rendre une vue en tableau markdown en profil `nu`** | Ce serait un cinquième générateur, donc un mécanisme, donc hors du périmètre du lot qui a posé les profils. Remontée 3 du lot 10. |
| **importer un corpus existant** | Hors plan, et assumé : c'est le vrai chantier d'amorçage, il dépend entièrement du sujet, et il mérite son propre cadrage. |
| **une interface graphique pour l'entretien** | Hors plan. L'entretien est conversationnel par nature ; un formulaire ramènerait les listes à cocher que les treize refus interdisent. |
| **évaluer une condition de section** | `existe_si:` est du français (« au moins une entrée datée »). Ni le validateur ni le semis ne peuvent l'évaluer ; `mesurer` compte à la place l'**usage réel** de la section. |
| **fabriquer les captures d'écran** | 27 sont déclarées, aucune n'existe. Une capture inventée montrerait une interface qui n'existe pas. |
| **confronter `kit.mode` au disque** | Une instance qui se déclare branchée avec un kit copié dedans passerait inaperçue. Remontée 2 du lot 10. |

---

# 4. Ce qui reste ouvert — et par qui

## 4.1 Les deux décisions qui appartiennent à floSa, et à personne d'autre

**La licence.** `LICENSE` porte **tous droits réservés**, et le fichier écrit
pourquoi : ce n'est pas une décision, c'est l'absence de décision posée dans la
forme la plus **réversible** qui soit. C'est le seul état depuis lequel on peut
aller vers n'importe quelle licence ; l'inverse est faux. Le dépôt n'a pas de
remote et n'a jamais été publié : **rien n'est joué**. La recommandation écrite
au cadrage (§5.7) — et **non prise** — est d'ouvrir le *kit* et de garder fermées
les *méthodes d'entretien*, parce que c'est là qu'est le savoir.

**La propriété de la taxonomie d'un brain construit pour quelqu'un d'autre.**
§5.8, et c'est la plus urgente des deux : le `brain.yml` d'un tel brain contient
l'ontologie d'un métier — ses axes, ses natures de page, ses règles de départage.
C'est un livrable, et c'est en même temps une description d'une organisation. La
recommandation écrite est de le céder et de ne jamais le réemployer, même
« anonymisé » : *un arbre de décision est signant*. **À trancher avant la
première remise, pas après.**

Aucun document du dépôt ne tranche ces deux points, et aucun ne porte de prix,
d'offre, d'argumentaire ni de nom de tiers. Un contrôle du jeu d'épreuve le
vérifie.

## 4.2 La décision qui appartient à floSa sur le DevBrain

La branche `claude/brainkit-lot9-devbrain-8463bb` fait du DevBrain une instance
du kit : `brain.yml` posé, les sept scripts réduits à des ponts, **aucun contenu
de page modifié** (337 briques, 297 notions, 47 vues, 74 hubs, tous intacts).
Elle est **locale et non intégrée**, `main` est restée à `8aaa257`, et rien n'a
été poussé. L'intégrer est une décision, pas une formalité : le journal du vault
en dit la commande.

## 4.3 Les remontées ouvertes, par ordre de coût

Chacune est développée dans le rapport de son lot. Ce qui suit est la liste, pas
l'argument.

**Presque gratuites, et elles évitent une erreur silencieuse :**

1. ~~**Comparer les sha256** de `exemples/devbrain.brain.yml` et du `brain.yml`
   du vault.~~ **FAIT au lot 11**, dans `outils/fidelite.py` (`passe_jumeau`) :
   l'outil sort en 1 si les deux ont divergé, et imprime les deux empreintes.
   *(lot 9 remontée 4, lot 10 remontée 4)*
2. **Un contrôle de socle `mode_du_kit_concorde`**, en `a_mesurer`. *(10 lignes,
   lot 9 remontée 5, lot 10 remontée 2)*
3. **Un contrôle du manifeste d'images**, dans les deux sens — une capture
   déclarée qui manque, un fichier posé que personne ne déclare. *(10 lignes,
   après la relecture devant l'écran)*

**Un peu de travail, et un vrai gain :**

4. **Relire les six sections Obsidian devant l'écran**, et prendre les 16
   captures de portée kit dans le même geste. C'est la **seule** partie du
   livrable dont la justesse repose sur une transcription et non sur une
   exécution. *(≈ 1 heure, lot 10 remontée 1)*
5. **Le genre grammatical d'un libellé d'axe.** « le domaine » se lit, « le
   période » ne se lit pas. Deux issues : un `genre:` facultatif dans `libelles`
   (une question de plus à l'entretien), ou la discipline « aucun article devant
   un libellé » étendue à la prose du semis. *(lot 10 remontée 5)*
6. **Brancher `page_atteignable` sur `racine.pages[].aiguille`.** Le bloc est
   déclaré, le semis l'honore, le validateur lit encore tous les `.md` de la
   racine. C'est un **durcissement**, donc il se mesure d'abord. *(lot 5
   remontée 1)*

**Des chantiers, à ouvrir quand le besoin arrive :**

7. **Le rendu des vues en profil `nu`** — nécessaire dès qu'un brain `nu` a des
   pages. *(lot 10 remontée 3)*
8. **Le seuil de promotion** est dérivé par une loi calibrée sur **deux points**
   (765 pages → 5, 600 pages → 12). Deux points ne font pas une loi ; la
   troisième instance réelle dira si elle tient. *(lot 6 remontée 4)*
9. **L'amorçage.** Un brain à 20 pages ne rend aucun service ; le vault
   d'origine n'a commencé à servir qu'à plusieurs centaines. Le mode lot du skill
   de capture existe pour ça, et il n'a jamais été exercé sur un vrai
   remplissage. *(§5.9)*

---

# 5. Ce qui a vraiment été transposé — et qui ne tient dans aucun fichier

Le cadrage l'annonçait avant d'écrire une ligne de code, et dix lots l'ont
confirmé : ce que ce chantier a produit n'est pas un vault, c'est une
**discipline**. Elle se dit en cinq règles, et aucune n'est du code :

1. **On ne durcit jamais une règle sans avoir compté ses violations.** `mesurer`
   est l'outil de ce comptage, et il refuse de proposer un durcissement sous 30
   pages — parce qu'en dessous, zéro violation ne prouve rien.
2. **On n'assouplit jamais sans écrire le motif.** Le kit refuse un
   `severite: avertissement` sans `motif:`.
3. **On réécrit la règle plutôt que d'ajouter une exception.** Deux des dix
   règles ont été réécrites parce que la mesure a montré que leur formulation
   d'origine était inatteignable.
4. **Rien ne se devine.** Ni un axe, ni une sévérité, ni une identité git, ni un
   chemin de kit, ni le libellé d'un dossier promu. Un champ vide est une
   question ouverte ; une valeur inventée est une faute. Treize refus de deviner
   sont écrits en liste fermée, et le premier — l'identité git — a **trois**
   filets, parce qu'un seul avait déjà lâché.
5. **Une ligne sans objet se déclare sans objet, elle ne se tait pas.** Un
   silence se lit comme un oubli ; une ligne qui dit « sans objet ici, parce que
   ceci » se lit comme une décision.

Et la phrase qui résume le tout, née d'une règle dure sur les hauts de page :
**une fiche vide honnêtement vaut mieux qu'une fiche remplie au jugé.**

---

# 6. Les chiffres, pour situer

| Quoi | Compte |
|---|---|
| lots du plan, tous avec leur critère tenu | **10** *(+1 après clôture)* |
| modules du paquet · lignes | 76 · ~18 900 |
| jeux d'épreuve · lignes de tests et d'outils | 10 · ~5 200 |
| rapports de lot · lignes de conception | 12 · ~10 500 |
| commandes | 8 |
| règles de §10 · contrôles de socle (DevBrain) | 10 · 19 |
| questions d'entretien · refus de deviner | 49 · 13 |
| manifestes complets, dont un contre-exemple | 3 |
| instances | 4 |

## 6.1 Comment tout relancer, en une fois

```bash
uv run schema/valider.py        # le contrat du manifeste
uv run outils/fidelite.py       # la fidélité au vault d'origine
uv run outils/emballer.py       # les documents du dépôt sont-ils à jour
uv run tests/epreuve.py         # la validation
uv run tests/generation.py      # les générateurs
uv run tests/semis.py           # le semis, re-seuiller, freeze
uv run tests/skills.py          # les skills, et leur généricité
uv run tests/mesure.py          # la mesure et ses garde-fous
uv run tests/amont.py           # la fraicheur : derivation, bandeau, regle, refus
uv run tests/entretien.py       # les 49 questions, les 13 refus
uv run tests/emballage.py       # l'emballage : docs, profils, ponts, figeage
```

Deux d'entre eux lisent le vault réel s'il est là. Sur un vault que quelqu'un est
en train d'éditer, `tests/generation.py` peut signaler un écart de zone
générée — ce n'est pas une régression du kit, c'est `--check` qui fait son
travail. Le cas est arrivé pendant le lot 10, et il est documenté là :
`design/10-emballage.md` §6.1.
