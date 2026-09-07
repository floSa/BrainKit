# BrainKit — le moteur de validation, branché sur le manifeste

> Conversation 44, « BrainKit lot 3, le moteur de validation », le 2026-09-07.
> Entrées : `design/01-manifeste.md` · `design/02-rapport-fidelite.md` ·
> `exemples/devbrain.brain.yml` · les deux validateurs du DevBrain, en
> **lecture seule absolue**.
>
> Livrables du lot : `brainkit/valider/` (neuf modules) · `tests/` (le jeu
> d'épreuve : un manifeste, deux vaults jumeaux, six scénarios) · ce document ·
> les trois corrections du manifeste que le moteur a exigées (commit
> `lot 3 : les trois corrections du manifeste…`).
>
> **Aucune écriture dans DevBrain.** Rien n'est généré : ni hub, ni index, ni
> bandeau, ni gabarit — c'est le lot 4. Aucune règle nouvelle, aucun changement
> de sévérité. Des douze points ouverts de `00-cadrage.md` §5, aucun n'est
> tranché hors des **trois arbitrages** que le lot 2 a explicitement renvoyés ici.

Le lot 2 a prouvé que le manifeste sait **redire** DevBrain. Ce lot répond à la
question suivante : sait-il le **valider** ? Le verdict tient en une phrase —
**oui, à la violation près, et il a fallu corriger le manifeste sur trois points
pour que ce soit vrai.**

---

# 1. Le critère d'acceptation, et comment il est tenu

Le critère du lot est dur : *sur DevBrain en lecture seule, même verdict, règle
par règle, et même compte de violations qu'aujourd'hui. Un écart d'une seule
violation est un échec du lot.*

## 1.1 La référence, capturée avant d'écrire une ligne

Les deux validateurs actuels du vault, lancés en lecture seule le 2026-09-07.

```
$ uv run AI/scripts/check_brain.py
check_brain : 765 pages actives contrôlées
  [WARN] … (111 lignes)
OK — aucune violation dure. (111 avertissement(s))
                                                              → code de sortie 0

$ uv run AI/scripts/check_arbo.py
check_arbo : 681 page(s) migrée(s) dans 20 domaine(s) — 10 rangée(s) par `role:` (pattern, rule)
  Automatisation no-code/ — 6 page(s)
  … (20 lignes, une par domaine)
OK — chemin et catégorie concordent partout.
                                                              → code de sortie 0
```

Le dépouillement des 111 avertissements, par code :

| Code | Compte | Ce que le code signale |
|---|---|---|
| `R20` | **62** | champ de voisinage vide dans un dossier peuplé |
| `R8a` | **13** | valeur d'axe assez peuplée sans vue qui la réunisse |
| `R5` | **13** | doublon d'alias, ou alias qui est le `nom:` d'une autre page du même rôle |
| `R8e` | **11** | page hors de toute vue alors qu'une vue retient ses pairs |
| `R23` | **5** | étiquette de `## Ressources` hors du vocabulaire fermé |
| `R26` | **4** | `## Définition` redit peut-être le bandeau |
| `R8d` | **1** | filtre de vue par liste de noms codée en dur |
| `R8b` | **1** | vue à moins de deux membres |
| `R14b` | **1** | `role: brique` sans valeur d'axe de nature |
| **Total** | **111** | **0 violation dure** |

## 1.2 Le verdict du nouveau moteur, côte à côte

```
$ uv run brainkit/valider/__main__.py
valider : 765 page(s) contrôlée(s) — vault `DevBrain`, manifeste `devbrain.brain.yml`
  [WARN] … (111 lignes)

verdict, règle par règle :
  reciprocite                        · 0 — tournée, aucun constat
  chemin_categorie                   · 0 — tournée, aucun constat
  completude_du_hub                  · 0 — tournée, aucun constat
  voisinage_declare                  · 62 avertissement
  redirection_sourcee                · 0 — tournée, aucun constat
  reinjection_du_resume              · 0 — tournée, aucun constat
  etiquettes_fermees/Ressources      · 5 avertissement
  citation_unique                    · 0 — tournée, aucun constat
  bandeau_a_jour                     · 0 — déléguée — portée par `build_bandeau --check`
  anti_repetition                    · 4 avertissement
  frontmatter_lisible                · 0 — tournée, aucun constat
  gabarit_par_role                   · 0 — tournée, aucun constat
  liens_resolus                      · 0 — tournée, aucun constat
  couverture_de_section              · 0 — tournée, aucun constat
  lien_vers_une_page_a_comprendre    · 0 — tournée, aucun constat
  nom_egal_fichier                   · 0 — tournée, aucun constat
  page_atteignable                   · 0 — tournée, aucun constat
  hub_par_niveau                     · 0 — tournée, aucun constat
  vocabulaire_ferme/axe_vide         · 1 avertissement
  unicite_du_nom_de_fichier          · 0 — tournée, aucun constat
  taille_avertissement               · 0 — tournée, aucun constat
  collision_alias                    · 13 avertissement
  couverture_des_vues/a              · 13 avertissement
  couverture_des_vues/b              · 1 avertissement
  couverture_des_vues/d              · 1 avertissement
  couverture_des_vues/e              · 11 avertissement
  champs_supprimes                   · 0 — tournée, aucun constat
  paire_inverse_bien_declaree        · 0 — non déclarée par ce manifeste

OK — aucune violation dure. (111 avertissement(s))
                                                              → code de sortie 0
```

| Code de référence | Référence | Moteur | Règle du manifeste |
|---|---|---|---|
| `R20` | 62 | **62** | `voisinage_declare` |
| `R8a` | 13 | **13** | `couverture_des_vues/a` |
| `R5` | 13 | **13** | `collision_alias` |
| `R8e` | 11 | **11** | `couverture_des_vues/e` |
| `R23` | 5 | **5** | `etiquettes_fermees/Ressources` |
| `R26` | 4 | **4** | `anti_repetition` |
| `R8d` | 1 | **1** | `couverture_des_vues/d` |
| `R8b` | 1 | **1** | `couverture_des_vues/b` |
| `R14b` | 1 | **1** | `vocabulaire_ferme/axe_vide` |
| **dures** | **0** | **0** | — |
| **total** | **111** | **111** | — |

## 1.3 L'égalité ne porte pas sur les comptes, elle porte sur les PAGES

Un compte égal peut cacher deux ensembles différents de même taille — c'est
exactement l'erreur que le lot 2 a documentée en boîte 1, point 7 (« les hubs
spéciaux sont trois, les manquants sont trois, donc ce sont les mêmes » : les
deux ensembles se recouvraient à moitié). La vérification porte donc sur les
**sujets**, code par code :

| Code | Sujets de référence | Sujets du moteur | Verdict |
|---|---|---|---|
| `R20`, `R5`, `R8b`, `R8d`, `R8e`, `R23`, `R26`, `R14b` | — | — | **ensembles IDENTIQUES** |
| `R8a` | 13 valeurs d'axe | les **mêmes** 13 | identiques, au libellé près |

Le seul écart de tout le lot est un **libellé de message** : la référence écrit
`categorie \`data/format\``, le moteur écrit `` `data/format` ``. Le mot
« categorie » est un mot du DevBrain ; le moteur ne l'a pas dans son code — il
lit `libelles.axe_rangement`, et le message n'a pas à porter le nom du champ.

Le sixième scénario de `tests/epreuve.py` **tient ce critère en code** : il
recharge `devbrain.brain.yml`, valide le vrai vault, et compare les neuf comptes
un par un à la table de la section 1.1. Un écart d'une violation fait échouer le
jeu d'épreuve, et pas seulement une relecture.

## 1.4 Le compte du lot 8 sur les trois avertissements : deux sur trois

L'énoncé du lot annonçait « 62, 5 et 11-dont-2 » et demandait de **vérifier
contre le vault plutôt que de recopier**. Le vault dit :

| Règle en avertissement | Mesure du lot 8 (2026-09-06) | Vault (2026-09-07) | |
|---|---|---|---|
| `voisinage_declare` (R20) | 62 | **62** | conforme |
| `etiquettes_fermees` / `Ressources` (R23) | 5 | **5** | conforme |
| `anti_repetition` (R26) | 11 candidats, 2 vrais | **4 candidats** | **écart — remontée 1** |

C'est le vault qui a raison. Le détail est en *Remontées*, point 1.

---

# 2. La correspondance, règle par règle

Trente contrôles dans l'ancien code, vingt-cinq règles branchées par le
manifeste. La correspondance n'est pas une bijection, et c'est le sujet de cette
section : trois contrôles ont **fusionné** dans une règle, un a été **délégué**,
et deux règles dures que le manifeste **avait oubliées** ont dû y être ajoutées.

## 2.1 Les dix règles de `brain-v3.md` §10

| # | Règle | Sévérité déclarée | Codes de l'ancien code | Où elle vit | Paramètres LUS dans le manifeste |
|---|---|---|---|---|---|
| 1 | `reciprocite` | dure | `R12`, `R18` | `dix.reciprocite` | `regles[].champs`, `champs.<x>.reciproque.{mode,champ}` |
| 2 | `chemin_categorie` | dure | `check_arbo` (1) | `dix.chemin_categorie` + `chemins.py` | `axes.rangement.{champ,exclusif,regle_de_majorite,prefixe_transversal,seuil_promotion,plafond_promotion,valeur_courte_autorisee,prefixes,rattachements}`, `roles[].{range_par,porte_categorie,pese_sur_le_seuil}` |
| 3 | `completude_du_hub` | dure | `R19` | `dix.completude_du_hub` | `regles[].roles`, à défaut `roles[].apparait_dans_le_hub` |
| 4 | `voisinage_declare` | **avertissement**, définitif | `R20` | `dix.voisinage_declare` | `regles[].champ`, et le périmètre se **dérive** : les rôles dont `autorises` porte ce champ |
| 5 | `redirection_sourcee` | dure | `R21` | `dix.redirection_sourcee` | `regles[].{sections,colonne,marqueur}`, `corps[genre: decision].colonne_positive`, l'index des pages `fonction: unite` |
| 6 | `reinjection_du_resume` | dure | `R1`, `R22` | `dix.reinjection_du_resume` | `regles[].{champ_resume,sections}`, `corps[].champ`, `champs.<x>.fonction: resume_court` |
| 7 | `etiquettes_fermees` | **table** : dure / avertissement | `R23` | `dix.etiquettes_fermees` | `regles[].severite` **par section**, `corps[genre: etiquetee].{obligatoires,permises}` |
| 8 | `citation_unique` | dure | `R24` | `dix.citation_unique` | `regles[].sections`, `corps[genre: liste_liens]` |
| 9 | `bandeau_a_jour` | dure | `build_bandeau --check` | **DÉLÉGUÉE**, déclarée comme telle | — |
| 10 | `anti_repetition` | **avertissement**, définitif, non scriptable | `R26` | `dix.anti_repetition` | `regles[].motifs_bornes`, indexés par **colonne de bandeau** ; `bandeau.{porte_par,colonnes}` ; `corps[genre: prose]` |

(1) `check_arbo` n'a pas de code `R` : c'est un script entier, et sa raison
d'être — un contrôle sur trois — est cette règle. Cf. *Remontées*, point 10.

**La règle 9 est déléguée, et c'est dit à haute voix.** Vérifier que la zone AUTO
du bandeau concorde avec le frontmatter, c'est **régénérer** le bandeau et
comparer les octets — donc posséder le générateur, qui est le lot 4. Le
validateur ne la réimplémente pas à moitié : il l'imprime dans son inventaire
avec son porteur nommé. C'est la leçon de `completude_du_hub`, retenue à
l'envers : *« une règle absente ne ressemble pas à une règle souple, elle
ressemble à une règle satisfaite. »*

## 2.2 Les règles de socle

| Règle | Sévérité | Ancien code | Où elle vit | Paramètres lus |
|---|---|---|---|---|
| `frontmatter_lisible` | dure | `R17` | `socle.frontmatter_lisible` | — (les quatre motifs sont une convention de format) |
| `gabarit_par_role` | dure | `R3` + les deux boucles sans code + `R16` | `socle.gabarit_par_role` | `roles[].champs.{requis,autorises,conditionnels}` |
| `vocabulaire_ferme` | dure | `R4`, `R14`, les trois boucles d'enum, (+ `R14b`) | `socle.vocabulaire_ferme` | `champs.<x>.{type,source,valeurs}`, `axes.*`, `vocabulaires.<x>.{fichier,mode,lecture,genere}` |
| `nom_egal_fichier` | dure | `R9` | `socle.nom_egal_fichier` | `champs.<x>.fonction: identite` |
| `liens_resolus` | dure | `R2` + la boucle du corps | `socle.liens_resolus` | `vue_embarquee.extension` (pour la seconde clé de résolution) |
| `page_atteignable` | dure | `R7` | `socle.page_atteignable` | `roles[fonction: hub]` |
| `hub_par_niveau` | dure | `check_arbo` (3) | `socle.hub_par_niveau` | `roles[fonction: hub]`, `roles[].porte_categorie` |
| `unicite_du_nom_de_fichier` | dure | **aucun — jamais implémentée** | `socle.unicite_du_nom_de_fichier` | `vue_embarquee.extension` |
| `taille_avertissement` | avertissement | la boucle sans code | `socle.taille_avertissement` | `roles[].taille_avertissement` |
| `collision_alias` | avertissement | `R5` | `socle.collision_alias` | `champs.<x>.fonction: alias` et `: identite` |
| `couverture_des_vues` | avertissement | `R8`, `R8a`..`R8e` | `vues.couverture_des_vues` | `seuils.{vue_min_valeurs_axe,vue_min_membres}`, `vue_embarquee.{extension,moteur}` |
| `champs_supprimes` | dure | `R25` | `socle.champs_supprimes` | `champs.<x>.deprecated` ∖ tous les `autorises` ; `genere.non_pages` ; `agent.racine` |
| `couverture_de_section` | dure | `R11`, `R22` | `socle.couverture_de_section` | `corps[genre: liste_liens].champ` |
| `lien_vers_une_page_a_comprendre` | dure | `R15` | `socle.lien_vers_une_page_a_comprendre` | `roles[].fonction` : `unite` d'un côté, `notion` et `hub` de l'autre |
| `paire_inverse_bien_declaree` | dure | **aucun — le mode inverse n'existe pas dans DevBrain** | `socle.paire_inverse_bien_declaree` | `champs.<x>.reciproque` — vérifiable sur le manifeste SEUL |

### Trois contrôles fondus en un, et pourquoi

`gabarit_par_role` absorbe quatre choses que l'ancien code écrivait en quatre
endroits : le `role:` sans gabarit (`R3`), les champs requis vides (sans code),
les champs hors gabarit (sans code) et les champs conditionnels (`R16`). La
raison n'est pas la concision : **le manifeste ne déclare qu'une règle pour les
quatre.** `roles[].champs` est un objet, avec une sévérité, et les quatre
contrôles en sont les quatre clauses. Les fondre garde la sévérité **là où le
manifeste la met** ; les séparer aurait obligé le moteur à inventer trois
sévérités que personne n'a déclarées.

Le compte reste séparable : `R16` sort avec la clé `conditionnels`, ce qui rend
la ligne `gabarit_par_role/conditionnels` comparable à part dans le verdict.

### `R14b` : la règle dont la sévérité ne vit pas dans la règle

`regles_de_socle[vocabulaire_ferme]` déclare `severite: dure` et
`code: [R4, R14, R14b]`. Or `R14b` est un **avertissement** dans le code de
référence. Le moteur ne suit donc pas la sévérité de la règle sur cette clause :
il la lit **où elle vit vraiment**, dans `axes.nature.vide_autorise`.

Ce n'est pas un contournement, c'est la lecture du manifeste au bon endroit. Le
champ dit exactement ce qu'il faut savoir : *« un champ vide est le SEUL signal
prévu pour "l'arbre de décision n'a pas tranché" ; une valeur inventée est une
faute, un champ vide est une question ouverte »*. `vide_autorise: true` **est**
la déclaration que l'absence signale sans faire faute. Le moteur sort donc
l'absence en avertissement quand le champ vaut `true`, et en dur quand il vaut
`false`, et il n'a aucune sévérité à inventer. La liste de codes reste trompeuse,
et c'est la remontée 2.

## 2.3 Les cinq sous-codes de `R8`

`regles_de_socle[couverture_des_vues].code` déclare `[R8, R8e]`. Le code de
référence en émet **cinq** : `R8` (vue illisible ou non évaluable), `R8a`
(valeur peuplée sans vue), `R8b` (vue sans comparaison), `R8c` (vue citée par
personne), `R8d` (filtre par liste de noms codée en dur), `R8e` (page hors de
toute vue). Le moteur les garde tous les cinq, distingués par la clé `a`..`e`,
pour que le verdict soit comparable ligne par ligne. Sur DevBrain : `a` 13,
`b` 1, `d` 1, `e` 11, `c` et `R8` à zéro.

---

# 3. Ce qui a été JETÉ

C'est la dette morte du point §5.10 du cadrage, et la recommandation y était
écrite : *« la portabilité se fait par réécriture guidée, pas par copie. Le
critère d'acceptation autorise à jeter tout ce qui ne sert plus. »* Voici ce qui
a été jeté, et pourquoi.

## 3.1 La dette que §5.10 nommait

| Jeté | Ce que c'était | Pourquoi |
|---|---|---|
| `V1_MARKERS` (11 noms de champs) et `is_active_v2()` | le filtre du réservoir v1, qui ne s'appliquait que sous `Wiki/` | `Wiki/` a été supprimé à la clôture du lot 4, le 2026-09-05. La fonction rendait `True` pour toutes les pages depuis quinze mois, et le jeu de onze champs ne servait plus à rien. **Le porter aurait mis la dette du DevBrain dans toutes les instances** — c'est le risque exact que §5.10 décrit. |
| `arbo.LEGACY`, le compteur `legacy` et le message *« N page(s) encore sous … »* | les dossiers racine « pas encore migrés » | l'ensemble est **vide** depuis le 2026-09-05, et c'est un point d'arrivée. Le manifeste n'a pas d'équivalent, et n'en a pas besoin : un dossier qui porte des pages porte des pages, et `genere.non_pages` dit lesquels n'en portent pas. |
| le `# 5b. R6 retirée avec status:` | un commentaire tenant la place d'une règle supprimée au lot 2 | une place vide n'est pas une règle. L'inventaire du nouveau moteur dit, nommément, quelles règles n'ont rien trouvé et pourquoi — c'est ce qui remplace un commentaire. |

## 3.2 Ce que le manifeste a rendu inutile

| Jeté | Devient |
|---|---|
| `check_brain.NON_PAGES` **et** `arbo.NON_PAGES` — les deux, identiques | `genere.non_pages`, lu une fois |
| `arbo.DOM_LABEL` (20), `arbo.DOM_RATTACHE` (1), `arbo.SUB_LABEL` (47), `arbo.SEUIL` | `axes.rangement.{prefixes,rattachements,seuil_promotion}` |
| `REQUIRED` et les **six** jeux `*_ALLOWED` | `roles[].champs.{requis,autorises}` |
| `VALUE_ENUMS`, `LIST_ENUMS` | `champs.<x>.{type,valeurs}` |
| `FAMILLES_HEBERGEES` | `roles[].champs.conditionnels[].si` |
| `SIZE_WARN` | `roles[].taille_avertissement` |
| `RES_LABELS`, `MEO_LABELS` | `corps[genre: etiquetee].{obligatoires,permises}` |
| `SECTIONS_LIENS`, `CHAMPS_ECOSYSTEME` | `regles[].sections`, `corps[].champ`, `champs.<x>.reciproque` |
| `MOT_LICENCE`, `MOT_MATURITE` | `regles[anti_repetition].motifs_bornes` |
| `BASE_MIN_CAT`, `BASE_MIN_MEMBRES` | `seuils.{vue_min_valeurs_axe,vue_min_membres}` |
| `CHAMPS_MORTS` | `champs.<x>.deprecated` ∖ tous les `autorises` (cf. correction 2 du manifeste) |
| `load_tag_vocab`, `load_theme_vocab`, `load_categories`, `load_familles`, `_fences` | **trois des quatre disparaissent** : les vocabulaires de l'axe de rangement, de l'axe de nature et de l'axe transverse vivent dans le manifeste. Seul `tags` reste un fichier, lu par **un** lecteur générique — et `vocabulaires.taxonomie.genere: true` dit pourquoi les trois autres ne se relisent plus : ce fichier est un **dérivé** du manifeste, et le relire recréerait le défaut que le manifeste existe pour supprimer. |
| `ALT_SECTION_RE`, `alt_section()`, `alt_names()` | la tolérance « `## Alternatives` en v2, `### Alternatives` en v3 » n'existait que pour la durée du lot 6, où dix-sept conversations convertissaient les 337 fiches en parallèle. Le lot est clos depuis le 2026-09-06, et la double lecture de niveau de titre avec elle. |
| `MOC` et `MOC.rglob()` dans `pages_aiguillage()` | le dossier `MOC/` **n'existe plus** (clôture du lot 4) ; le code le cherchait encore à chaque exécution. |
| `check_arbo.parse_fm()` | un **second** lecteur de frontmatter, identique au premier à la ligne près — les quatre mêmes motifs d'illisibilité, écrits deux fois. Un seul lecteur, dans `vault.py`. |
| `hors_vault()`, écrite dans `check_brain` | une fois, dans `vault.py` |

## 3.3 Ce qui a été jeté SANS être de la dette, et il faut le dire

| Jeté | Pourquoi, et où ça va |
|---|---|
| le recensement par domaine de `check_arbo` (« 681 page(s) migrée(s) dans 20 domaine(s) », puis vingt lignes) | c'est une **mesure**, pas une règle : elle ne rend aucun verdict. La passe de mesure est le lot 8 du kit, et c'est là que ce recensement appartient. Le moteur annonce le nombre de pages contrôlées, et s'arrête là. **Remontée 8.** |

## 3.4 Ce qui n'a PAS été jeté, contre l'apparence

Trois blocs ressemblent à de la dette et n'en sont pas. Ils sont repris **mot
pour mot**, et c'est délibéré :

- **Les expressions régulières de lecture.** `sections()` ne saute pas les blocs
  de code, `LIEN_RE` accepte un saut de ligne à l'intérieur d'un wikilink, la
  puce étiquetée exige un tiret cadratin entouré d'espaces. `outils/fidelite.py`
  fait certains de ces choix autrement. **Les corriger aurait changé les
  comptes**, et le critère du lot interdit d'améliorer une règle au passage. Ce
  qui a été trouvé au passage est en *Remontées*, point 5.
- **Les trois reformulations mesurées.** `redirection_sourcee` est la conjonction
  position × condition (357, 177, 18 puis 1 violation selon la formulation) ;
  `citation_unique` porte sur les entrées de puce (242 puis 0) ; `R8e` est la
  formulation la plus étroite qui attrape les deux groupes trouvés à la main
  (89, 51, 38 puis 11). Ces trois-là sont le résultat de mesures, et le
  manifeste porte leurs comptes. Les « simplifier » serait défaire quatre
  sessions de travail.
- **L'évaluateur de filtre de vue.** Il implémente le langage
  d'`obsidian-bases`, ce qui est une dépendance à un outil — mais le manifeste
  la **déclare** (`vue_embarquee.moteur`), et le moteur refuse de compter quand
  elle vaut autre chose. Un décompte faux serait pire qu'un décompte absent.

## 3.5 Le bilan en lignes, sans embellissement

| | Lignes |
|---|---|
| `check_brain.py` + `check_arbo.py` + `arbo.py` | **1 590** |
| `brainkit/valider/` (9 modules + 2 `__init__`) | **2 663** |

Le moteur est plus **long**, et il serait malhonnête de présenter autrement une
réécriture qui devait supprimer de la dette. Trois causes, et une seule est
bonne :

1. il porte **deux mécanismes de plus** — le mode inverse et l'axe non exclusif
   avec sa règle de majorité, son préfixe transversal et le cas de l'axe absent —
   plus **trois règles** que l'ancien code n'implémentait pas
   (`unicite_du_nom_de_fichier`, `paire_inverse_bien_declaree`) ou n'exprimait
   pas séparément ;
2. il porte un **modèle de manifeste** (384 lignes) que l'ancien code n'avait pas
   besoin d'avoir, puisque ses valeurs étaient dans ses constantes ;
3. il est **beaucoup plus commenté**, et c'est le motif de conception de ce
   dépôt depuis le lot 0 : ce qui ne tient dans aucun fichier, c'est la
   discipline d'arbitrage, et un `motif:` écrit est le seul moyen de la
   transporter.

Ce qui a **diminué**, et c'est la seule mesure qui compte pour un kit : le
nombre de valeurs du DevBrain écrites dans le code. Il est passé de plusieurs
centaines à **zéro**.

```
$ grep -nE "['\"](domaine|domaines|categorie|famille|brique|notion|pitch|alternatives|
             complements|hosted|scaling|licence_type|maturite|Définition|Alternatives|
             Ressources|Mise en)['\"]" -r brainkit/
brainkit/valider/contexte.py:112:  a_comprendre = set(mo.roles_de_fonction("notion")) | …
brainkit/valider/manifeste.py:39:  FONCTIONS = ("unite", "notion", "hub", "vue", …)
```

Les deux seules occurrences sont la **fonction** `notion`, l'un des six mots
fermés par le kit — et `histobrain.brain.yml` en porte une aussi. Ce n'est pas
un mot du dev : c'est un mot du contrat.

---

# 4. Les trois arbitrages

## 4.1 Le sens de la condition — `{champ, si, sens}`, `permet` par défaut

**Ce que le lot 2 renvoyait.** `conditionnels[].si` est une PERMISSION (le champ
n'existe que si la condition tient), pas une obligation. Lu à l'envers, il
produit 42 fausses violations sur un vault vert : 98 briques portent `hosted:` et
`scaling:`, 119 sont d'une famille hébergée, et les 21 de l'écart portent `os:`
à la place. La recommandation était de porter le sens explicitement.

**Ce qui est tranché.** Le sens est **explicite**, énumération fermée
`permet | exige`, **`permet` par défaut**. Trois décisions, pas une :

1. **Le défaut est `permet`**, et c'est une mesure et non un goût. Sur les deux
   seuls remplissages qui existent, cinq conditionnels sur cinq sont des
   permissions — les deux de DevBrain (`hosted:`, `scaling:`) et les trois de
   HistoBrain (`langue_originale:`, `traduction:`, `cote:`). Un défaut
   `exige` naîtrait avec 42 fausses violations sur le seul corpus mesuré.
2. **`exige` est implémenté**, dans `socle.gabarit_par_role` : quand la
   condition tient et que le champ est vide, la page échoue. Le lot 2 avait
   décliné l'ajout parce que **ni** DevBrain **ni** HistoBrain n'en avaient
   besoin, et le raisonnement était juste — *« ajouter un champ qu'aucun des
   deux remplissages n'emploie serait exactement le défaut que le cadrage
   reproche à `status:` »*. Ce qui a changé : le **jeu d'épreuve** en a besoin.
   Un sens qui ne peut pas s'écrire est un sens qui ne peut pas se tester, et
   une branche non testée n'est pas une branche.
3. **Le schéma gagne le champ**, `roles[].champs.conditionnels[].sens`,
   facultatif. Coût mesuré : une propriété facultative,
   `uv run schema/valider.py` reste vert sur les trois exemples, et **aucun
   changement sur DevBrain** — ni `devbrain.brain.yml` ni
   `histobrain.brain.yml` ne l'écrivent, parce qu'aucun des deux n'a
   d'obligation conditionnelle. Le défaut suffit à les décrire.

**Ce que le jeu d'épreuve prouve.** Quatre pages, deux par sens :
`Herodote - Histoires` (vert) porte `langue_originale:` avec sa condition vraie ;
`Braudel - La Mediterranee` (rouge) la porte avec sa condition fausse ;
`Fonds Moscou` (vert) porte `cote:` quand la condition l'exige ;
`Fonds Moscou` (rouge) ne la porte pas.

**Ce qui reste ouvert, et n'est pas tranché ici :** le point §5.11 du cadrage
(les champs vestiges) reste ouvert, et la remontée 2 du lot 2 est close — la
recommandation est appliquée, telle qu'elle était écrite.

## 4.2 L'homonymie « domaine » — quatre choses, et une discipline

**Ce que le lot 2 renvoyait.** Trois choses s'appellent « domaine » : le dossier
de l'arbre, le champ `domaine:` de `role: rule`, et l'axe de rangement. Le
contrôle C7 protège le nom du **dossier** d'un axe transverse et pas le nom du
**champ**. « Nomme-les distinctement dans le moteur. »

**Ce qui est tranché.** Elles sont **quatre**, pas trois, et la quatrième est
celle que le lot 2 avait trouvée en second (`champs.domaines`, le champ de l'axe
transverse, qui est le **pluriel** du libellé de l'axe de rangement) :

| Ce que c'est | Où ça vit dans le manifeste | Nom dans le moteur |
|---|---|---|
| le **dossier** de l'arbre | `axes.rangement.prefixes[].dossier` | `Modele.dossier_de_prefixe` |
| le **champ** de l'axe de rangement | `axes.rangement.champ` | `Modele.champ_rangement` |
| le **mot** que la prose emploie | `libelles.axe_rangement.{s,p}` | `Modele.libelle_rangement` |
| le **champ** d'un axe transverse | `axes.transverses[].champ` | `Modele.champs_transverses` |
| le **champ libre d'une prescription** | `champs.domaine` | **aucun nom — c'est une `ligne` comme une autre** |

**La cinquième ligne est la décision, et les quatre premières n'en sont que la
conséquence.** Un nommage ne protège de rien : il suffit d'un `if champ ==
"domaine"` pour que la confusion revienne. Ce qui protège, c'est une
**discipline de résolution** :

> **Le moteur ne reconnaît JAMAIS un champ par son nom.** Il le reconnaît par sa
> `source:` (quel axe il lit), par sa `fonction:` (`identite`, `alias`,
> `resume_court`) ou par son `reciproque:`.

`champs.domaine` ne déclare aucune des trois. Pour le moteur, c'est donc un
`type: ligne` sans fonction — et c'est exactement ce que c'est. Le champ n'a pas
besoin d'être protégé : il n'est jamais vu. La discipline est vérifiable, et la
vérification est celle de la section 3.5 : aucun littéral `"domaine"` dans
`brainkit/`.

**Ce qui reste ouvert :** la recommandation du lot 2 d'étendre **C7** au nom du
**champ** d'un axe transverse — « c'est la même faute, à un champ près ».
Elle porte sur `schema/valider.py`, artefact du lot 1, et sur l'entretien
d'initialisation, qui est le lot 6 du kit. **Non traitée ici, et remontée
maintenue.**

## 4.3 `A1` / `A3` — ce ne sont pas des règles

**Ce que le lot 2 renvoyait.** Sept des 26 groupes de sa boîte 2 sont
structurellement permanents : les 5 valeurs d'axe déclarées qu'aucune page ne
porte (`A1` — les cinq `skill/*`) et les 2 sous-libellés déclarés sans dossier
(`A3` — `automation/no-code` et `storage/objet`, bloqués par le plafond).
*« Un outil qui répète sept avertissements permanents à chaque exécution finit
ignoré. »* La recommandation : les sortir dans une section « backlog ».

**Ce qui est tranché : ce ne sont pas des règles, et elles n'entrent pas dans le
validateur.** Trois raisons, et la première suffit :

1. **Elles n'y ont jamais été.** `A1` et `A3` sont des contrôles
   d'`outils/fidelite.py` — des confrontations *manifeste ↔ vault*, pas des
   validations de vault. Ni `check_brain` ni `check_arbo` ne les portent. Les
   ajouter serait une **règle nouvelle**, ce que le lot interdit explicitement.
2. **Elles casseraient le critère d'acceptation** : sept avertissements de plus,
   soit 118 au lieu de 111. Un écart d'une seule violation est un échec.
3. **Leur objet n'est pas un verdict.** `A3` signale un état **voulu** — le
   manifeste garde le libellé d'une valeur plafonnée pour que *« la promotion
   reprenne d'elle-même le jour où le domaine gagne une seconde population »*.
   Une règle qui signale ce qu'on a décidé n'est pas une règle, c'est un rappel.

**Où elles vont, précisément :**

- **`A1` et `A3` restent dans `outils/fidelite.py`**, boîte 2, avec leurs
  verdicts écrits. Le lot 2 les y a mis, elles y sont justes, et rien n'en sort.
- **La section « backlog » que le lot 2 recommande appartient au lot 8 du kit**,
  la passe de mesure. C'est elle qui compte les violations par règle et propose
  un durcissement ; c'est le seul outil du kit dont la sortie soit une **liste de
  travail** et non un verdict. La même distinction vaut pour
  `couverture_des_vues`, dont le motif dit *« créer une vue est une décision
  ÉDITORIALE, pas technique »* — la différence est que celle-là est une règle
  déclarée, en avertissement, avec son motif : elle reste dans le validateur.
- **L'arbitrage sur les cinq `skill/*` orphelines appartient à floSa**, et son
  exécution au **lot 9**, le premier autorisé à écrire dans DevBrain. Les trois
  issues sont écrites dans le rapport du lot 2, remontée 3.

**Ce que ce lot n'a pas fait, et pourquoi.** Déplacer `A1`/`A3` dans une section
« backlog » de la sortie de `fidelite.py` serait une modification d'un artefact
du lot 2, hors du périmètre de celui-ci. C'est la remontée 9.

---

# 5. Les deux mécanismes neufs, et ce que le jeu d'épreuve a révélé

## 5.1 Le mode `reciproque: inverse`

DevBrain n'a que des champs **symétriques** : `alternatives:` ↔ `alternatives:`,
`complements:` ↔ `complements:`. Le moteur de la v3 ne connaît donc qu'un mode,
et il le connaît sans le savoir — il compare le **même** champ des deux côtés.

Le mode inverse demande une **paire** : `A.prolonge` contient `B` si et seulement
si `B.prolonge_par` contient `A`. Deux conséquences, et la seconde est celle qui
compte :

- `dix.reciprocite` lit le mode dans `champs.<x>.reciproque.mode` et le champ
  opposé dans `.champ`. Un champ symétrique est le cas où l'opposé est lui-même :
  **le code du mode symétrique est le code du mode inverse**, avec `oppose ==
  champ`. Aucune branche en plus.
- `socle.paire_inverse_bien_declaree` refuse une paire **mal déclarée** — un
  `inverse` qui pointe vers un champ qui ne pointe pas en retour. Sans elle, on
  remplacerait un trou par un autre : le validateur chercherait `prolonge_par`
  sur les pages, et personne ne vérifierait que `prolonge_par` existe. Elle est
  vérifiable sur le **manifeste seul**, sans lire une page, et le scénario 4 du
  jeu d'épreuve le prouve en sortant le même constat sur les deux vaults.

## 5.2 L'axe de rangement non exclusif

Trois mécanismes déclarés, et une question que le lot a dû trancher.

**Le préfixe transversal l'emporte.** Une page qui porte
`prefixe_transversal` vit dans le dossier de ce préfixe, quelles que soient les
autres valeurs qu'elle porte. Sans cette priorité, la règle de majorité
accepterait n'importe lequel des dossiers traversés, et le préfixe ne servirait
à rien.

**La règle de majorité, et ce qu'une machine peut en vérifier.** Le manifeste
définit la majorité comme *« la valeur de l'axe est celle qui rassemble le plus
de la page »*. C'est une phrase **éditoriale** : aucune machine ne pèse ce qu'une
page « rassemble ». Le lot a donc tranché sur ce que le validateur vérifie :

> Le dossier d'une page doit se dériver d'une valeur qu'elle **porte vraiment**.
> La règle de majorité choisit **laquelle** ; le validateur refuse un dossier qui
> ne correspond à **aucune**, et laisse le choix à l'auteur.

C'est la moitié mécanisable, et c'est celle qui attrape la faute réelle — une
page rangée là où rien ne la met. Quand la page ne porte qu'une valeur, la règle
dégénère exactement en celle de DevBrain : un chemin, une valeur.

**Le poids du seuil.** Une page à trois valeurs ne doit pas gonfler trois
sous-valeurs : elle compte **une fois**, pour sa valeur dominante. La résolution
de la dominante ne dépend PAS du seuil — sinon le calcul du seuil, qui en a
besoin, tournerait en rond : préfixe transversal d'abord, puis la valeur dont le
dossier de **préfixe** est celui où la page vit, puis la première déclarée. Sur
un axe exclusif, les quatre branches se réduisent à la première.

**L'axe absent.** Une page peut ne porter aucune valeur. Trois cas, trois
traitements distincts, et aucun n'est le silence :

| Cas | Ce que le moteur fait |
|---|---|
| le rôle ne porte pas l'axe (`porte_categorie: false`) | écarté de la dérivation, sans compter — un hub ne se range pas, il *est* le rangement |
| le rôle porte l'axe, le champ est vide, l'axe **n'est pas requis** | écarté de la dérivation, **compté**, et le compte est imprimé en note |
| le rôle porte l'axe, le champ est vide, l'axe **est requis** | `gabarit_par_role` échoue. Ce n'est pas la règle de chemin qui change d'avis : c'est le **gabarit** qui décide |

## 5.3 Ce que le jeu d'épreuve a révélé

Le jeu d'épreuve est `tests/` : un manifeste de 24 pages cibles, deux vaults
**jumeaux** de 13 et 14 pages, et six scénarios. Deux vaults, parce qu'un seul
vault fautif prouverait qu'une règle **crie**, jamais qu'elle se **taise** quand
il faut. Le vault vert est à zéro violation **et** zéro avertissement ; le rouge
porte sept défauts, un par mécanisme, et **rien d'autre** — ses hubs, son
atteignabilité, ses étiquettes fermées, sa couverture de sections et sa
réinjection de résumé sont corrects, pour que le verdict ne mesure que ce qu'il
prétend mesurer.

Quatre révélations, et deux sont des défauts que rien d'autre n'aurait trouvés.

**1. `LIEN_RE` accepte un saut de ligne à l'intérieur d'un wikilink.** Découvert
en le déclenchant : une phrase de prose du vault rouge citait
`` [[Tacite - `` en fin de ligne et `` Annales]] `` au début de la suivante, et
le moteur a rendu un **lien mort** — un huitième constat, non attendu. Le
comportement est celui de `check_brain`, reproduit à l'identique, et DevBrain
n'en contient aucun cas. Mais un lien coupé par un formatage automatique
deviendrait un lien mort sans que personne comprenne pourquoi. **Remontée 5.**

**2. L'unicité de nom de fichier ne se compte pas sur tous les fichiers.**
Première exécution : **47 violations dures**. Une vue embarquée porte le **même
nom** que la page qui l'embarque — c'est la déclaration du manifeste
(`vue_embarquee.embed: "![[<même nom>.base]]"`), et c'est l'extension qui les
distingue. La règle se compte donc **par extension**, et la nuance n'était
écrite nulle part : `regles_de_socle[unicite_du_nom_de_fichier]` dit « unique
dans le vault, à la casse près », ce qui, pris au mot, fait de la convention une
violation quarante-sept fois. C'est une règle que l'ancien code
**n'implémentait pas** : personne ne l'avait jamais exécutée.

**3. Un vocabulaire `genere: true` ne se relit pas.** Seconde exécution : une
violation dure, `vocabulaire fermé taxonomie illisible`. Le manifeste déclare
`vocabulaires.taxonomie.{mode: ferme, genere: true}` — le fichier est un
**dérivé** du manifeste, et le relire comme une source recréerait exactement le
défaut que le manifeste existe pour supprimer. Le moteur ne le lit donc plus, et
c'est `genere: true` qui le lui dit.

**4. Le vault vert est passé du premier coup, et c'est le résultat le plus
utile.** Treize pages écrites à la main contre un manifeste écrit pour un autre
sujet, **vingt** règles branchées et lancées, zéro violation et zéro
avertissement à la première exécution. Ce que ça mesure n'est pas la chance : c'est que les règles
sont **écrites en fonctions du manifeste** et non en fonctions du DevBrain. Un
moteur qui aurait gardé une seule valeur du dev en dur aurait échoué ici, sur un
vault dont pas un mot n'est du dev.

---

# 6. Comment rejouer

```bash
uv run brainkit/valider/__main__.py                    # DevBrain, chemins par défaut
uv run brainkit/valider/__main__.py --regle voisinage_declare
uv run brainkit/valider/__main__.py --tout             # avec les notes
uv run brainkit/valider/__main__.py --manifeste tests/epreuve.brain.yml --vault tests/vert
uv run --with jsonschema tests/epreuve.py              # les six scénarios
```

Le validateur sort **1** si une règle `dure` est violée, **0** sinon. Une règle
en `avertissement` signale ; une règle en `a_mesurer` compte, sans juger — c'est
la sévérité par défaut de toute instance neuve, et `histobrain.brain.yml` sort
ses dix règles ainsi.

**DevBrain n'est ouvert qu'en lecture.** Le paquet n'a aucun chemin d'écriture :

```bash
grep -rnE 'write_text|write_bytes|mkdir|unlink|rmtree|rename' brainkit/
# → une seule ligne : la phrase ci-dessus, dans la docstring de __main__.py
```

Vérifié après l'exécution sur les **26** points de travail du dépôt DevBrain — le
principal plus ses 25 worktrees : `git status --porcelain` vide partout.

---

# 7. Remontées

Dix points. Aucun n'est corrigé — sauf les **trois corrections du manifeste**
que le moteur a exigées, signalées comme telles au point 0 ci-dessous.

## 0. Les trois corrections du manifeste, et pourquoi elles n'étaient pas évitables

Commit séparé et explicite : `lot 3 : les trois corrections du manifeste que le
moteur a exigées`. Aucune n'a été faite « pour faire passer le critère » : deux
d'entre elles ne changent **aucun** compte sur DevBrain.

| # | Ce qui est corrigé | Pourquoi c'est le manifeste qui avait tort |
|---|---|---|
| 1 | `regles[anti_repetition].active` : `false` → `true` | `check_brain.py` émet `R26` sur les 337 briques à **chaque** exécution. Le lot 1 avait transcrit la **recommandation** du cadrage (« ne pas la livrer ») à la place de l'**état** du vault. Un manifeste qui prétend redire DevBrain ne le conseille pas. C'est la seule des trois qui touche le critère : sans elle, le moteur perdait 4 avertissements. La recommandation reste écrite dans le `motif:` et **appliquée** dans `histobrain.brain.yml`, qui sort la règle `active: false` — c'est là que cette décision appartient, dans un brain neuf et non dans la description d'un brain existant. |
| 2 | cinq champs supprimés entrent dans `champs:` avec `deprecated: true` | `regles_de_socle[champs_supprimes]` branchait une règle **dure** dont le manifeste ne portait **aucun** paramètre : la liste des champs morts vivait dans `check_brain.CHAMPS_MORTS`, donc dans le code. La règle serait née **morte**. La conjonction qui la branche est `deprecated: true` **plus** « autorisé par aucun rôle » : c'est elle qui sépare un champ **supprimé** d'un vestige **toléré** (`roles[].champs.deprecies`, où vivent `os:` et `domaines:`). Zéro violation sur DevBrain — la correction ne change aucun compte. |
| 3 | deux règles de socle manquantes sont déclarées : `couverture_de_section` (R11/R22) et `lien_vers_une_page_a_comprendre` (R15) | Toutes deux sont **dures** dans `check_brain` depuis le lot 8, toutes deux à zéro violation, et le lot 1 les a oubliées en transcrivant *« les règles hors des dix que le validateur porte »* (12 déclarées, 14 portées). Deux règles à zéro disparaissent sans bruit : c'est exactement ce que *« une règle absente ressemble à une règle satisfaite »* décrit. Zéro violation — la correction ne change aucun compte. |

Le schéma gagne par ailleurs **un** champ facultatif,
`roles[].champs.conditionnels[].sens` — c'est l'arbitrage 1, et il est justifié
en §4.1.

## 1. `anti_repetition` : le vault dit 4, le lot 8 disait 11

L'énoncé du lot demandait de vérifier « 11-dont-2 » contre le vault. Mesure du
2026-09-07 : **4 candidats**, tous sur `licence_type: open-source`, et **zéro**
sur `maturite:` — `Vanna`, `Ragas`, `TruLens`, `PuLP`.

La mesure du lot 8 n'est pas fausse, elle est **datée** : sept candidats ont
disparu depuis, par réécriture des sections `## Définition`. Deux des quatre
restants sont précisément ceux que le lot 8 comptait parmi ses « 2 vrais »
(`Ragas`) et ses faux positifs (`PuLP` — *« GLPK, HiGHS et SCIP côté open
source »* parle des solveurs, pas de la licence).

**Non corrigé** : la `mesure:` du manifeste est un objet **daté**, et réécrire
une mesure datée effacerait ce qu'elle mesurait. Une annotation
`note_mesure_2026_09_07` porte le nouveau compte à côté, ce que la propriété 2 du
manifeste autorise exactement. Ce que le fait apprend, et qui vaut au-delà du
chiffre : **une règle non scriptable en avertissement se vide toute seule quand
on relit les pages** — et c'est un argument de plus pour ne pas la durcir.

## 2. `regles_de_socle[vocabulaire_ferme]` mélange trois codes de trois sévérités

Elle déclare `severite: dure` et `code: [R4, R14, R14b]`. `R4` et `R14` sont
dures ; `R14b` est un **avertissement**. La sévérité de `R14b` ne vit pas dans la
règle : elle vit dans `axes.nature.vide_autorise`, et le moteur la lit là (cf.
§2.2). La liste de codes reste trompeuse pour un lecteur humain.

**Non corrigé** : le moteur lit la bonne source, la correction serait cosmétique,
et découper une règle de socle en trois demanderait de décider trois énoncés que
personne n'a écrits. À traiter si le lot 8 réécrit les sévérités.

## 3. Une règle de socle ne peut pas porter de PARAMÈTRE, une des dix peut

`$defs.regleDeSocle` est fermé par `unevaluatedProperties: false` et n'accepte
que `id`, `severite`, `enonce`, `code`, `depuis`, `mesure` plus les annotations.
`$defs.regles`, lui, accepte `champ`, `champs`, `sections`, `colonne`,
`marqueur`, `condition`, `champ_resume`, `motifs_bornes`… — quinze paramètres.

L'asymétrie n'est probablement pas voulue : la liste des dix est fermée par le
kit **et** paramétrable, celle du socle est ouverte **et** non paramétrable.
C'est elle qui a forcé la correction 2 à passer par `champs.<x>.deprecated`
plutôt que par un `champs:` sur la règle. La solution retenue est meilleure
(elle dit *pourquoi* un champ est mort, pas seulement qu'il l'est), mais elle a
été trouvée sous contrainte.

**Non corrigé** — toucher au schéma pour un besoin qu'une seule règle a eu, et
qui a trouvé une autre place, serait exactement ce que le lot 2 a refusé. À
rouvrir si une deuxième règle de socle a besoin d'un paramètre.

## 4. Un axe non exclusif dont le champ est typé `enum`

`histobrain.brain.yml` déclare `axes.rangement.exclusif: false` **et**
`champs.categorie.type: enum`. Un champ qui porte légitimement une **liste** est
donc typé comme un scalaire. `tests/epreuve.brain.yml` reproduit le même choix,
pour rester fidèle au remplissage qu'il transpose.

Le moteur tolère les deux formes — `vault.valeurs()` lit un scalaire comme une
liste d'un élément — et ne signale rien, parce que `check_brain` ne le signale
pas non plus (il ne contrôle la forme que pour `liste_enum`). Deux issues
possibles : ou le champ de l'axe de rangement devient `liste_enum` dès que
`exclusif: false`, ou le contrat écrit une phrase disant que la forme de ce champ
suit `exclusif` et n'est pas dans son `type`. **Non tranché** : c'est une
décision de contrat, donc du lot 1 ou d'une révision du schéma, pas du
validateur.

## 5. `LIEN_RE` accepte un saut de ligne à l'intérieur d'un wikilink

`\[\[([^\]|]+)(?:\|[^\]]+)?\]\]` : la classe `[^\]|]` accepte `\n`. Un wikilink
coupé en fin de ligne — par un formatage automatique, par une relecture, par un
éditeur qui replie à 80 colonnes — est donc lu comme **un lien, et un lien
mort**. DevBrain n'en contient aucun cas ; le jeu d'épreuve en a produit un sans
le vouloir, et c'est comme ça qu'on l'a su.

**Reproduit à l'identique et non corrigé** : corriger l'expression est une
amélioration de règle, ce que le lot interdit. Le correctif tient en un
caractère (`[^\]|\n]+`) et coûte zéro violation aujourd'hui. À faire par le lot
qui a le droit de changer un compte.

## 6. Rien dans le manifeste ne déclare la PORTE D'ENTRÉE du vault

`page_atteignable` (R7) a besoin des `.md` de la **racine** : mesure faite en
retirant la racine des pages d'aiguillage, **4 pages deviennent orphelines** —
`Automatisation no-code/Automatisation no-code.md`,
`Comparatifs/Comparatifs.md`, `Métiers/AI Engineering.md`,
`Métiers/Infrastructure & Ops.md`. Ce sont les hubs de premier niveau, qui n'ont
aucun parent pour les citer.

`check_brain` nommait `Home.md` en dur. Le moteur lit **tout** `.md` de la
racine, ce qui est une lecture générique (la racine n'est pas un dossier de
pages, donc elle est hors du périmètre par construction) mais **non déclarée** :
si un brain posait un brouillon à la racine, il élargirait silencieusement
l'atteignabilité. Le manifeste devrait pouvoir nommer sa porte d'entrée — un
champ à côté de `genere.chemins`, ou dans `frontieres_d_ecriture`, où `Inbox.md`
est déjà nommé. **À traiter au lot 4 ou 5**, avec le générateur sous les yeux :
c'est lui qui écrit `Home.md`.

## 7. Le périmètre de `champs_supprimes` s'appuie sur `agent.racine`, qui n'est pas fait pour ça

`R25` doit balayer ce qui est **hors** de l'arbre des pages, mais **pas** `AI/` —
les journaux de lot **citent** les champs morts pour raconter leur suppression.
`check_brain` codait le périmètre en dur (racine + `Documentation/` +
`Templates/`). Le moteur le dérive : `genere.non_pages`, moins les dossiers
cachés, moins `agent.racine`.

Deux effets. Le périmètre s'**élargit** à `Projects/` et `docs/` — mesure : zéro
violation de plus, la correction est neutre. Et l'exclusion d'`AI/` repose sur
`agent.racine`, un champ dont l'objet est de déclarer l'espace de l'agent, pas de
soustraire un dossier d'une règle. Ça marche, et c'est fragile : un manifeste
sans bloc `agent:` verrait ses journaux de lot échouer sur R25.

**Non corrigé** — la dérivation est celle qui existe, et la mesure dit qu'elle
est juste sur DevBrain. À reconsidérer si le lot 8 traite les périmètres.

## 8. Le recensement par domaine de `check_arbo` n'est pas porté

`check_arbo` imprimait, avant son verdict, « 681 page(s) migrée(s) dans 20
domaine(s) » puis une ligne par domaine avec son compte. Ce n'est pas une règle :
c'est une **mesure**, et elle ne rend aucun verdict. Le moteur ne la porte pas —
il annonce le nombre de pages contrôlées, et c'est tout.

C'est délibéré et c'est une perte : la sortie de `check_arbo` était le seul
endroit du vault où l'on voyait la forme de l'arbre d'un coup d'œil. Elle
appartient à la **passe de mesure**, qui est le lot 8 du kit, et c'est là qu'il
faut la remettre — avec les comptes de promotion, qui sont déjà calculés par
`chemins.promotions()`.

## 9. Déplacer `A1`/`A3` dans une section « backlog » de `fidelite.py` n'est pas fait

C'est la conséquence de l'arbitrage 3 (§4.3) : les deux contrôles restent dans
`outils/fidelite.py`, où le lot 2 les a mis, et la recommandation du lot 2 était
de les **sortir des écarts** dans une section séparée. Cette recommandation porte
sur un artefact du lot 2, hors du périmètre de ce lot-ci, et un lot qui découvre
un travail hors de son périmètre l'écrit ici plutôt que de le faire.

**À faire par le lot 8**, qui écrit la passe de mesure et qui aura, à ce
moment-là, la bonne place pour un backlog.

## 10. `code:` mélange deux choses : un identifiant de règle et un outil porteur

`regles[].code` et `regles_de_socle[].code` portent tantôt un code de règle de
l'ancien validateur (`R21`, `R8e`), tantôt un **script** (`check_arbo`), tantôt
une **commande** (`build_bandeau --check`). Les deux premiers sont de la
provenance ; le troisième est une **délégation**, et le moteur doit le lire comme
tel pour dire « déléguée — portée par `build_bandeau --check` ».

Aujourd'hui il le fait par convention, pas par déclaration. Un `porte_par:`
distinct de `code:` rendrait la délégation explicite, ce dont le lot 4 aura
besoin : c'est lui qui écrira le générateur qui porte `bandeau_a_jour`.
**À trancher au lot 4.**

---

# 8. Ce qui reste au lot 4

- Le générateur porte `bandeau_a_jour`, la seule des dix que ce lot délègue. Son
  `--check` est la règle : régénérer et comparer les octets.
- La forme de la zone AUTO d'un hub — trois formes, un seul gabarit déclaré — est
  la remontée 1 du lot 2, et elle reste entière : le validateur ne contrôle
  aucune zone AUTO, il ne fait que vérifier que les pages y **figurent**
  (`completude_du_hub`).
- La remontée 5 du lot 1 — le hub liste ses comparatifs depuis les fichiers de
  vue et non depuis `role:` — est **latente** et le reste : `couverture_des_vues`
  n'observe pas la source d'une liste, seulement son résultat. Le contrôle qui la
  réveillera est `A17` de `outils/fidelite.py`, pas une règle du validateur.
- La porte d'entrée du vault (remontée 6) et la séparation `code:` / `porte_par:`
  (remontée 10) se décident avec le générateur sous les yeux.
