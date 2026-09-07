# BrainKit — les générateurs, branchés sur le manifeste

> Conversation 45, « BrainKit lot 4, les générateurs », le 2026-09-07. Lot 4 du
> plan de `design/00-cadrage.md` §6. Périmètre : les quatre générateurs
> d'artefacts dérivés — index, hubs, liens, bandeau — réécrits en modules pilotés
> par `brain.yml`, plus le moteur de zone AUTO commun et son `--check`.
>
> **DevBrain n'a été ouvert qu'en lecture.** Les 414 artefacts régénérés ont été
> écrits dans un arbre de travail hors du vault. `git status --porcelain` est vide
> sur les 27 points de travail du dépôt DevBrain — le principal plus ses 26
> worktrees — et la vérification est en §7.

## Ce que le lot livre

| Livrable | Ce que c'est |
|---|---|
| `brainkit/generer/` | 11 modules, **950 lignes de code** (hors docstrings) |
| `pyproject.toml` + `brainkit/__main__.py` | le kit se lance proprement, et de trois façons |
| `tests/generation.brain.yml` + `tests/genere-vert/` + `tests/genere-rouge/` | deux vaults jumeaux, huit défauts |
| `tests/generation.py` | sept scénarios, 31 vérifications |
| `design/04-generation.md` | ce document |

Cinq arbitrages sont tranchés (§4), et deux remontées du lot 3 qui m'étaient
renvoyées sont closes : la séparation `code:` / `porte_par:` et la question des
trois formes de zone AUTO. La troisième — la porte d'entrée du vault — est
**rendue au lot 5**, avec son motif (§6).

---

# 1. Le critère d'acceptation, et comment il est tenu

## 1.1 La référence, capturée avant d'écrire une ligne

Le critère du lot est un `diff` **vide** contre les artefacts que DevBrain porte
aujourd'hui. La référence est donc le vault lui-même, à son commit `8aaa257`, et
elle n'a pas eu à être capturée : elle est versionnée. Un seul outil du DevBrain
a été lancé, et il n'écrit rien —
`uv run AI/scripts/build_bandeau.py --check` — pour disposer d'un compte de
comparaison sur la seule des quatre commandes qui possède un mode lecture seule.

```
765 page(s) balayée(s), 337 `role: brique`
39 bandeau(x) à cellule vide — champ absent du frontmatter
OK — tous les bandeaux concordent avec leur frontmatter.
```

## 1.2 Le rapport de diff, artefact par artefact

Régénération dans un arbre de travail hors du vault, puis comparaison
**octet pour octet** de chaque fichier posé contre son homologue :

```bash
uv run brainkit/generer/__main__.py --sortie /tmp/bk4-diff
# puis, pour chacun des 414 fichiers : cmp -s sortie/<rel> DevBrain/<rel>
```

| Artefact | Attendu par le lot | Posés | Identiques | En écart | Lignes de `diff` |
|---|---|---|---|---|---|
| `AI/index/brain-index.json` | 1 | 1 | 0 | **1** | **3** |
| `AI/index/brain-index.md` | 1 | 1 | 1 | 0 | 0 |
| `AI/index/liens.md` | 1 | 1 | 1 | 0 | 0 |
| zones AUTO des hubs — forme **arbre** | 67 | 67 | 67 | 0 | 0 |
| zone AUTO du hub de **ralliement** (`Comparatifs.md`) | 1 | 1 | 1 | 0 | 0 |
| zones AUTO des hubs **transverses** (`Métiers/`) | 6 | 6 | 6 | 0 | 0 |
| bandeaux | 337 | 337 | 337 | 0 | 0 |
| **Total** | **414** | **414** | **413** | **1** | **3** |

Les 74 hubs du critère se décomposent bien en **67 + 1 + 6**, et ces trois
comptes sont exactement ceux que le lot 2 avait mesurés pour ses trois formes.
Le générateur les rend séparément dans son rapport, ce qui n'était pas une
coquetterie : cf. §4.1 et le correctif 3 du §3.3.

**Refus : zéro sur 765 pages.** Aucun hub sans zone à balises, aucune page
portant un bandeau sans titre de niveau 1.

**Trous de bandeau : 39, nommés** — le même compte que l'ancien script, à la
page près. Une cellule vide est **signalée et jamais comblée** : elle dit qu'un
champ manque au frontmatter, et c'est une information.

## 1.3 Le seul écart : un dossier fantôme, et sa preuve

```diff
--- AI/index/brain-index.json (vault)
+++ AI/index/brain-index.json (régénéré)
@@ -28,2 +28 @@
-    "Web & API",
-    "obsidian_outer_backup_20260907"
+    "Web & API"
```

Le catalogue committé annonce, dans sa clé `scanned`, un dossier
`obsidian_outer_backup_20260907` **qui n'existe pas dans le vault**. Il a existé
sur le disque au moment où `build_index.py` a tourné pour la dernière fois — le
commit `8d1bfd1`, du 2026-09-07 — puis il a disparu. Il n'a jamais été suivi par
git.

**Fait du vault, pas défaut du générateur, et c'est prouvé** — pas argumenté.
Réinjecté en mémoire dans la liste des dossiers balayés, le catalogue redevient
identique à l'octet :

```
sans le dossier fantôme  : ÉCART
avec le dossier fantôme  : IDENTIQUE
```

C'est la vérification `et il tient à UN dossier fantôme : réinjecté, l'octet est
identique` du scénario 7 de `tests/generation.py`. **Il n'a pas été corrigé** :
`obsidian_outer_backup_20260907` n'a rien à faire dans un artefact versionné, et
la seule façon d'obtenir un `diff` vide serait de recréer le dossier — c'est-à-dire
d'écrire dans DevBrain. L'interdiction du lot passe avant le chiffre du lot.

Ce que le fait apprend, et qui vaut au-delà des trois lignes : **la clé `scanned`
publie le contenu non suivi de l'arbre de travail.** Un dossier de sauvegarde, un
`node_modules`, un dossier temporaire d'éditeur entre donc dans un artefact
versionné, et l'artefact cesse d'être reproductible. C'est la remontée 1.

## 1.4 Ce que la comparaison porte, et pourquoi les 413 sont quand même identiques à l'octet

`--check` compare le texte **logique** : lecture en fins de ligne universelles,
écriture en fins de ligne de la plateforme — exactement comme les quatre scripts
du DevBrain, et pour une raison mesurable. Le vault est stocké en LF et sorti au
format natif (`.gitattributes` : `* text=auto`, `core.autocrlf: true`), donc sous
Windows ses 765 fichiers sont **CRLF sur le disque**. Comparer les octets bruts
ferait apparaître 765 écarts de fin de ligne qui ne sont pas des écarts de
contenu, et masquerait les vrais.

Cela dit, le tableau du §1.2 est bien une comparaison d'**octets** (`cmp -s`), et
413 fichiers sur 414 y passent : la convention de fin de ligne rendue au disque
est celle du checkout, donc celle du vault. Le choix de comparer le texte logique
n'a rien relâché ici ; il protège une instance dont le checkout ne serait pas le
même que celui de la machine qui génère.

---

# 2. La correspondance, script par script

## 2.1 `build_index.py` → `brainkit/generer/index.py`

| Ce que l'ancien codait en dur | Où ça vit maintenant |
|---|---|
| `NON_PAGES` — 9 dossiers d'outillage | `genere.non_pages` |
| `FIELDS` — 12 champs indexés | `genere.index.champs` + `plus: [path]` |
| `OUT_JSON` / `OUT_MD` | `genere.index.fichiers`, reconnus par leur **extension** et non par leur rang |
| `"generated_by": "AI/scripts/build_index.py"` | `genere.index.signature` |
| `"scope": "v2-only (réservoir v1 exclu)"` | `genere.index.portee`, émise **seulement si déclarée** |
| `ROLE_LABEL` (5 titres) et `ROLE_ORDER` | `genere.index.groupes`, une liste **ordonnée** de `{role, titre}` |
| `"(sans catégorie)"` | `genere.prose["index.sans_valeur"]` |
| l'en-tête du document humain | `genere.prose["index.entete"]` |
| `descriptor()` — `pitch`, sinon `domaines`, sinon `alias` | résolu par `fonction: resume_court`, les axes transverses, puis `fonction: alias` |
| `p.get("tags")` pour l'index de mots-clés | le champ dont la `source:` commence par `vocabulaires.` |

Un rôle que `groupes` ne nomme pas n'est pas écarté : il sort **après** les
déclarés, sous son propre identifiant. C'est ce qui fait apparaître les 74 hubs
sous un `## hub` sans titre rédigé, dans le document humain du DevBrain. Fait du
vault, reproduit.

## 2.2 `build_mocs.py` → `brainkit/generer/hubs.py`

C'est la réécriture la plus profonde des quatre, parce que c'est le script le
plus intriqué et celui qui portait le plus de dette.

| Ce que l'ancien codait en dur | Où ça vit maintenant |
|---|---|
| `METIERS = VAULT / "Métiers"` | `axes.transverses[].dossier` |
| `HUBS_TRANSVERSES = {"Métiers"}` | dérivé de la même déclaration |
| `THEME_LABEL` — 6 libellés | `axes.transverses[].valeurs[].libelle` |
| **une seule** boucle transverse | une boucle **sur** `axes.transverses[]` — rupture 4 |
| `COMPARATIFS = VAULT / "Comparatifs"` | `roles[].hub_de_ralliement.dossier` |
| `ROLE_SECTION` — 4 couples `(role, titre)` | `roles[hub].corps[<AUTO>].sections[]`, avec `depuis: role` et `role:` |
| `"### Sous-domaines"` et son séparateur | la même liste, `depuis: sous_dossiers` + `separateur:` |
| `"### Comparatifs"` depuis `glob("*.base")` | la même liste, `depuis: vues` — **anomalie reproduite**, cf. remontée 2 |
| la phrase d'intro d'un hub transverse | `genere.prose["transverse.intro"]`, défaut du kit |
| `"*(dossier vide)*"` | `genere.prose["hubs.dossier_vide"]`, défaut du kit |
| `AUTO_RE` | `roles[hub].corps[<AUTO>].balises` |

Le groupement d'un hub transverse et d'un hub de ralliement — le **premier
segment du chemin, jamais le sous-dossier** — est déclaré par
`groupe_par: premier_segment_du_chemin`, vocabulaire fermé par le kit. Sans ce
choix, ces hubs redoubleraient l'arbre au lieu de le traverser, et la vingtaine
de groupes de `Comparatifs.md` deviendrait une cinquantaine.

## 2.3 `build_links.py` → `brainkit/generer/liens.py`

| Ce que l'ancien codait en dur | Où ça vit maintenant |
|---|---|
| `NON_PAGES` | `genere.non_pages` |
| `OUT` | `genere.liens.fichier` |
| `"Généré par AI/scripts/build_links.py"` | `genere.liens.signature` |
| `p["role"] == "notion"` pour la couverture d'un mot-clé | les rôles de `fonction: notion` |
| `"pas de page concept dédiée"` | `genere.prose["liens.sans_page"]` |
| les 9 titres et étiquettes de section | 9 gabarits par défaut du kit, surchargeables |
| `("*.md", "*.base")` pour les cibles résolvables | `.md` plus `roles[].vue_embarquee.extension` |

La normalisation qui rapproche un mot-clé (`series-temporelles`) du nom d'une
page (« Séries temporelles ») est restée : sans diacritique, en minuscules,
espaces et soulignés en tirets.

## 2.4 `build_bandeau.py` → `brainkit/generer/bandeau.py`

C'est la brique dont la séparation était déjà nette dans l'inventaire du
cadrage — I4 « le moteur », générique ; I5 « le contenu », à réécrire — et le
lot le confirme : **le moteur ne connaît aucune des quatre colonnes du DevBrain.**

| Ce que l'ancien codait en dur | Où ça vit maintenant |
|---|---|
| `COLONNES` — 4 titres | `bandeau.colonnes[].titre` |
| `NATURE`, `LICENCE`, `EXECUTION_FAMILLE` | `bandeau.colonnes[].table` |
| `HEBERGEES`, `HOSTED`, `SCALING` | `bandeau.colonnes[].depend_de` |
| l'exception « pas de langage pour un `saas` » | `exception_qualification: {si: "famille == saas"}` |
| le repli « une application de bureau porte `os:` » | `depend_de.repli: {si, source}` |
| `VIDE = "—"` | `bandeau.vide` |
| `START` / `END` | `bandeau.balises` |
| `fm.get("role") != "brique"` | `bandeau.porte_par` |
| le rendu du résumé en citation | `bandeau.porte_le_resume` |

Les deux conditions déclarées en français — `famille == saas` et
`famille == application et os renseigné` — sont lues par
`brainkit/valider/conditions.py`, écrit au lot 3, **sans une ligne d'ajout**.
C'est la seule brique du lot qui n'a rien coûté, et ce n'est pas un hasard : le
lot 3 avait fermé les trois formes de condition qu'un manifeste peut écrire, et
refusé d'en deviner une quatrième.

Une colonne sait faire cinq choses, et aucune ne nomme un sujet : lire une
**source**, rendre une valeur par une **table**, accoler un **second champ**,
écarter cette qualification sur une **condition déclarée**, et déléguer à **deux
autres champs** quand la source ne suffit pas. Une valeur de source absente de la
table rend le caractère vide — elle n'est pas absorbée en silence.

## 2.5 Ce qui n'existait pas, et qu'il a fallu écrire

| Module | Ce qu'il porte | Pourquoi il n'existait pas |
|---|---|---|
| `zone.py` (27 l.) | LE moteur de zone AUTO : trouver, remplacer en bloc, insérer sous le titre, signaler l'impossible | il était **dupliqué** entre `build_mocs` (deux variantes) et `build_bandeau` |
| `sortie.py` (115 l.) | le **seul** plan d'écriture du kit, ses trois modes, l'idempotence, le rapport chiffré | chaque script écrivait pour son compte, et deux n'avaient aucun mode lecture seule |
| `corpus.py` (94 l.) | un balayage du vault pour les quatre | il y en avait **quatre**, dont un qui relisait le JSON produit par un autre |
| `prose.py` (69 l.) | les 24 gabarits de phrase des documents générés, langue `fr`, surchargeables | la prose était en dur, avec les mots du dev dedans |
| `orchestre.py` (92 l.) | l'ordre, le point fixe, le rapport, la séparation refus / écart | c'était un ordre à retenir dans un runbook |

---

# 3. Ce qui a été JETÉ

## 3.1 La dette que §5.10 du cadrage nommait

Le cadrage annonçait trois dettes mortes dans ces scripts. Les trois sont
tombées, et la mesure dit ce que ça coûte : **rien**.

| Jeté | Où | Ce que ça valait |
|---|---|---|
| `V1_MARKERS` (13 champs) + `is_active_v2()` | `build_index.py` | le filtre rendait `True` pour **toute** page depuis la disparition de `Wiki/` au lot 4 de la migration ; le compte qu'il alimentait sort à **0** |
| `V1` (13 champs) + `active()` | `build_links.py` | idem, même dossier, même compte |
| `MOC_CONCEPT`, `CONCEPT_LABEL` (12 libellés), `WIKI_LABEL` (2), `wiki_group()` | `build_mocs.py` | l'étage `MOC/Concepts/` ; le dossier `MOC/` n'existe plus |
| le paramètre `scope` d'`upsert()` et sa branche `indexe:` | `build_mocs.py` | un champ hors du gabarit `role: hub`, qui ne survivait que sous `MOC/` |
| les deux boucles `MOC/Categories/` et `MOC/Types/` | `build_mocs.py` | déjà retirées à la clôture du lot 3 du DevBrain ; leurs commentaires restaient |
| la détection `nl = "\r\n" if "\r\n" in txt else "\n"` | `build_mocs.py` | elle ne pouvait **jamais** rendre `\r\n` : le texte comparé est lu en fins de ligne universelles |

La seule trace qui subsiste de la dette v1 est une **déclaration**, pas du code :
`genere.index.portee` et le gabarit surchargé `index.entete` disent que le
catalogue et l'en-tête du DevBrain annoncent encore un « réservoir v1 (0 pages
Wiki) ». Le kit ne porte pas le mécanisme ; il porte le fait qu'un artefact du
DevBrain le mentionne. Un brain neuf ne déclare rien de tout ça.

## 3.2 Le chaînage par fichier

`build_mocs.py` refusait de tourner sans le JSON produit par `build_index.py` :

```python
if not INDEX.exists():
    raise SystemExit("Index absent — lancer d'abord : uv run AI/scripts/build_index.py")
```

Il lisait donc un vault **vieux d'une exécution**. Le chaînage disparaît : les
quatre se composent du même corpus, lu une fois. Et il est remplacé par quelque
chose de plus fort — le point fixe du §4.5 — parce que le chaînage ne réparait
que la moitié du problème.

## 3.3 Ce que le jeu d'épreuve a fait jeter, et qui n'était pas de la dette

Trois correctifs qui ne se lisaient pas dans le code, et que seul le vault rouge
a sortis :

1. **Le point fixe s'interrompait sur un refus.** Une page sans zone AUTO est une
   condition **stable** du vault, identique à chaque passe. S'arrêter dessus
   laissait les artefacts dérivés composés depuis le corpus d'**avant** la
   réparation : `--ecrire` rendait un vault encore périmé, et un `--check` lancé
   juste après échouait. Mesure : le vault rouge réparé demandait deux exécutions.
2. **Une entrée de corpus n'est pas une ligne d'index.** Elle porte son chemin
   puis tout le frontmatter ; c'est le générateur d'index qui **projette** les
   colonnes publiées. `genere.index` décide de ce qui sort dans le catalogue, pas
   de ce que les générateurs ont le droit de lire — un manifeste sans bloc
   `index` laissait sinon les hubs sans un nom à citer, et plantait.
3. **Une pose porte la forme de sa zone.** Sans elle, un rapport ne dit pas
   laquelle des trois formes s'écarte, et un test ne peut pas vérifier qu'une
   forme a **cessé** d'être posée — ce que la boucle sur les axes transverses
   exige de savoir.

## 3.4 Ce qui n'a PAS été jeté, contre l'apparence

- **La sous-section `### Comparatifs` lit une extension de fichier**, là où les
  quatre autres lisent un `role:`. C'est une anomalie, elle est connue depuis le
  lot 1, mesurée latente par le lot 2, et elle est **reproduite**. La corriger
  coûterait le `diff` vide, et « ne corrige aucun artefact qui te paraîtrait mal
  formé » est l'interdiction du lot. Remontée 2.
- **Deux comptes de remplacement différents** : le générateur de hubs remplace
  **toutes** les occurrences d'une zone, celui du bandeau la **première**. Aucune
  page du vault n'en porte deux, donc la différence ne s'observe pas — elle est
  gardée telle quelle, parce que le critère du lot est le `diff` vide et non la
  ressemblance du code.
- **La forme de la zone transverse ne se `rstrip` pas** et porte sa phrase
  d'intro suivie d'une ligne vide, là où les deux autres formes se `rstrip`ent.
  C'est la forme du vault. Reproduite.
- **Le tri d'un groupe se fait sur le nom en minuscules**, ce qui place
  « Comparatif - Évaluation LLM » **après** « Comparatif - Observabilité LLM »
  (`é` > `o` en points de code). Un tri par locale changerait 47 lignes.

## 3.5 Le bilan en lignes, sans embellissement

| | Lignes de code | Fichiers |
|---|---|---|
| Les 4 scripts du DevBrain | **663** | 4 |
| `brainkit/generer/` + le dispatcheur | **950** | 12 |

**Le nouveau code est 43 % plus long, et il faut le dire.** Il ne fait pas la
même chose : il porte trois modes d'écriture au lieu d'un, un rapport chiffré par
artefact et par forme, un point fixe d'orchestration, une couche de prose
surchargeable, une ligne de commande à sous-commandes, et il est piloté par un
manifeste au lieu de vingt tables en dur. Ce qui a **diminué**, ce sont les
valeurs : zéro préfixe, zéro rôle, zéro colonne, zéro libellé du dev dans les 950
lignes.

---

# 4. Les cinq arbitrages

## 4.1 Les trois formes de zone AUTO — la forme se dérive du PÉRIMÈTRE

**La question**, posée par le lot 2 et bloquante pour ce lot : *un rôle porte-t-il
plusieurs gabarits de zone AUTO, ou la forme se dérive-t-elle du périmètre ?*

**Tranché : elle se dérive du périmètre, et le périmètre se lit sur le DOSSIER du
hub.** Un rôle ne porte donc qu'**un** gabarit de zone AUTO.

| forme | périmètre | comment le générateur la reconnaît | DevBrain |
|---|---|---|---|
| arbre | `dossier` | le cas général | 67 |
| transverse | `champ` | le dossier de tête est un `axes.transverses[].dossier` | 6 |
| ralliement | `role` | le dossier de tête est un `roles[].hub_de_ralliement.dossier` | 1 |

Trois raisons, et la troisième est la vraie :

1. **La forme n'est pas une propriété du rôle.** Les 74 pages portent le même
   `role: hub`. Un rôle qui déclarerait trois gabarits obligerait chaque page à
   dire lequel s'applique — donc à stocker dans le frontmatter ce que le chemin
   dit déjà. C'est exactement ce que la v3 du DevBrain a supprimé en tuant
   `galaxie:`.
2. **Rien de neuf n'est déclaré.** `axes.transverses[].dossier` et
   `roles[].hub_de_ralliement.dossier` existaient **avant** ce lot, parce qu'un
   dossier appartient à l'axe ou au rôle qui le peuple, pas au hub qui l'habite.
   La forme se déduit de déclarations déjà là, et posées pour une autre raison
   qu'elle.
3. **Trois gabarits sur le rôle, ce serait la même information à deux endroits** —
   le défaut exact que le manifeste existe pour supprimer. Constat E4 du cadrage :
   les cinq gabarits de `Templates/` ont pris du retard sur les 337 pages qu'ils
   décrivaient, parce que deux sources décrivaient le même gabarit.

Ce qui **est** déclaré, en revanche, c'est le gabarit unique de la forme arbre :
ses sous-sections, dans l'ordre, chacune avec son périmètre. `depuis:` est la
lecture machine de ce que `source:` disait en prose, et son vocabulaire est fermé
par le kit — `sous_dossiers`, `role`, `vues` — parce qu'un périmètre est du code,
pas une donnée. Les deux autres formes n'ont pas de sous-sections à déclarer :
l'une groupe par valeur d'axe, l'autre par segment de chemin, et les deux tirent
leurs sous-titres du vault.

**Ce que le choix coûte, et il faut le nommer :** si l'axe transverse est retiré
du manifeste, les pages qui vivaient sous son dossier **retombent dans la forme
arbre** — elles restent des hubs d'un dossier, et le générateur les traite comme
tels. Ce n'est pas un défaut, c'est la conséquence directe de « la forme se lit
sur le dossier », et le scénario 3 du jeu d'épreuve l'assert explicitement. Un
manifeste qui retire un axe transverse doit donc aussi décider du sort de son
dossier — et c'est un travail de `re-seuiller`, au lot 5.

## 4.2 `code:` et `porte_par:` — la délégation se déclare, elle ne se devine plus

**La remontée 10 du lot 3**, tranchée avec le générateur sous les yeux comme elle
le demandait.

`code:` portait trois choses : un identifiant de règle de l'ancien validateur
(`R21`, `R8e`), un nom de script (`check_arbo`), et une **commande**
(`build_bandeau --check`). Les deux premières sont de la **provenance** — d'où la
règle vient. La troisième est une **délégation** — qui la tient aujourd'hui. Le
moteur devait deviner par convention laquelle des trois il lisait, et annoncer la
délégation sur cette devinette.

**Tranché : `code:` ne porte plus que la provenance ; `porte_par:` nomme l'outil
qui TIENT la règle.** Sur DevBrain, une seule des vingt-deux règles en porte un —
`bandeau_a_jour` — et son message passe de *« portée par `build_bandeau --check` »*
à *« portée par `brainkit generer --quoi bandeau --check` »*, qui est vrai. Les
deux `code: [check_arbo]` restent de la pure provenance : le moteur tient ces
règles lui-même depuis le lot 3.

Un repli sur `code:` subsiste, pour un manifeste écrit avant l'arbitrage. Aucune
règle nouvelle, aucun changement de sévérité : le verdict sur DevBrain est
inchangé — **0 dure, 111 avertissements** — et le jeu d'épreuve du lot 3 passe en
entier.

## 4.3 Où vit la prose des documents générés

Trois des quatre artefacts sont des **documents** : ils portent des phrases
françaises. « Ne pas éditer à la main », « liens sortants », « Tags sans page
concept dédiée », « explorer par sous-domaine ». La question n'est pas de les
éviter, c'est de décider où elles vivent. Trois places, une seule tient :

1. **En dur dans le code** — ce que fait le DevBrain. Refusé : « concept » y est
   un libellé de sa v2, « sous-domaine » le libellé de l'axe du dev. Le lot
   interdit exactement ça.
2. **Entièrement dans le manifeste** — chaque phrase déclarée. Refusé aussi : un
   brain neuf devrait écrire vingt phrases françaises avant que son index se
   génère, et l'entretien du lot 6 devrait les demander. §3.5 point 7 du cadrage
   dit le contraire — ce que l'utilisateur ne peut pas connaître, on ne le lui
   demande pas.
3. **Un gabarit par défaut dans le kit, surchargeable par le manifeste.** Retenu.

Les 24 gabarits par défaut (`brainkit/generer/prose.py`) portent la **langue** —
`brain.langue: fr`, seule valeur légale en v1 — et des **trous nommés**, remplis
par le manifeste : `{brain}`, `{signature}`, `{pages}`, `{axe_rangement}`,
`{axe_transverse}`, `{notion}`, `{champ_role}`. Le mot « brique » n'apparaît pas
une fois dans le module, ni « domaine », ni « famille », ni un titre de section
du DevBrain.

DevBrain en surcharge **quatre**, et les quatre sont de la dette :

| clé surchargée | pourquoi |
|---|---|
| `index.entete` | annonce un « réservoir v1 (0 pages Wiki) » disparu, et dit « Document généré » là où la carte des liens dit « Généré » |
| `index.sans_valeur` | « (sans catégorie) » nomme le **champ** accentué, que la dérivation depuis `categorie` ne sait pas produire ; le défaut du kit rend « (sans domaine) » |
| `liens.sans_page` | « page **concept** » — le mot de la v2 pour ce que le vault appelle désormais une notion |
| `liens.tags_sans_page` | idem |

`tests/generation.brain.yml` n'en surcharge **aucune**, et c'est le cas qui passe :
les défauts du kit suffisent à un brain neuf.

## 4.4 Le mode par défaut, et le garde-fou mécanique

`--check` est le défaut, et le lot demandait qu'un générateur ne puisse pas écrire
sans qu'on le lui demande. Ce n'est pas tenu par une convention, c'est tenu par
l'architecture :

- **Un seul module du paquet écrit.** `grep -rnE 'write_text|write_bytes|mkdir'
  brainkit/generer/` ne rend que `sortie.py`, deux lignes.
- **Trois modes, et le défaut n'en écrit aucun.** `check` compare sans poser un
  octet ; `sortie` pose dans un arbre de travail séparé ; `ecrire` pose dans le
  vault, et seulement là où l'octet change.
- **Une sortie posée SOUS le vault est refusée** — ce serait écrire dans le vault
  par un autre nom.
- **`--ecrire` et `--sortie` s'excluent.**
- Codes de retour : **2** s'il reste un écart, **1** sur un refus, **0** si tout
  concorde. Le 2 est celui du `--check` du DevBrain : « il reste quelque chose à
  régénérer » n'est pas une erreur d'exécution.

Un corollaire : la promesse du lot 3 — « le paquet n'a aucun chemin d'écriture » —
est devenue fausse avec ce lot. Elle a été **restreinte** dans la docstring du
validateur, au périmètre `brainkit/valider/`, plutôt que laissée à pourrir.

## 4.5 Le point fixe de l'orchestration

Deux artefacts dépendent de ce que les autres écrivent, et le DevBrain ne le
voyait pas parce qu'il est déjà à son point fixe :

- **la zone AUTO d'un hub porte des wikilinks.** Les réécrire change les liens
  sortants du hub, donc la carte des liens — qui a été composée, dans la même
  passe, depuis le corpus lu **avant** ;
- **un hub transverse peut être créé.** La page n'existait pas quand le catalogue
  a compté les pages : il en annonce donc un de moins. Mesuré sur le vault
  d'épreuve : à la première génération, le catalogue disait 14 pages là où le
  vault en portait 18.

Le DevBrain contournait le premier cas à la main, dans sa procédure de clôture :
*« lancer `build_index.py` puis `build_mocs.py` / `build_links.py` »* — un ordre à
retenir, qui ne répare que la moitié et jamais le second cas.

**Tranché : en écriture, l'orchestration tourne jusqu'au point fixe.** Une passe
qui a écrit quelque chose invalide le corpus : on relit et on recommence, jusqu'à
ce qu'une passe n'écrive plus rien, avec un plafond de 4 passes et un refus
explicite si le point fixe n'est pas atteint. En `check` et en `sortie`, **une
seule passe** — et c'est voulu : le rapport doit dire ce que le vault **est**, pas
ce qu'il deviendrait après réparation.

Un **refus n'interrompt pas** le point fixe : une page sans zone ou sans titre est
une condition stable, et s'arrêter dessus laissait les artefacts dérivés
composés depuis un corpus périmé (§3.3 correctif 1).

---

# 5. La preuve de généricité, et ce que les cas HistoBrain ont révélé

`tests/generation.brain.yml` est de forme HistoBrain : l'unité est une **source**,
l'axe de rangement une **période**, le rôle-vue une **chronologie** avec son hub
de ralliement, la prescription une **méthode**, le bandeau porte
`Nature | Auteur et date`. **Aucune valeur en commun avec le DevBrain**, et le
même code.

Ce qu'il couvre, et pour chacun un cas qui passe et un cas qui échoue :

| Mécanisme | Cas qui PASSE | Cas qui ÉCHOUE |
|---|---|---|
| **deux** axes transverses | `Thèmes/` et `Espaces/`, 2 hubs chacun, tous conformes | un compte faux sur l'axe 1, une puce manquante sur l'axe 2 |
| **un seul** axe (mutation en mémoire) | les 2 hubs de l'axe 1 restent posés en forme transverse | les 2 de l'axe 2 cessent de l'être |
| **zéro** axe (mutation en mémoire) | aucune pose transverse, aucun dossier créé | — |
| forme **arbre** | les sous-sections déclarées, dans l'ordre déclaré | la sous-section des vues retirée de la zone |
| forme **ralliement** | groupée par le premier segment du chemin | groupée par le sous-dossier |
| forme **transverse** | intro puis une puce par groupe, sans sous-titres | un compte faux |
| bandeau | 3 bandeaux dérivés du frontmatter | une cellule qui n'en dérive plus |
| index | catalogue et document humain concordent | une entrée retirée du document |
| hub sans zone AUTO | — | **REFUS**, jamais un écart |
| page sans titre de niveau 1 | — | **REFUS**, jamais un écart |
| artefact non déclaré | — | **REFUS**, jamais un chemin inventé |
| réparation + idempotence | le rouge réparé devient identique au vert ; relance : 0 octet | — |

Les trois comptes d'axes transverses — **0, 1, 2** — sont couverts par les trois
manifestes ensemble : `epreuve.brain.yml` (0), `devbrain.brain.yml` (1),
`generation.brain.yml` (2). La rupture 4 du test à blanc est donc tenue par
mesure et non par déclaration.

## Ce que les cas ont révélé, et qui ne se lisait pas dans le code

Six choses, et aucune n'a été trouvée en relisant :

1. **Le point fixe s'interrompait sur un refus** (§3.3, correctif 1). Trouvé par
   le scénario de réparation : le vault rouge demandait deux exécutions.
2. **Le générateur plantait sur un manifeste sans bloc `genere.index`**
   (§3.3, correctif 2). Trouvé par le scénario 6 : `epreuve.brain.yml` ne déclare
   pas d'index, et une entrée de corpus n'avait donc pas de `path`.
3. **Un axe transverse retiré laisse ses hubs retomber en forme arbre**, ce qui a
   forcé `Pose.forme` (§3.3, correctif 3). Ce n'est pas un bug — c'est la
   conséquence du §4.1 — mais un test ne pouvait pas le distinguer d'une
   régression.
4. **Le catalogue comptait 14 pages là où le vault en portait 18** à la première
   génération d'un vault neuf, parce que les 4 hubs transverses naissaient après
   lui. C'est la seconde cause du point fixe.
5. **La collision de mot-clé `Prose.ligne(cle=...)`** : un axe transverse dont une
   valeur s'interpole sous le nom `{cle}` écrasait le paramètre nommé de la
   fonction. Corrigé par un paramètre positionnel — un détail, mais il ne serait
   apparu qu'à la première instance réelle.
6. **Le plafond de 260 caractères de Windows** : un arbre de travail posé sous un
   dossier temporaire dépasse le plafond, et l'échec se présentait comme un
   `FileNotFoundError` qui ne disait rien de sa cause. Contourné par le préfixe
   `\\?\`.

Et deux choses que le **DevBrain** a révélées, par le `diff` :

7. **`libelles.axe_transverse.domaines` n'était pas accentué** — seul des huit
   libellés du manifeste à échapper à la règle d'en-tête. Le générateur
   l'interpole dans la phrase d'intro des 6 hubs de `Métiers/` : sans l'accent,
   six pages en écart.
8. **`roles[hub].corps[<AUTO>].sections[].source` était de la prose.** Un
   générateur ne remplit pas une sous-section sur une phrase. `depuis:` a dû
   naître, avec son vocabulaire fermé.

---

# 6. La porte d'entrée du vault — pourquoi elle n'est pas de ce lot

Le lot me renvoyait la remontée 6 du lot 3 : *rien dans le manifeste ne déclare la
porte d'entrée du vault (`Home.md` et les autres `.md` de la racine) ; sans eux, 4
hubs deviennent orphelins*. Et il posait la condition : *si la porte d'entrée est
un artefact généré, elle est de ton périmètre ; sinon, dis-le et remonte-la.*

**Elle n'est pas un artefact dérivé, et elle n'est donc pas de ce lot.** La
distinction est nette et vérifiable :

- un artefact **dérivé** se régénère à chaque écriture dans le brain, se compare
  octet pour octet, et n'est jamais édité à la main. C'est ce que
  `genere.chemins` énumère, et les quatre générateurs de ce lot le tiennent.
- `Home.md` est un artefact de **semis** : écrit **une fois**, à la création de
  l'instance, puis édité à la main comme le corps d'un hub. Le cadrage le range
  explicitement là — §3.3, « ce qui est écrit à la fin de l'entretien » liste
  `Home.md`, `Inbox.md`, `AI/`, et c'est le **lot 5** qui l'écrit. Il n'apparaît
  dans aucune ligne de `genere.chemins`, et le DevBrain n'a aucun script qui le
  produise.

Le régénérer serait pire qu'inutile : le `Home.md` du DevBrain est un document
rédigé, et un générateur qui l'écrirait effacerait ce que floSa y a mis.

**Ce qui reste vrai, et que je remonte** : le besoin de la remontée 6 n'est pas
un besoin de génération, c'est un besoin de **déclaration**. Le validateur lit
tout `.md` de la racine pour son test d'atteignabilité, sans qu'aucun champ ne le
déclare — donc un brouillon posé à la racine élargirait silencieusement
l'atteignabilité. Cf. remontée 3.

Le vault d'épreuve porte le cas et l'écrit dans sa propre page :
`tests/genere-vert/Home.md` est la porte d'entrée, elle cite les hubs de premier
niveau, et **aucun générateur ne la touche** — la racine n'est pas un dossier de
pages, donc elle est hors du périmètre par construction.

---

# 7. Comment rejouer

```bash
# les quatre generateurs sur DevBrain, en LECTURE SEULE (mode par defaut)
uv run brainkit/generer/__main__.py

# le meme, en posant les artefacts dans un arbre de travail hors du vault
uv run brainkit/generer/__main__.py --sortie /tmp/bk4-diff

# un seul artefact
uv run brainkit/generer/__main__.py --quoi bandeau

# le jeu d'epreuve du lot 4 — sept scenarios
uv run tests/generation.py

# le jeu d'epreuve du lot 3, inchange
uv run --with jsonschema tests/epreuve.py

# les cinq manifestes contre le contrat du lot 1
uv run --with jsonschema schema/valider.py
uv run --with jsonschema schema/valider.py tests/epreuve.brain.yml tests/generation.brain.yml

# les trois chemins de lancement du kit
uv run brainkit/valider/__main__.py     # script autonome (en-tete PEP 723)
uv run -m brainkit.valider              # module du projet (pyproject.toml)
uv run brainkit generer                 # la commande
```

**DevBrain n'a été ouvert qu'en lecture.** Vérification sur les **27 points de
travail** du dépôt — le principal plus ses 26 worktrees :

```bash
git -C ../DevBrain worktree list --porcelain | grep '^worktree ' | sed 's/^worktree //' \
  | while read -r w; do echo "$(git -C "$w" status --porcelain | wc -l)  $w"; done
# -> 0 partout
```

Et le seul chemin d'écriture du paquet :

```bash
grep -rnE 'write_text|write_bytes|mkdir|unlink|rmtree|rename' brainkit/ --include='*.py'
# -> brainkit/generer/sortie.py, deux lignes ; le reste est de la documentation
```

---

# 8. Remontées

Cinq points. Aucun n'est corrigé — sauf les **corrections du manifeste et du
schéma** que les générateurs ont exigées, signalées comme telles au point 0.

## 0. Les sept corrections du manifeste, et pourquoi elles n'étaient pas évitables

Commit séparé et explicite : `lot 4 : les corrections du manifeste et du schema
que les generateurs ont exigees`. Aucune n'a été faite « pour faire passer le
critère » : **trois** ne changent aucun octet des artefacts, et les quatre autres
en changent, mais parce que le manifeste ne savait pas **redire** ce que le vault
contient.

| # | Corrigé | Pourquoi le manifeste avait tort | Coût sur le `diff` |
|---|---|---|---|
| 1 | `libelles.axe_transverse.domaines` : accentué | Seul des huit libellés à échapper à la règle d'en-tête (accents partout sauf commentaires et `motif:`). Interpolé dans l'intro des 6 hubs de `Métiers/` | **6 pages** |
| 2 | `axes.transverses[].groupe_par` | `pointe_vers:` disait la même chose en prose, et une prose ne se lit pas par une machine | 0 |
| 3 | `sections[].depuis` (+ `.role`) | `source:` restait de la prose ; sans lecture machine, le générateur écrivait « (dossier vide) » sur les 67 hubs d'arbre | **67 pages** |
| 4 | `<AUTO>.tranche_au_lot_4` | l'arbitrage laissé ouvert par le lot 2, écrit là où il se lit | 0 |
| 5 | `genere.index.signature` / `.portee` / `.groupes`, `genere.liens.signature` | ce que l'artefact annonce comme son producteur, sa réserve de périmètre, l'ordre et le titre de ses groupes — trois valeurs d'**instance** qui vivaient dans le code | **2 fichiers** |
| 6 | `genere.prose` — 4 surcharges | de la dette du DevBrain que le kit n'a aucune raison d'hériter (§4.3) | **2 fichiers** |
| 7 | `regles[bandeau_a_jour].porte_par` | la remontée 10 du lot 3, tranchée (§4.2) | 0 |

Le schéma gagne **onze** champs facultatifs, tous documentés, sans réindentation
ni modification d'un champ existant : `axeTransverse.groupe_par`,
`section.sections[].depuis` et `.role`, `section.tranche_au_lot_4`,
`genere.index.signature` / `.portee` / `.groupes`, `genere.liens.signature`,
`genere.prose`, `regles[].porte_par` et `regleDeSocle.porte_par`. Les
**cinq** manifestes du dépôt passent `uv run schema/valider.py`.

## 1. La clé `scanned` du catalogue publie le contenu NON SUIVI de l'arbre de travail

C'est la cause des 3 lignes du §1.3, et le fait vaut plus que l'écart.
`build_index.py` publie la liste des dossiers de premier niveau qu'il a balayés.
Un dossier qui existe sur le disque sans être suivi par git — une sauvegarde, un
`node_modules`, un dossier temporaire d'éditeur — entre donc dans un artefact
**versionné**, et l'artefact cesse d'être reproductible : deux machines qui
génèrent le même commit produisent deux catalogues différents.

Le générateur du kit **reproduit ce comportement à l'identique**, parce que le
critère du lot est le `diff` vide. Deux issues possibles, et aucune n'est de ce
lot : ou `scanned` se restreint aux dossiers **qui portent une page**, ou la clé
disparaît (elle est dérivable de `genere.non_pages`, donc du manifeste). **À
traiter au lot 9**, qui écrira dans DevBrain et régénérera ses artefacts : c'est
le premier moment où changer la clé ne coûte pas le critère d'un lot antérieur.

## 2. La sous-section des vues lit une EXTENSION là où les autres lisent un `role:`

La remontée 5 du lot 1, mesurée latente par le lot 2, et toujours latente.
`### Comparatifs` se remplit depuis `dossier.glob("*.base")` alors que la page
`role: comparatif` existe à côté de son fichier de vue depuis le lot 5 du
DevBrain, et que c'est **elle** qui devrait être listée.

Ce que ça coûte aujourd'hui : **rien d'observable**. Le lot 2 a mesuré la
bijection — 47 pages, 47 fichiers, ses contrôles C8 et A17 à zéro — donc les deux
sources donnent le même ensemble. Ce que ça coûte en réalité : la zone AUTO cite
le `.base` et non la page, or un `.base` n'a ni frontmatter, ni couleur de graphe,
ni lien sortant. C'est un défaut de **graphe**, pas de contenu.

**Reproduit et non corrigé** : corriger coûterait le `diff` vide, et
l'interdiction du lot est explicite. Le premier comparatif créé sans son `.base`,
ou le premier `.base` orphelin, réveillera l'anomalie — et `A17` de
`outils/fidelite.py` le dira. **À traiter au lot 9**, même argument que la
remontée 1.

## 3. La porte d'entrée du vault reste à DÉCLARER, et ce n'est pas de la génération

Détaillé en §6. Ce n'est pas un artefact dérivé — c'est un artefact de **semis**,
écrit une fois par le lot 5 puis édité à la main — donc hors de ce périmètre.

Mais le besoin de la remontée 6 du lot 3 subsiste, et il est de **déclaration** :
le validateur lit tout `.md` de la racine pour son test d'atteignabilité, sans
qu'aucun champ ne le déclare. Un brouillon posé à la racine élargirait
silencieusement l'atteignabilité de 4 hubs de premier niveau.

**Recommandation, non appliquée** : un bloc `racine:` avec `porte_d_entree:` et la
liste des pages d'aiguillage de la racine, à côté de `frontieres_d_ecriture` où
`Inbox.md` est déjà nommé. **À trancher au lot 5**, qui écrit ces fichiers et qui
saura donc lesquels une instance neuve porte.

## 4. Le kit ne lit qu'UN champ de mots-clés transverses

L'index de mots-clés et la section « Tags → pages » de la carte des liens sont
construits depuis **un seul** champ : celui dont la `source:` commence par
`vocabulaires.`. C'est exact sur les cinq manifestes du dépôt, qui n'en déclarent
qu'un chacun.

Un brain qui en déclarerait deux — des mots-clés de sujet et des mots-clés de
provenance, par exemple — verrait le second **absent** de la carte des liens,
sans qu'aucun message le dise. Le module le documente et rend le premier dans
l'ordre du manifeste.

**Non corrigé** : c'est une décision de contrat, pas de générateur. Ou le
manifeste désigne explicitement le champ qui alimente l'index de mots-clés (une
`fonction: mots_cles` dans le dictionnaire de champs, comme
`fonction: resume_court`), ou le kit les fusionne et le dit. La première solution
est plus conforme à la discipline du lot 3 — *le moteur ne reconnaît jamais un
champ par son nom* — et le champ des cinq manifestes est justement reconnu par sa
`source:`, ce qui n'est pas la même chose qu'une fonction déclarée. **À trancher
avec le lot qui touche au contrat.**

## 5. Les treize `.pyc` que le lot 3 avait seulement ignorés

Une règle de `.gitignore` ne désuit pas ce qui l'est déjà. Le commit `437ab9a`
(« lot 3 : ignore le bytecode Python ») a posé la règle mais laissé les treize
fichiers **suivis**, donc modifiés à chaque exécution du kit : `git status` était
sale en permanence, et chaque commit de ce lot aurait porté du binaire.

**Corrigé**, dans un commit séparé et sans toucher une ligne de code, parce que
c'était dans le chemin du lot : la vérification `git status` vide est un critère
d'acceptation, et elle n'était pas atteignable. C'est le seul point de ce
document qui corrige quelque chose hors de son périmètre, et je le signale comme
tel.

---

# 9. Ce qui reste au lot 5

- **`Home.md`, `Inbox.md` et les pages de la racine** sont des artefacts de semis :
  c'est le lot 5 qui les écrit, et c'est avec eux sous les yeux que la déclaration
  de la porte d'entrée se décide (remontée 3).
- **`re-seuiller`** (rupture 5) hérite d'une conséquence du §4.1 : un axe
  transverse retiré du manifeste laisse son dossier peuplé de hubs qui retombent
  en forme arbre. Décider du sort d'un dossier orphelin est le même travail que
  décider du sort d'un sous-dossier déseuillé.
- **La création d'un hub** est déjà là et déjà éprouvée : le générateur pose un
  hub transverse absent, avec le frontmatter que le manifeste **exige** du rôle
  hub et rien de plus. Le lot 5 en aura besoin pour l'arbre entier, et il peut
  s'appuyer sur `hubs._hub_neuf`.
- **Le mode `freeze` de §5.1** : les deux chemins de lancement coexistent déjà
  (`pyproject.toml` pour une instance branchée, l'en-tête PEP 723 pour une
  instance figée). Ce qui manque est la copie, et le test croisé du lot 10.
