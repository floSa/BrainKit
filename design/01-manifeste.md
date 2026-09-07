# BrainKit — le contrat de `brain.yml`

> Conversation 42, « BrainKit lot 1, le contrat du manifeste », le 2026-09-07.
> Spécification d'entrée : `design/00-cadrage.md` §2. **Aucun moteur, aucun
> générateur, aucun vault n'est écrit ici** — un contrat, un schéma vérifiable,
> deux remplissages complets et un contre-exemple.
>
> Livrables du lot : ce document · `schema/brain.schema.json` ·
> `schema/valider.py` · `exemples/devbrain.brain.yml` ·
> `exemples/histobrain.brain.yml` · `exemples/invalide.brain.yml`.

## Ce que ce lot a changé par rapport au cadrage

Le cadrage décrivait la **structure** de `brain.yml`. Un contrat demande autre
chose : pour chaque champ, un type, un caractère obligatoire, des valeurs légales,
une valeur par défaut, et **ce que le kit refuse**. Passer de l'un à l'autre a
forcé sept précisions que le cadrage ne portait pas, et elles sont listées en
*Ce que le schéma a forcé à préciser*. Aucun des douze points ouverts de §5 n'est
tranché ici ; chacun est cité là où il touche un champ, et le manifeste avance
avec la recommandation déjà écrite. La seule exception est
`git.identite.email`, tranchée par floSa.

---

# 1. Les trois propriétés, et ce que le contrat en fait

| Propriété du cadrage (§2.0) | Ce que le contrat en fait |
|---|---|
| **1 — Il est la seule source.** `taxonomie.md`, `tags.md`, `themes.md`, `Templates/`, la table de couleurs, la table de propagation, les guides : tous générés depuis lui. | `genere.chemins[]` est un champ, et il porte `par:` et `depuis:` — qui génère, et depuis quelle partie du manifeste. `vocabulaires.<x>.genere: true` marque un fichier de vocabulaire qui devient un dérivé. |
| **2 — Chaque valeur peut porter son motif.** | Le schéma ouvre un `patternProperties` `^(motif\|note)(_[a-z0-9_]+)?$` dans **tout** objet fermé (`$defs.annotations`). C'est la seule porte ouverte dans les objets qui refusent par ailleurs tout champ inconnu — parce que sans elle, une transcription en YAML perd huit lots de travail. |
| **3 — Il déclare des fonctions, pas seulement des mots.** | `roles[].id` est le mot du vault, `roles[].fonction` est ce que le kit lit, pris dans une liste **fermée de six**. Le schéma refuse toute autre valeur, et refuse un jeu de rôles qui ne porte pas exactement une `unite` et exactement un `hub`. |

## Les six fonctions, et leur cardinalité — vérifiée par le schéma

| `fonction:` | Ce qu'elle désigne | Cardinalité | Portée par le schéma |
|---|---|---|---|
| `unite` | Ce qu'on va chercher dans le brain. Porte l'axe de rangement, l'axe de nature, le bandeau, les liens réciproques. | **exactement 1** | `contains` + `minContains: 1` + `maxContains: 1` |
| `notion` | Ce qu'il faut comprendre. Porte l'axe de rangement, pas l'axe de nature. | 0 ou 1 | `maxContains: 1` |
| `hub` | La page d'un dossier. Ne se range pas : *elle est* le rangement. | **exactement 1** | `contains` + `minContains: 1` + `maxContains: 1` |
| `vue` | Une page qui embarque une table filtrée sur l'axe de rangement, plus une section écrite à la main. | 0 ou 1 | `maxContains: 1`, et `if fonction == vue then required [vue_embarquee, regle_de_categorie]` |
| `prescription` | Un objet transverse par construction, sans valeur d'axe de rangement, groupé par son rôle dans un dossier racine. | 0..n | — |
| `transverse` | Le hub d'une valeur d'un axe transverse. Généré, jamais écrit. | déduit de `axes.transverses` | — |

> **Pourquoi `notion` et `vue` sont plafonnés à un, alors que le cadrage ne le
> disait pas.** Les deux fonctions branchent une **ligne de la table de
> propagation** (« la notion du dossier », « la vue du dossier ») et un
> **sous-titre de la zone AUTO** des hubs. Deux rôles de fonction `notion` dans
> le même dossier rendraient ces deux dérivations ambiguës sans qu'aucune règle
> ne le signale. `prescription`, au contraire, est libre de multiplicité : DevBrain
> en a deux (`pattern`, `rule`), HistoBrain deux (`controverse`, `methode`), et
> aucune dérivation n'en dépend — leur chemin se lit sur leur propre `dossier`.

---

# 2. Structure, champ par champ

Convention de lecture : **O** = obligatoire · **F** = facultatif · **D** = a une
valeur par défaut. « Refus » dit ce que le contrat rejette, pas ce qu'il tolère.

## 2.1 `manifeste:` — la version du contrat

| Champ | Type | O/F | Valeurs légales | Refus |
|---|---|---|---|---|
| `manifeste` | entier | **O** | `1` et rien d'autre | Toute autre valeur. Le kit refuse un manifeste dont il ne connaît pas la version, **dans les deux sens** — un kit ancien devant un manifeste neuf comme l'inverse. |

## 2.2 `kit:` — la version du kit et son mode

Bloc **facultatif**. Il suit la recommandation écrite de §5.1 (générateur plutôt
que dépôt-gabarit, avec un mode de figeage) sans trancher le point.

| Champ | Type | O/F | Valeurs légales | Refus |
|---|---|---|---|---|
| `kit.version` | chaîne | O *(si `kit:`)* | `<entier>.<entier>.<entier>` | Une version non sémantique. |
| `kit.mode` | énum | O *(si `kit:`)* | `branche` \| `fige` | Toute autre valeur. `branche` : le code vit dans le kit. `fige` : le code a été copié dans `AI/scripts/`, la dépendance est coupée, et **l'instance ne recevra plus de correctif** — le manifeste doit l'écrire. |

## 2.3 `brain:` — l'en-tête

| Champ | Type | O/F | Valeurs légales | Refus |
|---|---|---|---|---|
| `brain.nom` | chaîne non vide | **O** | — | Vide. |
| `brain.sujet` | chaîne non vide, une phrase | **O** | — | Vide. **Jamais reformulée en mieux** : la phrase de l'utilisateur est la bonne (entretien 0.1). |
| `brain.langue` | énum | **O** | `fr` seul | Tout autre code. §5.4 : c'est une **limite écrite**, pas un oubli. Ne pas s'engager sur `en` avant que deux instances françaises tournent. |
| `brain.volume_cible` | entier ≥ 1 | **O** | — | Absent. C'est de là **que le seuil de promotion se dérive**, jamais d'une valeur tapée à la main : l'entretien demande le volume (2.6), jamais le seuil, que l'utilisateur n'a aucun moyen de connaître. |
| `brain.usage` | énum | **O** | `perso` \| `pro` \| `client` | Toute autre valeur. Décide la **polarité** du garde-fou d'identité git, et si le vault peut contenir de la donnée client. |
| `brain.profil` | énum | F, **D** = `obsidian` | `obsidian` \| `nu` | §5.5, recommandation écrite, point non tranché. En `nu` : pas de `.base`, donc un rôle `fonction: vue` rend un tableau markdown généré au lieu d'une vue vivante. **Le bandeau survit au profil nu** — c'est du markdown pur, et c'est lui qui porte l'essentiel du confort de lecture. |
| `brain.proprietaire.nom` | chaîne non vide | **O** | — | Vide. Sert la frontière `protege:`. |

## 2.4 `git:` — l'identité et ses garde-fous

| Champ | Type | O/F | Valeurs légales | Refus |
|---|---|---|---|---|
| `git.identite.name` | chaîne non vide | **O** | — | Vide. Posée en config **locale** du dépôt. |
| `git.identite.email` | chaîne | **O** | une adresse (`…@….…`) | Vide, ou sans `@`. **Jamais lue depuis l'annonce du harnais.** L'entretien s'arrête si la réponse ne vient pas (refus n° 1 de §3.5) — c'est le seul endroit du kit où une réponse manquante interrompt la conduite. |
| `git.domaines_refuses` | liste de chaînes | **O** *(peut être vide)* | — | Absente. Une liste vide est légale et signifie « aucun domaine interdit » ; l'absence du champ signifierait « la question n'a pas été posée », ce que le contrat refuse. |
| `git.trailers_refuses` | liste de chaînes | **O** | — | Absente. Par convention `[Co-Authored-By]`. |
| `git.branche_principale` | chaîne non vide | **O** | — | Vide. |

> **Point tranché par floSa, et le seul du lot :** `git.identite.email` vaut
> `florian_horellou@laposte.net`. Ce qui reste ouvert est en *Remontées*, point 12 :
> l'historique de DevBrain ne porte pas **une** adresse mais **trois**.

## 2.5 `libelles:` — le vocabulaire visible

Une entrée par mot que la prose générée doit employer, chacune au singulier
(`s`) et au pluriel (`p`). C'est le **seul endroit de BrainKit où le mot
« brique » existe**.

| Clé | O/F | Ce qu'elle nomme |
|---|---|---|
| `libelles.unite` | **O** | l'unité |
| `libelles.hub` | **O** | le hub |
| `libelles.axe_rangement` | **O** | ce que les paquets **sont** (« domaine », « période », « client », « discipline ») |
| `libelles.notion` | F | la notion, si un rôle en porte la fonction |
| `libelles.vue` | F | la vue |
| `libelles.prescription` | F | les prescriptions, en collectif |
| `libelles.axe_nature` | F | ce que les natures **sont** |
| `libelles.axe_transverse.<champ>` | F | un libellé par axe transverse |

Refus : une entrée sans `s` **ou** sans `p` ; une clé hors de cette liste.

> **`libelles.prescription` et `libelles.axe_transverse` n'existent pas dans le
> cadrage.** Les deux ont été ajoutés parce que la prose générée en a besoin : un
> guide qui dit « les prescriptions de ce brain » et un hub transverse dont le
> sous-titre doit s'écrire au pluriel du bon mot. Sans eux, le générateur
> retomberait sur un mot du kit — c'est-à-dire un mot de dev. Cf. *Ce que le
> schéma a forcé à préciser*, point 7.

## 2.6 `roles[]` — une entrée par nature de page

| Champ | Type | O/F | Valeurs légales | Refus |
|---|---|---|---|---|
| `id` | identifiant `^[a-z][a-z0-9-]*$` | **O** | — | Majuscule, espace, accent. C'est la valeur littérale de `role:` dans le frontmatter. |
| `fonction` | énum **fermée** | **O** | les six de §1 | **REFUS 1.** Toute autre valeur, `id` compris : `chronologie` est un `id:` légitime, ce n'est pas une `fonction:`. |
| `libelle` | `{s, p}` | **O** | — | Manquant. Alimente la prose et les titres de la zone AUTO d'un hub. |
| `range_par` | énum | **O** | `axe` \| `role` | Toute autre valeur. `axe` : le chemin se dérive de l'axe de rangement. `role` : le dossier est celui du rôle, à la racine. |
| `dossier` | chaîne non vide | **O si `range_par: role`** | — | **Absent quand `range_par: role`** — un rôle groupé par son rôle vit dans un dossier qu'il faut nommer. |
| `prefixe_nom` | chaîne | F | — | — |
| `protege` | booléen | F, **D** = `false` | — | `true` → création libre, **modification sur demande explicite**. Ne se pose jamais par défaut, ni ne se refuse (entretien 1.4). |
| `pese_sur_le_seuil` | booléen | F, **D** = `true` | — | `false` reproduit « un comparatif n'est pas un membre du comparatif ». |
| `apparait_dans_le_hub` | booléen | F, **D** = `true` | — | Alimente la règle 3. |
| `porte_categorie` | booléen | F, **D** = `true` | — | `false` sur un hub : il ne se range pas, il *est* le rangement. |
| `couleur` | `#RRGGBB` | F | — | Toute autre forme. Une couleur de graphe par rôle. |
| `taille_avertissement` | entier ≥ 1, ou nul | F | — | 0 ou négatif. |
| `population` | entier ≥ 0 | F | — | Une **mesure**, pas une cible. N'existe que sur un manifeste d'instance peuplée. |
| `regle_de_categorie` | énum | **O si `fonction: vue`** | `majorite` \| `unique` | Absent sur une `vue`. |
| `vue_embarquee` | objet | **O si `fonction: vue`** | voir ci-dessous | Absent sur une `vue`. |
| `hub_de_ralliement` | objet | F | `{dossier, lien_retour, groupe_par?}` | `dossier` ou `lien_retour` manquant. **C'est le lien retour qui fait la grappe** : sans lui, le hub cite les membres et aucun ne le cite. |
| `champs` | objet | F | voir 2.7 | — |
| `corps` | liste | F | voir 2.8 | — |

`vue_embarquee` : `extension` (**O**, commence par `.`) · `moteur` (**O**) ·
`embed` · `tri_par` · `direction` (`asc` \| `desc`) · `genere` (booléen) ·
`colonnes_par_defaut` (liste). Le manifeste peut donner **l'ordre de colonnes par
défaut et la forme du filtre** ; il ne peut pas donner les filtres eux-mêmes —
ce sont des fichiers de contenu (cf. §4, point 1).

## 2.7 `roles[].champs` — le contrat de frontmatter

| Champ | Type | O/F | Refus |
|---|---|---|---|
| `requis` | liste unique | **O** | Doublon. Champs **non vides** attendus sur toute page du rôle. |
| `autorises` | liste unique, non vide | **O** | Vide, ou doublon. **EXACTS** : tout champ hors liste fait échouer la page. |
| `conditionnels[]` | liste de `{champ, si}` | F | **REFUS 4 — `champ` ou `si` manquant.** Un conditionnel sans `si` est un champ autorisé qui se croit conditionnel : le validateur de vault ne saurait jamais quand le **permettre**. Tout autre champ dans l'entrée est refusé. |

> **`si` est une PERMISSION, pas une OBLIGATION.** *Corrigé au lot 2, mesuré.* La
> première rédaction écrivait « quand l'**exiger** » : elle lisait la condition
> comme une obligation, et la mesure du lot 2 montre que DevBrain n'en fait rien
> de tel. `hosted:` et `scaling:` sont portés par 98 briques ; 119 briques sont
> d'une famille hébergée. Les **21** de l'écart ne portent ni l'un ni l'autre, et
> les vingt-et-une portent `os:` à la place — R16 refuse le champ **hors** des
> trois familles, il ne l'exige nulle part. Lire `si` comme une obligation aurait
> donc produit 42 fausses violations sur un vault que ses deux validateurs
> déclarent verts. Un champ qui exprimerait une **vraie** obligation
> conditionnelle n'existe pas dans le contrat, et le lot 2 ne le crée pas : cf.
> `design/02-rapport-fidelite.md`, *Remontées*, point 2.
| `deprecies` | liste unique | F | §5.11, recommandation écrite, point non tranché : autorisés, absents du gabarit généré, comptés par la passe de mesure. |

Contrainte de cohérence **C1** : tout nom cité dans `requis`, `deprecies` ou
`conditionnels[].champ` doit figurer dans `autorises`.
Contrainte **C2** : tout nom cité dans `autorises` doit être défini une fois dans
le dictionnaire `champs:`.

## 2.8 `roles[].corps[]` — le gabarit du corps

Chaque section porte un `titre` (**O**), un `niveau` (**O** : `0`, `2` ou `3`) et
un `genre` (**O**) pris dans une liste fermée de huit. **Le genre est ce qui
branche les règles.**

| `genre` | Ce que c'est | Champs qu'il ouvre | Règles branchées |
|---|---|---|---|
| `prose` | Du texte suivi. La seule section où la prose est permise. | `doctrine`, `forme` | — |
| `bandeau` | Zone AUTO générée depuis le frontmatter. | — | règle 9 |
| `decision` | Un tableau à deux colonnes, l'une positive, l'autre négative avec redirections. | `colonne_positive`, `colonne_negative` | règle 5 |
| `etiquetee` | Des puces `- <Étiquette> — <valeur>`, vocabulaire **fermé**. | `obligatoires`, `permises` | règle 7 |
| `liste_liens` | Des puces dont l'**entrée** est un wikilink, éventuellement adossées à un champ. | `champ` (peut être `null`) | règles 1, 6, 8 |
| `auto` | Zone AUTO d'un hub ou d'une vue. | `balises`, `perimetre`, `sections[]`, `groupe_par` | — |
| `libre` | Rien de contrôlé. | `ecrit_a_la_main`, `hors_zone_auto` | — |
| `conditionnelle` | N'existe **que si** une condition est remplie. | `existe_si` (**obligatoire**), `forme` | — |

Refus : un genre hors des huit · un `niveau` autre que 0, 2 ou 3 · **un
`genre: conditionnelle` sans `existe_si`** · tout champ hors de la liste ci-dessus.

Champ facultatif utile sur toute section : `titre_rendu`, quand le titre écrit
dans le manifeste et le titre rendu dans la page diffèrent par une ligature ou un
accent. `mesure` porte le nombre de pages qui portent effectivement la section —
c'est une mesure, jamais une cible.

> **`existe_si` est permis sur TOUTE section, et seulement *exigé* sur une
> `conditionnelle`.** *Corrigé au lot 2.* Le schéma l'encodait déjà ainsi
> (`if genre == conditionnelle then required: [existe_si]`, jamais
> « allowed only then ») ; c'est le tableau ci-dessus qui laissait croire que
> `existe_si` était l'apanage d'un genre. La différence est réelle et vaut d'être
> écrite : `conditionnelle` est le genre d'une section que sa condition
> **définit** — on ne sait rien d'autre d'elle ; `existe_si` sur un autre genre
> dit seulement que la section **n'est pas universelle**, sans rien changer à ce
> que son genre contrôle. Sans cette nuance, cinq sections de DevBrain étaient
> déclarées universelles alors que le manifeste portait déjà leur mesure exacte :
> `Alternatives` (324/337), `Compléments` (103/337), `Notes` (13/74), et les deux
> sections d'aiguillage d'un hub (71/74). C'est la faute de la remontée 3, sur
> cinq sections que personne n'avait comptées — et un `mesure:` qui n'égale pas la
> population du rôle **est** la déclaration qu'une condition manque. Cf.
> `design/02-rapport-fidelite.md`, boîte 1.

Contrainte **C9** : toute section nommée dans `regles[].sections` ou dans une
`regles[].severite` par section doit exister comme `titre` ou `titre_rendu` d'un
`roles[].corps[]`.

## 2.9 `axes:` — les trois familles

```yaml
axes:
  rangement:      # EXACTEMENT UN, obligatoire. C'est lui qui donne le chemin.
  nature:         # ZÉRO OU UN. Il qualifie l'unité, il ne la range pas.
  transverses: [] # ZÉRO OU PLUSIEURS. Ils traversent l'arbre. La liste peut être VIDE.
```

Refus : `rangement` absent · `transverses` absent (une liste **vide** est légale,
son absence non — la question doit avoir été posée) · une clé hors de ces trois.

### `axes.rangement`

| Champ | Type | O/F | Refus |
|---|---|---|---|
| `champ` | chaîne non vide | **O** | Vide. |
| `exclusif` | booléen | **O** | Absent. `true` si une page ne peut porter qu'une valeur. |
| `regle_de_majorite` | booléen | **O si `exclusif: false`** | Absent quand l'axe n'est pas exclusif. |
| `prefixe_transversal` | identifiant | **O si `exclusif: false`** | Absent quand l'axe n'est pas exclusif ; **ou déclaré sans exister dans `prefixes[]`** (contrainte **C6**). |
| `seuil_promotion` | entier ≥ 2 | **O** | Absent, ou < 2. |
| `motif_seuil` | chaîne | **O** | **Absent.** Le seuil se **dérive** du volume cible : le calcul s'écrit, il ne se suppose pas. C'est la seule annotation que le contrat rend obligatoire. |
| `plafond_promotion` | booléen | **O** | Absent. `true` = un fils qui redoublerait son parent ne se promeut pas. |
| `niveaux` | énum `1` \| `2` | F, **D** = `2` | — |
| `valeur_courte_autorisee` | booléen | F, **D** = `false` | `true` si le préfixe seul est une valeur légale de l'axe. Cf. *Ce que le schéma a forcé à préciser*, point 3. |
| `prefixes[]` | liste non vide | **O** | Vide. |
| `rattachements` | table | F | Un préfixe qui n'est pas une valeur de l'axe et qu'une décision **explicite, nommée et datée** range quand même dans l'arbre. |
| `arbre_de_decision[]` | liste ≥ 2 | **O** | Moins de deux questions. |
| `departages[]` | liste | **O** *(peut être vide)* | Absente. **Naît vide** dans un brain neuf : le mécanisme à transposer est la **place** où ces arbitrages s'écrivent, pas leur contenu. |
| `frontieres[]` | liste | **O** *(peut être vide)* | Absente, pour la même raison. |

`prefixes[].*` : `cle` (**O**, identifiant) · `dossier` (**O**) · `sous`
(**O**, table pouvant être vide) · `portee` · `rattachement_de` · annotations.
`sous.<cle>` : `libelle` · `frontiere` · `portee` · annotations. **L'absence de
`libelle` n'est pas un oubli** : c'est ce qui fait échouer la dérivation plutôt
qu'inventer un nom de dossier le jour où la valeur franchit le seuil.

`arbre_de_decision[]` : `n` (**O**) · `question` (**O**) · `si_oui` (**O**, liste
ou chaîne) · `arret` · `defaut` · annotations. **L'ordre est strict, la première
réponse positive gagne.** L'ordre est *la* décision de conception : l'IA peut
proposer les questions, jamais leur rang.

`departages[]` : `n` (**O**) · `regle` (**O**) · `cas` · annotations.
`frontieres[]` : `entre` (**O**, chaîne) · `et` (**O**, liste non vide) ·
`distinction` (**O**) · annotations.

### `axes.nature`

Même forme, **sans** `seuil_promotion` ni `plafond_promotion`.

| Champ | Type | O/F | Refus |
|---|---|---|---|
| `champ` | chaîne non vide | **O** | Vide. |
| `porte_par` | liste non vide d'`id` de rôle | **O** | Vide, ou un `id` non déclaré (contrainte **C8**). |
| `interdit_sur` | liste d'`id` de rôle | F | Un `id` non déclaré. |
| `vide_autorise` | booléen | **O** | Absent. *Un champ vide est le **seul** signal prévu pour « l'arbre n'a pas tranché » ; une valeur inventée est une faute, un champ vide est une question ouverte.* |
| `valeurs[]` | liste non vide de `{cle, definition, frontiere?}` | **O** | Une valeur sans `definition`. |
| `arbre_de_decision[]` | liste ≥ 2 | **O** | Moins de deux questions. |
| `departages[]` | liste | **O** *(peut être vide)* | Absente. |
| `frontieres[]` | liste | F | — |

### `axes.transverses[]`

| Champ | Type | O/F | Refus |
|---|---|---|---|
| `champ` | chaîne non vide | **O** | Vide. |
| `dossier` | chaîne non vide | **O** | Vide · **le nom du pluriel de l'axe de rangement** · un nom déjà pris par un dossier de rôle, un hub de ralliement, un préfixe ou un autre axe transverse (contrainte **C7**). |
| `multivalue` | booléen | **O** | Absent. |
| `hub_par_valeur` | booléen | F, **D** = `true` | — |
| `valeurs[]` | liste non vide de `{cle, libelle, couvre?}` | **O** | Une valeur sans `libelle`. |

## 2.10 `champs:` — le dictionnaire, une fois

Table dont les clés matchent `^[a-z][a-z0-9_]*$`. Chaque champ cité dans un rôle
y est défini **une seule fois**.

| Clé | Type | O/F | Refus |
|---|---|---|---|
| `type` | énum | **O** | Hors de `ligne`, `texte`, `liste`, `enum`, `liste_enum`, `liens`, `url`, `bool`, `date`. |
| `source` | chaîne | **O si `type` ∈ {`enum`, `liste_enum`} et pas de `valeurs`** | Une `source` **et** des `valeurs` à la fois, ou ni l'une ni l'autre sur un champ énuméré. **Une `source` qui ne résout vers aucun axe ni vocabulaire déclaré** (contrainte **C3**). |
| `valeurs` | liste unique non vide | **O si `type` énuméré et pas de `source`** | Même refus, symétrique. |
| `fonction` | énum | F, **D** = `aucune` | Hors de `resume_court`, `identite`, `alias`, `aucune`. **Au plus un champ** du manifeste porte `resume_court` (contrainte **C10**). |
| `reciproque` | `null`, `{mode: symetrique}` ou `{mode: inverse, champ: <autre>}` | F | Un `mode` inconnu · un `inverse` **sans** `champ` · un `inverse` dont la cible ne déclare pas l'inverse en retour (contrainte **C5**). |
| `section` | chaîne ou `null` | F | — |
| `reinjecte_dans` | liste | F | — |
| `eliminatoire` | liste unique | F | Déclaré sur un champ non énuméré · **une valeur absente de l'énumération du champ** (contrainte **C4**). **Aucune valeur par défaut, jamais** : le kit ne doit avoir aucune intuition sur « quelle valeur d'énumération disqualifie ». |
| `deprecated` | booléen | F | — |
| `unicite` | énum `stricte` \| `souple` | F | — |
| `exemption` | chaîne | F | — |

> **Le mode `inverse` n'existe pas dans DevBrain**, et c'est la seule rupture du
> test à blanc qui exige une ligne de code que DevBrain n'aurait jamais fait
> écrire. « A prolonge B » n'implique pas « B prolonge A » : il implique « B est
> **prolongé par** A ». La relation demande une **paire** de champs, pas un
> miroir — et le contrat refuse une paire mal déclarée, sinon on remplace un trou
> par un autre.

## 2.11 `bandeau:` — le haut de page

| Champ | Type | O/F | Refus |
|---|---|---|---|
| `porte_par` | liste non vide d'`id` de rôle | **O** | Vide, ou un `id` non déclaré. |
| `vide` | chaîne non vide | **O** | Vide. Le caractère affiché quand la source manque. |
| `colonnes[]` | liste de 1 à **5** | **O** | Vide, ou **plus de cinq**. Le bandeau existe *parce que* dix-huit propriétés poussaient le texte sous la ligne de flottaison. |
| `balises`, `position`, `porte_le_resume`, `regle_dure`, `echappement` | — | F | — |

`colonnes[].*` : `titre` (**O**) · `source` (**O**) · `qualifie_par` ·
`table` · `exception_qualification` · `depend_de` · annotations.

**Une colonne dont la source n'est pas un champ déclaré est une erreur de
manifeste, pas une colonne vide** (contrainte C2). Et toute clé d'une `table`
doit être une valeur déclarée de l'énumération que la colonne lit (contrainte
**C4** — c'est le sixième refus).

## 2.12 `regles:` — les dix, activables, avec leur mesure

Liste de **exactement dix** entrées, une par `id` de la liste fermée du kit :
`reciprocite`, `chemin_categorie`, `completude_du_hub`, `voisinage_declare`,
`redirection_sourcee`, `reinjection_du_resume`, `etiquettes_fermees`,
`citation_unique`, `bandeau_a_jour`, `anti_repetition`.

| Champ | Type | O/F | Refus |
|---|---|---|---|
| `id` | énum fermée | **O** | Un `id` hors des dix. **La liste des dix est fermée par le kit** : le manifeste les *branche*, il ne les décrit pas. |
| `active` | booléen | **O** | Absent. |
| `severite` | `dure` \| `avertissement` \| `a_mesurer`, **ou** une table `{section: sévérité}` | **O** | Toute autre valeur. `a_mesurer` est la **valeur par défaut de toute instance neuve, et la seule que l'entretien sait écrire**. |
| `motif` | chaîne | **O si `severite: avertissement`** | **Absent quand la sévérité est un avertissement.** §5.6 : le kit refuse un avertissement sans motif écrit. |
| `mesure` | un objet `{date, population, violations…}`, une table de tels objets, ou une liste | F | — |
| `enonce`, `code`, `champ`, `champs`, `modes`, `roles`, `sections`, `colonne`, `marqueur`, `condition`, `champ_resume`, `normalisation`, `definition_de_liste`, `definitif`, `reecrite`, `scriptable`, `structurellement_dure`, `sortie`, `complication`, `motifs_bornes` | — | F | Les paramètres propres à chaque règle. |

> **Aucune sévérité n'est portable.** `dure` et `avertissement` sont des
> **résultats de mesure** sur un corpus, pas des propriétés de règle. Une instance
> neuve reçoit **toutes** les règles en `a_mesurer` et les durcit après avoir
> compté. §5.6 recommande deux exceptions — `chemin_categorie` et
> `bandeau_a_jour`, où une violation est une incohérence de **structure** et non
> un défaut de rédaction — et le point n'est **pas tranché** : le contrat les
> **permet** (`severite` accepte `dure` sur n'importe quelle règle) et
> `structurellement_dure: true` les **signale**, sans les imposer.
> `histobrain.brain.yml` les sort donc en `a_mesurer`, comme les huit autres.

`regles_de_socle[]` est une liste **facultative** et **ouverte** : les règles hors
des dix, que le vault a exigées. `id` (**O**, `^[a-z][a-z0-9_]*$`) · `severite`
(**O**) · `enonce` (**O**) · `code` · `depuis` · `mesure` · annotations.

## 2.13 Le reste

| Bloc | O/F | Contenu | Refus notable |
|---|---|---|---|
| `seuils` | F | `vue_min_valeurs_axe`, `vue_min_membres` | Entier < 1. |
| `vocabulaires.<nom>` | F | `fichier` (**O**), `mode` (**O** : `ferme` \| `propose` \| `libre`), `regle`, `lecture`, `porte`, `genere`, `vide` | Un `mode` hors des trois. |
| `graphe` | F | `ordre[]` (**O**, non vide) de `{requete, couleur, rgb?}` | Une couleur qui n'est pas `#RRGGBB`. **L'ordre compte** : une requête `path:` passe avant une requête `role:`, sinon un hub spécial prend la couleur des hubs ordinaires. |
| `genere` | F | `chemins[]` (**O**) de `{chemin, par, depuis?, balises?}`, plus `contrat`, `non_pages`, `index`, `liens` | Une entrée sans `par`. |
| `propagation` | F | `enonce` (**O**), `clause` (**O**), `derivee` (`true` seulement), `table[]` (**O**) de `{n, cible, trouve_par, par}`, `hubs_transverses[]` | Un `n` qui ne matche pas `^P[0-9]+$`. |
| `skills` | F | `capture` (**O**), `cloture` (**O**), `exploitation` | Un skill sans `nom`. Mieux vaut **deux skills que trois dont un inventé** : sans réponse à la question 10.1, `exploitation` n'est pas généré. |
| `agent` | F | `racine` (**O**), `sous[]` (**O**) de `{chemin, role}`, `hook_stop` | Une entrée sans `role`. |
| `frontieres_d_ecriture` | F | `libre`, `sur_confirmation`, `sur_demande_explicite`, `jamais_a_la_main`, `jamais_sans_accord`, `deplacement`, `second_mode` | — |

---

# 3. Les six refus, et où chacun vit

| # | Refus | Porté par | Message |
|---|---|---|---|
| 1 | Une `fonction:` hors de la liste fermée de six | JSON Schema, `$defs.fonction` | `roles[2].fonction : … 'chronologie' is not one of ['unite','notion','hub','vue','prescription','transverse']` |
| 2 | L'absence d'**exactement un** rôle de fonction `unite` | JSON Schema, `contains` + `minContains: 1` + `maxContains: 1` | `roles : REFUS 2 — … \| il en existe plusieurs` |
| 3 | L'absence d'**exactement un** rôle de fonction `hub` | idem | `roles : REFUS 3 — … \| il n en existe aucun` |
| 4 | Un champ conditionnel sans condition | JSON Schema, `required: [champ, si]` | `roles[0].champs.conditionnels[0] : … 'si' is a required property` |
| 5 | Une version de manifeste inconnue | JSON Schema, `enum: [1]` | `manifeste : … 7 is not one of [1]` |
| 6 | Une valeur d'énumération absente de la déclaration de son axe | **contrainte de cohérence C4** | `bandeau.colonnes[0].table.brochure : C4 — 'brochure' n est pas une valeur declaree de 'matiere'` |

## Pourquoi le sixième n'est pas dans le schéma, et pourquoi ce n'est pas un contournement

Le refus 6 est **intra-document** : il compare une valeur écrite quelque part à
une liste déclarée ailleurs **dans le même fichier**. JSON Schema n'a aucun
moyen de le faire. L'extension qui le permettrait, `$data`, est hors norme et
n'est pas implémentée par la bibliothèque de référence Python. Le contrat aurait
pu contourner en dupliquant les énumérations à chaque point d'usage — mais
dupliquer une énumération pour satisfaire un vérificateur est exactement le
défaut que le manifeste existe pour supprimer (motif E4 : deux sources décrivant
la même chose, dont l'une prend du retard).

Le refus vit donc dans `schema/valider.py`, avec neuf autres du même genre, et
c'est la reconduction exacte de la leçon du cadrage §2.3 point 2 : **le manifeste
branche les règles, il ne les décrit pas ; le kit garde du code par règle.**

## Les dix contraintes de cohérence

| # | Ce qu'elle vérifie | Ce qu'elle nomme |
|---|---|---|
| C1 | Tout champ `requis`, `deprecies` ou conditionnel figure dans `autorises` | `roles[i].champs.requis[j]` |
| C2 | Tout champ nommé (dans `autorises`, dans une section `liste_liens`, dans une colonne de bandeau) est défini dans `champs:` | `bandeau.colonnes[j].source` |
| C3 | La `source` d'un champ énuméré résout vers un axe ou un vocabulaire déclaré | `champs.<x>.source` |
| **C4** | **Toute valeur d'énumération écrite appartient à la déclaration de son axe** — clés de `table`, `depend_de.familles`, `eliminatoire` | `bandeau.colonnes[j].table.<clé>` |
| C5 | Une paire `reciproque: inverse` pointe dans les **deux** sens | `champs.<x>.reciproque.champ` |
| C6 | Un axe non exclusif déclare un `prefixe_transversal` qui **existe** | `axes.rangement.prefixe_transversal` |
| C7 | Aucun dossier d'axe transverse ne redouble le pluriel de l'axe de rangement, ni un autre dossier déjà pris | `axes.transverses[i].dossier` |
| C8 | Tout rôle nommé dans `porte_par`, `interdit_sur`, `bandeau.porte_par`, `regles[].roles` est déclaré | `axes.nature.porte_par[k]` |
| C9 | Toute section nommée dans une règle existe dans un corps de rôle | `regles[i].sections[k]` |
| C10 | Au plus un champ porte `fonction: resume_court`, et la règle 6 active le cite | `regles[i].champ_resume` |

Contrôle négatif exécuté : trois fautes de cohérence injectées dans une copie de
`histobrain.brain.yml` (un requis hors de `autorises`, une colonne de bandeau sur
un champ inexistant, une paire inverse cassée) sont sorties nommées, une par
ligne, par C1, C2 et C5. Le schéma seul les laissait passer.

---

# 4. Ce que le manifeste ne sait toujours PAS redire

Les six points de §2.3 tiennent, et le contrat en confirme cinq. Le sixième a
changé de forme.

| # | Ce qui ne rentre pas | Conséquence, confirmée par le contrat |
|---|---|---|
| 1 | **Les 47 filtres `.base`.** Chacun est une requête réglée à la main, souvent avec une seconde vue métier. | Les vues restent des **fichiers de contenu**. `vue_embarquee.genere: false` le déclare explicitement, et `colonnes_par_defaut` est tout ce que le manifeste donne. Le générateur en **amorce** un par dossier promu, il ne les tient pas. |
| 2 | **L'algorithme de la règle 5.** La conjonction « il y a une flèche » × « la cible est fichée » est du code. | La liste des dix règles est **fermée** par le schéma (`minItems: 10`, `maxItems: 10`, `id` en énumération). Le manifeste porte la section, la colonne, le marqueur et la condition en clair — pas l'algorithme. |
| 3 | **Le corps écrit à la main des hubs.** | Par conception. `ecrit_a_la_main: true` marque la place ; le générateur la pose vide. |
| 4 | **Le raisonnement derrière un arbitrage**, quand il fait plus d'une phrase. | `AI/migration/lot-N.md` reste le lieu du raisonnement, et `agent.sous[]` le déclare comme tel. **Le journal de lot n'est pas remplaçable par de la configuration.** Voir cependant la nuance ci-dessous : c'est le point qui a le plus bougé. |
| 5 | **L'ordre historique.** Le manifeste décrit un **état**, pas un chemin. | Confirmé. Ce qui se transpose est la **règle** qui a produit l'historique, pas l'historique : `axes.rangement.regle_de_retrait` porte « une valeur est retirée dès qu'aucune page ne la porte », qui est générique. |
| 6 | **`os:` et `domaines:` sur une brique sont des vestiges.** §5.11 proposait `deprecated: true` sur un champ. | Le contrat montre que la recommandation est **mal placée** : `domaines:` est *requis* sur une notion et vestigial sur une brique seulement. Le vestige est porté par le **rôle**, d'où `roles[].champs.deprecies[]`. `champs.<x>.deprecated` reste déclaré pour un champ vestigial partout. Cf. *Remontées*, point 8. |

## Le point 4, précisé : ce qu'un `motif:` porte, et ce qu'il ne porte pas

La transcription des 47 sous-libellés a mis ce point à l'épreuve, et il tient —
mais pas là où le cadrage le plaçait. Un `motif:` porte **une phrase, la raison
d'un choix** (« « RAG » est le nom de fichier d'une notion du dossier »). Ce qui
ne rentre pas n'est pas la longueur, c'est la **nature** : le motif dit *pourquoi
cette valeur*, jamais *quelles mesures ont été faites avant de la choisir*.

Un cas nouveau est apparu, et il n'est pas dans §2.3 : les **définitions de
frontière** de `taxonomie.md`. Une trentaine de sous-domaines y portent un
paragraphe qui trace leur frontière avec deux ou trois voisins — c'est le gros du
document, et c'est du contenu de gouvernance, ni un motif ni de la prose de
lecteur. Le contrat leur a ouvert un champ, `sous.<cle>.frontiere`, distinct de
`motif`. Sans lui, `taxonomie.md` ne pourrait pas être **généré** depuis le
manifeste sans perdre l'essentiel de sa substance — et il redeviendrait une
seconde source, ce que la propriété 1 interdit.

---

# 5. Ce que le schéma a forcé à préciser dans le cadrage

Sept points. Aucun n'est une correction du cadrage : ce sont des choses qu'un
document de structure peut laisser implicites et qu'un contrat ne peut pas.

1. **Les dates doivent être écrites entre guillemets.** YAML lit `2026-09-06`
   comme un objet date, qui n'existe pas en JSON — aucun JSON Schema ne peut le
   valider. Un manifeste doit être **représentable en JSON** pour être
   vérifiable : les treize dates de `devbrain.brain.yml` sont donc quotées.
2. **`genere:` ne peut pas être à la fois une liste et une table.** Les deux
   remplissages du cadrage l'écrivent comme une séquence de chemins **puis** des
   clés nommées, ce qui n'est pas du YAML. Le contrat pose `genere.chemins[]`
   pour la séquence, et les clés nommées à côté.
3. **`valeur_courte_autorisee` sur l'axe de rangement.** Dans DevBrain,
   `categorie:` est **toujours** `prefixe/sous` — le chargeur de vocabulaire ne
   construit que des paires, et aucune valeur nue n'est légale. Ni §2.2 ni §2.4
   ne le disaient, et HistoBrain a quatre périodes sur huit sans division interne :
   une source de la Préhistoire porte `categorie: prehistoire`, tout court. Le
   champ rend la différence explicite plutôt que de forcer une sous-valeur
   inventée — ce qui serait exactement le refus n° 3 de l'entretien.
4. **`notion` et `vue` sont plafonnées à un rôle.** Le cadrage écrivait
   « non » pour la cardinalité de `notion` et `vue`, sans plafond. Deux rôles de
   même fonction rendraient ambiguës la table de propagation et les sous-titres de
   zone AUTO qui s'en dérivent. Le schéma pose `maxContains: 1`.
5. **`motif_seuil` est obligatoire.** Le cadrage en fait un champ comme un autre.
   Le contrat le rend requis : le seuil se **dérive** du volume cible, et un seuil
   sans calcul écrit est un seuil tapé à la main — ce que le refus n° 4 de
   l'entretien interdit. C'est la seule annotation que le contrat exige.
6. **`departages` et `frontieres` sont obligatoires, et peuvent être vides.** La
   différence compte : une liste vide dit « la question a été posée, la réponse est
   *rien pour l'instant* » ; un champ absent dit « la question n'a pas été posée ».
   Même raisonnement sur `axes.transverses` et `git.domaines_refuses`.
7. **`libelles` a besoin de deux entrées de plus.** `prescription` et
   `axe_transverse.<champ>` n'existent pas dans le cadrage, et la prose générée en
   a besoin : sans elles, un guide qui parle des prescriptions du brain ou le
   sous-titre d'un hub transverse retombent sur un mot du kit, c'est-à-dire un mot
   de dev. C'est précisément le risque de §5.3 — le nom de l'unité qui fuit — sur
   deux mots que §5.3 ne nommait pas.

---

# 6. La complétude du remplissage DevBrain, chiffrée

Tout est mesuré sur le vault en lecture seule, le 2026-09-07. **Un compte qui ne
colle pas est une remontée, pas un arrondi** — les écarts sont en §7.

| Ce qui est transcrit | Manifeste | Vault | Source du compte |
|---|---|---|---|
| Préfixes de l'axe de rangement | **20** | **20** | `arbo.DOM_LABEL` |
| Rattachements de préfixe | **1** (`skill`) | **1** | `arbo.DOM_RATTACHE` |
| Sous-libellés déclarés | **47** | **47** | `arbo.SUB_LABEL` |
| … dont promus en dossier | **45** | **45** | `arbo.promotions()` sur la population réelle ; 2 bloqués par le plafond |
| Valeurs de `categorie:` déclarées | **109** | **109** | 103 dans le bloc ` ```domaine ` + 6 dans le fence nu `skill/*` |
| … dont portées par ≥ 1 page | — | **104** | balayage des 765 pages |
| Valeurs de `famille:` | **9** | **9** | bloc ` ```famille ` |
| Arbres de décision | **2** | **2** | `D1→D14` (14 questions) et `F1→F9` (9 questions) — 23 questions transcrites |
| Règles de départage | **13** | **13** | 7 pour le domaine (`D-R1..D-R7`), 6 pour la famille (`R1..R6`, renommées `F-R1..F-R6`) |
| Frontières disputées | **8** | **8** | section *Frontières disputées* de `taxonomie.md` |
| `frontiere:` sur une sous-valeur de l'axe de rangement | **58** | — | section *Sous-domaines qui prêtent à confusion* de `taxonomie.md` |
| `frontiere:` sur une valeur de l'axe de nature | **9** | **9** | table *Les 9 valeurs, définition et frontière* |
| `motif:` sur une sous-valeur de l'axe de rangement | **25** | — | les commentaires d'arbitrage de `SUB_LABEL` (tous les libellés qui s'écartent de leur clé, chacun pour une raison mesurée) plus les mentions « ouvert / élargi au lot 4 » de `taxonomie.md`. **C'est la propriété 2 du manifeste** : une transcription qui perd ces commentaires perd huit lots de travail |
| Annotations `motif` / `note` dans tout le manifeste | **104** | — | — |
| Rôles | **6** | **6** | `check_brain.ALLOWED` |
| Règles de `brain-v3.md` §10 | **10** | **10** | 7 dures, 3 en avertissement — sévérités **réelles**, avec leur mesure |
| Règles de socle transcrites | **12** | — | les règles hors des dix que le validateur porte (R2, R3, R5, R7, R8/R8e, R9, R14b, R17, R25, seuil de taille, unicité de nom, hub par niveau) |
| Champs conditionnels | **2** | **2** | `hosted:`, `scaling:`, condition `famille ∈ {plateforme, saas, application}` |
| Colonnes du bandeau | **4** | **4** | `build_bandeau.COLONNES` |
| Tables de rendu du bandeau | **5** | **5** | `NATURE` (9), `LICENCE` (4), `EXECUTION_FAMILLE` (6), `HOSTED` (3), `SCALING` (3) |
| Règles de couleur du graphe | **7** | **7** | `obsidian-graph.md`, bloc `colorGroups` — seule source, `graph.json` est gitignoré |
| Valeurs de l'axe transverse | **6** | **6** | `themes.md` |
| Champs indexés | **12** + `path` | **12** + `path` | `build_index.FIELDS` |
| Dossiers hors périmètre | **9** | **9** | `NON_PAGES` |
| Lignes de la table de propagation | **6** | **6** | `brain-v3.md` §10 |

## Le gabarit de corps, par rôle — mesuré sur les pages, pas sur `Templates/`

C'est le constat E4 pris au mot : la source de vérité du gabarit est la page, pas
le gabarit. Chaque section du manifeste porte son compte réel dans `mesure:`.

> *Complété au lot 2.* Les mesures de ce tableau sont exactes — le comparateur
> `outils/fidelite.py` a confronté les **54** comptes déclarés du manifeste au
> vault et n'en a trouvé **aucun** en écart. Ce qui manquait n'était pas un
> chiffre mais une **conséquence** : cinq des sections dont la mesure n'égale pas
> la population de leur rôle étaient déclarées universelles. Elles portent depuis
> un `existe_si` (colonne de droite, en gras).

| Rôle | Sections déclarées | Ce que la mesure donne |
|---|---|---|
| `brique` (337 pages) | **10** | bandeau 337 · Définition 337 · Prendre si / Écarter si 337 · Mise en œuvre 337 · Écosystème **333** · Alternatives **324, `existe_si`** · Compléments **103, `existe_si`** · Ressources 337 · Voir aussi 337 · Retours **0** |
| `notion` (297) | **6** | Aperçu 297 · Concepts clés 297 · Les maths, simplement **282** · En pratique 297 · Approches voisines & alternatives 297 · Pour aller plus loin 297 |
| `comparatif` (47) | **4** | accroche · embed · Ce qui départage 47 · Voir aussi 47 |
| `hub` (74) | **4** + **6** sous-sections AUTO | Ce qu'il faut comprendre **71, `existe_si`** · Choisir **71, `existe_si`** · zone AUTO (**trois formes**, cf. ci-dessous) · Notes **13, `existe_si`** · sous-sections : Sous-domaines 10, Notions 39, Briques 58, Patterns 1, Rules 1, Comparatifs 37 |
| `pattern` (5) | **5** | Contexte · Stack · Décisions clés · Pièges · Voir aussi — les 5 sur 5 |
| `rule` (5) | **9** | Principe · MUST · SHOULD · NICE-TO-HAVE · Exemples · Bon · Mauvais · Exceptions · Voir aussi — les 5 sur 5 |
| **Total** | **38** sections | plus 6 sous-sections de zone AUTO |

> **La zone AUTO d'un hub a trois formes, et le manifeste n'en déclarait qu'une.**
> *Corrigé au lot 2 pour le constat, la forme reste à trancher.* Les six
> sous-sections ci-dessus décrivent un hub d'**arbre** (67 pages, `perimetre:
> dossier`). Le vault en a deux autres : le hub de **ralliement** (1,
> « Comparatifs », `perimetre: role`, dont les 12 sous-titres sont des libellés de
> domaine et non des sections de gabarit) et le hub **transverse** (6, `Métiers/`,
> `perimetre: champ`, sans aucune sous-section). `perimetre` énumère déjà les
> trois valeurs ; ce qui manque est de savoir si un rôle porte **plusieurs**
> gabarits de zone AUTO ou si la forme se **dérive** de `hub_par_valeur` et de
> `hub_de_ralliement`. C'est une décision de générateur : elle appartient au
> lot 4. Cf. `design/02-rapport-fidelite.md`, *Remontées*, point 1.

Étiquettes des deux sections `etiquetee`, mesurées :

- `Mise en œuvre` — les **5** étiquettes obligatoires sur **337/337** pages.
  Zéro violation, d'où la sévérité dure.
- `Ressources` — Documentation 329 · Dépôt 309 · Papier 3 · Article 1, plus
  **4 « Site » et 1 « Poids »** hors vocabulaire. Ce sont **exactement les 5
  violations** que le lot 8 a mesurées et qui maintiennent cette moitié de la
  règle 7 en avertissement.

## Le remplissage HistoBrain, chiffré

| Ce qui est écrit | Compte | Exigence du test à blanc |
|---|---|---|
| Rôles | 6, **aucun** homonyme d'un rôle DevBrain | — |
| Préfixes de l'axe de rangement | 8 | — |
| Sous-valeurs déclarées | 17 (4 périodes en portent, 4 non) | point 3 de §5 du contrat |
| Valeurs de l'axe de rangement | 21 | — |
| Questions de l'arbre de rangement | **9**, écrites en entier (§2.4 s'arrêtait à D3) | — |
| Valeurs de l'axe de nature | 9, avec définition **et** frontière | — |
| Questions de l'arbre de nature | **9**, écrites en entier (§2.4 s'arrêtait à N2) | — |
| Départages et frontières | **0 et 0** — naissent vides | principe 2 |
| Axes transverses | **2** | **exigence 3** |
| Sections de corps | 38 | — |
| Colonnes du bandeau | 4 | — |
| Règles | 10, **toutes** en `a_mesurer` | principe 1 |
| Règles de socle | 12, dont une **nouvelle** : `paire_inverse_bien_declaree` | **exigence 1** |
| Lignes de propagation | 6 + **1** (`P7`, les hubs transverses) | conséquence de l'exigence 3 |
| Mode `reciproque: inverse` | `prolonge` / `prolonge_par` | **exigence 1** |
| Axe non exclusif | `exclusif: false` + `regle_de_majorite` + `prefixe_transversal: transversal` | **exigence 2** |
| Seuil dérivé | `12`, calcul écrit : 3 000 / 8 → ~375 par période | **exigence 4** |
| Rôle protégé | `notion`, `protege: true` | **exigence 5** |

---

# 7. Remontées

Quinze points — quatorze numérotés plus un « 6 bis ». Aucun n'est corrigé — sauf trois erreurs factuelles de
`design/00-cadrage.md`, dont la correction est signalée en tête de point.

## 1. Les comptes de pages du cadrage ne collent pas au vault

*Corrigé dans `00-cadrage.md`, en tête de « Ce qui est établi », et aux quatre
autres endroits qui reprenaient l'un de ces chiffres.*

`00-cadrage.md` annonçait « 338 briques, 299 notions, 47 comparatifs, 75 hubs,
6 patterns, 6 règles ». Le balayage du 2026-09-07 donne **337 / 297 / 47 / 74 /
5 / 5**, soit **765 pages** — et c'est ce que `CLAUDE.md` du DevBrain annonce
aussi.

Les chiffres d'origine ne correspondent à **aucun** périmètre cohérent, et c'est
ce qui les rend instructifs. En comptant les 6 gabarits de `Templates/`, qui
portent un `role:` (2 `brique`, 1 `notion`, 1 `pattern`, 1 `rule`), on obtient
339 / 298 / 47 / 74 / 6 / 6. Les 6 patterns et 6 règles annoncés viennent donc de
là ; les 338 briques et 299 notions de nulle part ; et les 75 hubs d'aucun des
deux. Les gabarits ne sont pas des pages du brain : `build_bandeau.py` les exclut
explicitement, « leur frontmatter est un exemple à trous, dont le bandeau dérivé
n'aurait aucun sens ».

**Conséquence pour le lot 2 :** le rapport de fidélité doit annoncer son
**périmètre** avant ses comptes, et le périmètre est celui de `genere.non_pages`.
Un test qui compare 338 à 337 échouera pour une raison qui n'est pas la bonne.

## 2. Le titre réel de la cinquième section d'une notion n'est pas celui de la spec

`brain-v3.md` §7 et `00-cadrage.md` §2.2 écrivent tous deux
`## Approches voisines`. Les **297** notions portent
`## Approches voisines & alternatives`. C'est le constat E4 attrapé sur un titre
précis, et il est plus grave que le cas `Templates/` : ici c'est la **spec** qui
est en retard, pas un gabarit oublié. Le manifeste transcrit le titre des pages.

## 3. `## Les maths, simplement` est déclaré inconditionnel et ne l'est pas

`brain-v3.md` §7 le liste comme les cinq autres. Mesure : **282 sur 297**. Quinze
notions n'ont pas de maths à expliquer et la section n'a pas été posée vide —
c'est le bon comportement, et c'est aussi la définition de `genre:
conditionnelle`. Le manifeste la déclare conditionnelle.

## 4. Quatre briques ne portent aucune section `## Écosystème`

`imbalanced-learn`, `Obsidian`, `Ruff`, `Quarto`. Elles n'ont donc ni
`### Alternatives` ni `### Compléments`. C'est le **seul** titre de corps de
brique qui ne soit pas à 337/337. Rapporté, non corrigé (interdiction du lot 1) —
et à ne pas corriger avant le lot 9, qui est le premier autorisé à écrire.

## 5. Le hub liste ses comparatifs depuis les fichiers `.base`, pas depuis le rôle

`build_mocs.zone_hub()` remplit `### Comparatifs` avec
`dossier.glob("*.base")`. C'est la seule sous-section de zone AUTO qui ne lise
pas `role:`, et c'est un reste d'avant le lot 5 : depuis le 2026-09-06, la page
`role: comparatif` existe à côté du `.base`, et c'est elle qui devrait être
listée. Aujourd'hui le hub cite le `.base`, qui n'a pas de frontmatter — donc pas
de couleur, pas de lien sortant. Conséquence mesurable : `### Comparatifs`
apparaît sur 37 hubs, et le manifeste doit déclarer `source: "fichiers *.base du
dossier"` pour rester fidèle. **À traiter au lot 4**, pas ici.

## 6. Trois compteurs de taxonomie divergent, et aucun n'est le bon

- `00-cadrage.md` A5 et lot 1 : `SUB_LABEL` (39) → **c'est 47**. *Corrigé dans
  `00-cadrage.md`, aux trois endroits qui portent le chiffre.*
- `00-cadrage.md` F3 et lot 1 : « les 94 valeurs de `categorie:` » → il y en a
  **109** (103 sous le bloc ` ```domaine `, 6 sous le fence nu `skill/*`). *Corrigé.*
- `Documentation/general/taxonomie.md`, en-tête : « 101 valeurs ». **Non corrigé —
  hors périmètre, DevBrain est en lecture seule.**
- `AI/scripts/check_brain.py`, docstring de `load_categories` : « les 94
  domaines ». **Non corrigé, même raison.**

Le vrai enseignement n'est pas l'écart mais sa **cause** : quatre endroits
comptent la même chose et aucun n'est dérivé des autres. C'est le motif E4, sur
un chiffre au lieu d'un gabarit — et c'est exactement ce que la propriété 1 du
manifeste supprime. Le compte doit être **généré**, jamais écrit.

## 6 bis. Cinq des six valeurs de `skill/*` ne portent aucune page

Découvert en chiffrant l'écart 109 / 104. Les cinq sont nommément
`skill/code-quality`, `skill/data`, `skill/dev-flow`, `skill/documents` et
`skill/meta` ; la sixième, `skill/knowledge`, porte la page `Obsidian`, seule du
préfixe. Aucune valeur portée n'est hors vocabulaire — l'écart est donc entier de
ce côté.

Ce n'est pas un détail de comptage : la **règle de retrait** du vocabulaire, écrite
dans `taxonomie.md` et transcrite dans le manifeste
(`axes.rangement.regle_de_retrait`), dit qu'*une valeur est retirée dès que plus
aucune page ne la porte, parce que la laisser autoriserait une rechute
silencieuse*. Elle a été appliquée sans exception aux onze valeurs de `concept/*`
au lot 4, y compris à `concept/devops` qui n'avait jamais porté de page. Les cinq
`skill/*` y échappent, et rien ne dit pourquoi. **Non corrigé — DevBrain est en
lecture seule.** À trancher avec le rapport du lot 2, qui doit les lister.

## 7. `domaine:` de `role: rule` est homonyme de l'axe de rangement sans être lui

`RULE_ALLOWED` contient `domaine`, une chaîne libre. L'axe de rangement du
DevBrain s'appelle `categorie:` et son libellé est « domaine ». Deux choses
différentes portent donc le même mot, et le manifeste est le premier document qui
les met côte à côte. Aucune conséquence machine aujourd'hui — `role: rule` n'a
pas de `categorie:` — mais un validateur piloté par le manifeste devra distinguer
`champs.domaine` (le champ d'une prescription) de `libelles.axe_rangement.s` (le
mot que la prose emploie). **À surveiller au lot 3.**

## 8. `deprecated: true` sur un champ est mal placé

§5.11 recommande d'ajouter `deprecated: true` sur un **champ autorisé**. La
transcription montre que ça ne marche pas pour le cas qui a motivé la
recommandation : `domaines:` est un vestige sur une brique et un champ **requis**
sur une notion. Un drapeau posé sur le champ marquerait les deux. Le contrat
ouvre donc `roles[].champs.deprecies[]`, portée par le rôle, et garde
`champs.<x>.deprecated` pour un champ vestigial partout. **Le point 5.11 reste
ouvert** — c'est sa forme qui a bougé, pas sa décision.

## 9. Le cadrage ne dit pas si un préfixe seul est une valeur légale

Détaillé en §5 point 3. La réponse est « non dans DevBrain, oui dans HistoBrain »,
et le contrat a dû créer un champ pour la porter. Sans lui, HistoBrain aurait
inventé une sous-valeur par période sans division interne — c'est-à-dire aurait
fabriqué de la taxonomie pour satisfaire un format.

## 10. Les blocs YAML de `00-cadrage.md` §2.2 et §2.4 ne sont pas du YAML valide

Ils écrivent des scalaires bloc (`motif: >`) **à l'intérieur** de mappings *flow*
(`{ … }`), ce que la grammaire YAML interdit, et un bloc de séquence à
l'intérieur d'un mapping flow (la zone AUTO d'un hub). Aucun parseur ne les lit.
Ce sont des **illustrations** dans un document de cadrage, donc ce n'est pas une
faute — mais c'est un piège pour qui les copierait, et la conversation 42 s'y est
fait prendre en les reprenant à l'identique. **Non corrigé** dans le cadrage : les
deux remplissages complets, eux, parsent.

## 11. Les dates YAML nues rendent un manifeste invérifiable

Détaillé en §5 point 1. `date: 2026-09-06` est un objet date en YAML, qui n'existe
pas en JSON : le manifeste sort du domaine que JSON Schema sait décrire. Toute
date d'un `brain.yml` doit être une **chaîne quotée**. À écrire dans le
générateur du lot 5, sinon chaque instance générée sera invalidée par son propre
contrat.

## 12. `git.identite.email` : l'historique de DevBrain porte trois adresses, pas deux

Le point est tranché pour la valeur du manifeste — `florian_horellou@laposte.net`
— et il reste ouvert pour ce qu'il faut faire de l'historique. Comptage exact sur
`git log` de DevBrain, le 2026-09-07 :

| Adresse | Commits |
|---|---|
| `florian_horellou@laposte.net` | **222** |
| `florian.horellou@gmail.com` | **46** |
| `34608761+floSa@users.noreply.github.com` | **10** |

L'énoncé du lot annonçait « un commit venu d'une autre machine » : c'est
**46**, plus 10 signés par l'adresse de redirection GitHub. Les trois désignent
la même personne, aucune n'est l'adresse pro — le garde-fou a donc bien tenu sur
ce qu'il visait. Ce qui reste à trancher : `git.domaines_refuses` ne liste que
`aosis.net`, or deux des trois adresses présentes ne sont pas celle déclarée en
`git.identite`. Faut-il un `git.identites_tolerees` pour les distinguer d'une
fuite, ou accepter que l'historique porte plusieurs adresses d'une même personne ?
**Recommandation : accepter, et ne rien réécrire.** L'identité future est celle de
la config locale ; réécrire 56 commits pour une cosmétique coûterait tout
l'historique. À trancher avant le lot 9, qui touchera à DevBrain.

## 13. Les renvois « §4 point N » du cadrage ne résolvent pas

`00-cadrage.md` renvoie une vingtaine de fois à « §4 point 3 », « §4 point 5 »,
« §4 point 9 », « §4 point 10 ». La section 4 n'a **aucun point numéroté** : elle
a cinq ruptures numérotées, quatre transpositions et trois insuffisances, toutes
titrées et non numérotées. La correspondance est déductible (le point 9 est la
rupture 5, le point 10 est « `role: notion` protégé »), mais elle demande de
relire toute la section. **Non corrigé** — c'est une reformulation de §4, pas une
erreur factuelle, et ce lot ne réécrit pas le cadrage. À traiter si §4 est révisé.

## 14. « Les 14 arbres de décision » : il y en a deux

*Corrigé dans `00-cadrage.md`, lot 1.* L'énoncé du lot 1 et §1 F3 parlent de
« l'arbre D1→D14 » ; le périmètre du lot l'a lu comme « 14 arbres ». Il y a
**deux** arbres de décision dans `taxonomie.md` : celui du domaine (14 questions,
`D1`→`D14`) et celui de la famille (9 questions, `F1`→`F9`), soit **23 questions**
transcrites. Le manifeste porte les deux en entier.

---

# 8. Ce qui reste au lot 2

Rappel du plan, et ce que ce lot lui laisse :

- Le manifeste `devbrain.brain.yml` est le **fichier d'entrée** du test de
  fidélité. Il déclare 109 valeurs d'axe, 47 sous-libellés, 38 sections de corps
  et 6 gabarits de frontmatter : c'est ce que le rapport devra confronter aux 765
  pages, page par page.
- Les cinq écarts déjà connus sont écrits ci-dessus (points 1 à 5). Le rapport de
  fidélité doit les **retrouver**, pas les découvrir : un rapport qui ne les
  signale pas n'a pas balayé.
- Les cinq valeurs déclarées qu'aucune page ne porte (109 − 104) sont déjà
  nommées en Remontée 6 bis : `skill/code-quality`, `skill/data`,
  `skill/dev-flow`, `skill/documents`, `skill/meta`. Le lot 2 doit les retrouver
  par balayage, pas les recopier.
- Aucun des douze points de §5 n'a été tranché ici, et `git.identite.email` est
  le seul qui l'ait été par floSa.
