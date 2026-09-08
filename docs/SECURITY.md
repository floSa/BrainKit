# Sécurité

Trois sujets, et un seul principe : **rien de secret n'entre dans un dépôt.**

---

## 1. La clé d'API du pont

Le plugin de pont expose le coffre en HTTPS et exige une clé passée en jeton
porteur. Cette clé donne un **accès complet en lecture et en écriture** à tout
le vault.

| Fait | Conséquence |
|---|---|
| le serveur n'écoute que sur `127.0.0.1` | inaccessible depuis le réseau local et depuis internet |
| la clé est exigée pour toute opération | le serveur seul ne suffit pas à lire le vault |
| le certificat est **auto-signé** | un client doit l'accepter explicitement, ou l'ajouter aux autorités de confiance |

### Ce qu'on ne fait pas

- **ne pas committer la clé.** Ni dans le vault, ni dans un fichier de
  configuration versionné du projet qui l'utilise.
- **ne pas la laisser visible dans une capture d'écran.** C'est arrivé dans le
  vault d'origine : deux captures ont dû être reprises avec la clé masquée.
  Le protocole de prise (`../design/12-captures.md`) en fait une consigne.
- **ne pas activer le serveur non chiffré** en dehors d'une machine locale, et
  jamais sur un poste exposé.

### Si elle a fui

La régénérer depuis le panneau du plugin — *Reset all crypto* régénère le
certificat, les clés et la clé d'API — puis la remplacer partout où elle avait
été collée. Une clé régénérée invalide l'ancienne, ce qui est exactement l'effet
voulu.

[08-depannage.md](08-depannage.md) donne les gestes.

---

## 2. L'identité git

C'est le sujet le plus contre-intuitif du dépôt, et il a coûté cinq commits dans
le vault d'origine avant d'être traité mécaniquement.

### Le problème

Un agent de code annonce, à chaque conversation, une adresse électronique qui
identifie l'utilisateur **auprès de l'outil**. Cette adresse peut être une
adresse professionnelle. Elle n'attribue **jamais** un commit d'un dépôt
personnel.

Une adresse entrée dans l'historique d'un dépôt entre dans la liste des
contributeurs de la forge, **d'où elle ne sort pas** sans réécriture
d'historique. C'est le genre de faute qui ne se répare pas discrètement.

### La règle

L'identité d'un commit est celle de la **config locale du dépôt**, et rien
d'autre :

```bash
git config --local user.name
git config --local user.email
```

- **committer nu.** Ne jamais passer d'identité en ligne de commande, ne jamais
  poser de variable d'environnement d'auteur. Git lit la config locale tout
  seul : c'est exactement le comportement voulu.
- **ne jamais lire l'adresse annoncée par l'outil** pour remplir un champ
  d'auteur.
- si la config locale manque ou paraît fausse : **s'arrêter et demander.** Ne
  pas la deviner, ne pas la « réparer » avec l'adresse qu'on a sous la main.

C'est le premier des treize refus de deviner de l'entretien, et le seul à avoir
**trois** garde-fous.

### Les trois garde-fous

Ils sont versionnés dans `.githooks/` et activés par une commande, une fois par
clone ([03-installation.md](03-installation.md) §3).

| Hook | Ce qu'il refuse | Pourquoi il existe séparément |
|---|---|---|
| `pre-commit` | un commit dont l'auteur ou le committer porte l'adresse professionnelle | il lit l'identité **effective**, donc couvre aussi les contournements en ligne de commande et par variable d'environnement |
| `commit-msg` | un message portant un trailer de co-auteur | git exécute `pre-commit` **avant** de composer le message : un test placé là ne verrait rien. C'est ce trou qui a laissé passer cinq commits |
| `pre-push` | de **pousser** un commit fautif, quelle que soit son origine | un contournement, un `rebase` qui rejoue une identité, un commit importé d'un autre clone ou d'un worktree sans hooks |

**Une consigne écrite ne suffit pas** — c'est le constat qui a fait naître ces
hooks. Elle existait déjà, et elle n'a pas tenu.

### Un hook qui refuse n'est pas un incident

C'est la règle qui fonctionne. **Le contournement de vérification ne s'utilise
pas ici.** Le message nomme ce qui a été refusé et ce qui est attendu : corriger,
puis recommencer.

Pour plusieurs commits déjà faits, une réécriture d'historique **ne se décide pas
seule** : en parler au propriétaire du dépôt.

---

## 3. Ce qu'un dépôt de brain ne doit pas contenir

Le contrôle est mécanique quand il peut l'être, et écrit quand il ne peut pas.

| Interdit | Contrôlé par |
|---|---|
| une clé, un jeton, un mot de passe | relecture. `sonder` est conçu **sans jeton** pour que la question ne se pose pas |
| une clé visible dans une capture d'écran | le protocole de prise, `../design/12-captures.md` |
| une adresse professionnelle en auteur de commit | les trois hooks, §2 |
| un trailer de co-auteur | le hook `commit-msg` |
| une valeur monétaire, une proposition commerciale, un argumentaire de vente, un nom de tiers | un contrôle du jeu d'épreuve, fichier par fichier — `tests/emballage.py` scénario 1 |

### Pourquoi `sonder` n'a pas de jeton

Sonder l'amont d'une unité pourrait aller plus vite avec un jeton d'accès à une
forge. Le kit **n'en prend pas**, et n'en prendra pas : un jeton dans un vault
serait un secret dans un dépôt. Il lit ce qui est public, et il accepte d'être
plus lent — `--pause` et `--limit` sont là pour ça.

C'est une contrainte de conception, pas une limite temporaire.

### Le side-car

`sonder` n'écrit **jamais** dans une page : les faits sondés vont dans un
fichier à part. Conséquence pour la sécurité : ce fichier contient ce qu'une
sonde publique a lu, rien de plus, et il se supprime sans perte — la commande le
reconstruit.

---

## 4. Signaler un problème de sécurité

Ce dépôt est personnel et n'a pas de procédure publique. Un problème se signale
directement à son propriétaire, avec la sortie complète de la commande qui l'a
révélé, et **sans** y coller la valeur du secret concerné.
