# BrainKit — cadrage

> Conversation 41, « cadrage BrainKit », le 2026-09-07. Document de **cadrage** :
> aucun vault, aucun script, aucun gabarit n'est écrit ici. Ce qui est écrit ici est
> ce qu'il faudra écrire, dans quel ordre, et ce qui ne se transposera pas.

## Le problème, en une phrase

Le DevBrain marche. Il marche sur **un** sujet — le dev — et **rien dans son
mécanisme n'est propre au dev**, sauf ses valeurs. BrainKit est l'opération qui
sépare les deux : la mécanique d'un côté, les valeurs de l'autre, et un entretien
qui produit les secondes pour n'importe quel sujet.

Le sujet « histoire » sert de banc d'essai dans tout ce document. Ce n'est **pas**
une thématique à livrer : c'est le sujet le plus éloigné du dev qui reste crédible
(des sources plutôt que des logiciels, des dates plutôt que des versions, des
controverses plutôt que des alternatives). S'il passe, un domaine client passe.

## Ce qui est établi avant de commencer

État du DevBrain au 2026-09-06, migration v3 close : 338 briques, 299 notions,
47 comparatifs, 75 hubs, 6 patterns, 6 règles. Trois axes (`role:`, `categorie:`,
`famille:`), un arbre de 20 domaines dérivé de `categorie:`, un seuil de promotion
à 5, deux validateurs, quatre générateurs, trois skills, huit lots de migration
dont chaque arbitrage est écrit avec sa mesure.

**C'est ce dernier point qui est la vraie valeur, et il faut le dire tôt** : ce que
huit lots ont produit n'est pas un vault, c'est une **discipline** — on ne durcit
jamais une règle sans avoir compté ses violations, on ne l'assouplit jamais sans
écrire le motif, et on réécrit la règle plutôt que d'ajouter une exception. Trois
règles du DevBrain sont en avertissement avec leur motif écrit ; deux ont été
réécrites parce que la mesure a montré que leur formulation d'origine était
inatteignable. Aucune ligne de code ne porte cette discipline. Elle se transpose
quand même, et c'est le premier livrable de BrainKit.

---

# 1. L'inventaire de séparation

## Comment lire les trois colonnes

Les définitions sont opérationnelles, pas esthétiques — chacune répond à « qu'est-ce
qu'il faut faire de cette brique pour l'installer ailleurs ? » :

| Colonne | Définition exacte |
|---|---|
| **GÉNÉRIQUE TEL QUEL** | Le code ou l'énoncé se transpose **sans une ligne de changement**. Il peut lire une déclaration du manifeste, mais il la lit comme une **donnée** — il n'y a rien à réécrire dedans. |
| **PARAMÉTRABLE** | La mécanique est générique, mais une **table de valeurs dev est aujourd'hui codée en dur** (`DOM_LABEL`, `NATURE`, `MEO_LABELS`, `THEME_LABEL`…). Le travail consiste à **l'extraire** dans le manifeste, pas à la réécrire. |
| **À RÉÉCRIRE PAR SUJET** | Ni le code ni les valeurs ne survivent. Seule la **forme** se reprend, et le contenu se refait de zéro à chaque sujet. |

Deux principes traversent tout l'inventaire et valent d'être posés avant lui :

1. **Aucune sévérité n'est portable.** `dure`, `avertissement` sont des **résultats de
   mesure** sur 338 fiches dev, pas des propriétés de règle. Une instance neuve reçoit
   **toutes** les règles en avertissement et les durcit après avoir compté. Porter une
   sévérité, c'est porter une mesure qu'on n'a pas faite.
2. **Une liste d'arbitrages naît vide.** Les 6 règles de départage de `famille:` et les
   7 de `categorie:` sont le sédiment de 338 pages. Un brain neuf n'en a aucune, et
   c'est normal : le mécanisme à transposer est **la place où elles s'écrivent**, pas
   leur contenu.

## A. L'ossature

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| A1 | L'arbre de dossiers par domaine à la racine | **GÉNÉRIQUE** | « Un dossier par domaine, un sous-dossier quand un sous-domaine grossit » ne contient aucun mot de dev ; les 20 noms sont ailleurs (A5). |
| A2 | L'axe `role:` — un champ fermé qui **choisit le gabarit** que le validateur applique | **GÉNÉRIQUE** | `check_brain` R3 refuse un `role:` inconnu ou absent et applique `ALLOWED[role]` : c'est un moteur de schéma indexé par une chaîne, indifférent aux chaînes. |
| A3 | Les **6 valeurs** de `role:` (`brique`, `notion`, `comparatif`, `hub`, `pattern`, `rule`) | **PARAMÉTRABLE** | `hub` est structurel et obligatoire partout ; `notion` se transpose (« ce qu'il faut comprendre ») ; les quatre autres sont des choix de sujet. La liste sort dans le manifeste. |
| A4 | La dérivation `categorie:` → chemin (`arbo.domaine()`, `arbo.dossier_attendu()`, `arbo.promotions()`) | **GÉNÉRIQUE** | Trente lignes qui coupent un préfixe, cherchent dans une table, comptent par domaine et appliquent un seuil. Zéro vocabulaire dev **dans le code**. |
| A5 | Les trois tables d'`arbo.py` : `DOM_LABEL` (20), `DOM_RATTACHE` (1), `SUB_LABEL` (39) | **PARAMÉTRABLE** | Ce sont les valeurs, et elles portent chacune un **motif d'arbitrage en commentaire** (« RAG & retrieval » parce que « RAG » est le nom d'une notion du dossier). Le manifeste doit donc porter `libelle:` **et** `motif:` — sans quoi la sortie en YAML perd ce que huit lots ont appris. |
| A6 | `SEUIL = 5` et son **plafond** (« un fils ne se promeut pas s'il ne laisse aucune page au parent ») | **PARAMÉTRABLE** | Le plafond est un raisonnement générique et remarquable ; le `5` est calibré sur ~700 pages. Voir §4 point 9 : c'est la valeur qui casse le plus vite. |
| A7 | Les wikilinks **nus** et la contrainte qui va avec (nom de fichier unique dans le vault, à la casse près) | **GÉNÉRIQUE** | Un lien qualifié casse au premier `git mv` ; le lot 3 a déplacé 682 fichiers sans toucher un lien. Vrai de tout vault Obsidian, quel que soit le sujet. |

## B. Les pages générées

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| B1 | Le hub par dossier et sa zone `<!-- AUTO -->` — la fonction **lit un dossier** | **GÉNÉRIQUE** | Le périmètre d'un hub est `ls` de son dossier, groupé par `role:`. Aucune connaissance du sujet n'entre là-dedans. |
| B2 | Les titres des sous-sections de la zone AUTO (`### Sous-domaines`, `### Notions`, `### Briques`, `### Comparatifs`) | **PARAMÉTRABLE** | Ils **sont** la liste des rôles au pluriel : ils se dérivent du manifeste au lieu d'être écrits. |
| B3 | `Métiers/` — un hub dont le périmètre est un **CHAMP** et non un dossier | **GÉNÉRIQUE** | L'idée « un axe qui traverse l'arbre, un hub par valeur d'un champ multivalué » est le mécanisme le plus réutilisable du lot 3. Mais `build_mocs.py` n'en gère **qu'un** — voir §4 point 4. |
| B4 | Les 6 valeurs de `domaines:` (`themes.md` : data-sci, data-eng, mlops, ml-eng, ai-eng, infra-ops) | **À RÉÉCRIRE** | Ce sont les métiers de floSa. Rien à en garder ailleurs. |
| B5 | `Comparatifs/` — un hub dont le périmètre est un **RÔLE** | **GÉNÉRIQUE** | Et son enseignement l'est aussi : *c'est le lien retour qui fait la grappe*. Un hub qui cite 47 pages sans qu'aucune le cite ajoute un nœud et ne rassemble rien. Vrai pour n'importe quel rôle dispersé dans l'arbre. |
| B6 | Le moteur de zone AUTO : balises dédiées, remplacement en bloc, **idempotence**, `--check` en code 2, préservation de la zone manuelle | **GÉNÉRIQUE** | C'est le contrat « ce qui est généré n'est jamais édité à la main, et se vérifie ». Zéro sujet dedans. |

## C. Les comparatifs

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| C1 | Le **couple** page `.md` + vue `.base` embarquée par un lien d'embed | **PARAMÉTRABLE** | La primitive réelle est « une page qui embarque une vue filtrée sur une catégorie, plus une section écrite à la main ». Générique. Ce qui est dev, c'est la colonne du tableau (le frontmatter d'une brique) et l'**intention** (départager). |
| C2 | La règle de majorité (`categorie:` d'un comparatif = celle qui rassemble le plus de ses membres) et `ROLES_HORS_SEUIL` (« un comparatif n'est pas un membre du comparatif ») | **GÉNÉRIQUE** | Deux raisonnements purs sur une page qui enjambe plusieurs valeurs de l'axe de rangement. §4 point 5 montre qu'ils servent bien au-delà des comparatifs. |
| C3 | Le **rôle** `comparatif` lui-même — départager des objets interchangeables | **À RÉÉCRIRE** | C'est le mécanisme qui casse le plus franchement hors du dev. Détail en §4 point 2. |
| C4 | Les **47 `.base`** — filtres et vues réglés un par un (`role == "brique"`, `categorie == …`, vue « Self-hostable » sur `hosted.contains("self")`) | **À RÉÉCRIRE** | Chacun est un arbitrage éditorial. Le manifeste peut donner un **gabarit de vue par défaut** (l'ordre des colonnes) ; les 47 filtres, non. |

## D. Les rôles rangés par rôle

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| D1 | Le mécanisme « un rôle **sans `categorie:`** est groupé par son rôle dans un dossier à la racine » (`ROLES_SANS_CATEGORIE`) | **GÉNÉRIQUE** | La justification est générique : un objet transverse par construction n'a pas de domaine à porter, donc son chemin se lit sur son rôle. |
| D2 | Le rôle `pattern` et son gabarit (`contexte`, `services_cles`, `projets_appliques`) | **À RÉÉCRIRE** | « Architecture éprouvée » n'existe pas hors du dev. La **place** existe (D1) ; le contenu, non. |
| D3 | Le rôle `rule` et son gabarit (`domaine`, `applicable`, `strictness`) | **À RÉÉCRIRE** | Le plus transposable des deux — « une prescription transverse, avec un degré de fermeté » se dit dans tous les sujets — mais aucun de ses trois champs ne survit tel quel. |

## E. Les gabarits

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| E1 | Le **contrat de frontmatter par rôle** : `REQUIRED` (non vides), `ALLOWED` (exacts, tout champ hors liste échoue), `VALUE_ENUMS`, `LIST_ENUMS` | **GÉNÉRIQUE** | C'est un moteur de schéma. Il ne connaît que « ce rôle attend ces clés, avec ces valeurs » : le schéma est de la donnée, pas du code. |
| E2 | Les **6 schémas** eux-mêmes (14 champs de brique + 2 conditionnels, 6 de notion, 4 de comparatif, 6 de hub, 5 de pattern, 5 de rule) | **À RÉÉCRIRE** | `pitch`, `famille`, `licence_type`, `hosted`, `scaling`, `url_repo` : la liste **est** le sujet. |
| E3 | Le mécanisme du **champ conditionnel** (R16 : `hosted:`/`scaling:` n'existent que si `famille ∈ {plateforme, saas, application}`) | **GÉNÉRIQUE** | « Ce champ n'existe que si cet autre champ vaut ceci » est une contrainte de schéma ordinaire, et §4 point 1 montre qu'elle se réemploie immédiatement en histoire. |
| E4 | Les **5 fichiers de `Templates/`** (`Service-Dev`, `Outil-Dev`, `Concept-Wiki`, `Pattern`, `Rule`) | **À RÉÉCRIRE** | Et un constat qui compte pour la conception : ils sont **périmés**. `Service-Dev.md` porte encore `## Pourquoi`, `## Pièges`, `## Liens` — le corps v2 — alors que les 338 briques portent le gabarit du lot 6. La source de vérité du gabarit est `brain-v3.md` §6, pas `Templates/`. **Conséquence pour BrainKit : les gabarits doivent être GÉNÉRÉS depuis le manifeste, jamais maintenus à la main à côté de lui** — c'est exactement le défaut qu'on vient de constater. |
| E5 | Le **corps** de `role: brique` (`## Définition`, `## Prendre si / Écarter si`, `## Mise en œuvre`, `## Écosystème` et ses deux listes, `## Ressources`, `## Voir aussi`) | **À RÉÉCRIRE** | Six titres, six intentions de dev. Ce qui se garde est la **doctrine** : une ligne, une étiquette, une idée ; aucune prose hors de `## Définition` ; une section `## Retours` n'existe **que** si une entrée datée existe. |
| E6 | Le corps de `role: notion` (`Aperçu`, `Concepts clés`, `Les maths simplement`, `En pratique`, `Approches voisines`, `Pour aller plus loin`) | **PARAMÉTRABLE** | Quatre des six titres marchent tels quels sur n'importe quel sujet. `Les maths, simplement` est le seul vraiment lié — et il devient « la chose technique du sujet, expliquée ». |

## F. La taxonomie

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| F1 | La **forme** de l'arbre de décision : questions **fermées**, **ordre strict**, première réponse positive gagne, et « si aucune ne tranche : laisser vide et **demander** » | **GÉNÉRIQUE** | C'est l'invention centrale de `taxonomie.md` et elle est intégralement transposable. L'ordre est *la* décision de conception : prise une fois, écrite, valable pour toutes les pages. |
| F2 | Les **règles de départage** — 6 pour `famille:`, 7 pour `categorie:` — et le fait qu'il existe une place pour elles | **GÉNÉRIQUE** | Le mécanisme est « l'endroit où s'écrit un arbitrage récurrent, une fois, avec le cas qui l'a provoqué ». Elle **naît vide** dans un brain neuf (principe 2 du préambule). |
| F3 | Les **94 valeurs** de `categorie:` en 20 préfixes, l'arbre D1→D14, les frontières disputées | **À RÉÉCRIRE** | C'est le dev, entièrement. |
| F4 | Les **9 valeurs** de `famille:`, l'arbre F1→F9, les 9 définitions et frontières | **À RÉÉCRIRE** | Idem. Le **slot** survit (voir §2, axe `nature`), pas les valeurs. |
| F5 | Les blocs clôturés ` ```domaine ` / ` ```famille ` comme **unique source machine** lue par le validateur | **PARAMÉTRABLE** | Excellente idée — un vocabulaire fermé lisible par l'humain **et** par le script, en un seul endroit. Dans BrainKit, cette place devient le **manifeste**, et `taxonomie.md` devient un document **généré**. |
| F6 | `tags.md` — vocabulaire contrôlé, kebab-case, « le skill pioche, il n'invente jamais ; un tag manquant se propose, s'ajoute ici, puis s'utilise » | **PARAMÉTRABLE** | La règle est parfaite et générique ; les ~200 tags sont dev. |

## G. Les dix règles de `brain-v3.md` §10

Rappel du principe 1 : les sévérités ci-dessous **ne se portent pas**. Elles sont
citées pour dire ce que la mesure a coûté, pas ce qu'une instance neuve hérite.

| # | Règle (état DevBrain) | Colonne | Pourquoi |
|---|---|---|---|
| G1 | **1 — Réciprocité** : A cite B en `alternatives:` ⇒ B cite A ; idem `complements:` *(dure, R12/R18)* | **PARAMÉTRABLE** | La symétrie de graphe est pure ; `CHAMPS_ECOSYSTEME` code en dur les deux noms de champ et leurs titres de section. Et §4 point 3 exhibe un cas que DevBrain n'a jamais eu : un lien **asymétrique**, qui a besoin d'un champ inverse et non d'un miroir. |
| G2 | **2 — Cohérence chemin / catégorie** *(dure, `check_arbo.py`)* | **GÉNÉRIQUE** | Le script compare un chemin réel à un chemin dérivé et propose le `git mv`. Le seul contenu dev est dans les tables d'`arbo.py`, déjà comptées en A5. |
| G3 | **3 — Complétude du dossier** : toute brique du dossier apparaît dans le hub *(dure, R19)* | **PARAMÉTRABLE** | Le code teste `role == "brique"`. Générique dès que le manifeste déclare *quels rôles doivent apparaître dans le hub de leur dossier*. |
| G4 | **4 — Voisinage déclaré** : `alternatives:` vide dans un dossier peuplé *(avertissement **définitif**, R20)* | **PARAMÉTRABLE** | Mêmes deux constantes. Le motif du maintien en avertissement est, lui, générique et à réécrire tel quel dans toute instance : *une page peut légitimement n'avoir aucun voisin — la signaler aide, l'interdire mentirait*. |
| G5 | **5 — Exclusion sourcée**, réécrite au lot 8 : une cellule qui **redirige** (flèche) vers une page **fichée** porte son wikilink *(dure, R21)* | **PARAMÉTRABLE** | La **conjonction** position (la flèche) × condition (la cible est couverte) est un raisonnement générique, et il transpose (§4 point 7). Ce qui se paramètre : la section qui porte le tableau, et le marqueur. Ce qui ne se porte pas : le fait qu'elle donne 1 violation — c'est vrai sur *ce* corpus. |
| G6 | **6 — Réinjection du résumé** : chaque puce commence par le `pitch:` **courant** de sa cible *(dure, R1/R22)* | **PARAMÉTRABLE** | « Un champ désigné comme résumé d'une ligne est recopié, jamais retapé, chez tous ses citeurs » : générique. `pitch` est un nom dev. |
| G7 | **7 — Étiquettes fermées** : `Mise en œuvre` porte ses 5 étiquettes ; `Ressources` pioche dans 7 *(dure / avertissement, R23)* | **PARAMÉTRABLE** | Le mécanisme « une section déclarée étiquetée a un vocabulaire fermé » est générique. Les deux vocabulaires sont dev et comptés en E5. |
| G8 | **8 — Pas de double citation**, réécrite au lot 8 : une cible ne se **liste** pas dans deux sections de liste de liens ; « listé » = **entrée** d'une puce *(dure, R24)* | **PARAMÉTRABLE** | La distinction « entrée de puce » contre « lien cité dans une phrase » est une trouvaille générique et non évidente : sans elle, la règle punit la forme qu'on recommande. La liste des sections concernées se paramètre. |
| G9 | **9 — Bandeau à jour** : la zone générée concorde avec le frontmatter *(dure, `--check`)* | **GÉNÉRIQUE** | « Régénérer et comparer les octets » ne connaît pas le sujet. Ce qui est dev, c'est la composition du bandeau (I5). |
| G10 | **10 — Anti-répétition** : `## Définition` ne redit pas le bandeau *(avertissement **définitif**, non scriptable, R26)* | **À RÉÉCRIRE** | Déjà déclarée non scriptable sur les mots dev (11 candidats, 2 vrais). En histoire c'est pire : « ouvrage », « article », « source » sont les mots les plus fréquents du corpus. **Recommandation : ne pas la livrer** — la proposer comme relecture assistée optionnelle, et rien de plus. |

## H. Les validateurs, comme squelettes

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| H1 | `check_arbo.py` — les 4 contrôles (concordance, seuil, **un hub par niveau du chemin**, frontmatter lisible) et sa sortie « voici le `git mv` à faire » | **GÉNÉRIQUE** | Rien de dev. Le contrôle « tout niveau du chemin porte son hub, pas seulement la feuille » est le genre de détail qu'on ne retrouve pas en réécrivant. |
| H2 | `check_brain.py` — le squelette : périmètre **par la négative** (`NON_PAGES`), et **R17 : un frontmatter illisible est une ERREUR, jamais une absence** | **GÉNÉRIQUE** | R17 est né d'un vrai dégât — une page sautée en silence, hors du total, hors de toutes les autres règles, pour un `pitch:` non quoté contenant « : ». C'est une leçon de conception de validateur, pas une règle de dev. |

## I. Les quatre générateurs

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| I1 | `build_index.py` → `brain-index.json` + `brain-index.md` (catalogue machine et document humain) | **PARAMÉTRABLE** | Balayage, `fm.get()`, sortie triée sans horodatage : générique. `NON_PAGES` et la liste des champs indexés sortent dans le manifeste. |
| I2 | `build_mocs.py` → zones AUTO des hubs, `Métiers/`, `Comparatifs/` | **PARAMÉTRABLE** | `THEME_LABEL`, `HUBS_TRANSVERSES` et les chemins `Métiers`/`Comparatifs` sont en dur, et **une seule** boucle transverse existe (§4 point 4). À noter : le fichier porte encore des branches mortes v2 (`MOC_CONCEPT`, `WIKI_LABEL`, `wiki_group()`) pour des dossiers supprimés — dette à ne pas hériter. |
| I3 | `build_links.py` → `liens.md` : tags, liens sortants, backlinks, **et « à créer » : les liens non résolus** | **GÉNÉRIQUE** | Pur graphe. La sortie « à créer » est un mécanisme de backlog qui vaut pour tout sujet. |
| I4 | `build_bandeau.py` — le **moteur** : zone AUTO dédiée, idempotent (zéro octet écrit si rien ne change), `--check` en code 2, portée par chemin, et la règle dure du lot 6 — **une cellule sans source dans le frontmatter affiche un tiret cadratin, jamais une valeur plausible** | **GÉNÉRIQUE** | « Une fiche vide honnêtement vaut mieux qu'une fiche remplie au jugé » est la meilleure phrase du dépôt, et elle n'a pas de sujet. |
| I5 | `build_bandeau.py` — le **contenu** : les 4 colonnes (Nature, Licence, Exécution, Maturité) et leurs tables `NATURE`, `LICENCE`, `EXECUTION_FAMILLE`, `HOSTED` | **À RÉÉCRIRE** | Cent pour cent dev. §4 point 6 montre la transposition en histoire : elle est propre, et elle est totale. |

## J. La règle de propagation

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| J1 | L'énoncé — **« le rayon de propagation d'une insertion est le dossier d'accueil plus ses hubs parents ; le voisinage d'une page est `ls` de son dossier »** | **GÉNÉRIQUE** | C'est le joyau, et il est sans sujet. Il ne dépend que d'un fait structurel : le dossier porte le domaine. Tout brain construit sur A1 l'obtient gratuitement. |
| J2 | La table **P1→P6** (hub du dossier, hubs parents, comparatif, notion, pairs, résumés réinjectés) et la clause « **une ligne sans objet se déclare sans objet, elle ne se tait pas** » | **GÉNÉRIQUE** | Les six lignes ne sont pas six décisions : elles **se dérivent** de la liste des rôles du manifeste (un rôle-vue → une ligne comparatif ; un rôle protégé → une ligne notion ; les pairs = même rôle dans le dossier). La table est donc générée, pas écrite. |

## K. Les skills

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| K1 | La **triade** capture / clôture / exploitation | **GÉNÉRIQUE** | Le découpage est structurel, pas thématique : un skill qui **écrit** dans le brain, un skill qui **clôt** toute écriture (régénérer, valider, committer), un skill qui **consomme** le brain sans y écrire. Tout brain a besoin des trois. |
| K2 | `enrichir-brain` | **PARAMÉTRABLE** | Le squelette est générique de bout en bout : dériver le dossier → `ls` le rayon → P1..P6 → écrire dans les deux sens → `[V1]` vérifier la réinjection → *mode mise à jour* avec sa **table des effets de bord** (champ modifié → consommateurs → commande de vérification). Chaque nom de champ, de section et de rôle qu'il cite est un paramètre. La table des effets de bord se **génère** depuis le manifeste. |
| K3 | `cloturer-brain` | **GÉNÉRIQUE** | Quatre étapes sans sujet : régénérer, passer les deux validateurs au vert, vérifier la divergence avec `origin/main` **avant** tout commit, committer et intégrer en fast-forward. Le seul contenu à paramétrer est le nom des scripts et l'identité git. |
| K4 | `planifier-projet` | **À RÉÉCRIRE** | C'est le consommateur, donc le plus lié au sujet : archétypes de projet, filtrage sur `maturite`, format de candidature avec `famille`/`langage`, `Prendre si`/`Écarter si`. Ce qui survit est la **forme** : identifier l'usage → poser seulement les questions pertinentes → interroger l'index → produire un livrable **sourcé** qui contraint l'aval. Cette forme est le slot K1-exploitation. |

## L. Le graphe Obsidian

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| L1 | Une couleur par `role:`, l'**ordre** des règles (`path:` avant `role:`, sinon un hub spécial prend la couleur des hubs ordinaires), et le constat « **un `.base` ne se colore pas** — il n'a pas de frontmatter, donc pas de `role:` » | **GÉNÉRIQUE** | Trois faits sur Obsidian, aucun sur le dev. |
| L2 | La palette (6 entiers RGB) et les 6 requêtes | **PARAMÉTRABLE** | Une couleur par rôle → se dérive de la liste des rôles. À noter : `.obsidian/graph.json` est **gitignoré**, donc cette table est la seule source de vérité et se réapplique à la main sur chaque poste — c'est une étape d'installation, pas un fichier. |

## M. Les garde-fous git

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| M1 | `commit-msg` — refus du trailer `Co-Authored-By`, via `git stripspace --strip-comments` | **GÉNÉRIQUE** | « Les commits sont à une seule personne » est une politique de dépôt, pas de sujet. Le hook est réutilisable octet pour octet. |
| M2 | `pre-commit` / `pre-push` — refus d'un **domaine d'adresse**, lu par `git var GIT_AUTHOR_IDENT` (la seule lecture qui ne se contourne pas : config, env, `-c user.email`) | **PARAMÉTRABLE** | Le domaine interdit est une valeur — **et sa polarité peut s'inverser** : un brain de domaine client, vendu chez Aosis, est un dépôt **pro**, et c'est alors l'adresse perso qu'il faut refuser. Le hook doit donc lire « identité attendue » dans la config, pas coder un domaine. |
| M3 | Le **garde-fou du garde-fou** : `pre-commit` refuse de committer si `commit-msg` n'est pas installé sous le `core.hooksPath` **effectif** | **GÉNÉRIQUE** | Raisonnement rare et à copier tel quel : une installation partielle ne doit pas pouvoir faire disparaître un contrôle en silence. Y compris son détail Windows — git juge un hook exécutable dès qu'il commence par `#!`, `test -x` ne suffit pas. |
| M4 | L'**emplacement** de la règle d'identité : dans `CLAUDE.md`, parce que c'est le seul fichier chargé à **chaque** conversation, au même moment que l'annonce du harnais | **GÉNÉRIQUE** | Un raisonnement sur l'ordre de chargement du contexte, pas sur le dev. Une contre-instruction qui arrive après coup arrive trop tard : cinq commits avaient déjà été signés. |

## N. La documentation

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| N1 | `INSTALL.md` — 15 sections : pré-requis, clone, **hooks (§3.5, obligatoire)**, coffre Obsidian, 4 plugins, REST API + MCP, Templater, File Hider, couleurs, `CLAUDE.md`, hook Stop, vérification, dépannage | **PARAMÉTRABLE** | La séquence entière est de l'installation **Obsidian + Claude Code**, indifférente au sujet. Les valeurs : nom du coffre, table de couleurs, dossier de gabarits, nom des skills. La section *Dépannage* se reprend telle quelle. |
| N2 | 17 des 28 captures — panneaux de réglages Obsidian, navigateur de plugins, options de plugin | **GÉNÉRIQUE** | Elles montrent l'**interface d'Obsidian**, pas le DevBrain. Réutilisables sans retouche. |
| N3 | 11 des 28 captures — sélecteur de dossier, arbre du coffre, fiche Postgres, deux comparatifs, vue d'ensemble, graphe coloré, snippet de rôles, menus File Hider | **À RÉÉCRIRE** | Elles montrent du contenu dev. À reprendre par instance — ce qui veut dire que la doc générée doit **référencer** ses captures par un manifeste d'images, pas les embarquer en dur. |
| N4 | `docs/manuel-utilisateur.md` — les natures de page, où vit une page, lire une fiche, lire un comparatif, trouver quelque chose, ce qui est généré | **PARAMÉTRABLE** | Les 7 sections sont structurelles : chacune se **génère** depuis le manifeste. C'est le meilleur candidat à la génération de tout le dépôt. |
| N5 | `docs/guide-enrichissement.md` — « tu ne crées pas une page, tu déclenches une propagation », les deux valeurs qu'on ne devine jamais, la frontière `role: notion`, la clôture qu'on ne saute pas | **PARAMÉTRABLE** | Même remarque, et son titre de section 1 est l'énoncé de J1 en langage d'utilisateur. |
| N6 | `docs/guide-projet.md` — ne pas travailler dans le vault, interroger l'index, ce qui remonte du projet vers le brain | **À RÉÉCRIRE** | Côté consommateur, comme K4. |

## O. Le routeur et les places restantes

| # | Brique | Colonne | Pourquoi |
|---|---|---|---|
| O1 | `CLAUDE.md` — l'**annonce de mode** au démarrage, les frontières d'écriture (ce qui est libre, ce qui demande confirmation, ce qui est interdit), la tolérance aux anciens noms de mode | **PARAMÉTRABLE** | La structure est générique : un routeur qui déclare qui écrit où. Tout son vocabulaire est dev. |
| O2 | `CLAUDE-build.md` — le contexte du mode d'enrichissement | **PARAMÉTRABLE** | Idem. |
| O3 | `CLAUDE-project.md` — le gabarit installé **dans le projet consommateur** | **À RÉÉCRIRE** | Il n'existe que parce que le consommateur du DevBrain est un dépôt de code. Un brain d'histoire n'a pas de « projet » au même sens. |
| O4 | La frontière **`role: notion` = mémoire perso** : création libre, **modification sur demande explicite**, et surtout — *la frontière est portée par le champ, pas par le chemin ; donc lire le frontmatter avant d'écrire* | **GÉNÉRIQUE** | Le mécanisme se généralise en un seul drapeau : `protege: true` sur un rôle. §4 point 10 : c'est celui qui compte le plus hors du dev, où les notes de l'utilisateur *sont* la valeur. |
| O5 | `Home.md`, `Inbox.md` (écrit par l'utilisateur, modifiable dans les deux modes), `Projects/`, `AI/` (espace agent : `design/`, `migration/` un fichier par lot avec ses *Remontées*, `index/` généré, `sessions/`, `scripts/`, `backlog.md`) et le hook Stop qui écrit un résumé de session | **GÉNÉRIQUE** | Des **places**, pas du contenu. Ce découpage est réutilisable tel quel, et il est une bonne partie de la raison pour laquelle huit lots ont tenu. |
| O6 | `query_index.py` — interroger l'index par `--role` et filtres | **GÉNÉRIQUE** | Un lecteur de JSON. |

## Le compte

| Colonne | Briques | Part |
|---|---|---|
| **GÉNÉRIQUE TEL QUEL** | **32** | 44 % |
| **PARAMÉTRABLE** | **25** | 34 % |
| **À RÉÉCRIRE PAR SUJET** | **16** | 22 % |
| **Total** | **73** | |

Ce que ce compte dit, et qu'il faut lire comme un résultat de conception :

- **78 % du système part sans réécriture** (générique + paramétrable). Le DevBrain
  est, sans l'avoir cherché, presque entièrement générique — parce que ses trois axes
  séparent déjà *ce qu'une page est*, *de quoi elle parle* et *ce qu'elle est
  techniquement*. Cette séparation est ce qui rend BrainKit possible.
- **Les 16 « à réécrire » sont presque toutes des LISTES DE VALEURS** : les 94
  catégories, les 9 familles, les 6 métiers, les 4 colonnes du bandeau, les 6 titres
  de corps, deux gabarits de rôle, les 47 filtres `.base`, deux documents de
  consommateur, onze captures. Une seule est un *mécanisme* qui ne survit pas — le
  rôle `comparatif` (C3) — et une seule est une règle à ne pas livrer :
  l'anti-répétition (G10).
- **Les 25 paramétrables sont le travail réel.** Ce ne sont pas des réécritures, ce
  sont des **extractions** : sortir `DOM_LABEL`, `NATURE`, `MEO_LABELS`, `THEME_LABEL`,
  `CHAMPS_ECOSYSTEME`, `SECTIONS_LIENS` du code vers un fichier unique. Ce fichier est
  l'objet de la section 2.

---

# 2. Le manifeste du brain

## 2.0 Ce qu'il est, et ce qu'il n'est pas

**Un fichier, `brain.yml`, à la racine du vault.** Il porte tout ce que la section 1
a classé « PARAMÉTRABLE », et rien d'autre. Il ne porte **jamais** de contenu de
page, jamais de prose destinée à un lecteur, jamais de code.

Trois propriétés non négociables, chacune pour une raison mesurée dans le DevBrain :

1. **Il est la seule source.** `taxonomie.md`, `tags.md`, `themes.md`, les gabarits
   de `Templates/`, la table de couleurs du graphe, la table P1→P6 du skill de
   capture, les trois guides : tous **générés** depuis lui. Motif : E4 — les 5
   gabarits de `Templates/` sont périmés par rapport aux 338 pages qu'ils étaient
   censés produire, parce que deux sources décrivaient le même gabarit.
2. **Chaque valeur peut porter son motif.** Tout libellé, toute sévérité, toute
   valeur d'énumération accepte un champ `motif:` frère. Motif : A5 — les 39 entrées
   de `SUB_LABEL` valent surtout par le commentaire qui dit *pourquoi ce libellé et
   pas l'évident*. Une sortie en YAML qui perd ces commentaires perd huit lots.
3. **Il déclare des fonctions, pas seulement des mots.** Chaque rôle porte un `id:`
   — le mot que l'utilisateur lit dans son vault, `role: brique` ou `role: source` —
   **et** une `fonction:` prise dans une liste fermée du kit. Le vault se lit dans la
   langue de son sujet ; le kit ne raisonne que sur les fonctions. Sans ce
   dédoublement, aucun outil partagé ne peut filtrer deux instances.

Les six fonctions du kit, et c'est une liste fermée :

| `fonction:` | Ce qu'elle désigne | Obligatoire ? |
|---|---|---|
| `unite` | Ce qu'on va chercher dans le brain. Porte l'axe de rangement, l'axe de nature, le bandeau, les liens réciproques. | **oui, exactement une** |
| `notion` | Ce qu'il faut comprendre. Porte l'axe de rangement, pas l'axe de nature. | non |
| `hub` | La page d'un dossier. Ne se range pas : *elle est* le rangement. | **oui, exactement une** |
| `vue` | Une page qui embarque une table filtrée sur l'axe de rangement, plus une section écrite à la main. | non |
| `prescription` | Un objet transverse par construction, sans valeur d'axe de rangement, groupé par son rôle dans un dossier racine. | non, 0..n |
| `transverse` | Le hub d'une valeur d'un axe transverse. Généré, jamais écrit. | non, déduit des axes |

## 2.1 Structure, champ par champ

### `manifeste:` et `brain:` — l'en-tête

| Champ | Type | Rôle | Obligatoire |
|---|---|---|---|
| `manifeste` | entier | Version du **contrat**, pas du brain. Le kit refuse un manifeste dont il ne connaît pas la version. | oui |
| `brain.nom` | chaîne | Nom du vault et du dépôt. | oui |
| `brain.sujet` | chaîne, une phrase | De quoi ce brain parle. Réutilisée dans `Home.md` et dans la description des skills. | oui |
| `brain.langue` | code ISO | Langue de la prose générée. v1 : `fr` uniquement (cf. §5 point 9). | oui |
| `brain.volume_cible` | entier | Nombre de pages visé à terme. **C'est de là que le seuil de promotion se dérive** (A6, §4 point 9) — jamais d'une valeur tapée à la main. | oui |
| `brain.proprietaire.nom` | chaîne | Qui écrit. Sert la frontière `protege:`. | oui |
| `brain.usage` | `perso` \| `pro` \| `client` | Décide la **polarité** du garde-fou d'identité (M2), et si le vault peut contenir de la donnée client. | oui |

### `git:` — l'identité et ses garde-fous

| Champ | Type | Rôle |
|---|---|---|
| `git.identite.name` | chaîne | Posée en config **locale** du dépôt. |
| `git.identite.email` | chaîne | Idem. **Jamais** lue depuis l'annonce du harnais (M4). |
| `git.domaines_refuses` | liste | Domaines d'adresse qu'un commit ne peut pas porter. Sur un brain `usage: perso`, le domaine pro ; sur un `usage: client`, l'inverse. |
| `git.trailers_refuses` | liste | Par défaut `[Co-Authored-By]`. |
| `git.branche_principale` | chaîne | `main`. |

### `libelles:` — le vocabulaire visible

Une entrée par mot que la prose générée doit employer, chacune au singulier et au
pluriel. C'est le seul endroit où le mot « brique » existe dans BrainKit.

### `roles:` — une entrée par nature de page

| Champ | Type | Rôle |
|---|---|---|
| `id` | chaîne | La valeur littérale de `role:` dans le frontmatter. |
| `fonction` | énum fermée | Une des six ci-dessus. Ce que le kit lit. |
| `libelle` | `{s, p}` | Singulier et pluriel, pour la prose et les titres de zone AUTO (B2). |
| `range_par` | `axe` \| `role` | `axe` : le chemin se dérive de l'axe de rangement. `role` : le dossier est `<Dossier du rôle>/` à la racine (D1). |
| `dossier` | chaîne | Uniquement si `range_par: role`. |
| `protege` | booléen | `true` → création libre, **modification sur demande explicite** (O4). |
| `pese_sur_le_seuil` | booléen | `false` reproduit `ROLES_HORS_SEUIL` (C2). |
| `apparait_dans_le_hub` | booléen | Alimente la règle 3 (G3). |
| `couleur` | hex | Une couleur de graphe par rôle (L2). |
| `taille_avertissement` | entier ou nul | Lignes au-delà desquelles on suggère de scinder. |
| `champs.requis` | liste | Non vides. |
| `champs.autorises` | liste | **Exacts** : tout champ hors liste échoue (E1). |
| `champs.conditionnels` | liste de `{champ, si}` | `si` est une condition sur un autre champ (E3). |
| `corps` | liste de sections | Voir ci-dessous. |
| `motif` | chaîne | Pourquoi ce rôle existe. |

### `roles[].corps[]` — le gabarit du corps

Chaque section porte un `titre`, un `niveau` (2 ou 3) et un `genre` pris dans une
liste fermée. **Le genre est ce qui branche les règles** — c'est lui qui remplace
`SECTIONS_LIENS`, `MEO_LABELS` et `ALT_SECTION_RE` :

| `genre` | Ce que c'est | Règles qu'il branche |
|---|---|---|
| `prose` | Du texte suivi. La seule section où la prose est permise. | — |
| `bandeau` | Zone AUTO générée depuis le frontmatter. | règle 9 (G9) |
| `decision` | Un tableau à deux colonnes, l'une positive, l'autre négative avec redirections. | règle 5 (G5) |
| `etiquetee` | Des puces `- <Étiquette> — <valeur>`, vocabulaire **fermé**, avec `obligatoires:` et `permises:`. | règle 7 (G7) |
| `liste_liens` | Des puces dont l'**entrée** est un wikilink, adossées à un champ du frontmatter. | règles 1, 6, 8 (G1, G6, G8) |
| `auto` | Zone AUTO d'un hub, remplie par `ls` du dossier. | B1 |
| `libre` | Rien de contrôlé. | — |
| `conditionnelle` | N'existe **que si** une condition est remplie (« une section `## Retours` n'existe que si une entrée datée existe »). | — |

### `axes:` — les trois familles d'axes

```yaml
axes:
  rangement:      # EXACTEMENT UN. C'est lui qui donne le chemin.
  nature:         # ZÉRO OU UN. Il qualifie l'unité, il ne la range pas.
  transverses: [] # ZÉRO OU PLUSIEURS. Ils traversent l'arbre.
```

| Champ de `axes.rangement` | Rôle |
|---|---|
| `champ` | Nom du champ (`categorie` dans DevBrain). |
| `exclusif` | `true` si une page ne peut porter qu'une valeur. **Si `false`, il faut une règle de majorité et un préfixe transversal** (§4 point 5). |
| `seuil_promotion` | Dérivé de `brain.volume_cible`, avec le motif du calcul. |
| `plafond_promotion` | `true` = un fils qui redoublerait son parent ne se promeut pas (A6). |
| `prefixes[]` | `{cle, dossier, motif, sous: {cle: {libelle, motif}}}` — c'est `DOM_LABEL` plus `SUB_LABEL`, avec leurs motifs. |
| `rattachements` | `{prefixe: dossier}` — c'est `DOM_RATTACHE`, les exceptions nommées et datées. |
| `arbre_de_decision[]` | `{n, question, si_oui, motif}` — ordre strict, première réponse positive gagne (F1). |
| `departages[]` | `{n, regle, cas}` — **naît vide** (F2, principe 2). |
| `frontieres[]` | `{entre, et, distinction}` — les frontières disputées, écrites une fois. |

`axes.nature` a la même forme, sans `seuil_promotion` ni `plafond_promotion` :
`champ`, `porte_par` (les rôles concernés), `valeurs[]` avec
`{cle, definition, frontiere}`, `arbre_de_decision[]`, `departages[]`, et
`vide_autorise:` — le drapeau qui reproduit la décision la plus fine de
`taxonomie.md` : *un champ vide est le seul signal prévu pour « l'arbre n'a pas
tranché » ; une valeur inventée est une faute, un champ vide est une question
ouverte.*

`axes.transverses[]` : `{champ, dossier, multivalue, valeurs: [{cle, libelle, couvre}]}`.
La liste peut être **vide** — un brain sans axe transverse est légal, et le
générateur ne doit alors créer aucun dossier.

### `champs:` — le dictionnaire, une fois

Chaque champ cité dans un rôle est défini ici une seule fois :

| Clé | Rôle |
|---|---|
| `type` | `ligne`, `texte`, `liste`, `enum`, `liste_enum`, `liens`, `url`, `bool`, `date` |
| `valeurs` | Pour `enum` et `liste_enum`. |
| `fonction` | `resume_court` (le champ réinjecté, G6), `identite` (égal au nom de fichier, R9), `alias`, `aucune`. |
| `reciproque` | `null`, `{mode: symetrique}`, ou `{mode: inverse, champ: <autre>}`. **Le mode inverse n'existe pas dans DevBrain** et il est nécessaire ailleurs (§4 point 3). |
| `section` | La section `liste_liens` qui doit couvrir ce champ. |
| `eliminatoire` | Optionnel : pour un `enum`, la ou les valeurs qui **disqualifient** une page auprès du skill d'exploitation. **Aucune valeur par défaut** (§4 point 6). |
| `motif` | Pourquoi ce champ existe, et pourquoi pas un autre. |

### `bandeau:` — le haut de page

`porte_par` (les rôles), `vide` (le caractère affiché quand la source manque — le
tiret cadratin de I4), et `colonnes[]` : `{titre, source, table, qualifie_par,
depend_de}`. Une colonne dont la source n'est pas un champ déclaré est une **erreur
de manifeste**, pas une colonne vide.

### `regles:` — les dix, activables, avec leur mesure

Chaque entrée : `{id, active, severite, motif, mesure: {date, population, violations}}`,
plus les paramètres propres à la règle. `severite` prend `dure`, `avertissement` ou
**`a_mesurer`** — la valeur par défaut de toute instance neuve, et la seule que le
générateur sait écrire (principe 1).

### Le reste

`vocabulaires:` (les fichiers de vocabulaire fermé et leur mode : `ferme`,
`propose`, `libre`) · `graphe:` (l'ordre des règles de couleur, `path:` avant
`role:`) · `genere:` (la liste des chemins qu'aucune main n'édite) · `skills:` (les
trois de la triade K1, avec leur nom instancié) · `agent:` (l'arborescence de `AI/`).

## 2.2 Rempli une première fois — DevBrain à l'identique

C'est le **test de fidélité** : si le manifeste ne sait pas redire DevBrain, il est
faux. Les listes longues sont tronquées à un échantillon **explicitement marqué**
`# … 17 autres préfixes` ; tout ce qui est tronqué est une répétition de la même
forme, jamais un cas différent. Ce qui ne **rentre pas** est en 2.3, et c'est la
partie de cette section qui compte.

```yaml
manifeste: 1

brain:
  nom: DevBrain
  sujet: "Les briques et les notions du développement data, ML et IA, rangées par domaine."
  langue: fr
  volume_cible: 800          # 338 briques + 299 notions + 47 comparatifs + marge
  usage: perso
  proprietaire:
    nom: floSa

git:
  identite:
    name: floSa
    email: <adresse perso>   # config LOCALE du depot, jamais l annonce du harnais
  domaines_refuses: [aosis.net]
  trailers_refuses: [Co-Authored-By]
  branche_principale: main
  motif: >
    Depot PERSO. Cinq commits ont deja ete signes avec l adresse pro et sont
    entres dans les contributeurs GitHub. La regle est ecrite dans CLAUDE.md
    parce que c est le seul fichier charge a chaque conversation.

libelles:
  unite:      { s: brique, p: briques }
  notion:     { s: notion, p: notions }
  vue:        { s: comparatif, p: comparatifs }
  hub:        { s: hub, p: hubs }
  axe_rangement: { s: domaine, p: domaines }
  axe_nature:    { s: famille, p: familles }

roles:
  - id: brique
    fonction: unite
    libelle: { s: brique, p: briques }
    range_par: axe
    protege: false
    pese_sur_le_seuil: true
    apparait_dans_le_hub: true
    couleur: "#412CDD"
    taille_avertissement: 90
    champs:
      requis: [role, nom, pitch, categorie]
      autorises: [role, nom, alias, pitch, categorie, famille, domaines,
                  licence_type, langage, os, hosted, scaling, maturite,
                  alternatives, complements, tags, url_docs, url_repo]
      conditionnels:
        - { champ: hosted,  si: "famille in [plateforme, saas, application]" }
        - { champ: scaling, si: "famille in [plateforme, saas, application]" }
      motif_conditionnels: >
        177 fiches famille:paquet portaient une valeur d hebergement. Une
        bibliotheque ne s heberge pas et ne scale pas.
    corps:
      - { titre: "<bandeau>",              niveau: 0, genre: bandeau }
      - { titre: "Définition",             niveau: 2, genre: prose }
      - { titre: "Prendre si / Écarter si", niveau: 2, genre: decision,
          colonne_positive: "Prendre si", colonne_negative: "Écarter si" }
      - { titre: "Mise en œuvre",          niveau: 2, genre: etiquetee,
          obligatoires: [Installation, "Point d'entrée", Prérequis, Exécution, Coût],
          permises:     [Installation, "Point d'entrée", Prérequis, Exécution, Coût] }
      - { titre: "Écosystème",             niveau: 2, genre: libre }
      - { titre: "Alternatives",           niveau: 3, genre: liste_liens, champ: alternatives }
      - { titre: "Compléments",            niveau: 3, genre: liste_liens, champ: complements }
      - { titre: "Ressources",             niveau: 2, genre: etiquetee,
          obligatoires: [],
          permises: [Documentation, Dépôt, Tutoriel, Article, Papier, Cours, Vidéo] }
      - { titre: "Voir aussi",             niveau: 2, genre: liste_liens, champ: null }
      - { titre: "Retours",                niveau: 2, genre: conditionnelle,
          existe_si: "au moins une entrée datée",
          forme: "- YYYY-MM-DD — <symptôme> : <correctif>." }

  - id: notion
    fonction: notion
    libelle: { s: notion, p: notions }
    range_par: axe
    protege: true              # <- la frontiere « memoire perso » (O4)
    pese_sur_le_seuil: true
    apparait_dans_le_hub: true
    couleur: "#7AB800"
    taille_avertissement: 200
    champs:
      requis: [role, nom, categorie, domaines]
      autorises: [role, nom, alias, categorie, domaines, tags]
    corps:
      - { titre: "Aperçu",                niveau: 2, genre: libre }
      - { titre: "Concepts clés",         niveau: 2, genre: libre }
      - { titre: "Les maths, simplement", niveau: 2, genre: libre }
      - { titre: "En pratique",           niveau: 2, genre: libre }
      - { titre: "Approches voisines",    niveau: 2, genre: liste_liens, champ: null }
      - { titre: "Pour aller plus loin",  niveau: 2, genre: libre }
    motif: "Ce que floSa a compris et ecrit pour lui-meme. On y ajoute, on n y reecrit pas."

  - id: comparatif
    fonction: vue
    libelle: { s: comparatif, p: comparatifs }
    range_par: axe
    prefixe_nom: "Comparatif - "
    vue_embarquee: { extension: ".base", moteur: "obsidian-bases" }
    regle_de_categorie: majorite      # celle qui rassemble le plus de ses membres
    pese_sur_le_seuil: false          # un comparatif n est pas un membre du comparatif
    apparait_dans_le_hub: true
    couleur: "#EF4444"
    hub_de_ralliement: { dossier: "Comparatifs", lien_retour: "Voir aussi" }
    champs:
      requis: [role, nom, categorie]
      autorises: [role, nom, categorie, tags]
    corps:
      - { titre: "<accroche>", niveau: 0, genre: prose, forme: "On tranche sur : …" }
      - { titre: "<embed>",    niveau: 0, genre: auto }
      - { titre: "Ce qui départage", niveau: 2, genre: liste_liens, champ: null }
      - { titre: "Voir aussi", niveau: 2, genre: liste_liens, champ: null }

  - id: hub
    fonction: hub
    libelle: { s: hub, p: hubs }
    range_par: axe            # il EST le rangement : pas de categorie
    porte_categorie: false
    couleur: "#FF922B"
    champs:
      requis: [role, nom, pitch]
      autorises: [role, nom, alias, pitch, domaines, tags]
    corps:
      - { titre: "Ce qu'il faut comprendre", niveau: 2, genre: libre }
      - { titre: "Choisir",                  niveau: 2, genre: libre }
      - { titre: "<AUTO>",                   niveau: 0, genre: auto,
          groupe_par: role, sous_titres_depuis: libelle.p }

  - id: pattern
    fonction: prescription
    libelle: { s: pattern, p: patterns }
    range_par: role
    dossier: Patterns
    prefixe_nom: "Pattern - "
    couleur: "#94A3B8"
    champs:
      requis: [role, contexte, services_cles]
      autorises: [role, tags, contexte, services_cles, projets_appliques]

  - id: rule
    fonction: prescription
    libelle: { s: règle, p: règles }
    range_par: role
    dossier: Rules
    prefixe_nom: "Rule - "
    couleur: "#94A3B8"
    champs:
      requis: [role, domaine, applicable, strictness]
      autorises: [role, tags, domaine, applicable, strictness]

axes:
  rangement:
    champ: categorie
    exclusif: true
    seuil_promotion: 5
    motif_seuil: "Calibre sur ~700 pages en 20 domaines. Cf. §4 point 9."
    plafond_promotion: true
    motif_plafond: >
      Un fils qui ne laisse aucune page au niveau du domaine n apporte aucune
      information et ajoute un niveau. Mesure sur Stockage (6/6) et
      Automatisation no-code (5/5), defaits le 2026-09-04.
    prefixes:
      - cle: ml
        dossier: "Machine Learning"
        sous:
          apprentissage-profond: { libelle: "Apprentissage profond" }
          socle:  { libelle: "Socle",
                    motif: "Reprend le mot du corps du hub depuis le lot 3." }
          eval:   { libelle: "Évaluation de modèles",
                    motif: "« Évaluation » est deja le hub de LLM & IA générative/." }
          non-supervise: { libelle: "Non supervisé",
                    motif: "« Apprentissage non supervisé » est le nom d une NOTION du dossier." }
          # … rl, series-temporelles, nlp, serving, vision, tracking,
          #   interpretabilite, tabulaire ; et graphe, embeddings, hyperopt,
          #   orchestration, monitoring, feature-store, hub sous le seuil
      - cle: llm
        dossier: "LLM & IA générative"
        sous:
          rag: { libelle: "RAG & retrieval",
                 motif: "« RAG » est le nom de fichier d une notion du dossier." }
          observabilite: { libelle: "Observabilité des LLM",
                 motif: "« Observabilité » est le hub du domaine homonyme." }
          passerelle: { libelle: "Passerelles",
                 motif: "Le singulier lirait comme la notion, pas comme le dossier." }
          # … agent-de-code, runtime, agents, finetuning, text-to-sql,
          #   assistant, eval, sortie-structuree, modele
      - cle: database
        dossier: "Bases de données"
        sous: { vecteur: {libelle: Vectoriel}, admin: {libelle: Administration},
                recherche: {libelle: Recherche}, relationnel: {libelle: Relationnel} }
      # … 17 autres prefixes : data, devtools, stats, compute, design, storage,
      #   web, automation, media, ui, observability, security, signal, network,
      #   devops, docs, math
    rattachements:
      skill: "Outils de développement"     # tranche le 2026-09-04, lot 3 remontee 5
    arbre_de_decision:
      - { n: D1, question: "A-t-il besoin d'un grand modèle de langage pour fonctionner ?", si_oui: "llm/*" }
      - { n: D2, question: "Entraîne-t-il, sert-il, suit-il ou explique-t-il un modèle d'apprentissage ?", si_oui: "ml/*" }
      - { n: D3, question: "Stocke et interroge-t-il des données de façon persistante ?", si_oui: "database/*" }
      # … D4 a D13
      - { n: D14, question: "Aucun des précédents", si_oui: "ARRÊT — demander avant d'inventer" }
    departages:
      - { n: D-R1, regle: "Le tri D1/D2 se fait sur ce dont l'objet a besoin pour tourner, pas sur ce à quoi il ressemble.", cas: "TransformerLens, SAELens, nnsight → ml/*" }
      - { n: D-R2, regle: "data/* = sortie destinée à une machine ; docs/* = sortie destinée à un humain.", cas: "Stirling PDF → docs/pdf ; docTR → data/parsing" }
      # … D-R3 a D-R7
    frontieres:
      - { entre: "ml/socle", et: "ml/tabulaire", distinction: "scikit-learn ne suppose rien du type de données, XGBoost si." }
      # … 8 autres

  nature:
    champ: famille
    porte_par: [brique]
    vide_autorise: true
    motif_vide: >
      Un champ vide est le SEUL signal prevu pour « l arbre n a pas tranche ».
      Une famille inventee est une faute, un champ vide est une question ouverte.
    valeurs:
      - { cle: paquet,        definition: "S'installe dans un projet et s'importe dans du code." }
      - { cle: plateforme,    definition: "Se déploie et tourne en processus qu'un autre programme appelle." }
      - { cle: application,   definition: "S'utilise par une interface faite pour un humain." }
      - { cle: cli,           definition: "S'invoque en commande shell sans être importé." }
      - { cle: saas,          definition: "Compte chez un tiers obligatoire, aucun auto-hébergement." }
      - { cle: extension,     definition: "Ne s'exécute qu'à l'intérieur d'un hôte tiers." }
      - { cle: specification, definition: "Norme, format ou protocole sans implémentation de référence." }
      - { cle: modele,        definition: "Le livrable est un jeu de poids entraînés." }
      - { cle: annuaire,      definition: "Liste de ressources externes, pas un logiciel." }
    arbre_de_decision:
      - { n: F1, question: "Décrit-elle une liste de ressources externes plutôt qu'un logiciel ?", si_oui: annuaire }
      - { n: F2, question: "Est-ce une norme, un format ou un protocole, sans implémentation de référence unique ?", si_oui: specification }
      # … F3 a F8
      - { n: F9, question: "Aucun des précédents", si_oui: paquet }
    departages:
      - { n: F-R1, regle: "Si le code est publié et déployable, la famille est plateforme, jamais saas.", cas: "Comet, Neptune, W&B, LangSmith, E2B" }
      # … F-R2 a F-R6

  transverses:
    - champ: domaines
      dossier: "Métiers"
      multivalue: true
      motif_du_nom: "« Domaines » designe deja les 20 dossiers de l arbre — l homonymie serait un piege."
      valeurs:
        - { cle: data-sci,  libelle: "Data Science",           couvre: "exploration, modélisation, viz, stats" }
        - { cle: data-eng,  libelle: "Data Engineering",       couvre: "pipelines, ELT, qualité, streaming" }
        - { cle: mlops,     libelle: "MLOps",                  couvre: "déploiement modèle, monitoring, infra ML" }
        - { cle: ml-eng,    libelle: "ML Engineering",         couvre: "entraînement scalable, optimisation" }
        - { cle: ai-eng,    libelle: "AI Engineering",         couvre: "apps LLM, RAG, agents, MCP" }
        - { cle: infra-ops, libelle: "Infrastructure & Ops",   couvre: "réseau, supervision, self-hosting, sécurité opérationnelle" }

champs:
  nom:        { type: ligne, fonction: identite,
                exemptions: "un nom portant / \\ : * ? \" < > | ne peut pas etre un nom de fichier" }
  alias:      { type: liste, fonction: alias, unicite: souple,
                motif: "L unicite globale detruirait shap, yolo, map." }
  pitch:      { type: ligne, fonction: resume_court, section: null }
  categorie:  { type: enum, source: axes.rangement }
  famille:    { type: enum, source: axes.nature }
  domaines:   { type: liste_enum, source: "axes.transverses[domaines]" }
  licence_type: { type: enum, valeurs: [open-source, source-available, proprietary, open-core] }
  maturite:   { type: enum, valeurs: [production, beta, experimental, deprecated],
                eliminatoire: [deprecated],
                motif: "Critere ELIMINATOIRE pour planifier-projet, seul depuis la
                        suppression de status: au lot 2." }
  hosted:     { type: liste_enum, valeurs: [self, managed],
                motif: "« both » ne disait rien qu une enumeration ne dise mieux." }
  scaling:    { type: enum, valeurs: [single-node, distributed, serverless] }
  langage:    { type: ligne }
  os:         { type: ligne }
  alternatives: { type: liens, reciproque: { mode: symetrique }, section: "Alternatives" }
  complements:  { type: liens, reciproque: { mode: symetrique }, section: "Compléments" }
  tags:       { type: liste_enum, source: "vocabulaires.tags" }
  url_docs:   { type: url }
  url_repo:   { type: url }

bandeau:
  porte_par: [brique]
  vide: "—"
  motif: >
    Le panneau natif d Obsidian est masque : 18 proprietes rendues avant le titre
    poussaient ## Definition sous la ligne de flottaison. Le lecteur a besoin de
    quatre faits, la machine des dix-huit.
  regle_dure: "Une cellule sans source dans le frontmatter affiche `vide`, jamais une valeur plausible."
  colonnes:
    - titre: Nature
      source: famille
      qualifie_par: langage
      table: { paquet: Librairie, plateforme: Plateforme, application: Application,
               cli: CLI, saas: SaaS, extension: Extension,
               specification: Spécification, modele: Modèle, annuaire: Annuaire }
    - titre: Licence
      source: licence_type
      table: { open-source: open-source, open-core: open-core,
               source-available: source-available, proprietary: propriétaire }
    - titre: Exécution
      source: famille
      table: { paquet: "en bibliothèque, rien à héberger",
               cli: "en ligne de commande, rien à héberger",
               extension: "dans le moteur hôte, rien à héberger",
               specification: "rien à exécuter", annuaire: "rien à exécuter",
               modele: "à charger dans un runtime" }
      depend_de: [hosted, scaling]     # pour les 3 familles hebergees
    - titre: Maturité
      source: maturite

regles:
  - id: reciprocite
    active: true
    severite: dure
    champs: [alternatives, complements]
    mesure: { date: 2026-09-06, population: 337, violations: 0 }
    motif: >
      R1 et R11 ne regardaient qu alternatives: — c est ce qui a laisse douze
      moities orphelines pendant tout le lot 6. Un couple non reciproque ne se
      voit pas en relisant une seule page.
  - id: chemin_categorie
    active: true
    severite: dure
  - id: completude_du_hub
    active: true
    severite: dure
    roles: [brique]
  - id: voisinage_declare
    active: true
    severite: avertissement
    definitif: true
    champ: alternatives
    mesure: { date: 2026-09-06, population: 337, violations: 62 }
    motif: "Une brique peut legitimement n avoir aucune alternative. La signaler aide, l interdire mentirait."
  - id: redirection_sourcee
    active: true
    severite: dure
    sections: ["Prendre si / Écarter si"]
    colonne: "Écarter si"
    marqueur: "→|->"
    condition: "la cible est une page fichée"
    mesure: { date: 2026-09-06, population: 1388, violations: 1 }
    motif: >
      Forme d origine (« toute cellule porte un wikilink ») : 357/1388, inatteignable.
      Position seule : 18. Condition seule : 177. La CONJONCTION : 1.
  - id: reinjection_du_resume
    active: true
    severite: dure
    champ_resume: pitch
    sections: [Alternatives, Compléments]
  - id: etiquettes_fermees
    active: true
    severite: { "Mise en œuvre": dure, "Ressources": avertissement }
    mesure: { "Ressources": { violations: 5, detail: "4 « Site », 1 « Poids »" } }
    motif: "Durcir Ressources demanderait d ouvrir le vocabulaire — arbitrage de floSa."
  - id: citation_unique
    active: true
    severite: dure
    sections: [Alternatives, Compléments, "Voir aussi"]
    definition_de_liste: "entrée de puce, pas lien cité dans une phrase"
    mesure: { toutes_sections: 242, entrees_de_puce: 0 }
  - id: bandeau_a_jour
    active: true
    severite: dure
  - id: anti_repetition
    active: false
    severite: avertissement
    definitif: true
    motif: >
      NON SCRIPTABLE. production, paquet, modele, application, open-source sont
      des mots francais ordinaires : 11 candidats, 2 vrais. Durcir rendrait la
      regle contournee, pas respectee.

seuils:
  comparatif_min_categorie: 3
  comparatif_min_membres: 2

vocabulaires:
  tags: { fichier: "Documentation/general/tags.md", mode: ferme,
          regle: "Le skill pioche, il n invente jamais. Un tag manquant se propose,
                  s ajoute ici, puis s utilise." }

graphe:
  ordre:
    - { requete: "path:Comparatifs/", couleur: "#EF4444",
        motif: "Point de ralliement des 47, pas un aiguillage de dossier — doit passer avant role:hub." }
    - { requete: "path:Métiers/",     couleur: "#FFD43B" }
    - { requete: 'role:hub',          couleur: "#FF922B" }
    - { requete: 'role:brique',       couleur: "#412CDD" }
    - { requete: 'role:notion',       couleur: "#7AB800" }
    - { requete: 'role:comparatif',   couleur: "#EF4444" }
    - { requete: 'role:pattern OR role:rule', couleur: "#94A3B8" }
  note: ".obsidian/graph.json est gitignore : cette table est la seule source, a reappliquer par poste."

genere:
  - "AI/index/"
  - "zones AUTO des hubs"
  - "Métiers/"
  - "Comparatifs/Comparatifs.md"
  - "bandeaux des briques"
  - "Documentation/general/taxonomie.md"
  - "Templates/"
  - "docs/"

skills:
  capture:      { nom: enrichir-brain }
  cloture:      { nom: cloturer-brain }
  exploitation: { nom: planifier-projet,
                  livrable: "cahier des charges sourcé qui contraint l'IA de dev",
                  archetypes: "Documentation/perso/archetypes.md",
                  questions:  "Documentation/general/questions-projet.md" }

agent:
  racine: "AI/"
  sous: [design/, migration/, index/, sessions/, scripts/, backlog.md]
```

## 2.3 Ce que le manifeste ne sait PAS redire — et c'est le résultat utile

Le test de fidélité ne se passe pas à 100 %, et l'honnêteté sur ces six points vaut
plus que le manifeste lui-même.

| # | Ce qui ne rentre pas | Conséquence de conception |
|---|---|---|
| 1 | **Les 47 filtres `.base`.** Chacun est une requête réglée à la main (`role == "brique"` **et** `categorie == …`, plus une seconde vue « Self-hostable » sur `hosted.contains("self")`). Le manifeste ne peut donner que l'ordre de colonnes par défaut et la forme du filtre. | Les vues restent des **fichiers de contenu**, pas des dérivés. Le générateur en **amorce** un, il ne les tient pas. |
| 2 | **L'algorithme de la règle 5.** La conjonction « il y a une flèche » × « la cible est une page fichée » n'est pas une donnée : c'est du code. Le manifeste ne déclare que la section, la colonne et le marqueur. | Le kit garde du **code par règle**. Le manifeste **branche** les règles, il ne les décrit pas. La liste des dix reste fermée par le kit. |
| 3 | **Le corps écrit à la main des 75 hubs** (`Ce qu'il faut comprendre`, `Choisir`). | Par conception. Le manifeste déclare la **place**, l'humain écrit le contenu. Le générateur d'un brain neuf pose la place vide. |
| 4 | **Le raisonnement derrière un arbitrage**, quand il fait plus d'une phrase. `motif:` porte « pourquoi ce libellé » ; il ne porte pas les quatre paragraphes de la remontée qui l'a produit. | `AI/migration/lot-N.md` reste le lieu du raisonnement, et le manifeste **pointe** vers lui. Le journal de lot n'est pas remplaçable par de la configuration. |
| 5 | **L'ordre historique.** Le manifeste décrit un **état**, pas un chemin. Il ne sait pas dire que `hosted:` était un scalaire avant le lot 2, ni que `Wiki/` a existé. | Un manifeste n'est pas un historique. C'est git et `AI/migration/` qui le sont — et §6 lot 9 en dépend. |
| 6 | **`os:` et `domaines:` sur une brique.** Ils sont dans `BRIQUE_ALLOWED` parce que les gabarits `service` et `outil` ont fusionné au lot 2 : leur présence est un vestige, pas une intention. | Le manifeste les déclare et perd l'information « c'est un vestige ». Ajouter `deprecated: true` sur un champ autorisé est une décision à prendre (§5 point 11). |

## 2.4 Rempli une seconde fois — un brain d'histoire

Seuls les blocs qui **changent** sont donnés ; tout ce qui n'apparaît pas ici est
identique en forme au remplissage DevBrain. Les cinq mécanismes qui cassent sont
signalés en ligne et détaillés en §4.

```yaml
manifeste: 1

brain:
  nom: HistoBrain
  sujet: "Ce que je lis en histoire, les sources qui l'établissent et les notions qui l'expliquent."
  langue: fr
  volume_cible: 3000        # -> seuil de promotion derive a 12, cf. §4 point 9
  usage: perso
  proprietaire: { nom: floSa }

libelles:
  unite:      { s: source, p: sources }
  notion:     { s: notion, p: notions }
  vue:        { s: chronologie, p: chronologies }   # PAS « comparatif » — §4 point 2
  axe_rangement: { s: période, p: périodes }
  axe_nature:    { s: nature, p: natures }

roles:
  - id: source
    fonction: unite
    libelle: { s: source, p: sources }
    range_par: axe
    protege: false
    pese_sur_le_seuil: true
    apparait_dans_le_hub: true
    couleur: "#412CDD"
    taille_avertissement: 120
    champs:
      requis: [role, nom, apport, categorie]
      autorises: [role, nom, alias, apport, categorie, nature, themes, espaces,
                  auteur, date_publication, langue, fiabilite, acces,
                  contredit, prolonge, prolonge_par, tags, url, cote]
      conditionnels:
        - { champ: langue_originale, si: "nature == source-primaire" }
        - { champ: traduction,       si: "nature == source-primaire" }
        - { champ: cote,             si: "nature in [archive, source-primaire]" }
      motif_conditionnels: >
        Reemploi direct du mecanisme R16 (E3) : une cote de fonds n a de sens
        que pour un document d archive, comme hosted: n en avait que pour une
        plateforme.
    corps:
      - { titre: "<bandeau>", niveau: 0, genre: bandeau }
      - { titre: "Ce que c'est", niveau: 2, genre: prose }
      - { titre: "Ce qu'elle établit / Ce qu'elle ne peut pas établir",
          niveau: 2, genre: decision,
          colonne_positive: "Établit",
          colonne_negative: "N'établit pas" }        # -> regle 5 transpose, §4 point 7
      - { titre: "Comment y accéder", niveau: 2, genre: etiquetee,
          obligatoires: [Édition, Langue, Accès, Cote, Coût] }
      - { titre: "Autour", niveau: 2, genre: libre }
      - { titre: "Contredit par", niveau: 3, genre: liste_liens, champ: contredit }
      - { titre: "Prolonge",      niveau: 3, genre: liste_liens, champ: prolonge }
      - { titre: "Prolongée par", niveau: 3, genre: liste_liens, champ: prolonge_par }
      - { titre: "Voir aussi",    niveau: 2, genre: liste_liens, champ: null }
      - { titre: "Notes de lecture", niveau: 2, genre: conditionnelle,
          existe_si: "au moins une entrée datée",
          forme: "- YYYY-MM-DD — <ce que j'y ai trouvé>." }

  - id: notion
    fonction: notion
    protege: true             # <- inchange, et c est ici que ca compte le plus (§4 point 10)
    range_par: axe
    couleur: "#7AB800"
    champs:
      requis: [role, nom, categorie, themes]
      autorises: [role, nom, alias, categorie, themes, espaces, tags]
    corps:
      - { titre: "Aperçu",              niveau: 2, genre: libre }
      - { titre: "Concepts clés",       niveau: 2, genre: libre }
      - { titre: "Ce qui fait débat",   niveau: 2, genre: libre }   # remplace « Les maths, simplement »
      - { titre: "En pratique",         niveau: 2, genre: libre }
      - { titre: "Notions voisines",    niveau: 2, genre: liste_liens, champ: null }
      - { titre: "Pour aller plus loin", niveau: 2, genre: libre }

  - id: chronologie
    fonction: vue
    libelle: { s: chronologie, p: chronologies }
    range_par: axe
    prefixe_nom: "Chronologie - "
    vue_embarquee: { extension: ".base", moteur: "obsidian-bases",
                     tri_par: date_evenement, direction: asc }
    regle_de_categorie: majorite       # <- reemploi de C2
    pese_sur_le_seuil: false
    couleur: "#EF4444"
    hub_de_ralliement: { dossier: "Chronologies", lien_retour: "Voir aussi" }
    corps:
      - { titre: "<accroche>", niveau: 0, genre: prose, forme: "La séquence : …" }
      - { titre: "<embed>",    niveau: 0, genre: auto }
      - { titre: "Ce que la séquence montre", niveau: 2, genre: liste_liens, champ: null }
      - { titre: "Voir aussi", niveau: 2, genre: liste_liens, champ: null }
    motif: >
      Ce rôle N EST PAS un comparatif traduit. Herodote et Thucydide ne sont pas
      des alternatives : on lit les deux. Ce qui survit du comparatif est la
      PRIMITIVE (page + vue filtree + section ecrite a la main) ; l intention
      « departager des interchangeables » ne survit pas. Cf. §4 point 2.

  - id: hub
    fonction: hub
    couleur: "#FF922B"

  - id: controverse
    fonction: prescription
    libelle: { s: controverse, p: controverses }
    range_par: role
    dossier: Controverses
    prefixe_nom: "Controverse - "
    couleur: "#94A3B8"
    champs:
      requis: [role, question, positions]
      autorises: [role, tags, question, positions, sources_cles, etat]
    motif: "Occupe la place de `pattern` (D1). Une controverse enjambe les periodes par construction."

  - id: methode
    fonction: prescription
    libelle: { s: méthode, p: méthodes }
    range_par: role
    dossier: Méthodes
    prefixe_nom: "Méthode - "
    couleur: "#94A3B8"
    champs:
      requis: [role, domaine, applicable, strictness]
      autorises: [role, tags, domaine, applicable, strictness]
    motif: >
      Occupe la place de `rule`, et c est la transposition la plus directe du
      DevBrain : « toute affirmation chiffree porte sa source primaire ou dit
      que c est une estimation » est une regle transverse avec un degre de
      fermete, exactement comme une Rule.

axes:
  rangement:
    champ: categorie
    exclusif: false                    # <- CASSE, §4 point 5
    motif_non_exclusif: >
      Une synthese « Histoire de la France des origines a nos jours » ne tombe
      dans aucune periode unique. DevBrain n a jamais eu ce cas : une brique a
      exactement un domaine. Deux mecanismes empruntes ailleurs le reparent —
      la regle de MAJORITE (C2, inventee pour les comparatifs) devient la regle
      generale de l axe, et un prefixe `transversal/*` accueille ce qui couvre
      vraiment tout.
    regle_de_majorite: true
    prefixe_transversal: transversal
    seuil_promotion: 12
    motif_seuil: "volume_cible 3000 / 8 prefixes -> ~375 pages par domaine. A 5, chaque domaine exploserait en 40 sous-dossiers."
    plafond_promotion: true
    prefixes:
      - { cle: prehistoire,  dossier: "Préhistoire" }
      - { cle: antiquite,    dossier: "Antiquité",
          sous: { proche-orient: {libelle: "Proche-Orient ancien"},
                  grece: {libelle: "Monde grec"},
                  rome: {libelle: "Rome"},
                  hors-mediterranee: {libelle: "Hors Méditerranée"} } }
      - { cle: medieval,     dossier: "Moyen Âge",
          sous: { haut: {libelle: "Haut Moyen Âge"}, feodal: {libelle: "Époque féodale"},
                  bas: {libelle: "Bas Moyen Âge"}, islam: {libelle: "Mondes de l'Islam"} } }
      - { cle: moderne,      dossier: "Époque moderne",
          sous: { renaissance: {libelle: Renaissance}, reformes: {libelle: Réformes},
                  colonial: {libelle: "Premières colonisations"}, lumieres: {libelle: Lumières} } }
      - { cle: revolutions,  dossier: "Révolutions et empires" }
      - { cle: industriel,   dossier: "Âge industriel" }
      - { cle: xxe,          dossier: "XXe siècle",
          sous: { gm1: {libelle: "Première Guerre mondiale"},
                  entre-deux: {libelle: "Entre-deux-guerres"},
                  gm2: {libelle: "Seconde Guerre mondiale"},
                  guerre-froide: {libelle: "Guerre froide"},
                  decolonisation: {libelle: Décolonisations} } }
      - { cle: transversal,  dossier: "Transversal",
          motif: "Le prefixe qui repare la non-exclusivite. Reserve aux syntheses de longue duree." }
    arbre_de_decision:
      - { n: D1, question: "La source porte-t-elle sur plus de trois des périodes ci-dessous ?", si_oui: "transversal/*" }
      - { n: D2, question: "Est-elle antérieure à l'écriture ?", si_oui: "prehistoire/*" }
      - { n: D3, question: "Son objet est-il antérieur à 476 ?", si_oui: "antiquite/*" }
      # … D4 a D8, dans l ordre chronologique
      - { n: D9, question: "Aucun des précédents", si_oui: "ARRÊT — demander" }
    departages: []                     # NAIT VIDE (F2, principe 2)
    frontieres: []                     # idem

  nature:
    champ: nature
    porte_par: [source]
    vide_autorise: true
    valeurs:
      - { cle: source-primaire, definition: "Produite par les contemporains du fait." }
      - { cle: archive,         definition: "Document non publié, conservé en fonds, avec une cote." }
      - { cle: ouvrage,         definition: "Livre d'auteur, appareil critique." }
      - { cle: article,         definition: "Publié dans une revue à comité." }
      - { cle: these,           definition: "Travail universitaire soutenu." }
      - { cle: cours,           definition: "Enseignement structuré (MOOC, séminaire, manuel)." }
      - { cle: carte,           definition: "Représentation spatiale." }
      - { cle: iconographie,    definition: "Image, photo, film comme document." }
      - { cle: base-de-donnees, definition: "Corpus interrogeable (recensements, prosopographie)." }
    arbre_de_decision:
      - { n: N1, question: "Le document est-il contemporain du fait qu'il rapporte ?", si_oui: source-primaire }
      - { n: N2, question: "Est-il conservé en fonds sans avoir été publié ?", si_oui: archive }
      # … N3 a N8
      - { n: N9, question: "Aucun des précédents", si_oui: ouvrage }
    departages: []

  transverses:                          # DEUX, la ou DevBrain n en a qu UN — §4 point 4
    - champ: themes
      dossier: "Thèmes"
      multivalue: true
      valeurs:
        - { cle: politique,  libelle: "Pouvoir et institutions" }
        - { cle: economie,   libelle: "Économies et échanges" }
        - { cle: social,     libelle: "Sociétés et travail" }
        - { cle: religieux,  libelle: "Croyances et religions" }
        - { cle: guerre,     libelle: "Guerres et armées" }
        - { cle: culture,    libelle: "Cultures et savoirs" }
        - { cle: technique,  libelle: "Techniques et environnement" }
    - champ: espaces
      dossier: "Espaces"
      multivalue: true
      valeurs:
        - { cle: france,        libelle: "France" }
        - { cle: europe,        libelle: "Europe" }
        - { cle: mediterranee,  libelle: "Méditerranée" }
        - { cle: asie,          libelle: "Asie" }
        - { cle: afrique,       libelle: "Afrique" }
        - { cle: ameriques,     libelle: "Amériques" }
        - { cle: mondial,       libelle: "Échelle mondiale" }

champs:
  apport:     { type: ligne, fonction: resume_court }   # remplace `pitch`
  auteur:     { type: ligne }
  date_publication: { type: date }
  langue:     { type: ligne }
  fiabilite:  { type: enum,
                valeurs: [etablie, discutee, contestee, obsolete],
                eliminatoire: [],                        # <- VIDE, et c est le point : §4 point 6
                motif: >
                  Transposition exacte de maturite:, MAIS sans valeur eliminatoire.
                  Une source contestee est souvent celle qui interesse le plus.
                  Le manifeste ne doit donc jamais mettre de valeur par defaut ici. }
  acces:      { type: enum, valeurs: [libre, abonnement, papier, sur-place] }
  cote:       { type: ligne }
  contredit:  { type: liens, reciproque: { mode: symetrique }, section: "Contredit par",
                motif: "Une contradiction est symetrique par nature — reciprocite dure, comme alternatives:." }
  prolonge:   { type: liens, reciproque: { mode: inverse, champ: prolonge_par },
                section: "Prolonge",
                motif: >
                  MODE INVERSE, absent de DevBrain. « A prolonge B » n implique pas
                  « B prolonge A » : il implique « B est prolonge par A ». Le moteur
                  de reciprocite doit gerer une PAIRE de champs, pas un miroir. §4 point 3. }
  prolonge_par: { type: liens, reciproque: { mode: inverse, champ: prolonge },
                  section: "Prolongée par" }

bandeau:
  porte_par: [source]
  vide: "—"
  colonnes:
    - { titre: Nature,   source: nature,
        table: { source-primaire: "Source primaire", archive: Archive,
                 ouvrage: Ouvrage, article: Article, these: Thèse, cours: Cours,
                 carte: Carte, iconographie: Iconographie,
                 base-de-donnees: "Base de données" } }
    - { titre: "Auteur et date", source: auteur, qualifie_par: date_publication }
    - { titre: Langue,   source: langue }
    - { titre: Fiabilité, source: fiabilite,
        table: { etablie: "établie", discutee: "discutée",
                 contestee: "contestée", obsolete: "obsolète" } }

regles:
  # TOUTES en `a_mesurer`, sans exception : principe 1. Aucune severite du DevBrain
  # n est heritee, y compris celles qui « paraissent evidentes ».
  - { id: reciprocite,          active: true,  severite: a_mesurer, champs: [contredit, prolonge] }
  - { id: chemin_categorie,     active: true,  severite: a_mesurer }
  - { id: completude_du_hub,    active: true,  severite: a_mesurer, roles: [source] }
  - { id: voisinage_declare,    active: false, severite: a_mesurer,
      motif: "Desactivee au demarrage : dans un brain de sources, l absence de voisin est la norme, pas l exception." }
  - { id: redirection_sourcee,  active: true,  severite: a_mesurer,
      sections: ["Ce qu'elle établit / Ce qu'elle ne peut pas établir"],
      colonne: "N'établit pas", marqueur: "→|->" }
  - { id: reinjection_du_resume, active: true, severite: a_mesurer, champ_resume: apport }
  - { id: etiquettes_fermees,   active: true,  severite: a_mesurer }
  - { id: citation_unique,      active: true,  severite: a_mesurer,
      sections: ["Contredit par", "Prolonge", "Prolongée par", "Voir aussi"] }
  - { id: bandeau_a_jour,       active: true,  severite: a_mesurer }
  - { id: anti_repetition,      active: false, severite: avertissement,
      motif: "Non livree. « ouvrage », « article », « source » sont les mots les plus frequents du corpus." }

skills:
  capture:      { nom: enrichir-histobrain }
  cloture:      { nom: cloturer-histobrain }
  exploitation: { nom: preparer-un-propos,
                  livrable: "un plan sourcé — cours, article ou note — où chaque affirmation porte sa source",
                  archetypes: "Documentation/perso/usages.md" }
```
