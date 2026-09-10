# Recette — livrer une instance figée

> **Pour qui** : un agent de code, dans le dépôt du kit, avec l'instance à
> côté. Terminal. Aucune clé d'API, et c'est le point : une instance figée doit
> tourner sur une machine **sans accès à internet**.
>
> **Quand** : le vault part chez quelqu'un qui n'aura pas le kit à côté — une
> livraison hors ligne, un poste isolé, un client qui ne peut rien installer.
>
> **Ce que ça produit** : le paquet copié **dans** l'instance
> (`AI/scripts/brainkit/`), trois lanceurs autonomes, et `kit.mode` passé à
> `fige` dans le manifeste.
>
> **Critère de fin** : l'instance figée rend le **même verdict que le kit,
> ligne pour ligne**, sur son propre vault — et tu l'as vérifié en lançant les
> deux.

---

## 0. Comprendre ce que ça coûte, avant de le faire

Le kit est un **générateur**, pas un dépôt-gabarit qu'on clone. Le jour du
clone, le code fourche : avec trois instances, chaque correction se réapplique
trois fois à la main, et la troisième divergera. C'est pourquoi une instance
normale ne contient **aucun code**.

Figer est donc un **arbitrage**, pas une commodité. Ce qu'on perd :

| Ce qui reste dehors | Conséquence |
|---|---|
| les correctifs à venir | une instance figée ne recevra plus rien |
| le validateur de manifeste (`schema/`) | un `brain.yml` modifié ne se vérifie plus contre le contrat |
| les outils de dépôt et les jeux d'épreuve | aucun moyen de prouver, **sur place**, que ce kit figé se comporte comme le kit |
| la version | `kit.version` fige la date, et le kit refuse de tourner sur une version qu'il ne connaît pas — dans les deux sens |

**Dis ces quatre lignes à l'utilisateur avant de figer**, et attends sa réponse.
Défiger n'est pas une opération : c'est un nouveau semis.

## 1. Clôture d'abord

Une instance se fige **propre**. Passe
[`cloturer-une-ecriture.md`](cloturer-une-ecriture.md) en entier : artefacts
régénérés, validateurs verts, `git status` vide. Figer par-dessus une écriture
non clôturée fige aussi l'écart.

## 2. Simule

```bash
uv run brainkit freeze --vault <instance>
```

Sans `--ecrire`, rien n'est posé. Le kit annonce ses **quatre étapes** et refuse
deux cas :

- la cible n'est pas une instance (pas de `brain.yml`) ;
- l'instance est **déjà figée** — refiger n'est pas idempotent, c'est écraser.

Lis les quatre étapes. C'est le moment de voir qu'on fige la mauvaise instance.

## 3. Applique

```bash
uv run brainkit freeze --vault <instance> --ecrire
```

Ce qui est posé :

- `AI/scripts/brainkit/` — le paquet, **copié** et non réécrit. C'est la
  mitigation du risque « deux chemins de code qui se comportent
  différemment » : ils sont le même code, aux octets près ;
- trois lanceurs à en-tête PEP 723 (`valider.py`, `generer.py`, `semer.py`) qui
  se lancent par `uv run` **sans rien installer** ;
- `kit.mode: fige` dans le manifeste — la seule modification de contenu que
  `freeze` apporte, et elle est volontairement visible dans un `git diff`.

Le bytecode n'est jamais copié : ni `__pycache__`, ni `.pyc`.

## 4. Prouve que le verdict est le même

C'est le critère, et il ne se déduit pas — il se lance :

```bash
# le kit, depuis son dépôt
uv run brainkit valider --vault <instance>          > /tmp/verdict-kit.txt

# l'instance figée, avec son propre code
cd <instance> && uv run AI/scripts/valider.py       > /tmp/verdict-fige.txt

diff /tmp/verdict-kit.txt /tmp/verdict-fige.txt
```

`diff` doit être **vide**. S'il ne l'est pas, ne livre pas : deux chemins de
code qui divergent sur le même vault, c'est exactement ce que figer est censé
éviter.

Fais la même chose pour `generer --check`.

## 5. Clôture, et documente la bascule

Le `freeze` a modifié le manifeste et ajouté des fichiers : c'est une écriture,
donc elle se clôt ([`cloturer-une-ecriture.md`](cloturer-une-ecriture.md)).

Écris dans l'espace agent de l'instance, en clair :

- **la version du kit figée**, et la date ;
- **les quatre pertes** de §0, telles quelles ;
- **comment relancer** : `uv run AI/scripts/valider.py`,
  `uv run AI/scripts/generer.py --ecrire` ;
- **ce qu'il faut faire pour revenir sur une version à jour** : re-semer depuis
  le kit courant, et rejouer le contenu. Ne promets pas une mise à jour en
  place : il n'y en a pas.

## 6. Ce que tu ne fais jamais

- **figer une instance qui n'est pas verte.** L'écart part avec le paquet, et
  il ne se répare plus depuis dehors ;
- **refiger une instance déjà figée.** Le kit refuse ; ne contourne pas ;
- **modifier `AI/scripts/brainkit/` à la main.** C'est une copie ; la modifier
  ouvre exactement la fourche que tout le dispositif évite ;
- **promettre des correctifs.** Une instance figée est une instance qui ne
  recevra plus rien, et il vaut mieux le dire une fois de trop.
