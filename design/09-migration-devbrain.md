# BrainKit — lot 9 : DevBrain devient une instance

> Conversation 50, « BrainKit lot 9, DevBrain devient une instance », le 2026-09-08.
> **Premier lot autorisé à écrire dans le DevBrain**, et il n'y a été autorisé que
> parce que les lots 2, 3, 4 et 8 avaient tous passé leur acceptation en lecture
> seule. Le journal côté vault — ce qu'un futur lot du DevBrain doit savoir — est
> dans `AI/migration/lot-9-brainkit.md` de ce vault. Ce document-ci dit ce que le
> lot a appris **au kit**.

## Ce que le lot a changé par rapport au cadrage

Un seul point, et c'est un arbitrage, pas une découverte : le cadrage (§6, lot 9)
écrit « remplacer l'outillage de `AI/scripts/` par le kit », ce qui se lit
naturellement comme *supprimer les scripts et taper `brainkit`*. Ce n'est **pas**
ce qui a été fait. Les sept fichiers restent, réduits à des **ponts** de vingt
lignes, pour deux raisons mesurables développées en §3.2. La formule du cadrage
n'est pas contredite — aucune ligne du kit n'est copiée dans le vault, et le
manifeste pilote tout — mais la lettre mérite d'être corrigée : le
remplacement d'un outillage par un kit passe, dans une instance qui a déjà des
habitudes, par une couche d'adaptation qu'il faut nommer et écrire.

---

# 1. L'état de départ, vérifié avant d'écrire une ligne

| Contrôle | Résultat |
|---|---|
| `git fetch origin` | aboutit |
| `git log HEAD..origin/main --oneline` | **vide** |
| `git merge-base HEAD origin/main` | `8aaa257` — et `HEAD`, `main`, `origin/main` valent tous `8aaa257` |
| `git status --porcelain` sur les **32** arbres de travail | vide sur les 32, dont le principal |
| `git config --local user.name` / `user.email` | `floSa` / l'adresse **perso** — **lue**, jamais posée |
| `git config core.hooksPath` | `.githooks` |

Aucune divergence. Le travail s'est fait sur la branche dédiée
`claude/brainkit-lot9-devbrain-8463bb`, dans son worktree ; `main` n'a pas été
touchée, et rien n'a été poussé.

Deux baselines ont été relevées **avant** toute écriture, pour que « inchangé »
soit vérifiable et pas déclaratif :

```
brainkit valider  -> 0 dure, 111 avertissements
brainkit generer --check -> 1 écart : AI/index/brain-index.json, 4 lignes
```

Ce second écart est le sujet du §4 : il existait **avant** le lot, sur un vault
que ses deux validateurs déclarent vert.

---

# 2. Le diff, fichier par fichier

```
 AI/index/brain-index.json      |    4 +-
 AI/migration/lot-9-brainkit.md |  339 ++++++
 AI/scripts/README.md           |  201 ++--
 AI/scripts/_pont_kit.py        |  133 +++
 AI/scripts/arbo.py             |  325 ++----
 AI/scripts/build_bandeau.py    |  371 +------
 AI/scripts/build_index.py      |  241 +----
 AI/scripts/build_links.py      |  188 +---
 AI/scripts/build_mocs.py       |  379 +------
 AI/scripts/check_arbo.py       |  205 ++--
 AI/scripts/check_brain.py      | 1187 +--------------------
 brain.yml                      | 2254 ++++++++++++++++++++++++++++++++++++++++
 12 files changed, 3147 insertions(+), 2680 deletions(-)
```

| Fichier | Ce que c'est | Commentaire |
|---|---|---|
| `brain.yml` | **posé** | Copie **identique à l'octet** de `exemples/devbrain.brain.yml` (sha256 vérifié). C'est le fichier que le lot 2 a passé au test de fidélité et sur lequel les lots 3, 4 et 8 ont rendu leurs verdicts. |
| `AI/scripts/_pont_kit.py` | **posé** | La résolution du kit, écrite **une** fois, lue par les six autres. §3.3. |
| `AI/scripts/check_brain.py` | 1 159 → 64 | Pont vers `brainkit valider`. |
| `AI/scripts/check_arbo.py` | 163 → 88 | Pont vers `brainkit valider`, restreint à trois règles. §3.4. |
| `AI/scripts/build_index.py` | 221 → 64 | Pont vers `generer --quoi index`. |
| `AI/scripts/build_mocs.py` | 365 → 56 | Pont vers `generer --quoi hubs`. |
| `AI/scripts/build_links.py` | 180 → 50 | Pont vers `generer --quoi liens`. |
| `AI/scripts/build_bandeau.py` | 361 → 60 | Pont vers `generer --quoi bandeau`, `--check` compris. |
| `AI/scripts/arbo.py` | 268 → 107 | Pont **bibliothèque** vers `brainkit.valider.chemins`. §3.5. |
| `AI/scripts/README.md` | réécrit | Il décrivait cinq scripts PowerShell et un hook, et ne nommait aucun des six outils qu'il documentait censément. Il dit maintenant les ponts, la résolution du kit, et sépare ce qui est du kit de ce qui est propre au vault. |
| `AI/index/brain-index.json` | 1 + / 3 − | **Le seul artefact qui bouge**, et le §4 lui est consacré. |
| `AI/migration/lot-9-brainkit.md` | posé | Le journal, à sa place habituelle dans le vault. |

**Aucun autre fichier.** La preuve, et elle est vérifiable :

```
git diff --name-only origin/main..HEAD -- '*.md' '*.base' ':(exclude)AI/**'
    -> 0 fichier

git diff --stat origin/main..HEAD -- . ':(exclude)AI/**' ':(exclude)brain.yml'
    -> aucune ligne
```

Ni les 337 briques, ni les 297 notions, ni les 47 comparatifs et leurs 47 `.base`,
ni les 74 hubs, ni les 5 patterns, ni les 5 règles, ni la gouvernance de
`Documentation/`, ni `Templates/`, ni `docs/`.

---

# 3. Les arbitrages

## 3.1 `brain.yml` est une copie, pas une variante

Le manifeste posé à la racine du vault est **identique à l'octet** à l'exemple du
kit. La tentation était d'y glisser une ligne — un `kit.racine:`, un
`signature:` mis à jour — et chacune aurait coûté la même chose : la fidélité
prouvée au lot 2 cesse d'être reproductible dès que les deux fichiers diffèrent
d'un octet, parce que plus rien ne dit lequel a été mesuré.

Deux `motif:` de l'exemple ont quand même dû changer, et le changement a été fait
**des deux côtés dans le même commit** :

- `genere.index.motif_signature` disait « le DevBrain annonce encore les siens, et
  c'est exact tant que le lot 9 n'a pas remplacé son outillage ». C'est le lot 9
  qui l'a rendu faux, et le pont qui le rend de nouveau vrai (§3.2) ;
- `agent.sous[scripts/].role` disait « vide sur une instance `kit.mode: branche` ».
  Une instance branchée porte ses ponts ; le dossier n'est pas vide.

Prose seule, aucune valeur machine touchée, les cinq manifestes du dépôt passent
toujours `schema/valider.py` et le verdict est inchangé. La remontée 4 propose de
mécaniser cette égalité, qui n'est aujourd'hui tenue que par attention.

## 3.2 Des ponts, pas la commande du kit — et pourquoi ce n'est pas de la nostalgie

C'est la décision principale du lot. Elle a deux motifs, et aucun n'est
sentimental.

**Un contrat.** `cloturer-brain`, `enrichir-brain`, `.claude/settings.json` et le
hook `Stop` nomment tous `AI/scripts/<script>.py`. Ce sont les quatre fichiers qui
pilotent l'écriture dans le vault, et ils sont lus à chaque session. Le critère
d'acceptation du lot est *aucun contenu de page modifié* ; le tenir en cassant ce
qui écrit les pages aurait été une victoire de comptable. Le pont rend les deux
vrais en même temps.

**Un octet.** `genere.index.signature` vaut `AI/scripts/build_index.py`, et cette
chaîne est **dans l'artefact versionné** — la clé `generated_by` du catalogue et
l'en-tête du document humain. Tant que le fichier lancé porte ce nom, la signature
reste exacte et les deux fichiers d'index ne bougent pas. Une bascule vers
`brainkit generer` aurait réécrit deux artefacts pour ne rien gagner.

Ce que le lot en tire, et qui vaut pour le lot 10 et pour toute instance future :
**la signature d'un artefact nomme la commande qu'un humain lance, pas le paquet
qui fait le travail.** C'est exactement pour cela qu'elle est déclarée comme une
valeur d'instance ; le lot 4 l'avait écrit sans en avoir la preuve, le lot 9 la
fournit.

## 3.3 Où vit le kit — la remontée 5 du lot 7, tranchée

Le lot 7 avait mesuré le trou : `kit.mode: branche` dit que le code est ailleurs
sans dire **où**, et ni `brainkit valider` ni `uv run brainkit valider` ne
résolvent depuis le dossier d'une instance. Deux propositions y étaient posées,
aucune tranchée. Les deux sont **écartées ici**, avec leur motif :

- **`kit.racine:` au manifeste** — ce serait un chemin absolu de poste dans un
  fichier versionné et partagé entre trois machines, et il ferait diverger
  `brain.yml` de l'exemple du kit (§3.1) ;
- **le PATH** — c'est une étape d'installation, donc du lot 10, et une étape
  d'installation qu'on oublie est un outillage qui ne tourne plus.

Ce qui est fait à la place : une résolution en trois pistes, dans
`AI/scripts/_pont_kit.py`, essayées dans l'ordre et arrêtées à la première qui
répond.

| # | Piste | Pour qui |
|---|---|---|
| 1 | `$BRAINKIT_RACINE` | l'échappatoire explicite, un kit rangé ailleurs |
| 2 | `<vault>/AI/scripts/brainkit/` | une instance **figée**, où `freeze` a copié le kit |
| 3 | `<parent>/BrainKit`, en remontant depuis la racine du vault | le cas nominal, et le cas worktree |

L'ordre porte une décision : **la piste 2 passe avant la 3**, parce qu'une
instance figée est une instance qui ne doit plus jamais lire un kit du dehors —
c'est toute sa raison d'être. Une résolution qui trouverait le kit voisin avant
le kit copié annulerait `freeze` en silence.

La piste 3 remonte **tous** les parents, et pas seulement le premier. Ce n'est pas
de la générosité : le worktree d'un agent vit trois niveaux sous la racine du
dépôt (`<vault>/.claude/worktrees/<nom>/`), et c'est là que tout le travail de ce
lot s'est fait. Une résolution qui ne regarderait que `../BrainKit` aurait été
inutilisable exactement là où on en avait besoin.

Aucune piste ne répond : les ponts **sortent en 2** et impriment les trois. Ils ne
devinent pas — un kit deviné est un verdict rendu par un code qu'on n'a pas
choisi, et c'est le même raisonnement que `defauts.py` applique au manifeste.

## 3.4 Deux entrées de validation pour un seul validateur

Le kit a fusionné `check_brain` et `check_arbo`. Les deux entrées du vault
survivent, et `check_arbo.py` **restreint** le verdict à trois règles :
`chemin_categorie`, `hub_par_niveau`, `frontmatter_lisible` — exactement les
quatre contrôles de l'ancien script, le seuil étant porté par la dérivation de la
première.

Le motif est dans `cloturer-brain` : *ne lancer que `check_brain` et croire le
vault validé* y est un anti-pattern écrit. Un verdict de 111 avertissements où
l'on cherche à l'œil les trois lignes de structure n'est pas le même outil qu'un
verdict de structure. Fusionner les moteurs est un progrès ; fusionner les
**questions** en aurait été un déguisé.

Ce qui est perdu, et qui est écrit dans le pont : l'ancien script proposait le
`git mv` en toutes lettres. Le kit nomme le dossier attendu — même information,
autre phrase. Ce n'est pas rattrapé ici, parce que rattraper une phrase de sortie
aurait demandé de toucher le kit pour une instance.

## 3.5 `arbo.py` reste une bibliothèque, avec la même API

`enrichir-brain` ne lance pas `arbo.py` : il l'**importe**, et appelle
`domaine()`, `promotions(categories)` et `dossier_attendu(categorie, promus)`.
Le kit, lui, compte le seuil sur des **pages** et non sur des chaînes — il doit
pouvoir écarter un rôle hors seuil et résoudre la valeur dominante d'un axe non
exclusif (rupture 3).

Le pont porte donc un adaptateur de huit lignes : chaque catégorie devient une
page du rôle d'unité, celui qui pèse. Il n'invente rien, et la vérification est
la seule qui compte :

```
SEUIL                          5 = 5
promotions identiques          True — 45 promus
dossiers attendus différents   0 / 765
```

Une différence de vocabulaire, sans conséquence mesurée : `ROLES_SANS_CATEGORIE`
et `ROLES_HORS_SEUIL` sont désormais **dérivés du manifeste** et contiennent donc
`hub`, que l'ancien code écartait par un `if` séparé. C'est plus juste, et aucun
consommateur ne s'en sert autrement.

**Enseignement pour le kit :** l'API que le lot 7 expose aux skills est une
surface publique au même titre que la CLI. `chemins.promotions(pages, mo)` est la
bonne signature *pour le kit* et la mauvaise *pour un appelant qui n'a que des
valeurs d'axe*. Une fonction `promotions_depuis_valeurs(valeurs, mo)` dans
`chemins.py` aurait évité l'adaptateur — voir remontée 2.

## 3.6 Ce que la réécriture a jeté, et qui ne revient pas

`V1_MARKERS` et `is_active_v2()` de `check_brain.py`, `MOC_CONCEPT` /
`WIKI_LABEL` / `wiki_group()` de `build_mocs.py`, le jeu `V1` de
`build_links.py`, `arbo.LEGACY` — la dette de §5.10, mesurée au lot 3 et jetée
par la réécriture guidée. Elle disparaît **du vault** aujourd'hui, et non
seulement du kit : c'est la première fois que le §5.10 produit un effet
observable, et il vaut 2 677 lignes retirées contre 553 posées.

---

# 4. La clé `scanned` — la remontée que deux lots avaient renvoyée ici

## 4.1 Le fait, et sa preuve dans le vault réel

`scanned` publiait **tout** dossier de premier niveau hors `genere.non_pages`,
suivi par git ou non. Un dossier posé sur le disque par autre chose que le dépôt —
une sauvegarde, un `node_modules`, un dossier temporaire d'éditeur — entrait donc
dans un artefact **versionné**, et l'artefact cessait d'être reproductible : deux
machines qui génèrent le même commit produisaient deux catalogues différents.

Le DevBrain en portait la preuve, et c'est le seul écart que le lot 4 n'avait pas
pu fermer :

```diff
   "scanned": [
-    ".githooks",
     "Automatisation no-code",
     …
-    "Web & API",
-    "obsidian_outer_backup_20260907"
+    "Web & API"
   ],
```

`obsidian_outer_backup_20260907` **n'existe pas sur le disque**. Il a existé le
jour où l'index a été généré, il est parti depuis, et le catalogue committé
l'annonce encore. `.githooks` existe, mais ne porte aucune page : il est de
l'outillage.

Le lot 5 avait fourni le second cas, plus net : sur HistoBrain vierge, `scanned`
annonçait quatorze dossiers dont **trois** ne portent rien. La clé était donc
fausse par construction et dès le premier jour, pas seulement en présence d'un
dossier parasite.

## 4.2 Le correctif, et l'issue qui n'a pas été prise

Le lot 4 posait deux issues : restreindre `scanned` aux dossiers qui portent une
page, ou supprimer la clé (elle est dérivable de `genere.non_pages`). Le lot 5
tranchait pour la première. Le lot 9 l'applique.

```python
premiers = {p.chemin.split("/", 1)[0] for p in self.pages if "/" in p.chemin}
self.scannes = sorted(d.name for d in self.racine.iterdir()
                      if d.is_dir() and d.name not in mo.non_pages
                      and d.name in premiers)
```

Six lignes dans `brainkit/generer/corpus.py`, plus le déplacement du calcul
**après** la lecture du vault — il lui faut les pages. Ce qui n'est pas suivi par
git ne porte pas de page indexée, donc ne s'annonce plus : la clé devient exacte
et reproductible d'un coup, sans avoir à consulter git.

La seconde issue a été écartée. Supprimer la clé aurait retiré du catalogue une
information que ses consommateurs peuvent lire, pour corriger un défaut qui tenait
à sa **définition**, pas à son existence.

## 4.3 Le jeu d'épreuve, écrit pour tenir des deux côtés de la bascule

`tests/generation.py`, scénario 7, affirmait « **un seul** écart : le catalogue
machine » et « il tient à **un** dossier fantôme ». Les deux devenaient faux après
la régénération du vault — non parce que le kit régresse, mais parce que le fait
qu'ils décrivent disparaît.

Le scénario a donc été réécrit pour être vrai **avant et après** :

- « **au plus** un écart : le catalogue machine » (`ecarts(s) <= {…}`) ;
- « et il tient aux **seuls dossiers sans page** de `scanned` » — le catalogue
  régénéré est soit déjà identique au fichier committé, soit identique dès qu'on
  réinjecte `.githooks` et `obsidian_outer_backup_20260907`.

C'est la même vérification des deux côtés, et elle prouve toujours la même chose :
le générateur n'a changé **que** cette clé.

## 4.4 Ce qui ne bouge pas

**413 artefacts sur 414 sont identiques à l'octet** : 337 bandeaux, 67 hubs
d'arbre, 6 hubs de `Métiers/`, `Comparatifs.md`, la carte des liens, et le
document humain de l'index. Après la régénération, `brainkit generer --check`
sort en **0** sur les 414.

---

# 5. Les vérifications, toutes par exécution

| Contrôle | Commande | Résultat |
|---|---|---|
| Contenu | `uv run AI/scripts/check_brain.py` | code 0 — **0 dure, 111 avertissements** |
| Structure | `uv run AI/scripts/check_arbo.py` | code 0 — chemin et catégorie concordent partout |
| Bandeaux | `uv run AI/scripts/build_bandeau.py --check` | code 0 — les 337 concordent |
| Tous artefacts | `brainkit generer --check` depuis le vault | code 0 — **les 414 concordent** |
| Mesure | `brainkit mesurer` | **identique à l'octet** à la mesure d'avant la bascule, hors ligne d'en-tête |
| Liens | `build_links` | 0 lien non résolu |
| Dérivation | ancienne `arbo` contre le kit | 45 promotions identiques, **0 écart sur 765 pages** |
| Hooks | les trois, lancés sur le vrai intervalle de push | code 0 chacun |
| Identité | `git log -1 --format='%an <%ae> \| %cn <%ce>'` | `floSa <adresse perso>` des deux côtés |
| Trailer | `git log -1 --format=%B \| grep -ci co-authored-by` | 0 |

Le compte de 111 se répartit exactement comme au lot 8 : 62 `voisinage_declare`,
13 `collision_alias`, 13 + 11 + 1 + 1 `couverture_des_vues`, 5
`etiquettes_fermees/Ressources`, 4 `anti_repetition`, 1
`vocabulaire_ferme/axe_vide`.

Les six jeux d'épreuve du kit passent en entier après le correctif de §4 :
`epreuve`, `generation`, `semis`, `skills`, `mesure`, `entretien`.

---

# 6. Ce que le lot n'a pas fait

- **Aucune page touchée**, et en particulier aucune des **297 notions**.
- **Aucune règle durcie, aucune sévérité changée, aucune règle nouvelle.**
- **Aucune faute de contenu corrigée** : les 8 sections `Alternatives` vides, les
  3 briques sans nature, les 5 valeurs `skill/*` orphelines, les 39 bandeaux à
  cellule vide, les 2 sections mortes du gabarit et les 2 champs vestigiaux sont
  toujours là. `brainkit mesurer` les liste ; le lot les regarde et n'y touche pas.
- **Aucun push, aucune intégration.** La branche est locale, `main` est intacte.
  Ce que floSa aura à lancer est en fin du journal du vault.

---

# 7. Remontées

*Ce qui a été trouvé hors du périmètre du lot, et qui ne s'y corrige pas. Une
remontée nomme le fait, dit ce qu'il coûte, et propose — elle ne tranche pas.*

**1 — Une instance branchée a besoin d'une couche d'adaptation, et le kit ne la
fournit pas.** *(lot 10)* Les sept ponts écrits ici sont du **code d'instance** :
ils ne sont dans aucun paquet, ils ne sont testés par aucun jeu d'épreuve du kit,
et la prochaine instance qui voudra la même chose les réécrira. Or c'est le cas
général, pas une singularité du DevBrain — toute instance qui a des habitudes
(un hook, un skill, une commande dans un README) préférera garder ses noms.
Mesuré : 553 lignes, dont 133 de résolution qui sont **intégralement génériques**.
Proposition : `brainkit semer` pose un `AI/scripts/_pont_kit.py` par défaut, et le
manifeste déclare les alias souhaités (`ponts: {check_brain: valider, …}`). Coût :
un générateur de plus au semis, et un cas de plus au test croisé branché/figé.

**2 — `chemins.promotions()` a la mauvaise signature pour un appelant externe.**
*(lot 10, ou le premier lot qui touche `valider/`)* Elle prend des `Page`, parce
qu'elle doit écarter les rôles hors seuil et résoudre la valeur dominante d'un axe
non exclusif. Un appelant qui n'a que des valeurs d'axe — c'est le cas du skill de
capture, qui lit l'index — doit fabriquer des pages factices. Huit lignes ici,
huit lignes dans chaque instance. Proposition : une
`promotions_depuis_valeurs(valeurs, mo)` dans `chemins.py`, qui fait la fabrication
une fois et à la bonne place. Ce n'est pas une correction : c'est la reconnaissance
que le kit a une **API**, et pas seulement une CLI.

**3 — Les skills du DevBrain décrivent un outillage qui n'existe plus.**
*(lot 7 / lot 10)* Mesuré dans le vault : `enrichir-brain` cite `arbo.py` comme
« seule source de la dérivation » et dit qu'un libellé promu « doit être ajouté à
`SUB_LABEL` dans `arbo.py` » — la table est dans `brain.yml` depuis ce lot. Le
`/tmp/ou.py` qu'il donne, lui, **fonctionne toujours** (vérifié par exécution),
parce que le pont garde l'API. Les sept commandes de `cloturer-brain` sont
exactes et tournent. Ce n'est pas corrigé ici, et pour une raison de fond : le
lot 7 **génère** les skills depuis le manifeste, et c'est là que la correction est
structurelle. Le DevBrain est aujourd'hui la seule instance dont les skills sont
écrits à la main — donc la seule à pouvoir prendre du retard sur son manifeste,
qui est le constat E4 en entier. Proposition : régénérer les trois skills du vault
depuis `brain.yml` au lot 10, et faire du DevBrain le contrôle négatif de cette
génération.

**4 — Rien ne vérifie que `exemples/devbrain.brain.yml` et le `brain.yml` du vault
sont identiques.** *(ce lot, non corrigé)* Ils le sont aujourd'hui, à l'octet, et
c'est tenu par attention seule. Le jour où l'un bouge sans l'autre, le kit
continuera de tourner sans rien dire, et le test de fidélité du lot 2 cessera
d'être reproductible **en silence**. Coût : nul aujourd'hui, entier au premier
correctif de manifeste. Deux issues : le jeu d'épreuve compare les deux sha256 et
échoue s'ils divergent (cinq lignes, et le scénario DevBrain de `tests/epreuve.py`
est déjà conditionné à la présence du vault) ; ou l'exemple cesse d'être un fichier
et devient un pointeur. La première est de loin la moins chère.

**5 — `mesurer` ne dit rien du basculement, alors qu'il pourrait le mesurer.**
*(lot 10)* Une instance qui passe de `fige` à `branche` ou l'inverse ne laisse
aucune trace mesurable : `kit.mode` est déclaré, jamais confronté à ce qui est sur
le disque. Un `AI/scripts/brainkit/` présent sur une instance qui se déclare
`branche` — ou l'inverse — passerait inaperçu, et les deux chemins de code
tourneraient sans qu'on sache lequel. C'est exactement le risque résiduel écrit en
§5.1 du cadrage. Proposition : un contrôle de socle `mode_du_kit_concorde`, en
`a_mesurer`, qui compare `kit.mode` à la présence du paquet copié. Ce serait une
règle nouvelle, donc hors du périmètre de ce lot.

**6 — Le vault a maintenant une dépendance de poste, et rien ne la déclare.**
*(vault, mineur)* `.claude/settings.json` autorise
`Bash(uv run AI/scripts/check_brain.py)` et le hook `Stop` lance ce fichier ; les
deux **tournent**, vérifié par exécution. Mais la commande a désormais besoin que
BrainKit soit atteignable. Sur une machine où il manque, le hook rapportera une
sortie 2 avec les trois pistes au lieu d'un verdict — comportement voulu du pont,
surprise quand même pour qui lit `settings.json`. Proposition côté vault : une
ligne dans `Documentation/perso/machines.md`. Proposition côté kit : que le semis
écrive cette ligne, puisqu'il connaît le mode de l'instance.

**7 — Les instances d'essai héritent du correctif `scanned` sans avoir été
régénérées.** *(essais, pas kit)* HistoBrain, CimeBrain et `devbrain-controle`
vivent hors de tout dépôt suivi, et leur `brain-index.json` committé — quand il
l'est — annonce encore les dossiers sans page. `generer --check` y sortira en 2
sur cette seule clé, exactement comme le DevBrain avant ce lot. Ce n'est pas un
défaut : c'est le correctif qui se voit. À régénérer au premier lot qui les
rouvre, ou à laisser tel quel — ce sont des bancs d'essai, pas des livrables.

---

# 8. Ce qui reste au lot 10

- **La couche de pont, générée** (remontée 1) — c'est le plus gros morceau, et il
  est déjà écrit une fois, en vrai, sur une instance réelle.
- **Le test croisé branché / figé** (§5.1) a maintenant une instance branchée
  *réelle* à faire tourner, et non plus seulement une instance semée à zéro page.
  Le DevBrain est le meilleur candidat : 765 pages, 414 artefacts, 111
  avertissements — un `freeze` qui les reproduit tous prouve le mode figé bien
  mieux qu'un vault vierge.
- **Le défaut d'instance de `valider` et `generer`** (remontée 3 du lot 5) est
  tombé au lot 6 avec `defauts.py`, et ce lot l'a exercé : lancé depuis la racine
  du vault, `brainkit generer --check` trouve `brain.yml` tout seul et ne demande
  aucune option. La remontée est **close**.
- **La signature comme valeur d'instance** est maintenant prouvée (§3.2), et
  `INSTALL.md` généré devra dire laquelle poser selon `kit.mode`.
