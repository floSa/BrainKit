# BrainKit — lot 10 : l'emballage

> Conversation 51, « BrainKit lot 10, l'emballage », le 2026-09-08. **Dernier
> lot du plan** de `design/00-cadrage.md` §6. Ce lot n'ajoute pas de mécanisme :
> il rend installable et documenté ce que neuf lots ont construit, et il traite
> les remontées que les lots précédents lui avaient renvoyées.
>
> L'état final du chantier — ce que le kit fait, ce qu'il ne fait pas, ce qui
> reste ouvert — est dans `design/etat-final.md`. C'est ce document-là qu'il faut
> relire dans six mois ; celui-ci raconte comment on y est arrivé.

## Ce que le lot livre

| Livrable | Contenu |
|---|---|
| `brainkit/emballer/` | 4 modules — `INSTALL.md` et les trois guides, **générés**, plus le manifeste d'images |
| `brainkit/semer/ponts.py` | la couche d'adaptation d'une instance : le résolveur de kit, plus huit cibles d'alias |
| `brainkit/contrat.py` | `kit.version` et `manifeste:`, comparés **dans les deux sens** |
| `outils/emballer.py` | régénère les documents du dépôt, `--check` par défaut, code 2 sur écart |
| `README.md` · `LICENSE` · `INSTALL.md` · `docs/` | le dépôt installable |
| `tests/emballage.py` · `tests/blanc.reponses.yml` | huit scénarios, deux cas négatifs, et l'entretien de l'installation à blanc **rejouable** |
| ce document · `design/etat-final.md` | le rapport, et la clôture du chantier |

Ce que le lot **ne** livre **pas**, et le dit : **aucune capture d'écran**. Le
manifeste d'images déclare les 27 qui seraient nécessaires, dit ce que chacune
doit montrer et à quel endroit du document elle va — et n'en fabrique aucune.
Une capture inventée montrerait une interface qui n'existe pas, ce qui est
strictement pire qu'un trou nommé.

---

# 1. L'installation à blanc — le critère d'acceptation

## 1.1 Comment elle a été jouée

Dans un dossier vierge (`~/Documents/BrainKit-essais/lot10-blanc2/`), en
suivant l'`INSTALL.md` généré **et rien d'autre**. Pas de mémoire du projet, pas
de `design/`, pas de commande devinée : quand le document ne disait pas quoi
faire, l'installation s'est **arrêtée**, et le trou a été noté puis corrigé dans
le document.

Deux limites, écrites parce qu'elles pèsent sur la valeur du résultat :

- **Le kit a été transmis par `git bundle`**, faute d'URL — et c'est le premier
  trou trouvé (§1.3, trou 1). Le dépôt n'a pas de remote.
- **Les six sections Obsidian n'ont pas été exécutées.** Il n'y a pas d'Obsidian
  dans l'environnement où ce lot a travaillé. Ce qui a été vérifié à leur place
  est ce qui *peut* l'être sans interface : que chaque valeur que ces sections
  citent existe bien dans le vault semé, au chemin annoncé et avec le contenu
  annoncé — le dossier de gabarits, l'espace de l'agent à masquer, la table de
  couleurs ligne pour ligne contre `Documentation/graphe.md`. **Ce n'est pas la
  même chose que d'avoir cliqué**, et c'est écrit en remontée 1.

## 1.2 Le déroulé, pas à pas et mesuré

| § du guide | Ce qui a été fait | Résultat |
|---|---|---|
| 2 — Pré-requis | git, Python 3.12, `uv` | présents |
| 3 — Installer le kit | `git clone <bundle> kit` | le clone atterrit en **HEAD détachée** *(trou 2)* |
| 3 — variante a | `uv run brainkit` depuis le clone | les **sept** sous-commandes, code 2 (l'usage) |
| 3 — variante b | `uv tool install --editable`, dans un `UV_TOOL_DIR` isolé | `brainkit` sur le PATH, et l'avertissement `uv tool update-shell` que le guide annonce |
| 4 — Entretien | `--refus`, `--repondre '0.2=…'`, `--reponses`, `--verifier`, `--composer` | 49 réponses sur 49, les treize refus passent, manifeste de **1 167 lignes** écrit |
| 5 — Semer | `semer` en lecture, puis `--ecrire` | **48 fichiers**, 23 dossiers, 14 artefacts dérivés, dépôt initialisé, hooks actifs, commit initial |
| 12 — Vérifier | `valider`, `generer`, `git status` | **0 dure, 0 avertissement** · **0 écart sur 14** · arbre **propre** |
| 13 — Livrer figé | `freeze --ecrire` | 73 fichiers, et l'instance figée rend le **même verdict** (§2) |

Le brain obtenu — **DroitBrain**, les obligations d'un employeur de petite
structure — porte 11 hubs, 5 gabarits, **zéro autre page**, et 9 dossiers de
premier niveau dont un transversal. Le sujet n'a pas été choisi pour dépayser
une quatrième fois : c'est le **cas d'usage visé**, un domaine métier apporté par
quelqu'un qui le connaît et qui n'a jamais entendu parler du kit.

L'entretien est transcrit dans `tests/blanc.reponses.yml`, et
`tests/emballage.py` le rejoue. Un critère d'acceptation qui ne se rejoue pas
n'est pas un critère, c'est un souvenir.

## 1.3 Les sept endroits où le document était muet — et ce qu'ils sont devenus

**Chacun est un défaut du livrable, pas une inattention du lecteur.** C'est la
règle du lot, et elle a bien fonctionné : quatre des sept ne se voient pas en
relisant le document, seulement en l'exécutant.

### Trou 1 — il supposait une URL de clone que ce dépôt n'a pas

`git clone <url du dépôt BrainKit>` : il n'y a pas d'URL. Le dépôt n'a **aucun
remote**, et une livraison hors ligne — le cas §5.1, la spécialité de floSa —
n'en aura jamais non plus. Le lecteur était bloqué à la première commande.

**Corrigé** : les trois formes de transmission sont nommées, avec ce que chacune
coûte — un dossier copié, un `git bundle` (la forme à préférer : elle garde
l'historique **et** se vérifie), une archive (l'historique est perdu, et la seule
trace de version restante est `__version__`). Et la phrase qui manquait le plus :
*rien de ce qui suit ne suppose un remote.*

### Trou 2 — un clone de bundle atterrit en HEAD détachée, et le guide n'en disait rien

Sur le **kit**, c'est sans conséquence : on n'y committe pas. Sur une
**instance**, c'est un piège sérieux — un vault se remplit, donc on y committe,
et des commits posés sur une HEAD détachée sont laissés derrière au prochain
`switch`.

**Corrigé** dans les deux documents, avec la distinction : mention simple côté
kit, `git switch -c <branche principale>` **avant la première écriture** côté
instance — et la branche est celle que le manifeste déclare, pas `main` en dur.

### Trou 3 — il ne disait pas COMMENT répondre à une question

C'est le trou le plus grave, parce qu'il est au milieu du chemin et qu'il
paralyse : le guide disait que l'entretien produit le manifeste, montrait
`--questions` et `--refus`, puis passait au semis. **Aucune commande pour
enregistrer une réponse.** Un lecteur qui suit le document arrive devant
« On reprend à la question 0.1 » et n'a rien pour y répondre.

**Corrigé**, et la correction a doublé la section : `--repondre 'ID=VALEUR'`
(avec le fait que la valeur est lue **en YAML**, ce qui explique comment répondre
une liste ou un dictionnaire), `--reponses <fichier>` par lot, `--rappel` pour
relire avant de reprendre, `--oublier <ID>` pour rouvrir une question — *« c'est
la bonne façon de changer d'avis : écraser une réponse par une autre laisserait
le brouillon en dire deux choses »* — et `--composer`. Plus les deux choses que
le document taisait :

- **qui pose les questions** : un skill, `skills/entretien/SKILL.md`, qu'on
  charge dans l'agent. La commande est ce que le skill *appelle* ;
- **à quoi ressemble un fichier de réponses** : deux exemples complets vivent
  dans `tests/`, chacun avec le raisonnement du sujet en tête. *C'est la forme à
  copier, pas le contenu.*

### Trou 4 — la table de couleurs rendait du markdown cassé

La valeur `graphe.cible` du manifeste porte elle-même des accents graves
(`` .obsidian/graph.json, clé `colorGroups` ``). Le générateur l'enveloppait dans
des accents graves de plus : le rendu affichait des backticks orphelins au milieu
d'une phrase.

**Corrigé** : la valeur est rendue nue, à elle de porter son propre balisage. La
leçon est petite et générale — *une valeur de manifeste peut porter du balisage,
donc un gabarit ne doit pas en rajouter par-dessus*.

### Trou 5 — il présentait le résolveur comme une solution pour un humain

*« Si le kit n'est pas sur le PATH, le vault sait le chercher »* — vrai, mais
trompeur : `_pont_kit.py` est une **bibliothèque**, lue par les scripts du vault
(ses ponts, son hook de fin de session). Elle ne rend `brainkit` tapable par
personne. Un lecteur sans PATH et sans pont déclaré n'avait toujours pas de
commande.

**Corrigé** : la limite est écrite (*« ce n'est pas une commande »*) et le repli
qui manquait est donné — `uv run --project <racine du kit> brainkit …`.

### Trou 6 — il demandait la capture d'une chose que le kit ne produit pas

Le manifeste d'images, transcrit de l'`INSTALL.md` du DevBrain, réclamait une
capture de l'extrait CSS des rôles. Le DevBrain en a un, **écrit à la main** ;
aucun mécanisme du kit ne produit d'extrait CSS.

**Corrigé** : la capture est retirée (27 et non 28), avec le motif en
commentaire. C'est exactement le bruit que le manifeste d'images existe pour
éviter, et il s'y était glissé au premier jet.

### Trou 7 — sa liste de vérifications était incomplète, et muette sur un faux positif

Elle citait les huit jeux d'épreuve de `tests/` et oubliait `outils/fidelite.py`
et `outils/emballer.py`. Surtout, elle ne disait pas ce qui arrive quand on lance
`tests/generation.py` sur un vault que quelqu'un est **en train d'éditer** : un
écart de zone générée apparaît, et il se lit comme une régression du kit alors
que c'est `--check` qui fait son travail. Le lot a rencontré le cas pour de vrai
(§5.3).

**Corrigé** : les dix commandes, et la note qui dit quoi faire — régénérer, ou
relancer sur une copie du dernier commit.

### Et une faute de frappe

*« Un kit devine est un verdict rendu par un code qu'on n'a pas choisi »* →
*deviné*. Elle est citée parce qu'elle était dans la phrase la plus importante
de la section.

---

# 2. Le test croisé branché / figé — §5.1

## 2.1 Le risque, et ce qui le mesure

§5.1 pose le risque résiduel du mode de figeage en une ligne : *« deux chemins de
code (branché / figé) qui peuvent se comporter différemment »*, et la mitigation
en une autre : *« `freeze` copie, il ne réécrit pas, et le lot 10 ajoute un test
qui fait tourner les deux chemins sur la même instance »*.

Ce test est fait, et il l'est sur **trois** instances de tailles très
différentes — parce qu'un mécanisme qui casse casse à 300 pages, pas à 0.

## 2.2 Le résultat, côte à côte

**Instance A — le DevBrain, 765 pages, 414 artefacts.** Une copie du commit
`c6e2400` de la branche du lot 9 (`git archive`, donc **sans écrire une ligne**
dans le vault), figée, puis les deux chemins lancés sur elle.

| Contrôle | Kit **BRANCHÉ** | Kit **FIGÉ** | Identique ? |
|---|---|---|---|
| commande | `brainkit valider --vault <copie>` | `uv run AI/scripts/valider.py` | — |
| code de sortie | **0** | **0** | oui |
| verdict | 0 dure, **111** avertissements | 0 dure, **111** avertissements | oui |
| lignes de verdict | **145** | **145** | **oui, ligne pour ligne** |
| commande | `brainkit generer --vault <copie>` | `uv run AI/scripts/generer.py` | — |
| code de sortie | **0** | **0** | oui |
| artefacts | **414 concordent** | **414 concordent** | oui |
| lignes de rapport | **23** | **23** | **oui, ligne pour ligne** |
| `mesurer` | 238 lignes | 238 lignes | **oui, ligne pour ligne** |

**Instance B — HistoBrain vierge**, semée puis figée, dans le jeu d'épreuve
(scénario 4) : mêmes codes de sortie, **31 lignes de verdict identiques**.

**Instance C — DroitBrain**, l'instance de l'installation à blanc : `valider` et
`generer` en code 0 des deux côtés, après un `freeze` de 73 fichiers.

## 2.3 Ce que la comparaison écarte, et pourquoi

Deux choses, et pas une de plus :

- **l'en-tête de sortie**, qui nomme le manifeste et le vault. Ce sont des
  **chemins**, pas un verdict : le lanceur figé passe des chemins absolus, la
  commande branchée les prend relatifs ;
- **le bruit de `uv`** sur `stderr` (l'avertissement de lien matériel). Il vient
  du lanceur, pas du kit.

Tout le reste est comparé **à l'octet**, et la première version du test l'a
prouvé à sa manière : elle ne filtrait pas le bruit de `uv`, et elle a échoué en
signalant une différence à la ligne 0. Un test qui compare des sorties doit
d'abord dire ce qu'il ne compare pas.

## 2.4 Ce que le test croisé garantit — et ce qu'il ne garantit pas

Il garantit que **le même code, copié, rend le même verdict** : `freeze` ne
transforme rien. Il ne garantit pas que deux instances figées **à deux dates**
se comportent pareil — elles ne portent pas le même code, et rien dans le vault
ne le dit à l'ouverture. C'est écrit dans `FIGE.md` de chaque instance figée, et
c'est le sujet de la remontée 2.

---

# 3. Les deux profils — §5.5

## 3.1 Ce que le lot a trouvé en arrivant

`brain.profil` était **déjà déclaré** au contrat (lot 1) avec ses deux valeurs,
et **consommé à un seul endroit** : le jeton de Templater dans un gabarit
généré. Le reste de la recommandation de §5.5 n'était pas branché.

Le lot ne l'a pas branché en entier, et le motif est l'interdiction du lot :
*aucun mécanisme nouveau*. §5.5 propose que les rôles de fonction `vue`
deviennent, en profil `nu`, *« des pages avec un tableau markdown généré au lieu
d'une vue vivante »* — ce serait un **cinquième générateur**. Il n'est pas écrit,
et la remontée 3 dit ce qu'il coûterait.

## 3.2 Ce que le profil `nu` perd, mesuré fichier par fichier

Le même manifeste, semé deux fois, avec la seule ligne `brain.profil` changée :

| Mesure | `obsidian` | `nu` | Écart |
|---|---|---|---|
| fichiers semés | 49 | **48** | **1** |
| dossiers | 23 | 23 | 0 |
| artefacts dérivés | 14 | 14 | 0 |
| violations dures | 0 | **0** | 0 |
| avertissements + à-mesurer | 0 | **0** | 0 |
| écarts `generer --check` | 0 | **0** | 0 |

**L'écart est un fichier, et c'est `Documentation/graphe.md`** — la table de
couleurs du graphe. Un brain `nu` n'a pas de graphe à colorer : poser le document
quand même donnerait une page de gouvernance qui décrit une interface que ce
brain n'a pas.

Trois autres différences, qui ne changent aucun compte de fichier :

- **le jeton de gabarit** — `<titre de la page>` au lieu du jeton que Templater
  résout. C'était le seul effet du profil avant ce lot ;
- **le lien d'embed d'une page de vue** — remplacé par une phrase qui dit ce
  qu'il en est : *« pas de vue vivante ici ; la table, si elle est voulue, se
  tient à la main — et la section écrite ci-dessous reste la partie qui a de la
  valeur »*. Même arbitrage que le jeton, et même raisonnement que la règle du
  bandeau : mieux vaut un trou nommé qu'une promesse qui ne tient pas ;
- **l'`INSTALL.md` généré** — aucune section Obsidian, aucun plugin demandé, et
  une section qui dit ce que le profil perd. Demander à un brain qui n'ouvre pas
  Obsidian d'installer Templater aurait été la définition d'un document faux.

## 3.3 Ce qu'il ne perd pas — et c'est le point de §5.5

**Le haut de page survit** : c'est du markdown pur, et c'est lui qui porte
l'essentiel du confort de lecture. Vérifié dans le jeu d'épreuve, gabarit par
gabarit — la zone du bandeau est présente dans exactement les mêmes gabarits
qu'en profil `obsidian`.

Survivent aussi, et il faut le lire comme une liste et non comme une évidence :
la dérivation des chemins, le seuil et son plafond, les dix règles, la
propagation, la mesure, le semis, le figeage, `re-seuiller`, les trois skills, et
**la validité**. Un vault `nu` passe **les mêmes validateurs** qu'un vault
`obsidian`, avec le même verdict à zéro.

*« Ce qui est perdu en profil nu est la vue filtrée, pas la fiche »* — §5.5 le
prévoyait, la mesure le confirme, et l'écart est plus petit que ce que le cadrage
laissait craindre.

---

# 4. Les remontées d'emballage, traitées

## 4.1 `valider` / `generer` sans défaut d'instance — **close, vérifiée**

Remontée 3 du lot 5, avancée au lot 6 (`brainkit/defauts.py`) parce qu'elle avait
déjà piégé une vérification. Le lot 10 devait vérifier plutôt que croire, et il
le fait par exécution — scénario 7 du jeu d'épreuve : `valider` et `generer`
lancés **dans** un vault, **sans aucune option**, sortent en 0 et prennent le
manifeste du vault. Le contrôle inclut la négative : aucune ligne de la sortie ne
nomme le manifeste de développement du kit.

**Rien à faire de plus.** La remontée est close, et elle l'était avant ce lot.

## 4.2 `kit.version` comparée à rien — **corrigée**

Remontée 6 du lot 5. Le semis lisait `kit.version` pour l'écrire dans un README
et ne la comparait à rien. §5.1 exige l'inverse en toutes lettres : *« le kit
refuse de tourner sur un manifeste d'une version qu'il ne connaît pas, dans les
deux sens »*.

`brainkit/contrat.py`, et deux versions qui ne disent pas la même chose :

| Comparé | À quoi | Une divergence veut dire |
|---|---|---|
| `manifeste:` | `CONTRAT = 1` | le **format** a changé — les champs ne sont plus les mêmes |
| `kit.version` | `__version__` du paquet | le **code** a changé — mêmes champs, autre comportement |

Le premier refuse sans nuance. Le second se gradue, et la graduation est celle
que le kit pratique en `0.x` — c'est le **mineur** qui porte les ruptures :

- majeur ou mineur différent → **refus**, dans les deux sens, et le message
  nomme les deux versions ;
- correctif différent → on le **dit**, et on tourne ;
- bloc `kit:` absent → **rien**. Il est facultatif au contrat, et se plaindre
  d'une déclaration facultative serait exiger ce que le schéma n'exige pas.

**Où le contrôle vit, et c'est la partie qui compte** : dans
`valider.charge()`, le seul entonnoir de chargement du kit — les sept
sous-commandes et les ponts d'instance y passent tous. Le poser dans chaque
`__main__` aurait donné sept endroits à tenir à jour, donc six oublis en
puissance : c'est le constat E4 appliqué à un contrôle plutôt qu'à un gabarit.

Le refus prend la forme d'un `SystemExit(2)`. C'est brutal pour une fonction de
chargement, et c'est voulu : une version inconnue n'est pas une donnée douteuse
dont on pourrait faire quelque chose, c'est un **contrat absent**.

Effet de bord réglé au passage : `pyproject.toml` **lit** désormais la version
dans `brainkit/__init__.py` (`[tool.hatch.version]`) au lieu de la recopier. Deux
sources pour une version, c'était E4 en miniature — et il fallait de toute façon
que la version soit lisible par le **code**, y compris dans une instance figée où
`pyproject.toml` n'est pas copié.

## 4.3 `--reponses` accepte un lot entier — **documentée comme ce qu'elle est**

Remontée 8 du lot 6 : *« à surveiller au lot 10, si l'emballage documente cette
porte comme un usage »*. Elle l'est, et avec son prix écrit :

> C'est ce qui rend le jeu d'épreuve possible — rejouer un entretien complet est
> la seule façon de **prouver** qu'un entretien produit un vault vert — et c'est
> un usage légitime pour qui sait déjà ce qu'il veut. Mais il faut savoir ce
> qu'on saute : les treize refus tournent toujours sur le brouillon et sur le
> manifeste composé, **pas** sur la conversation. Ce qu'on perd, c'est le moment
> où une question ouverte fait changer d'avis — et c'est là qu'est la valeur de
> l'entretien. Employer `--reponses` pour rejouer, pas pour se dispenser de
> réfléchir.

C'est le traitement juste : la porte n'est pas un défaut, elle est un raccourci
dont on doit connaître le coût. Aucun code n'a changé.

## 4.4 L'absence de PATH pour `brainkit` dans une instance semée — **deux bouchons**

Remontée 5 du lot 7, renvoyée par le lot 9 (§3.3) avec sa moitié de solution.
Une instance `kit.mode: branche` sait qu'elle dépend d'un kit ; elle ne sait pas
**où** il vit.

Le lot pose les **deux** bouchons, et écrit qu'aucun n'est facultatif :

1. **le PATH** — c'est une étape d'installation, et l'`INSTALL.md` généré lui
   donne une section entière avec les deux façons de lancer le kit, la
   vérification (`brainkit` doit afficher les sept sous-commandes) et le cas où
   le dossier des outils `uv` n'est pas sur le PATH. *Une étape d'installation
   qu'on oublie est un outillage qui ne tourne plus* — d'où le second ;
2. **le résolveur**, posé par le semis dans **toute** instance (§4.5).

Et le skill de clôture, qui donnait auparavant un repli approximatif avec la
mention *« remontée connue du lot 7 »*, donne maintenant les deux issues réelles
— `BRAINKIT_RACINE`, ou `uv run --project`.

## 4.5 La couche d'adaptation de 133 lignes — **posée par le semis**

Remontée 1 du lot 9, et le plus gros morceau du lot. Les sept ponts que le lot 9
a écrits à la main dans le DevBrain étaient du **code d'instance** : dans aucun
paquet, testés par aucun jeu d'épreuve, et la prochaine instance les aurait
réécrits. Or ce n'est pas une singularité du DevBrain — toute instance qui a des
habitudes préférera garder ses noms.

`brainkit/semer/ponts.py` :

| Quoi | Quand | Depuis |
|---|---|---|
| `<agent>/scripts/_pont_kit.py` | **toujours**, y compris sur une instance figée | rien à déclarer — la résolution est intégralement générique |
| `<agent>/scripts/<nom>.py` | si `agent.ponts` le déclare | `{nom: cible}` |

**Le résolveur, en trois pistes**, reprises du lot 9 avec leur ordre et son
motif : `$BRAINKIT_RACINE`, puis le kit **copié dans l'instance**, puis un
`BrainKit/` chez un parent — en remontant **tous** les parents, pas seulement le
premier. La piste 2 passe avant la 3 parce qu'*une instance figée est une
instance qui ne doit plus jamais lire un kit du dehors* ; une résolution qui
trouverait le kit voisin d'abord annulerait `freeze` en silence. Aucune ne
répond : sortie en 2, les trois pistes imprimées, **aucune devinette**.

Le nombre de niveaux à remonter n'est plus codé en dur : il se **calcule** depuis
`agent.racine`. Le DevBrain dit `AI/`, un autre brain dira autre chose.

**Les cibles sont fermées** — huit, et c'est délibéré : `valider`, `structure`,
`generer`, `index`, `hubs`, `liens`, `bandeau`, `chemins`. Une cible en chaîne
libre aurait été un mini-langage de commande dans un manifeste, donc une seconde
façon de lancer le kit — et deux façons de lancer le même code divergent. Les
huit couvrent exactement les sept ponts du lot 9, plus la validation complète.

Trois points qui valent d'être écrits :

- **`chemins` est une bibliothèque, pas une commande.** Le pont correspondant
  n'a pas de `main()` : il s'**importe**, parce que c'est comme ça que le skill
  de capture s'en sert. Il expose `SEUIL`, `ROLES_SANS_AXE`, `ROLES_HORS_SEUIL`,
  `tete()`, `promotions()` et `dossier_attendu()` — l'API que le lot 9 avait dû
  adapter à la main ;
- **un pont de construction ÉCRIT par défaut**, là où `brainkit generer` ne fait
  que vérifier. Ce n'est pas une distraction, c'est la seule raison d'être d'un
  pont : un fichier nommé « construis ceci » est appelé par un hook et par un
  skill pour **construire**. En faire un vérificateur silencieux casserait
  exactement l'habitude que le pont existe pour ménager ;
- **une cible inventée est refusée avant toute écriture**, par la passe
  d'exigences du semis — et le refus nomme les huit cibles connues. Un pont vers
  une cible inconnue serait un fichier qui ne tourne pas, posé dans l'espace de
  l'agent, nommé par un skill.

Les huit ponts sont **lancés pour de vrai** dans le jeu d'épreuve, chacun sur une
instance semée, et la bibliothèque est importée.

## 4.6 Deux remontées de plus, traitées parce qu'elles étaient sur le chemin

**Remontée 2 du lot 9 — `chemins.promotions()` a la mauvaise signature pour un
appelant externe.** Elle prend des pages, et elle a raison : elle doit écarter un
rôle hors seuil et résoudre la valeur dominante d'un axe non exclusif. Mais un
appelant qui lit l'index n'a que des chaînes, et le lot 9 lui avait fait
fabriquer huit lignes de pages factices **dans l'instance**.

`chemins.promotions_depuis_valeurs(valeurs, mo)` fait la fabrication une fois et
à la bonne place. Sans elle, le pont `chemins` généré aurait reproduit ces huit
lignes dans **chaque** instance — c'est-à-dire exactement ce que la remontée 1
reproche au lot 9. Ce n'est pas une correction du calcul : *c'est la
reconnaissance que le kit a une **API**, et pas seulement une ligne de commande.*

**Remontée 6 du lot 9 — le vault a une dépendance de poste et rien ne la
déclare.** Le côté kit est fait : le README de l'espace des scripts, généré, dit
maintenant ce que le dossier porte, comment le kit est résolu, et que le PATH est
l'autre bouchon. Le côté vault (une ligne dans la documentation des machines du
DevBrain) appartient au vault, et ce lot n'écrit pas dedans.

---

# 5. Les arbitrages

## 5.1 Deux `INSTALL.md`, un seul générateur

Le périmètre demande « un `INSTALL.md` généré depuis le manifeste ». Il y en a
**deux**, et la coupure est celle du **lecteur** :

| Lecteur | Où il lit | Ce qu'il ne sait pas encore |
|---|---|---|
| celui qui n'a **aucun** brain | `INSTALL.md` du dépôt du kit | tout — ni manifeste, ni vault |
| celui qui reçoit **un** brain | `INSTALL.md` de l'instance | comment ouvrir CE vault sur SA machine |

Le premier a besoin de la route entière ; le second a un vault et un `brain.yml`,
il n'a rien à semer mais il a des valeurs à poser. Les deux sortent du **même**
générateur — `document(None)` et `document(mo)` — parce qu'un générateur par
lecteur aurait fait deux textes à tenir à jour pour une seule séquence
d'installation, et que le second aurait pris du retard. C'est E4, encore.

Le premier chaîne explicitement vers le second : *« celui-ci décrit la route ;
celui-là décrit l'arrivée »*.

## 5.2 La liste des plugins est une connaissance du KIT, pas du manifeste

Aucun manifeste ne déclare de plugin, et aucun ne le fera : un plugin est exigé
par un **mécanisme du kit** — un gabarit qui porte un jeton, un rôle qui embarque
une vue — jamais par le sujet d'un brain. La table vit donc dans le code, à côté
de `MOTEUR_CONNU` du validateur, et pour la même raison.

Ce qui a changé par rapport à la liste du DevBrain n'est pas son contenu mais sa
**colonne** : chaque plugin porte *ce qui le rend nécessaire*, et c'est ce qui
requalifie deux d'entre eux. Le moteur de gabarits est **requis** parce que le
kit écrit lui-même le jeton que ce moteur résout — c'est vérifiable, pas une
opinion. Le moteur de requêtes en ligne devient **confort** : rien dans le kit ne
l'exige, il sert de repli. *Un plugin dont on ne sait pas dire quel mécanisme
l'exige est un plugin qu'on n'installe pas.*

## 5.3 Aucune capture, et une raison qui n'est pas la paresse

Le périmètre l'exige (*« sans les fabriquer »*) et l'inventaire l'expliquait
(N3) : la doc générée doit **référencer** ses captures, pas les embarquer. Le
manifeste déclare 27 captures — **16 du kit** (l'interface d'Obsidian, prises une
fois, valables pour toutes les instances) et **11 de l'instance** (le vault
lui-même, fausses dès la deuxième instance).

Le générateur pose, à l'endroit exact où chacune va, un **appel de figure** : pas
une balise d'image — un lien vers un fichier absent afficherait une image cassée,
ce qui se lit comme un défaut du document plutôt que comme un travail à faire —
mais une ligne qui dit ce qu'il faudrait photographier. Le jeu d'épreuve vérifie
qu'aucun document ne porte de balise d'image et qu'aucune image n'est dans le
dépôt.

## 5.4 Les guides dans le dépôt sont ceux d'une instance de démonstration

Les quatre documents d'instance sont posés par le **semis**, dans l'instance. Ils
n'ont rien à faire dans le dépôt du kit — sauf qu'un dépôt qui annonce « le semis
pose un guide d'installation et trois guides d'usage » sans qu'on puisse les lire
demande de le croire sur parole.

Ils sont donc rendus **une fois**, sous `docs/histobrain/`, depuis le manifeste
de démonstration, avec un README qui dit ce qu'ils sont. HistoBrain et pas
DevBrain, et ce n'est pas un hasard : *le kit doit se montrer sur le sujet le
plus éloigné de celui dont il est extrait*. Un brain de développement logiciel
aurait laissé planer le doute.

`outils/emballer.py --check` les tient à jour, et `tests/emballage.py` l'appelle
— donc un document du dépôt retouché à la main fait **échouer le lot**, et pas
une relecture humaine.

## 5.5 Un outil de dépôt, pas une huitième sous-commande

Régénérer les documents du dépôt du kit n'est pas un usage d'instance : c'est un
geste de développement du kit, comme `outils/fidelite.py` ou `schema/valider.py`.
En faire une sous-commande aurait ajouté un mécanisme à un lot dont
l'interdiction est explicite. `brainkit <sous-commande>` s'adresse à une
instance, et à elle seule.

## 5.6 Le guide d'enrichissement n'affiche pas tous les champs

La table des effets de bord dérivée compte 30 lignes sur HistoBrain, dont une
dizaine disent « aucun consommateur déclaré ». Le **skill** les garde — une liste
de contrôle exhaustive a besoin de dire « rien à faire ici ». Le **guide** les
écarte : un guide se lit en entier, et vingt lignes qui disent « rien à faire » y
noient les dix qui disent quoi faire.

C'est la même table, filtrée pour un autre lecteur — pas une seconde table.

## 5.7 La licence : « tous droits réservés », et ce que ça n'est pas

Le périmètre l'ordonne, et le fichier écrit **pourquoi** : ce n'est pas une
décision, c'est l'absence de décision posée dans la forme la plus **réversible**
qui soit. « Tous droits réservés » est le seul état depuis lequel on peut aller
vers n'importe quelle licence ; l'inverse est faux — une fois du code publié sous
licence permissive, les copies faites sous cette licence le restent.

Le dépôt n'a pas de remote et n'a jamais été publié. **Rien n'est joué**, et
c'est l'état voulu tant que le choix n'est pas fait. Le fichier nomme les deux
questions ouvertes (§5.7 et §5.8), dit laquelle est la plus urgente — la
propriété de la taxonomie d'un brain construit pour quelqu'un d'autre, à trancher
**avant** la première remise — et dit à qui elles appartiennent.

## 5.8 Rien de commercial dans le dépôt, et un contrôle qui le vérifie

Aucun prix, aucune offre, aucun argumentaire, aucun nom de tiers. Le jeu
d'épreuve le vérifie sur les huit documents du dépôt, par expressions à frontière
de mot.

Le premier jet cherchait des sous-chaînes, et il a signalé **onze fausses
promesses commerciales** — parce que « coffre » contient « offre ». La leçon est
celle du lot 7 : *un contrôle qui teste des sous-chaînes de mots courants mesure
la langue, pas ce qu'on veut contrôler.* « prix » est sorti de la liste pour la
raison inverse : il a un emploi légitime fréquent (« c'est le prix, pas un
défaut ») et aucun emploi commercial qu'un autre motif ne prenne déjà. *Un motif
qui ne peut que faire du bruit ne se garde pas.*

---

# 6. Les vérifications, toutes par exécution

| Contrôle | Commande | Résultat |
|---|---|---|
| contrat du manifeste | `uv run schema/valider.py` | code 0 — 2 valides, 1 contre-exemple refusé |
| fidélité | `uv run outils/fidelite.py` | code 0 |
| documents du dépôt | `uv run outils/emballer.py` | code 0 — **les 6 concordent** |
| validation | `uv run tests/epreuve.py` | code 0 |
| générateurs | `uv run tests/generation.py` | code 0 **sur une copie du dernier commit** — cf. §5.3 ci-dessous |
| semis | `uv run tests/semis.py` | code 0 |
| skills | `uv run tests/skills.py` | code 0 |
| mesure | `uv run tests/mesure.py` | code 0 |
| entretien | `uv run tests/entretien.py` | code 0 |
| **emballage** | `uv run tests/emballage.py` | code 0 — **8 scénarios, 59 vérifications** |
| DevBrain, contenu | `brainkit valider --vault ../DevBrain` | **0 dure, 111 avertissements** |
| croisé, 765 pages | branché contre figé | **verdicts identiques ligne pour ligne** |
| installation à blanc | `INSTALL.md` seul, dossier vierge | **instance verte** |

## 6.1 Le seul jeu d'épreuve qui a été rouge, et pourquoi ce n'est pas le lot

`tests/generation.py` échoue **sur le DevBrain vivant**, et passe sur une copie
du dernier commit. La cause est extérieure au kit et elle est datée :

```
 M "Data & pipelines/missingno.md"
 M README.md
```

À 09:18, pendant ce lot, un éditeur a **réaligné le tableau** de la zone générée
d'une fiche du vault — les barres verticales sont passées de `|---|---|` à
`| ---------------- | ----------- |`. Le kit écrit `"|" + "---|" * len(titres)`
(`generer/bandeau.py:182`) et n'a jamais produit de barres alignées : la
modification ne vient d'aucune commande de ce lot, et le second fichier ne porte
qu'un changement de fin de ligne.

Ce que ça montre, et qui est plutôt une bonne nouvelle : **`generer --check` a vu
une zone générée éditée à la main**, immédiatement, sur un vault de 765 pages.
C'est exactement son travail. La conséquence pour le livrable est une note dans
l'`INSTALL.md` généré (trou 7), et rien d'autre : le lot n'a pas touché ces deux
fichiers et ne les touchera pas — ce sont ceux de floSa, et les régénérer serait
écrire dans le DevBrain.

## 6.2 Ce que le lot n'a pas fait

- **Aucune écriture dans le DevBrain.** Le vault a été lu, et la copie du test
  croisé a été faite par `git archive` depuis le commit de la branche du lot 9 —
  jamais par une écriture. La branche du lot 9 n'est pas intégrée, `main` est
  restée à `8aaa257`.
- **Aucune règle nouvelle, aucune sévérité changée.** Les dix règles et les
  quinze contrôles de socle sont ceux du lot 8, et le compte de 111 est
  inchangé.
- **Aucun générateur nouveau.** Les quatre sont ceux du lot 4. Les documents de
  ce lot sont des artefacts de **semis**, pas des artefacts dérivés : ils
  s'écrivent une fois, `generer --check` ne les regarde pas, et le motif est
  celui de la porte d'entrée du vault (arbitrage 3.1 du lot 5) — *un document
  que le propriétaire du brain peut vouloir compléter ne se régénère pas sous
  ses pieds*.
- **Aucune capture fabriquée.**
- **Aucune promesse commerciale.**
- **Aucune instance d'essai versionnée** dans le dépôt du kit — le refus du plan
  d'écriture l'interdit de toute façon, et il a été exercé.

---

# 7. Remontées

*Ce qui a été trouvé hors du périmètre du lot, et qui ne s'y corrige pas. Une
remontée nomme le fait, dit ce qu'il coûte, et propose — elle ne tranche pas.*

**1 — Les six sections Obsidian de l'`INSTALL.md` n'ont jamais été exécutées.**
*(le premier lot qui a un Obsidian sous la main)* L'installation à blanc a joué
tout ce qui se joue en ligne de commande, et **rien** de ce qui se clique : il
n'y a pas d'Obsidian dans l'environnement de ce lot. Ce qui a été vérifié à la
place — que chaque valeur citée existe au chemin annoncé, table de couleurs
comprise — est nécessaire et pas suffisant. Coût si c'est faux : le lecteur bute
sur un libellé de menu qui a changé de nom, et il n'a aucun moyen de savoir si
c'est lui ou le document. Proposition : une passe de relecture **devant
l'écran**, avec la prise des 16 captures de portée kit dans le même geste. C'est
une heure de travail, et c'est la seule partie du livrable dont la justesse
repose sur une transcription plutôt que sur une exécution.

**2 — Rien ne confronte `kit.mode` à ce qui est sur le disque.** *(remontée 5 du
lot 9, non prise ici)* Une instance qui se déclare `branche` avec un
`AI/scripts/brainkit/` posé, ou l'inverse, passerait inaperçue — et les deux
chemins de code tourneraient sans qu'on sache lequel. Le lot 10 vient de prouver
qu'ils rendent le même verdict *aujourd'hui*, ce qui rend le trou moins grave et
pas moins réel : deux instances figées à deux dates ne portent pas le même code.
Ce serait un **contrôle de socle nouveau** (`mode_du_kit_concorde`, en
`a_mesurer`), donc hors du périmètre d'un lot qui n'ajoute aucun mécanisme. Coût
d'écriture : une dizaine de lignes. Le résolveur de pont porte déjà la détection
— il cherche `<scripts>/brainkit/` — il ne fait qu'en tirer une piste au lieu
d'un constat.

**3 — Le profil `nu` ne rend pas les vues en tableau markdown.** *(le premier lot
qui livre un brain `nu` réel)* §5.5 le propose : *« les rôles `fonction: vue`
deviennent des pages avec un tableau markdown généré »*. Ce serait un cinquième
générateur, donc un mécanisme nouveau, donc hors périmètre. Ce que le lot fait à
la place est honnête et suffisant pour un brain vide — le gabarit dit qu'il n'y a
pas de vue vivante ici — mais **insuffisant à 200 pages** : sans table, une page
de vue en profil `nu` ne montre plus ses membres, et c'est la moitié de son
intérêt. Coût : le générateur existe déjà en substance (le filtre est évalué par
`valider/vues.py` pour compter la couverture) ; ce qui manque est le rendu et le
choix des colonnes, que le manifeste déclare déjà
(`vue_embarquee.colonnes_par_defaut`). À faire quand un brain `nu` a des pages.

**4 — `exemples/devbrain.brain.yml` et le `brain.yml` du vault ne sont toujours
comparés par rien.** *(remontée 4 du lot 9, non corrigée — et le lot 10 vient
d'augmenter le risque)* Ils sont identiques à l'octet, tenus par attention seule.
Ce lot a ajouté trois sources qui **lisent** ce manifeste (les deux `INSTALL.md`
et les trois guides), donc trois documents de plus à devenir faux en silence le
jour où l'un des deux fichiers bouge. La proposition du lot 9 tient et reste la
moins chère : cinq lignes dans `tests/epreuve.py` qui comparent les deux sha256
et échouent s'ils divergent. Le scénario DevBrain est déjà conditionné à la
présence du vault.

**5 — Les libellés d'axe sont employés avec un article, et le genre n'est pas
déclaré.** *(le premier lot qui touche `libelles`)* Mesuré en écrivant les
guides : *« le domaine »* se lit bien, *« le période »* ne se lit pas.
`libelles.axe_rangement` porte `s` et `p`, pas le genre. Les documents de ce lot
contournent en évitant l'article — *« l'axe qui range (période) »* plutôt que
*« le période »* — et c'est tenable, mais la prose du semis, elle, ne contourne
pas : `semis.hub.apport_arbre` écrit *« ce {axe_rangement} »*, donc *« ce
période »* dans HistoBrain. Deux issues : un `genre: m|f` facultatif dans
`libelles` (une question de plus à l'entretien, un défaut masculin), ou la
discipline « aucun article devant un libellé » appliquée aussi à
`generer/prose.py`. La seconde est gratuite et moins juste ; la première coûte
une question et rend la langue correcte. Non tranchée.

**6 — Une valeur de manifeste peut porter du balisage, et aucun gabarit ne le
sait.** *(mineur, général)* Le trou 4 de §1.3 en est un cas : `graphe.cible`
porte ses propres accents graves, et le gabarit en rajoutait. Le même piège
attend n'importe quel champ de prose (`motif:`, `portee:`, `definition:`) rendu
dans un tableau ou entre accents graves. Il n'y a pas de règle générale
satisfaisante — échapper serait pire, on perdrait le balisage voulu. Proposition :
la convention explicite *« un champ de prose du manifeste se rend NU ; c'est à
lui de porter son balisage »*, écrite dans `generer/prose.py`, et un contrôle
paresseux au jeu d'épreuve — aucun document généré ne porte deux accents graves
consécutifs.

**7 — Les instances d'essai s'accumulent, et rien ne dit lesquelles sont
vivantes.** *(essais, pas kit)* `BrainKit-essais/` porte maintenant HistoBrain,
CimeBrain, `devbrain-controle`, plus les cinq dossiers de ce lot
(`lot10-histo`, `lot10-blanc2`, `lot10-blanc3`, `devbrain-croise`,
`devbrain-pristine`). Deux sont **figés**, donc portent une copie du kit de ce
jour ; deux sont des copies d'un vault de 765 pages. Aucun n'est versionné, aucun
n'est un livrable, et la remontée 7 du lot 9 signalait déjà que leurs artefacts
ont pris du retard. Ce n'est pas un défaut du kit : c'est du ménage, et il vaut
mieux qu'il soit décidé que subi. Proposition : garder HistoBrain (le banc
d'essai de référence) et `lot10-blanc3` (l'installation à blanc, rejouable), jeter
le reste — les deux copies de DevBrain surtout, qui pèsent le vault entier chacune.

**8 — Le manifeste d'images pourrait se vérifier, et il ne se vérifie pas.**
*(petit, et il grossira)* Le jeu d'épreuve contrôle qu'aucune image n'est
embarquée. Il ne contrôle pas l'inverse : le jour où les 16 captures de portée
kit existeront, rien ne dira qu'une capture déclarée manque sur le disque, ni
qu'un fichier posé sous `docs/install/img/` n'est déclaré par personne. C'est le
même contrôle que `couverture_des_vues` fait pour les vues, dans les deux sens.
Coût : dix lignes, et il n'a aucun sens avant que la première capture existe —
donc après la remontée 1.

---

# 8. Comment rejouer

```bash
# les documents du depot : sont-ils ceux que le kit genere ?
uv run outils/emballer.py                    # --check, sortie 2 sur ecart
uv run outils/emballer.py --ecrire

# le jeu d epreuve du lot 10 — huit scenarios
uv run tests/emballage.py

# l entretien de l installation a blanc, rejoue
uv run brainkit entretien --brouillon /tmp/b.yml --reponses tests/blanc.reponses.yml
uv run brainkit entretien --brouillon /tmp/b.yml --verifier
uv run brainkit entretien --brouillon /tmp/b.yml --composer /tmp/blanc.brain.yml
uv run brainkit semer --manifeste /tmp/blanc.brain.yml --dans <dossier> --ecrire

# le test croise, a la main, sur une instance
uv run brainkit valider --vault <instance>          # branche
uv run brainkit freeze  --vault <instance> --ecrire
uv run <instance>/AI/scripts/valider.py             # fige — meme verdict

# le profil nu : le meme manifeste, une ligne changee
#   brain.profil: obsidian -> nu, puis semer et valider

# les neuf lots anterieurs, inchanges
uv run schema/valider.py · uv run outils/fidelite.py
uv run tests/epreuve.py · generation.py · semis.py · skills.py · mesure.py · entretien.py
```

Et les deux promesses du lot, vérifiables en une commande chacune :

```bash
# aucune capture n est fabriquee
find docs -name '*.png' | wc -l          # -> 0

# un seul module du paquet d emballage ecrit, et c est le plan du semis
grep -rnE 'write_text|write_bytes|mkdir' brainkit/emballer/
# -> rien
```
