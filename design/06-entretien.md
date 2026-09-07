# BrainKit — l'entretien d'initialisation

> Conversation 47, « BrainKit lot 6, l'entretien », le 2026-09-07.
> Lot 6 du plan de `design/00-cadrage.md` §6. C'est le lot que l'utilisateur voit
> en premier : sans lui, créer un brain demande d'écrire cent kilo-octets de YAML
> à la main, ce que personne ne fera.

## Ce que le lot livre

| Livrable | Contenu |
|---|---|
| `brainkit/entretien/` | 6 modules — les passes en données, les treize refus en contrôles, l'induction, le brouillon de reprise, le composeur, le rendu |
| `brainkit entretien` | une sixième commande : `--questions`, `--refus`, `--etat`, `--repondre`, `--reponses`, `--rappel`, `--oublier`, `--verifier`, `--composer`, `--semer` |
| `skills/entretien/SKILL.md` | le skill qui **mène** l'entretien — la conduite, l'induction en quatre gestes, la clôture |
| `.claude/skills/reprendre-l-entretien/` | le skill **instancié** par le semis : rouvrir une question sur un brain qui existe, avec le prix de chaque changement |
| `racine.dossiers[]` | l'arbitrage `Projects/` — le dossier d'atelier se **déclare** |
| `brainkit/defauts.py` | le manifeste par défaut est celui du **vault**, et une incohérence se dit |
| `tests/entretien.py` | 7 scénarios, **49 vérifications**, dont le contrôle négatif de l'identité et la reprise |
| `tests/cimebrain.reponses.yml` | les 49 réponses d'un entretien joué en entier, sur un **troisième** sujet |
| l'instance `CimeBrain` | semée hors de tout dépôt suivi, `~/Documents/BrainKit-essais/cimebrain` |

Ce que le lot **ne** livre **pas**, et le dit : les trois skills du brain
(capture, clôture, exploitation) restent au lot 7. Le semis pose leur dossier et
le README qui les nomme, comme au lot 5. Le seul skill instancié est celui de
reprise, et la raison est écrite en §8.9.

---

# 1. Le critère d'acceptation, et comment il est tenu

## 1.1 Un entretien joué en entier sur un TROISIÈME sujet

Ni le dev, ni l'histoire : **la montagne**. Le sujet a été choisi parce qu'il
éloigne de deux façons à la fois, et non d'une seule.

- **L'unité n'est ni un outil ni une source, c'est un ITINÉRAIRE** — une chose
  qu'on *fait*, pas une chose qu'on lit ni qu'on installe. Le DevBrain range des
  choses qu'on installe ; HistoBrain range des choses qu'on lit. CimeBrain range
  des choses qu'on n'a pas encore faites, et c'est un troisième rapport au temps.
- **L'axe qui range est presque exclusif, et ce sont les traversées qui le
  cassent.** Le mécanisme non exclusif se rejoue donc sur un cas qui n'a rien à
  voir avec les synthèses de longue durée de HistoBrain : une Haute Route n'est
  pas une synthèse, c'est un objet qui traverse physiquement.

| Mesure | DevBrain | HistoBrain | **CimeBrain** |
|---|---|---|---|
| unité | brique (un outil) | source (un texte) | **course (un itinéraire)** |
| axe de rangement | domaine | période | **massif** |
| paquets | 20 | 8 | **7** |
| exclusif | oui | non | **non** |
| axe de nature | famille (9) | nature (9) | **terrain (7)** |
| axes transverses | 1 | 2 | **1** |
| rôles | 6 | 6 | **5** |
| unités interchangeables (8.1) | oui | non | **non** |
| réciprocité inverse | non | oui | **oui** |
| volume cible | 700 | 3000 | **600** |
| **seuil dérivé** | 5 | 12 | **7** |

## 1.2 Le résultat, chiffré

```
uv run brainkit entretien --brouillon <b.yml> --reponses tests/cimebrain.reponses.yml
uv run brainkit entretien --brouillon <b.yml> --semer ~/Documents/BrainKit-essais/cimebrain --ecrire
```

| Ce qui est vérifié | Résultat |
|---|---|
| le manifeste composé — `uv run schema/valider.py` | **VALIDE** (schéma + les dix contraintes de cohérence du lot 1) |
| le manifeste composé — pré-conditions de semis | **0 manque** |
| fichiers semés | **44**, dont 9 pages, toutes `role: hub` |
| **pages d'unité** | **0** |
| `brainkit valider` — violations **dures** | **0** |
| `brainkit valider` — avertissements **et** à-mesurer | **0** |
| `brainkit generer --check` juste après | **12 artefacts, 0 écart**, code 0 |
| les 20 titres cités en 2.1, dans `Inbox.md` | **20 / 20**, en cases à cocher |
| … et pages écrites pour eux | **0** |
| identité du commit initial | `floSa <florian_horellou@laposte.net>` — celle du **manifeste** |
| `git status` juste après le semis | **vide** |
| `git -c user.email=…@aosis.net commit` | **refusé** par `pre-commit` |
| message portant `Co-Authored-By:` | **refusé** par `commit-msg` |

Le manifeste produit fait **1 212 lignes**, dont les `motif:` — écrits par le
composeur, pas recopiés d'un autre brain. Il déclare 5 rôles, 20 champs, 7
valeurs de nature, 7 préfixes, 1 axe transverse à 4 valeurs, 4 colonnes de
bandeau, 10 règles **toutes en `a_mesurer`**, 12 règles de socle, 7 entrées de
graphe et une table de propagation de 6 lignes plus P7.

## 1.3 Ce que la mesure 2 vaut

**Zéro avertissement**, et pas seulement « aucun avertissement injustifié ». Sur
un vault à zéro page d'unité, tout avertissement serait injustifié par
construction : il porterait sur une page que personne n'a écrite. Un
avertissement au semis signalerait donc un défaut **du kit**, pas du vault.
C'est le même contrôle qu'au lot 5, et il tient sur un manifeste qui n'a pas été
écrit à la main.

---

# 2. Les onze passes, telles qu'elles sont implémentées

`uv run brainkit entretien --questions` les imprime, avec pour chaque question ce
qu'elle produit et quel refus la garde. Elles vivent en **données**
(`brainkit/entretien/passes.py`) et non en prose, pour une raison mesurable :
une liste en prose se dégrade — une question saute, une autre change d'ordre, et
personne ne s'en aperçoit parce que rien ne compte. Ici le jeu d'épreuve compte,
vérifie l'ordre, et vérifie que chacun des treize refus est porté.

| Passe | Titre | Questions | Ce qu'elle établit |
|---|---|---|---|
| 0 | Identité et dépôt | **6** | sujet, nom, usage, **identité git**, domaine refusé, dossier cible |
| 1 | L'unité | **5** | l'unité, les notions, les protégées, les prescriptions |
| 2 | L'axe qui range | 7 | l'échantillon, les paquets, l'exclusivité, le volume, l'arbre |
| 3 | L'axe qui qualifie | 4 | les natures, leurs frontières, les champs conditionnels |
| 4 | Les axes transverses | 3 | zéro, un ou plusieurs |
| 5 | Le haut de page | 3 | trois à cinq faits, et leur champ source |
| 6 | Le corps | 5 | les sections, dans l'ordre, et leur genre |
| 7 | Les liens et le résumé | 4 | les relations, leur réciprocité, le résumé court |
| 8 | Ce qui rassemble | 3 | un rôle `vue`, ou aucun |
| 9 | Gouvernance et frontières | **6** | tags, suppressions, second mode, générés, **racine**, **atelier** |
| 10 | L'exploitation | 3 | le livrable et ses formes |
| | **total** | **49** | |

## 2.1 Quarante-neuf et non quarante-cinq — les quatre questions ajoutées

Le cadrage en compte quarante-cinq. Il en manquait quatre, et le manque n'était
pas théorique : **sans elles, l'entretien ne saurait produire ni le manifeste
DevBrain, ni le manifeste HistoBrain**, qui sont pourtant ses deux remplissages
de référence.

| id | Ce qu'elle produit | Pourquoi elle manquait |
|---|---|---|
| **0.6** | le dossier de l'instance | l'entretien finit par appeler le semis ; le chemin ne se devine pas plus qu'une adresse, et le plan d'écriture a quatre refus de cible qu'il vaut mieux rejouer à vide avant de proposer |
| **1.5** | les rôles `fonction: prescription` | **aucune** question du cadrage ne les crée, et les deux remplissages de référence en portent **deux chacun** (`pattern` + `rule`, `controverse` + `methode`). C'est le trou le plus net de §3.1 |
| **9.5** | le bloc `racine:` | demandé par le lot 5, §10 : *« il porte une question de plus à poser »*. La réponse par défaut — une porte et une inbox — est celle des deux remplissages, mais elle ne se devine pas plus qu'une autre |
| **9.6** | `racine.dossiers[]` | l'arbitrage `Projects/`, remontée 4 du lot 5, renvoyée à ce lot |

Chacune porte un champ `ajoutee:` avec son motif écrit, et le jeu d'épreuve
vérifie que ce champ est rempli : **une question hors cadrage sans motif écrit
serait une question inventée**, et l'entretien n'en pose pas plus qu'il n'en
devine.

## 2.2 Les questions conditionnelles se sautent toutes seules

Sept des quarante-neuf sont conditionnelles. Sur un brain qui répond « non » à
3.1, trois questions disparaissent — 3.2, 3.3, 3.4 — et l'entretien n'a pas à
s'en souvenir : `Brouillon.posable()` évalue la condition, `restantes()` les
retire, et `sautees()` les distingue des oubliées. Le jeu d'épreuve compose un
brain **sans axe de nature** pour le prouver.

---

# 3. L'induction — le cœur difficile

## 3.1 Le problème, et pourquoi la solution évidente est la mauvaise

L'utilisateur ne connaît pas sa taxonomie. Il ne sait pas nommer ses domaines,
et si on les lui propose il en cochera — par politesse, par fatigue, parce que
la liste a l'air raisonnable. Le brain héritera alors d'une taxonomie qui n'est
pas la sienne, et il s'en apercevra à la trentième page, quand il ne saura plus
où ranger. Il sera trop tard : déplacer trente pages coûte plus que les écrire.

L'entretien fait l'inverse. **La taxonomie n'est pas proposée, elle est LUE dans
un geste.**

## 3.2 Les quatre gestes

**Geste 1 — faire citer vingt pages RÉELLES.** Pas des catégories : des titres
qu'il ouvrirait vraiment. L'entretien attend, et ne propose rien. Sous dix
titres, `induis_les_paquets` rend un diagnostic **bloquant** — l'induction ne
tient pas, et un manifeste ne se compose pas.

**Geste 2 — le faire ranger DE SA MAIN.** « Range ces vingt en paquets. Combien
de paquets, et comment les appelles-tu ? » Aucune suggestion de fusion, aucune
suggestion de découpe. Ce qu'on observe est le résultat : **quel axe a-t-il
choisi spontanément ?**

C'est là que tout se joue, et les trois sujets le confirment :

| Sujet | Axe choisi spontanément | Pourquoi lui |
|---|---|---|
| dev | le domaine | il exclut : une base de données n'est pas un outil de CI |
| histoire | la **période** — ni le thème, ni l'espace | la période exclut, le thème et l'espace se **cumulent** |
| montagne | le **massif** — ni la difficulté, ni la saison | le massif exclut, la difficulté et la saison se **cumulent** |

Le même résultat, trois fois, sans qu'on ait eu à en discuter : **l'axe de
rangement est celui qui exclut**, et le geste le donne. Un entretien qui aurait
proposé « range par difficulté ? » aurait obtenu un oui poli et un brain faux.

**Geste 3 — lire le geste, et le rendre à haute voix.** `induction.py` compte et
rend, en français :

- les paquets, leur clé technique, leur dossier, leur population dans
  l'échantillon, **dans l'ordre où ils ont été nommés** — l'ordre porte souvent
  un sens (chronologique, géographique), et le trier alphabétiquement serait déjà
  une opinion ;
- les titres rangés **nulle part** → il manque un paquet, à lui de le nommer
  *(bloquant)* ;
- les titres rangés dans **plusieurs** paquets → l'axe n'exclut pas, poser 2.3
  puis 2.4 ;
- les paquets qui ne tiennent que par **une** page → garder ou fondre est sa
  décision ;
- deux paquets qui se réduisent à la même clé → renommer *(bloquant)*.

L'utilisateur doit **reconnaître son geste** dans cette lecture. S'il ne le
reconnaît pas, l'induction s'est trompée et il faut y revenir tout de suite —
pas après avoir construit huit blocs par-dessus.

**Geste 4 — dériver ce qui se dérive, demander ce qui se demande.** Le seuil se
calcule du volume ; l'ordre de l'arbre, non.

## 3.3 Le seuil de promotion — la loi, et son honnêteté

Refus n° 4 : le seuil ne se demande **jamais**. L'utilisateur n'a aucun moyen de
le connaître ; le volume, si.

```
seuil = arrondi( 1,6 × (volume_cible / nb_paquets)^(1/3) ),  borné à [3, 20]
```

| Brain | Volume / paquets | Par paquet | Calcul | Seuil |
|---|---|---|---|---|
| DevBrain | 700 / 20 | 35 | 1,6 × 35^⅓ = 5,2 | **5** — le seuil réel du vault |
| HistoBrain | 3000 / 8 | 375 | 1,6 × 375^⅓ = 11,5 | **12** — le seuil écrit au lot 1 |
| CimeBrain | 600 / 7 | 86 | 1,6 × 86^⅓ = 7,1 | **7** |

La loi en racine cubique dit une chose défendable : *un paquet dix fois plus
peuplé ne veut pas dix fois plus de pages par sous-dossier, il en veut environ
deux fois plus* — sinon l'arbre se reforme en liste.

**Elle est calibrée sur les deux seuls points qui existent, et le module le dit
lui-même.** Deux points ne font pas une loi. C'est écrit dans `motif_seuil`, dans
le manifeste de chaque brain produit, et c'est aussi pour ça que `re-seuiller`
existe : le nombre est une **proposition mesurée**, pas une vérité, et une
migration outillée coûte moins qu'un seuil choisi au doigt mouillé.

## 3.4 Ce que l'induction fait quand les réponses ne suffisent pas

**Elle ne complète pas : elle renvoie à une question.** Chaque `Diagnostic` porte
l'identifiant de la question à reposer, la phrase à dire, et un drapeau
`bloquant`. C'est la différence entre un entretien et un formulaire — un
formulaire accepte un champ vide et continue.

| Insuffisance | Question reposée | Bloquant |
|---|---|---|
| moins de dix titres | 2.1 | oui |
| un titre rangé nulle part | 2.2 | oui |
| deux paquets, une seule clé | 2.2 | oui |
| un titre dans deux paquets | 2.3 puis 2.4 | non — c'est un **fait**, pas un défaut |
| un paquet à une seule page | 2.2 | non — sa décision |
| un paquet qu'aucune branche n'atteint | 2.7 | oui |
| un arbre sans branche d'ARRÊT | 2.7 | oui |
| un arbre sans rangs | 2.7 | oui — refus n° 5 |
| une nature à une seule page | 3.2 | non |
| une nature sans frontière | 3.2 | non |
| un titre sans nature | 3.2 | non — le champ reste **vide**, refus n° 8 |
| un dossier transverse qui redouble l'arbre | 4.3 | oui |

## 3.5 Les autres inductions

- **les natures (3.2)** se lisent dans l'étiquetage de l'échantillon : les
  valeurs sont ce qui apparaît, pas ce qu'on propose. L'entretien demande la
  **frontière** avant la définition — c'est la frontière qu'on relit quand on
  hésite ;
- **les axes transverses (4.1)** : zéro est une réponse. Si l'utilisateur propose
  quelque chose qui est déjà un **champ**, l'entretien le dit — un axe transverse
  qui double un champ crée des dossiers que personne n'ouvrira. C'est exactement
  ce qui s'est passé en §4, passe 4 ;
- **le corps (6.1)** porte sur la page d'unité. Les autres rôles reçoivent un
  **squelette** de trois sections, marqué comme tel dans le manifeste — un
  squelette à réécrire, pas une induction. C'est un arbitrage, il est en §8.6.

---

# 4. La transcription — CimeBrain, l'entretien joué

Simulation intégrale, les deux rôles tenus. Abrégée là où elle se répète, jamais
là où elle décide. **E** = l'entretien, **U** = l'utilisateur.

### Passe 0 — identité et dépôt

> **E** — Ça prend une heure à une heure et demie, et la passe 2 en prend le
> tiers : c'est celle où tu vas citer une vingtaine de pages et les ranger à la
> main. On peut s'arrêter n'importe quand. Une seule chose m'arrêtera pour de
> bon : si tu ne me donnes pas le nom et l'adresse sous lesquels signer les
> commits, je ne sème rien. Je ne les devinerai pas. De quoi ce brain
> parle-t-il, en une phrase ?
>
> **U** — Ce que je grimpe et ce que je veux grimper : les courses de montagne,
> ce qu'elles demandent, et ce que j'ai compris de la technique.
>
> **E** — Je la garde telle quelle. Comment veux-tu l'appeler ?
>
> **U** — CimeBrain.
>
> **E** — Personnel, professionnel, ou celui d'un client ?
>
> **U** — Perso.
>
> **E** — Sous quel nom et quelle adresse ses commits doivent-ils être signés ?
>
> **U** — Tu n'as pas déjà mon adresse ?
>
> **E** — J'en ai une sous la main, oui : celle que le harnais m'annonce. C'est
> précisément celle que je ne prendrai pas — elle t'identifie auprès d'un outil,
> elle n'attribue pas un commit, et une adresse entrée dans un historique n'en
> ressort pas sans réécriture. Donne-la-moi.
>
> **U** — floSa, `florian_horellou@laposte.net`.
>
> **E** — Et quelle adresse ne doit *jamais* apparaître dans un commit ici ?
>
> **U** — Tout ce qui est en `@aosis.net`. C'est le pro.
>
> **E** — Noté, et ça verrouille aussi la réponse précédente : je refuserai
> désormais toute identité portant ce domaine, y compris si elle m'arrive par un
> autre chemin. Dans quel dossier veux-tu que ce brain soit semé ?
>
> **U** — `~/Documents/BrainKit-essais/cimebrain`.
>
> **E** — Je lance le semis à blanc dessus tout de suite, pour vérifier le
> chemin sans rien écrire… c'est bon : le dossier n'existe pas encore, il ne vit
> ni sous un dépôt git, ni sous un autre vault.

### Passe 1 — l'unité

> **E** — Dans six mois, tu ouvres ce brain pour t'en servir. Qu'est-ce que tu
> vas chercher ?
>
> **U** — Quoi faire ce week-end. Quelque chose que je peux tenir avec le niveau
> que j'ai, à la saison qu'il fait, dans un massif où je peux aller.
>
> **E** — Alors ce que tu cherches n'est ni un sommet, ni une technique : c'est
> un **itinéraire**, quelque chose qui se fait. Comment appelles-tu cette chose,
> au singulier et au pluriel ?
>
> **U** — Une course, des courses.
>
> **E** — Y a-t-il, à côté, des pages qui n'expliquent pas *quoi faire* mais *ce
> qu'il faut comprendre* ?
>
> **U** — Oui. Le rappel débrayable, la lecture d'un manteau neigeux, la
> progression encordée sur glacier. Ce ne sont pas des courses.
>
> **U** — Et ça, c'est ce que j'ai compris moi. Je ne veux pas qu'une IA le
> réécrive.
>
> **E** — Alors je pose `protege: true` dessus, et ce sera écrit dans le
> `CLAUDE.md` du vault : création libre, modification sur demande explicite. La
> frontière sera portée par le champ `role:`, pas par un dossier — une technique
> et une course vivront côte à côte, et rien dans le chemin ne les distinguera.
> Comment appelles-tu ces pages ?
>
> **U** — Des techniques.
>
> **E** — Dernière de cette passe : y a-t-il des pages qui ne décrivent pas une
> course mais qui **prescrivent** — une règle, une méthode — et qui traversent
> tous les massifs par construction ?
>
> **U** — Oui : « on fait demi-tour à l'heure décidée, pas à l'heure qu'on
> voudrait ». Ça ne dépend d'aucun massif.
>
> **E** — Une règle, donc, dans `Règles/`, préfixée `Règle - `. Elle ne portera
> pas de massif : son chemin se lira sur son rôle.

### Passe 2 — l'axe qui range

> **E** — Cite-moi vingt pages que tu voudrais dans ce brain. Des vraies, pas
> des catégories.
>
> **U** — Le Mont Blanc par les Trois Monts, l'arête des Cosmiques, l'éperon des
> Cosmiques, l'aiguille du Tour…
>
> *(vingt titres, la liste complète est en `tests/cimebrain.reponses.yml`)*
>
> **E** — Range ces vingt en paquets, de ta main. Combien de paquets, et comment
> les appelles-tu ?
>
> **U** — Attends, tu ne me proposes pas des catégories ?
>
> **E** — Non, et c'est délibéré. Si je te propose une liste, tu cocheras — et
> tu t'en apercevras à la trentième page, quand tu ne sauras plus où ranger. Tes
> vingt titres sont sous tes yeux : fais des tas.
>
> **U** — Mont-Blanc, Écrins, Vanoise, Vercors, Pyrénées, Queyras-Ubaye. Six.
>
> **U** — Sauf que la Grande Traversée des Alpes ne rentre nulle part. Je fais
> un septième : Traversées.
>
> **E** — Le septième est né de ta main, pour la vingtième page. Je te relis ce
> que je vois : sept paquets, rangés par **massif** — pas par difficulté, pas
> par saison. Tu as choisi l'axe qui **exclut** : une course est dans un massif
> ou dans un autre, alors que la difficulté et la saison se cumulent. C'est ce
> qui en fait un axe de rangement et pas un axe transverse. Chacune de tes vingt
> tombe-t-elle dans exactement un paquet ?
>
> **U** — Non, deux débordent.
>
> **E** — Le Tour de la Vanoise est dans Vanoise **et** dans Traversées, la
> Grande Traversée des Alpes dans quatre paquets. Pour chacune : est-ce qu'un
> paquet domine quand même, ou couvre-t-elle vraiment tout ?
>
> **U** — Le Tour de la Vanoise ne quitte jamais le massif, donc Vanoise. La
> Grande Traversée va du Léman à la Méditerranée : elle ne domine nulle part.
>
> **E** — Deux mécanismes, alors, et aucun n'invente : une **règle de majorité**
> pour celles qui ont un centre de gravité, et ton paquet `Traversées` comme
> **préfixe transversal** pour celles qui n'en ont pas. Sans ça, tu mentirais
> dans le champ — et le validateur resterait vert, ce qui est le pire des
> résultats. Comment appelles-tu ce que ces paquets sont ?
>
> **U** — Des massifs.
>
> **E** — Combien de pages ce brain aura-t-il quand il sera plein ?
>
> **U** — Six cents, à vue de nez. Et le seuil de sous-dossier, je le mets à
> combien ?
>
> **E** — Je ne te le demanderai pas, parce que tu n'as aucun moyen de le
> connaître — mais le volume, si. 600 pages sur 7 massifs font 86 pages par
> massif ; le seuil sort à **7**, et j'écris le calcul dans le manifeste. Si le
> brain grandit autrement, `re-seuiller` refera l'arbre par `git mv`.
>
> **E** — Dernière, et c'est la plus importante de la passe. Pour chaque paire
> de massifs qui pourrait se disputer une course : quelle question **fermée**
> tranche ? Je peux te proposer les questions ; leur **ordre** restera à toi,
> parce qu'une page se range à la première question qui répond oui — donc
> l'ordre décide.
>
> **U** — Alors la première, ce n'est pas de la géographie : « est-ce que ça
> enjambe plus de deux massifs sans qu'aucun ne domine ? ». Sinon la Grande
> Traversée tombera dans le Mont-Blanc juste parce qu'elle y passe. Ensuite
> Mont-Blanc, Écrins, Vanoise, Vercors, Pyrénées, Queyras-Ubaye, et une
> huitième : aucun des précédents, on demande.
>
> **E** — C'est exactement ça, et c'est *la* décision de conception de ta
> taxonomie. Ta huitième branche est un **arrêt** : un massif manquant ne
> s'invente jamais, il se nomme.

### Passe 3 — l'axe qui qualifie

> **E** — Deux courses du même massif peuvent-elles être de deux natures très
> différentes ?
>
> **U** — Franchement oui. L'arête des Cosmiques et une cascade de glace à
> Ceillac n'ont rien à voir.
>
> **E** — En regardant tes vingt : quelles natures vois-tu ? Étiquette-les.
>
> **U** — Rocher, neige, glace, mixte, ski, randonnée, cascade.
>
> **E** — Sept. Pour chacune, ce que je veux n'est pas la définition mais la
> **frontière** : qu'est-ce qui la distingue de sa voisine la plus proche ?
> Neige contre glace, par exemple.
>
> **U** — Le piolet plante dans la neige, il s'ancre dans la glace.
>
> **E** — Voilà un fait vérifiable, c'est ce qu'il faut. Et « ski » ?
>
> **U** — Ski, c'est un moyen, pas un terrain.
>
> **E** — Je l'écris tel quel dans la frontière : *« la seule valeur de l'axe
> qui décrive un mode de déplacement, et c'est assumé »*. Une incohérence
> déclarée vaut mieux qu'une taxonomie propre et fausse. Y a-t-il des
> informations qui n'ont de sens que pour certaines de ces natures ?
>
> **U** — La cotation glace, pour la glace, le mixte et les cascades. La pente
> maximale, seulement pour le ski.
>
> **E** — Deux champs conditionnels. Un champ qui décrirait 100 % des pages ne
> discriminerait rien.

### Passe 4 — les axes transverses

> **E** — Y a-t-il une question que tu poseras au brain et qui traverse tous les
> massifs ?
>
> **U** — La saison. Et la difficulté, non ?
>
> **E** — La saison, oui : « qu'est-ce que je peux faire en mars ? » traverse
> tout. La difficulté, non — et la raison est mécanique : tu m'as déjà donné une
> **cotation**, et ce sera un champ du frontmatter. Un axe transverse qui double
> un champ crée un dossier de hubs que personne n'ouvrira, parce que la question
> se pose mieux par un filtre. Tu peux en avoir zéro, un ou plusieurs ; je n'en
> inventerai aucun.
>
> **U** — Alors un seul : les saisons.
>
> **E** — Multivalué ?
>
> **U** — Oui, une course peut se faire au printemps et en été.
>
> **E** — Le dossier qui les rassemble ?
>
> **U** — `Saisons/`.
>
> **E** — Il ne redouble aucun nom de ton arbre, c'est bon. Le DevBrain a nommé
> le sien `Métiers/` et non `Domaines/` pour cette raison exacte.

### Passe 5 — le haut de page

> **E** — Tu ouvres une course. Avant le texte, quels trois à cinq faits
> veux-tu voir ?
>
> **U** — Le terrain, la cotation, le dénivelé et la durée, l'engagement. Et si
> c'est beau.
>
> **E** — Les quatre premiers, oui — et « si c'est beau » n'entre pas, parce que
> je te demanderais alors de quel champ il vient, et il n'y en a aucun. Une
> colonne dérivée d'un jugement et non d'un champ n'entre pas dans le bandeau :
> je ne saurais pas la remplir, et je la remplirais au juge. Le dénivelé et la
> durée, c'est une cellule ou deux ?
>
> **U** — Une seule, « 1400 m / 6 h ».
>
> **E** — Un champ qualifié par un autre, donc. Et quand un de ces faits manque
> sur une page, on affiche quoi ?
>
> **U** — Rien.
>
> **E** — Un tiret cadratin, alors, et la règle qui va avec : une cellule sans
> source affiche un tiret, **jamais** une valeur plausible. Une fiche vide
> honnêtement vaut mieux qu'une fiche remplie au juge.

### Passe 6 — le corps

> **E** — Sur une page de course, que veux-tu lire, dans l'ordre ?
>
> **U** — Ce que c'est. Ce qui passe et ce qui ne passe pas. Sur place. Autour.
> Voir aussi. Et mes sorties, quand j'en ai faites.
>
> **E** — « Ce qui passe / Ce qui ne passe pas » est une section où tu
> **décides** : deux colonnes. Ce qui va dans la négative, ce ne sont pas des
> défauts, ce sont des **bornes** — « pas avant mi-juin, le pont de neige ne
> tient plus » — et des **redirections** vers une autre course. « Sur place » ?
>
> **U** — L'accès, le refuge, le matériel, le créneau. Toujours les quatre.
>
> **E** — Quatre étiquettes, vocabulaire **fermé**, et je ne le compléterai pas :
> quatre étiquettes que tu as nommées valent mieux que six dont deux inventées.
> « Sorties » ne se pose que s'il y en a une, donc je la déclare conditionnelle
> et datée — une section vide sur toutes les pages est une section à supprimer du
> gabarit, et le kit doit pouvoir le mesurer.

### Passe 7 — les liens et le résumé

> **E** — Deux courses peuvent-elles être en opposition ? En complément ?
>
> **U** — Il y a « s'enchaîne avec » — deux courses qu'on fait dans le même
> week-end. Et « variante de ».
>
> **E** — Si A s'enchaîne avec B, est-ce que B s'enchaîne avec A ?
>
> **U** — Oui.
>
> **E** — Symétrique. Et si A est une variante de B ?
>
> **U** — Non, l'inverse c'est « B a pour variante A ».
>
> **E** — Alors ce n'est pas un miroir, c'est une **paire** de champs :
> `variante_de` et `variantes`, chacun déclarant l'autre. Je ne forcerai pas la
> symétrie — c'est le trou que le test à blanc « histoire » avait trouvé, et le
> validateur refuse une paire mal déclarée. Quel champ est le résumé d'une ligne
> qu'on recopiera chez tous ceux qui citent la page ?
>
> **U** — `resume`.

### Passe 8 — ce qui rassemble

> **E** — Tes courses sont-elles interchangeables ? En choisit-on une **contre**
> une autre ?
>
> **U** — Oui et non. Pour un week-end donné, je choisis.
>
> **E** — Creusons, parce que la réponse décide de la forme d'une page entière.
> Est-ce qu'en faire une rend l'autre inutile ?
>
> **U** — Non, pas du tout. Je les ferai toutes les deux, un jour.
>
> **E** — Alors elles ne sont pas interchangeables, et je ne te proposerai pas
> de page qui les « départage » — le mot serait faux à l'écrit. Y a-t-il quand
> même une **table** que tu voudrais voir ?
>
> **U** — Oui : par massif, triée par cotation. Ce que je peux faire là-bas, du
> plus facile au plus dur.
>
> **E** — Une sélection, donc, avec sa vue embarquée. Veux-tu un dossier qui les
> rassemble toutes ?
>
> **U** — `Sélections/`.
>
> **E** — Et chaque sélection portera un lien retour vers ce hub : c'est le lien
> retour qui fait la grappe dans le graphe, pas le dossier.

### Passes 9 et 10

> **E** — Les mots-clés transverses : vocabulaire fermé ou libre ?
>
> **U** — Fermé.
>
> **E** — Je le recommande, et le fichier naîtra **vide** avec sa règle : les
> tags d'un autre brain sont ceux d'un autre sujet. Une suppression de page :
> permise, ou toujours à te demander ?
>
> **U** — À me demander.
>
> **E** — Un second mode, pour travailler *depuis* ce brain dans un autre dépôt ?
>
> **U** — Non.
>
> **E** — Réponse légale : le DevBrain en a un parce que son consommateur est un
> dépôt de code ; toi, non. Quels fichiers vis-tu à la racine du vault, et lequel
> cite tes hubs ?
>
> **U** — Une page d'accueil et une inbox.
>
> **E** — L'accueil **aiguille** — c'est lui, et lui seul, qui rend atteignables
> les hubs de premier niveau. L'inbox vit à la racine **sans** aiguiller : une
> page qu'elle mentionne ne devient pas atteignable pour autant. Veux-tu un
> dossier d'atelier, vide dès le premier jour, que le validateur ne lira pas ?
> Je te le demande une fois, et je te dis le coût : le `Projects/` du DevBrain
> porte zéro page en dix-huit mois. Par défaut, il n'y en a aucun.
>
> **U** — Un seul : `Carnet/`, mes comptes rendus bruts écrits le soir même.
>
> **E** — Il naîtra vide, et il sera hors du périmètre du validateur — sinon tes
> comptes rendus seraient lus comme des pages fautives. Dernière passe : que
> produiras-tu **à partir** de ce brain ?
>
> **U** — Une fiche de course prête à partir : l'itinéraire, le matériel, les
> créneaux, et ce qu'on fait si ça ne passe pas.
>
> **E** — C'est ce qui décide de ton troisième skill. Sans cette réponse je n'en
> aurais généré que deux — mieux vaut deux skills que trois dont un inventé.

### Clôture

> **E** — Je te redis l'ensemble, et je ne veux qu'un seul oui, parce que les
> incohérences sont *entre* les blocs, pas dedans.
>
> > Ton brain s'appelle CimeBrain, il parle de ce que tu grimpes et de ce que tu
> > veux grimper. Son unité est la **course**. Il se range par **massif**, en
> > sept paquets dont un transversal, et l'axe n'est pas exclusif : une règle de
> > majorité et le paquet `Traversées` s'en occupent. Une course porte un
> > **terrain** pris dans sept valeurs, et le champ peut rester **vide** quand
> > l'arbre ne tranche pas. Un axe le traverse : les saisons. Le haut de page
> > montre quatre faits, tous adossés à un champ. Le corps a dix sections, dont
> > une prose, une décision à deux colonnes, une étiquetée à quatre étiquettes
> > fermées et une conditionnelle. Deux relations : une symétrique, une paire
> > inverse. Les sous-dossiers se promeuvent à **7** pages, dérivé de tes 600.
> > Les dix règles sont **toutes en attente de mesure** — je ne sais pas écrire
> > `dure`. Les départages et les frontières naissent **vides** : elles se
> > rempliront page par page, quand un arbitrage se répétera. Trois skills, dont
> > le troisième parce que tu m'as dit ce que tu produiras. Et un dossier
> > d'atelier, `Carnet/`, que tu m'as demandé.
>
> **U** — Oui.
>
> **E** — *(semis)* Ton brain existe. Neuf hubs, **aucune autre page** : je n'ai
> rien écrit à ta place. Les deux validateurs sont verts, zéro violation et zéro
> avertissement, et les générateurs ne trouvent aucun écart. Tes vingt titres
> sont dans `Inbox.md`, en cases à cocher — c'est ton premier backlog. Le dépôt
> est initialisé, signé `floSa <florian_horellou@laposte.net>`, ses trois hooks
> sont actifs et `git status` est vide.

## 4.1 Ce que la transcription montre, et qu'un questionnaire ne montrerait pas

Six moments où l'entretien **n'a pas** transcrit :

1. **Passe 0** — l'adresse était sous la main, il l'a refusée et l'a expliquée.
2. **Passe 2.2** — il a refusé de proposer les paquets, et le septième est né de
   la main de l'utilisateur pour la vingtième page.
3. **Passe 2.3** — il a lu le débordement au lieu de le laisser passer, et a
   distingué le Tour de la Vanoise (majorité) de la Grande Traversée
   (transversal). Sans cette distinction, l'utilisateur aurait menti dans le
   champ et le validateur serait resté vert.
4. **Passe 4** — l'utilisateur proposait un second axe transverse ; l'entretien
   l'a **retiré**, en montrant que c'était déjà un champ.
5. **Passe 5** — « si c'est beau » a été refusé comme colonne de bandeau, faute
   de champ source.
6. **Passe 8** — « oui et non » a été creusé jusqu'à une réponse utilisable, et
   le mot « comparatif » n'est jamais apparu.

Aucun de ces six n'est un détail de forme. Chacun change le manifeste produit.

---

# 5. Le contrôle négatif — l'identité git

C'est le second critère d'acceptation du lot, et il est joué par
`tests/entretien.py`, scénario 2.

## 5.1 Pourquoi ce refus est d'une autre nature que les douze autres

Les douze autres protègent la **qualité** d'un manifeste : une valeur inventée y
est une faute réparable. Celui-ci protège une **signature** : une adresse
inventée entre dans l'historique d'un dépôt, et elle n'en sort pas sans
réécriture d'historique. C'est le seul refus qui **arrête** l'entretien.

## 5.2 Trois filets, parce qu'un seul a déjà lâché

| # | Filet | Ce qu'il attrape |
|---|---|---|
| 1 | la **provenance** — seule `utilisateur` est acceptée | une réponse marquée `harnais`, `environnement`, `git-global`, `devine`, `kit`, `exemple` |
| 2 | le **domaine** — l'identité ne peut porter un domaine nommé par 0.5 | l'accident réel : l'adresse pro annoncée par le harnais est exactement celle que 0.5 interdit |
| 3 | l'**environnement** — égalité avec `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_EMAIL`, `EMAIL`, ou le `user.email` de la config git **globale** | une adresse lue quelque part et recopiée, présentée comme une réponse |

Le troisième a l'air paranoïaque. Il ne l'est pas : c'est la seule façon de
distinguer *« l'utilisateur a répondu cette adresse »* de *« quelque chose l'a lue
et l'a recopiée »*, quand la provenance, elle, se déclare.

## 5.3 Mesuré

| Cas | Résultat |
|---|---|
| 0.4 sans réponse | `arret()` rend un motif nommant le harnais ; `compose()` rend `None` ; **le dossier cible n'existe pas** |
| `--provenance harnais`, adresse `@aosis.net` | **refusée à l'enregistrement** — rien n'entre dans le brouillon |
| adresse `@aosis.net` présentée comme réponse de l'utilisateur | **refusée** — elle porte le domaine que 0.5 vient d'interdire |
| adresse égale à `GIT_AUTHOR_EMAIL` | **refusée** — l'environnement la portait déjà |
| **identité donnée par l'utilisateur** | **passe** |

Le dernier compte autant que les quatre premiers : **un garde-fou qui refuse
tout ne prouve rien.**

## 5.4 Et sur l'instance semée

Les trois hooks du lot 5 ont été éprouvés à l'envers sur `CimeBrain` :

```
git -c user.email=florian.horellou@aosis.net commit  -> REFUSÉ (pre-commit)
git commit -m "…\n\nCo-Authored-By: …"               -> REFUSÉ (commit-msg)
git commit, identité locale                          -> passe
```

Après les deux refus : `git status` vide, **un seul commit** dans l'historique.

---

# 6. Le mode reprise

Un entretien de quarante-neuf questions ne tient pas toujours en une séance. La
passe 2 prend le tiers du temps à elle seule.

Le brouillon (`entretien.yml`) porte les **réponses**, pas le manifeste : ce qui
a été dit, avec sa provenance et son horodatage. Le manifeste s'en compose à la
fin, et il se recompose autant de fois qu'on veut **sans reposer une question**.

Trois propriétés, et la troisième est la moins évidente :

1. **Rien ne se redemande.** `prochaine()` rend la première question sans réponse
   dont la condition est remplie. *Mesuré : vingt réponses, rechargement, reprise
   exacte à la vingt-et-unième posable.*
2. **Les conditionnelles se sautent toutes seules.** *Mesuré : `3.1 = non` retire
   3.2, 3.3 et 3.4 des restantes, les compte comme sautées et non comme oubliées,
   et le brain se compose sans axe de nature.*
3. **La provenance est stockée avec la réponse.** C'est ce qui rend le refus n° 1
   vérifiable **après coup** : six mois plus tard, on relit le brouillon d'une
   instance et on voit que l'identité git est bien venue de l'utilisateur. Une
   provenance gardée en mémoire vive n'aurait rien prouvé.

`--oublier <id>` est le **seul** moyen de rouvrir une question. Un brouillon ne
s'édite pas à la main pendant un entretien, précisément à cause de la propriété 3.

En reprenant, `--rappel` relit les dernières réponses **à haute voix**. Une
reprise qui redémarrerait sans rappeler forcerait l'utilisateur à se souvenir de
ce qu'il a dit la semaine dernière — et il répondrait autrement, ce qui est pire
qu'une question reposée.

---

# 7. Ce que l'entretien refuse d'écrire — les treize, mesurés

`uv run brainkit entretien --refus` les imprime. Les treize portent un
**contrôle**, et les contrôles tournent sur le brouillon *et* sur le manifeste
composé — certains ne se voient qu'une fois le manifeste assemblé.

| # | Refus | Contrôle | Vérifié par |
|---|---|---|---|
| 1 | l'identité git | provenance + domaine + environnement | scénario 2, 5 cas |
| 2 | le nom de l'unité et des rôles | 1.2 répondue ; lexique du dev refusé sauf `assume: true` | scénario 6 |
| 3 | les paquets | ≥ 10 titres, 2.2 répondue | scénario 3 |
| 4 | le seuil | 2.6 répondue ; `motif_seuil` non vide | scénario 3 |
| 5 | l'ordre des arbres | `ordre_de_l_utilisateur`, rangs présents | scénario 3 |
| 6 | toute sévérité | aucune règle active hors `a_mesurer` | scénario 6 |
| 7 | le vocabulaire de tags | `vide: true` | scénario 6 |
| 8 | une nature non tranchée | `vide_autorise: true` | scénario 6 |
| 9 | l'existence d'un rôle `vue` | pas de rôle `vue` sans 8.1/8.2 | composeur |
| 10 | l'existence d'un axe transverse | pas plus d'axes que demandé en 4.1 | composeur |
| 11 | départages et frontières | listes vides | scénario 6 |
| 12 | une colonne sans source | source présente et connue du dictionnaire | scénario 6 |
| 13 | le livrable | pas de skill d'exploitation sans 10.1 | composeur |

**Le refus n° 2 a une sortie de secours, et elle est écrite.** Un utilisateur qui
emploie de lui-même un mot du lexique du dev — un maçon dont l'unité *est* la
brique — l'impose en marquant sa réponse `assume: true`. La sortie laisse une
trace, et elle est à lui. Sans elle, le kit imposerait son vocabulaire par la
négative, ce qui serait le même défaut à l'envers.

---

# 8. Les arbitrages

## 8.1 `Projects/` — il disparaît comme dossier, il renaît comme déclaration *(renvoyé)*

Remontée 4 du lot 5 : *« le DevBrain porte un `Projects/` que son manifeste ne
nomme que dans `genere.non_pages` — c'est exactement le genre de dossier qu'un
utilisateur ne demandera jamais et regrettera de ne pas avoir. »*

Deux issues étaient possibles :

- **le coder en dur dans le semis** — toute instance naîtrait avec un dossier que
  personne n'a demandé. La mesure du DevBrain condamne cette issue : son
  `Projects/` porte **zéro page en dix-huit mois**. Poser un dossier vide dans
  chaque brain neuf est exactement l'arbitrage 3.3 du lot 5 à l'envers — *une
  page vide dans un graphe est un nœud de plus qui ne rassemble rien* ;
- **le déclarer** — c'est celle-ci.

**Tranché : `racine.dossiers[]`**, et la question **9.6** qui le remplit.

```yaml
racine:
  dossiers:
    - { chemin: "Carnet/", role_editorial: atelier,
        motif: "les comptes rendus bruts, avant d'en tirer quoi que ce soit" }
```

Trois propriétés, et chacune répond à une moitié du problème :

1. **Le défaut est ZÉRO dossier.** Rien n'est posé que l'utilisateur n'ait
   demandé.
2. **La question est posée UNE fois, avec son coût annoncé.** L'entretien dit la
   mesure avant la réponse — « le `Projects/` du DevBrain porte zéro page en
   dix-huit mois ». C'est ce qui sauve le « il ne le demandera jamais » sans
   tomber dans le « on lui impose ».
3. **Le premier segment doit figurer dans `genere.non_pages`**, et une
   pré-condition de semis le vérifie. Sans ça, le contenu d'un carnet serait lu
   comme des pages fautives — un dossier d'atelier ne porte ni rôle ni catégorie.

Le schéma et le semis sont touchés dans un **commit séparé et explicite**, comme
le lot l'exige : le manifeste était en cause.

## 8.2 Le manifeste par défaut est celui du vault *(renvoyé)*

Remontée 3 du lot 5, avancée du lot 10 à ce lot-ci. `valider` et `generer`
prenaient `exemples/devbrain.brain.yml` et `../DevBrain` : des défauts de
**développement du kit**, pas d'usage.

Le pire n'était pas l'échec, c'était le **silence**. Un vault d'histoire validé
contre le manifeste du dev échoue partout, et un utilisateur qui ne connaît pas
le kit conclut que son brain est cassé.

**`brainkit/defauts.py`, partagé par les cinq commandes :**

1. `--manifeste` donné → celui-là ;
2. sinon `<vault>/brain.yml` → le manifeste de l'**instance** ;
3. sinon, et **seulement** si le vault est le défaut de développement du kit →
   `exemples/devbrain.brain.yml`, **en le disant** ;
4. hors de ces trois cas, on s'arrête. *Deviner un manifeste, c'est deviner
   contre quoi on juge.*

Le vault par défaut devient le **dossier courant** s'il porte un `brain.yml` :
c'est le cas d'usage — l'utilisateur tape `brainkit valider` dans son brain.

**L'incohérence se dit**, en toutes lettres, avant le verdict :

```
ATTENTION — le vault porte SON manifeste (`…/cimebrain/brain.yml`, brain
« CimeBrain ») et tu valides contre `…/histobrain.brain.yml` (brain « HistoBrain »).
    Ce ne sont pas le même brain. Ce qui suit juge « CimeBrain » contre les
    règles de « HistoBrain » : les violations n'auront pas de sens.
```

Un `--manifeste` donné l'emporte **toujours** : c'est un ordre, et le kit n'a pas
à le contredire. Les trois commandes qui **écrivent** (semer, re-seuiller,
freeze) refusent en revanche le repli du cas 3 : acceptable pour un verdict, pas
pour une migration.

**Ergonomie, pas règle** : aucune règle nouvelle, aucune sévérité changée, aucun
code de sortie déplacé. Les trois jeux d'épreuve antérieurs passent inchangés.

## 8.3 `racine:` est rempli par la passe 9.5 *(renvoyé)*

Le bloc existe depuis le lot 5 et aucune règle ne le lit encore (c'est le lot 8).
Ce que ce lot devait garantir est qu'il soit **rempli correctement**, et il l'est
par une question dédiée :

- `porte_d_entree` — le fichier qui cite les hubs de premier niveau ;
- `pages[]` — tous les `.md` de la racine, et aucun autre ;
- `aiguille` — **la moitié qui compte** : une inbox vit à la racine sans
  aiguiller ;
- `amorce` — les titres cités en 2.1, qui atterrissent là et nulle part ailleurs.

Défaut si l'utilisateur ne dit rien : une porte et une inbox — la réponse des
deux remplissages de référence, posée comme un défaut **annoncé**, pas comme une
devinette.

## 8.4 Quarante-neuf questions, et le cadrage est en retard

Voir §2.1. Le cadrage §3.1 dit quarante-cinq ; il en manque quatre pour que
l'entretien puisse produire ses deux propres exemples. C'est une **remontée**
(§9.1), pas une correction unilatérale du cadrage : ce document ne réécrit pas
la spécification, il constate l'écart et le chiffre.

## 8.5 Le seuil se dérive par une loi calibrée sur deux points

Voir §3.3. L'alternative — demander le seuil — est le refus n° 4 ; l'alternative
inverse — poser une constante — aurait donné 5 partout, c'est-à-dire quarante
sous-dossiers par période sur un brain d'histoire. La loi est le moindre mal,
elle est écrite dans chaque manifeste avec son calcul, et elle se dit elle-même
provisoire.

## 8.6 Le corps des rôles secondaires est un SQUELETTE, et il le dit

La question 6.1 porte sur la page d'unité — c'est le cadrage, et c'est
défendable : décrire six corps de page ferait une passe de trente minutes.

Les autres rôles reçoivent donc trois sections minimales, et le manifeste porte
une entrée `<squelette>` dont le `motif:` dit exactement cela :

> *SQUELETTE, pas induction. La question 6.1 porte sur la page d'unité ; le corps
> d'une page « technique » n'a pas été décrit. Trois sections minimales sont
> posées pour que le gabarit existe, et elles sont à réécrire au premier usage.
> Les laisser telles quelles six mois serait le signe qu'il fallait reposer la
> question.*

L'entretien accepte aussi une réponse 6.1 **par rôle** (un dictionnaire), et
c'est alors celle de l'utilisateur qui passe. Le squelette est un repli déclaré,
pas un choix silencieux. Remontée §9.2.

## 8.7 La palette du graphe est posée, pas demandée

C'est la **seule** valeur visible que l'entretien écrit sans l'avoir demandée :
une couleur par fonction de rôle. Ce n'est pas un des treize refus, et la raison
est assumée — une couleur de graphe est une convention de lecture, pas une
décision de taxonomie ; elle se change dans Obsidian en trois clics ; et
l'entretien a de meilleures questions à poser avec le temps qu'il coûterait.
Écrit ici pour que ce ne soit pas une omission silencieuse.

## 8.8 Le brouillon voyage avec l'instance

Le semis pose `AI/entretien/entretien.yml` **si et seulement si** l'entretien en
a fourni un. Ce n'est pas un vestige : c'est la seule trace de **pourquoi** la
taxonomie est celle-là, au-delà des `motif:`. « Pourquoi sept paquets et pas
cinq ? » se relit dans le rangement que l'utilisateur a fait de sa main.

Un manifeste écrit à la main n'a pas de brouillon, et le semis n'en fabrique pas
un : une trace inventée serait la pire des traces.

## 8.9 Un seul skill instancié, et c'est celui de la reprise

Le lot 5 pose l'emplacement des trois skills du brain sans les écrire, et son
motif est juste : *poser un skill à moitié serait pire que ne pas en poser — il
serait chargé, et il mentirait.* Le lot 7 les écrira.

`reprendre-l-entretien` fait exception parce que **tout ce qu'il dit se dérive du
manifeste qu'on vient d'écrire** : l'unité, l'axe, les paquets, le seuil, les
rôles protégés, le chemin du brouillon. Il est donc complet, ou il n'est pas.

Il ne fait pas le même travail que le skill du kit. Celui du kit **mène** un
entretien depuis rien ; celui-ci **rouvre** une question sur un brain qui existe,
et il annonce le **prix** de chaque changement avant de le faire :

| Ce qu'on change | Ce que ça coûte |
|---|---|
| un `motif:`, une définition, une frontière | rien |
| une colonne de bandeau | une régénération |
| une section du corps | le gabarit ; les pages écrites ne bougent pas |
| **le seuil** | une **migration** par `git mv` |
| **retirer une valeur de l'axe** | des pages **orphelines** |
| **renommer un rôle** | chaque page, le gabarit, les hubs, l'index, le graphe |

## 8.10 `--semer` compose dans un temporaire

Le plan d'écriture du semis refuse une cible qui vit sous un dossier portant un
`brain.yml` — *« un brain ne se sème pas dans un autre brain »*. Poser le
manifeste composé à côté du brouillon, puis semer dans un sous-dossier du même
endroit, déclenche donc ce refus, et le message parle d'un vault qui n'existe
pas.

`--semer` compose donc dans un fichier **temporaire**, hors de l'arborescence de
la cible ; le semis le copie de toute façon à la racine de l'instance, et c'est
cette copie qui devient le manifeste du brain. Un `--composer` explicite mal
placé est **refusé avec la raison écrite**, plutôt que de laisser le semis rendre
un message trompeur. Remontée §9.6.

---

# 9. Remontées

## 1. Le cadrage §3.1 compte quarante-cinq questions ; il en faut quarante-neuf

Et le manque n'est pas cosmétique : **aucune question du cadrage ne crée un rôle
`fonction: prescription`**, alors que les deux remplissages de référence en
portent deux chacun. Un entretien fidèle à §3.1 à la lettre n'aurait su produire
ni `Patterns/` + `Rules/`, ni `Controverses/` + `Méthodes/`.

Les trois autres manques (0.6, 9.5, 9.6) sont plus vénielles : deux sont des
conséquences du lot 5, la troisième est opérationnelle.

**À corriger dans `00-cadrage.md` §3.1 et §3.5** au premier lot qui rouvre le
cadrage. Non corrigé ici : ce document constate l'écart, il ne réécrit pas la
spécification d'un autre lot.

## 2. Le corps des rôles secondaires n'est pas induit

Voir §8.6. La vraie réponse serait une question 6.1 **par rôle**, posée seulement
pour les rôles qui existent — deux à quatre questions de plus, cinq minutes
chacune. L'entretien accepte déjà la réponse ; il ne la **demande** pas.

**À trancher au lot 7**, qui écrit les skills et qui verra le premier ce que
valent ces squelettes à l'usage.

## 3. `existe_si` reste du français non évaluable

Confirmé sur un **troisième** manifeste : `roles[].corps[].genre: conditionnelle`
porte un `existe_si:` en français (« au moins une sortie datée »). Ni le
validateur ni le semis ne peuvent l'évaluer ; le gabarit le rend en commentaire.

C'est la remontée 5 du lot 5, inchangée, et la mesure qu'elle appelle est
toujours la même : *une section qui n'existe sur aucune page au bout de N pages
est une section à supprimer du gabarit, pas à laisser « au cas où »*. **Lot 8.**

## 4. La loi du seuil est calibrée sur deux points

Deux points ne font pas une loi, et le module le dit lui-même. Le troisième point
(CimeBrain, 600/7 → 7) n'en est pas un : il est **produit** par la loi, pas
observé. La loi ne se validera que le jour où un brain réel aura assez de pages
pour qu'on mesure si son seuil était juste — ou pour qu'on le re-seuille.

**À rouvrir quand un brain tiers atteint son volume cible.** Rien à faire d'ici là,
sinon garder le calcul écrit là où on le relira : dans `motif_seuil`.

## 5. `page_atteignable` ne lit toujours pas `racine:` — et le bloc a grossi

Remontée 1 du lot 5, **toujours ouverte** : le validateur lit
`racine.glob("*.md")` et non `racine.pages[].aiguille`. Ce lot y **ajoute** un
champ (`dossiers[]`) sans que la règle en lise davantage.

Le durcissement est le lot 8, et l'interdiction de ce lot est explicite. La
mesure à faire n'a pas changé : sur DevBrain, neuf `.md` à la racine dont un seul
aiguille — combien de pages perdraient leur atteignabilité si les huit autres
cessaient de compter ? Si la réponse est zéro, le durcissement est gratuit.

## 6. Le refus « sous un vault » ne distingue pas un vault d'un manifeste posé

`plan._controle_la_cible` refuse une cible dont un parent porte `brain.yml` **ou**
`.obsidian`. C'est juste pour un vault semé ; ça l'est moins pour un dossier de
travail où un `brain.yml` vient d'être **composé** et où rien n'a encore été
semé. Le message parle alors d'un « vault » qui n'existe pas.

Contourné dans l'entretien (§8.10), **non corrigé** : c'est un garde-fou du lot 5,
et le desserrer demande de savoir distinguer « un manifeste posé » de « un vault
semé » — probablement par la présence d'un `.git` ou d'un hub. À traiter au
**lot 10**, avec l'emballage, où les chemins d'usage réels seront tous connus.

## 7. `libelles.prescription` est un singulier pour une liste de rôles

Le schéma offre **un** `libelles.prescription`, alors que `roles[]` en accepte
plusieurs (DevBrain : `pattern` + `rule` ; HistoBrain : `controverse` +
`methode`). Le composeur écrit le premier et l'annonce dans le `motif:` du bloc.

Sans conséquence tant que `roles[]` fait foi — et il fait foi partout dans le
code. À nettoyer si `libelles` devient un jour une source pour autre chose que la
prose générée.

## 8. `--reponses` accepte un lot entier

C'est ce qui rend le jeu d'épreuve possible : rejouer un entretien complet sans
conversation est la seule façon de **prouver** qu'un entretien produit un vault
vert. C'est aussi une porte pour remplir un brain sans entretien du tout.

Ce n'est pas un défaut — un utilisateur qui sait ce qu'il veut a le droit de
l'écrire — mais c'est une facilité qui contourne les treize refus au moment de
la **conversation**, et non au moment du contrôle : les refus tournent toujours
sur le brouillon et sur le manifeste. À surveiller au **lot 10**, si l'emballage
documente cette porte comme un usage.

---

# 10. Comment rejouer

```bash
# les onze passes et les 49 questions, avec ce que chacune produit
uv run brainkit entretien --questions

# les treize refus, en liste fermee
uv run brainkit entretien --refus

# rejouer l entretien CimeBrain, du brouillon au vault
uv run brainkit entretien --brouillon <b.yml> --reponses tests/cimebrain.reponses.yml
uv run brainkit entretien --brouillon <b.yml> --etat
uv run brainkit entretien --brouillon <b.yml> --verifier
uv run brainkit entretien --brouillon <b.yml> --semer <dossier>             # a blanc
uv run brainkit entretien --brouillon <b.yml> --semer <dossier> --ecrire

# le jeu d epreuve du lot 6 — 7 scenarios, 49 verifications
uv run tests/entretien.py

# les lots anterieurs, inchanges
uv run tests/epreuve.py          # lot 3
uv run tests/generation.py       # lot 4
uv run tests/semis.py            # lot 5
uv run schema/valider.py         # lot 1
uv run outils/fidelite.py        # lot 2
```

Sur une instance, les deux commandes de tous les jours n'ont plus besoin d'options :

```bash
cd ~/Documents/BrainKit-essais/cimebrain
uv run brainkit valider          # prend `./brain.yml` tout seul
uv run brainkit generer          # --check par defaut, n ecrit rien
```

Et l'identité ne se devine nulle part :

```bash
grep -rnE "GIT_AUTHOR|GIT_COMMITTER|--author|-c user\." brainkit/entretien/
# -> le module qui les REFUSE, et lui seul
```

---

# 11. Ce qui reste au lot 7

- **Les trois skills du brain**, instanciés depuis le manifeste que l'entretien
  vient d'écrire : la table de propagation est déjà **dérivée** (P1→P7), les
  libellés sont déjà là, et le nom des trois skills est déjà dans `skills:`.
- **Le corps des rôles secondaires** (remontée 2) : le lot 7 est le premier à
  voir ce que valent les squelettes quand un skill de capture s'en sert.
- **Le mode lot du skill de capture** : `skills.capture.mode_lot: true` est écrit
  par le composeur, avec son motif — les vingt titres de `Inbox.md` sont son
  premier travail, et sans mode lot l'amorçage coûte une conversation par page.
