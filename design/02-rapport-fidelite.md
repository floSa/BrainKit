# BrainKit — le test de fidélité du manifeste

> Conversation 43, « BrainKit lot 2, le test de fidélité », le 2026-09-07.
> Entrées : `design/01-manifeste.md` · `exemples/devbrain.brain.yml` · le vault
> DevBrain, en **lecture seule absolue**.
>
> Livrables du lot : `outils/fidelite.py` · ce rapport · les corrections de
> `exemples/devbrain.brain.yml` et de `design/01-manifeste.md` que la boîte 1
> impose (commit `lot 2, boite 1 : …`).
>
> **Aucune écriture dans DevBrain.** Rien n'est généré : ni hub, ni index, ni
> bandeau, ni gabarit — c'est le lot 4. Rien n'est validé au sens de
> `brain-v3.md` §10 — c'est le lot 3. Aucun des douze points ouverts de
> `00-cadrage.md` §5 n'est tranché.

Le lot 1 a produit un manifeste qui **prétend** redire DevBrain à l'identique.
Ce lot met la prétention à l'épreuve : un outil lit les deux et rapporte chaque
écart. Le verdict tient en une phrase — **le manifeste sait redire DevBrain, et
il se trompait sur neuf points, tous du même genre.**

---

# 1. Le périmètre, avant les comptes

C'est la conséquence pour ce lot de la remontée 1 du lot 1 : *un test qui compare
338 à 337 échoue pour une raison qui n'est pas la bonne.* Le périmètre est donc
lu **dans le manifeste**, pas décidé ici : `genere.non_pages`, énuméré par la
négative — tout dossier de la racine qui n'est pas de l'outillage porte des
pages.

Neuf dossiers écartés : `.git` · `.claude` · `.obsidian` · `AI` ·
`Documentation` · `Templates` · `Projects` · `docs` · `MOC`.

`Templates/` en fait partie, et c'est la clé du compte : ses six gabarits portent
un `role:` (2 `brique`, 1 `notion`, 1 `pattern`, 1 `rule`) sans être des pages du
brain. Ce sont eux qui produisaient les « 6 patterns, 6 règles » du cadrage.

## Les populations, mesurées contre `roles[].population`

| Rôle | `population` déclarée | Pages mesurées | Écart |
|---|---|---|---|
| `brique` | 337 | **337** | 0 |
| `notion` | 297 | **297** | 0 |
| `comparatif` | 47 | **47** | 0 |
| `hub` | 74 | **74** | 0 |
| `pattern` | 5 | **5** | 0 |
| `rule` | 5 | **5** | 0 |
| **Total** | **765** | **765** | **0** |

765 pages lues, **765 au frontmatter lisible** — zéro page illisible, ce qui
confirme la mesure de la règle de socle `frontmatter_lisible`. Aucun `role:`
inconnu du manifeste. Les six comptes du `CLAUDE.md` de DevBrain et de la
remontée 1 sont donc exacts, et retrouvés indépendamment.

---

# 2. Ce que l'outil confronte, et ce qu'il ne confronte pas

`outils/fidelite.py`, lecture seule, PEP 723, `uv run outils/fidelite.py`.
**Aucune valeur de DevBrain n'est écrite dans le code** : les 20 préfixes, les
109 valeurs d'axe, le seuil de promotion et son plafond, les 47 sous-libellés,
les 38 sections de corps, les 4 colonnes du bandeau et leurs 5 tables de rendu
sont **lus dans le manifeste**. Un test qui recopierait le vault ne testerait
rien : il vérifierait que la conversation 43 sait relire la conversation 42.

Six passes, **58 contrôles** :

| Famille | Ce qu'elle confronte |
|---|---|
| `P*` | la population d'un rôle contre `roles[].population` |
| `F*` (14) | le gabarit de frontmatter : `requis`, `autorises`, dictionnaire `champs:`, vocabulaires d'énumération, `conditionnels[]` dans les deux sens, `deprecies`, `porte_par` / `interdit_sur` de l'axe de nature, lisibilité |
| `C*` (17) | le gabarit de corps : sections déclarées absentes, titres présents et **non** déclarés avec leur libellé réel, couverture d'une section à condition, `mesure:` contre le compte réel, vocabulaire fermé d'une section `etiquetee`, section adossée à un champ, embed et fichier de vue, zones AUTO |
| `B*` (7) | le bandeau **rendu depuis le frontmatter** selon les tables déclarées : en-tête, nombre de cellules, réinjection du résumé, et chaque cellule contre sa dérivation |
| `A*` (17) | l'axe et les chemins : valeurs déclarées sans page et l'inverse, promotions contre le seuil et son plafond, `prefixe_nom`, dérivation du chemin, un hub par dossier et par valeur transverse, lien retour du hub de ralliement |
| `N*` (2) | l'homonymie : une valeur d'axe qui porte le nom d'un rôle, un champ qui porte le libellé de l'axe de rangement |

**Ce que l'outil ne fait pas**, et pourquoi c'est délibéré : il ne vérifie
aucune des dix règles de `brain-v3.md` §10 (réciprocité, réinjection du résumé,
citation unique, redirection sourcée…). Le lot 3 écrit le validateur de vault ;
ici on ne compare que le manifeste au vault. Là où les deux se touchent — les
étiquettes fermées de `Ressources`, la section adossée à `alternatives:` — c'est
parce que le **manifeste déclare** le vocabulaire ou la liaison, pas parce que
la règle est réimplémentée.

## Le mécanisme qui interdit une divergence inexpliquée

Le critère du lot — *aucune divergence « inexpliquée » ne doit subsister* — n'est
pas tenu par de la bonne volonté mais par du code. La table `VERDICTS` de
`fidelite.py` porte, pour chaque groupe de divergences, une boîte (`manifeste` ou
`vault`) et un motif d'une ligne. **Un groupe sans verdict sort en
`INEXPLIQUEE` et l'outil rend le code 1.** Une divergence nouvelle ne peut donc
pas passer en silence : elle casse la sortie jusqu'à ce qu'on la range.

L'inventaire `CONTROLES` sert la même défiance dans l'autre sens : le rapport
imprime les codes qui n'ont **rien** trouvé, nommés. Sans cette liste, un
contrôle vert et un contrôle mort se ressemblent — c'est exactement ce que la
règle `completude_du_hub` a coûté au DevBrain (« une règle absente ne ressemble
pas à une règle souple, elle ressemble à une règle satisfaite »).

---

# 3. Le chiffrage

Deux exécutions, sur le **même** vault et le **même** outil, avec les deux
versions du manifeste. La première est rejouable :
`git show bb69ebf:exemples/devbrain.brain.yml`.

| | Manifeste du lot 1 | Manifeste corrigé |
|---|---|---|
| Groupes de divergences | **35** | **34** |
| Occurrences (pages × groupes) | **526** | **296** |
| **Boîte 1 — erreur du manifeste** | **9 groupes**, 408 occurrences | 8 groupes, 178 occurrences |
| **Boîte 2 — fait connu du vault** | **26 groupes**, 118 occurrences | 26 groupes, 118 occurrences |
| **Inexpliquées** | **0** | **0** |
| Codes actifs / muets | 14 / 44 | 13 / 45 |
| `mesure:` confrontées / en écart | **54 / 0** | **54 / 0** |

Trois lectures de ce tableau.

**Les 54 comptes déclarés sont tous justes.** Chaque `mesure:` du manifeste a été
confronté au vault : **35** des 38 sections de corps (les trois autres sont des
marqueurs de place sans compte — l'accroche et l'embed d'un comparatif, la zone
AUTO d'un hub), **6** sous-sections de zone AUTO, **6** populations de rôle plus
leur total, **5** comptes de l'axe de rangement (109 valeurs déclarées, 104
portées, 20 préfixes, 47 sous-libellés, 45 promus) et **1** de l'axe de nature
(9 valeurs). **Zéro écart.** La transcription du lot 1 est exacte au chiffre
près, ce qui est le résultat le plus important de ce lot et le moins visible : il
n'apparaît nulle part dans la liste des divergences.

**Les 9 erreurs sont toutes du même genre**, et il n'est pas celui qu'on
attendait. Aucune n'est une valeur fausse. Ce sont neuf endroits où le manifeste
portait déjà le **bon chiffre** et n'en avait pas tiré la **conséquence** : une
section mesurée à 324/337 était déclarée universelle, une condition mesurée dans
un sens était écrite dans l'autre. Le manifeste savait, et disait autre chose.

**La boîte 2 ne bouge pas.** 26 groupes avant, 26 après : la correction du
manifeste n'efface aucun fait du vault, et c'est la preuve que les deux boîtes ne
se mélangent pas.

---

# 4. Boîte 1 — les neuf erreurs du manifeste, une par une

Le manifeste disait faux, le vault avait raison. Chacune est corrigée dans
`exemples/devbrain.brain.yml`, et trois d'entre elles ont aussi demandé de
corriger `design/01-manifeste.md` : la spec avait mal guidé la transcription.

## 1 à 5. Cinq sections non universelles, déclarées sans condition

| Section | Rôle | Mesure déclarée | Population | Pages sans la section |
|---|---|---|---|---|
| `### Alternatives` | `brique` | 324 | 337 | **13** |
| `### Compléments` | `brique` | 103 | 337 | **234** |
| `## Notes` | `hub` | 13 | 74 | **61** |
| `## Ce qu'il faut comprendre` | `hub` | 71 | 74 | **3** |
| `## Choisir` | `hub` | 71 | 74 | **3** |

Les cinq portaient leur `mesure:` exacte — le lot 1 les avait comptées — et
étaient déclarées comme les sections universelles voisines. L'outil les a donc
sorties comme 314 pages incomplètes.

**Un `mesure:` qui n'égale pas la population de son rôle EST la déclaration
qu'une condition manque.** C'est la faute de la remontée 3 du lot 1, sur cinq
sections que personne n'avait comptées : `Les maths, simplement` a été passée en
`conditionnelle` parce que quelqu'un a mesuré 282/297 ; les cinq ci-dessus ont
été mesurées et laissées inconditionnelles.

Les cinq portent désormais un `existe_si`. Ce que la mesure apprend au passage,
et qui va au-delà du format :

- **Les 13 briques sans `### Alternatives`** sont 10 pages d'`Outils de
  développement/` (Pydantic, pytest, Rich, Ruff, Typer, testcontainers, jupysql,
  papermill, Quarto, Obsidian) et 3 de `Machine Learning/` (SetFit,
  imbalanced-learn, supervision). Ce n'est pas un défaut de rédaction : ce sont
  des briques sans concurrente fichée, exactement le cas que la règle
  `voisinage_declare` déclare **souple pour toujours** — « une brique peut
  légitimement n'avoir aucune alternative ; la signaler aide, l'interdire
  mentirait ».
- **Les 13 hubs qui portent `## Notes`** sont **tous les treize** sous
  `Machine Learning/`. Une section manuelle qui n'existe que dans un domaine
  n'est pas un élément de gabarit : c'est un usage local, né d'un lot. Le
  déclarer universel aurait fait de 61 hubs des pages en dette.
- **Les 3 hubs sans corps d'aiguillage** sont nommés au point 7 ci-dessous.

## 6. `### Alternatives` déclarée comme le miroir de son champ, et 51 pages le démentent

`Alternatives` était déclarée `genre: liste_liens, champ: alternatives`, ce qui
dit que la section liste le contenu du champ. Le décompte réel des 324 :

- **273** pages où `alternatives:` est renseigné et la section le liste ;
- **51** pages où la section existe avec un champ **vide** ;
- 13 pages sans ni l'un ni l'autre.

Les 51 ne sont pas une faute : c'est la forme que la règle `citation_unique`
**recommande** explicitement, et son motif la cite mot pour mot — « Aucune
outillée dans le brain : l'approche concurrente est [[Diff-in-Diff]] », où le
lien **explique** au lieu de **lister**. Vérification sur `docTR` : « Aucune dans
le brain : les moteurs OCR concurrents — PaddleOCR, EasyOCR, TrOCR, Tesseract —
sont hors périmètre. »

Le `champ:` seul surdéclarait donc un miroir que le vault n'a jamais tenu, et le
manifeste se contredisait d'un bloc à l'autre : `roles[].corps` promettait un
miroir strict que `regles[citation_unique].motif` disait de ne pas tenir.
L'`existe_si` écrit la vraie condition. À l'inverse, `Compléments` **est** le
miroir exact de son champ : zéro page avec la section et un champ vide, zéro page
avec un champ rempli sans la section. Les deux sections voisines ne se
comportent pas pareil, et le manifeste ne le disait pas.

## 7. Un `motif:` faux : les trois hubs sans corps d'aiguillage ne sont pas les bons

Le lot 1 écrivait : *« les trois qui ne le portent pas sont les hubs de
ralliement, dont le corps est une phrase et une zone AUTO propre (Comparatifs)
ou deux notions chapeaux absorbées ».* Mesure :

| Hub | Pourquoi il n'a pas les deux sections |
|---|---|
| `Bases de données/Bases de données.md` | a absorbé une notion chapeau et garde son corps de **notion** |
| `LLM & IA générative/Text-to-SQL/Text-to-SQL.md` | idem |
| `Métiers/Infrastructure & Ops.md` | hub **transverse** sans aucun corps écrit : son unique contenu est sa zone AUTO |

Le hub `Comparatifs`, que le lot 1 comptait parmi les trois, **porte les deux
sections**. L'erreur est instructive parce qu'elle est arrivée par déduction : le
lot 1 a raisonné « les hubs spéciaux sont trois, les manquants sont trois, donc
ce sont les mêmes ». Les deux ensembles ont la même taille et ne se recouvrent
qu'à moitié.

## 8. La zone AUTO d'un hub a trois formes, le manifeste n'en déclarait qu'une

`roles[hub].corps` déclare **une** zone AUTO, `perimetre: dossier`, avec six
sous-sections dont les mesures sont justes. Le vault en a trois :

| Forme | Pages | `perimetre` | Sous-sections |
|---|---|---|---|
| hub d'**arbre** | 67 | `dossier` | les six déclarées (Sous-domaines 10, Notions 39, Briques 58, Patterns 1, Rules 1, Comparatifs 37) |
| hub de **ralliement** | 1 (`Comparatifs`) | `role` | **12**, qui sont des libellés de domaine et non des sections de gabarit |
| hub **transverse** | 6 (`Métiers/`) | `champ` | aucune : une phrase, puis une puce par sous-hub |

L'outil a retrouvé les 12 sous-titres du hub de ralliement en les confrontant à
l'ensemble des étiquettes de groupe **dérivables du manifeste** — les dossiers de
préfixe de l'axe de rangement. Les 12 en sont, toutes : Automatisation no-code ·
Bases de données · Calcul distribué · Data & pipelines · Design & diagrammes ·
Interfaces & apps data · LLM & IA générative · Machine Learning · Mathématiques ·
Outils de développement · Signal & audio · Statistiques & inférence. Le
manifeste **déclare** le groupement (`hub_de_ralliement.groupe_par`) ; ce qu'il
ne déclare pas, c'est que la zone AUTO du rôle en dépend.

`perimetre` énumère déjà les trois valeurs — la forme est *exprimable*. Ce qui
manque est de savoir si un rôle porte **plusieurs** gabarits de zone AUTO ou si
la forme se **dérive** de `hub_par_valeur` et de `hub_de_ralliement`. C'est une
décision de générateur : elle appartient au lot 4, et ce lot ne la prend pas. Le
constat est écrit et mesuré dans le manifeste, en `motif_trois_formes`.

## 9. `conditionnels[].si` : une permission écrite comme une obligation

§2.7 du contrat écrivait : *« un conditionnel sans `si` est un champ autorisé qui
se croit conditionnel : le validateur de vault ne saurait jamais quand
l'**exiger** »*. Lu ainsi, `si: "famille in [plateforme, saas, application]"`
**exige** `hosted:` et `scaling:` sur toute brique de ces trois familles.
Mesure :

| | Compte |
|---|---|
| briques portant `hosted:` (et `scaling:`) | **98** |
| briques d'une famille hébergée | **119** |
| briques des trois familles sans ni l'un ni l'autre | **21** |
| … dont portant `os:` à la place | **21 sur 21** (18 `application`, 2 `saas`, 1 `plateforme`) |

R16, la règle qui a créé ces deux conditionnels, refuse le champ **hors** des
trois familles ; elle ne l'exige nulle part. Lire `si` comme une obligation
produisait donc **42 fausses violations** sur un vault que ses deux validateurs
déclarent vert — et sur des pages qui répondent déjà à la question autrement :
une application de bureau ne s'héberge pas, elle tourne sur un `os:`, et c'est
exactement ce que la colonne *Exécution* du bandeau va chercher en repli.

`si` est donc une **permission** : le champ n'existe **que si** la condition
tient. La spec est corrigée, et le manifeste porte la mesure. Un champ qui
exprimerait une **vraie** obligation conditionnelle n'existe pas dans le
contrat ; ce lot ne le crée pas — cf. *Remontées*, point 2.

## Les onze corrections, et ce qu'elles changent

Neuf divergences, closes par **onze** corrections.

Dans `exemples/devbrain.brain.yml` (**8**) :

| # | Où | Ce que ça change |
|---|---|---|
| 1 | `roles[brique].corps` → `Alternatives` | `existe_si` + le décompte 273 / 51 / 13. Un générateur ne posera plus la section vide sur les 13 |
| 2 | `roles[brique].corps` → `Compléments` | `existe_si` sur le champ, et la mention que celle-ci **est** le miroir exact, contrairement à sa voisine |
| 3 | `roles[hub].corps` → `Ce qu'il faut comprendre` | `existe_si` + les trois hubs **nommés** |
| 4 | `roles[hub].corps` → `Choisir` | `existe_si`, mêmes trois hubs |
| 5 | `roles[hub].corps` → `Notes` | `existe_si` + le fait que les 13 sont tous sous un seul domaine |
| 6 | `roles[hub].motif` | ne nomme plus « les hubs de ralliement » ; renvoie aux trois hubs mesurés |
| 7 | `roles[hub].corps` → `<AUTO>` | `motif_trois_formes` : les trois formes, leurs `perimetre`, leurs comptes, et le renvoi au lot 4 |
| 8 | `roles[brique].champs` | `note_sens_de_la_condition` : `si` permet, n'exige pas, avec les quatre comptes |

Dans `design/01-manifeste.md` (**3**) :

| # | Où | Ce que ça change |
|---|---|---|
| 9 | §2.7, `conditionnels[]` | « quand le **permettre** » remplace « quand l'exiger », plus un bloc qui écrit la mesure. Sans quoi le validateur du lot 3 naîtrait avec 42 fausses violations |
| 10 | §2.8, gabarit de corps | `existe_si` est permis sur **toute** section et seulement *exigé* sur une `conditionnelle` — ce que le schéma encodait déjà et que le tableau des genres démentait |
| 11 | §6, la complétude chiffrée | un chapeau qui dit que les 54 comptes sont confrontés et justes ; les cinq sections marquées `existe_si` ; le bloc sur les trois formes de zone AUTO |

**Le schéma n'est pas touché.** Les onze corrections tiennent dans le contrat du
lot 1 : `uv run schema/valider.py` passe les trois exemples au vert, `existe_si`
et les annotations `motif_*` / `note_*` étaient déjà légales partout où elles
sont posées. Une correction qui aurait demandé un champ neuf est restée une
remontée, pas une modification.

---

# 5. Boîte 2 — les vingt-six faits connus du vault

Le manifeste dit vrai, le vault s'en écarte. **Aucun n'est réparé**, y compris
quand c'est une vraie faute de la page : DevBrain est en lecture seule, et le
premier lot autorisé à y écrire est le lot 9.

## Le vocabulaire d'axe : 5 valeurs déclarées que personne ne porte

`A1` — les cinq, retrouvées par balayage : **`skill/code-quality`, `skill/data`,
`skill/dev-flow`, `skill/documents`, `skill/meta`**. La sixième,
`skill/knowledge`, porte `Obsidian`, seule page du préfixe rattaché.

C'est l'écart 109 − 104, et il est **entier de ce côté** : aucune valeur portée
n'est hors vocabulaire (`A2` à zéro). La `regle_de_retrait` transcrite dans le
manifeste dit qu'*une valeur est retirée dès qu'aucune page ne la porte, parce
que la laisser autoriserait une rechute silencieuse* — elle a été appliquée sans
exception aux onze valeurs de `concept/*`, y compris à `concept/devops` qui
n'avait jamais porté de page. Les cinq `skill/*` y échappent et rien ne dit
pourquoi. **Le rapport les liste, comme la remontée 6 bis le demandait ; il ne
les retire pas.**

`A3` — deux sous-libellés déclarés sans dossier : **`automation/no-code`** (5
pages au seuil, 6 au total) et **`storage/objet`** (6 et 6). Les deux sont
bloqués par le plafond de promotion, le manifeste le déclare et l'explique. La
différence 5/6 et 6/6 est elle-même une confirmation : le comparatif du dossier
compte dans le total et **pas** au seuil, `pese_sur_le_seuil: false` fonctionne.

## Les sections : 12 groupes

`C1` — **4 briques ne portent aucune section `## Écosystème`** :
`imbalanced-learn`, `Quarto`, `Obsidian`, `Ruff`. Elles n'ont donc ni
`### Alternatives` ni `### Compléments`. C'est le **seul** titre de corps de
brique qui ne soit pas à 337/337, et c'est la seule section de la boîte 1 que je
n'ai **pas** passée en conditionnelle : ici le manifeste déclare volontairement
une section universelle et une faute du vault (remontée 4), pas une section
facultative. C'est ce qui départage les deux boîtes sur un cas presque identique
aux cinq du point précédent.

`C2` — **6 sections de notion sur 2 hubs** : `Bases de données` et `Text-to-SQL`
portent `## Aperçu`, `## Concepts clés`, `## Les maths, simplement`,
`## En pratique`, `## Approches voisines & alternatives`,
`## Pour aller plus loin`. Ces deux hubs de domaine ont **absorbé** une notion
chapeau — c'est cette fusion qui a supprimé la dernière collision de nom du
vault — et gardent son corps.

`C2` — **2 sections manuelles sur 2 comparatifs** :
`## Pourquoi la vue liste ses membres nom par nom`
(`Interfaces & apps data/Comparatif - Frontends web légers`) et
`## Ce comparatif ne compare rien, et ce n'est pas la conversion qui le règle`
(`Mathématiques/Optimisation/Comparatif - Solveurs d'optimisation`). Deux notes
d'arbitrage laissées dans la page, hors du gabarit de quatre sections.

`C3` — **2 titres de niveau 3 dans une section contrôlée** :
`### Modèles locaux disponibles` sous `## Mise en œuvre` (`Médias/Superwhisper`,
une section `etiquetee`, donc à vocabulaire fermé) et
`### Outils — données tabulaires & factices (hors LLM)` sous
`## Approches voisines & alternatives`
(`LLM & IA générative/Fine-tuning/Synthetic data generation`). Les deux seuls du
vault : partout ailleurs, les `###` libres vivent sous une section `genre: libre`,
où ils sont permis par déclaration.

`C4` — **`## Les maths, simplement` sur 282 notions sur 297.** Les 15 qui ne la
portent pas, nommées : `Migrations de schéma`, `ORM`, `Architecture médaillon`,
`Change Data Capture (CDC)`, `Contrats de données & qualité`,
`EDA automatisée & profiling`, `ELT vs ETL & idempotence`, `Web scraping`,
`Stream processing`, `Versionnage de données`, `a2a-protocol`, `Agent skills`,
`Feature store — concept`, `Model registry & versioning`,
`Sandboxing de code généré`. Aucune n'a de formule à expliquer, et la section n'a
pas été posée vide — c'est le bon comportement, et c'est la remontée 3, retrouvée
par mesure.

`C11` — **5 étiquettes hors du vocabulaire fermé de `## Ressources`** :
« Poids » sur `needle`, « Site » sur `OpenCut`, `Superwhisper`, `croc`,
`Sniffnet`. Ce sont **exactement** les 5 violations que le lot 8 a mesurées et
qui maintiennent cette moitié de la règle `etiquettes_fermees` en avertissement.
Le manifeste les déclare dans `mesure_etiquettes` ; l'outil les retrouve seul, et
nomme les pages, ce que la mesure du lot 8 ne faisait pas. L'arbitrage — ouvrir
le vocabulaire ou corriger les 5 pages — appartient à floSa.

## Les champs : 4 groupes

`F8` — les deux champs déclarés `deprecies` sur `role: brique` sont encore
portés : **`os:` par 37 briques**, **`domaines:` par 30**. C'est la remontée 8,
mesurée. Le chiffre a une conséquence pratique que le lot 1 n'avait pas
soulignée : `os:` n'est pas un vestige mort. Les 21 briques du point 9 de la
boîte 1 s'appuient dessus pour remplir la colonne *Exécution* du bandeau. Retirer
le champ viderait 21 cellules — le déclarer vestigial et le garder est le bon
compromis, et le manifeste avait raison de le porter par le **rôle** plutôt que
par le champ.

`F12` — **1 brique sans valeur d'axe de nature** : `Obsidian`. C'est **légal** :
`vide_autorise: true`, et le manifeste écrit pourquoi — *un champ vide est le seul
signal prévu pour « l'arbre de décision n'a pas tranché »*. Le compte annoncé par
le manifeste (« 1 brique concernée ») est exact.

`F7` — les 21 briques du point 9 de la boîte 1, comptées pour mémoire une fois la
spec corrigée. Le groupe reste dans la boîte 1 parce que c'est une erreur du
manifeste qui l'a fait apparaître.

## L'homonymie : 3 groupes

`N1` — **`ml/hub`** est une sous-valeur de l'axe de rangement homonyme du rôle
`hub`, et **2 briques la portent** : `Machine Learning/HuggingFace` et
`Machine Learning/datasets`. Deux choses différentes portent le même mot dans
deux champs différents de la même page.

`N2` — **`domaine:`** de `role: rule` est une chaîne libre, et c'est le libellé de
l'axe de rangement, dont le champ s'appelle `categorie:`. C'est la remontée 7,
retrouvée mécaniquement.

`N2` — **`domaines:`** est le champ de l'axe transverse, et c'est le **pluriel**
du libellé de l'axe de rangement. Le manifeste le sait — c'est pour cette raison
exacte que le dossier s'appelle `Métiers/` et non `Domaines/`, et la note est
dans le code de DevBrain — mais le **champ**, lui, garde le mot. Un validateur
piloté par le manifeste devra distinguer trois choses qui s'écrivent « domaine » :
`champs.domaine` (une prescription), `champs.domaines` (l'axe transverse) et
`libelles.axe_rangement` (le mot de la prose).

---

# 6. Les neuf divergences connues du lot 1 : huit trouvées, une latente

Contrôle de vérité du lot. Aucune n'a été soufflée à l'outil : les verdicts ont
été écrits **après** la première exécution, sur ce qu'elle avait sorti.

| Remontée du lot 1 | Ce que l'outil a produit seul | Verdict |
|---|---|---|
| **1.** 337 / 297 / 47 / 74 / 5 / 5 = 765, et non 338 / 299 / 47 / 75 / 6 / 6 | `P1` à zéro sur les six rôles, total 765, périmètre lu dans `genere.non_pages` | **trouvée** |
| **2.** le titre réel de la 5ᵉ section d'une notion est `## Approches voisines & alternatives` | contrôle négatif ci-dessous : nourri du titre de la spec, l'outil sort 297 pages sans la section, la `mesure:` en écart, et **le titre réel sur les 297** | **trouvée** |
| **3.** `## Les maths, simplement` est sur 282/297, pas 297 | contrôle négatif : `mesure: 297` déclarée, 282 mesurées, et les 15 pages nommées | **trouvée** |
| **4.** 4 briques sans `## Écosystème` | `C1` : `imbalanced-learn`, `Quarto`, `Obsidian`, `Ruff` — les quatre, nommées | **trouvée** |
| **5.** le hub liste ses comparatifs depuis les `.base`, pas depuis `role:` | `C8` **et** `A17` à zéro : les deux sources donnent aujourd'hui le même ensemble de 47 | **LATENTE — non observable** |
| **6.** 47 sous-libellés et 109 valeurs d'axe, contre les 39 et 94 annoncés | les mesures `sous_libelles_declares: 47`, `valeurs_declarees: 109`, `prefixes: 20`, `sous_domaines_promus: 45` confrontées, 0 écart | **trouvée** |
| **6 bis.** 5 des 6 valeurs `skill/*` ne portent aucune page | `A1` : les cinq, nommées, plus l'écart 109 − 104 = 5 refermé des deux côtés (`A2` à zéro) | **trouvée** |
| **7.** `domaine:` de `role: rule` est homonyme de l'axe sans être lui | `N2` : trouvée, **plus** une seconde du même genre que le lot 1 n'avait pas nommée (`domaines:`) | **trouvée** |
| **8.** `os:` et `domaines:` sont des vestiges portés par le rôle | `F8` : 37 et 30 pages, nommées | **trouvée** |

**Huit sur neuf, mécaniquement. La neuvième est aveugle et je le dis.**

## La remontée 5 n'est pas manquée : elle est latente, et c'est mesuré

`build_mocs.zone_hub()` remplit `### Comparatifs` avec `dossier.glob("*.base")`
au lieu de lire `role: comparatif`. Un comparateur manifeste ↔ vault ne peut pas
voir un choix de **source** : il ne voit que le résultat. Or les deux sources
donnent aujourd'hui le même ensemble, et c'est ce que deux contrôles à zéro
disent :

- `C8` — aucune page `role: comparatif` sans son `.base` : **47 sur 47** ;
- `A17` — aucun `.base` sans sa page : **47 fichiers, 47 pages**.

Tant que la bijection tient, l'anomalie ne produit aucune différence
observable — elle produit seulement un `.base` cité à la place de sa page dans
la zone AUTO, ce qui est un défaut de **graphe** (le `.base` n'a ni frontmatter,
ni couleur, ni lien sortant) et non de contenu. Le premier comparatif créé sans
son `.base`, ou le premier `.base` orphelin, la réveillera : `A17` le dira. La
remontée reste donc à traiter au lot 4, et le lot 2 apporte ce qui manquait — la
**mesure** qui dit qu'elle ne coûte rien aujourd'hui, et le contrôle qui préviendra
le jour où elle coûtera quelque chose.

## Le contrôle négatif : ce que l'outil sort quand on lui donne la spec

Les remontées 2 et 3 sont des divergences **spec ↔ vault** que le manifeste du
lot 1 avait déjà absorbées : il transcrit le titre des pages, pas celui de
`brain-v3.md` §7. Un comparateur manifeste ↔ vault ne peut donc que les
**confirmer** — sauf si on lui donne à lire la version de la spec. C'est
exactement le contrôle négatif du lot 1, reconduit.

Deux substitutions dans une copie de `exemples/devbrain.brain.yml` :

1. `titre: "Approches voisines & alternatives"` → `titre: "Approches voisines"` ;
2. `Les maths, simplement` repassée en `genre: libre`, `mesure: 297`,
   `existe_si` retiré.

Résultat : **37 groupes, 891 occurrences, 5 inexpliquées, 2 `mesure:` en écart** —
et l'outil rend le code 1. Les cinq lignes, telles qu'il les imprime :

```
[!! INEXPLIQUEE] notion.Approches voisines — section declaree `## Approches voisines`
                 absente (297/297 page(s) de `role: notion`)  (297)
[!! INEXPLIQUEE] notion.Approches voisines & alternatives — `## Approches voisines &
                 alternatives` present sur `role: notion` et absent du gabarit
                 declare  (297)
[!! INEXPLIQUEE] notion.Approches voisines — `mesure: 297` declaree et 0 page(s) la
                 portent  (1)
[!! INEXPLIQUEE] notion.Les maths, simplement — section declaree absente
                 (15/297 page(s) de `role: notion`)  (15)
[!! INEXPLIQUEE] notion.Les maths, simplement — `mesure: 297` declaree et 282
                 page(s) la portent  (1)
  [ECART] corps/notion · Approches voisines : declare 297, mesure 0
  [ECART] corps/notion · Les maths, simplement : declare 297, mesure 282
```

L'outil ne sort pas seulement « la section manque » : il sort **le libellé réel**,
sur les 297 pages, ce qui est la remontée 2 mot pour mot. Les deux étaient donc
trouvables, et le sont.

---

# 7. Ce que le manifeste redit juste

C'est le résultat central, et il n'apparaît nulle part dans les six sections
précédentes. **45 des 58 contrôles n'ont rien trouvé.** Les plus significatifs :

| Contrôle | Ce que son silence dit |
|---|---|
| `A12` | **les 765 chemins de page se dérivent du manifeste seul.** Le seuil (5), son plafond, les 20 dossiers de préfixe, le rattachement `skill`, les 47 sous-libellés et le comptage par domaine des seules pages qui `pese_sur_le_seuil` reproduisent l'arbre **à l'identique** : zéro page ailleurs que là où le manifeste la met. C'est la propriété la plus difficile du contrat, et elle tient |
| `A13`, `A14`, `A15`, `A9` | tout niveau de chemin porte son hub, aucun hub n'est orphelin, les 6 valeurs de l'axe transverse ont leur hub dans `Métiers/`, et chaque hub nomme soit son dossier soit une valeur transverse |
| `A16` | **les 47 comparatifs portent tous leur lien retour `[[Comparatifs]]`.** « C'est le lien retour qui fait la grappe » n'est pas une intention : c'est vérifié, 47/47 |
| `B3`, `B4`, `B7` | **les 337 bandeaux se rendent depuis le frontmatter par les seules tables du manifeste.** En-tête, nombre de cellules, et **chaque cellule** — les 5 tables de rendu, la qualification par `langage:` et son exception sur `saas`, la composition `<hosted> · <scaling>`, le repli sur `os:` pour une `application`. Zéro cellule divergente sur 1 348 |
| `B5` | le résumé est réinjecté en citation dans les 337 zones de bandeau |
| `C10` | **les 41 `mesure:` de corps — 35 sections plus 6 sous-sections de zone AUTO — zéro écart** |
| `F2`, `F3`, `F4`, `F14` | **aucun champ manquant, aucun champ en trop, aucun champ inconnu**, sur les 765 pages et les 6 gabarits. Le dictionnaire `champs:` couvre exactement ce que le vault écrit |
| `F5` | **aucune valeur d'énumération hors vocabulaire**, sur `role`, `categorie`, `famille`, `domaines`, `licence_type`, `maturite`, `hosted`, `scaling`. Les vocabulaires fermés sont fermés |
| `F9` | zéro page au frontmatter illisible |
| `A2`, `A4`, `A6` | aucune valeur portée et non déclarée, sur les trois axes. L'écart 109/104 est entier du côté « déclarée sans page » |
| `C6`, `C7`, `C8`, `C12`, `C15` | les 337 zones de bandeau, les 47 embeds, les 47 fichiers de vue, les 5 étiquettes obligatoires de `Mise en œuvre` sur 337 pages, les 74 zones AUTO : tous présents |

La conclusion du lot, dite dans l'autre sens : **le manifeste sait redire
DevBrain.** Sa structure — six rôles, deux axes plus un transverse, un
dictionnaire de champs, un gabarit de corps par rôle, un bandeau dérivé, une
dérivation de chemin — suffit à reproduire un vault de 765 pages sans exception
de chemin, sans exception de champ et sans exception de valeur. Ce qu'il n'avait
pas su faire, c'est tirer les conséquences de ses propres mesures.

---

# 8. Remontées

Six points. Aucun n'est corrigé ici — sauf les onze corrections de la boîte 1,
signalées comme telles à la section 4.

## 1. La forme de la zone AUTO d'un hub reste à trancher, et c'est du lot 4

Constaté et mesuré (boîte 1, point 8) : trois formes, un seul gabarit déclaré.
Deux options, et je n'en choisis aucune :

- **plusieurs `corps[]` de zone AUTO par rôle**, sélectionnés par une condition
  — lisible, mais ouvre la porte à des gabarits conditionnels partout ;
- **la forme dérivée** de `hub_par_valeur` (transverse) et de
  `hub_de_ralliement` (ralliement), l'arbre par défaut — plus économe, mais rend
  la zone AUTO implicite, donc invisible au lecteur du manifeste.

Ce qui est acquis : `perimetre` porte déjà les trois valeurs, et le sous-titrage
du hub de ralliement est **dérivable** (les étiquettes sont les dossiers de
préfixe de l'axe de rangement) — l'outil le fait déjà. Ce qui n'est pas acquis,
c'est la forme de déclaration. **À trancher au lot 4**, avec le générateur sous
les yeux.

## 2. Une VRAIE obligation conditionnelle ne s'exprime pas dans le contrat

`conditionnels[].si` est désormais écrit comme une permission, parce que c'est ce
que DevBrain fait. Mais un brain pourrait légitimement vouloir l'autre sens :
« si `famille: modele`, alors `poids_licence:` est **requis** ». Le contrat n'a
aucun moyen de le dire — `champs.requis` est inconditionnel, `conditionnels[]`
permet.

Je n'ai pas créé le champ, et c'est délibéré : l'entrée du contenu de
`{champ, si}` est fermée par `additionalProperties: false` dans le schéma, donc
l'ajouter aurait demandé de modifier `schema/brain.schema.json` — un artefact du
lot 1 — pour un besoin que **ni DevBrain ni HistoBrain n'ont**. Ajouter un champ
qu'aucun des deux remplissages n'emploie serait exactement le défaut que le
cadrage reproche à `status:` : une case que personne ne remplit et que le
validateur doit quand même porter.

Recommandation, pour quand le besoin apparaîtra : `{champ, si, sens: permet |
exige}`, `permet` par défaut. **À trancher au lot 3**, qui écrit le validateur et
qui verra le premier ce que la distinction coûte.

## 3. Les cinq `skill/*` orphelines : la règle de retrait attend un arbitrage

La remontée 6 bis demandait au lot 2 de les lister. C'est fait, nommément, à la
section 5. Ce que la mesure ajoute : l'écart est **entier** de ce côté (aucune
valeur portée n'est hors vocabulaire), et le préfixe `skill` est un
**rattachement**, pas un domaine — sa seule page vivante, `Obsidian`, est aussi
la seule brique du vault sans `famille:`. Le préfixe entier tient sur une page
qui est elle-même un cas limite.

Trois issues, aucune n'est de mon ressort : retirer les cinq et appliquer la règle
de retrait ; garder les six et écrire l'exception dans la règle ; ou retirer le
rattachement entier et recatégoriser `Obsidian`. **À trancher par floSa**, et à
exécuter au lot 9 au plus tôt — c'est une écriture dans DevBrain.

## 4. Le remplissage HistoBrain porte le même défaut de modélisation

`exemples/histobrain.brain.yml` déclare 38 sections de corps et **deux**
`existe_si`. Il ne porte aucun `mesure:` — c'est un brain neuf, sans pages — donc
rien ne permet aujourd'hui de dire lesquelles de ses 36 autres sections seront
universelles. Ce n'est **pas** une erreur du lot 1 : on ne mesure pas un vault
vide, et je ne l'ai pas corrigé.

Mais la leçon de la boîte 1 se transpose telle quelle, et elle vise le
**générateur** : une section qu'un brain neuf déclare universelle deviendra, au
bout de cent pages, soit une section universelle, soit une dette de cent pages
incomplètes. Le lot 8 du kit (la passe de mesure) doit donc pouvoir **proposer**
un `existe_si` sur toute section dont la couverture mesurée n'égale pas la
population de son rôle. C'est mécanisable : `outils/fidelite.py` le calcule déjà.
**À écrire au lot 8**, et à ne pas oublier au lot 5, qui écrit le générateur.

## 5. Trois choses s'écrivent « domaine », et le manifeste les met côte à côte

`N2` a trouvé deux homonymies, pas une : `champs.domaine` (la chaîne libre d'une
`role: rule`) et `champs.domaines` (le champ de l'axe transverse) portent tous
deux le libellé de l'axe de **rangement**, dont le champ s'appelle `categorie:`.
Le lot 1 n'avait nommé que la première.

Aucune conséquence machine aujourd'hui — les trois vivent dans des champs
distincts — mais trois conséquences pour la suite : le validateur du lot 3 doit
distinguer les trois ; la prose générée du lot 5 emploie `libelles.axe_rangement`
et dira « domaine » là où une page dit `domaines:` ; et l'entretien
d'initialisation devrait **refuser** qu'un axe transverse porte le libellé de
l'axe de rangement, comme la contrainte C7 le refuse déjà pour son **dossier**.
C7 protège le nom du dossier et pas le nom du champ : c'est la même faute, à un
champ près. **À surveiller au lot 3.**

## 6. `A1` et `A3` sont deux avertissements permanents, pas des divergences

Sept des 26 groupes de la boîte 2 sont structurellement permanents : les 5
valeurs déclarées sans page et les 2 sous-libellés déclarés sans dossier. Les
premiers attendent un arbitrage (point 3) ; les seconds sont **voulus** — le
manifeste garde le libellé d'une valeur plafonnée pour que « la promotion
reprenne d'elle-même le jour où le domaine gagne une seconde population ».

Un outil qui répète sept avertissements permanents à chaque exécution finit
ignoré. La table `VERDICTS` les tient à l'écart du bruit — ils sortent avec leur
motif — mais un vault qui vieillit en accumulera d'autres. **Recommandation pour
le lot 3 :** ces deux contrôles-là ne sont pas des règles de validation, ce sont
des lignes de **backlog** — la même distinction que `couverture_des_vues`, dont
le motif dit « créer une vue est une décision ÉDITORIALE, pas technique ». Les
sortir dans une section « backlog » séparée, plutôt que parmi les écarts.

---

# 9. Comment rejouer

```bash
uv run outils/fidelite.py
```

Chemins par défaut : `exemples/devbrain.brain.yml` et le dossier `DevBrain/`
voisin de `BrainKit/`. Sinon `--manifeste` et `--vault`. `--pages` nomme toutes
les pages de chaque groupe au lieu des six premières ; `--groupe C4` ou
`--groupe "C4/notion.Les maths, simplement"` n'imprime qu'un code ou qu'un
groupe, en entier.

L'outil rend **0** si toute divergence porte un verdict, **1** sinon.

Le manifeste du lot 1, avant les corrections de la boîte 1 :

```bash
git show bb69ebf:exemples/devbrain.brain.yml > /tmp/lot1.brain.yml
uv run outils/fidelite.py --manifeste /tmp/lot1.brain.yml
```

**DevBrain n'est ouvert qu'en lecture.** L'outil n'a aucun chemin d'écriture :
`grep -E 'write_text|write_bytes|open\(|mkdir|unlink|rmtree|rename' outils/fidelite.py`
ne rend rien. Vérifié après l'exécution sur les **25** points de travail du dépôt
— le principal plus ses 24 worktrees : `git status --porcelain` vide partout.
