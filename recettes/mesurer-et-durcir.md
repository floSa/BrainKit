# Recette — mesurer une règle avant de la durcir

> **Pour qui** : un agent de code, dans le vault ou à côté. Terminal. Aucune
> clé d'API. **La mesure n'écrit pas un octet dans le vault** — au plus un
> rapport, au chemin qu'on lui donne.
>
> **Quand** : « peut-on rendre cette règle dure ? », « pourquoi cette règle est
> en avertissement ? », ou périodiquement, quand le brain a beaucoup grossi.
>
> **Ce que ça produit** : une décision **chiffrée** — durcir, ou pas — ou un
> refus qui dit exactement ce qui manque pour trancher.
>
> **Critère de fin** : chaque règle proposée au durcissement porte son compte de
> violations, sa population, et un `motif:` **écrit à la main**. Aucune sévérité
> ne change sans ces trois choses.

---

> **Où tu lances ces commandes.** `uv run brainkit …` se lance **depuis le
> dépôt du kit** ; `uv tool install --editable <dépôt du kit>` met `brainkit`
> sur le PATH ; une instance **figée** se lance depuis elle-même
> (`uv run AI/scripts/valider.py`). Le vault est toujours désigné par
> `--vault`, et il ne vit jamais sous le dépôt du kit.


## 1. La règle du jeu, en une phrase

**Une sévérité est un résultat de mesure sur un corpus, pas une propriété de
règle.** Elle ne se porte donc pas d'un brain à l'autre : un brain neuf naît
avec ses dix règles en `a_mesurer`, et c'est cette recette qui les fait
évoluer — jamais l'intuition, jamais la copie d'un autre manifeste.

## 2. Mesurer

```bash
uv run brainkit mesurer --vault <vault>
uv run brainkit mesurer --vault <vault> --regle <id>          # une seule règle
uv run brainkit mesurer --vault <vault> --rapport AI/mesure/<date>-mesure.md
```

Les codes de sortie disent des choses différentes, et il faut les distinguer :

| Code | Ce que ça veut dire |
|---|---|
| **0** | la mesure est faite, et aucun refus ne se tient |
| **1** | garde-fou 2 : au moins une règle en `avertissement` **sans `motif:` écrit**. Le kit refuse |
| **2** | erreur d'usage — vault ou manifeste introuvable |

**Le refus du plancher n'est PAS un code 1**, et c'est délibéré : un vault de
douze pages qui refuse tout durcissement est un vault en bonne santé, pas un
vault en faute.

## 3. Lire les trois garde-fous

Ils ne sont pas des options : ce sont eux qui distinguent une mesure d'une
superstition.

**Garde-fou 1 — le plancher.** Une règle ne se durcit pas sous **30 pages de
l'unité**. Sous le plancher, zéro violation ne dit pas « la règle est
respectée », il dit « la règle n'a rien vu ». Le kit le lit deux fois : le
plancher de l'**instance** (le vault porte-t-il 30 pages du rôle
`fonction: unite` ?) et le plancher de la **règle** (cette règle-là a-t-elle
réellement mesuré 30 pages ?). Une règle dont le dénominateur n'est pas un
volume de corpus — vérifiable sur le **manifeste**, sans lire une page — y
échappe, et c'est le seul cas.

Quand le plancher n'est pas tenu, le kit dit **combien de pages il manque**.
C'est la seule chose à faire : écrire des pages. Il n'y a pas de raccourci.

**Garde-fou 2 — le motif obligatoire.** Une règle qui reste en `avertissement`
doit porter un `motif:` **écrit**. Le kit refuse sinon, et c'est le seul endroit
où le code de sortie change. Corollaire : toute proposition de durcissement
sort avec un emplacement `motif:` **vide et obligatoire**. Le kit sait mesurer ;
il ne sait pas écrire pourquoi.

**Garde-fou 3 — les règles structurellement dures.** La liste est **fermée par
le kit** : une violation y est une incohérence de *structure*, pas un défaut de
rédaction. Un manifeste qui déclare le contraire est **contredit**, et la règle
n'est jamais proposée. Un garde-fou qu'une instance peut désactiver n'est pas un
garde-fou.

## 4. Décider — et ce que tu écris

Pour chaque règle que la mesure propose :

1. **regarde les violations une à une**, pas seulement leur compte. Une règle
   qui sort 4 violations dont 3 sont des faux positifs n'est pas une règle à
   durcir : c'est une règle à **réécrire**. Deux des dix règles du kit ont été
   réécrites pour cette raison exacte ;
2. **si tu durcis** : passe `severite: dure` dans le manifeste, **et répare les
   violations** avant la prochaine clôture. Une règle dure sur un vault qui la
   viole rend le vault rouge en permanence, et un vault rouge en permanence n'est
   plus lu ;
3. **si tu laisses en avertissement** : écris le `motif:`. Pas « à voir plus
   tard » — le motif dit *pourquoi cette règle ne peut pas mordre ici*, et il
   sera relu par quelqu'un qui ne se souviendra de rien ;
4. **si tu désactives** : c'est un `active: false` **avec motif**, et c'est une
   décision plus lourde qu'un assouplissement. Une règle absente ne ressemble pas
   à une règle souple : elle ressemble à une règle satisfaite.

> **On réécrit la règle plutôt que d'ajouter une exception.** Une règle qui a
> besoin d'exceptions est une règle mal formulée. Le comptage sert à ça : il
> montre *où* la formulation ne tient pas.

## 5. Le rapport

```bash
uv run brainkit mesurer --vault <vault> --rapport AI/mesure/<date>-mesure.md
```

Dépose-le dans l'espace agent du vault, daté. C'est ce qui permet à la mesure
suivante de dire « 62 → 41 » plutôt que « 41 ». Un compte sans son précédent ne
dit rien d'une tendance.

Puis clôture normalement :
[`cloturer-une-ecriture.md`](cloturer-une-ecriture.md).

## 6. Ce que tu ne fais jamais

- **durcir sans compter.** Même une règle qui « paraît évidente » ;
- **recopier une sévérité d'un autre brain.** Porter une sévérité, c'est porter
  une mesure qu'on n'a pas faite ;
- **assouplir sans écrire le motif** ;
- **contourner le plancher** en abaissant un seuil dans le code. Le plancher
  protège contre une conclusion tirée de rien ; l'abaisser ne fait pas
  apparaître les pages qui manquent.
