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

---

# 3. L'entretien d'initialisation

## 3.0 Ce que l'entretien est

Un skill, invoqué une seule fois dans la vie d'un brain, à l'ouverture d'un vault
vierge. Il ne produit **qu'une chose** : un `brain.yml` valide. La génération de
l'arborescence, des gabarits et des skills n'est pas son travail — c'est celui du
générateur qu'il appelle en dernière étape (§6, lot 5).

Trois propriétés de conduite, et elles ne sont pas décoratives :

- **Il induit, il ne propose pas.** La tentation évidente est de présenter à
  l'utilisateur une liste de 20 domaines candidats à cocher. C'est exactement ce
  qu'il faut refuser : un utilisateur coche par politesse, et le brain hérite d'une
  taxonomie qui n'est pas la sienne. L'entretien lui fait **citer des pages réelles**
  et en **induit** les paquets.
- **Il ne devine aucune sévérité.** Toutes les règles sortent en `a_mesurer`. Il
  n'existe aucun cas où l'entretien écrit `dure`.
- **Il s'arrête à zéro page de contenu.** Aucune source, aucune notion, aucun
  contenu de page. Ce qui a été cité pendant l'entretien part dans `Inbox.md` comme
  liste de travail, pas comme pages.

## 3.1 Les onze passes, dans l'ordre

L'ordre est la seule décision de conception de l'entretien, et il est contraint :
chaque passe a besoin de la réponse de la précédente. On ne peut pas demander les
sections du corps avant de savoir quelle est l'unité, ni le seuil de promotion avant
le volume cible.

### Passe 0 — Identité et dépôt (5 questions)

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 0.1 | De quoi ce brain parle-t-il, en une phrase ? | `brain.sujet` | Ne jamais reformuler en mieux : la phrase de l'utilisateur est la bonne. |
| 0.2 | Comment veux-tu l'appeler ? | `brain.nom`, nom du dépôt et du coffre | — |
| 0.3 | Ce brain est-il personnel, professionnel, ou celui d'un client ? | `brain.usage`, et la **polarité** du garde-fou d'identité (M2) | — |
| 0.4 | Sous quel nom et quelle adresse ses commits doivent-ils être signés ? | `git.identite` | **REFUS ABSOLU de deviner.** Ne jamais reprendre l'adresse annoncée par le harnais. Si l'utilisateur ne répond pas, l'entretien s'arrête là. |
| 0.5 | Quelle adresse ne doit *jamais* apparaître dans un commit ici ? | `git.domaines_refuses` | — |

### Passe 1 — L'unité (4 questions) — la passe qui commande tout

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 1.1 | Dans six mois, tu ouvres ce brain pour t'en servir. **Qu'est-ce que tu vas chercher ?** | Identifie l'unité : `fonction: unite` | Ne jamais nommer l'unité soi-même. |
| 1.2 | Comment appelles-tu cette chose, au singulier et au pluriel ? | `roles[].id`, `libelles.unite` | **REFUS de traduire depuis le dev.** « brique » ne sort jamais de la bouche de l'entretien. |
| 1.3 | Y a-t-il, à côté, des pages qui n'expliquent pas *quoi utiliser* mais *ce qu'il faut comprendre* ? | Crée ou non un rôle `fonction: notion` | Réponse « non » légale : un brain sans notions est valide. |
| 1.4 | Y a-t-il des pages que **tu** écris pour toi, et que l'IA ne doit pas réécrire sans te demander ? | `protege: true` sur les rôles concernés | Ne jamais poser `protege: true` par défaut, ni le refuser. |

### Passe 2 — L'axe qui range (7 questions) — la passe la plus longue, et la plus payante

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 2.1 | Cite-moi **vingt pages** que tu voudrais dans ce brain. Des vraies, pas des catégories. | L'échantillon d'induction | **REFUS de proposer les vingt.** L'entretien attend, quitte à revenir. Moins de dix : il redemande, l'induction ne tient pas. |
| 2.2 | Range ces vingt en paquets, **de ta main**. Combien de paquets, et comment les appelles-tu ? | `axes.rangement.prefixes[]` — les dossiers de domaine | **REFUS de proposer les paquets.** C'est le cœur de la méthode : la taxonomie est induite d'un échantillon réel. |
| 2.3 | Chacune de tes vingt pages tombe-t-elle dans **exactement un** paquet ? | `axes.rangement.exclusif` | Si « non » : ne pas passer outre. Poser 2.4. |
| 2.4 | *(si 2.3 = non)* Pour celles qui débordent : est-ce qu'un paquet **domine** quand même, ou couvrent-elles vraiment tout ? | `regle_de_majorite: true` et/ou `prefixe_transversal` | Ne jamais forcer une valeur unique pour faire passer la contrainte. C'est le cas histoire, §4 point 5. |
| 2.5 | Comment appelles-tu ce que ces paquets sont ? (« domaine », « période », « client », « discipline »…) | `libelles.axe_rangement` | — |
| 2.6 | Combien de pages ce brain aura-t-il **quand il sera plein** ? Un ordre de grandeur suffit. | `brain.volume_cible`, dont le **seuil de promotion se dérive** | **REFUS de demander le seuil directement.** L'utilisateur n'a aucun moyen de le connaître ; le volume, si. |
| 2.7 | Pour chaque paire de paquets qui pourrait se disputer une page : quelle **question fermée** tranche, et laquelle passe en premier ? | `axes.rangement.arbre_de_decision[]` | **REFUS de fabriquer l'ordre.** L'ordre est *la* décision de conception ; l'IA peut proposer les questions, jamais leur rang. |

`departages[]` et `frontieres[]` sortent **vides**, et l'entretien le dit à haute
voix : « ces deux listes se rempliront page par page, quand un arbitrage se répétera.
Les remplir maintenant serait inventer des problèmes qu'on n'a pas. »

### Passe 3 — L'axe qui qualifie (4 questions)

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 3.1 | Deux pages du **même paquet** peuvent-elles être de deux natures très différentes ? | Crée ou non `axes.nature` | Réponse « non » **légale et fréquente** : un brain sans axe de nature est valide, et l'entretien ne doit pas insister. |
| 3.2 | *(si oui)* En regardant tes vingt pages : quelles natures vois-tu ? | `axes.nature.valeurs[]` avec définitions | Induit de l'échantillon, jamais listé d'avance. |
| 3.3 | Dans quel ordre les questions fermées qui les séparent ? | `axes.nature.arbre_de_decision[]` | Idem 2.7. |
| 3.4 | Y a-t-il des informations qui n'ont de sens que pour **certaines** de ces natures ? | `champs.conditionnels` (E3) | — |

L'entretien inscrit `vide_autorise: true` et l'explique : *un champ vide est le seul
signal prévu pour « l'arbre n'a pas tranché » ; une valeur inventée est une faute,
un champ vide est une question ouverte.*

### Passe 4 — Les axes transverses (3 questions)

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 4.1 | Y a-t-il une question que tu poseras au brain et qui **traverse tous les paquets** ? | Zéro, un ou plusieurs `axes.transverses[]` | **REFUS d'en inventer un.** Zéro axe transverse est légal, et le générateur ne créera alors aucun dossier. |
| 4.2 | *(par axe)* Une page en porte-t-elle une seule valeur, ou plusieurs ? | `multivalue` | — |
| 4.3 | *(par axe)* Comment appelles-tu le dossier qui les rassemble ? | `dossier` | Vérifier qu'il ne redouble aucun nom de l'axe de rangement — le DevBrain a nommé `Métiers/` et non `Domaines/` pour cette raison exacte. |

### Passe 5 — Le haut de page (3 questions)

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 5.1 | Tu ouvres une page. **Avant le texte**, quels trois à cinq faits veux-tu voir ? | `bandeau.colonnes[]` | Plus de cinq : redemander. Le bandeau existe *parce que* dix-huit propriétés poussaient le texte sous la ligne de flottaison. |
| 5.2 | *(par colonne)* D'où vient ce fait — quel champ du frontmatter le porte ? | `colonnes[].source` | **REFUS d'une colonne sans source.** Une colonne dérivée d'un jugement, pas d'un champ, n'entre pas dans le bandeau. |
| 5.3 | Et quand un de ces faits manque sur une page, on affiche quoi ? | `bandeau.vide` | Proposer le tiret cadratin et la règle : *une cellule sans source affiche un tiret, jamais une valeur plausible.* |

### Passe 6 — Le corps (5 questions)

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 6.1 | Sur une page d'unité, que veux-tu lire, **dans l'ordre** ? | `roles[].corps[]` — les titres et leur rang | Ne pas proposer les titres du DevBrain. |
| 6.2 | Laquelle de ces sections est une **prose** ? | `genre: prose` | Une seule, en principe. Si l'utilisateur en veut trois, le dire : la doctrine du lot 6 est *aucune prose hors de la section de définition*, et elle a une raison mesurée. |
| 6.3 | Y a-t-il une section où tu **décides** — d'un côté ce qui va, de l'autre ce qui ne va pas ? | `genre: decision`, et la règle 5 se branche | Réponse « non » légale. La règle 5 se désactive alors, elle ne se force pas. |
| 6.4 | Y a-t-il une section qui est une **liste de liens** vers d'autres pages ? Lesquelles ? | `genre: liste_liens`, et les règles 1, 6, 8 se branchent | — |
| 6.5 | Y a-t-il une section **étiquetée** — des puces « Étiquette — valeur » ? Quelles étiquettes exactement, et lesquelles sont obligatoires ? | `genre: etiquetee`, vocabulaire fermé, règle 7 | **REFUS de compléter le vocabulaire.** Cinq étiquettes nommées par l'utilisateur valent mieux que sept dont deux inventées. |

### Passe 7 — Les liens et le résumé (4 questions)

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 7.1 | Deux pages peuvent-elles être en **opposition** ? En **complément** ? Autrement ? | Les champs `type: liens` | — |
| 7.2 | *(par relation)* Si A est dans cette relation avec B, est-ce que **B est dans la même relation avec A** ? | `reciproque: {mode: symetrique}` | — |
| 7.3 | *(si non)* Comment se dit la relation **dans l'autre sens** ? | `reciproque: {mode: inverse, champ: …}` | **REFUS de forcer la symétrie.** C'est le trou de DevBrain, découvert en §4 point 3 : « A prolonge B » n'est pas « B prolonge A ». |
| 7.4 | Quel champ est le **résumé d'une ligne** qu'on recopiera chez tous ceux qui citent la page ? | `fonction: resume_court`, règle 6 | Si aucun : la règle 6 se désactive. Ne pas en inventer un. |

### Passe 8 — Ce qui rassemble (3 questions) — la passe qui sauve le comparatif

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 8.1 | Tes unités sont-elles **interchangeables** ? En choisit-on une **contre** une autre ? | Si oui : un rôle `fonction: vue` orienté « départager » | — |
| 8.2 | *(si non)* Y a-t-il quand même une **table** que tu voudrais voir, une liste filtrée sur un paquet, triée sur quelque chose ? | Un rôle `fonction: vue` orienté « séquence » ou « panorama », avec son `tri_par` | **REFUS de traduire le comparatif.** Si les unités ne sont pas interchangeables, le mot « comparatif » ne doit pas apparaître. Cf. §4 point 2. |
| 8.3 | *(si un rôle `vue` existe)* Veux-tu un dossier qui les rassemble tous ? | `hub_de_ralliement` et son lien retour | Rappeler pourquoi : *c'est le lien retour qui fait la grappe* (B5). |

### Passe 9 — Gouvernance et frontières (4 questions)

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 9.1 | Les mots-clés transverses : vocabulaire **fermé** (on propose avant d'ajouter) ou libre ? | `vocabulaires.tags.mode` | Recommander `ferme` et dire pourquoi, mais accepter `libre`. |
| 9.2 | Une suppression de page : permise, ou toujours à te demander ? | La frontière du `CLAUDE.md` généré | — |
| 9.3 | Y a-t-il un second mode — travailler **depuis** ce brain, dans un autre dépôt ? | Génère ou non un `CLAUDE-consommation.md` | Réponse « non » légale ; le DevBrain en a un parce que son consommateur est un dépôt de code. |
| 9.4 | Quels chemins ne doivent **jamais** être édités à la main ? | `genere[]` | Proposer la liste déduite du manifeste, la faire confirmer. |

### Passe 10 — L'exploitation (3 questions)

| Q | Question | Ce qu'elle produit | Refus |
|---|---|---|---|
| 10.1 | Que produiras-tu **à partir** de ce brain ? | `skills.exploitation.livrable` | **REFUS de deviner.** C'est la question qui décide si le troisième skill est un cadreur de projet, un préparateur de propos, ou une note de synthèse client. |
| 10.2 | Ce livrable a-t-il des **formes types** ? Lesquelles ? | Les archétypes du skill d'exploitation | Zéro archétype légal au démarrage. |
| 10.3 | Quelles questions faut-il te poser avant de produire ce livrable ? | La check-list du skill | Induire des réponses précédentes, faire compléter. |

## 3.2 La clôture de l'entretien

Avant d'écrire quoi que ce soit, l'entretien **redit le manifeste en prose**, en
français, en une vingtaine de lignes : « ton brain s'appelle X, il parle de Y ; son
unité est la *source* ; il se range par *période*, en huit paquets ; une source
porte une *nature* prise dans neuf valeurs ; deux axes le traversent ; le haut de
page montre quatre faits ; les dix règles sont **toutes en attente de mesure** ».

Puis **un seul oui**. Pas une validation par bloc : l'utilisateur doit voir
l'ensemble d'un coup, parce que les incohérences sont entre les blocs, pas dedans.

Ensuite, et alors seulement, l'entretien appelle le générateur.

## 3.3 Ce qui est généré à la fin

| Ce qui est écrit | Depuis quoi |
|---|---|
| `brain.yml` | l'entretien |
| L'arbre des dossiers de domaine, **avec un hub à zéro entrée par dossier** | `axes.rangement.prefixes` |
| Les dossiers des rôles `range_par: role`, avec leur hub | `roles[]` |
| Les dossiers des axes transverses, avec un hub par valeur | `axes.transverses[]` |
| Un gabarit par rôle dans `Templates/` | `roles[].champs` et `roles[].corps` |
| `Documentation/<axe>/taxonomie.md` — les vocabulaires, les arbres, les places vides pour les départages | `axes` |
| `Documentation/.../tags.md` — l'en-tête et la règle, vocabulaire vide | `vocabulaires` |
| Les deux validateurs, **branchés** sur `brain.yml` (pas copiés) | le kit |
| Les quatre générateurs, idem | le kit |
| Les trois skills, instanciés avec le vocabulaire du brain, table de propagation **dérivée** | `libelles`, `roles`, `skills` |
| `CLAUDE.md` + le contexte de mode, avec la **règle d'identité git en tête** | `brain`, `git`, `roles[].protege` |
| `.githooks/` (les trois) + `core.hooksPath` + l'identité en config locale | `git` |
| La table de couleurs du graphe et son étape d'installation | `graphe` |
| `Home.md`, `Inbox.md`, `AI/` (design, migration, index, sessions, scripts) | `agent` |
| `INSTALL.md` et les guides, générés | tout le manifeste |
| Le premier fichier de `AI/migration/` : **le journal du lot 1 du brain**, vide, avec sa section *Remontées* | — |

## 3.4 Où l'entretien s'arrête, où le remplissage commence

**La frontière est nette et elle est vérifiable :** l'entretien se termine quand les
deux validateurs sont **verts sur un brain à zéro page d'unité**. C'est son critère
d'acceptation, et c'est le seul.

Concrètement, à la fin de l'entretien :

- il existe un hub par dossier, et **aucune** autre page ;
- `check_arbo` compte « 0 page rangée » et ne trouve aucun écart ;
- `check_brain` valide les hubs et ne trouve aucune violation ;
- **les vingt pages citées en passe 2.1 sont dans `Inbox.md`**, en liste à traiter,
  et pas une n'a été écrite. C'est le point qui distingue l'entretien du
  remplissage : l'entretien a *utilisé* ces vingt titres pour induire la taxonomie,
  il ne les a pas capturés.

Le remplissage commence au premier appel du skill de capture. C'est un autre skill,
un autre commit, et il obéit à la règle de propagation — laquelle n'a rien à faire
tant qu'il n'y a qu'un hub par dossier.

## 3.5 Ce que l'entretien doit REFUSER de deviner, et redemander

Récapitulatif, parce que c'est la partie du skill qui se dégrade le plus vite si
elle n'est pas écrite comme une liste fermée :

| # | Ce qu'il ne devine jamais | Ce qu'il fait à la place |
|---|---|---|
| 1 | **L'identité git**, sous aucune forme | Redemande, et s'arrête si la réponse ne vient pas. Ne lit **jamais** l'adresse annoncée par le harnais. |
| 2 | **Le nom de l'unité** et la liste des rôles | Fait décrire l'usage (1.1) et reprend les mots de l'utilisateur. |
| 3 | **Les paquets de l'axe de rangement** | Fait citer vingt pages réelles et les fait ranger à la main. Jamais de liste à cocher. |
| 4 | **Le seuil de promotion** | Demande le volume cible et *dérive*, en écrivant le calcul dans `motif_seuil`. |
| 5 | **L'ordre des arbres de décision** | Peut proposer les questions ; l'ordre reste à l'utilisateur, et il l'annonce comme *la* décision de conception. |
| 6 | **Toute sévérité de règle** | Écrit `a_mesurer` partout. Ne sait pas écrire `dure`. |
| 7 | **Le vocabulaire de tags** | Laisse le fichier vide avec sa règle. |
| 8 | **Une valeur de l'axe de nature quand l'arbre ne tranche pas** | Laisse le champ vide — c'est le signal prévu — et le dit. |
| 9 | **L'existence d'un rôle `vue`** | Passe 8. Si les unités ne sont pas interchangeables, ne traduit pas le comparatif. |
| 10 | **L'existence d'un axe transverse** | Zéro est une réponse. Ne crée aucun dossier par analogie avec `Métiers/`. |
| 11 | **Les règles de départage et les frontières** | Les laisse vides, et dit qu'elles se rempliront page par page. |
| 12 | **Une colonne de bandeau sans champ source** | Refuse la colonne et redemande d'où vient le fait. |
| 13 | **Le livrable du skill d'exploitation** | Passe 10.1. Sans réponse, le skill n'est pas généré — mieux vaut deux skills que trois dont un inventé. |

---

# 4. Le test à blanc « histoire »

But du test : **trouver ce qui casse**. Un test à blanc qui conclut « tout passe »
n'a pas été fait. Douze points sont sortis ; cinq sont de vraies ruptures, quatre
sont des transpositions propres qui valident un mécanisme, trois sont des
insuffisances du **code actuel** que le manifeste seul ne répare pas.

## 4.1 L'entretien, déroulé

**Passe 0** — HistoBrain ; « ce que je lis en histoire, les sources qui l'établissent
et les notions qui l'expliquent » ; `usage: perso` ; identité perso ; domaine pro
refusé. Rien de neuf : la passe 0 est indifférente au sujet.

**Passe 1** — 1.1 : *« je vais chercher sur quoi appuyer une affirmation »*. L'unité
est donc la **source**, pas le fait ni le personnage. 1.2 : « source / sources ».
1.3 : oui — la féodalité, le mercantilisme, l'Anschluss ne sont pas des sources, ce
sont des choses à comprendre → un rôle `notion`. 1.4 : oui, les notions → `protege: true`.

**Passe 2** — 2.1, vingt titres cités : *Thucydide, La Guerre du Péloponnèse* ·
*Hérodote, Enquête* · *Duby, Les trois ordres* · *Braudel, La Méditerranée* ·
*Bloch, La société féodale* · *Le Roy Ladurie, Montaillou* · *Hobsbawm, L'ère des
révolutions* · *Paxton, La France de Vichy* · *Kershaw, Hitler* · *Cours du Collège
de France sur les Lumières* · *Édit de Nantes (texte)* · *Cahiers de doléances
(fonds)* · *Recensement de 1851 (base)* · *Carte des mobilités antiques
(ORBIS)* · *Actes du concile de Trente* · *Un article de revue sur la peste noire* ·
*Une thèse sur les ouvriers du textile lyonnais* · *Photographies de la Commune* ·
*Manuel de paléographie* · *Histoire de la France des origines à nos jours*.

2.2, l'utilisateur range de sa main. Il fait **huit paquets**, et il les nomme par
**période** : Préhistoire, Antiquité, Moyen Âge, Époque moderne, Révolutions et
empires, Âge industriel, XXe siècle — et un huitième qu'il crée en cours de route
pour la vingtième page : *Transversal*.

> **C'est le premier résultat du test, et il tombe à la question 2.2.** L'utilisateur
> n'a pas rangé par thème ni par espace. Il a rangé par période, spontanément, parce
> que c'est l'axe qui **exclut** — une source antique n'est pas une source moderne —
> alors que le thème et l'espace se cumulent. La méthode d'induction a produit le bon
> axe sans qu'on ait eu à en discuter.

2.3 : non — deux pages débordent (*Braudel* enjambe Antiquité à Moderne, *Histoire de
la France* couvre tout). 2.4 : Braudel a un centre de gravité (l'époque moderne),
*Histoire de la France* n'en a pas. → `regle_de_majorite: true` **et**
`prefixe_transversal: transversal`. 2.5 : « période ». 2.6 : « trois mille pages,
peut-être ». → seuil dérivé à **12**. 2.7 : l'utilisateur donne un arbre
chronologique, avec une seule question hors chronologie **en premier** : *« porte-t-elle
sur plus de trois périodes ? »*.

**Passe 3** — 3.1 : oui, franchement. Un texte de l'Édit de Nantes et un livre de
Duby sont dans le même paquet et ne se lisent pas du tout pareil. 3.2 : neuf natures.
3.4 : oui — une cote de fonds n'a de sens que pour une archive ; une langue originale
et une traduction, que pour une source primaire.

**Passe 4** — 4.1 : deux axes. *Thèmes* (politique, économie, social, religieux,
guerre, culture, technique) et *Espaces* (France, Europe, Méditerranée, Asie,
Afrique, Amériques, mondial). Tous deux multivalués.

**Passe 5** — quatre faits : Nature · Auteur et date · Langue · Fiabilité.

**Passe 6** — corps : *Ce que c'est* (prose) · *Ce qu'elle établit / Ce qu'elle ne
peut pas établir* (décision) · *Comment y accéder* (étiquetée : Édition, Langue,
Accès, Cote, Coût) · *Autour* avec trois listes de liens · *Voir aussi* · *Notes de
lecture* (conditionnelle et datée).

**Passe 7** — deux relations, et la seconde casse quelque chose : *contredit* est
symétrique ; *prolonge* ne l'est pas.

**Passe 8** — 8.1 : **non**, les sources ne sont pas interchangeables. 8.2 : oui, une
table par période, **triée par date**. → rôle `chronologie`, `hub_de_ralliement`
`Chronologies/`.

**Passe 9 / 10** — tags fermés ; suppression sur demande ; pas de second mode ;
livrable : *un plan sourcé — cours, article ou note*.

## 4.2 L'arborescence qui en sort

```
Préhistoire/
└── Préhistoire.md                            (hub)
Antiquité/
├── Antiquité.md                              (hub)
├── Proche-Orient ancien/  Monde grec/  Rome/  Hors Méditerranée/
│   └── <Sous-domaine>.md                     (hub) + sources, notions, chronologies
└── <sources et notions restées au niveau de la période>
Moyen Âge/
├── Moyen Âge.md
└── Haut Moyen Âge/  Époque féodale/  Bas Moyen Âge/  Mondes de l'Islam/
Époque moderne/
├── Époque moderne.md
└── Renaissance/  Réformes/  Premières colonisations/  Lumières/
Révolutions et empires/    Âge industriel/
XXe siècle/
├── XXe siècle.md
└── Première Guerre mondiale/  Entre-deux-guerres/  Seconde Guerre mondiale/
    Guerre froide/  Décolonisations/
Transversal/
└── Transversal.md                            (le paquet né à la question 2.4)

Thèmes/     ← 7 hubs générés depuis `themes:`      (axe transverse 1)
Espaces/    ← 7 hubs générés depuis `espaces:`     (axe transverse 2)
Chronologies/ ← Chronologies.md et RIEN d'autre    (hub de ralliement du rôle `vue`)
Controverses/ ← Controverses.md + Controverse - <question>.md
Méthodes/     ← Méthodes.md + Méthode - <nom>.md
Documentation/  Templates/  AI/  Home.md  Inbox.md
```

Vingt-huit dossiers de domaine et de sous-domaine, contre vingt et quatre-vingt-quinze
dans le DevBrain. Les **rôles** : `source`, `notion`, `hub`, `chronologie`,
`controverse`, `methode` — six, comme le DevBrain, et **aucun** ne porte le même nom.
Les **natures** : neuf, comme les familles du DevBrain, par coïncidence.

Un exemple de page pour fixer les idées — `Moyen Âge/Époque féodale/Bloch - La
société féodale.md` :

```yaml
role: source
nom: "Bloch - La société féodale"
apport: "Fonde la lecture de la féodalité comme rapport social total, pas comme régime juridique."
categorie: medieval/feodal
nature: ouvrage
themes: [social, politique]
espaces: [france, europe]
auteur: "Marc Bloch"
date_publication: 1939
langue: fr
fiabilite: etablie
acces: papier
contredit: []
prolonge: []
prolonge_par: ["[[Duby - Les trois ordres]]"]
```

`Nature | Auteur et date | Langue | Fiabilité` rendus en bandeau :
« Ouvrage | Marc Bloch, 1939 | fr | établie ». Trois lignes, comme pour Qdrant.

## 4.3 Ce qui casse — les cinq vraies ruptures

### Rupture 1 — le rôle `comparatif` ne survit pas

**Ce qui casse.** Le comparatif présuppose des objets **interchangeables**, classés
sur des axes partagés, dont on choisit **un**. Hérodote et Thucydide ne sont pas des
alternatives : on lit les deux, et le second corrige le premier sans le remplacer.
La section « Ce qui départage » n'a pas d'objet, et la phrase d'accroche « On tranche
sur : … » est fausse à l'écrit.

**Ce qui survit, précisément.** La **primitive** : une page `.md` qui embarque une
vue `.base` filtrée sur une valeur de l'axe de rangement, plus une section écrite à
la main, plus un hub de ralliement avec lien retour. Cette primitive est excellente
et elle se réemploie telle quelle. Ce qui ne survit pas, c'est l'**intention**.

**Conséquence.** Le manifeste ne doit pas offrir un rôle « comparatif » : il doit
offrir la fonction `vue`, avec un `tri_par` et un titre de section libres. Le
DevBrain instancie « départager » ; HistoBrain instancie « mettre en séquence ». Et
l'entretien doit poser la question 8.1 avant 8.2, sans quoi il traduira le
comparatif par réflexe.

**Coût :** faible. C'est une généralisation, pas une perte.

### Rupture 2 — la réciprocité a besoin d'un mode INVERSE, que DevBrain n'a jamais eu

**Ce qui casse.** `alternatives:` et `complements:` sont tous deux **symétriques** :
si A est une alternative de B, B est une alternative de A. Les deux seuls champs de
liens réciproques du DevBrain le sont, donc `CHAMPS_ECOSYSTEME` ne connaît qu'un
mode — le miroir.

En histoire, `contredit:` est symétrique (une contradiction l'est par nature, et
c'est une jolie confirmation). Mais `prolonge:` **ne l'est pas** : « Duby prolonge
Bloch » n'implique pas « Bloch prolonge Duby ». Il implique « Bloch **est prolongé
par** Duby ». La relation demande une **paire** de champs, pas un miroir.

**Conséquence.** `champs[].reciproque` doit prendre trois formes : `null`,
`{mode: symetrique}`, `{mode: inverse, champ: <l'autre>}`. Le moteur de réciprocité
change : il vérifie que `A.prolonge ∋ B` **si et seulement si** `B.prolonge_par ∋ A`.
Le validateur doit aussi refuser une paire mal déclarée (un `inverse` qui pointe vers
un champ qui ne pointe pas en retour) — sinon on remplace un trou par un autre.

**Coût :** réel mais borné. C'est un mode de plus dans un moteur qui en a un. À
noter : c'est la **seule** rupture qui exige une ligne de code que le DevBrain
n'aurait jamais fait écrire. Le test à blanc l'a payée à lui seul.

### Rupture 3 — l'axe de rangement n'est pas exclusif, et le DevBrain n'a jamais eu ce cas

**Ce qui casse.** Une brique a **exactement un** domaine, toujours ; `check_arbo`
compare un chemin à une valeur unique. Une source d'histoire peut n'avoir aucune
période dominante : *Histoire de la France des origines à nos jours* ne relève ni de
l'Antiquité ni du XXe siècle, elle relève des deux et de tout ce qui est entre.

Sans correctif, l'utilisateur mentira dans `categorie:` — ce qui est le pire des
résultats, parce que le validateur restera vert.

**Ce qui répare, et c'est déjà dans le DevBrain.** Deux mécanismes empruntés :

1. La **règle de majorité**, inventée au lot 5 pour les comparatifs qui enjambent
   deux valeurs (`Comparatif - Bases NoSQL` réunit trois catégories). Elle se
   généralise sans effort : *la valeur de l'axe est celle qui rassemble le plus de
   la page.*
2. Un **préfixe déclaré** pour ce qui couvre vraiment tout — `transversal/*`. C'est
   l'exact pendant de `DOM_RATTACHE` : une exception **nommée** dans le manifeste,
   pas une échappatoire.

**Conséquence.** `axes.rangement.exclusif` devient un champ, et `regle_de_majorite` /
`prefixe_transversal` deviennent obligatoires quand il vaut `false`. L'entretien pose
la question 2.3 exactement pour ça, et refuse de passer outre.

**Coût :** faible en code, important en conception — c'est la question qui distingue
un axe de rangement d'un axe transverse, et un brain qui la rate range mal pour
toujours.

### Rupture 4 — un seul axe transverse est codé en dur, l'histoire en veut deux

**Ce qui casse.** `build_mocs.py` a **une** constante `METIERS`, **une** table
`THEME_LABEL`, **une** boucle. HistoBrain a besoin de `Thèmes/` **et** `Espaces/`, et
un brain de domaine client en voudra sans doute trois (client, service, échéance).

**Conséquence.** La boucle transverse devient une boucle **sur** `axes.transverses`.
Et une contrainte de nommage devient explicite : aucun dossier d'axe transverse ne
peut porter le nom de l'axe de rangement au pluriel — le DevBrain a nommé `Métiers/`
plutôt que `Domaines/` pour cette raison précise, et la note est dans le code.

**Coût :** faible. C'est une extraction de constante en liste, mais elle touche le
générateur le plus intriqué des quatre.

### Rupture 5 — le seuil de 5 est faux, et le changer est une migration

**Ce qui casse.** `SEUIL = 5` est calibré sur ~700 pages en 20 domaines, soit ~35
pages par domaine : à 5, un domaine se coupe en une poignée de sous-dossiers. Sur
3 000 pages en 8 périodes — ~375 par période — le même seuil produirait **quarante
sous-dossiers par période**, ce qui n'est plus un arbre mais une liste. À l'inverse,
un brain de domaine client de 40 pages en 6 paquets ne promouvrait jamais rien.

**Conséquence, en deux temps.** D'abord le seuil se **dérive** du volume cible, avec
le calcul écrit dans `motif_seuil` (HistoBrain : 12). Ensuite — et c'est la partie
que le DevBrain n'a jamais eu à faire — **changer le seuil reforme l'arbre**. Un brain
qui grandit plus que prévu devra re-seuiller, c'est-à-dire déplacer des pages. Il faut
donc une opération `re-seuiller` qui émet des `git mv`, refuse de tourner sur un arbre
sale, et qui n'existe nulle part aujourd'hui. Le DevBrain s'en est passé parce qu'il
a fixé son seuil une fois, avec 700 pages déjà écrites sous les yeux.

**Coût :** modéré, mais c'est une **fonctionnalité nouvelle**, pas une extraction.

## 4.4 Ce qui transpose proprement — et qui valide le mécanisme

### `famille:` → `nature:` : le slot survit, le contenu non, et le conditionnel brille

Les 9 valeurs et l'arbre F1→F9 sont à jeter. Mais le **mécanisme du champ
conditionnel** (R16) se réemploie au premier essai : `cote:` n'a de sens que pour une
archive, `langue_originale:` et `traduction:` que pour une source primaire —
exactement comme `hosted:` n'avait de sens que pour une plateforme. Le raisonnement
d'origine (« 177 fiches `paquet` portaient une valeur d'hébergement ; deux champs qui
décrivent 100 % des fiches ne discriminent rien ») se transpose mot pour mot.

`vide_autorise: true` transpose aussi, et il est **plus** utile en histoire : une
source hybride (un manuel de paléographie est-il un `cours` ou un `ouvrage` ?) doit
pouvoir rester sans nature en attendant l'arbitrage.

### Le bandeau : transposition totale, et c'est la meilleure preuve de l'inventaire

`Nature | Licence | Exécution | Maturité` devient `Nature | Auteur et date | Langue |
Fiabilité`. Quatre colonnes, chacune dérivée d'un champ, chacune avec sa table de
rendu, un tiret cadratin quand la source manque. **Le moteur ne change pas d'une
ligne.** C'est la démonstration la plus nette que I4 (générique) et I5 (à réécrire)
sont bien deux briques distinctes.

### La règle 5 transpose, et elle transpose bien

`## Prendre si / Écarter si` devient `## Ce qu'elle établit / Ce qu'elle ne peut pas
établir`, et la colonne négative se remplit exactement de la même façon : des bornes
qui ne pointent vers personne (« l'auteur n'a pas eu accès aux archives soviétiques »)
et des **redirections** vers une autre source (« pour la démographie → [[Recensement
de 1851]] »). La conjonction *flèche × cible fichée* garde son sens intégral.

Une réserve, et elle est de méthode : que la règle donne 1 violation sur 1 388
cellules est vrai **du corpus dev**. Sur HistoBrain elle sort en `a_mesurer`, comme
les neuf autres.

### `role: notion` protégé : survit tel quel, et devient central

Dans le DevBrain, les notions sont 299 pages sur 738 — importantes mais pas
majoritaires. Dans un brain d'histoire, **ce que l'utilisateur a compris et écrit est
l'essentiel de la valeur** : les sources, on peut les relister ; la synthèse
personnelle, non. La frontière « création libre, modification sur demande explicite »
devient la règle la plus sensible du vault, et le drapeau `protege: true` la porte
intégralement.

Conséquence à écrire dans le `CLAUDE.md` généré, mot pour mot comme dans le DevBrain :
*la frontière est portée par le champ, pas par le chemin ; donc lire le frontmatter
avant d'écrire.*

## 4.5 Les trois insuffisances du code actuel que le manifeste ne répare pas

### `maturite:` transpose ; sa sémantique d'élimination, non

`fiabilite: [etablie, discutee, contestee, obsolete]` est une transposition parfaite
de `maturite: [production, beta, experimental, deprecated]` — même forme, même
gradation, même utilité au bandeau.

Mais dans le DevBrain, `deprecated` est **éliminatoire** : `planifier-projet` filtre
sur l'index sans ouvrir les fiches, et proposerait sinon une brique abandonnée. En
histoire, `contestee` n'élimine rien — c'est souvent la source la plus intéressante,
et une source `obsolete` reste un objet d'historiographie.

**Ce qu'il faut en tirer :** `eliminatoire:` doit être un champ **explicite et vide
par défaut**. Le kit ne doit avoir aucune intuition sur « quelle valeur d'énumération
disqualifie ». Le DevBrain, lui, a cette règle écrite dans `planifier-projet`, où
elle est invisible depuis le manifeste.

### Les 47 `.base` ne se génèrent pas, et ils sont un tiers du travail réel

Chaque `.base` porte un filtre réglé à la main et souvent une seconde vue métier. Un
générateur peut poser le premier ; il ne peut pas poser les quarante-sept. En histoire
c'est identique : une chronologie du XXe siècle voudra une vue « sources primaires
seulement », une autre « ce que j'ai lu ».

**Ce qu'il faut en tirer :** les vues sont du **contenu**, et le manifeste doit dire
qu'elles le sont. Le générateur en amorce une par dossier promu, avec le filtre
évident et l'ordre de colonnes par défaut, et s'arrête là.

### `## Retours` / `## Notes de lecture` : la place existe, le contenu n'est jamais venu

Le DevBrain a une convention d'entrée datée (`- YYYY-MM-DD — <symptôme> :
<correctif>.`) et une section conditionnelle pour l'accueillir. Mesure du lot 6 :
sur 337 fiches, **aucune** entrée datée, aucune section créée.

Ce n'est pas un défaut de format, c'est un fait sur l'usage : la section n'a pas été
alimentée en dix-huit mois. En histoire, les *notes de lecture* datées sont bien plus
probables — c'est même l'usage principal d'un tel brain.

**Ce qu'il faut en tirer :** `genre: conditionnelle` est le bon mécanisme, et il faut
le garder. Mais il faut aussi que le kit **mesure l'usage** de ce qu'il génère : une
section qui n'existe sur aucune page au bout de N pages est une section à supprimer du
gabarit, pas à laisser en place « au cas où ». Cela relève du lot 8 (mesure).

## 4.6 Verdict du test

| Mécanisme | Verdict |
|---|---|
| L'arbre dérivé de l'axe de rangement | **passe**, et l'induction par échantillon produit le bon axe |
| Le seuil de promotion et son plafond | **passe le plafond**, **casse la valeur** (rupture 5) |
| `role:` et le moteur de schéma par rôle | **passe** intégralement |
| Les hubs et leurs zones AUTO | **passe** |
| Le bandeau | **passe** — moteur inchangé, contenu entièrement réécrit |
| Les champs conditionnels | **passe**, et se réemploie au premier essai |
| La réciprocité | **casse** — il manque le mode inverse (rupture 2) |
| Le rôle `comparatif` | **casse** — la primitive survit, l'intention non (rupture 1) |
| L'exclusivité de l'axe de rangement | **casse** — réparable par deux mécanismes déjà présents (rupture 3) |
| Un seul axe transverse | **casse** — l'histoire en veut deux (rupture 4) |
| `famille:` | **survit comme slot**, contenu à réécrire |
| Les 6 axes `Métiers/` | **survivent comme mécanisme**, valeurs à réécrire, **et se multiplient** |
| La règle de propagation P1→P6 | **passe** sans une retouche |
| La règle 5 (exclusion sourcée) | **passe**, sévérité à re-mesurer |
| La règle 10 (anti-répétition) | **ne passe pas et ne doit pas être livrée** |
| `protege:` sur un rôle | **passe**, et devient le mécanisme le plus important |
| Les hooks git | **passent**, avec une polarité à inverser selon `usage:` |
| La triade de skills | **passe**, le troisième entièrement réécrit |

---

# 5. Les risques et les points à trancher

Douze points. Chacun a une recommandation ; aucune n'est prise, elles attendent
floSa. Les deux premiers sont ceux que le prompt de cadrage désigne, et ce sont
effectivement les deux qui commandent tout le reste.

## 5.1 Dépôt-gabarit qu'on clone, ou générateur qu'on lance ?

**Le choix, posé net.** Soit BrainKit est un dépôt qu'on `git clone` puis qu'on vide
et qu'on adapte — soit c'est un outil qu'on installe une fois et qu'on lance pour
**écrire** un vault neuf.

**Ce qui plaide pour le gabarit cloné :** l'instance est autonome le jour un, sans
dépendance, ce qui compte pour un client on-prem ou air-gapped. Et c'est plus rapide
à faire — on part du DevBrain, on retire le dev.

**Ce qui le condamne :** le jour du clone, **le code fourche**. Les 10 règles du
validateur, les 4 générateurs et la dérivation d'`arbo` sont exactement les briques
qui vont continuer à recevoir des corrections (le mode inverse de la rupture 2, la
boucle transverse de la rupture 4, le `re-seuiller` de la rupture 5). Avec trois
instances clonées, chaque correction se réapplique trois fois à la main, et la
troisième divergera. C'est le problème qui a déjà été observé **à l'intérieur** du
DevBrain, en petit : deux sources décrivaient le même gabarit, `Templates/` a pris du
retard sur les 338 pages (E4).

**Recommandation : générateur, avec un mode de figeage.**

- BrainKit est un paquet Python installable (`uv tool install brainkit`), et une
  instance ne contient que : son contenu, son `brain.yml`, ses documents générés, ses
  hooks. **Pas de code.**
- `brain.yml` porte la **version du kit** avec laquelle l'instance a été générée. Le
  kit refuse de tourner sur un manifeste d'une version qu'il ne connaît pas, dans les
  deux sens.
- `brainkit freeze` copie les scripts dans `AI/scripts/` de l'instance et coupe la
  dépendance. **Ce mode n'est pas optionnel** : la spécialité de floSa est l'on-prem,
  et un vault livré chez un industriel ne pourra pas installer un outil depuis
  internet. Une instance figée est explicitement une instance qui ne recevra plus de
  correctif — et le manifeste doit l'écrire.

**Risque résiduel :** deux chemins de code (branché / figé) qui peuvent se comporter
différemment. Mitigation : `freeze` copie, il ne réécrit pas, et le lot 10 ajoute un
test qui fait tourner les deux chemins sur la même instance.

## 5.2 DevBrain devient-il une instance de BrainKit ?

**Ce qui plaide pour le garder séparé :** il marche. C'est le brain de travail
quotidien de floSa, il vient de sortir de huit lots de migration, et le transformer
en instance est un neuvième chantier dont il n'a aucun besoin.

**Ce qui plaide pour le migrer :** c'est **le seul corpus réel**. 738 pages, dix
règles mesurées, 1 388 cellules de tableau de décision, 47 vues. Un kit validé
uniquement sur une instance neuve à zéro page n'est pas validé : les mécanismes qui
cassent cassent à 300 pages, pas à 0. Garder DevBrain dehors, c'est se priver du seul
banc d'essai qui a du volume — et accepter que BrainKit soit vendu avant d'avoir été
éprouvé une seule fois.

**Recommandation : oui, mais en dernier, et par génération inverse.**

L'ordre est le point important :

1. Les lots 2 à 4 font tourner le validateur et les générateurs de BrainKit **sur
   DevBrain en lecture seule**, et exigent une **identité octet pour octet** : même
   verdict règle par règle, même compte de violations, et des artefacts régénérés dans
   un arbre de travail séparé dont le `diff` avec les vrais est **vide**.
2. Tant que ce `diff` n'est pas vide, on n'a pas compris ce que fait le DevBrain, et
   on ne touche à rien.
3. Le lot 9 seulement remplace l'outillage du DevBrain par le kit, en un commit qui
   **ne change aucun contenu**.

**Risque résiduel :** DevBrain vit pendant tout ce temps — floSa y écrit. Mitigation :
tous les lots 1 à 8 travaillent en lecture seule sur un chemin de travail isolé, et le
lot 9 commence par la vérification de divergence de `cloturer-brain`.

## 5.3 Le nom de l'unité fuit partout

**Risque.** Le mot « brique » est dans les noms de skill, les titres de section, la
prose des guides, les valeurs de `role:`, le nom des tables du code. Si le générateur
interpole ce mot mais que le kit **raisonne** dessus, alors deux instances ne sont plus
comparables : aucun outil partagé ne peut filtrer « les unités » sans connaître les
mots de chaque brain.

**Recommandation : le dédoublement `id:` / `fonction:` de §2.0.** Le vault porte
`role: brique` ou `role: source` — le mot de l'utilisateur, littéralement, parce que
la fidélité au DevBrain l'exige et parce qu'un vault doit se lire. Le kit ne raisonne
que sur `fonction:`, prise dans une liste de six. Un seul endroit fait le pont : le
manifeste.

**À trancher tout de même :** faut-il indexer `fonction:` dans le frontmatter des
pages, en plus de `role:` ? Recommandation : **non** — un champ dérivable ne se
stocke pas, et le validateur a le manifeste sous la main.

## 5.4 La langue

**Risque.** Tout le système est en français : titres de section, libellés, questions
des arbres de décision, prose générée, messages des hooks. Un brain vendu à un client
anglophone demanderait de traduire non pas des chaînes, mais des **documents générés**.

**Recommandation : déclarer `langue: fr` et n'implémenter que le français en v1**, en
l'écrivant comme une limite et non comme un oubli. Le pont est déjà en place : la prose
générée sort de gabarits, et un gabarit se duplique par langue. Ne pas s'engager sur
`en` avant que deux instances françaises tournent.

## 5.5 L'accrochage à Obsidian

**Risque.** Quatre plugins requis (Local REST API, Templater, Dataview, File Hider),
plus les `.base` qui dépendent d'une version récente d'Obsidian, plus des couleurs de
graphe **gitignorées** donc à réappliquer par poste. Un client ne fera pas les onze
étapes d'`INSTALL.md`.

**Recommandation : deux profils déclarés dans le manifeste.**

- `profil: obsidian` — tout, y compris les `.base` et les couleurs.
- `profil: nu` — markdown, frontmatter, validateurs, générateurs, skills. **Pas** de
  `.base`, donc les rôles `fonction: vue` deviennent des pages avec un tableau
  markdown généré au lieu d'une vue vivante.

Point important : le **bandeau** survit au profil nu (c'est du markdown pur), et c'est
lui qui porte l'essentiel du confort de lecture. Ce qui est perdu en profil nu est la
vue filtrée, pas la fiche.

## 5.6 Les sévérités, et la tentation de les hériter

**Risque.** Une instance neuve sans aucune règle dure est molle : rien n'empêche
d'écrire n'importe quoi les trois premiers mois. La tentation sera forte de livrer les
sept règles dures du DevBrain « puisqu'elles marchent ».

**Recommandation : ne jamais hériter, et livrer l'outil de mesure avec le kit.**
`brainkit mesurer` sort, règle par règle, le compte de violations sur l'instance, et
propose le durcissement de celles qui sont à zéro. Trois garde-fous :

- une règle ne se durcit pas sous **30 pages** de l'unité — en dessous, zéro violation
  ne prouve rien ;
- une règle qui reste en avertissement doit porter un `motif:` **écrit** ; le kit
  refuse un `severite: avertissement` sans motif ;
- deux règles sont structurellement dures dès le départ, parce qu'une violation y est
  une **incohérence de structure** et non un défaut de rédaction : `chemin_categorie`
  et `bandeau_a_jour`. À trancher : est-ce une exception acceptable au principe 1 ?
  Recommandation : oui, et l'écrire comme telle dans le kit.

## 5.7 Le produit vendable — ce qui se vend n'est pas ce qui se code

**Risque.** Le réflexe est de vendre le kit. Mais la valeur mesurée en section 1 se
répartit ainsi : 44 % de mécanique générique (du code, copiable, sans avantage
concurrentiel), 34 % d'extraction (du travail), 22 % de valeurs — et, hors inventaire,
**la discipline d'arbitrage**, qui est le seul actif non copiable et qui ne tient dans
aucun fichier.

**Recommandation : ne pas vendre un outil, vendre un cadrage outillé.** Concrètement,
la prestation est *« nous construisons le second brain de votre domaine »* — l'entretien
mené avec les experts métier du client, le manifeste comme **livrable de conception**,
l'instance générée et figée, et une passe de mesure après les 50 premières pages. Le
kit est l'outil du consultant, pas le produit du client.

**À trancher :** faut-il ouvrir le kit (licence permissive) et vendre le cadrage, ou
le garder fermé ? Recommandation : ouvrir le **kit**, garder fermées les **méthodes
d'entretien** (les 45 questions, les 13 refus, la mesure) — c'est là qu'est le savoir,
et c'est ce qu'un concurrent ne retrouvera pas en lisant le code.

## 5.8 La propriété de la taxonomie d'un brain client

**Risque.** `brain.yml` d'un brain client contient l'ontologie du métier du client :
ses domaines, ses natures de document, ses règles de départage. C'est un actif de
conseil, et c'est en même temps une description de son organisation. Qui le possède,
qui peut le réutiliser chez un concurrent du client ?

**Recommandation :** le `brain.yml` est un **livrable au client**, cédé, et le kit est
licencié. Ne pas réutiliser une taxonomie client, même « anonymisée » — un arbre de
décision est signant. À faire trancher avant la première vente, pas après.

## 5.9 L'amorçage — un brain vide n'est pas utilisable

**Risque.** À la fin de l'entretien, le vault contient des hubs et zéro page. Personne
ne remplit 300 pages à la main, et un brain à 20 pages ne rend aucun service — le
DevBrain n'a commencé à servir qu'à plusieurs centaines.

**Recommandation :** deux mesures, et elles sont dans le plan de lots.

- Les vingt titres de la passe 2.1 partent dans `Inbox.md` comme premier backlog. Ce
  n'est pas du remplissage, c'est du travail déjà identifié.
- Le skill de capture doit avoir un **mode lot** : capturer dix à vingt unités d'un
  même dossier en une conversation, en n'appliquant la propagation qu'une fois à la
  fin. Sans ce mode, l'amorçage coûte une conversation par page et personne ne le fera.

## 5.10 La dette morte du code source

**Risque.** `build_mocs.py` porte encore `MOC_CONCEPT`, `WIKI_LABEL` et `wiki_group()`
pour des dossiers supprimés au lot 4 ; `build_links.py` porte un jeu `V1` de champs
hérités de la v1 ; `check_brain.py` porte `V1_MARKERS` et `is_active_v2()`. Porter ce
code dans le kit, c'est porter la dette du DevBrain dans **toutes** les instances.

**Recommandation : la portabilité se fait par réécriture guidée, pas par copie.** Le
lot 3 réécrit le validateur en le **branchant** sur le manifeste, et prouve
l'équivalence par le verdict, pas par la ressemblance du code. Le critère
d'acceptation (même verdict, même compte) autorise à jeter tout ce qui ne sert plus.

## 5.11 Les champs vestiges

**Risque.** `os:` et `domaines:` sont autorisés sur une brique parce que les gabarits
`service` et `outil` ont fusionné au lot 2 : leur présence est un vestige. Le
manifeste les déclarera comme des champs légitimes et perdra cette information.

**Recommandation :** ajouter `deprecated: true` sur un champ autorisé — le validateur
le tolère, le générateur ne le met pas dans le gabarit, et `mesurer` compte combien de
pages le portent encore. Coût faible, et cela évite qu'un vestige devienne une
intention par transposition.

## 5.12 Le nombre de rôles, et la tentation d'en ajouter

**Risque.** Six rôles dans le DevBrain, six en histoire — la coïncidence est
rassurante et trompeuse. Un utilisateur en entretien voudra en ajouter (« et les
personnages ? et les lieux ? et les événements ? »). Chaque rôle ajouté coûte un
gabarit, une couleur, une ligne de propagation, une section de zone AUTO et un
sous-titre dans chaque hub.

**Recommandation : un plafond souple à six rôles, avec une question de contrôle.**
Avant d'accepter un rôle de plus, l'entretien demande : *« cette page se range-t-elle
sur le même axe que les autres, et y a-t-il une règle qui ne s'applique qu'à elle ? »*
Si non aux deux, ce n'est pas un rôle, c'est une **valeur de l'axe de nature** ou un
**tag**. Les personnages et les lieux d'un brain d'histoire sont, presque toujours, des
notions.

---

# 6. Le plan de lots

Un lot = une conversation. Chaque lot porte son périmètre, son livrable, son critère
d'acceptation et ses interdictions. Deux interdictions valent pour **tous** les lots
et ne sont pas répétées ensuite :

> **Interdictions générales.** (1) **Aucune écriture, aucun déplacement, aucune
> suppression dans DevBrain** avant le lot 9 — lecture seule, dans un arbre de travail
> isolé, floSa continue de s'en servir. (2) **Aucun trailer `Co-Authored-By`** dans
> aucun message de commit, et l'identité git est celle de la config **locale** du
> dépôt BrainKit — jamais l'adresse annoncée par le harnais.
>
> Et une règle de conduite : **un lot qui découvre un problème hors de son périmètre
> l'écrit dans ses *Remontées* et ne le corrige pas.** C'est le mécanisme qui a fait
> tenir les huit lots du DevBrain.

## Lot 0 — Le cadrage *(fait, c'est ce document)*

**Livrable :** `design/00-cadrage.md`, six sections, dépôt initialisé avec ses hooks.

## Lot 1 — Le contrat du manifeste

- **Périmètre.** Figer la structure de `brain.yml` : chaque champ, son type, son
  caractère obligatoire, ses valeurs légales. Écrire les deux remplissages **en
  entier**, sans troncature — les 20 préfixes et 39 sous-libellés du DevBrain, ses 94
  catégories, ses 9 familles, ses 14 arbres de décision.
- **Livrable.** `design/01-manifeste.md` (la spécification) · `schema/brain.schema.json`
  (le contrat vérifiable) · `exemples/devbrain.brain.yml` **complet** ·
  `exemples/histobrain.brain.yml`.
- **Acceptation.** Le schéma valide les deux exemples. Un troisième fichier, volontairement
  incorrect, est refusé avec un message qui nomme le champ fautif.
- **Interdictions.** Aucun code d'exécution en dehors de la validation de schéma. Aucun
  vault. Ne pas décider les points ouverts de §5 — les citer.

## Lot 2 — Le test de fidélité, en lecture seule

- **Périmètre.** Un outil qui lit DevBrain **et** `devbrain.brain.yml` et rapporte
  chaque divergence entre ce que le manifeste dit et ce que le vault est.
- **Livrable.** `outils/fidelite.py` · `design/02-rapport-fidelite.md` avec les comptes :
  combien de pages conformes au schéma déclaré, combien de champs hors manifeste,
  combien de valeurs d'énumération inconnues, combien de sections de corps absentes ou
  en trop.
- **Acceptation.** Le rapport est **explicable ligne par ligne** : chaque divergence est
  soit une erreur du manifeste à corriger, soit un fait connu du vault à documenter. Aucune
  divergence « inexpliquée » ne subsiste.
- **Interdictions.** Ne rien générer. Ne rien réparer dans DevBrain — les divergences se
  **rapportent**, y compris celles qui sont de vraies fautes du vault.

## Lot 3 — Le moteur de validation, branché sur le manifeste

- **Périmètre.** Réécrire `check_brain` et `check_arbo` en validateur piloté par
  `brain.yml`. Y compris les deux mécanismes que le test à blanc a exigés : le mode
  `reciproque: inverse` (rupture 2) et l'axe de rangement non exclusif avec sa règle de
  majorité et son préfixe transversal (rupture 3).
- **Livrable.** `brainkit/valider/` · `design/03-validation.md` : la correspondance
  règle par règle avec l'ancien code, et ce qui a été **jeté** (dette de §5.10).
- **Acceptation.** Sur DevBrain en lecture seule : **même verdict, règle par règle, et
  même compte de violations qu'aujourd'hui** — 0 dure, et les comptes exacts du lot 8
  sur les trois avertissements. Un écart d'une seule violation est un échec du lot.
- **Interdictions.** Aucune règle nouvelle. Aucun changement de sévérité. Ne pas
  « améliorer » une règle au passage : une amélioration casse le critère d'acceptation.

## Lot 4 — Les générateurs, branchés sur le manifeste

- **Périmètre.** Les quatre : index, hubs et axes transverses (avec la boucle sur
  `axes.transverses`, rupture 4), liens, bandeau. Plus le moteur de zone AUTO commun et
  son `--check`.
- **Livrable.** `brainkit/generer/` · `design/04-generation.md`.
- **Acceptation.** Régénérer les artefacts dérivés de DevBrain **dans un arbre de travail
  séparé** et obtenir un `diff` **vide** contre les vrais : `brain-index.json`, `liens.md`,
  les zones AUTO des 75 hubs, les 6 hubs de `Métiers/`, `Comparatifs.md`, les 338 bandeaux.
- **Interdictions.** Écrire dans DevBrain, y compris « juste pour tester ». Le mode par
  défaut des générateurs, pendant ce lot, est `--dry-run` avec une sortie vers un chemin
  imposé en argument.

## Lot 5 — Le générateur d'instance

- **Périmètre.** De `brain.yml` à un vault vierge : l'arbre, un hub par dossier, les
  gabarits par rôle, la taxonomie générée, les vocabulaires vides, `CLAUDE.md` et son
  contexte de mode, les trois hooks avec l'identité locale, la table de couleurs,
  `Home.md`, `Inbox.md`, `AI/`. Plus l'opération `re-seuiller` (rupture 5) et le mode
  `freeze` (§5.1).
- **Livrable.** `brainkit/semer/` · une instance HistoBrain vierge écrite **hors de
  DevBrain** · `design/05-semis.md`.
- **Acceptation.** Les deux validateurs **verts sur zéro page d'unité**, un hub par
  niveau de chemin, et l'instance committée avec l'identité déclarée — les hooks passent.
  `re-seuiller` sur l'instance vierge ne produit aucun `git mv` et le dit.
- **Interdictions.** Aucun entretien : le manifeste est donné en fichier. **Aucune page de
  contenu générée** — pas une source d'exemple, pas une notion de démonstration.

## Lot 6 — L'entretien

- **Périmètre.** Le skill qui conduit les onze passes de §3, produit un `brain.yml`
  valide, le redit en prose, obtient un oui, puis appelle le lot 5. Les treize refus de
  §3.5 sont écrits dans le skill comme une liste fermée.
- **Livrable.** `skills/initialiser-brain/SKILL.md` · `design/06-entretien.md` avec le
  **journal d'un entretien réel**.
- **Acceptation.** Un entretien mené **avec floSa, en direct, sur un troisième sujet**
  — ni le dev, ni l'histoire : le cinéma, ou un domaine client. Le manifeste produit passe
  le schéma du lot 1, et le lot 5 le sème au vert. Et un contrôle négatif : sur une réponse
  manquante à la question 0.4, l'entretien **s'arrête**.
- **Interdictions.** Écrire une page de contenu. Proposer une liste de domaines à cocher.
  Écrire une sévérité autre que `a_mesurer`.

## Lot 7 — Les trois skills, instanciés

- **Périmètre.** Capture (avec sa table de propagation **dérivée** du manifeste, son mode
  mise à jour et sa table des effets de bord), clôture, exploitation. Plus le **mode lot**
  de la capture (§5.9).
- **Livrable.** `brainkit/skills/` (les gabarits) · les trois skills générés dans
  HistoBrain · `design/07-skills.md`.
- **Acceptation.** Capturer **dix sources réelles** dans HistoBrain, dans au moins deux
  dossiers, et les clôturer. Vérifier que le rayon de propagation a été honoré : chaque
  ligne de la table est soit faite, soit **déclarée sans objet** — jamais tue. Les
  réciprocités, y compris une paire `prolonge` / `prolonge_par`, sont vertes.
- **Interdictions.** Toucher aux skills du DevBrain.

## Lot 8 — La mesure et le durcissement

- **Périmètre.** `brainkit mesurer` : par règle, le compte de violations, la population
  mesurée, la date, et une proposition de durcissement pour celles à zéro. Les trois
  garde-fous de §5.6 (plancher de 30 pages, motif obligatoire, les deux règles
  structurellement dures).
- **Livrable.** `brainkit/mesurer/` · `design/08-mesure.md` · le premier rapport de mesure
  de HistoBrain.
- **Acceptation.** Sur DevBrain en lecture seule, `mesurer` retrouve **les comptes du
  lot 8 du DevBrain** — 62 pour le voisinage déclaré, 5 pour les étiquettes de ressources,
  11 candidats dont 2 vrais pour l'anti-répétition. Sur HistoBrain à 10 pages, il **refuse**
  de proposer un durcissement et dit pourquoi.
- **Interdictions.** Durcir quoi que ce soit sans mesure écrite. Modifier une sévérité dans
  `devbrain.brain.yml`.

## Lot 9 — DevBrain devient une instance

- **Périmètre.** Le **premier lot autorisé à écrire dans DevBrain**, et seulement après que
  les lots 2, 3, 4 et 8 ont tous passé leur acceptation. Poser `brain.yml` à la racine,
  remplacer l'outillage de `AI/scripts/` par le kit, régénérer, vérifier l'identité.
- **Livrable.** DevBrain avec son manifeste · `AI/migration/lot-9-brainkit.md` (le journal
  de lot, dans DevBrain, à sa place habituelle) · `design/09-migration-devbrain.md`.
- **Acceptation.** **Aucun contenu de page modifié** — `git diff --stat` ne touche que
  `AI/scripts/`, `brain.yml` et les artefacts régénérés, et ces derniers doivent être
  **identiques** (donc absents du diff). Les deux validateurs verts. Les trois hooks
  passent. La clôture se fait par `cloturer-brain`, pas à la main.
- **Interdictions.** Commencer avant la vérification de divergence avec `origin/main`.
  Corriger une faute de contenu au passage, même évidente — elle va aux *Remontées*.
  Toucher aux 299 notions, quelle que soit la raison.

## Lot 10 — L'emballage

- **Périmètre.** `INSTALL.md` généré (avec le manifeste d'images de N3), les guides
  générés, les deux profils `obsidian` / `nu` (§5.5), le test croisé branché/figé (§5.1),
  la licence, le `README`.
- **Livrable.** Un dépôt installable et documenté · `design/10-emballage.md`.
- **Acceptation.** Une **installation à blanc sur une machine neuve**, en suivant
  l'`INSTALL.md` généré et sans rien savoir du projet, aboutit à une instance verte. Et
  l'instance figée passe les mêmes validateurs que l'instance branchée.
- **Interdictions.** Aucun mécanisme nouveau. Aucune promesse commerciale dans le dépôt
  — §5.7 et §5.8 doivent être tranchés d'abord.

## Ce qui n'est pas dans le plan, et pourquoi

- **Une interface graphique pour l'entretien.** L'entretien est conversationnel par
  nature ; le mettre dans un formulaire ramènerait les listes à cocher que §3 refuse.
- **Le multilingue.** §5.4 : après deux instances françaises.
- **Un brain client réel.** Il vient après le lot 10, et c'est une prestation, pas un lot.
- **Un import depuis un corpus existant** (une bibliothèque Zotero, un dossier de PDF).
  C'est le vrai chantier d'amorçage, il mérite son propre cadrage, et il dépend
  entièrement du sujet.
