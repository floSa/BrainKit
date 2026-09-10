# Recette — capturer une page

> **Pour qui** : un agent de code lancé **dans le dossier du vault**, pas dans
> le dépôt du kit. Système de fichiers et terminal. Aucune clé d'API.
>
> **Quand** : « ajoute X au brain », « documente Y », « capture ces cinq
> pages », ou en fin de conversation « mets à jour le brain ».
>
> **Ce que ça produit** : la page demandée **et tout son rayon de propagation**,
> clôturés ensemble.
>
> **Critère de fin** : chaque ligne du rayon est **honorée** ou **déclarée sans
> objet** — aucune tue — et la clôture est passée
> ([`cloturer-une-ecriture.md`](cloturer-une-ecriture.md)).

---

> **Où tu lances ces commandes.** `uv run brainkit …` se lance **depuis le
> dépôt du kit** ; `uv tool install --editable <dépôt du kit>` met `brainkit`
> sur le PATH ; une instance **figée** se lance depuis elle-même
> (`uv run AI/scripts/valider.py`). Le vault est toujours désigné par
> `--vault`, et il ne vit jamais sous le dépôt du kit.


## 0. Lis d'abord ce que ce vault-ci dit

Cette recette donne la **méthode**. Les **valeurs** — les rôles, les axes, les
sections, le rayon exact — sont dans les documents que le semis a générés pour
ce brain, depuis son manifeste :

```
<vault>/docs/enrichir.md        ← le rayon de propagation, ligne par ligne
<vault>/docs/manuel.md          ← comment ce vault se lit
<vault>/CLAUDE.md               ← le routeur, s'il existe
<vault>/Documentation/…/taxonomie.md   ← les arbres de décision
```

Ils sont **générés** : ils ne s'éditent pas à la main, et ils sont à jour du
manifeste par construction. Une recette générique ne peut pas les remplacer —
elle ne connaît pas les mots de ce sujet.

> Si `<vault>/docs/enrichir.md` n'existe pas (profil `nu`, ou instance
> ancienne), la table du rayon reste dérivable : `uv run brainkit generer
> --vault <vault> --quoi hubs --check` te dit ce que les hubs attendent, et le
> manifeste porte tout le reste.

## 1. Le principe, et il n'y en a qu'un

**Le rayon d'une insertion est le DOSSIER D'ACCUEIL, plus ses HUBS PARENTS. Le
voisinage d'une page est `ls` de son dossier.**

Tu ne crées pas une page : tu déclenches une propagation. Une page nouvelle
change une dizaine d'autres choses, et si on ne les change pas, le vault ment.

## 2. Les six gestes, dans l'ordre

**Geste 1 — trouver le dossier, sans le deviner.** Le chemin se **dérive** de la
valeur de l'axe de rangement, jamais de l'intuition. Déroule l'arbre de décision
de `Documentation/<axe>/taxonomie.md` : questions fermées, ordre strict, la
première réponse positive gagne. **Si aucune question ne tranche : laisse le
champ vide et demande.** Une valeur inventée range la page au mauvais endroit
pour toujours.

**Geste 2 — vérifier que le nom est libre.** Le nom de fichier doit être unique
dans le vault, **à la casse près** — c'est la seule contrainte que le wikilink
nu impose, et elle mord surtout là où un même mot est déjà un dossier, un hub ou
une notion.

**Geste 3 — écrire la page au gabarit de son rôle.** `Templates/` porte un
gabarit par rôle, généré depuis le manifeste. Les champs requis sont requis ; un
champ hors de la liste `autorises` fait échouer la validation. Une section
`conditionnelle` ne se pose pas vide.

> **Rien qui ne soit sourcé.** Une cellule sans source reste vide et se signale.
> Une fiche vide honnêtement vaut mieux qu'une fiche remplie au jugé.

**Geste 4 — faire le tour du dossier, `ls` à la main.** Pour chaque page du
dossier, **lis son `role:` dans le frontmatter** — le chemin ne le dit pas. Puis
traite chaque ligne du rayon :

| Ligne | Ce que tu fais |
|---|---|
| le hub du dossier, et les hubs parents | rien : leurs zones AUTO sont générées. Mais **relis leur corps** — il est écrit à la main, et il peut être devenu faux |
| la vue / séquence du dossier | la vue embarquée prend la page toute seule si elle filtre sur l'axe. Les sections écrites à la main, non |
| la notion du dossier | à écrire, **dans les deux sens**. Rôle **protégé** : la créer est normal, **modifier une page qui existe déjà demande une demande explicite**. Sinon : proposer, et attendre |
| les pairs — les autres pages d'unité du dossier | à écrire, **réciprocité obligatoire**. Un pair écarté est un CHOIX, pas un oubli : le dire |
| les résumés réinjectés | le résumé se **copie** depuis la cible, il ne se retape pas |
| les hubs d'axe transverse | rien : générés depuis les valeurs que la page porte |

**Une ligne sans objet se déclare sans objet.** « Ce dossier ne porte aucune
page de notion — faut-il en créer une ? » est une réponse. Le silence n'en est
pas une.

**Geste 5 — vérifier le rayon, par une commande et non par relecture.**

```bash
uv run brainkit valider --vault <vault>
uv run brainkit generer --vault <vault>        # --check par défaut
```

**Geste 6 — clôturer.** [`cloturer-une-ecriture.md`](cloturer-une-ecriture.md).
Ce n'est pas une étape facultative : c'est elle qui régénère et qui commite.

---

## 3. Mettre à jour une page qui existe : un autre mode

Une page qu'on crée n'a pas de consommateurs ; une page qui existe en a. Jamais
un patch improvisé.

`<vault>/docs/enrichir.md` porte la **table des effets de bord**, champ par
champ : qui lit ce champ, et par quelle commande on vérifie. Elle est dérivée du
manifeste — bandeau, vues, champs réciproques, conditionnels, champs indexés.
Suis-la ligne à ligne pour chaque champ modifié.

Trois cas qui coûtent cher si on les rate :

- **le `nom:`** entraîne le nom du **fichier**, et le renommage se fait par
  `git mv`. Puis tous les wikilinks qui le citent, dans le corps **et** dans le
  frontmatter ;
- **le résumé court** est recopié chez **toutes** les pages qui citent celle-ci.
  Le modifier sans propager fait mentir leurs puces ;
- **la valeur d'axe de rangement** fait **déménager** la page, par `git mv`, et
  change la population de deux dossiers — donc, peut-être, une promotion ou une
  dépromotion. Ça, c'est `re-seuiller`, pas une capture.

---

## 4. Le mode lot

Capturer plusieurs pages d'un même dossier en une fois, en n'appliquant la
propagation qu'**une** fois à la fin. C'est ce qui rend l'amorçage possible :
sans lui, remplir un brain neuf coûte une conversation par page, et personne ne
le fait.

La discipline change sur un point, et un seul : **le tour du dossier se fait
après la dernière page**, pas après chacune. Tout le reste est identique.

---

## 5. Ce que tu ne fais jamais

- **écrire dans une page d'un rôle protégé sans demande explicite.** La
  frontière est portée par le champ `role:`, jamais par le chemin : une page
  voisine, dans le même dossier, sous le même hub, peut être protégée. **Lis le
  frontmatter avant d'écrire** ;
- **éditer à la main un chemin de `genere:`** — zones AUTO, index, carte des
  liens, hauts de page, gabarits, taxonomie ;
- **poser une valeur d'axe hors du vocabulaire.** Une valeur nouvelle se pose
  dans le manifeste, qui génère la taxonomie — pas dans l'arborescence ;
- **supprimer une page**, ni déplacer autrement que par `git mv` ;
- **durcir une règle** parce qu'elle « paraît évidente ». C'est
  [`mesurer-et-durcir.md`](mesurer-et-durcir.md), et ça se compte d'abord.
