# Livrer une instance autonome — `freeze`

Le cas visé : un vault remis sur une machine où l'on **n'installera rien depuis
internet**. Un poste isolé, un réseau fermé, une machine dont on ne gère pas
l'outillage.

---

## 1. Le problème, et pourquoi il n'a pas de solution douce

Une instance normale ne contient **pas de code**. C'est ce qui garantit qu'une
correction du validateur atteint toutes les instances le jour où elle est faite
([02-architecture.md](02-architecture.md) §1).

> **Problème** : un vault remis sur une machine sans accès à un dépôt de paquets
> ne peut pas atteindre le kit — donc il ne sait pas se valider, ni se
> régénérer. Une instance qui ne sait pas se valider n'est pas remettable.
> **Options** : (a) réécrire un validateur autonome, léger, dans l'instance ;
> (b) **copier** le kit tel quel dans l'instance ; (c) renoncer et ne remettre
> que du markdown. **Retenu** : (b), **plutôt que** (a) **parce que** deux
> chemins de code se comportent différemment — et la différence se découvre chez
> le destinataire ; **plutôt que** (c) **parce qu'**un brain sans ses contrôles
> n'est plus un brain, c'est un dossier de fichiers. **Limite** : l'instance
> figée ne reçoit plus rien. C'est le prix, écrit au §3.

Le choix (b) a une conséquence vérifiable, et elle a été vérifiée : le jeu
d'épreuve fait tourner **la même instance** avec le kit branché puis avec le kit
figé, et compare. **Même verdict, ligne pour ligne.** `freeze` copie, il ne
réécrit pas.

---

## 2. La commande

```bash
brainkit freeze --vault <racine du vault>              # simulation : n ecrit rien
brainkit freeze --vault <racine du vault> --ecrire
```

Ce qu'elle pose dans l'instance :

| Quoi | Où | Rôle |
|---|---|---|
| le paquet du kit | `AI/scripts/brainkit/` | les deux validateurs, les quatre générateurs, le semis |
| trois lanceurs autonomes | `AI/scripts/valider.py`, `generer.py`, `semer.py` | à en-tête PEP 723 : ils se lancent par `uv run` **sans rien installer**, et résolvent le manifeste et la racine tout seuls |
| une note de figeage | `AI/scripts/FIGE.md` | ce qui a été copié, ce qui est perdu, et comment rebrancher |

Elle passe en plus `kit.mode` à `fige` dans `brain.yml`, **par édition d'une
seule ligne**. C'est délibéré : relire et réécrire le YAML en entier perdrait
tous les champs `motif:`, qui sont la moitié de la valeur d'un manifeste.

Cette modification d'une ligne est la **seule** touche de `freeze` au contenu,
et elle est volontairement visible dans un `git diff`.

Ce qui n'est jamais copié : le bytecode et les arbres de travail.

### Les commandes, dans une instance figée

```bash
uv run AI/scripts/valider.py
uv run AI/scripts/generer.py              # --check
uv run AI/scripts/generer.py --ecrire
```

Elles remplacent `brainkit valider` et `brainkit generer`. Tout le reste de
[06-manuel.md](06-manuel.md) reste vrai, aux commandes près.

---

## 3. Ce que `freeze` perd — et c'est le prix, pas un défaut

| Ce qui reste dehors | Conséquence |
|---|---|
| **les correctifs à venir** | l'instance ne recevra plus rien. C'est la ligne qui compte |
| le contrat du manifeste (`schema/`) | un `brain.yml` modifié ne se vérifie plus contre son contrat |
| les jeux d'épreuve (`tests/`) | aucun moyen de prouver, **sur place**, que ce kit figé se comporte comme le kit |
| l'outil de fidélité | idem |
| la comparabilité | deux instances figées à deux dates ne portent pas le même code |
| cette documentation | elle vit dans le dépôt du kit. L'instance porte la **sienne**, générée depuis son manifeste |

La dernière ligne mérite d'être dite clairement : une instance figée est
**documentée** — son `INSTALL.md` et ses trois guides sont dans le vault, écrits
depuis son propre manifeste. Ce qu'elle ne porte pas, c'est la documentation du
**kit**, celle que vous lisez. Ce n'est pas un manque : le destinataire n'a pas
à installer le kit, il a un vault qui marche.

---

## 4. Il n'y a pas de dégel automatique

Et c'est délibéré : un dégel silencieux ferait cohabiter deux versions du même
code sans que personne ne le sache.

Rebrancher se fait à la main, et `AI/scripts/FIGE.md` — posé dans l'instance —
en donne la marche : supprimer `AI/scripts/brainkit/` et les trois lanceurs,
puis remettre `kit.mode` à `branche`.

---

## 5. Une limite ouverte, et il faut la connaître avant de livrer

Le kit **ne confronte pas `kit.mode` au disque**. Une instance qui se déclare
`branche` alors qu'un kit est copié dedans passerait inaperçue, et l'inverse
aussi.

Concrètement, avant une remise : vérifier les deux à la main.

```bash
grep -A2 '^kit:' brain.yml           # ce que l instance DECLARE
ls AI/scripts/brainkit >/dev/null 2>&1 && echo "un kit est copie dedans"
```

C'est une remontée ouverte, chiffrée à une dizaine de lignes, et elle est
listée dans `../design/etat-final.md` §4.3.

---

## 6. La liste avant remise

| Contrôle | Commande | Attendu |
|---|---|---|
| le vault est vert | `uv run AI/scripts/valider.py` | aucune violation dure |
| les artefacts dérivés concordent | `uv run AI/scripts/generer.py` | code 0, aucun écart |
| l'arbre est propre | `git status --porcelain` | vide |
| le mode déclaré est le mode réel | §5 ci-dessus | les deux concordent |
| aucun secret dans le dépôt | [SECURITY.md](SECURITY.md) §3 | rien |
| l'identité des commits | `git log --format='%ae' \| sort -u` | seulement l'adresse attendue |

Le dernier point n'est pas une formalité. Une adresse entrée dans l'historique
d'un dépôt n'en sort pas sans réécriture d'historique — voir
[SECURITY.md](SECURITY.md) §2.

---

## 7. Ce qui n'est pas tranché, et n'appartient pas à ce document

La propriété de l'ontologie d'un brain construit pour un tiers — son axe de
rangement, ses natures de page, ses règles de départage — n'est **pas** tranchée
dans ce dépôt. C'est un livrable, et c'est en même temps la description d'une
organisation.

Le point est ouvert dans `../design/00-cadrage.md`, et il appartient au
propriétaire du dépôt. Aucun document ici ne le tranche à sa place, et aucun ne
porte de valeur monétaire ni de nom de tiers.
