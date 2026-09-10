# AGENTS.md — ce dépôt, pour un agent de code

Tu es dans **BrainKit**. Ce fichier est le premier que tu lis, et il suffit à
savoir quoi faire. Il est écrit pour n'importe quel agent de code — Claude Code,
Cursor, Antigravity, Windsurf, ou un autre — parce que tous lisent ce fichier et
qu'aucun n'a besoin d'un format propriétaire pour suivre une recette en
Markdown.

**La voie normale d'usage de ce kit est un agent de code, pas une clé d'API.**
Aucune clé, aucun jeton, aucun compte n'est requis pour quoi que ce soit ici.
Ce que le kit fait tout seul, il le fait dans un terminal ; ce qui demande un
jugement, c'est toi qui le portes, en conversation avec l'humain.

---

## 1. Ce qu'est ce dépôt

Un **paquet Python** qui crée, valide et entretient un *second brain* : un vault
de fichiers Markdown, ouvrable dans Obsidian, versionné dans git.

Tout ce qui est propre à un sujet vit dans **un seul fichier**, le manifeste
`brain.yml` de l'instance. **Rien dans ce dépôt ne nomme un sujet** — c'est une
propriété, pas une coïncidence : les rôles du manifeste de référence s'appellent
« unité » et « notion », ses valeurs d'axe « Domaine A » et « nature-3 ». Si tu
lis un nom propre thématique quelque part hors de `design/`, c'est une
régression.

Une instance ne contient **pas de code** : le kit vit ailleurs et lit son
manifeste — sauf si on la **fige**, pour une livraison hors ligne.

```
AGENTS.md          ← tu es ici
recettes/          ← LES RECETTES : une par tâche, Markdown pur, exécutables
gabarit/brain.yml  ← le manifeste de RÉFÉRENCE : tous les mécanismes, aucun sujet
gabarit/rendu/     ← les 4 documents qu'une instance reçoit, rendus pour lecture
brainkit/          ← le paquet : valider, generer, semer, entretien, mesurer, amont…
outils/            ← 3 outils de dépôt (fidélité, emballage, captures)
schema/            ← le contrat du manifeste (JSON Schema + cohérences)
tests/             ← 8 jeux d'épreuve, et leurs fixtures — abstraites, sans sujet
docs/              ← la documentation du kit, écrite à la main
design/            ← LES ARCHIVES DU CHANTIER : 14 rapports de lot. Voir §6
skills/            ← enveloppes minces pour Claude Code, qui pointent vers recettes/
```

---

## 2. Par quoi commencer

1. **`recettes/README.md`** — l'index des recettes. Va y chercher la tâche
   demandée, et suis-la. C'est la source unique : si une recette et un autre
   document se contredisent, la recette gagne.
2. Si la tâche n'a pas de recette : **`docs/README.md`**, puis
   `docs/02-architecture.md`.
3. Ne lis `design/` que si on te demande *pourquoi* une décision a été prise.

Vérifie d'abord que le kit répond :

```bash
uv run brainkit
```

Si `uv` manque, `docs/03-installation.md` §1 le dit. Il n'y a rien d'autre à
installer : une seule dépendance d'exécution, PyYAML, qu'`uv` pose tout seul.

---

## 3. Les huit commandes

Toutes se lancent par `uv run brainkit <commande>`, et toutes **prennent le
manifeste du vault** (`<vault>/brain.yml`) quand on ne leur en donne pas.

| Commande | Ce qu'elle fait |
|---|---|
| `entretien` | mène les 49 questions, en refuse 13, écrit le manifeste |
| `semer` | crée le vault : dossiers, hubs, gabarits, skills, hooks git, dépôt |
| `valider` | les 10 règles de contenu, plus les contrôles de socle déclarés |
| `generer` | les 4 artefacts dérivés. `--check` par défaut, code 2 sur écart |
| `mesurer` | ce qu'une règle **coûterait** avant de la durcir |
| `sonder` | l'amont d'une unité — sans jeton, et n'écrit qu'un side-car |
| `re-seuiller` | change le seuil de promotion : une migration, par `git mv` |
| `freeze` | copie le kit **dans** l'instance et coupe la dépendance |

---

## 4. Ce que tu peux faire sans demander

- lire n'importe quoi, ici comme dans un vault ;
- lancer `valider`, `generer --check`, `mesurer`, `sonder --rapport`, et les
  jeux d'épreuve de `tests/` — aucun n'écrit dans un vault ;
- écrire dans `AI/` d'une instance, hors `AI/index/` ;
- proposer une modification, en la montrant.

## 5. Ce que tu ne fais JAMAIS sans un ordre explicite

- **écrire dans une page d'un rôle `protege: true`.** La frontière est portée
  par le champ `role:` du frontmatter, jamais par le chemin : **lis le
  frontmatter avant d'écrire dans une page**. Création libre, modification sur
  demande explicite ;
- **éditer à la main un chemin listé dans `genere:`** du manifeste — zones AUTO
  des hubs, index, carte des liens, hauts de page, gabarits, taxonomie. Ce qui
  est généré se régénère ; deux sources qui décrivent la même chose divergent ;
- **supprimer une page.** Un **déplacement** se fait par `git mv`, jamais par
  suppression puis création : sans quoi l'historique de la page est perdu ;
- **deviner une valeur du manifeste.** Ni un axe, ni une sévérité, ni un seuil,
  ni une identité git. Un champ vide est une question ouverte ; une valeur
  inventée est une faute. Les treize refus sont une liste fermée :
  `uv run brainkit entretien --refus` ;
- **committer une identité git que l'utilisateur n'a pas donnée.** Tu ne prends
  JAMAIS l'adresse que ton harnais t'annonce : elle t'identifie auprès d'un
  outil, elle n'attribue pas un commit. Jamais de `-c user.email`, de
  `--author`, de `GIT_AUTHOR_EMAIL`, ni de `--no-verify`. Trois hooks git le
  font respecter ; un hook qui refuse n'est pas un incident à contourner ;
- **ajouter un trailer `Co-Authored-By`** ni mentionner un outil dans un message
  de commit ;
- **écrire une page de contenu dans un brain neuf.** Ni exemple, ni
  démonstration, ni lorem. Un brain neuf est vide, et c'est le critère ;
- **ajouter un sujet dans ce dépôt.** Pas de fixture thématique, pas de manifeste
  d'un domaine réel, pas de page d'exemple. Un exemple vit **inline dans la
  documentation**, jamais comme fichier livré.

Et deux interdits de fond, qui ne dépendent d'aucun ordre : **aucune clé, aucun
jeton, aucun secret dans un fichier** ; **aucune promesse commerciale** — ni
prix, ni offre, ni argumentaire, ni nom de client. Un contrôle du jeu d'épreuve
le vérifie (`tests/emballage.py`).

---

## 6. `design/` — les archives, pas la doc

Les quatorze fichiers de `design/` sont le **journal du chantier** : un rapport
par lot, avec ses mesures et ses remontées. Ils citent le vault réel sur lequel
tout a été prouvé, et ils le nomment. **C'est le seul endroit du dépôt où un
nom propre apparaît, et c'est délibéré** : effacer les mesures effacerait les
preuves qui justifient chaque seuil et chaque sévérité.

Conséquence pratique : ne cite pas `design/` comme documentation du produit, et
ne recopie pas ses exemples dans une page destinée à un utilisateur. Commence
par `design/etat-final.md` si on te demande l'état du chantier.

---

## 7. Comment tu clôtures une écriture

Toute écriture dans un vault se clôt par la recette
[`recettes/cloturer-une-ecriture.md`](recettes/cloturer-une-ecriture.md) :
régénérer, valider, vérifier la divergence avec le distant, puis committer.
C'est le **seul** endroit où la politique git d'une instance est écrite.

Pour une modification de ce dépôt-ci, avant de committer :

```bash
uv run schema/valider.py
uv run tests/epreuve.py
uv run tests/generation.py
uv run tests/semis.py
uv run tests/skills.py
uv run tests/mesure.py
uv run tests/amont.py
uv run tests/entretien.py
uv run tests/emballage.py
uv run outils/emballer.py
uv run outils/captures.py
bash  outils/neutralite.sh      # 0 occurrence : le dépôt ne nomme aucun sujet
```

Deux jeux d'épreuve savent en plus tourner sur un **vault témoin** réel, s'il y
en a un sur la machine : ils le prennent par `--vault-temoin <chemin>`, par la
variable `BRAINKIT_VAULT_TEMOIN`, ou par une ligne `vault_temoin=<chemin>` dans
un fichier `.brainkit-local` non suivi. Sans témoin, ces scénarios sont
**sautés** et le disent — un scénario sauté n'est pas un scénario vert. Le
détail est dans `tests/temoin.py`.

---

## 8. Voix

Français par défaut. Phrases courtes. Pas de marketing. Tu peux contredire :
« ça ne marche pas parce que X » vaut mieux que « intéressante idée ». Pas
d'émojis sauf si l'utilisateur en met.

Et la règle qui résume le reste, née d'une règle dure sur les hauts de page :
**une fiche vide honnêtement vaut mieux qu'une fiche remplie au jugé.**
