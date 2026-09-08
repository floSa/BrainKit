# BrainKit — la fraîcheur, ou l'amont d'une unité

> Conversation 52, « DevBrain, la fraîcheur des briques », le 2026-09-08. Lot 11,
> mené **après** la clôture du plan de dix lots : `design/etat-final.md` reste le
> document à relire d'abord, et il a été mis à jour là où ce lot l'a rendu faux.
>
> Ce document rend l'arbitrage du rangement de la donnée, les deux sondes et le
> refus du jeton, les cinq états, la sixième forme de colonne de bandeau, la
> règle et sa mesure, le contrôle négatif sur HistoBrain, la remontée fermée au
> passage, et les remontées ouvertes.
>
> **Aucun contenu de page n'a été écrit** — ni `## Définition`, ni `## Retours`,
> ni une `maturite:` que l'amont contredit. Les zones `<!-- AUTO:BANDEAU -->` des
> 337 briques ont été régénérées, et c'est tout.

## Le problème que ce lot résout, en une phrase

Une brique porte `maturite: production`, et c'est **déclaratif** : écrit une fois
à la capture, jamais revérifié. Rien dans le vault ne disait qu'un dépôt n'avait
pas eu de release depuis trois ans, ni qu'il était archivé — et il y en a sept.

Le kit sait maintenant aller voir. Et parce qu'une source d'histoire n'a pas de
dépôt, **il ne sait le faire que sur déclaration** : sans bloc `amont:` au
manifeste, il ne sonde rien, ne signale rien et n'affiche aucune colonne. C'est
le contrôle négatif du lot, et il est aussi important que le positif.

---

# 1. Où la donnée sondée est rangée — et pourquoi pas dans les pages

La recommandation reçue au cadrage de ce lot était le **side-car**. Elle est
confirmée, et le motif compte plus que la conclusion : il y en a trois, et
chacun suffirait.

**Un — cette donnée se périme toute seule.** Un frontmatter dit ce que floSa a
décidé ; une date de release dit ce que le monde a fait pendant qu'il ne
regardait pas. Les mêler ferait porter à l'auteur une valeur dont il n'est pas
responsable et qu'il ne peut pas tenir à jour. C'est exactement le reproche que
le lot fait à `maturite:` — une valeur écrite une fois et jamais revérifiée — et
le corriger en créant une seconde valeur de la même famille serait absurde.

**Deux — un sondage produirait 337 diffs.** Un par brique, à chaque passage,
dont aucun ne parlerait du travail de la semaine. Le side-car en produit **un**.
Le vault d'origine a déjà payé ce prix : le lot 9 note qu'un artefact versionné
qui bouge sans raison rend deux machines incapables de produire le même commit.

**Trois — un side-car se jette.** Le supprimer ne perd rien qu'un sondage ne
refasse ; supprimer un champ de frontmatter perd une décision. La réversibilité
n'est pas la même, et elle doit se voir dans l'endroit où la donnée est rangée.

## 1.1 Le fichier choisi, et le conflit qu'il a fallu trancher

Le manifeste déclare `amont.side_car: "AI/index/fraicheur.json"`. C'est le chemin
qu'écrivait déjà `verifier_fraicheur.py`, le script de fraîcheur d'avant le kit,
et le reprendre était le bon choix : **deux fichiers de fraîcheur seraient
exactement la seconde source que le manifeste existe pour supprimer.**

Mais deux écrivains sur un fichier, avec deux formes d'enregistrement, s'effacent
l'un l'autre en silence — et un side-car à moitié écrit ne se voit pas. Le script
d'origine écrit donc `AI/index/fraicheur-hors-ligne.json`, et il garde ce que le
kit ne fait pas : les URL mortes et les redirections de domaine, la licence
constatée contre `licence_type:`, la version majeure affirmée dans le corps
contre celle du registre, le corps qui décrit un déclin sous une `maturite:`
vive, et le croisement avec les puces de fin de vie des comparatifs.

Le recouvrement entre les deux se limite à **un fait**, l'archivage, et le kit le
sonde autrement — sans jeton. Fondre les deux est une remontée, pas un geste de
ce lot.

## 1.2 Ce que le side-car garde, et ce qu'il ne garde pas

Il garde les **faits bruts** — une date de release, une étiquette, une date de
commit, un drapeau d'archivage, une version de registre — **et** l'état dérivé,
avec la date qui a servi à le décider.

Garder l'état écrit est un arbitrage, et il n'est pas une optimisation. Un état
recalculé à la lecture dépendrait de la date du jour : la zone AUTO d'une page
changerait toute seule, sans qu'aucun sondage ait eu lieu et sans que rien le
dise. **Un artefact généré doit être une fonction de ce qui est écrit, pas de
quand on le lit.** Le prix de ce choix est qu'un seuil modifié demande une
re-dérivation ; `brainkit sonder --recalculer` la rejoue sur les faits déjà
sondés, sans un seul appel réseau.

## 1.3 La clé est un chemin, et c'est un défaut connu

Une page n'a pas d'identifiant stable : la clé du side-car est son chemin, et un
`git mv` la casse. Le vault d'origine en a fait l'expérience — 101 entrées
devenues orphelines après un lot de déplacement, et un mécanisme de reprise mort
en silence pendant tout un lot, parce qu'un compteur à zéro ressemble à une bonne
nouvelle.

On ne peut pas y remédier ici : inventer un identifiant de page serait un autre
lot, et un champ de plus dans 337 pages. On peut **refuser de se taire** — le
rapport de sondage nomme les entrées orphelines et dit que leurs sondes sont
perdues.

---

# 2. Les deux sondes, et le refus du jeton

## 2.1 Pourquoi l'API REST n'est pas employée

`api.github.com/repos/{slug}` rend tout ce qu'on veut en **un** appel : archivé,
dernier push, licence, dernière release. Et **60 appels par heure** sans jeton.
Sur les 316 dépôts déclarés par le vault, une passe complète prendrait plus de
cinq heures, ou exigerait un jeton.

Un jeton dans un vault versionné est un secret publié. Un jeton dans
l'environnement est une étape d'installation qu'on oublie, donc un outillage qui,
un jour, ne tourne plus — et qui ne le dit pas. L'interdiction posée au cadrage
de ce lot (« aucun jeton d'API écrit où que ce soit ») n'est donc pas une gêne à
contourner : c'est ce qui a **forcé** la conception qui suit, et la conception
qui suit est meilleure.

## 2.2 Les trois URL, et ce qu'elles rendent

Ce sont celles qu'un navigateur charge, sans compte et sans quota d'API.

| URL | Ce qu'elle rend | Coût |
|---|---|---|
| `github.com/<slug>/releases.atom` | date et étiquette de la dernière version publiée | ~2 à 450 Ko |
| `github.com/<slug>/commits.atom` | date du dernier mouvement de la branche par défaut | ~16 Ko |
| `github.com/<slug>` | `"isArchived": true\|false`, plus la **date** d'archivage en clair | lecture **bornée** |

La troisième est la plus chère, et c'est le seul endroit où l'archivage se lit
sans jeton. Sa lecture s'arrête dès que le marqueur est vu, ou à 400 Ko. On
télécharge un quart de mégaoctet là où l'API en rendait deux kilos : **le prix de
l'absence de jeton est payé en octets plutôt qu'en secret.**

Le registre — `pypi.org/pypi/<paquet>/json` — est la quatrième requête, et elle
n'est pas un doublon : un paquet publie parfois sur le registre sans taguer son
dépôt, et sa seule date de publication est là. Sur le vault réel, elle date
**161** briques, dont trois qu'aucune release de dépôt ne datait.

Mesure de la passe complète : **1 128 requêtes anonymes** pour 337 pages, en
environ neuf minutes, sans un seul refus de l'hôte.

## 2.3 Ce qu'on ne sait pas atteindre, et qui est dit

- **1 hôte non déclaré** — `git.deuxfleurs.fr` (la brique Garage). Le kit n'a pas
  de sonde pour cet hôte ; la page sort en « aucun amont fiché ». Dire qu'on ne
  sait pas vaut mieux que ne rien dire, et vaut infiniment mieux que deviner.
- **1 URL qui vise un sous-arbre** — ScaNN, dans le monorepo `google-research`.
  Le dépôt est sondé, et le rapport dit en toutes lettres que ses dates décrivent
  le dépôt entier et non le sous-arbre.
- **1 dépôt disparu** — FossFLOW rend 404 sur son slug. État `sans_amont`.
- **4 pages dont l'archivage n'a pas pu être lu** : le marqueur n'était pas
  atteint sous le plafond de lecture. Elles sont **nommées** dans le rapport, et
  le drapeau reste absent du side-car plutôt que posé à `false` — la différence
  entre « non archivé » et « je n'ai pas vu » est exactement celle que ce lot
  refuse de perdre.
- **19 briques sans URL d'amont** — Figma, AWS S3, Pinecone, Zapier, LM Studio…
  Ce ne sont pas des trous : ce sont des services qui n'ont pas de dépôt public.

---

# 3. Les cinq états, et les deux silences qui ne se confondent pas

Fermés par le kit, comme les six fonctions de rôle. Le manifeste leur donne un
**libellé**, il n'en ajoute ni n'en retire.

| État | Ce qu'il dit |
|---|---|
| `recente` | la dernière trace datée de l'amont est dans le seuil |
| `ancienne` | elle le dépasse |
| `archive` | le propriétaire a fermé le dépôt |
| `sans_amont` | on a regardé, il n'y a rien à atteindre |
| `jamais_sonde` | le side-car ne connaît pas cette page |

Les deux derniers sont **deux silences différents**, et les fondre serait la
faute du lot : un compteur unique ferait passer « je n'ai pas encore travaillé »
pour « il n'y a rien à savoir ». C'est la même leçon que « une règle absente ne
ressemble pas à une règle souple, elle ressemble à une règle satisfaite »,
transposée à un rapport.

## 3.1 L'ordre des tests EST la règle

1. **jamais sondé** — rien dans le side-car : on ne sait pas, et on le dit.
2. **archivé** — cela prime sur toute date. Une release récente d'un dépôt
   archivé ne dit pas que le projet vit : elle date sa dernière respiration.
3. **une release datée** — la plus récente gagne, quelle que soit sa provenance,
   dépôt ou registre.
4. **un commit daté** — plus faible, et son seuil est donc **distinct**. Un projet
   stable peut ne rien publier pendant deux ans en recevant des correctifs ;
   l'inverse n'existe pas. Sur le vault réel, **4** pages sont dans ce cas.
5. **sinon** — sans amont atteignable.

## 3.2 Le seuil est mesuré, pas choisi

Le manifeste déclare `release_ancienne_jours: 730` et `commit_ancien_jours: 365`.
Le premier a été arrêté **après** la mesure, sur les 337 briques sondées :

| Seuil | Briques au-delà |
|---|---|
| 180 j | 38 |
| 365 j | 21 |
| 545 j | 16 |
| **730 j** | **13** |
| 1 095 j | 10 |
| 1 460 j | 8 |

La courbe est plate après 730 : descendre à 365 ajoute huit briques dont la
plupart sont des paquets stables qui publient peu, et monter à 1 095 n'en retire
que trois. 730 est le point où la liste reste **relisable en une fois** sans rien
perdre de ce qui compte. Le chiffre se change dans le manifeste, et
`--recalculer` rejoue la dérivation sans réseau : c'est ce qui rend l'arbitrage
révisable au lieu d'être gravé.

---

# 4. Le bandeau — une sixième forme de colonne

Le haut de page d'une brique portait quatre colonnes dérivées du frontmatter. Il
en porte cinq, et la cinquième ne lit pas le frontmatter :

```
| Nature | Licence | Exécution | Maturité | Fraîcheur |
|---|---|---|---|---|
| Librairie Rust | open-source | en bibliothèque, rien à héberger | production | à jour · 2026-09-02 |
```

```
| Plateforme Go | open-source | self-hébergé · distribué | production | dépôt archivé · 2026-04-25 |
```

La seconde ligne est la brique MinIO, et elle dit tout le lot : la fiche déclare
`production`, l'amont dit archivé depuis avril. Les deux se lisent **ensemble**,
sur la même ligne, et le désaccord se voit sans ouvrir un rapport.

## 4.1 Ce que le moteur a gagné, et ce qu'il n'a pas changé

Une colonne déclare `externe: amont`. Le moteur ne change pas d'une ligne — même
`table:`, même `qualifie_par:`, même caractère vide, même échappement du `|` —
seul **l'endroit où il va chercher la valeur** diffère. C'est ce qui rend
l'ajout sûr : les quatre colonnes existantes n'ont pas été touchées, et les 337
bandeaux régénérés ne diffèrent que par la cellule ajoutée.

Une seule chose est neuve : `separateur:`, l'espace par défaut. Il existe parce
qu'une qualification peut être de même nature que sa base (« Librairie Python »)
ou d'une autre (« à jour » et une date). Dans le second cas, l'espace seul colle
deux choses qui ne se lisent pas ensemble.

## 4.2 La cellule n'est jamais vide, et c'est délibéré

Les cinq états couvrent tous les cas, y compris les deux silences. Une page
jamais sondée affiche « amont non sondé », pas le tiret cadratin — parce que le
tiret veut dire « champ absent du frontmatter », et que ce serait faux : le champ
n'existe pas, c'est le sondage qui n'a pas eu lieu, et les deux ne se réparent
pas de la même façon.

Conséquence mesurable : le rapport de trous du générateur reste à **39** avant
comme après, et ces 39 sont tous des `Maturité` absentes. La colonne ajoutée n'en
crée aucun.

## 4.3 Le coût assumé : un sondage réécrit 337 pages

Il faut le dire, parce que c'est l'objection au fait d'afficher la fraîcheur dans
la page plutôt que dans un rapport. Elle tient, et elle est acceptée : la valeur
affichée est une **date**, qui ne change que lorsque l'amont publie
effectivement. Un second sondage à une semaine d'intervalle ne touchera que les
briques dont l'amont a bougé. La régénération, elle, reste mécanique et
vérifiable — `generer --check` sort en 2 tant qu'elle n'a pas été faite.

---

# 5. La règle `amont_concorde`

Une règle de **socle**, pas une des dix : la liste des dix est fermée par le kit.
Trois sous-clés, qui ne se comptent pas ensemble parce qu'elles ne se réparent
pas de la même façon.

| Sous-clé | Ce qu'elle signale | Compte |
|---|---|---|
| `archive` | l'amont est archivé, la page ne le dit pas | **4** |
| `ancien` | la dernière trace datée dépasse le seuil | **10** |
| `contredit` | l'inverse : l'amont publie encore, la page porte une valeur **éliminatoire** | **2** |

La troisième vaut autant que les deux autres, et elle n'était pas dans le cahier
des charges sous cette forme. Une brique `maturite: deprecated` dont le dépôt a
publié la semaine dernière est aussi trompeuse qu'une brique dite vive qui ne
l'est plus — et **personne ne relit une fiche qu'il croit enterrée**. Sur le
vault réel elle trouve Marqo et AutoGen.

## 5.1 Jamais dure, et ce n'est pas provisoire

Une violation ici n'est pas une faute de rédaction : c'est un désaccord entre le
vault et un **tiers**, dont le tiers peut avoir tort — un dépôt miroir archivé
pendant que le vrai développement déménage, un projet qui ne tague plus ses
versions mais livre sur son registre. L'outil ne sait pas laquelle des deux
sources dit vrai, et trancher appartient à l'auteur.

Durcir reviendrait à faire échouer la clôture d'un vault parce qu'un inconnu a
cliqué sur « archiver ». C'est la même raison qui fait sortir `sonder` en **0**
sur ses constats : **un brain ne doit pas être otage de son amont.** La règle
héritée de `verifier_fraicheur.py`, et elle tient.

## 5.2 Le dénominateur est le nombre de pages SONDÉES

Pas le nombre de briques. Une page jamais sondée n'est pas conforme, elle est
**inconnue** : la compter ferait passer un side-car vide pour un vault sain. Les
deux coïncident aujourd'hui (337 sur 337) parce que la passe est complète, et ils
se sépareront dès qu'une passe sera bornée par `--limit`. Le nombre de pages hors
population est dit dans une note du validateur, jamais tu.

## 5.3 Ce que la mesure en dit

```
amont_concorde   avertissement   16   337 page(s)
    à réparer — 16 violation(s) à réparer d'abord — un durcissement ne se propose pas sur un passif
      · ancien      10
      · archive      4
      · contredit    2
```

`mesurer` ne propose donc rien, et c'est le comportement juste : une règle qui a
un passif ne se durcit pas, elle se travaille. Le garde-fou 2 est satisfait — la
règle porte trois `motif:` écrits.

---

# 6. Le contrôle négatif — HistoBrain ne sonde rien

C'est le scénario qui prouve que le mécanisme est déclaratif, et il est aussi
important que tout ce qui précède. Le manifeste d'HistoBrain ne porte pas de bloc
`amont:` — une source d'histoire n'a pas de dépôt.

| Commande | Ce qui se passe |
|---|---|
| `brainkit sonder` | **sort en 2**, refuse, et dit pourquoi : « ce brain n'a pas d'amont à sonder. Ce n'est pas une faute. » Zéro requête réseau |
| `brainkit valider` | `amont_concorde · 0 — non déclarée par ce manifeste`. L'inventaire nomme le silence |
| `brainkit generer --check --quoi bandeau` | **sort en 0**, les 10 artefacts concordent. Le bandeau garde ses quatre colonnes |
| `grep -rl "Fraîcheur" *.md` | aucune ligne |

Le refus est un **code 2 et non un code 0** : une commande sans objet sur ce brain
se dit, elle ne rend pas un rapport vide qui ressemblerait à « tout va bien ».

`tests/amont.py` porte le même contrôle en version reproductible, sur le manifeste
du jeu d'épreuve : avec le bloc, deux colonnes et seize constats ; sans lui, une
colonne et rien.

---

# 7. La remontée fermée au passage

**Remontée 1 de `design/etat-final.md` §4.3** — comparer les sha256 de
`exemples/devbrain.brain.yml` et du `brain.yml` du vault. Ils étaient identiques
« par attention seule » depuis le lot 9, et cinq documents du dépôt les lisent
l'un pour l'autre.

C'est fait dans `outils/fidelite.py` (`passe_jumeau`), et l'outil sort en **1**
s'ils ont divergé, en imprimant les deux empreintes. Le motif écrit dans le code
est celui qui rendait la remontée urgente malgré son coût dérisoire : *une
divergence ne casse rien — elle rend faux tout ce qu'on croit avoir vérifié.*

Ce lot en a eu besoin dès sa première heure : il modifie les deux manifestes, et
c'est exactement le geste où l'un des deux se serait oublié.

---

# 8. Les vérifications

| Quoi | Résultat |
|---|---|
| `schema/valider.py` | les 3 manifestes, verdict inchangé |
| `outils/fidelite.py` | toute divergence porte un verdict · **les deux manifestes identiques à l'octet** |
| `outils/emballer.py` | les 6 documents du dépôt concordent |
| `tests/epreuve.py` | 0 dure, **127** avertissements, compte exact règle par règle |
| `tests/generation.py` | 337 bandeaux, 74 hubs, liens, index — tout concorde |
| `tests/amont.py` | 6 scénarios, 46 vérifications, aucun appel réseau |
| `tests/semis.py` · `skills.py` · `entretien.py` · `emballage.py` · `mesure.py` | inchangés, verts |
| `brainkit generer --check` sur DevBrain | **0**, les 414 artefacts concordent |
| `check_brain.py` · `check_arbo.py` | 0 dure · chemin et catégorie concordent partout |

Le compte d'avertissements passe de **111 à 127**. Les seize sont **tous** des
constats de `amont_concorde`, une règle neuve : aucun compte existant n'a bougé,
et c'est ce qu'il fallait vérifier.

---

# 9. Arbitrages

**1 — L'API REST écartée au profit de trois URL publiques.** Le cahier des
charges annonçait « sans jeton (60 appels/h) avec reprise incrémentale », ce qui
décrivait l'API et sa contrainte. La reprise incrémentale est là, mais la
contrainte a disparu : les flux Atom et la page du dépôt n'ont pas de quota
d'API, et une passe complète tient en neuf minutes au lieu de cinq heures. Le
prix est une lecture HTML bornée pour un seul fait, l'archivage — et un marqueur
HTML est plus fragile qu'un champ d'API. Il est donc **borné, nommé, et son échec
se dit** : quatre pages sont sorties en « archivage non lu » plutôt qu'en « non
archivé ».

**2 — L'état est écrit dans le side-car, pas recalculé à la lecture.** Sinon la
zone AUTO d'une page changerait le jour où un seuil est franchi, sans sondage et
sans trace. Cf. §1.2.

**3 — Une cinquième colonne plutôt qu'une ligne ou une marque.** Le schéma
plafonne le bandeau à cinq colonnes, et on y est exactement. Une ligne
supplémentaire aurait doublé la hauteur du bandeau pour un seul fait ; une marque
(un emoji, un astérisque) aurait demandé une légende, donc un endroit où la
mettre. La colonne se lit sur la même ligne que `Maturité`, ce qui est
précisément où le désaccord doit se voir.

**4 — Le side-car garde le chemin de `verifier_fraicheur.py`, et c'est ce dernier
qui déménage.** Cf. §1.1. L'alternative — deux fichiers de fraîcheur — était la
seconde source que tout le chantier existe pour supprimer.

**5 — `sans_amont` n'est PAS signalé par la règle.** Dix-neuf briques n'ont pas
de dépôt public parce que ce sont des services propriétaires ; les signaler
ajouterait dix-neuf avertissements permanents pour un fait qui n'est pas un
défaut. Le compte est dans le rapport de sondage, où il appartient.

---

# Remontées

**1 — Fondre les règles hors ligne de `verifier_fraicheur.py` dans le kit.**
Elles sont bonnes et le kit ne les a pas : URL mortes et redirections de domaine,
licence constatée contre la licence déclarée, version majeure affirmée dans le
corps contre celle du registre, corps qui décrit un déclin sous une maturité
vive, croisement avec les puces de fin de vie des pages de comparatif. Les trois
premières sont génériques ; les deux dernières demandent qu'un manifeste puisse
déclarer un motif de texte, ce qui est un mécanisme neuf. *(un lot)*

**2 — Une sonde `gitlab`, et le cas général de l'hôte inconnu.** Une seule brique
est concernée aujourd'hui, ce qui ne justifie pas le code. Mais la vraie question
est plus large : le kit refuse un `sonde:` hors de sa liste fermée, ce qui est
juste, et ne propose rien pour un hôte que personne ne sait sonder. Aujourd'hui
la page sort en `sans_amont`, ce qui est honnête mais confond « pas de dépôt » et
« dépôt que je ne sais pas lire ». Un sixième état ? Ou une ligne de rapport ?
*(à trancher avant d'ajouter une seconde sonde)*

**3 — L'archivage lu en HTML est le seul fait fragile du lot.** Le marqueur
`"isArchived": true|false` est un détail d'implémentation de GitHub, pas un
contrat. Il tiendra jusqu'au jour où il ne tiendra plus, et ce jour-là **quatre
pages deviendront trois cents** dans la liste « archivage non lu ». C'est
précisément ce que cette liste existe pour rendre visible — mais il faut que
quelqu'un la lise. *(un seuil d'alerte dans le rapport : si plus de 10 % des
pages sortent en archivage non lu, le dire fort)*

**4 — La clé du side-car est un chemin.** Cf. §1.3. Un `git mv` perd les sondes
de la page déplacée. Le rapport les nomme, elles se refont au sondage suivant, et
c'est tout ce qu'on peut faire sans donner un identifiant stable aux pages.

**5 — `taille_avertissement` et `collision_alias` n'ont toujours pas de
`motif:`.** `brainkit mesurer` sort donc en **1** sur le DevBrain, par le
garde-fou 2, et c'était déjà vrai avant ce lot. Ce n'est pas un défaut du kit :
c'est le garde-fou qui fonctionne, et il attend deux phrases dans le manifeste.
*(deux phrases, et l'arbitrage appartient à floSa)*

**6 — Le sondage n'est dans aucune boucle automatique.** Il se lance à la main,
et rien ne rappelle qu'il faudrait le faire. Un side-car vieux de six mois ne se
distingue d'un side-car frais que par les dates `sonde_le` qu'il porte, et
personne ne les lit. Une ligne dans le rapport de clôture — « le side-car de
l'amont a N jours » — coûterait dix lignes. *(10 lignes, à poser dans le skill de
clôture ou dans le validateur)*
