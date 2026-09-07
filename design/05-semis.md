# BrainKit — le semis d'instance

> Conversation 46, « BrainKit lot 5, le générateur d'instance », le 2026-09-07.
> Lot 5 du plan de `design/00-cadrage.md` §6. C'est le livrable central du projet :
> la commande qui crée un second brain vierge sur n'importe quel sujet.

## Ce que le lot livre

| Livrable | Contenu |
|---|---|
| `brainkit/semer/` | 10 modules — le plan d'écriture et ses quatre refus, les pré-conditions de manifeste, les pages, la gouvernance, le routeur, les trois hooks, le dépôt, `re-seuiller`, `freeze` |
| `brainkit semer` · `re-seuiller` · `freeze` | trois commandes de plus, mode lecture par défaut pour les trois |
| `racine:` | un bloc de manifeste et sa part de schéma — l'arbitrage que le lot 4 renvoyait |
| `tests/semis.py` | sept scénarios, dont le cas négatif |
| deux instances semées | HistoBrain vierge, et DevBrain vierge pour le contrôle de généricité — **hors de DevBrain, hors de BrainKit, non versionnées** |

Ce que le lot **ne** livre **pas**, et le dit : les trois skills ne sont pas
instanciés — leur **emplacement** est posé, avec le README qui nomme les trois et
renvoie au lot 7. Poser un skill à moitié serait pire que ne pas en poser : il
serait chargé, et il mentirait.

---

# 1. Le critère d'acceptation, et comment il est tenu

## 1.1 HistoBrain vierge, mesuré

```
uv run brainkit semer --manifeste exemples/histobrain.brain.yml \
                      --dans ~/Documents/BrainKit-essais/histobrain --ecrire
```

| Ce qui est écrit | Compte |
|---|---|
| pages `role: hub` | **11** — 8 périodes, `Controverses/`, `Méthodes/`, `Chronologies/` |
| **toute autre page** | **0** |
| gabarits `Templates/` | 6 — un par rôle |
| gouvernance | 3 — la taxonomie générée, le vocabulaire de tags vide, la table de couleurs |
| routeur | 2 — `CLAUDE.md`, `CLAUDE-enrichir.md` |
| racine | 2 — `Home.md`, `Inbox.md` |
| espace agent | 4 — le backlog, le journal du lot 1, le README des scripts, celui des sessions |
| hooks et dépôt | 5 — les trois hooks, `.gitignore`, `.gitattributes` |
| manifeste | 1 — `brain.yml` à la racine, copié à l'identique |
| dossiers | 23 |
| **total semé** | **44 fichiers** |
| artefacts **dérivés**, posés par les générateurs | 3 — `brain-index.json`, `brain-index.md`, `liens.md` |
| **total suivi par git** | **47** |

## 1.2 Les cinq vérifications, et leur résultat

| # | Vérification | Résultat |
|---|---|---|
| 1 | `brainkit valider` — violations **dures** | **0** |
| 2 | `brainkit valider` — avertissements **et** à-mesurer | **0** |
| 3 | `brainkit generer --check` juste après le semis | **0 écart, 0 refus**, code 0 |
| 4 | pages de démonstration, exemples, lorem | **aucun** — 11 pages, 11 hubs |
| 5 | `re-seuiller` sur l'instance vierge | **aucun `git mv`**, et il le dit |

La vérification 2 mérite d'être isolée, parce qu'elle est plus forte que ce que
le lot demandait. Le critère écrit était « aucun avertissement **injustifié** » ;
le résultat est **zéro avertissement du tout**. Ce n'est pas de la chance : sur
un vault à zéro page d'unité, tout avertissement serait injustifié par
construction — il porterait sur une page que personne n'a écrite. Un
avertissement au semis aurait donc signalé un défaut du **kit**, pas du vault.
C'est un contrôle qui ne peut passer que si le semis est juste, et c'est pour ça
qu'il est dans le jeu d'épreuve avec cette formulation.

## 1.3 Les vingt titres du test à blanc

Les vingt titres cités en passe 2.1 de l'entretien (`00-cadrage.md` §4.1) sont
dans `Inbox.md`, en cases à cocher, et **pas une de ces pages n'est écrite**.
C'est le point exact qui distingue l'entretien du remplissage (§3.4) : ils ont
servi à **induire** la taxonomie — c'est eux qui ont fait sortir huit paquets
rangés par période, et le préfixe `transversal` à la vingtième — ils n'ont pas
été capturés.

Ils vivent dans le manifeste, sous `racine.pages[].amorce`, et c'est délibéré :
ce que l'entretien a récolté ne doit pas se perdre entre l'entretien et le
premier remplissage.

## 1.4 Le dépôt de l'instance

```
f31f569 | floSa <florian_horellou@laposte.net> | semis : HistoBrain — l'instance vierge, un hub par dossier
```

- identité en config **locale**, prise dans `git.identite` du manifeste ;
- `core.hooksPath = .githooks`, posé par le semis ;
- branche `main`, prise dans `git.branche_principale` ;
- `git status` vide juste après le semis.

Le commit initial **traverse les trois hooks** : c'est le test, et il n'est pas
simulé. Les trois ont aussi été éprouvés à l'envers, sur l'instance semée :

| Tentative | Résultat |
|---|---|
| message portant `Co-Authored-By:` | **refusé** par `commit-msg` |
| `git -c user.email=…@aosis.net commit` | **refusé** par `pre-commit` |
| commit nu, identité locale | **passe** |

Le troisième compte autant que les deux premiers : un garde-fou qui refuse tout
ne prouve rien.

---

# 2. Ce que le semis écrit, et depuis quoi

La table de §3.3 du cadrage, confrontée à ce qui est réellement posé.

| §3.3 annonce | Écrit ? | Depuis quoi |
|---|---|---|
| l'arbre des dossiers de l'axe de rangement, avec un hub à zéro entrée | oui | `axes.rangement.prefixes[]` |
| les dossiers des rôles `range_par: role`, avec leur hub | oui | `roles[].dossier` |
| les dossiers des axes transverses, **avec un hub par valeur** | **le dossier seulement** | `axes.transverses[]` — cf. arbitrage 3 |
| un gabarit par rôle dans `Templates/` | oui | `roles[].champs` et `roles[].corps` |
| la taxonomie générée | oui | `axes` |
| les vocabulaires vides, avec en-tête et règle | oui | `vocabulaires` |
| les deux validateurs et les quatre générateurs, **branchés** | oui | `brain.yml` à la racine + `AI/scripts/README.md` |
| les trois skills, instanciés | **emplacement seulement** | lot 7 |
| `CLAUDE.md` + contexte de mode, **règle d'identité git en tête** | oui | `brain`, `git`, `roles[].protege`, `frontieres_d_ecriture` |
| `.githooks/` (les trois) + `core.hooksPath` + identité locale | oui | `git` |
| la table de couleurs du graphe et son étape d'installation | oui | `graphe` |
| `Home.md`, `Inbox.md`, `AI/` | oui | `racine`, `agent` |
| `INSTALL.md` et les guides | **non** | lot 10 (`design/00-cadrage.md` §6) |
| le journal du lot 1, vide, avec sa section *Remontées* | oui | — |

## 2.1 Le hub semé, et pourquoi sa zone AUTO n'est pas vide

Un hub semé porte déjà sa zone AUTO **remplie comme le générateur la remplirait
sur un dossier vide** :

```markdown
<!-- AUTO:START -->
*(dossier vide)*
<!-- AUTO:END -->
```

et, pour un hub de ralliement :

```markdown
<!-- AUTO:START -->
*(aucune page `role: chronologie`)*
<!-- AUTO:END -->
```

Les deux lignes sont lues dans la **même** table de prose que celle du générateur
(`hubs.dossier_vide`, `hubs.aucune_page`). Elles ne peuvent donc pas diverger :
une surcharge `genere.prose.hubs.dossier_vide` les change d'un coup. C'est le
même principe que le manifeste applique partout — une seule source, jamais deux
qui décrivent la même chose.

## 2.2 Le gabarit d'un rôle

Un `Templates/Gabarit - <libellé>.md` par rôle. Le préfixe n'est pas décoratif :
un gabarit nommé d'après son rôle (`Notion.md`) porterait le nom d'une page
probable du vault, et la convention de wikilink **nu** ne résoudrait plus de
façon déterministe. `Templates/` étant hors du périmètre du validateur, la
violation ne serait **pas signalée** — ce qui est pire, pas mieux.

Le frontmatter reprend `requis` puis `autorises`, **dans l'ordre du manifeste**.
Le corps reprend `corps[]`, avec le genre de chaque section rendu :
`decision` → un tableau à deux colonnes nommées, `etiquetee` → ses étiquettes
en puces, `liste_liens` → le champ qui l'adosse, `conditionnelle` → un
avertissement au-dessus du titre disant de la **supprimer** si elle ne se
remplit pas.

---

# 3. Les arbitrages

## 3.1 La porte d'entrée du vault — le bloc `racine:` *(arbitrage demandé)*

**Le lot 4 avait établi ce que `Home.md` n'est pas** : un artefact dérivé. Aucun
des quatre générateurs ne le produit, et le DevBrain n'a aucun script qui
l'écrive. C'est un artefact de **semis** — écrit une fois, puis édité à la main
comme le corps d'un hub — et le régénérer effacerait ce que floSa y a mis.

**Ce qui restait n'était donc pas un besoin de génération, c'était un besoin de
déclaration** : le validateur lit **tout** `.md` de la racine pour son test
d'atteignabilité, sans qu'aucun champ ne dise lesquels aiguillent. Un brouillon
posé à la racine élargissait silencieusement l'atteignabilité de tous les hubs de
premier niveau — ceux qui n'ont pas de parent, et que seule la porte d'entrée
cite.

**Tranché : le bloc `racine:`, avec trois choses et non une.**

```yaml
racine:
  porte_d_entree: Home.md
  pages:
    - { fichier: Home.md,  titre: Accueil, aiguille: true,  role_editorial: porte }
    - { fichier: Inbox.md, titre: Inbox,   aiguille: false, role_editorial: capture,
        amorce: ["source : Thucydide, La Guerre du Péloponnèse", …] }
```

| Champ | Ce qu'il porte | Pourquoi il est là |
|---|---|---|
| `porte_d_entree` | **le** fichier qui cite les hubs de premier niveau | c'est lui, et lui seul, qui rend les hubs sans parent atteignables |
| `pages[]` | **tous** les `.md` que le semis pose à la racine, et aucun autre | ce qui n'est pas déclaré n'est pas semé |
| `aiguille` | true = la page compte pour l'atteignabilité | **c'est la moitié qui manquait** |
| `amorce` | les items à traiter, en cases à cocher | ce que l'entretien a récolté ne doit pas se perdre |

**`aiguille: false` est la partie qui justifie le bloc.** Le lot 4 recommandait
« un bloc `racine:` avec `porte_d_entree:` et la liste des pages d'aiguillage ».
Une liste de pages d'aiguillage seule aurait redit ce que le validateur suppose
déjà — *tout `.md` de la racine aiguille* — au lieu de le corriger. Une inbox vit
à la racine **sans** aiguiller, et une page qu'elle mentionnerait ne doit pas
devenir atteignable pour autant. Sans ce champ, la déclaration aurait été
décorative.

**Ce que le lot ne fait pas, délibérément : brancher `page_atteignable` sur la
déclaration.** Le validateur continue de lire `racine.glob("*.md")`. Changer le
périmètre d'une règle existante est du **durcissement**, et le durcissement est
le lot 8 — l'interdiction du lot 5 est explicite : *aucune règle de validation
nouvelle, aucun changement de sévérité*. La déclaration existe, le semis
l'honore (il n'écrit à la racine que ce que `pages[]` déclare), et la remontée 1
dit ce qui reste à câbler.

**Le remplissage DevBrain est une transcription, pas une prescription.** Le vault
réel porte neuf `.md` à sa racine ; deux sont des pages, une seule aiguille. Les
sept autres — `README`, `INSTALL`, `CHANGELOG`, `CONTRIBUTING` et les
trois `CLAUDE*` — sont des documents de dépôt : ils ne citent aucun hub, donc
`page_atteignable` ne les lit pour rien.

## 3.2 L'arbre naît **plat**

Un dossier par préfixe déclaré, et **rien en dessous**. Les 17 sous-valeurs
déclarées par HistoBrain (Rome, Époque féodale, Guerre froide…) n'ont **pas** de
dossier au semis.

La raison est mécanique et non esthétique : la promotion d'une sous-valeur se
calcule sur une population de pages (`chemins.promotions`) qui vaut **zéro** le
jour du semis. Poser d'avance les dossiers des sous-valeurs déclarées créerait
des dossiers que `dossier_attendu()` ne rendrait pas — donc des dossiers que
`re-seuiller` proposerait aussitôt de défaire, et des hubs sans population que
`page_atteignable` obligerait à citer depuis la porte d'entrée.

La taxonomie générée porte la table des sous-valeurs déclarées, avec la phrase
qui l'explique : *un sous-dossier n'existe que promu — 12 pages ou plus.*

## 3.3 Aucun hub d'axe transverse n'est semé, seulement son dossier

**C'est le seul point où ce lot contredit §3.3 du cadrage, et il le fait
sciemment.** Le cadrage annonce « les dossiers des axes transverses, **avec un
hub par valeur** ». Le lot 4 a mesuré et écrit le contraire, dans
`generer/hubs.py` :

> *Une valeur déclarée que personne ne porte ne produit AUCUN hub : le vault
> n'aurait rien à y montrer, et une page vide dans un graphe est un nœud de plus
> qui ne rassemble rien.*

La règle de départage entre les deux est celle du prompt de ce lot : **en cas de
désaccord, le livrable le plus récent a raison.**

Semer les quatorze hubs de HistoBrain (7 thèmes + 7 espaces) poserait quatorze
pages qu'aucun générateur ne régénérerait, qu'il faudrait citer depuis la porte
d'entrée pour qu'elles soient atteignables, et qui n'auraient rien à montrer.

Le **dossier**, lui, est semé — avec un `.gitkeep`, git ne suivant aucun dossier
vide — parce qu'il dit **où** ces hubs naîtront. Et ils naîtront tout seuls :
`hubs._hub_neuf` sait créer un hub transverse absent, avec le frontmatter que le
manifeste **exige** du rôle hub et rien de plus, et c'est éprouvé depuis le lot 4.

## 3.4 Les artefacts dérivés sont posés par les **générateurs**, pas par le semis

Le semis n'écrit ni `AI/index/`, ni la carte des liens, ni un bandeau. Il écrit
ce qui s'écrit **une fois**, puis appelle `genere_tout(…, mode=ECRIRE)` sur le
vault qu'il vient de poser.

Deux conséquences, et la seconde est le critère d'acceptation :

1. **Il n'existe pas deux codes qui composent le même artefact.** C'est le défaut
   E4 de l'inventaire — deux sources décrivant le même gabarit, dont l'une prend
   du retard — et le manifeste existe pour le supprimer.
2. **Le semis est à son point fixe par construction.** Un `generer --check` lancé
   juste après est silencieux, mesuré : 14 artefacts, 0 écart, code 0. *Un semis
   qui n'est pas déjà à son point fixe est un semis faux*, et la seule façon de
   le garantir est de laisser les générateurs poser leurs propres artefacts.

## 3.5 Un gabarit ne liste **pas** les valeurs d'un champ énuméré

Le premier jet écrivait `categorie:   # une valeur de : antiquite, medieval, …`.
Retiré. C'est le refus n° 3 de l'entretien (§3.5) appliqué au gabarit : *jamais
de liste à cocher*. Une liste sous les yeux fait choisir la valeur qui ressemble
le plus ; l'arbre de décision fait répondre à des questions **fermées**, dans un
**ordre strict**, et l'ordre **est** la décision de conception.

Le gabarit renvoie donc à l'arbre :

```yaml
categorie:       # 25 valeurs — dérouler l'arbre de décision de `Documentation/periodes/taxonomie.md`
```

## 3.6 Les hooks lisent l'**identité attendue**, pas un domaine

M2 de l'inventaire classait `pre-commit` / `pre-push` PARAMÉTRABLE avec un motif
précis : **la polarité peut s'inverser**. Un brain de domaine client, vendu chez
un employeur, est un dépôt **pro** — et c'est alors l'adresse **perso** qu'il
faut refuser.

Les hooks générés portent donc deux contrôles au lieu d'un :

| # | Contrôle | Polarité |
|---|---|---|
| 1 | l'identité **effective** du commit == `git config --local user.email` | aucune — vaut pour un dépôt perso comme pro |
| 2 | l'adresse n'appartient à aucun `git.domaines_refuses` | déclarée dans le manifeste |

Le premier rend le second presque redondant, et c'est voulu :
`domaines_refuses: []` laisse un hook qui protège encore. Le second est gardé
parce qu'il **nomme le danger**, ce qui fait un message qui explique au lieu de
constater.

`git var GIT_AUTHOR_IDENT` reste la seule lecture employée : elle résout la
config locale, la globale, l'environnement **et** l'override `-c user.email=…`.
Lire `git config user.email` raterait les trois dernières.

Le **garde-fou du garde-fou** est repris tel quel — `pre-commit` refuse de
committer si `commit-msg` n'est pas installé sous le `core.hooksPath` effectif,
avec son détail Windows (git juge un hook exécutable dès qu'il commence par
`#!`, `test -x` ne suffit pas).

## 3.7 `core.hooksPath` est posé par le **semis**, pas laissé à l'installation

Dans le DevBrain, les hooks sont versionnés mais leur activation est manuelle
(`INSTALL.md` §3.5). Le lot 6 de sa migration a mesuré ce que ça coûte : cinq
commits passés parce que rien ne cherchait. Une instance neuve n'a aucune raison
de naître avec ses garde-fous éteints.

---

# 4. `re-seuiller` — changer le seuil est une **migration**

## 4.1 Ce qu'elle fait

`brainkit re-seuiller --vault <d> --seuil <n>` recalcule les promotions avec le
nouveau seuil, compare, et rend :

- les **promotions** et les **dépromotions** de sous-valeurs ;
- la liste des pages à déplacer, **une commande `git mv` par page** ;
- les hubs à **créer** pour les dossiers nouvellement promus ;
- les hubs qui restent **sans dossier** après la migration ;
- les sous-valeurs au-dessus du seuil **sans `libelle:` déclaré** — le nom d'un
  dossier ne se devine pas.

## 4.2 Trois règles, aucune négociable

1. **`git mv`, jamais suppression + création.** Un déplacement par `rm` + `add`
   perd l'historique de la page, et l'historique est ce qui distingue un vault
   d'un dossier de fichiers.
2. **Le mode par défaut n'écrit rien.** `--appliquer` se demande. Sur un arbre de
   700 pages, la réponse à « ce que ça ferait » tient rarement dans ce qu'on
   imaginait.
3. **Une dépromotion ne supprime rien.** Un sous-dossier qui retombe sous le
   seuil rend ses pages au parent, et son hub devient orphelin. Le hub n'est pas
   effacé : il est **signalé**. « Jamais sans accord » vaut pour toute
   suppression de page, et une migration automatique n'est pas un accord.

`--appliquer` **refuse sur un arbre de travail sale** : un `git mv` mêlé à des
modifications non committées ne se défait pas, et une migration dont on ne peut
pas sortir n'est pas une migration.

## 4.3 Ce que l'opération crée quand même

Le hub d'un dossier **nouvellement promu**. Sans lui, `hub_par_niveau` — règle
**dure** — serait violée dès la fin de la migration, et l'opération livrerait un
vault rouge. Ce n'est pas une exception à la règle 3 : on ne supprime rien, on
pose la page que la structure exige.

## 4.4 Mesuré

| Cas | Résultat |
|---|---|
| HistoBrain vierge, seuil 12 → 5 | **0 `git mv`**, et l'opération le dit |
| HistoBrain vierge, seuil 12 → 3 | idem |
| `tests/genere-vert`, seuil 2 → 3 | 1 dépromotion (`antiquite/rome`), **3 `git mv`**, 1 hub orphelin signalé |
| le même, appliqué | `git status` voit **3 `R`** — des renommages, pas des suppressions + créations |
| le même, sur un arbre sale | **refusé**, avec les lignes fautives |

**Le jeu d'épreuve a corrigé une attente fausse, et le fait vaut d'être écrit :**
la dépromotion déplace **trois** pages et non deux — la page `fonction: vue` du
dossier suit, alors qu'elle ne **pèse** pas sur le seuil. Les deux notions ne se
confondent pas : `pese_sur_le_seuil: false` dit « ne compte pas dans la décision
de promotion », **pas** « ne se range pas ». Une vue restée dans un dossier
dépromu serait une page hors de son dossier dérivé, donc une violation de
`chemin_categorie`.

---

# 5. `freeze` — l'instance figée

## 5.1 Pourquoi ce mode n'est pas optionnel

§5.1 du cadrage. Le kit est un **générateur**, pas un dépôt-gabarit qu'on clone :
le jour du clone, le code fourche, et avec trois instances chaque correction se
réapplique trois fois à la main — la troisième divergera. Une instance ne
contient donc que son contenu, son `brain.yml`, ses documents générés et ses
hooks. **Pas de code.**

Sauf que la spécialité de floSa est l'**on-prem**. Un vault livré chez un
industriel ne pourra pas installer un outil depuis internet, et une instance qui
ne sait pas se valider toute seule n'est pas livrable.

## 5.2 Ce que `freeze` copie

| Quoi | Où |
|---|---|
| le paquet `brainkit/` — 38 modules, les deux validateurs, les quatre générateurs, le semis | `AI/scripts/brainkit/` |
| trois lanceurs à en-tête **PEP 723** (`valider.py`, `generer.py`, `semer.py`) | `AI/scripts/` |
| `FIGE.md` — ce qui est copié, ce qui est perdu, comment revenir en arrière | `AI/scripts/` |
| `kit.mode: branche` → `fige` | `brain.yml` |

**42 fichiers**, mesurés sur HistoBrain. Les lanceurs résolvent `brain.yml` et la
racine du vault tout seuls : `uv run AI/scripts/valider.py` suffit, sans rien
installer.

La bascule de `kit.mode` se fait par **édition de ligne**, jamais par relecture +
réécriture du YAML : relire et réécrire perdrait tous les commentaires, donc tous
les `motif:`, qui sont la moitié de la valeur d'un manifeste. Vérifié par le jeu
d'épreuve — les `motif:` survivent, et un `git diff` montre **une** ligne changée.

## 5.3 Ce que `freeze` **perd**

| Ce qui reste dehors | Conséquence |
|---|---|
| les correctifs à venir | **l'instance ne recevra plus rien** — un défaut corrigé dans le kit reste chez elle |
| `schema/brain.schema.json` et son validateur | un `brain.yml` modifié ne se vérifie plus contre le contrat |
| `outils/fidelite.py` et les jeux d'épreuve | aucun moyen de prouver, **sur place**, que le kit figé se comporte comme le kit |
| la comparabilité | deux instances figées à deux dates ne portent pas le même code, et rien ne le dit à l'ouverture |

C'est écrit dans l'instance elle-même, pas seulement ici : `AI/scripts/FIGE.md`.
Une instance figée qui ne saurait pas qu'elle l'est serait le pire des deux
mondes.

**Il n'y a pas d'`unfreeze`, et c'est délibéré** : un dégel silencieux ferait
cohabiter deux versions du même code sans que personne ne le sache. `FIGE.md`
dit comment rebrancher à la main.

## 5.4 Ce que `freeze` refuse

- un dossier qui ne porte pas de `brain.yml` — figer un dossier quelconque n'a
  aucun sens ;
- une instance dont `kit.mode` vaut déjà `fige` — refiger la ferait diverger
  davantage, pas moins.

**Vérifié** : l'instance figée reste **verte** aux deux validateurs.

---

# 6. Le contrôle de généricité — DevBrain semé, comparé au vault réel

C'est la répétition du lot 9 à blanc, **sans toucher au vault**. DevBrain est
semé depuis `exemples/devbrain.brain.yml` dans un dossier d'essai, et sa
structure vide est comparée à l'arbre réel en **lecture seule**.

## 6.1 Le résultat, chiffré

| Mesure | Instance semée | DevBrain réel | Écart |
|---|---|---|---|
| **hubs de premier niveau** | **23** | **23** | **0** |
| dossiers de premier niveau | 27 | 29 | 2 |
| dossiers portant au moins un `.md` | 26 | 27 | 1 |
| gabarits dans `Templates/` | 6 | 5 | 1 |
| pages `.md` (hors `.git`, `.claude`) | 43 | 828 | 785 |
| violations dures du validateur | 0 | 0 | 0 |
| écarts `generer --check` | 0 | (hors sujet) | — |

**Les 23 hubs de premier niveau sont identiques, nom pour nom** : les 20 dossiers
de domaine, `Patterns/`, `Rules/`, `Comparatifs/`. C'est le résultat que le
contrôle cherchait — un manifeste transcrit d'un vault réel, resemé à vide,
redonne **exactement** l'ossature de ce vault.

## 6.2 Les quatre écarts, expliqués

| # | Écart | Explication |
|---|---|---|
| 1 | `Métiers/` porte 6 hubs dans le vault réel, 0 dans l'instance | **arbitrage 3.3.** Aucune page ne porte encore de valeur de `domaines:`, donc aucun hub transverse ne naît. Le premier `build_mocs` après la première capture les créera lui-même. |
| 2 | `Projects/` absent de l'instance | scaffold vide du DevBrain, qu'**aucune déclaration du manifeste ne demande**. Il est dans `genere.non_pages`, ce qui dit « ne pas le lire », pas « le créer ». Le créer depuis `non_pages` serait faux : cette liste contient aussi `.git` et `.obsidian`. |
| 3 | `docs/` absent de l'instance | les guides générés — **lot 10** (`00-cadrage.md` §6 : *`INSTALL.md` généré, les guides générés*). Hors du périmètre de ce lot. |
| 4 | 6 gabarits contre 5, et aucun nom commun | **c'est le constat E4 qui se voit**. Le vault réel porte `Service-Dev`, `Outil-Dev`, `Concept-Wiki`, `Pattern`, `Rule` — cinq fichiers **périmés**, tenus à la main, dont deux décrivent le même rôle (`brique`) et dont aucun ne couvre `comparatif`. L'instance en porte **six, un par rôle, générés**. L'écart n'est pas une régression : c'est la dette que le kit supprime. |

L'écart de 785 pages est le **contenu**, et c'est tout l'intérêt : un brain
vierge est vide.

---

# 7. Ce que le semis refuse

## 7.1 Les quatre situations que le plan d'écriture refuse

`brainkit/semer/plan.py` est le seul module du paquet capable d'écrire :

```bash
grep -rnE 'write_text|write_bytes|mkdir|copytree|copy2' brainkit/semer/
# -> plan.py, plus figer.py qui copie le kit (et le declare)
```

| Refus | Ce qu'il évite |
|---|---|
| la cible existe et n'est pas vide | écraser un vault qu'on croyait absent |
| la cible vit **sous le dépôt du kit** | versionner une instance d'essai dans BrainKit |
| la cible vit **sous un dépôt git** | semer dans DevBrain, ou dans n'importe quel dépôt |
| la cible vit **sous un vault** (`brain.yml` ou `.obsidian` chez un parent) | semer un brain à l'intérieur d'un autre |

Les deux derniers sont volontairement formulés **sans nommer DevBrain**. Un
garde-fou qui interdit un chemin par son nom protège **un** chemin ; un garde-fou
qui interdit une **situation** protège tous les chemins qui s'y trouveront un
jour — y compris le dépôt d'un client qu'on n'a pas encore rencontré.

## 7.2 Le cas négatif — un manifeste incomplet est refusé, pas semé à moitié

`brainkit/semer/exigences.py` porte la passe qui manquait entre le contrat du
lot 1 et le semis. **Le schéma dit si un manifeste est bien formé ; il ne dit pas
s'il est semable**, et les deux ne se recouvrent pas : un rôle `range_par: role`
sans `dossier:` satisfait le schéma — parce qu'un manifeste peut n'en avoir aucun
— et bloque le semis, parce qu'il faudrait inventer un nom de dossier.

Tous les manques sont rendus **d'un coup**, avant que le plan d'écriture existe.
Un semis qui poserait douze dossiers puis s'arrêterait sur le treizième
laisserait un vault à demi écrit, dont les deux validateurs diraient n'importe
quoi.

Ce que la passe contrôle : l'identité git, l'existence et la complétude du rôle
hub (y compris **ses balises de zone AUTO** et le fait que ses champs requis
soient tous remplissables par le semis), le dossier de chaque rôle `range_par:
role` et de chaque hub de ralliement, les préfixes de l'axe de rangement et leur
dossier, le seuil, le préfixe transversal quand l'axe n'est pas exclusif, le
champ et le dossier de chaque axe transverse **plus la contrainte de nommage de
la rupture 4** (aucun dossier d'axe transverse ne peut porter le nom d'un dossier
de l'arbre), le bloc `racine:`, la racine de l'agent, la présence de `Templates`,
`Documentation` et de la racine de l'agent dans `genere.non_pages`, la
**lisibilité** de chaque vocabulaire fermé, et la table de couleurs du graphe.

Éprouvé sur quatre amputations, en mémoire, sans toucher un fichier : chacune est
refusée, le refus **nomme** le champ, et le dossier cible **reste inexistant**.

---

# 8. Comment rejouer

```bash
# le semis, en mode LECTURE — ne pose pas un octet
uv run brainkit semer --manifeste exemples/histobrain.brain.yml --dans <dossier>

# pour de bon
uv run brainkit semer --manifeste exemples/histobrain.brain.yml --dans <dossier> --ecrire

# les deux validateurs et les generateurs sur l instance
uv run brainkit valider --manifeste exemples/histobrain.brain.yml --vault <dossier>
uv run brainkit generer --manifeste exemples/histobrain.brain.yml --vault <dossier>

# re-seuiller — simulation, puis application sur un arbre PROPRE
uv run brainkit re-seuiller --vault <dossier> --seuil 5
uv run brainkit re-seuiller --vault <dossier> --seuil 5 --appliquer

# freeze — simulation, puis copie
uv run brainkit freeze --vault <dossier>
uv run brainkit freeze --vault <dossier> --ecrire

# le jeu d epreuve du lot 5 — sept scenarios
uv run tests/semis.py

# les lots anterieurs, inchanges
uv run tests/epreuve.py          # lot 3
uv run tests/generation.py       # lot 4
uv run schema/valider.py         # lot 1
uv run outils/fidelite.py        # lot 2
```

Un seul module du paquet écrit :

```bash
grep -rnE 'write_text|write_bytes|mkdir|copytree' brainkit/semer/
```

Et l'identité git ne se devine nulle part :

```bash
grep -rnE "GIT_AUTHOR|GIT_COMMITTER|--author|-c user\." brainkit/semer/
# -> le docstring de depot.py, et les hooks generes qui l INTERDISENT
```

---

# 9. Remontées

## 1. `page_atteignable` ne lit pas encore `racine:`

Le bloc est déclaré, le schéma le porte, le semis l'honore — il n'écrit à la
racine que ce que `pages[]` déclare. **Le validateur, lui, lit toujours
`racine.glob("*.md")`.**

Ce n'est pas un oubli : brancher la règle sur `racine.pages[].aiguille` change le
**périmètre d'une règle existante**, et l'interdiction du lot 5 est explicite —
*aucune règle de validation nouvelle, aucun changement de sévérité*. Un brouillon
posé à la racine élargit donc encore l'atteignabilité.

**À câbler au lot 8**, avec la mesure : sur DevBrain, neuf `.md` à la racine dont
un seul aiguille, et il faut compter combien de pages perdraient leur
atteignabilité si les huit autres cessaient de compter. Si la réponse est zéro,
le durcissement est gratuit.

## 2. La clé `scanned` : un second cas, plus net que le premier

La remontée 1 du lot 4 disait que `scanned` publie tout dossier de premier niveau
qui n'est pas dans `genere.non_pages`, y compris ce qui n'est pas suivi par git.
**Le semis fournit un second cas, et il est plus propre à lire.** Sur HistoBrain
vierge, `scanned` vaut :

```
['.githooks', 'Antiquité', 'Chronologies', 'Controverses', 'Espaces', 'Moyen Âge',
 'Méthodes', 'Préhistoire', 'Révolutions et empires', 'Thèmes', 'Transversal',
 'XXe siècle', 'Âge industriel', 'Époque moderne']
```

Trois de ces quatorze entrées portent **zéro page** : `.githooks` (un dossier
d'outillage), `Thèmes` et `Espaces` (les dossiers d'axe transverse, vides par
l'arbitrage 3.3).

**Ce que ça change pour le lot 9 :** rien sur la reproductibilité — tout ce que
`scanned` liste ici est **suivi par git**, donc deux machines produisent le même
catalogue. Mais la clé est désormais fausse **par construction et dès le premier
jour**, pas seulement en présence d'un dossier parasite. Le vault réel le montre
d'ailleurs déjà : son `scanned` committé porte `.githooks` **et**
`obsidian_outer_backup_20260907`.

La recommandation du lot 4 tient, et la première de ses deux issues gagne :
**`scanned` se restreint aux dossiers qui portent au moins une page.** Ne rien
faire laisserait chaque instance neuve naître avec un catalogue qui annonce
quatorze dossiers balayés dont trois ne le sont pas.

**Non corrigé ici** : c'est le générateur d'index, et l'interdiction du lot est
explicite — *aucune « amélioration » d'un générateur*. Le lot 9 est le premier
moment où changer la clé ne coûte pas le critère d'un lot antérieur.

## 3. `valider` et `generer` n'ont pas de défaut d'instance

`brainkit semer`, `re-seuiller` et `freeze` résolvent `<vault>/brain.yml` quand
`--manifeste` n'est pas donné. `valider` et `generer` ne le font pas : leur
défaut reste `exemples/devbrain.brain.yml` et `../DevBrain`, qui sont des défauts
de **développement du kit**, pas d'usage.

Conséquence pour un utilisateur d'instance : les deux commandes qu'il tapera le
plus souvent exigent deux options, et une faute de frappe sur `--manifeste`
validerait son vault contre le manifeste d'un **autre brain** — silencieusement,
avec un verdict qui n'aurait aucun sens.

**Non corrigé** : changer un défaut de `generer` est un changement de
comportement d'un générateur, et le critère d'acceptation du lot 4 se rejoue sur
ces défauts. **À trancher au lot 10** (l'emballage), avec la même règle que
`semer` : `./brain.yml` s'il existe, jamais un exemple du kit.

## 4. `Projects/` n'est déclaré nulle part

Le DevBrain porte un `Projects/` — « log des projets en cours, scaffold, vide
pour l'instant » — et son manifeste le nomme uniquement dans `genere.non_pages`,
c'est-à-dire dans la liste de ce qu'il **ne faut pas lire**. Le semis ne le crée
donc pas, et c'est cohérent : `non_pages` contient aussi `.git` et `.obsidian`.

Si un scaffold de ce type doit exister dans toute instance, il lui faut une
déclaration à lui — la plus proche serait une entrée de `racine:` ou un bloc
frère de `agent:`. **À trancher avec le lot 6** (l'entretien), qui saura s'il
faut poser la question ou pas : c'est exactement le genre de dossier qu'un
utilisateur ne demandera jamais et regrettera de ne pas avoir.

## 5. La section conditionnelle d'un gabarit n'a pas de forme mesurable

`roles[].corps[].genre: conditionnelle` porte un `existe_si:` en **français**
(« au moins une entrée datée », « la notion porte une controverse
historiographique »). Le gabarit le rend en commentaire, et c'est tout ce qu'on
peut en faire : ni le validateur ni le semis ne peuvent l'évaluer.

Le manifeste HistoBrain écrit lui-même ce qu'il faudrait : *le kit doit MESURER
l'usage de ce qu'il génère — une section qui n'existe sur aucune page au bout de
N pages est une section à supprimer du gabarit, pas à laisser « au cas où »*. La
mesure du DevBrain est éloquente : **zéro** entrée en dix-huit mois dans la
section `## Retours` de ses 337 briques.

**À traiter au lot 8**, qui est le lot de la mesure. Ce n'est pas une règle de
validation : c'est un rapport sur le gabarit lui-même.

## 6. Le semis ne vérifie pas `kit.version`

§5.1 du cadrage : *`brain.yml` porte la version du kit avec laquelle l'instance a
été générée. Le kit refuse de tourner sur un manifeste d'une version qu'il ne
connaît pas, **dans les deux sens**.* Le semis lit `kit.version` pour l'écrire
dans `AI/scripts/README.md`, mais il ne la **compare** à rien.

C'est sans conséquence aujourd'hui — une seule version existe — et ça en aura le
jour du premier correctif diffusé. **À traiter au lot 10**, avec le test croisé
branché/figé, qui est le premier endroit où deux versions du kit coexistent
vraiment.

---

# 10. Ce qui reste au lot 6

- **L'entretien produit ce que le semis consomme.** Le bloc `racine:` est
  désormais dans cette liste, et il porte une question de plus à poser : *quels
  fichiers vis-tu à la racine, et lequel cite tes hubs ?* La réponse par défaut —
  une porte et une inbox — est celle des deux remplissages, mais elle ne se
  devine pas plus qu'une autre.
- **`racine.pages[].amorce` est la sortie de la passe 2.1.** Les vingt titres que
  l'entretien fait citer pour induire la taxonomie ont maintenant une place
  déclarée où atterrir. L'entretien n'a plus à choisir quoi en faire : il les
  écrit là, et le semis les pose en cases à cocher.
- **Les quatre refus du plan d'écriture sont des messages, pas des exceptions.**
  L'entretien peut les rejouer avant de proposer un chemin : `seme()` en mode
  lecture répond en une milliseconde et n'écrit rien.
