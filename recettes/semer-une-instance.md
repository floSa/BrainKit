# Recette — semer une instance

> **Pour qui** : un agent de code, quel qu'il soit. Système de fichiers et
> terminal. Aucune clé d'API.
>
> **Quand** : un `brain.yml` existe — écrit par l'entretien, ou copié de
> `gabarit/brain.yml` et réécrit à la main — et le vault n'existe pas encore.
>
> **Ce que ça produit** : un vault complet et **vide de contenu** : les dossiers,
> un hub par dossier, un gabarit par rôle, la taxonomie, les vocabulaires, le
> routeur d'agent, trois skills, trois hooks git, la couche de ponts,
> `INSTALL.md` et trois guides, le dépôt et son premier commit.
>
> **Critère de fin** : `uv run brainkit valider --vault <cible>` rend **0
> violation dure et 0 avertissement**, `uv run brainkit generer --vault <cible>`
> rend **0 écart**, et il existe **un hub par dossier et aucune autre page**.

---

## 0. Avant de lancer quoi que ce soit

Le manifeste doit passer le contrat :

```bash
uv run schema/valider.py <chemin du brain.yml>
```

S'il échoue, **arrête-toi** : le refus nomme le champ fautif par son chemin dans
le document (`roles[2].fonction`, `bandeau.colonnes[1].source`). Un manifeste
faux sème un vault faux, et le vault ne le dira pas.

## 1. Lance à blanc, TOUJOURS

```bash
uv run brainkit semer --manifeste <brain.yml> --dans <cible>
```

Sans `--ecrire`, le semis ne pose pas un octet. Il répond en une milliseconde et
rejoue ses **quatre refus de cible** :

| Refus | Pourquoi |
|---|---|
| la cible n'est pas vide | on n'écrase pas ce qu'on n'a pas lu |
| la cible vit sous un dépôt git | un vault est son propre dépôt, pas un sous-dossier d'un autre |
| la cible vit sous un autre vault | deux `brain.yml` imbriqués : le validateur ne saurait plus lequel applique |
| la cible vit sous le dépôt du kit | le kit ne contient aucune instance, et il ne doit pas en contenir |

Un chemin refusé se corrige **avant**, pas après. Lis aussi la liste des
fichiers annoncés : c'est le moment de voir qu'un dossier manque ou qu'un rôle
n'a pas de gabarit.

## 2. Écris

```bash
uv run brainkit semer --manifeste <brain.yml> --dans <cible> --ecrire
```

Le semis est **tout ou rien** : s'il manque quelque chose au manifeste, il refuse
et ne pose aucun fichier. Il ne sème jamais à moitié.

Il crée le dépôt git, pose les trois hooks (`.githooks/`), active
`core.hooksPath`, écrit l'identité **du manifeste** dans la config **locale** du
dépôt, et fait le premier commit.

> **Tu ne touches pas à cette identité.** Elle vient de `git.identite` du
> manifeste, que l'entretien a refusé de deviner. Si elle te paraît fausse,
> arrête-toi et demande — ne la « répare » pas avec l'adresse que tu as sous la
> main.

## 3. Vérifie, et montre ce que tu as vérifié

```bash
uv run brainkit valider --vault <cible>
uv run brainkit generer --vault <cible>
git -C <cible> status --porcelain
git -C <cible> log -1 --format='%an <%ae>'
```

Ce que tu dois obtenir, et que tu annonces :

- **0 violation dure et 0 avertissement.** Sur un vault à zéro page d'unité, un
  avertissement porterait forcément sur une page que personne n'a écrite ;
- **0 écart aux générateurs.** Le semis est à son point fixe : ce qu'il pose est
  exactement ce que les générateurs regénéreraient ;
- **un hub par dossier, et aucune autre page.** Compte-les ;
- **`git status` vide**, et le commit porte l'identité du manifeste ;
- les titres cités pendant l'entretien sont dans `Inbox.md`, **en cases à
  cocher**, et **pas une de ces pages n'est écrite**.

## 4. Ce que tu dis en rendant la main

Le brain est vide, et c'est le critère. Dis-le, et dis la suite :

> Ton brain existe et il est vert. Il ne contient aucune page — je n'ai rien
> écrit à ta place. Tes titres sont dans `Inbox.md`, en cases à cocher : c'est
> ton premier backlog. La suite est la capture, recette
> `capturer-une-page.md`. Avant de l'ouvrir dans Obsidian, il y a `INSTALL.md`
> à la racine du vault : il a été écrit pour ce brain-ci.

---

## Les deux cas particuliers

### Semer sans être passé par l'entretien

Copie `gabarit/brain.yml` et **réécris-le**. Rien n'y est à garder tel quel sauf
la forme : chaque libellé, chaque clé d'axe et chaque `motif:` est à remplacer.
Un `motif:` recopié sans être relu est un motif faux.

Les cinq blocs qu'on rate le plus souvent, dans l'ordre où ils se lisent :

1. `libelles` — la langue du sujet. Le kit ne raisonne que sur les six
   *fonctions* (`unite`, `notion`, `hub`, `vue`, `prescription`, `transverse`) ;
   tout le reste est du vocabulaire à écrire ;
2. `axes.rangement.prefixes` — les paquets, et **rien d'autre**. Un axe qui se
   cumule n'est pas un axe de rangement, c'est un axe transverse ;
3. `axes.rangement.seuil_promotion` — se **dérive** du volume cible
   (`volume_cible / nombre de préfixes`), et le calcul s'écrit dans
   `motif_seuil` ;
4. `regles` — **toutes** en `a_mesurer`. Une sévérité est un résultat de mesure
   sur un corpus ; un brain neuf n'a pas de corpus ;
5. `racine.pages[].aiguille` — quelle page de la racine cite les hubs de premier
   niveau. Sans elle, les hubs de premier niveau sont « atteignables depuis
   aucun hub ».

Puis reviens à l'étape 0.

### Changer le seuil après coup

C'est une **migration**, pas une édition :

```bash
uv run brainkit re-seuiller --vault <cible> --seuil <n>          # à blanc
uv run brainkit re-seuiller --vault <cible> --seuil <n> --appliquer
```

Elle émet des `git mv`, elle **refuse de tourner sur un arbre de travail sale**,
et elle **signale** les hubs devenus orphelins sans les supprimer. Un hub
orphelin se supprime à la main, après lecture — jamais par la migration.
