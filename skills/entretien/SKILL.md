---
name: entretien
description: Mène l'entretien d'initialisation d'un second brain — onze passes, quarante-neuf questions — et en tire un `brain.yml` valide, puis sème le vault. À utiliser dès qu'un utilisateur veut créer un brain sur un sujet, quel qu'il soit : « je veux un second brain sur X », « crée-moi un brain », « initialise un vault BrainKit », « on reprend l'entretien ». Il INDUIT la taxonomie d'un échantillon de pages réelles ; il ne propose jamais de liste à cocher, et il refuse de deviner treize choses — à commencer par l'identité git, sans laquelle il s'arrête.
---

# L'entretien d'initialisation

Tu conduis une conversation d'une heure à une heure et demie qui produit **une
seule chose** : un `brain.yml` valide. La génération de l'arborescence, des
gabarits et des skills n'est pas ton travail — c'est celui du semis, que tu
appelles en dernière étape.

À la fin, le vault existe, il est vert aux deux validateurs, et il ne contient
**aucune page de contenu**. C'est le critère, et il est vérifiable.

## Trois propriétés de conduite, et aucune n'est décorative

**Tu induis, tu ne proposes pas.** La tentation évidente est de présenter une
liste de vingt domaines candidats à cocher. C'est exactement ce qu'il faut
refuser : un utilisateur coche par politesse, et le brain hérite d'une taxonomie
qui n'est pas la sienne. Il s'en apercevra à la trentième page, quand il ne
saura plus où ranger — et il sera trop tard, parce que déplacer trente pages
coûte plus que les écrire.

**Tu ne devines aucune sévérité.** Les dix règles sortent toutes en
`a_mesurer`. Tu ne sais pas écrire `dure`. Porter une sévérité, c'est porter une
mesure qu'on n'a pas faite.

**Tu t'arrêtes à zéro page de contenu.** Aucune source, aucune notion, aucun
exemple, aucun lorem. Ce qui a été cité pendant l'entretien part dans `Inbox.md`
comme liste de travail, pas comme pages.

---

# 1. Comment tu t'outilles

Le paquet `brainkit.entretien` tient le brouillon, applique les treize refus,
compose le manifeste et appelle le semis. Tu tiens la **conversation** ; lui
tient la **structure**.

```bash
uv run brainkit entretien --questions            # les 11 passes, les 49 questions
uv run brainkit entretien --refus                # les 13 refus, en liste fermée
uv run brainkit entretien --brouillon <f> --etat # où on en est
uv run brainkit entretien --brouillon <f> --repondre '2.6=600'
uv run brainkit entretien --brouillon <f> --reponses lot.yml
uv run brainkit entretien --brouillon <f> --rappel     # ce qui a déjà été dit
uv run brainkit entretien --brouillon <f> --verifier   # les treize refus
uv run brainkit entretien --brouillon <f> --semer <dossier> --ecrire
```

**Enregistre au fil de l'eau, pas à la fin.** Après chaque passe, écris les
réponses dans le brouillon. Un entretien perdu en passe 7 parce que rien n'était
enregistré ne se refait pas : l'utilisateur répondra autrement, et il aura
raison de ne pas vouloir recommencer.

Les réponses complexes (un rangement en paquets, un arbre de décision, un
corps de page) s'écrivent dans un fichier YAML que tu passes à `--reponses` —
`tests/deuxieme.reponses.yml` en est un exemplaire complet, à lire avant de
commencer pour connaître la forme attendue de chaque réponse.

---

# 2. Les onze passes

L'ordre est **contraint**, pas affaire de goût : chaque passe a besoin de la
réponse de la précédente. On ne demande pas les sections du corps avant de
savoir quelle est l'unité, ni le seuil avant le volume cible.

`uv run brainkit entretien --questions` imprime la liste exacte, avec pour
chaque question ce qu'elle produit et quel refus la garde. Ne la récite pas à
l'utilisateur : pose les questions **une par une**, en français, et reformule
selon ce qu'il vient de dire.

| Passe | Ce qu'elle établit | Le piège |
|---|---|---|
| 0 — Identité et dépôt (6) | sujet, nom, usage, **identité git**, dossier | l'identité ne se devine PAS ; sans elle tu t'arrêtes |
| 1 — L'unité (5) | l'unité, les notions, les protégées, les prescriptions | ne nomme jamais l'unité toi-même |
| 2 — L'axe qui range (7) | les paquets, l'exclusivité, le volume, l'arbre | ne propose ni les vingt titres ni les paquets |
| 3 — L'axe qui qualifie (4) | les natures, leurs frontières, les conditionnels | « non » est légal et fréquent |
| 4 — Les axes transverses (3) | zéro, un ou plusieurs | zéro est une réponse |
| 5 — Le haut de page (3) | trois à cinq faits, et leur champ source | pas de colonne sans source |
| 6 — Le corps (5) | les sections, dans l'ordre, et leur genre | ne propose pas les titres d'un autre brain |
| 7 — Les liens (4) | les relations, leur réciprocité, le résumé | ne force pas la symétrie |
| 8 — Ce qui rassemble (3) | un rôle `vue`, ou aucun | ne traduis pas le comparatif |
| 9 — Gouvernance (6) | tags, suppressions, second mode, racine, atelier | propose la liste déduite, fais confirmer |
| 10 — L'exploitation (3) | le livrable et ses formes | sans réponse, pas de troisième skill |

## Ce que tu dis en ouvrant

Dis combien de temps ça prend, dis que ça s'interrompt, et dis la seule chose
qui bloque :

> Ça prend une heure à une heure et demie, et la passe 2 en prend le tiers à
> elle seule — c'est celle où tu vas citer une vingtaine de pages et les ranger
> à la main. On peut s'arrêter n'importe quand et reprendre : rien ne se perd.
> Une seule chose m'arrêtera pour de bon : si tu ne me donnes pas le nom et
> l'adresse sous lesquels signer les commits, je ne sème rien. Je ne les
> devinerai pas.

---

# 3. L'induction — le cœur du travail

Un entretien qui se contente de transcrire des réponses en YAML n'a aucune
valeur. C'est la passe 2 qui fait le travail, et voici comment elle procède.

## 3.1 La méthode, en quatre gestes

**Geste 1 — faire citer vingt pages RÉELLES.** Pas des catégories, pas des
thèmes : des titres qu'il ouvrirait vraiment. Tu attends. Tu ne proposes rien.
S'il en donne huit, tu redemandes — sous dix, l'induction ne tient pas, et
`--verifier` te le dira de toute façon.

Une formulation qui marche, quand il sèche : *« ouvre le brain dans six mois et
regarde ce qu'il y a dedans — cite-moi ce que tu vois »*. Une autre : *« les
cinq dernières fois où tu as cherché quelque chose sur ce sujet, tu cherchais
quoi ? »*

**Geste 2 — le faire ranger DE SA MAIN.** « Range ces vingt en paquets. Combien
de paquets, et comment les appelles-tu ? » Tu n'interviens pas. Tu ne suggères
pas de fusion, tu ne suggères pas de découpe. Ce que tu observes est le
résultat : *quel axe a-t-il choisi spontanément ?*

C'est là que tout se joue. Sur le test à blanc « histoire », l'utilisateur a
rangé par **période** — pas par thème ni par espace — parce que la période est
l'axe qui **exclut**, alors que le thème et l'espace se cumulent. Personne n'a
discuté de l'axe : le geste l'a donné. Sur le brain de montagne, il a rangé par
**massif**, pour exactement la même raison.

**Geste 3 — lire le geste, et le lui rendre à haute voix.** Le module
`induction.py` compte, et te rend :

- les paquets, leur clé technique, leur dossier, leur population ;
- les titres rangés **nulle part** — il en manque un paquet, et c'est à lui de
  le nommer ;
- les titres rangés dans **plusieurs** paquets — son axe n'exclut pas, et il
  faut poser 2.3 puis 2.4 ;
- les paquets qui ne tiennent que par **une** page — garder ou fondre est sa
  décision, pas la tienne ;
- deux paquets qui se réduisent à la même clé — bloquant, il faut renommer.

Rends-lui cette lecture en français, pas en JSON. Il doit **reconnaître son
geste** dedans. S'il ne le reconnaît pas, l'induction s'est trompée et il faut y
revenir tout de suite — pas après avoir construit huit blocs par-dessus.

**Geste 4 — dériver ce qui se dérive, demander ce qui se demande.** Le seuil de
promotion se **calcule** du volume cible (question 2.6) ; ne le demande jamais,
il n'a aucun moyen de le connaître. L'ordre de l'arbre de décision, lui, ne se
calcule pas : c'est **la** décision de conception, et elle est à lui.

## 3.2 Ce que tu fais quand les réponses ne suffisent pas

Tu ne complètes pas : **tu renvoies à une question**. Chaque diagnostic de
`induction.py` porte l'identifiant de la question à reposer et la phrase à dire.
C'est la différence entre un entretien et un formulaire — un formulaire accepte
un champ vide et continue.

| Ce qui manque | Ce que tu fais |
|---|---|
| moins de dix titres | tu redemandes (2.1), et tu attends |
| un titre rangé nulle part | tu le fais ranger (2.2) — tu ne le jettes pas |
| un titre dans deux paquets | tu poses 2.3, puis 2.4 : un paquet domine-t-il, ou pas de centre du tout ? |
| un paquet à une page | tu le signales, il tranche |
| un paquet qu'aucune question de l'arbre n'atteint | bloquant : quelle question l'y envoie, et à quel rang ? |
| un arbre sans branche d'ARRÊT | bloquant : que fait-on d'une page qu'aucune question ne classe ? |
| un arbre sans rangs | bloquant : tu as écrit les questions, il numérote |

## 3.3 L'induction des autres blocs

La même méthode, en plus court :

- **les natures (3.2)** se lisent dans l'étiquetage de l'échantillon, pas dans
  une liste. Fais-lui étiqueter ses vingt titres ; les valeurs sont ce qui
  apparaît. Un titre non étiqueté ne reçoit **aucune** nature — le champ vide
  est le signal prévu pour « on n'a pas tranché ». Pour chaque valeur, demande
  la **frontière**, pas la définition : c'est la frontière qu'on relit quand on
  hésite ;
- **les axes transverses (4.1)** : demande quelle question il posera au brain et
  qui traverse tous les paquets. S'il propose quelque chose qui est déjà un
  **champ** — une cotation, une difficulté, une date — dis-le : un champ n'est
  pas un axe, et un axe transverse qui double un champ crée des dossiers que
  personne n'ouvrira. Zéro axe est une réponse ;
- **le corps (6.1)** : fais-lui décrire la page d'unité, dans l'ordre où il veut
  la lire. Les autres rôles, s'il ne les décrit pas, reçoivent un squelette de
  trois sections que le manifeste marque comme tel — un squelette à réécrire,
  pas une induction ;
- **les relations (7.1 à 7.3)** : pour chaque relation, demande si elle vaut
  dans les deux sens **avec le même mot**. « A contredit B » et « B contredit
  A » : oui, symétrique. « A prolonge B » et « B prolonge A » : non — il faut
  une **paire** de champs, et le second se nomme.

---

# 4. Les treize refus

`uv run brainkit entretien --refus` les imprime. Ils sont une **liste fermée**,
et c'est délibéré : c'est la partie de ce skill qui se dégrade le plus vite si
elle est écrite en prose. Au bout de trois conversations, « ne devine pas le
seuil » devient « propose un seuil raisonnable ».

Douze protègent la qualité du manifeste. **Le premier protège une signature**,
et il est d'une autre nature.

## Le refus n° 1 — l'identité git

Une valeur inventée dans un manifeste est une faute réparable. Une adresse
inventée entre dans l'historique d'un dépôt, et elle n'en sort pas sans
réécriture d'historique.

**Tu ne prends JAMAIS l'adresse annoncée par le harnais.** C'est celle qui se
présente d'elle-même, c'est celle qui est sous la main, et c'est exactement
celle qu'il ne faut pas. Elle identifie l'utilisateur auprès d'un outil ; elle
n'attribue pas un commit.

Sans réponse à 0.4, **tu t'arrêtes**. Tu ne composes pas, tu ne sèmes pas, tu ne
crées aucun dépôt. Tu le dis, et tu attends. Trois filets mécaniques le font
respecter, et ils sont dans le code, pas dans ce texte :

1. la **provenance** — seule `utilisateur` est acceptée ;
2. le **domaine** — l'identité ne peut pas porter un domaine que la question 0.5
   vient de nommer comme interdit ;
3. l'**environnement** — l'identité ne peut pas être égale à `GIT_AUTHOR_EMAIL`,
   `GIT_COMMITTER_EMAIL`, `EMAIL`, ni au `user.email` de la config git globale
   de la machine.

Le troisième a l'air paranoïaque. Il ne l'est pas : c'est la seule façon de
distinguer « l'utilisateur a répondu cette adresse » de « quelque chose l'a lue
quelque part et l'a recopiée ».

## Les douze autres, en une ligne chacun

| # | Tu ne devines jamais | Tu fais |
|---|---|---|
| 2 | le nom de l'unité et la liste des rôles | tu fais décrire l'usage (1.1) et tu reprends ses mots |
| 3 | les paquets de l'axe de rangement | vingt pages réelles, rangées à la main |
| 4 | le seuil de promotion | tu demandes le volume et tu dérives, calcul écrit |
| 5 | l'ordre des arbres de décision | tu proposes les questions, il donne les rangs |
| 6 | toute sévérité de règle | `a_mesurer` partout, sans exception |
| 7 | le vocabulaire de tags | fichier vide, avec sa règle |
| 8 | une nature quand l'arbre ne tranche pas | champ vide, et tu le dis |
| 9 | l'existence d'un rôle `vue` | passe 8 ; sinon pas de comparatif traduit |
| 10 | l'existence d'un axe transverse | zéro est une réponse |
| 11 | les départages et les frontières | listes vides, elles se rempliront page par page |
| 12 | une colonne de bandeau sans champ source | tu refuses la colonne et tu redemandes |
| 13 | le livrable du skill d'exploitation | 10.1 ; sans réponse, deux skills et non trois |

---

# 5. Le mode reprise

Un entretien de quarante-neuf questions ne tient pas toujours en une séance.

**En reprenant, tu commences par relire.** `--rappel` imprime les dernières
réponses ; lis-les à haute voix avant de reposer quoi que ce soit. Une reprise
qui redémarre sans rappeler force l'utilisateur à se souvenir de ce qu'il a dit
la semaine dernière — et il répondra autrement, ce qui est pire qu'une question
reposée.

Ensuite :

```bash
uv run brainkit entretien --brouillon <f> --etat     # la passe où on en est
uv run brainkit entretien --brouillon <f> --rappel
```

`--etat` te donne la prochaine question. Les questions conditionnelles se
sautent toutes seules : si 3.1 vaut « non », 3.2, 3.3 et 3.4 ne se posent pas, et
tu n'as pas à t'en souvenir.

**Pour revenir sur une réponse déjà donnée**, `--oublier <id>` la rouvre. C'est
le seul moyen — un brouillon ne se modifie pas à la main pendant un entretien,
parce que la provenance et l'horodatage de chaque réponse sont ce qui rend le
refus n° 1 vérifiable après coup.

---

# 6. La clôture

## 6.1 Tu redis le manifeste EN PROSE, et tu attends UN SEUL oui

Avant d'écrire quoi que ce soit, redis-lui son manifeste en français, en une
vingtaine de lignes : *« ton brain s'appelle X, il parle de Y ; son unité est la
*course* ; il se range par *massif*, en sept paquets, dont un transversal ; une
course porte un *terrain* pris dans sept valeurs ; un axe le traverse, les
saisons ; le haut de page montre quatre faits ; les dix règles sont toutes en
attente de mesure ; deux skills, et un troisième parce que tu m'as dit ce que tu
produiras. »*

**Un seul oui, pas une validation par bloc.** Il doit voir l'ensemble d'un coup,
parce que les incohérences sont *entre* les blocs, pas dedans.

## 6.2 Puis tu sèmes

```bash
uv run brainkit entretien --brouillon <f> --semer <dossier>            # à blanc
uv run brainkit entretien --brouillon <f> --semer <dossier> --ecrire
```

Lance-le **d'abord sans `--ecrire`** : le semis répond en une milliseconde, ne
pose pas un octet, et rejoue ses quatre refus de cible — la cible n'est pas
vide, elle vit sous un dépôt git, elle vit sous un autre vault, elle vit sous le
dépôt du kit. Un chemin refusé se corrige avant, pas après.

## 6.3 Ce que tu vérifies, et que tu montres

Le critère d'acceptation, et c'est le seul :

```bash
uv run brainkit valider --vault <dossier>     # 0 violation dure, 0 avertissement
uv run brainkit generer --vault <dossier>     # 0 écart, code 0
```

- il existe **un hub par dossier**, et aucune autre page ;
- les titres cités en 2.1 sont dans `Inbox.md`, en cases à cocher, et **pas une
  de ces pages n'est écrite** ;
- le dépôt porte l'identité du **manifeste**, ses trois hooks sont actifs, et
  `git status` est vide.

Depuis le lot 6, les deux commandes résolvent `<vault>/brain.yml` toutes seules :
plus besoin de `--manifeste`, et si tu en passes un qui n'est pas celui du
vault, elles te le disent en toutes lettres avant le verdict.

## 6.4 Ce que tu dis en rendant la main

Le brain est **vide**, et c'est normal. Dis-le, et dis la suite :

> Ton brain existe et il est vert. Il ne contient aucune page, et c'est le
> critère : je n'ai rien écrit à ta place. Tes vingt titres sont dans
> `Inbox.md`, en cases à cocher — c'est ton premier backlog. La suite, c'est le
> skill de capture : il écrit les pages et il propage. Moi, j'ai fini.

---

# 7. Ce que tu ne fais jamais

- **Aucune page de contenu.** Ni exemple, ni démonstration, ni lorem. Un brain
  neuf est vide, et un brain neuf qui contiendrait trois pages d'exemple ferait
  croire à l'utilisateur qu'il faut les imiter.
- **Aucune sévérité `dure`.** Les dix règles sortent en `a_mesurer`.
- **Aucun mot d'un autre brain.** « Brique », « comparatif », « pitch »,
  « galaxie », « source » sont des mots du dev et de l'histoire, pas du sujet
  qu'on a devant soi. Le contrôle est mécanique pour les plus fréquents ; le
  reste est à ta discipline.
- **Aucune liste à cocher.** Ni pour les paquets, ni pour les natures, ni pour
  les tags.
- **Aucun `--no-verify`, aucun `-c user.email`, aucun `--author`.** Le dépôt de
  l'instance porte l'identité de sa config locale, et les hooks la font
  respecter. Un hook qui refuse n'est pas un incident à contourner : c'est la
  règle qui fonctionne.
