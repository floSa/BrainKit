# BrainKit — la mesure et le durcissement

> Conversation 49, « BrainKit lot 8, la mesure et le durcissement », le
> 2026-09-07. Lot 8 du plan de `design/00-cadrage.md`. Ce document rend la
> méthode de mesure, les trois garde-fous, le rapport sur DevBrain confronté à
> son histoire, le refus opposé à HistoBrain, les cinq remontées renvoyées à ce
> lot, les arbitrages et les remontées.
>
> **DevBrain n'a pas été écrit.** Ni page, ni manifeste, ni sévérité. La mesure
> est en lecture seule, et le durcissement appartient au lot 9.

## Le problème que ce lot résout, en une phrase

Une sévérité est un **résultat de mesure sur un corpus**, pas une propriété de
règle. Le kit savait déjà le dire — le moteur du lot 3 lit les sévérités et n'en
propose aucune — mais rien ne savait encore les **mesurer**. `brainkit mesurer`
est l'outil qui dit, règle par règle, ce qu'une règle coûte avant qu'on la
durcisse.

Le risque que §5.6 nommait est exact : *« la tentation sera forte de livrer les
sept règles dures du DevBrain puisqu'elles marchent »*. Sept règles dures qui
marchent sur 337 briques de dev ne prouvent rien sur dix sources d'histoire, et
un brain neuf qui les hériterait aurait sept superstitions au lieu de sept
règles.

---

# 1. La méthode — le dénominateur, et rien d'autre

## 1.1 Ce qui manquait, et qui tient en un mot

Le validateur du lot 3 rendait, pour chaque règle, un **numérateur** : le nombre
de violations. Il ne rendait aucun dénominateur. Or « zéro violation » est
exactement le même texte quand la règle a balayé 337 pages et quand elle en a
balayé trois — et ce sont deux situations sans rapport.

Ce lot ajoute donc, à chaque règle, la **population réellement mesurée**. Trois
mots comptent dans cette phrase, et le troisième est le lot :

- **population** — pas un compte de constats, un compte d'objets examinés ;
- **réellement** — pas le total du vault, ni même le total du rôle : le nombre
  de pages sur lesquelles une violation était **possible**. Une page seule de
  son rôle dans son dossier n'a pas de voisinage à déclarer ; la compter
  gonflerait le dénominateur d'une règle qui ne l'a jamais regardée ;
- **mesurée** — déclarée par la règle elle-même, au moment où elle tourne.

## 1.2 Pourquoi la règle déclare sa propre population

L'alternative était de recalculer les périmètres dans `brainkit/mesurer/`, à
partir des `roles:`, `champ:` et `sections:` que le manifeste déclare. Elle a été
écartée, et le motif est le constat E4 : deux codes qui calculent le même
périmètre divergent au premier correctif, **et en silence** — le validateur
continuerait à contrôler un ensemble pendant que la mesure en annoncerait un
autre.

`Rapport.population(regle, pages, cle, objets, objet)` est donc appelé **par la
règle**, une fois, au point où elle sait ce qu'elle regarde. Le coût est
d'environ vingt-cinq appels dans `dix.py`, `socle.py` et `vues.py` ; le gain est
qu'il n'existe qu'une définition de « ce que la règle a vu ».

Deux comptes tombent juste **tout seuls**, et c'est la vérification de la
méthode :

| ce que le kit mesure | ce que la source disait |
|---|---|
| `redirection_sourcee` : **1 388 cellules** | `mesure: { population: 1388 }` dans `devbrain.brain.yml`, écrit au lot 8 du DevBrain |
| `chemin_categorie` : **681 pages** | `check_arbo` imprimait « 681 page(s) migrée(s) dans 20 domaine(s) » |

Aucun de ces deux nombres n'est écrit dans le code de mesure. Ils sortent de la
règle qui compte ce qu'elle a regardé.

## 1.3 Une règle qui ne compte pas des pages le dit

Toutes les règles ne se mesurent pas en pages, et prétendre le contraire ferait
dire « 1 violation sur 337 » là où la vérité est « 1 sur 1 388 ». La population
porte donc, en plus des pages, un **objet** et son compte quand ils diffèrent :
cellules d'une colonne, couples cités dans un champ à réciprocité, entrées de
puce, étiquettes, wikilinks, noms de fichier, niveaux de chemin.

Un troisième cas existe et il est à part : une règle **vérifiable sur le
manifeste**, sans lire une seule page. `paire_inverse_bien_declaree` en est
l'exemple. Son dénominateur n'est pas un volume de corpus, donc le plancher de
pages ne s'y applique pas — et c'est la seule exception au garde-fou 1.

---

# 2. Les trois garde-fous de §5.6

Ils ne sont pas des options de la mesure : ils sont ce qui distingue une mesure
d'une superstition. Ils vivent dans `brainkit/mesurer/gardes.py`, ensemble, et
ce module ne contient rien d'autre.

## 2.1 Garde-fou 1 — le plancher, lu DEUX fois

> Une règle ne se durcit pas sous **30 pages de l'unité**.

**Plancher d'instance** — le vault porte-t-il 30 pages du rôle
`fonction: unite` ? Si non, **aucune proposition n'est émise, pour aucune
règle**. C'est le garde-fou tel que le cadrage l'écrit, et c'est le contrôle
négatif du lot (§4).

**Plancher de règle** — arbitrage de ce lot, et il est argumenté en §7.1. Le
cadrage exprime son plancher en « pages de l'unité » parce que c'est la
population de la plupart des règles ; une règle dont la population **réelle**
est plus petite n'est pas couverte par ce raisonnement. Une règle à zéro sur
trois pages n'a rien prouvé, même dans un vault de mille pages.

Sur DevBrain, cette seconde lecture ne change **rien** : aucune règle proposable
n'a une population sous 30. C'est précisément ce qui a permis de la poser — elle
ne se paie pas.

## 2.2 Garde-fou 2 — le motif obligatoire

> Une règle qui reste en avertissement doit porter un `motif:` **écrit** ; le
> kit **refuse** un `severite: avertissement` sans motif.

« Refuse » est pris au mot : c'est le **seul** endroit de `mesurer` qui change
le code de sortie. Un refus qui ne se voit pas dans le code de sortie est un
refus que personne ne lit — le même raisonnement que « une règle absente ne
ressemble pas à une règle souple, elle ressemble à une règle satisfaite ».

Codes de sortie de `brainkit mesurer` :

| code | ce qu'il dit |
|---|---|
| 0 | la mesure est faite, aucun refus ne se tient |
| 1 | garde-fou 2 : au moins une sévérité `avertissement` sans motif écrit |
| 2 | erreur d'usage (vault ou manifeste introuvable) |

Un plancher non tenu n'est **pas** un code 1, et c'est délibéré : un vault de
douze pages qui refuse tout durcissement est un vault en bonne santé, pas un
vault en faute.

**Corollaire, et c'est un arbitrage** : toute proposition émise par `mesurer`
porte un emplacement `motif:` **vide et obligatoire**, littéralement
`"À ÉCRIRE — le kit refuse une sévérité sans motif"`. Le kit sait mesurer, il ne
sait pas écrire pourquoi ; et une sévérité dont personne n'a écrit la raison est
exactement la sévérité héritée que §5.6 interdit.

## 2.3 Garde-fou 3 — les deux règles structurellement dures

> `chemin_categorie` et `bandeau_a_jour` sont dures dès le départ : une violation
> y est une **incohérence de structure**, pas un défaut de rédaction.

La liste est **fermée par le kit**, comme celle des dix. Elle ne se lit pas dans
le manifeste, et c'est le point : un garde-fou qu'une instance désactive en
écrivant `structurellement_dure: false` n'est pas un garde-fou. Le manifeste
d'HistoBrain écrit exactement cela — il portait la recommandation de §5.6 sans
l'appliquer, parce que le point n'était pas tranché quand il a été écrit.

Ce que garde-fou 3 fait : il **signale** la contradiction. Ce qu'il ne fait
pas : proposer un durcissement. Ces deux règles ne relèvent pas du régime de la
mesure — leur dureté ne s'obtient pas en comptant des violations —, donc elles
se décident quand le manifeste s'écrit, pas quand on mesure. Sur un vault sous
le plancher, `mesurer` ne propose donc **rien**, y compris pour elles. C'est ce
qui permet de tenir les deux textes à la fois : §5.6 les veut dures, et le
critère du lot veut zéro proposition sur HistoBrain.

---

# 3. Le rapport de mesure sur DevBrain, confronté à son histoire

`uv run brainkit mesurer` sur le vault réel, en lecture seule, le 2026-09-07.
765 pages, unité `brique` : **337 pages**, plancher **largement tenu**.

## 3.1 Les trois comptes que le lot 8 du DevBrain annonçait

| règle | mesure du lot 8 du DevBrain (2026-09-06) | ce que le vault dit aujourd'hui | |
|---|---|---|---|
| `voisinage_declare` | 62 | **62** violations sur **334** pages | conforme |
| `etiquettes_fermees` / `Ressources` | 5 | **5** violations sur 337 pages · 647 étiquettes | conforme |
| `anti_repetition` | 11 candidats dont 2 vrais | **4** violations sur 336 pages · 362 valeurs de bandeau | **écart, et c'est le vault qui a raison** |

Le troisième écart n'est pas une découverte de ce lot : le lot 3 l'avait déjà
établi (remontée 1) et le manifeste porte l'annotation
`note_mesure_2026_09_07`. La mesure du lot 8 du DevBrain n'est pas fausse, elle
est **datée** — sept candidats ont disparu depuis par réécriture des sections de
définition. Ce que le fait apprend vaut au-delà du chiffre : **une règle non
scriptable en avertissement se vide toute seule quand on relit les pages**, ce
qui est un argument de plus pour ne pas la durcir.

Le lot 8 ajoute une chose que ni le lot 3 ni l'histoire ne disaient : le
**dénominateur**. `voisinage_declare` mesure 334 pages et non 337 — trois
briques sont seules de leur rôle dans leur dossier et n'ont donc aucun voisinage
à déclarer.

## 3.2 La mesure complète, règle par règle

| règle | sévérité | violations | population réellement mesurée | verdict |
|---|---|---:|---|---|
| `reciprocite` | dure | 0 | 301 pages · 952 couples | déjà dure |
| `chemin_categorie` | dure | 0 | 681 pages | structurelle |
| `completude_du_hub` | dure | 0 | 337 pages | déjà dure |
| `voisinage_declare` | avertissement | 62 | 334 pages | à réparer |
| `redirection_sourcee` | dure | 0 | 337 pages · **1 388 cellules** | déjà dure |
| `reinjection_du_resume` | dure | 0 | 301 pages · 952 puces | déjà dure |
| `etiquettes_fermees` / `Mise en œuvre` | dure | 0 | 337 pages · 1 685 étiquettes | déjà dure |
| `etiquettes_fermees` / `Ressources` | avertissement | 5 | 337 pages · 647 étiquettes | à réparer |
| `citation_unique` | dure | 0 | 333 pages · 2 153 entrées de puce | déjà dure |
| `bandeau_a_jour` | dure | — | — | **déléguée** à `brainkit generer --quoi bandeau --check` |
| `anti_repetition` | avertissement | 4 | 336 pages · 362 valeurs | à réparer |
| `frontmatter_lisible` | dure | 0 | 765 pages | déjà dure |
| `gabarit_par_role` | dure | 0 | 765 pages | déjà dure |
| `liens_resolus` | dure | 0 | 765 pages · 10 886 wikilinks | déjà dure |
| `couverture_de_section` | dure | 0 | 301 pages · 952 cibles | déjà dure |
| `lien_vers_une_page_a_comprendre` | dure | 0 | 337 pages | déjà dure |
| `nom_egal_fichier` | dure | 0 | 755 pages | déjà dure |
| `page_atteignable` | dure | 0 | 765 pages | déjà dure |
| `hub_par_niveau` | dure | 0 | 64 dossiers · 65 niveaux | déjà dure |
| `vocabulaire_ferme` | dure | 1 | 756 pages · 4 967 valeurs | déjà dure |
| `unicite_du_nom_de_fichier` | dure | 0 | 765 pages · 812 noms | déjà dure |
| `taille_avertissement` | avertissement | 0 | 634 pages | **PROPOSÉE** |
| `collision_alias` | avertissement | 13 | 685 pages · 2 635 alias | à réparer |
| `couverture_des_vues` | avertissement | 26 | 337 pages · 47 vues | à réparer |
| `champs_supprimes` | dure | 0 | — | déjà dure |

`couverture_des_vues` se détaille en cinq sous-constats — a : 13, b : 1, c : 0,
d : 1, e : 11 — et le total, 26, est bien la somme. Le détail est **affiché** ;
la décision, elle, se prend au niveau de la règle (§7.4).

## 3.3 Une seule proposition, et elle est instructive

```yaml
  - id: taille_avertissement
    severite: dure
    motif: "À ÉCRIRE — le kit refuse une sévérité sans motif"
    mesure: { date: "2026-09-07", population: 634, violations: 0 }
```

Une seule proposition sur vingt-cinq règles : **DevBrain est déjà mesuré**. Sept
de ses règles sont dures parce que le lot 8 de sa migration les avait mesurées à
zéro, et les autres portent des violations qu'un durcissement ne ferait pas
disparaître. C'est le résultat attendu d'un vault qui sort de huit lots
d'arbitrages écrits — et c'est aussi ce qui rend la mesure d'HistoBrain lisible
par contraste.

**Rien n'a été appliqué.** L'interdiction du lot est explicite, et la proposition
est là pour floSa, pas pour le kit : durcir `taille_avertissement` ferait échouer
la validation dès la première page longue, ce qui est une décision éditoriale.

## 3.4 Le refus du garde-fou 2, dès le premier passage

```
REFUS — garde-fou 2 : 2 sévérité(s) `avertissement` sans `motif:` écrit.
  - `taille_avertissement` : `severite: avertissement`, aucun `motif:`
  - `collision_alias`      : `severite: avertissement`, aucun `motif:`
```

Le garde-fou mord sur le premier vault réel auquel on l'applique, et il a raison
de mordre : ces deux règles sont souples depuis toujours et **personne n'a jamais
écrit pourquoi**. Les quatre autres règles souples du DevBrain
(`voisinage_declare`, `etiquettes_fermees/Ressources`, `anti_repetition`,
`couverture_des_vues`) portent chacune un motif, et de bons motifs.

Les deux motifs manquants **n'ont pas été écrits ici** : ce serait inventer une
raison à la place de celui qui a pris la décision. C'est la remontée 1.

`brainkit mesurer` sur DevBrain sort donc en **code 1**. Ce n'est pas un échec
de la mesure — la mesure est complète et juste — c'est le refus qui se voit.

## 3.5 Le recensement par domaine, remis à sa place

Remontée 8 du lot 3, exécutée. Le recensement retrouve les chiffres de
`check_arbo` au chiffre près :

```
recensement : 681 page(s) rangée(s) par l'axe dans 20 dossier(s)
              — 10 rangée(s) par `role:` (pattern, rule) — 74 hub(s)
  Automatisation no-code/                   6 page(s)   brique 5 · comparatif 1 · hub 1
  Bases de données/                        61 page(s)   brique 47 · comparatif 10 · hub 5 · notion 4
  …
  Machine Learning/                       252 page(s)   brique 85 · comparatif 12 · hub 13 · notion 155
  promotions : 45 sous-valeur(s) promue(s) (seuil 5)
  proche du seuil : `data/eda` — 4 page(s), il en manque 1
  proche du seuil : `compute/distribue` — 3 page(s), il en manque 2
```

Trois choses de plus que l'original, et aucune n'est gratuite :

- **le compte par rôle dans chaque dossier**. Le total d'un domaine mélange les
  unités, les notions et les vues — et c'est justement ce mélange qui est le
  point d'arrivée de la v3. `Machine Learning/` : 85 briques et 155 notions ;
  `Mathématiques/` : 1 brique et 26 notions. On voit la forme du brain, pas
  seulement sa taille ;
- **les 74 hubs, comptés à part**, parce qu'un hub ne se range pas — il *est* le
  rangement. C'est ce découpage qui fait retomber sur 681 et non sur 746 ;
- **la distance au seuil** de chaque valeur non promue : ce qui va changer la
  forme de l'arbre au prochain ajout.

## 3.6 L'occupation du gabarit — 34 sections mesurées, 2 mortes

C'est la forme mesurable d'`existe_si` (§5.2). Sur DevBrain :

| rôle . section | présente | remplie | |
|---|---:|---:|---|
| `brique` . Retours | 0/337 | 0/337 | **MORTE** — `existe_si: "au moins une entree datee"` |
| `hub` . Notes | 13/74 | 0/74 | **MORTE** — le titre existe, rien dessous |
| `brique` . Alternatives | 324/337 | 316/337 | 8 pages portent le titre sans rien dessous |
| `brique` . Compléments | 103/337 | 103/337 | conditionnelle, et cohérente |
| `notion` . Les maths, simplement | 282/297 | 282/297 | conditionnelle, et cohérente |
| les 29 autres | universelles | universelles | |

`brique.Retours` est le cas que la remontée 5 du lot 5 annonçait — *« zéro entrée
en dix-huit mois »* — et la mesure est pire que l'annonce : la section n'est même
pas **posée**. Zéro sur 337 en présence, zéro en remplissage. Une section
conditionnelle qui n'a jamais eu d'objet.

`hub.Notes` est le contre-exemple qui justifie de mesurer **deux** choses : elle
est présente sur 13 hubs et remplie sur aucun. Un compte de présence seul l'aurait
ratée.

---

# 4. Le refus opposé à HistoBrain — le contrôle négatif

HistoBrain, l'instance d'essai semée au lot 5 et remplie de dix sources au lot 7 :
38 pages contrôlées, unité `source` : **10 pages**.

```
mesurer : vault `histobrain`, manifeste `brain.yml`, mesuré le 2026-09-07
  38 page(s) · unité `source` : 10 page(s) · plancher de durcissement : 30
  REFUS GLOBAL — sous le plancher, AUCUN durcissement n'est proposé.
  Il manque 20 page(s) de `source`.
  …
propositions de durcissement : AUCUNE.
  11 règle(s) refusée(s) par le plancher — voir ci-dessus.
```

**Onze règles sont à zéro violation, et pas une n'est proposée.** C'est le
résultat que le lot demandait, et il est aussi important que celui de §3 : un
outil qui durcirait un brain de dix pages transformerait chaque règle en
superstition.

Le refus est **chiffré et nommé**, jamais muet :

| ce que le refus dit | valeur |
|---|---|
| le plancher | 30 pages de l'unité |
| ce que le vault a | 10 pages de `source` |
| ce qui manque | **20 pages** |
| combien de règles sont bloquées | 11 |

Et deux contradictions de garde-fou 3 sont signalées : le manifeste d'HistoBrain
déclare `chemin_categorie` et `bandeau_a_jour` en `a_mesurer` avec
`structurellement_dure: false`. Le kit ne les suit pas et ne les corrige pas : il
le dit.

## 4.1 Le premier rapport de mesure d'HistoBrain

Écrit dans l'instance, à `AI/mesure/2026-09-07-mesure.md` (188 lignes). Il répond
aux trois questions, dans cet ordre, et c'est sa structure :

**Ce qu'on sait.** 19 règles ont réellement mesuré quelque chose, 3 n'ont rien
mesuré (deux désactivées par le manifeste avec leur motif, une déléguée). Le
tableau donne, pour chacune, sa sévérité, ses violations, sa population et son
verdict. Deux règles mordent déjà : `page_atteignable` (13 constats) et
`vocabulaire_ferme/axe_vide` (3 sources sans `nature:` — la remontée 3 du lot 7,
sur l'arbre de décision incomplet de l'exemple).

**Ce qu'on ne sait pas encore.** Le plancher n'est pas tenu, et la liste dit,
règle par règle, ce que chacune a mesuré malgré tout — *le chiffre est vrai,
c'est sa portée qui ne l'est pas encore*. `reciprocite` : 0 sur 8 pages et 8
couples. `citation_unique` : 0 sur 10 pages et 31 entrées de puce.

**À partir de combien de pages on saura.** 20 pages de `source` pour le plancher
d'instance — *« c'est le seul chiffre qui débloque quoi que ce soit »*. Puis un
tableau du manque **par règle**, parce qu'une fois le plancher d'instance
franchi, chaque règle doit encore avoir vu 30 pages pour elle :

| règle | mesuré aujourd'hui | il en manque |
|---|---:|---:|
| `reciprocite` | 8 | 22 |
| `hub_par_niveau` | 2 | 28 |
| `redirection_sourcee` | 10 | 20 |
| `liens_resolus` | 30 | **0** |
| `frontmatter_lisible` | 38 | **0** |

La dernière colonne est l'information que ni le validateur ni l'entretien ne
savaient donner : **six** règles ont déjà leur population — celles qui lisent
toutes les pages, quel que soit leur rôle — et elles n'attendent que le plancher
d'instance. Les treize autres attendent des sources.

---

# 5. Les cinq remontées renvoyées à ce lot

## 5.1 `page_atteignable` ne lisait pas `racine:` — branchée, et gratuitement

*(Remontée 1 du lot 5, reconduite par la remontée 5 du lot 6, coût mesuré par la
remontée 1 du lot 7.)*

Le bloc `racine:` existe depuis le lot 5, le schéma le porte, le semis l'honore.
**Aucune règle ne le lisait** : `page_atteignable` prenait `racine.glob("*.md")`,
donc tout `.md` posé à la racine élargissait silencieusement l'atteignabilité de
tous les hubs de premier niveau. Un brouillon suffisait.

Le lot 5 demandait explicitement de **mesurer avant de brancher** : *« sur
DevBrain, neuf `.md` à la racine dont un seul aiguille, et il faut compter
combien de pages perdraient leur atteignabilité si les huit autres cessaient de
compter. Si la réponse est zéro, le durcissement est gratuit. »*

Mesure faite, avant d'écrire la moindre ligne du branchement :

| vault | fichiers de racine lus, périmètre `glob` | périmètre `racine.pages[].aiguille` | pages inatteignables |
|---|---:|---:|---:|
| DevBrain | 9 | 1 (`Home.md`) | **0 → 0** |
| HistoBrain | 4 | 1 (`Home.md`) | **13 → 13** |

La réponse est zéro. Le durcissement est gratuit, et c'est **parce qu'il l'est**
qu'il est posé : `sources_d_aiguillage()` lit `racine.pages[].aiguille`, et un
manifeste sans le bloc garde le comportement qu'il avait — un durcissement
silencieux sur un manifeste muet serait exactement ce que ce lot interdit.

Conséquence sur le critère du lot 3 : **aucune**. DevBrain reste à 0 violation
dure et 111 avertissements ; HistoBrain reste à 13 constats `page_atteignable`.
Le périmètre effectif est désormais imprimé en note (`--tout`), pour qu'on ne le
redevine jamais.

**Ce qui n'est pas durci** : la sévérité. `page_atteignable` est `dure` dans
DevBrain, `a_mesurer` dans HistoBrain, et le lot 8 n'y touche pas — la mesure
d'HistoBrain donne 13 violations, ce qui interdit toute proposition de toute
façon (verdict « à réparer »).

## 5.2 `genre: conditionnelle` reçoit une forme mesurable

*(Remontée 5 du lot 5, reconduite telle quelle par la remontée 3 du lot 6, sur un
troisième manifeste.)*

Le problème : `roles[].corps[].existe_si` porte une phrase **en français** — « au
moins une entrée datée », « la notion porte une controverse historiographique ».
Ni le validateur ni le semis ne peuvent l'évaluer ; le gabarit la rend en
commentaire.

**Arbitrage : on n'évalue pas la condition, on mesure son RÉSULTAT.**

C'est la seule sortie qui ne demande pas d'inventer un langage d'expression dans
un fichier de configuration — ce que le kit refuse partout ailleurs (« le
manifeste BRANCHE les règles, il ne les décrit pas », §2.3 du cadrage). Une
condition en français reste en français ; ce qui devient mesurable, c'est le fait
qu'elle produise ou non une section sur les pages réelles.

Le manifeste HistoBrain avait écrit lui-même le cahier des charges : *« le kit
doit MESURER l'usage de ce qu'il génère — une section qui n'existe sur aucune
page au bout de N pages est une section à supprimer du gabarit, pas à laisser au
cas où. »*

Deux nombres, pas un — et c'est ce qui rend la mesure juste :

- **présence** : combien de pages portent le titre ;
- **remplissage** : combien portent quelque chose dessous.

Deux détails d'implémentation ont dû être trouvés, et aucun n'est cosmétique :

1. **Le sous-arbre, pas le corps propre.** `Page.sections` s'arrête au titre
   suivant quel que soit son niveau — ce qu'il faut à une règle qui contrôle le
   corps d'une section, pas à une mesure d'occupation. `## Concepts clés` porte
   trois `###` libres sur chacune des 297 notions : son corps propre est vide
   partout, et une lecture naïve l'aurait déclarée morte alors qu'elle porte tout
   le contenu de la page. La mesure lit donc du titre jusqu'au prochain titre de
   niveau inférieur ou égal.
2. **Un `niveau: 0` n'est pas un titre.** C'est un marqueur de place — bandeau,
   accroche, embed, zone AUTO. Le chercher parmi les `##` d'une page inventait
   quatre sections mortes par manifeste.

Résultat sur DevBrain : 34 sections mesurées, **2 mortes** (§3.6). Sur
HistoBrain : 1 morte (`source.Notes de lecture`, `existe_si: "au moins une entrée
datée"` — la même section que `brique.Retours`, transposée, et le même verdict).

**Ce que la mesure ne dit pas** : de supprimer. Sous le plancher, le rapport
donne le taux et se tait — c'est le même raisonnement que le garde-fou 1.

## 5.3 `existe_si` n'est toujours pas évaluable — et il ne le sera pas

*(Remontée du lot 6, troisième manifeste.)*

C'est la même remontée que la précédente, vue de l'autre côté, et elle reçoit ici
un **refus** plutôt qu'une solution : le kit ne se dotera pas d'un évaluateur de
conditions en langue naturelle, et il ne demandera pas non plus à l'utilisateur
d'écrire ses conditions dans un mini-langage.

Les trois raisons, dans l'ordre de force :

1. **Ce serait un langage de programmation dans un fichier de configuration.** Le
   kit garde du code par règle exactement pour ne pas faire ça
   (`brainkit/valider/dix.py`, en-tête). Une condition comme « la notion porte
   une controverse historiographique » n'est pas mécanisable de toute façon : il
   n'existe aucun champ qui la porte.
2. **La condition n'a pas besoin d'être évaluée pour être utile.** Elle est
   destinée à un **lecteur humain** au moment où il remplit la page, et le
   gabarit la lui rend en commentaire. C'est son emploi réel, et il fonctionne.
3. **Ce qu'on voulait vraiment savoir, c'est le taux d'occupation** — et §5.2 le
   donne. Une section conditionnelle à 0 % après N pages est le seul verdict
   qu'on cherchait, et il ne demande aucune évaluation.

Le champ `existe_si` reste donc **déclaratif, et déclaré tel**. Ce qui change,
c'est qu'il est désormais **confronté** : `mesurer` affiche la condition écrite à
côté du taux qu'elle produit, et le backlog code `G0` la cite en entier quand la
section est morte.

## 5.4 `A1` / `A3` reçoivent leur place : un backlog

*(Recommandation du lot 2, arbitrage 3 et remontée 9 du lot 3, qui disaient tous
deux que la place se déciderait ici.)*

Le lot 3 avait tranché ce qu'elles **ne sont pas** — pas des règles : elles n'ont
jamais été dans les validateurs du DevBrain, les ajouter aurait cassé son critère
d'acceptation (118 avertissements au lieu de 111), et `A3` signale un état
**voulu**. Il restait à dire ce qu'elles **sont**.

**Ce sont des entrées de backlog, et le backlog est la seule sortie du kit qui ne
soit pas un verdict.** Deux exécutions :

- **Dans `outils/fidelite.py`** — les sept groupes permanents quittent le corps
  du rapport pour une section « BACKLOG » en fin de sortie, avec un renvoi vers
  `brainkit mesurer`. Ils ne sont **pas** supprimés : un état voulu qu'on
  cesserait d'imprimer redeviendrait un oubli. Le compte des divergences passe de
  34 à 27 groupes, et la ligne de tête dit où sont passés les sept. L'outil sort
  toujours en 0, boîte 1 à 8 groupes, boîte 2 à 26, zéro inexpliquée.
- **Dans `brainkit/mesurer/backlog.py`** — recalculés sur les mêmes données,
  parce qu'un backlog qui renverrait à la sortie d'un autre outil ne serait pas
  une liste de travail. Avec deux codes de plus que le lot 2 n'avait :

| code | ce qu'il liste | DevBrain | HistoBrain |
|---|---|---:|---:|
| `A1` | valeur d'axe déclarée et portée par aucune page | 5 (`skill/*`) | 20 |
| `A3` | `libelle` déclaré pour une valeur non promue | 2 (plafond) | 4 |
| `F8` | champ vestigial (`deprecies`) encore porté — §5.11 du cadrage | 2 (`os` : 40 pages, `domaines` : 39) | 0 |
| `G0` | section qu'aucune page ne remplit — §5.2 | 2 | 1 |
| `E4` | information déclarée **et** dérivée | 1 | 1 |

`F8` exécute la recommandation de §5.11 du cadrage, qui nommait `mesurer` en
toutes lettres : *« `mesurer` compte combien de pages le portent encore. Coût
faible, et cela évite qu'un vestige devienne une intention par transposition. »*
Les deux champs sont `os` (40 briques) et `domaines` (39 briques) — le lot 2 en
comptait 37 pour `os`, l'écart tient au périmètre (le lot 2 comptait les briques
d'un rôle, ici on compte toutes les pages du rôle qui portent le champ).

**L'arbitrage sur les cinq `skill/*` orphelines reste à floSa**, et son exécution
au lot 9. Rien n'a changé sur ce point.

## 5.5 `propagation.table` cesse d'être une source

*(Remontée 2 du lot 7.)*

Le constat : le schéma rendait `table:` **obligatoire** dans `propagation`, le
composeur de l'entretien l'écrivait, et le lot 7 la **dérivait** à la place. Deux
sources de la même information, divergeant déjà en longueur — 7 lignes déclarées
contre 9 dérivées pour HistoBrain, parce que la déclaration repliait les deux axes
transverses en une ligne et enfouissait le hub de ralliement. C'est exactement le
constat E4 que le manifeste existe pour supprimer.

Le lot 7 proposait deux issues et ne tranchait pas. **Tranché ici : la
déclaration est retirée**, c'est-à-dire la seconde issue, la plus simple.

L'argument contre la première (« marquer le champ `genere: true` et le régénérer
à chaque composition ») : un champ régénéré depuis la dérivation n'est pas une
source, c'est une **copie** — avec, en plus, le coût de la tenir à jour et le
risque qu'un jour elle ne le soit plus. L'argument *pour* la première était « ça
garde un manifeste lisible seul » ; il ne tient pas, parce que ce qui rend la
règle lisible seule est son **énoncé** et sa **clause**, pas la table de ses
lignes — et ces deux phrases restent, elles.

Trois changements, dans un commit séparé et explicite :

- `schema/brain.schema.json` : `table` sort de `required`, et un `$comment` dit
  pourquoi. Le champ reste **accepté** — le refuser invaliderait les deux
  exemples, qui sont des manifestes écrits avant l'arbitrage ;
- `brainkit/entretien/composer.py` : n'écrit plus ni `table` ni
  `hubs_transverses`. Il garde `enonce`, `clause`, `derivee: true` et son motif ;
- `brainkit/mesurer/backlog.py` : confronte une table encore déclarée à la
  dérivation, sous le code `E4`. Une seconde source qu'on ne veut plus se
  **mesure** — et la mesure retrouve le chiffre du lot 7 : « 7 lignes déclarées
  contre 9 dérivées » pour HistoBrain, « 6 contre 8 » pour DevBrain.

Les deux exemples restent valides, les trois cas de `schema/valider.py` passent,
et les cinq jeux d'épreuve des lots 2 à 7 sont verts.

---

# 6. Le renommage de branche

Le dépôt BrainKit était sur `master` alors que les trois manifestes déclarent
`git.branche_principale: main`. Corrigé : `git branch -m master main`.

Vérifications faites :

| ce qui a été vérifié | résultat |
|---|---|
| le dépôt a-t-il un remote ? | **non** — rien à repousser, rien à retracker |
| du code suppose-t-il un nom de branche ? | non : `semer/depot.py` et `skills/cloture.py` lisent `git.branche_principale` avec `"main"` pour défaut, et n'écrivent jamais `master` |
| les trois manifestes | déclaraient déjà `main` — c'est le dépôt qui était en retard, pas eux |
| les trois hooks | inchangés, et ils continuent de refuser (le premier commit du lot est passé sous `master`, les suivants sous `main`, sans différence) |
| l'identité git | **non touchée** — `git config --local` reste `floSa` / l'adresse perso |

Un point est resté en dehors et il est en remontée : `init.defaultBranch` vaut
`master` sur la machine, ce qui explique l'origine. Ce réglage est global, il
n'affecte que les `git init` futurs, et changer la configuration globale de la
machine sort du périmètre d'un lot.

---

# 7. Les arbitrages

## 7.1 Le plancher se lit deux fois — d'instance, et de règle

**Le fait.** §5.6 écrit un seul plancher : « 30 pages de l'unité ». Une règle
peut avoir une population bien plus petite que le nombre de pages de l'unité :
`hub_par_niveau` mesure 64 dossiers, `couverture_des_vues/b` mesure 47 fichiers
de vue, `collision_alias` sur le vault d'épreuve mesure 0 page.

**L'arbitrage.** Le plancher s'applique **aussi** à la population réelle de la
règle. Le cadrage exprime son plancher en pages de l'unité parce que c'est la
population de la plupart des règles ; une règle dont la population réelle est
plus petite n'est pas couverte par ce raisonnement, et la lettre du texte la
laisserait passer alors que son esprit la refuse.

**Ce que ça coûte, mesuré.** Sur DevBrain : **rien**. Aucune règle proposable n'a
une population sous 30, donc la seconde lecture ne retire aucune proposition. Un
garde-fou qui ne se paie pas et qui ferme un trou se pose.

**L'exception, unique et nommée.** Une règle vérifiable **sur le manifeste**
(`sur_le_manifeste`) échappe au plancher : son dénominateur n'est pas un volume
de corpus. C'est le cas de `paire_inverse_bien_declaree`, qu'HistoBrain déclare
dure d'emblée — et ce n'est pas une entorse au principe 1, c'est un trou qu'on
refuse d'ouvrir, comme `frontmatter_lisible`.

## 7.2 Garde-fou 3 signale, il ne propose pas — et c'est ce qui tient les deux textes

**Le conflit apparent.** §5.6 veut `chemin_categorie` et `bandeau_a_jour` dures
dès le départ. Le critère d'acceptation de ce lot veut **zéro proposition** sur
HistoBrain, qui les déclare `a_mesurer`.

**L'arbitrage.** Ces deux règles **sortent du régime de la mesure**. Leur dureté
ne s'obtient pas en comptant des violations — elle vient de ce qu'une violation y
est une incohérence de structure — donc elle se décide **quand le manifeste
s'écrit**, pas quand on mesure. `mesurer` ne propose rien pour elles, ni sous le
plancher ni au-dessus ; il **signale** qu'un manifeste les déclare autrement.

**Ce qui est tranché, et ce qui ne l'est pas.** §5.6 posait la question « est-ce
une exception acceptable au principe 1 ? » et recommandait « oui, et l'écrire
comme telle ». Le prompt du lot la tranche dans ce sens : les deux règles sont
non négociables. Ce que le lot n'a **pas** fait, et ne pouvait pas faire, c'est
appliquer la conséquence dans `histobrain.brain.yml` : ce serait écrire une
sévérité dans un manifeste, ce qui appartient à celui qui l'écrit. Le kit dit la
contradiction ; il ne la résout pas.

## 7.3 La liste des structurellement dures est fermée par le KIT, pas par le manifeste

**Le fait.** `devbrain.brain.yml` porte `structurellement_dure: true` sur ses deux
règles ; `histobrain.brain.yml` porte `structurellement_dure: false` sur les
siennes, avec un motif écrit qui dit que le point n'était pas tranché.

**L'arbitrage.** Le kit **ne lit pas** ce champ pour décider. Un garde-fou qu'une
instance peut désactiver en écrivant un booléen n'est pas un garde-fou, c'est une
option. La liste vit dans `gardes.STRUCTURELLEMENT_DURES`, à côté de
`LES_DIX` — deux listes fermées par le kit, pour la même raison.

Le champ du manifeste garde une utilité : il est **cité dans le message de
contradiction**, ce qui rend visible d'un coup d'œil que le manifeste avait une
opinion, et laquelle.

## 7.4 La sévérité se décide au niveau où elle est déclarée

**Le fait.** `couverture_des_vues` produit cinq sous-constats (a, b, c, d, e) et
déclare **une seule** sévérité, scalaire. Le sous-constat `c` est à zéro
violation sur 47 fichiers de vue ; `a` en a treize.

**Le piège.** Une lecture par sous-clé aurait proposé de durcir `c`. Or il
n'existe aucune façon d'écrire ça dans le manifeste : la sévérité est un scalaire,
la durcir durcirait aussi `a`, `b`, `d` et `e`.

**L'arbitrage.** L'**unité de décision** est la clé sur laquelle la sévérité est
**déclarée** : la règle entière quand la sévérité est scalaire, la section quand
elle est une table (`etiquettes_fermees`, dont `Mise en œuvre` est dure et
`Ressources` en avertissement). Les sous-comptes restent **affichés** en détail —
ce sont eux que le critère du lot 3 confronte — mais ils ne portent pas de
verdict.

## 7.5 `mesurer` sort en 1 quand le garde-fou 2 refuse, et en 0 quand le plancher refuse

**Le fait.** Deux refus cohabitent dans la sortie, et ils n'ont pas la même
nature. Le plancher refuse une **proposition** ; le garde-fou 2 refuse un
**manifeste**.

**L'arbitrage.** Seul le second change le code de sortie. Un vault de douze pages
qui refuse tout durcissement est un vault en bonne santé ; un manifeste qui porte
une sévérité dont personne n'a écrit la raison est un manifeste en faute, et
§5.6 dit « le kit refuse ». Un refus qui ne se voit pas dans le code de sortie
est un refus que personne ne lit.

**Conséquence assumée** : `brainkit mesurer` sur DevBrain sort en **1**, et
c'est correct. La mesure est complète ; c'est le manifeste qui doit deux phrases.

## 7.6 La population est déclarée par la règle, pas recalculée par la mesure

**L'alternative écartée.** Recalculer chaque périmètre dans `brainkit/mesurer/`
depuis les `roles:`, `champ:` et `sections:` du manifeste. C'était moins invasif
— zéro ligne touchée dans le validateur.

**Le motif du refus.** Deux codes qui calculent le même périmètre divergent au
premier correctif, et **en silence** : le validateur contrôlerait un ensemble
pendant que la mesure en annoncerait un autre. C'est le constat E4, appliqué au
kit lui-même.

**Ce que ça a coûté.** Vingt-cinq appels à `Rapport.population()` dans `dix.py`,
`socle.py` et `vues.py`. **Aucun verdict n'a bougé** : DevBrain reste à 0 dure et
111 avertissements, et les cinq jeux d'épreuve des lots 2 à 7 sont verts.

**Ce que ça a rapporté, et qui n'était pas cherché** : deux vérifications
gratuites. `redirection_sourcee` retrouve les 1 388 cellules du manifeste, et
`chemin_categorie` retrouve les 681 pages de `check_arbo`.

## 7.7 La déclaration `propagation.table` est retirée, pas régénérée

Voir §5.5. Résumé : un champ régénéré depuis une dérivation n'est pas une source,
c'est une copie ; l'énoncé et la clause suffisent à rendre le manifeste lisible
seul.

## 7.8 Aucun motif n'a été écrit à la place de floSa

**Le fait.** Le garde-fou 2 refuse deux règles de `devbrain.brain.yml`. Écrire
leurs motifs aurait fait sortir la commande en 0.

**L'arbitrage.** Ne pas les écrire. Un motif est la **raison de celui qui a pris
la décision** ; en inventer un produirait exactement ce que §5.6 interdit — une
sévérité qui a l'air motivée et qui ne l'est pas. Le refus reste, et il est en
remontée 1.

---

# 8. Le critère d'acceptation, point par point

| ce que le lot demandait | résultat |
|---|---|
| `mesurer` retrouve les comptes du lot 8 du DevBrain : **62** | **62**, sur une population mesurée de 334 pages |
| … **5** pour les étiquettes de ressources | **5**, sur 337 pages · 647 étiquettes |
| … le troisième compte, daté, vaut 4 aujourd'hui | **4** — vérifié contre le vault, et écrit en §3.1 |
| `mesurer` **REFUSE** de proposer un durcissement sur HistoBrain | **aucune proposition**, 11 règles refusées, 20 pages manquantes nommées |
| le premier rapport de mesure d'HistoBrain est produit et lisible | `AI/mesure/2026-09-07-mesure.md`, 188 lignes, trois sections |
| les cinq jeux d'épreuve des lots 2 à 7 restent verts | **verts**, tous les cinq |
| `valider` sur DevBrain rend 0 dure et 111 avertissements | **0 et 111**, inchangés — y compris après le branchement de `racine:` |

Le jeu d'épreuve du lot lui-même — `tests/mesure.py`, neuf scénarios — tient ces
résultats **en code** : les trois comptes historiques, les 1 388 cellules, le
recensement 681/20/10 plus 74 hubs, les deux règles sans motif nommées, et le
contrôle négatif.

Les scénarios 1 et 2 sont **jumeaux**, et c'est ce qui rend le contrôle négatif
concluant : le même vault, la même mesure, et une seule chose qui change — le
plancher, abaissé en mémoire. Sans le second, on prouverait que l'outil ne
propose jamais rien ; avec lui, on prouve que c'est bien le plancher qui l'en
empêche.

---

# 9. Remontées

*Ce qui a été trouvé hors du périmètre du lot, et qui ne s'y corrige pas. Une
remontée nomme le fait, dit ce qu'il coûte, et propose — elle ne tranche pas.*

**1 — Deux règles du DevBrain sont souples sans qu'aucun motif n'ait jamais été
écrit.** *(mesuré, lot 8)* `taille_avertissement` et `collision_alias` déclarent
`severite: avertissement` et ne portent ni `motif:` ni `note_<x>`. Le garde-fou 2
les refuse, et `brainkit mesurer` sort en 1 sur DevBrain à cause d'elles. Coût :
tant que ces deux phrases ne sont pas écrites, la commande de mesure ne peut pas
sortir en 0 sur le vault de référence, ce qui rendra le lot 9 bruyant. Les motifs
n'ont **pas** été écrits ici — inventer une raison à la place de celui qui a pris
la décision produirait exactement ce que §5.6 interdit. Proposition : deux
phrases dans `devbrain.brain.yml` au lot 9, ou le constat que ces règles étaient
souples par défaut et non par décision — auquel cas le motif est *« jamais
mesurée »* et la vraie réponse est `a_mesurer`.

**2 — `taille_avertissement` est proposée à `dure`, et la proposition mérite un
débat.** *(mesuré, lot 8)* 0 violation sur 634 pages : la mesure autorise le
durcissement. Mais durcir signifie qu'une page qui dépasse `taille_avertissement`
lignes fait **échouer** la validation, donc bloque une clôture. C'est une
décision éditoriale (« une page longue est-elle une faute ? »), pas technique.
Le kit a fait son travail en la proposant ; l'appliquer est un arbitrage de
floSa, au lot 9. Note : la même mesure vaut argument dans l'autre sens — zéro
violation en dix-huit mois peut vouloir dire que la limite est trop haute pour
mordre.

**3 — `vocabulaire_ferme` déclare une sévérité qu'elle n'applique pas.** *(lot 3,
remontée 2, désormais VISIBLE)* La règle déclare `severite: dure` et
`code: [R4, R14, R14b]` ; `R14b` sort en **avertissement**, parce que sa sévérité
vit dans `axes.nature.vide_autorise` et non dans la règle. Le moteur lit la bonne
source depuis le lot 3 ; ce qui est neuf, c'est que `mesurer` **voit** l'écart et
l'imprime (« sévérité déclarée `dure`, sévérité APPLIQUÉE `avertissement` »).
Coût : un lecteur du manifeste croit la règle entièrement dure. Le fait se
reproduit à l'identique sur les deux vaults. Proposition inchangée depuis le
lot 3 : découper la règle de socle en trois, ou déclarer la sévérité comme une
table par sous-code — ce qui demande d'écrire trois énoncés que personne n'a
encore écrits.

**4 — `agent.sous` ne déclare aucune place pour un rapport de mesure.** *(lot 5 /
lot 6)* Le rapport d'HistoBrain a été déposé dans `AI/mesure/`, un dossier que le
manifeste ne déclare pas : `agent.sous` liste `design/`, `migration/`, `index/`,
`sessions/`, `scripts/` et `backlog.md`. Le kit produit donc un artefact que
l'instance n'a pas de place pour recevoir, et le chemin est passé à la main en
`--rapport`. Coût faible aujourd'hui, réel au lot 10 : un `INSTALL.md` généré
devra dire où mettre les rapports. Proposition : une entrée
`{ chemin: "mesure/", role: "les rapports de `brainkit mesurer`, datés" }` dans
`agent.sous`, et un défaut de `--rapport` qui la lise.

**5 — `init.defaultBranch` vaut `master` sur la machine.** *(hygiène)* C'est
l'origine du dépôt sur `master` alors que tous les manifestes déclarent `main`.
La branche du dépôt est corrigée ; le réglage global, lui, ne l'est pas — il est
hors du périmètre d'un lot, et il ne concerne que les `git init` futurs. Coût :
le prochain dépôt créé sur cette machine repartira sur `master`. Proposition :
`git config --global init.defaultBranch main`, ou une étape de l'`INSTALL.md` du
lot 10 pour un poste neuf.

**6 — `brique.Alternatives` : 8 pages portent le titre et rien dessous.**
*(mesuré, lot 8)* Présente sur 324 briques, remplie sur 316. Huit briques ont
donc un `## Écosystème` → `### Alternatives` vide, ce qu'aucune règle n'attrape :
`couverture_de_section` ne mord que si le **champ** `alternatives:` porte des
cibles, et `voisinage_declare` ne mord que si le champ est vide **et** que le
dossier est peuplé. Une section vide sur une page dont le champ est vide et le
dossier solitaire passe entre les deux. Coût : huit sections vides dans le vault
de référence, invisibles aux deux validateurs. Ce n'est pas forcément une faute —
la forme recommandée pour une section sans voisine est une **phrase** (« aucune
outillée dans le brain : … »), et huit pages ne l'ont pas écrite. Proposition :
regarder les huit au lot 9, et décider si une section déclarée non
conditionnelle doit être non vide.

**7 — Le compte de `F8` diffère de celui du lot 2, et le périmètre explique tout.**
*(lot 2 / lot 8)* Le lot 2 comptait `os` sur **37** briques ; `mesurer` en compte
**40**, et trouve en plus `domaines` sur **39**. L'écart n'est pas une
divergence de mesure : le lot 2 lisait `F8` sur un sous-ensemble (les briques
confrontées à leur gabarit), la mesure lit toutes les pages du rôle. Coût : deux
chiffres différents pour la même chose dans deux documents du projet.
Proposition : au lot 9, aligner le périmètre de `F8` dans `fidelite.py` sur
celui de `mesurer`, ou écrire la différence dans les deux.

**8 — `hub_par_niveau` mesure 64 dossiers pour 74 hubs.** *(observation)* La
règle ne regarde que les dossiers qui portent au moins une page rangée par
l'axe ; dix hubs vivent donc dans des dossiers qu'elle ne visite pas
(`Métiers/`, `Comparatifs/`, `Patterns/`, `Rules/` et leurs niveaux). Ce n'est
pas une faute — ces dossiers sont groupés par `role:`, pas par l'axe — mais la
règle ne peut structurellement pas y détecter un hub manquant. Coût : un angle
mort de dix dossiers dans une règle **dure**. Proposition : vérifier au lot 9 que
`A13`/`A15` de `fidelite.py` couvrent bien ces dix, sinon la règle a un trou que
personne ne voit.

**9 — Le rapport Markdown n'a pas de version « courte ».** *(lot 10)* Le rapport
d'HistoBrain fait 188 lignes dont 60 de backlog `A1` — vingt valeurs d'axe
déclarées sans page, ce qui est **normal** dans un brain neuf et attendu pendant
des mois. Coût : la première chose qu'on lit dans le premier rapport d'une
instance neuve est une liste de vingt lignes qui disent toutes la même chose.
Proposition : replier `A1` en une ligne (« 20 valeurs déclarées sans page, dont
15 sous-valeurs — normal avant l'amorçage ») avec le détail derrière une option.

**10 — `couverture_des_vues/c` est une règle vivante et parfaitement invisible.**
*(lot 3)* Le sous-constat « une vue que plus aucune page ne cite » n'apparaît
dans aucun tableau du lot 3, parce qu'il n'a jamais produit de constat. Il existe
pourtant bien des deux côtés : `check_brain.py:654` l'émet sous `R8c`, et
`vues.py` le porte. La mesure le rend visible **avec son dénominateur** — 0 sur
47 fichiers de vue —, ce qui est exactement le service que le lot 8 rend. Ce qui
mérite d'être noté : c'était, jusqu'à aujourd'hui, une règle dont personne ne
pouvait dire si elle tournait ou si elle était morte. Le mot du lot 3 s'applique
à un cran plus bas que là où il avait été écrit : **un sous-constat sans
dénominateur ne ressemble pas à un sous-constat satisfait, il ne ressemble à
rien.** Proposition : imprimer la population de chaque sous-constat dans la table
du validateur, et pas seulement dans celle de la mesure — c'est trois lignes.

---

# 10. Ce qui reste au lot 9

- **Les deux motifs manquants** (remontée 1) et l'arbitrage sur
  `taille_avertissement` (remontée 2) : ce sont les deux premières choses que le
  lot 9 écrira dans `devbrain.brain.yml`, et ce sont les deux premières que ce
  lot s'est interdit d'écrire.
- **La décision sur les deux structurellement dures d'HistoBrain** : le kit dit
  la contradiction, il ne l'a pas résolue. Une instance qui l'applique change
  `severite: a_mesurer` en `dure` sur deux règles, et retire
  `structurellement_dure: false`.
- **Les cinq `skill/*` orphelines** : inchangées depuis le lot 2, et toujours à
  floSa.
- **Le durcissement de `page_atteignable` dans HistoBrain** ne se pose pas : la
  règle y a 13 violations, donc le verdict est « à réparer », pas « proposée ».
  Ce qui se pose est la remontée 1 du lot 7 — donner un hub d'index à chaque
  dossier d'axe transverse — et elle reste ouverte.
