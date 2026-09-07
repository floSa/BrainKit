# BrainKit — les trois skills, instanciés

> Conversation 48, « BrainKit lot 7, les trois skills », le 2026-09-07.
> Spécification d'entrée : `design/00-cadrage.md` §1 briques J1-J2 et K1-K4,
> §5.9 (l'amorçage), §5.12 (le nombre de rôles), et le plan de lots, *Lot 7*.
>
> Livrables du lot : ce document · `brainkit/skills/` (six modules) ·
> `tests/skills.py` · les trois skills générés dans HistoBrain et dans
> CimeBrain · dix captures réelles dans HistoBrain.

## Ce que ce lot a changé par rapport au cadrage

Le cadrage annonçait que la table de propagation « se dérive » (J2) sans dire
**de quoi**, ligne par ligne. L'écrire a forcé sept familles de lignes, un
champ de plus sur chaque ligne (`origine`, ce qui la produit dans le manifeste),
et un second champ (`sans_objet_si`) qui rend la clause vérifiable au lieu de la
laisser à la conscience de celui qui capture.

Deux choses n'étaient pas dans le cadrage et sont dans le lot :

- **le contrôle mécanique du rayon** (`brainkit/skills/controle.py`), sans lequel
  « chaque ligne est soit faite, soit déclarée sans objet » reste une promesse ;
- **la décision de ne PAS écrire le skill d'exploitation** quand le manifeste ne
  déclare pas ce que le brain produit. C'est l'arbitrage 1 ci-dessous.

Aucun des douze points ouverts de §5 n'est tranché ici, hors l'arbitrage sur
l'exploitation que le lot demandait explicitement. Aucune règle de validation
n'a été ajoutée, aucune sévérité changée : tout sort en `a_mesurer`, et c'est le
lot 8 qui durcit.

---

# 1. La dérivation de la table de propagation

## 1.1 L'énoncé, et pourquoi il ne dépend d'aucun sujet

> **Le rayon de propagation d'une insertion est le DOSSIER D'ACCUEIL, plus ses
> HUBS PARENTS. Le voisinage d'une page est `ls` de son dossier.**

Il ne repose que sur un fait de structure : **le dossier porte la valeur de
l'axe de rangement**. Tout brain construit sur l'arbre l'obtient gratuitement.
C'est la brique J1, classée GÉNÉRIQUE dans l'inventaire de séparation, et la
mesure du lot le confirme — elle passe d'un brain de sources d'histoire à un
brain de courses de montagne sans une retouche.

> **Une ligne sans objet se DÉCLARE sans objet, elle ne se tait pas.**

C'est cette clause, et elle seule, qui distingue « j'ai propagé » de « j'ai
écrit une page ». Elle est la raison d'être de la section 3 de ce document.

## 1.2 Les sept familles de lignes, et ce qui les fait naître

Aucune ligne n'est écrite dans `propagation.py`. Chacune naît d'un fait déclaré
dans `brain.yml` :

| Famille | Ce qui la fait naître | Qui fait le travail |
|---|---|---|
| le hub du dossier | un rôle `fonction: hub` | **généré** (zone AUTO) + le corps à relire |
| les hubs parents | `axes.rangement.niveaux > 1` **et** des sous-valeurs déclarées | **généré** + le corps à relire |
| les autres rôles du dossier | chaque rôle `range_par: axe` qui **porte** la valeur d'axe, sauf celui qu'on capture | à écrire |
| les pairs | le rôle qu'on capture, confronté à lui-même, plus ses champs `reciproque:` | à écrire |
| les résumés réinjectés | un champ `fonction: resume_court` **avec** un `reinjecte_dans` | à écrire |
| les hubs de ralliement | un rôle qui déclare `hub_de_ralliement` | zone AUTO générée + **le lien retour** à écrire |
| les hubs transverses | **une ligne par entrée** de `axes.transverses` | généré |

Quatre remarques sur cette table, parce que ce sont les quatre endroits où elle
aurait pu être écrite au lieu d'être dérivée.

**La table dépend du rôle qu'on capture.** Capturer une unité met à jour la
notion du dossier ; capturer la notion met à jour les unités. La ligne « les
pairs » désigne toujours le rôle capturé, et chaque autre rôle rangé par l'axe a
sa propre ligne. `derive(mo, rid)` prend donc le rôle en argument, et le défaut
est le rôle d'unité.

**Les hubs transverses font UNE ligne par axe, pas une ligne pour tous.** Le
DevBrain n'a qu'un axe transverse, et sa table historique n'a qu'une ligne — la
tentation était de garder cette forme. Elle est fausse dès qu'il y a deux axes :
une page peut porter un thème sans porter d'espace, et l'une des deux lignes est
alors **sans objet**, ce qui doit se déclarer séparément. C'est la seule
différence de longueur entre les tables d'HistoBrain et de CimeBrain, et elle
n'est pas cosmétique.

**Le hub de ralliement est la ligne que le DevBrain avait enfouie.** Dans
`enrichir-brain`, le hub `Comparatifs/` apparaît au milieu de la ligne P3, en
incise, comme « un consommateur que le dossier ne rend pas ». C'en est une
ligne à part entière : il vit **hors du dossier**, `ls` ne le rend pas, et il
n'entre dans le rayon que si la capture **crée** une page du rôle rallié. Le
sortir en ligne propre lui donne sa condition de « sans objet », que l'incise
n'avait pas.

**La ligne des hubs parents peut être sans objet POUR TOUJOURS.** Sur un brain
dont l'axe ne déclare aucune sous-valeur — CimeBrain — l'arbre est plat et
aucun dossier n'a de parent. La ligne existe quand même, avec sa condition
écrite : *« toujours, dans ce brain : l'arbre est plat. La ligne existe pour le
jour où une sous-valeur le sera. »* Une ligne retirée serait une ligne qu'on
oublierait de remettre.

## 1.3 Ce que chaque ligne porte en plus de son intitulé

Deux champs, et ils sont le cœur du lot :

- **`origine`** — ce qui, **dans `brain.yml`**, fait exister la ligne.
  `` `roles[chronologie].hub_de_ralliement` ``, `` `champs.apport.fonction:
  resume_court` ``. Une ligne sans origine serait une ligne qu'on ne pourrait ni
  contester ni retirer en changeant le manifeste. Le jeu d'épreuve le vérifie
  sur chacune.
- **`sans_objet_si`** — la seule façon légitime de ne rien écrire pour cette
  ligne, énoncée. Sans elle, « une ligne sans objet se déclare sans objet » est
  une phrase morale ; avec elle, c'est une condition qu'on peut confronter au
  vault.

Un troisième, `genre`, ne sert pas au rendu : il sert au **contrôle**, qui doit
savoir comment trouver les objets d'une ligne dans un vault réel. Vocabulaire
fermé par le kit — c'est du code, pas une donnée.

## 1.4 La table dérivée, pour HistoBrain

Neuf lignes. C'est celle que porte `enrichir-histobrain`, et que `CLAUDE.md`
porte à l'identique.

| # | À mettre à jour | Ce qui la produit dans le manifeste | Sans objet quand… |
|---|---|---|---|
| P1 | le hub du dossier d'accueil | un rôle `fonction: hub` (`hub`) | **jamais** |
| P2 | les hubs parents | `niveaux: 2` et 17 sous-valeurs déclarées | la page atterrit directement dans le dossier de période |
| P3 | la chronologie du dossier | `roles[chronologie]` est `range_par: axe` | le dossier ne porte aucune `role: chronologie` |
| P4 | la notion du dossier | `roles[notion]` est `range_par: axe` | le dossier ne porte aucune `role: notion` |
| P5 | les pairs — les autres `role: source` | le rôle capturé, plus ses `reciproque:` | la page est la première du dossier |
| P6 | les résumés réinjectés (`apport:`) | `champs.apport.fonction: resume_court` + `reinjecte_dans` | aucune puce ajoutée dans ces sections |
| P7 | le hub de ralliement `Chronologies/` | `roles[chronologie].hub_de_ralliement` | la capture ne crée aucune chronologie |
| P8 | les hubs de `themes:` | une entrée de `axes.transverses` | la page ne porte aucun thème |
| P9 | les hubs de `espaces:` | une entrée de `axes.transverses` | la page ne porte aucun espace |

Une note s'ajoute en dessous, dérivée elle aussi : `role: controverse` et
`role: methode` sont `range_par: role`, vivent dans leur dossier, et n'ont donc
**pas ce rayon-là** — leur rayon est leur dossier plus son hub, et les lignes
d'axe sont sans objet.

---

# 2. Le contrôle de généricité — trois manifestes, trois tables

C'est la preuve que la table est dérivée et non recopiée : trois manifestes sans
un mot commun donnent trois tables différentes, et chacune est juste.

| | HistoBrain | CimeBrain | DevBrain |
|---|---|---|---|
| unité | la **source** | la **course** | la **brique** |
| axe de rangement | la **période** | le **massif** | le **domaine** |
| rôles | 6 | 5 | 6 |
| axes transverses | **2** (`themes`, `espaces`) | **1** (`saisons`) | 1 (`domaines`) |
| **lignes de rayon** | **9** | **8** | **8** |
| lignes d'effets de bord | 28 | 20 | 29 |

## 2.1 Ligne par ligne, HistoBrain contre CimeBrain

| # | HistoBrain | CimeBrain |
|---|---|---|
| P1 | le hub du dossier d'accueil | *(identique — la ligne ne cite aucune valeur d'instance)* |
| P2 | les hubs parents · sans objet si la page tombe dans le dossier de **période** | *(intitulé identique)* · **sans objet TOUJOURS** : aucune sous-valeur déclarée, l'arbre est plat |
| P3 | la **chronologie** du dossier — `role: chronologie`, préfixe `Chronologie - ` | la **sélection** du dossier — `role: selection`, préfixe `Sélection - ` |
| P4 | la **notion** du dossier — `role: notion`, **protégé** | la **technique** du dossier — `role: technique`, **protégé** |
| P5 | les autres `role: source` · réciprocité sur `contredit:` (symétrique) **et** la paire `prolonge:` / `prolonge_par:` (inverse) | les autres `role: course` · réciprocité sur `enchaine_avec:` (symétrique) **et** la paire `variante_de:` / `variantes:` (inverse) |
| P6 | `apport:` réinjecté dans « Contredit par » · « Prolonge » · « Prolongée par » | `resume:` réinjecté dans « Variante de » · « Variantes » · « S'enchaîne avec » |
| P7 | le hub de ralliement `Chronologies/`, lien retour dans « Voir aussi » | le hub de ralliement `Sélections/`, lien retour dans « Voir aussi » |
| P8 | les hubs de `themes:` — `Thèmes/` | les hubs de `saisons:` — `Saisons/` |
| P9 | les hubs de `espaces:` — `Espaces/` | **la ligne n'existe pas** : un seul axe transverse |

**Deux lignes seulement sont communes mot pour mot**, et ce sont exactement
celles qui ne citent aucune valeur d'instance : le hub du dossier et les hubs
parents. Elles ne parlent que de la structure de l'arbre, qui est la même
partout — c'est le fait dont toute la règle dépend. Le jeu d'épreuve pose cette
assertion telle quelle, et une ligne de plus en commun le ferait échouer.

Un second contrôle double le premier : **aucun jeton de vocabulaire d'un brain
n'apparaît dans les skills de l'autre** — `role: source`, `prolonge_par`,
`Antiquité`, `contredit:` d'un côté ; `role: course`, `massif`, `terrain`,
`variante_de` de l'autre. Dix-sept jetons, tous vérifiés dans les deux sens.

## 2.2 Une déduplication que CimeBrain a exigée

`cimebrain.brain.yml` porte « Variantes » **deux fois** dans le `reinjecte_dans`
de son champ de résumé, parce que le champ a deux côtés qui visent la même
section. Une table qui la listerait deux fois ferait croire à deux travaux
distincts. `sections_de_reinjection()` déduplique en gardant l'ordre déclaré, et
le motif est écrit à côté. C'est le genre de détail qu'un seul manifeste ne
révèle jamais.

---

# 3. Le contrôle du rayon — de la promesse au fait

## 3.1 Pourquoi ce n'est pas une règle du validateur

Parce qu'il faut savoir **ce qui vient d'être capturé**, et un validateur ne le
sait pas : il voit un vault, pas une session. La liste des fichiers touchés
vient de `git status --porcelain`, c'est-à-dire du travail en cours. Un vault où
toutes les lignes ont été tues depuis six mois est un vault **avec de la dette**,
pas un vault invalide — et le confondre avec une violation ferait échouer la
validation d'un brain repris à froid.

```bash
uv run brainkit/skills/controle.py --vault . --page "<chemin de la page>"
```

## 3.2 Ce qu'il contrôle, et ce qu'il ne contrôle pas

Il ne contrôle que les lignes **à écrire**. Les lignes générées sont déléguées à
`brainkit generer --check` et à la règle `completude_du_hub` ; exiger qu'on les
« touche » ferait sortir un faux défaut à chaque capture.

Il ne dit rien de la **qualité** de ce qui a été écrit, et il le dit : qu'un pair
ait été touché ne prouve pas que la réciprocité est bonne. Les deux se
complètent — **celui-ci trouve les oublis, `valider --regle reciprocite` trouve
les erreurs**.

## 3.3 Les deux précisions que l'usage a payées

| ce qu'il a fallu ajouter | ce qui se passait sans |
|---|---|
| `git status -uall` | git replie un dossier entier non suivi en **une** ligne : un lot de dix pages neuves devenait un seul chemin de dossier, et le contrôle déclarait TUE tout ce qui était neuf |
| `git -c core.quotepath=false` | tout chemin non-ASCII sort échappé en octal (`Antiquit\303\251/`), et aucune comparaison avec le vault ne tient |

Les deux ont été trouvées en lançant le contrôle sur les dix vraies captures, pas
en le relisant. Elles sont écrites dans le code, avec leur motif.

---

# 4. La table des effets de bord — le mode mise à jour

**Règle d'or, et c'est elle qui justifie la table** : une modification de champ
n'est pas finie quand la page est enregistrée ; elle est finie quand ses
**consommateurs** sont à jour. Une page qu'on crée n'a aucun consommateur ; une
page qui existe en a. C'est toute la différence entre le mode ciblé et le mode
mise à jour.

## 4.1 Comment chaque ligne se dérive

Un champ, une ligne. Le branchement se fait sur ce que le champ **déclare**,
jamais sur son nom — c'est la même discipline de résolution que le moteur de
validation.

| ce que le champ déclare | les consommateurs qui en découlent |
|---|---|
| `fonction: identite` | le nom du fichier (par `git mv`) · les wikilinks du corps **et du frontmatter** · l'unicité du nom · index, hubs, liens |
| `fonction: resume_court` | les puces de chaque section de `reinjecte_dans`, chez **tous** les citeurs · le bandeau s'il le porte |
| `fonction: alias` | la collision d'alias · la résolution des `[[alias]]` |
| `source: axes.rangement` | **change de rayon** : la page déménage · hub quitté et hub d'accueil · les vues filtrées · **le seuil de promotion** |
| `source: axes.nature` | le vocabulaire fermé · **les champs conditionnels dont le `si:` cite ce champ** · la colonne de bandeau |
| `source: axes.transverses[x]` | les hubs de `x.dossier` — celui qu'on quitte peut tomber à zéro page |
| `source: vocabulaires.y` | le fichier `y.fichier`, dans son mode |
| `source: roles[].id` | le gabarit appliqué · le dossier si le rôle change de rangement · la couleur du graphe |
| `reciproque:` | l'autre côté — **l'inverse déclaré** si le mode est `inverse` · la section adossée, des deux côtés · la citation unique |
| `type: liens` | chaque cible doit exister : un lien mort en frontmatter ne se voit pas à la lecture |
| cité par `bandeau.colonnes[]` | la zone AUTO du bandeau |
| présent dans `genere.index.champs` | l'index — donc lu par le skill d'exploitation sans ouvrir la page |
| `eliminatoire:` non vide | le filtre du skill d'exploitation |

Deux lignes n'ont **aucun** champ, et ce sont les plus dangereuses : **renommer
ou déplacer une page**, et **supprimer une page**. Les omettre laisserait le cas
qui produit des liens morts sans procédure. Elles sont dérivées de
`champs de fonction: identite` + `regles_de_socle.nom_egal_fichier` pour la
première, de `frontieres_d_ecriture.jamais_sans_accord` pour la seconde.

## 4.2 Les quatre marqueurs, redéfinis pour un brain neuf

Le DevBrain en a quatre : `[M]` manuel, `[G]` générateur, `[D]` couvert par une
règle **dure**, `[!]` dérive silencieuse. Le troisième ne transpose pas tel
quel : sur une instance neuve, **toutes** les règles sortent en `a_mesurer`.

`[D]` est donc redéfini en « **déclaré** — une règle du validateur le contrôle »,
et le skill porte la précision en encadré :

> Les règles **comptent**, elles ne **bloquent** pas, tant que personne n'a
> mesuré. Une règle ne se durcit qu'après un comptage écrit — c'est le travail
> du lot 8, pas une case à cocher à la volée.

C'est la seule transposition qui demandait un travail de sens plutôt qu'un
renommage.

---

# 5. Le mode LOT — la réponse à §5.9

**Le risque.** À la fin de l'entretien, le vault contient des hubs et zéro page.
Personne ne remplit trois cents pages une conversation à la fois, et un brain à
vingt pages ne rend aucun service.

**Ce que le mode change** — et, surtout, ce qu'il ne relâche pas :

| ce qui change | ce qui ne change pas |
|---|---|
| le rayon s'applique **une fois pour le lot**, pas N fois | la table est remplie **ligne par ligne**, et une ligne sans objet se déclare |
| une seule clôture, un commit par dossier | chaque page est écrite en entier, gabarit respecté |
| les réciprocités **entre pages du lot** se posent au fil de l'eau | les réciprocités avec les pages **déjà là** se posent au rayon |
| le plan passe avant l'écriture | rien ne s'écrit avant le GO |

**Le danger propre au mode lot, et c'est le seul que le mode ciblé n'a pas : le
SEUIL.** Dix pages posées d'un coup peuvent faire franchir le seuil de promotion
à une sous-valeur, et donc promouvoir un sous-dossier **au milieu du lot**. Le
compte se fait sur le lot **entier**, avant d'écrire la première page. Si le lot
promeut, c'est une réorganisation (`brainkit re-seuiller`), et elle passe
**avant** la capture — capturer d'abord et déplacer ensuite double le travail et
perd des liens.

Le mode s'ancre sur la page `role_editorial: capture` de `racine.pages` quand il
y en a une : `Inbox.md` porte le premier backlog, et le skill dit de **cocher au
fur et à mesure, pas à la fin**. Une file à moitié drainée dont rien n'est coché
est une file perdue.

---

# 6. L'arbitrage sur l'exploitation

Le mot « projet » est du dev. La question générique est : **à quoi sert ce brain
quand on l'interroge ?**

## 6.1 Ce qui se généralise : la FORME, pas le livrable

Quatre pas, les mêmes quel que soit le sujet, chacun avec une fin vérifiable :

| # | Pas | Fin d'étape vérifiable |
|---|---|---|
| 1 | identifier la **forme** du livrable | la forme est **nommée**, pas supposée |
| 2 | poser **seulement** les questions pertinentes | les réponses sont écrites, en clair |
| 3 | interroger l'**index**, pas les pages | une liste de candidats **bornée**, avec leur chemin |
| 4 | produire un livrable **sourcé** | chaque affirmation porte un wikilink nu |

Ce qui ne se généralise pas : **ce que le livrable est**. Le kit n'a aucune
intuition là-dessus et n'en fabrique pas. La passe 10 de l'entretien le demande,
avec un refus de deviner écrit, et le manifeste le porte dans
`skills.exploitation.livrable`.

## 6.2 Arbitrage 1 — pas de déclaration, pas de skill

**Si `skills.exploitation` n'est pas déclaré, le skill n'est PAS écrit.** Le
schéma ne le rend pas obligatoire — la passe 10 porte un refus de deviner, et un
utilisateur peut ne pas savoir encore ce qu'il produira.

Un skill d'exploitation qui ne sait pas ce qu'il produit serait une **fiction
chargée à chaque conversation**. C'est exactement le raisonnement qui a fait
attendre le lot 7 pour les trois skills — *« poser un skill à moitié serait pire
que ne pas en poser : il serait chargé, et il mentirait »*. Le README des skills
écrit alors l'absence, et nomme la question qui la répare :

> Aucun skill d'exploitation n'est écrit pour ce brain, et c'est délibéré. […]
> Pour l'écrire : `reprendre-l-entretien`, question 10.1.

**Une absence déclarée vaut mieux qu'une présence creuse.**

## 6.3 Arbitrage 2 — le filtre éliminatoire se lit, il ne se devine pas

`planifier-projet` filtre sur `maturite: deprecated` sans ouvrir les fiches, et
cette sémantique était **écrite dans le skill**, invisible depuis le manifeste.

Le kit la lit désormais dans `champs.<x>.eliminatoire`, **vide par défaut**. Et
quand la liste est vide, le skill l'écrit en clair au lieu de se taire :

> **Rien ne disqualifie une page dans ce brain**, et c'est **déclaré**, pas
> supposé. […] Si l'une doit être écartée, c'est un jugement de la conversation
> en cours, il se dit en clair, et il ne se déguise pas en règle du brain.

C'est la différence la plus instructive entre les deux instances : en histoire,
une source `contestee` est souvent la plus intéressante, et une source `obsolete`
reste un objet d'historiographie.

## 6.4 Ce que le skill garde de `planifier-projet`

L'entrée **par le hub** quand le nom cherché est inconnu — le gain de l'arbre.
Le corps d'un hub est écrit à la main : c'est le jugement du propriétaire du
brain, et aucune requête ne le donne. Les portes dérivées sont énumérées : les
dossiers d'axe transverse, les dossiers de rôles rangés par rôle, les hubs de
ralliement.

Et le **format de sortie** : cadrage, corps, **Écartés** (avec la raison réelle,
jamais un motif inventé), **Ce qui manque** (ce à quoi aucune page ne répond —
une capture à faire, et c'est une autre décision).

---

# 7. Les dix captures — le critère d'acceptation

Dix sources réelles dans HistoBrain, deux dossiers, en mode LOT. Le vault passe
de 11 à **38 pages**.

## 7.1 Ce qui a été écrit

**`Antiquité/` — 5 sources**

| Page | `nature:` | `categorie:` | réciprocité |
|---|---|---|---|
| Hérodote - Enquête | *(vide)* | `antiquite/grece` | `prolonge_par:` → Thucydide |
| Thucydide - La Guerre du Péloponnèse | `source-primaire` | `antiquite/grece` | `prolonge:` → Hérodote |
| Tacite - Annales | *(vide)* | `antiquite/rome` | `contredit:` ↔ Suétone |
| Suétone - Vies des douze Césars | *(vide)* | `antiquite/rome` | `contredit:` ↔ Tacite |
| ORBIS - modèle géospatial du monde romain | `base-de-donnees` | `antiquite/rome` | — |

**`XXe siècle/` — 5 sources**

| Page | `nature:` | `categorie:` | réciprocité |
|---|---|---|---|
| Kennan - Le long télégramme | `source-primaire` | `xxe/guerre-froide` | `prolonge_par:` → article X |
| Kennan - Les sources de la conduite soviétique | `article` | `xxe/guerre-froide` | `prolonge:` → le câble |
| Gaddis - We Now Know | `ouvrage` | `xxe/guerre-froide` | `contredit:` ↔ Hobsbawm |
| Hobsbawm - L'âge des extrêmes | `ouvrage` | `xxe` *(valeur courte)* | `contredit:` ↔ Gaddis |
| Paxton - La France de Vichy | `ouvrage` | `xxe/gm2` | — |

**Ce que le rayon a exigé en plus** — quatre pages et deux fichiers de vue, tous
sortis des lignes P3, P4 et P7, aucun demandé par personne :

- `Antiquité/Historiographie antique.md` (`role: notion`, **protégée**) et
  `XXe siècle/Endiguement.md` — ligne **P4** ;
- `Antiquité/Chronologie - Rome impériale.md` + son `.base`, et
  `XXe siècle/Chronologie - Guerre froide.md` + son `.base` — ligne **P3** ;
- le lien retour `[[Chronologies]]` dans le *Voir aussi* des deux chronologies —
  ligne **P7**, la seule que `ls` du dossier ne rend pas.

Quatre lignes d'`Inbox.md` sont cochées, avec le wikilink de la page qui les a
absorbées : Thucydide, Hérodote, Paxton, ORBIS.

## 7.2 Le rayon honoré, ligne par ligne — `Hérodote - Enquête`

Sortie du contrôle, verbatim, sur le dossier `Antiquité/` :

| # | État | Objets |
|---|---|---|
| P1 | **déléguée** | portée par `generer --check` et `completude_du_hub` |
| P2 | **déléguée** | idem — et P1/P2 désignent ici la même page, l'arbre est plat sous le seuil |
| P3 | **honorée** | `Antiquité/Chronologie - Rome impériale.md` — touché |
| P4 | **honorée** | `Antiquité/Historiographie antique.md` — touché |
| P5 | **honorée** | ORBIS · Suétone · Tacite · Thucydide — tous touchés |
| P6 | **honorée** | `Thucydide` — le seul citeur, son `apport:` recopié dans « Prolongée par » |
| P7 | **sans objet** | *cette capture ne crée aucune `role: chronologie`* — déclarée, pas tue |
| P8 | **déléguée** | les hubs de `themes:` |
| P9 | **déléguée** | les hubs de `espaces:` |

**Aucune ligne tue.** Les douze pages du lot ont été passées au contrôle, une par
une : toutes rendent « chaque ligne du rayon est honorée ou sans objet ».

Les deux chronologies ont un rayon différent, et le contrôle le montre : leur
ligne des pairs est **sans objet** (« la page est la première du dossier ») et
leur ligne P7 est **honorée** — c'est la seule capture du lot qui active le hub
de ralliement, puisque c'est la seule qui crée une page du rôle rallié.

## 7.3 Les réciprocités, dont la paire orientée

Quatre couples, deux par mode, tous verts à `valider --regle reciprocite` :

| mode | couple | ce que le mode garantit |
|---|---|---|
| symétrique | Tacite ↔ Suétone | A cite B **et** B cite A, dans le **même** champ |
| symétrique | Gaddis ↔ Hobsbawm | idem |
| **inverse** | Thucydide `prolonge` Hérodote / Hérodote `prolonge_par` Thucydide | A.X contient B **si et seulement si** B.**Y** contient A |
| **inverse** | Kennan 1947 `prolonge` Kennan 1946 / Kennan 1946 `prolonge_par` Kennan 1947 | idem |

Le mode inverse est la rupture 2 du test à blanc, la seule qui ait exigé une
ligne de code que le DevBrain n'aurait jamais fait écrire. Elle est ici
**exercée sur du contenu réel**, pas seulement déclarée dans un manifeste :
« Thucydide prolonge Hérodote » n'implique pas « Hérodote prolonge Thucydide »,
il implique « Hérodote **est prolongé par** Thucydide ». Écrire le même champ
des deux côtés fabriquerait une relation fausse — le skill le liste dans ses
anti-patterns, dérivé de `paires_inverses()`.

## 7.4 L'état après les dix captures

| contrôle | résultat |
|---|---|
| `brainkit valider` | **aucune violation dure** — 3 avertissements, 13 `a_mesurer` |
| `brainkit generer --check` | **silencieux** — les 37 artefacts concordent |
| `--regle reciprocite` | 0 constat |
| `--regle reinjection_du_resume` | 0 constat |
| `--regle completude_du_hub` | 0 constat |
| `--regle chemin_categorie` | 0 constat |
| hooks git | les trois actifs ; `pre-commit` refuse bien une identité `aosis.net` |

**Les trois avertissements sont délibérés et écrits sur les pages.** Hérodote,
Tacite et Suétone sortent **sans `nature:`**. L'arbre de décision demande
d'abord si le document est contemporain du fait qu'il rapporte, et les trois
écrivent une à deux générations après ; le défaut de l'arbre (`ouvrage`, « livre
d'auteur, appareil critique ») décrit un objet moderne. Le champ vide est le
signal que le manifeste prévoit — *« un champ vide est une question ouverte ;
une valeur inventée est une faute »*. C'est **Remontée 3**.

ORBIS montre le mécanisme inverse, et c'est le meilleur résultat du lot :
l'`Inbox.md` l'appelait « carte des mobilités antiques ». L'ordre strict de
l'arbre donne `base-de-donnees` — N3 (« un corpus qu'on interroge plutôt qu'on
ne lit ») passe **avant** N4 (« la représentation d'un espace »). C'est
exactement ce que l'ordre existe pour trancher, et il a tranché contre
l'intuition de celui qui avait écrit la ligne d'inbox.

**Les treize `a_mesurer` sont tous le même constat**, et il est nouveau : les
treize hubs d'axe transverse nés de ces captures ne sont cités par aucun hub.
C'est **Remontée 1** — le compte est passé de 0 à 13, et le skill de clôture dit
qu'un compte qui augmente doit être vu. Il l'est.

---

# 8. Les arbitrages du lot

**1 — Pas de déclaration d'usage, pas de skill d'exploitation.** §6.2. Une
absence déclarée vaut mieux qu'une présence creuse.

**2 — Le filtre éliminatoire se lit dans `champs.<x>.eliminatoire`, et son
absence s'écrit.** §6.3.

**3 — `CLAUDE.md` rend la table DÉRIVÉE, pas `propagation.table`.** Le routeur
lisait jusqu'ici la table déclarée dans le manifeste ; le skill de capture, lui,
la dérive. Deux tables issues de deux sources dans les **deux fichiers les plus
lus du vault** est le constat E4 en miniature. Le routeur dérive donc lui aussi,
et le jeu d'épreuve vérifie l'égalité ligne par ligne. `propagation.table` reste
dans le manifeste comme **documentation** — voir Remontée 2.

**4 — Le contrôle du rayon n'est pas une sous-commande.** Il vit dans
`brainkit/skills/controle.py`, lançable directement, comme les modules `__main__`
du kit. Ajouter `brainkit rayon` au routeur est une décision d'emballage
(lot 10), et le lot 7 n'a pas à l'anticiper. Voir Remontée 4.

**5 — Une ligne par axe transverse, pas une ligne pour tous.** §1.2. La forme du
DevBrain était juste **parce qu'il n'a qu'un axe**, et fausse dès qu'il y en a
deux.

**6 — Le hub de ralliement devient une ligne à part entière.** §1.2. L'incise du
DevBrain n'avait pas de condition de « sans objet ».

**7 — Le contrôle ne juge que les lignes à écrire.** §3.2. Exiger un « touché »
sur une ligne générée ferait sortir un faux défaut à chaque capture, et le faux
défaut est ce qui tue un contrôle.

**8 — Les commandes sont données en forme courte, avec une ligne de repli.**
`brainkit` n'est sur le PATH d'aucune instance fraîchement semée. Donner une
commande qui ne tourne pas serait pire que n'en donner aucune ; inventer un
chemin d'installation serait pire encore. Voir Remontée 5.

---

# 9. Remontées

*Ce qui a été trouvé hors du périmètre du lot, et qui ne s'y corrige pas. Une
remontée nomme le fait, dit ce qu'il coûte, et propose — elle ne tranche pas.*

**1 — Les hubs d'axe transverse ne sont atteignables depuis rien.** *(lot 4 / 5)*
Mesuré : **13 constats `page_atteignable`** apparus à la première capture réelle,
sur un vault qui en avait zéro. `Home.md` nomme les dossiers `Thèmes/` et
`Espaces/` en texte, pas en wikilink, et les hubs par valeur naissent après le
semis — donc personne ne les cite. Le coût est un compteur qui monte de 13 d'un
coup à la première capture de tout brain neuf ayant un axe transverse, ce qui
noie le signal des vraies dettes. Trois issues : donner un hub d'index à chaque
dossier d'axe transverse (comme les dossiers de rôle en ont un) ; rendre la
section transverse de `Home.md` générée ; ou déclarer ces hubs hors du test
d'atteignabilité. La première paraît la plus propre — le dossier d'un rôle rangé
par rôle en a déjà un, et la symétrie manque.

**2 — `propagation.table` est une seconde source de la table.** *(lot 1 / 6)* Le
schéma la rend **obligatoire** dans `propagation`, et le composeur de l'entretien
l'écrit. Le lot 7 la dérive à la place. Les deux ne divergent pas aujourd'hui sur
le fond, mais elles diffèrent déjà en longueur — 7 lignes déclarées contre 9
dérivées pour HistoBrain, parce que la déclaration replie les deux axes
transverses en une ligne et enfouit le hub de ralliement. C'est exactement le
défaut E4 que le manifeste existe pour supprimer. Deux issues : marquer le champ
`genere: true` et le régénérer depuis la dérivation à chaque composition, ou le
retirer du schéma. La seconde est plus simple ; la première garde un manifeste
lisible seul. **Aucune n'a été appliquée** : toucher au schéma sortait du
périmètre.

**3 — L'arbre de `nature:` d'HistoBrain n'a pas de branche pour un récit antique.**
*(exemple, pas kit)* Mesuré : **3 sources sur 5** du dossier `Antiquité/` sortent
sans `nature:`. La question N1 (« contemporain du fait qu'il rapporte ? ») exclut
tout auteur écrivant une génération après, et le défaut N9 (`ouvrage`, « livre
d'auteur, appareil critique ») décrit un objet moderne. Le mécanisme du kit
fonctionne — le champ vide est le signal prévu, et il a été employé — mais le
**vocabulaire** de l'exemple est incomplet. Proposition : une valeur
`recit-ancien` ou une question N intercalaire, à trancher par
`reprendre-l-entretien` sur l'instance. Ce n'est **pas** un défaut du kit :
c'est le kit qui l'a rendu visible, et c'est ce qu'on lui demande.

**4 — Le contrôle du rayon gagnerait à être une sous-commande.** *(lot 10)*
Aujourd'hui `uv run brainkit/skills/controle.py`, alors que le skill de capture
en fait une étape de sa procédure. Une sous-commande `brainkit rayon --page <x>`
mettrait le critère central du lot dans la boucle de travail au lieu de le
laisser dans le jeu d'épreuve. Coût : une entrée dans le routeur, une aide, un
scénario de plus. Non fait — le routeur est de l'emballage.

**5 — Une instance ne sait pas où vit le kit.** *(lot 5 / 10)* `kit.mode: branche`
dit que le kit est ailleurs, sans dire **où**. Conséquence mesurée : ni
`brainkit valider` ni `uv run brainkit valider` ne résolvent depuis le dossier
d'une instance fraîchement semée — et pourtant `CLAUDE.md` et
`AI/scripts/README.md`, tous deux écrits par le semis, donnent ces commandes
telles quelles. Les skills du lot 7 les donnent aussi, avec une ligne de repli
(`uv run --project <racine du kit>`) qui, elle, fonctionne. Proposition : un
champ `kit.racine:` posé au semis, ou une étape d'installation qui met le kit sur
le PATH.

**6 — `type: date` n'est vérifié par rien.** *(lot 3)* Le contrat déclare le type,
et aucune règle ne contrôle la forme. Constaté en écrivant
`date_publication: "2012"` (une année seule) et `"1946-02-22"` (une date
complète) dans le même corpus : les deux passent, et le bandeau les rend telles
quelles. Le coût est faible et il est réel — un tri par date sur une colonne de
vue mélangera les deux formes. Proposition : une règle de socle
`format_de_champ`, en `a_mesurer`, au lot 8.

**7 — `generated_by` de l'index est vide.** *(lot 4)* `brain-index.json` porte
`"generated_by": ""`, et `brain-index.md` rend `> Généré par ``.`. Cosmétique,
mais c'est la première ligne que lit un humain qui ouvre l'index. Proposition :
`brainkit <version>`.

**8 — Une collision de nom latente entre un hub promu et une notion.** *(lot 5)*
`unicite_du_nom_de_fichier` est **dure** et vérifie les pages existantes. Elle ne
peut pas voir qu'une sous-valeur déclarée porte un libellé — « Guerre froide » —
qui sera un jour le nom d'un dossier **et** de son hub, et qu'une notion de ce
nom entrerait alors en collision. Le cas a été évité dans les dix captures en
nommant la notion `Endiguement`, mais par attention, pas par mécanisme. Coût : la
collision n'apparaîtra qu'au re-seuillage, c'est-à-dire au pire moment.
Proposition : `re-seuiller` refuse une promotion dont le libellé est déjà un nom
de page.

**9 — Le semis n'écrit pas le fichier de `skills.exploitation.archetypes`.**
*(lot 5)* Le manifeste d'HistoBrain déclare `Documentation/perso/usages.md` ; le
semis ne le crée pas, et le skill d'exploitation pointe donc vers un fichier
absent. Le skill le **dit** en clair — « ce fichier peut ne pas exister encore,
et ce n'est pas une erreur : zéro forme est une réponse légale ». Mais un chemin
déclaré et jamais créé est une décision à prendre, pas un silence : soit le semis
l'ouvre vide avec sa règle, comme il le fait pour `tags.md`, soit le champ cesse
d'être un chemin.

**10 — Le lien `[[X.base]]` ne se distingue pas de `[[X]]` dans le graphe.**
*(lot 4, connue)* Rappelée ici parce que les deux chronologies capturées l'ont
exercée : un `.base` n'a pas de frontmatter, donc pas de rôle, donc pas de
couleur. Le fait est déjà écrit dans `graphe.note_base` du manifeste ; rien à
faire, sinon ne pas s'en étonner à la première lecture du graphe.
