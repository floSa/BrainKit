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
