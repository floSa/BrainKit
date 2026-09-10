# Lot 12 — la documentation du kit, et le protocole de captures

> Écrit le 2026-09-08, après la clôture du plan de dix lots et le lot 11 de la
> fraîcheur. Ce lot ne pose **aucun mécanisme nouveau**, sauf un : le contrôle
> du manifeste d'images, qui ferme la remontée 8 du lot 10 et la remontée 3 de
> `etat-final.md` §4.3.

---

## 1. Ce que ce lot corrige

Le dépôt annonçait un guide d'installation, un manifeste de 27 captures, et
**aucune image**. Le manque n'était pas seulement l'absence d'images : c'était
une confusion de **natures**.

| Document | Nature réelle | Comment il était produit | Défaut |
|---|---|---|---|
| `INSTALL.md` à la racine | doc **du kit** | **généré**, par `install.document(None)` | il ne lisait aucune valeur de manifeste : c'était de la prose écrite en Python, et le générateur interdit (à raison) toute balise d'image. **Ce document ne pouvait donc pas être illustré** |
| `docs/README.md` | doc **du kit** | **généré**, par `outils/emballer.py` | même défaut, à plus petite échelle |
| `docs/histobrain/*` | doc **d'une instance** | généré depuis `exemples/histobrain.brain.yml` | juste, mais rangé sous `docs/`, ce qui laissait croire que `docs/` était généré |

La frontière est simple, et elle décide de tout :

> **La doc d'une instance dépend d'un manifeste, donc elle se génère. La doc du
> kit n'en dépend d'aucun, donc elle s'écrit.**

Le kit n'a jamais eu besoin de générer sa propre documentation : la générer
était un **accident de fabrication** — le générateur d'instance existait, il
suffisait de l'appeler avec un manifeste vide. Le prix de cet accident était
l'impossibilité d'y mettre une image.

### Ce qui a bougé

| Avant | Après |
|---|---|
| `INSTALL.md` (racine, généré, 470 lignes) | supprimé. Son contenu est réparti dans `docs/03-installation.md`, `docs/04-obsidian.md`, `docs/05-premier-brain.md`, `docs/07-livrer-une-instance.md`, `docs/08-depannage.md` |
| `docs/README.md` (généré) | écrit à la main : l'index de la doc du kit |
| `docs/histobrain/` (généré) | `exemples/rendu-histobrain/`, par `git mv` — au bon endroit, à côté du manifeste dont il est rendu |
| `brainkit.emballer.rendus_du_kit()` | retiré. Le paquet ne s'adresse plus qu'à une instance |
| `outils/emballer.py` rendait 5 fichiers | il en rend 4, tous d'instance |
| aucun contrôle d'images | `outils/captures.py`, dans les deux sens |

---

## 2. Le tri des 28 captures du vault d'origine

Le vault d'origine porte **28** fichiers sous `docs/install/img/`. Chacun a été
**ouvert et regardé** avant d'être classé — pas classé sur son nom.

### Paquet (a) — réutilisables telles quelles : **15 fichiers**

Elles montrent l'interface d'Obsidian et rien du contenu. Elles sont copiées
dans `docs/img/` sous le nom du manifeste d'images, **sans aucune
modification**.

| Fichier d'origine | Copié en | Ce qu'il montre |
|---|---|---|
| `02-welcome-vault-picker.png` | `01-obsidian-selecteur-de-coffre.png` | l'écran d'accueil d'Obsidian, bouton « Ouvrir un dossier comme coffre » |
| `01-settings-general.png` | `02-obsidian-reglages-general.png` | Paramètres → Général, et la barre latérale des sections |
| `04-restricted-mode.png` | `03-obsidian-mode-restreint.png` | Modules complémentaires, mode restreint actif |
| `05-community-plugins-enabled.png` | `04-obsidian-modules-actives.png` | le même panneau après avoir quitté le mode restreint, zéro module |
| `06-plugins-browser.png` | `05-obsidian-catalogue.png` | le navigateur de plugins, recherche vide |
| `07-search-local-rest-api.png` | `06-plugin-rest-api-recherche.png` | la recherche du plugin de pont et ses **sept** résultats, homonymes compris |
| `08-local-rest-api-detail.png` | `06b-plugin-rest-api-carte.png` | la carte du plugin **avant** installation, bouton *Installer* |
| `09-local-rest-api-activated.png` | `07-plugin-rest-api-active.png` | la même carte après *Installer* puis *Activer* |
| `10-local-rest-api-options.png` | `08-plugin-rest-api-options.png` | les options du pont : URL locale, clé d'API **masquée** |
| `13-mcp-endpoint-json-config.png` | `09-plugin-rest-api-mcp.png` | la section MCP : points d'entrée, en-tête d'autorisation **masqué** |
| `12-all-plugins-enabled.png` | `10-plugins-tous-actives.png` | les quatre plugins installés et activés |
| `22-templater-settings.png` | `11-templater-reglages.png` | Templater, champ du dossier de gabarits vide |
| `23-templater-folder-set.png` | `12-templater-dossier-pose.png` | le même champ renseigné |
| `15-file-hider-options.png` | `13-file-hider-options.png` | les options de File Hider, liste vide |
| `14-local-rest-api-advanced.png` | `29-plugin-rest-api-avance.png` | les réglages avancés du pont : certificats, réinitialisation |

**Deux réserves écrites, et la première a été RENVERSÉE — révision du
2026-09-10 :**

1. ~~la **barre de titre** de ces panneaux affiche le nom du vault sur lequel
   elles ont été prises. C'est le seul endroit où elles ne sont pas génériques ;
   le contenu des panneaux, lui, est celui d'Obsidian.~~ **Ce n'est plus une
   réserve acceptable : c'est un défaut.** Le dépôt ne doit nommer aucun sujet,
   et une barre de titre est un nom de sujet dans un fichier livré — que la
   recherche textuelle ne trouve pas, ce qui la rend pire, pas meilleure. Le
   nouveau tri est ci-dessous.
2. sur `09-plugin-rest-api-mcp.png`, le bloc de configuration lui-même est
   **sous la ligne de pliure** : on voit son titre, pas son contenu. Le document
   le dit, et ajoute que ce bloc se copie depuis l'écran et jamais depuis une
   image, puisqu'il contient la clé. Une reprise serait un confort, pas une
   correction — mais cette capture est de toute façon à reprendre, pour le
   motif 1.

#### Le nouveau tri du paquet (a) : **1 acceptable, 14 à reprendre**

Chacune a été **rouverte et regardée** le 2026-09-10, pas jugée sur son nom.

| Verdict | Fichiers | Motif |
|---|---|---|
| **acceptable telle quelle** — 1 | `01-obsidian-selecteur-de-coffre.png` | aucun coffre n'est ouvert au moment de la prise : la fenêtre ne porte **aucun** nom de vault. C'est la seule des quinze dans ce cas |
| **à reprendre** — 14 | `02-obsidian-reglages-general.png` · `03-obsidian-mode-restreint.png` · `04-obsidian-modules-actives.png` · `05-obsidian-catalogue.png` · `06-plugin-rest-api-recherche.png` · `06b-plugin-rest-api-carte.png` · `07-plugin-rest-api-active.png` · `08-plugin-rest-api-options.png` · `09-plugin-rest-api-mcp.png` · `10-plugins-tous-actives.png` · `11-templater-reglages.png` · `12-templater-dossier-pose.png` · `13-file-hider-options.png` · `29-plugin-rest-api-avance.png` | la barre de titre porte le nom du vault d'origine (`Paramètres - <nom> - Obsidian 1.13.7`, et sa variante pour la fenêtre des modules) |

**La reprise est mécanique, et c'est important de le dire** : ces quatorze
captures sont **justes sur le fond** — elles montrent des panneaux d'Obsidian
qui ne dépendent d'aucun sujet. Il n'y a rien à recadrer, rien à repenser : même
écran, même geste, sur le brain de démonstration **neutre** de §4.1. C'est la
raison pour laquelle elles restent en place en attendant la séance plutôt que
d'être supprimées : un guide qui montre le bon panneau avec la mauvaise barre de
titre vaut mieux qu'un guide sans image. `docs/04-obsidian.md` le dit en tête de
chapitre, en toutes lettres.

**La séance passe donc de 16 à 30 prises.** Les quatorze reprises n'ont pas de
table à elles : elles se prennent en suivant `docs/04-obsidian.md` du début à la
fin, ce que §4.1 demande déjà.

### Paquet (b) — à refaire sur un vault BrainKit : **9 fichiers**

Elles montrent des dossiers ou des pages de développement logiciel. Elles sont
fausses dès la deuxième instance.

| Fichier d'origine | Ce qu'il montre de trop | Remplacé par |
|---|---|---|
| `02b-folder-picker-devbrain.png` | le chemin du vault d'origine | `18-selecteur-dossier-du-vault.png` |
| `03-vault-opened.png` | l'arbre du vault d'origine, dossiers de dev | `19-arbre-du-vault.png` |
| `24-vault-overview.png` | l'arbre **et** la porte d'entrée, avec 20 domaines de dev | `19-` et `20-porte-d-entree.png` |
| `18-vault-structure-expanded.png` | l'arbre déplié, sous-domaines de dev | `19-arbre-du-vault.png` |
| `19-postgres-fiche-properties.png` | une fiche de brique de dev, nommée | `21-page-d-unite-proprietes.png` |
| `20-comparatif-bases-relationnelles.png` | une vue de dev | `23-page-de-vue.png` |
| `16-file-hider-context-menu.png` | **ce n'est pas le bon écran** — voir l'encadré | `14-file-hider-menu-contextuel.png` |
| `17-file-hider-after-hidden.png` | la barre latérale et la porte d'entrée du vault d'origine | `15-file-hider-apres.png` |
| `25-graph-groupes-config.png` | le panneau Groupes, mais avec les **requêtes de rôles** du vault d'origine | `16-graphe-groupes-reglages.png` |

> **Un défaut trouvé en regardant, et il vaut d'être noté.** La capture
> `16-file-hider-context-menu.png` du vault d'origine est censée montrer le menu
> contextuel de File Hider. Elle montre en réalité le **panneau du graphe**, avec
> un menu contextuel ouvert par-dessus. Le guide d'origine l'appelle donc à un
> endroit où elle n'illustre pas ce qu'il dit. C'est le motif de la consigne
> « contrôler l'image après la prise, pas seulement le geste », écrite dans
> `docs/04-obsidian.md` §5 et au §4 ci-dessous.
>
> Ce défaut est dans le vault d'origine, qui est **hors du périmètre de ce lot** :
> il est reporté en remontée (§6).

### Paquet (c) — sans objet pour le kit : **4 fichiers**

| Fichier d'origine | Pourquoi sans objet |
|---|---|
| `11-all-plugins-installed.png` | **doublon binaire** de `12-all-plugins-enabled.png` — même `sha256` (`72b405cd…`). Le guide d'origine les appelle à deux étapes différentes en montrant deux fois la même image |
| `26-graph-colore.png` | **doublon binaire** de `25-graph-groupes-config.png` — même `sha256` (`136ed780…`). Même défaut |
| `21-comparatif-llm-frameworks.png` | une **seconde** vue de dev. Le kit n'en déclare qu'une, et une deuxième n'ajoute rien |
| `27-snippet-roles-active.png` | l'extrait CSS. **Aucun mécanisme du kit ne produit d'extrait CSS** — le vault d'origine en a un, écrit à la main. Le retrait était déjà acté au lot 10 (trou 6) |

**15 + 9 + 4 = 28.** Le compte est bon.

---

## 3. Le nommage et la numérotation

`docs/img/NN-slug.png`, numéroté dans l'**ordre de lecture** de la
documentation. Les numéros ne sont pas jointifs, et n'ont pas à l'être : ils
disent l'ordre, pas un compte.

Trois bandes, et la distinction sert à savoir qui refait quoi :

| Bande | Portée | Qui la refait |
|---|---|---|
| `01` à `16` | les captures de portée **kit** du manifeste d'images (`brainkit/emballer/images.py`) | une fois, jamais plus : l'interface d'Obsidian ne dépend d'aucun sujet |
| `18` à `28` | les captures de portée **instance** du manifeste | à chaque brain. Dans la doc du kit, elles illustrent un vault de **démonstration** |
| `29` et au-delà, plus `NNb` | les captures dont **seule la doc du kit** a besoin | avec la doc du kit |

Deux trous délibérés, pour que personne ne les rebouche par erreur :

- **`17` est vide** : c'était la capture de l'extrait CSS, retirée au lot 10
  parce que le kit ne produit pas d'extrait CSS. Ne pas réaffecter ce numéro.
- **`06b`** s'insère entre `06` et `07` plutôt que de décaler la suite : la carte
  du plugin avant installation est une étape intermédiaire, et renuméroter aurait
  fait mentir toutes les références déjà écrites.

---

## 4. Le protocole de prise

**Ce chapitre est exécutable seul.** Il ne suppose pas d'avoir lu le reste.

### 4.0 Avant de commencer — cinq consignes

1. **Aucune clé, aucun jeton, aucun secret visible.** Sur toute capture qui
   montre le plugin de pont, un terminal d'agent, un fichier de configuration ou
   une variable d'environnement : masquer la valeur **avant** d'enregistrer le
   fichier, ou masquer le champ à l'écran. Les deux captures du vault d'origine
   qui montraient la clé ont dû être reprises ; elles portent aujourd'hui un
   cadre rouge et la mention « cle API masquee ». Reprendre ce procédé.
2. **Contrôler l'image après la prise, pas seulement le geste.** Ouvrir le
   fichier et vérifier qu'il montre ce que la ligne dit. Une capture du vault
   d'origine montre le panneau du graphe là où elle annonce un menu contextuel :
   personne ne l'a rouverte.
3. **Travailler sur un vault de démonstration NEUTRE**, semé pour la séance,
   **hors de tout dépôt**, et jamais sur un brain réel. Aucun nom de sujet,
   aucun nom de tiers, aucun contenu privé ne doit apparaître — **y compris
   dans la barre de titre de la fenêtre**, qui affiche le nom du coffre ouvert.
   C'est ce point qui a fait reprendre quatorze captures (§2). Le brain de
   démonstration se sème depuis `gabarit/brain.yml`, dont les valeurs sont
   volontairement vides de sens (« Domaine A », « Unité »), et son **dossier**
   se nomme neutrement lui aussi — c'est ce nom-là qui s'affichera.
4. **Un environnement, et le dire.** Les captures présentes ont été prises sous
   **Obsidian 1.13.7 en français, Windows 11**. Rester sur la même version et la
   même langue, sinon les deux jeux ne se ressemblent plus.
5. **Format et nom.** PNG, nom exact de la table ci-dessous, dans `docs/img/`.
   Ne pas retailler : la largeur d'origine des captures présentes va de 1200 à
   1950 pixels, et la documentation les affiche à la largeur du texte.

### 4.1 Préparer la scène

Trois choses, une fois pour toutes, avant la première prise :

```bash
# 1. semer un brain de demonstration, hors de tout depot
brainkit semer --manifeste exemples/histobrain.brain.yml --dans ~/DemoBrain --ecrire

# 2. lui donner de quoi montrer quelque chose : au moins trois unites
#    comparables, une page de vue, un hub avec un corps ecrit a la main,
#    et une page dont un champ de haut de page est VIDE
#    (c est le sujet de la capture 22)

# 3. l ouvrir dans Obsidian, et faire docs/04-obsidian.md du debut a la fin
```

Le point 2 n'est pas une formalité : cinq des seize captures ne montrent rien
sur un vault vide. La table le dit ligne par ligne, colonne *Avant*.

### 4.2 La table de prise — 16 captures, dans l'ordre

Les colonnes se lisent : **Écran** = où l'on est ; **Avant** = ce qu'il faut
avoir fait ; **Cadrer** = ce qui doit tenir dans l'image ; **Masquer** = ce qui
ne doit pas y être.

| # | Fichier | Écran | Avant | Cadrer | Masquer |
|---|---|---|---|---|---|
| 1 | `18-selecteur-dossier-du-vault.png` | la boîte de dialogue système « Sélectionner un dossier » | avoir semé `~/DemoBrain`, ouvert Obsidian et cliqué *Ouvrir un dossier comme coffre* | la boîte entière, le chemin lisible dans son champ | rien de sensible ; éviter qu'un chemin fasse apparaître un nom de tiers |
| 2 | `30-editeur-proprietes-masquees.png` | Paramètres → **Éditeur**, réglage des propriétés du document | rien | le libellé du réglage et sa valeur ; si le sélecteur est ouvert, ses **trois** valeurs | rien |
| 3 | `31-fichiers-liens-filtres-exclusion.png` | Paramètres → **Fichiers & Liens**, section *Filtres d'exclusion* | avoir ajouté l'espace de l'agent à la liste | la section entière, l'entrée lisible, avec assez de contexte pour la situer | rien |
| 4 | `14-file-hider-menu-contextuel.png` | l'explorateur du vault, **menu contextuel ouvert** sur le dossier de l'agent | File Hider installé et activé ; l'explorateur en barre latérale gauche ; **aucun onglet de graphe ouvert** | la barre latérale **et** le menu en entier, entrée *Hide Folder* lisible | rien ; vérifier qu'aucun autre onglet n'expose de contenu |
| 5 | `15-file-hider-apres.png` | le même explorateur, après masquage | avoir cliqué *Hide Folder* | la barre latérale seule, assez large pour qu'on voie que le dossier a disparu et les autres non | rien |
| 6 | `16-graphe-groupes-reglages.png` | le **panneau du graphe**, onglet *Groupes*, sélecteur de couleur ouvert | ouvrir le graphe, son engrenage, *Groupes* ; saisir **une** requête et ouvrir son sélecteur | le panneau *Groupes* **plus** le sélecteur, champs **R / G / B** visibles — c'est ce champ qu'on cherche, et il est en bas | rien ; la requête doit être celle du vault de démonstration |
| 7 | `25-graphe-colore.png` | le graphe entier, table appliquée | avoir saisi **toutes** les lignes du groupe, dans l'ordre, puis fermé le panneau | la zone du graphe, sans la barre latérale si possible : c'est la répartition des couleurs qui est le sujet | les noms de page si le vault porte du contenu de tiers |
| 8 | `19-arbre-du-vault.png` | la barre latérale d'Obsidian | replier tout, puis déplier la racine sur **un** niveau | tous les dossiers de premier niveau et les fichiers de la racine | rien |
| 9 | `20-porte-d-entree.png` | la porte d'entrée du vault, en mode lecture, à côté de l'arbre | l'ouvrir depuis la racine | l'arbre à gauche **et** la page à droite dans le même écran : c'est leur rapport qui est le sujet | rien |
| 10 | `21-page-d-unite-proprietes.png` | une page d'unité, mode lecture, frontmatter **déplié** | régler les propriétés sur *Visible* ; avoir capturé une **vraie** page — une page vide ne montre rien | tout le bloc de propriétés **plus** les premières lignes du texte | rien |
| 11 | `22-bandeau-genere.png` | le haut d'une page d'unité, haut de page généré | capturer une page dont un champ de haut de page **n'est pas renseigné** : c'est le sujet de l'image | le tableau du haut de page en entier, **la cellule vide comprise** | rien |
| 12 | `23-page-de-vue.png` | une page de vue | le vault doit porter au moins **trois** unités comparables, sinon la table est vide | la fin de la table **et** le début de la section écrite à la main, dans le même écran | rien |
| 13 | `24-hub-zone-auto.png` | un hub, mode lecture | choisir un hub d'un dossier à au moins deux pages, **et lui avoir écrit un corps à la main** | les **bornes** de la zone générée doivent être lisibles : c'est la frontière qu'on montre | rien |
| 14 | `26-verdict-valider.png` | le terminal | `cd ~/DemoBrain && brainkit valider` | la commande tapée **et** tout le verdict, jusqu'au code de sortie | vérifier qu'aucune variable d'environnement ne s'affiche dans l'invite |
| 15 | `27-verdict-generer-check.png` | le terminal | `brainkit generer`, juste après | la commande et le rapport entier, avec la ligne qui dit qu'il ne reste aucun écart | idem |
| 16 | `28-agent-connecte.png` | le terminal de l'agent | Obsidian ouvert sur le vault, pont activé, serveur MCP déclaré ; demander à l'agent de lister trois pages | la demande **et** la réponse, assez pour qu'on voie que ce sont des pages du vault | **la clé d'API si elle apparaît** dans une configuration ou une variable. C'est la capture la plus risquée du lot |

### 4.3 Après la séance — deux gestes, dans cet ordre

1. **Convertir chaque trou nommé en balise d'image.** Dans le document qui la
   nomme, remplacer le bloc

   ```
   > **Capture à prendre en séance** — `img/NN-nom.png`
   > Écran : …
   ```

   par la balise, avec un texte alternatif qui décrit ce qu'on voit :

   ```
   ![Ce que la capture montre](img/NN-nom.png)
   ```

   L'outil de contrôle **signale** un fichier présent qu'un document annonce
   encore comme « à prendre » : c'est exactement la dérive qu'il attrape.

2. **Passer le contrôle :**

   ```bash
   uv run outils/captures.py --liste
   ```

   Il doit sortir en **0**, et la ligne « à prendre en séance » doit avoir
   diminué d'autant.

---

## 5. Le contrôle, et pourquoi il regarde dans quatre directions

`outils/captures.py`. Il ferme la remontée 8 du lot 10.

| Direction | Ce qu'elle attrape | Sévérité |
|---|---|---|
| une image **référée** par une balise doit exister | une image brisée dans le rendu | écart, code 2 |
| une image **présente** doit être référée | un fichier mort qui grossit le dépôt et vieillit sans qu'on le voie | écart, code 2 |
| un **trou nommé** ne doit **pas** encore exister | la séance a eu lieu et personne n'a converti le trou en balise | écart, code 2 |
| chaque capture de portée **kit** du manifeste d'instance doit être couverte | une capture déclarée qu'on a oubliée en silence | avertissement |

La quatrième est un avertissement et pas une faute, et le motif est écrit dans
l'outil : une capture déclarée pour une **instance** peut légitimement ne pas
illustrer la doc du **kit**. Ce qui serait une faute, c'est de l'oublier sans
que rien ne le dise.

### Ce que le contrôle ne fait pas

**Il ne regarde pas le contenu d'une image.** Il ne peut donc pas dire qu'une
clé y est visible. C'est une relecture humaine, et c'est la première consigne du
§4.0.

État à l'écriture de ce rapport :

```
15 image(s) référée(s) par une balise
16 capture(s) nommée(s) « à prendre en séance »
15 fichier(s) dans docs/img/
16 captures de portée kit déclarées, 16 couvertes
OK — aucune image référée ne manque, aucune image posée n'est orpheline.
```

---

## 6. Les remontées

Par ordre de coût, comme dans les rapports précédents.

**Presque gratuites :**

1. **Le chemin `mo is None` de `brainkit/emballer/install.py` n'a plus
   d'appelant.** `rendus_du_kit()` est retiré ; les quatre sections qui ne
   servaient qu'au document du dépôt (`_installer_le_kit`, `_entretien`,
   `_semer`, `_profils`) et les vingt branches `mo is None` sont désormais du
   code mort. Son retrait est un refactor d'environ 250 lignes du générateur —
   **hors du périmètre d'un lot de documentation**, et à faire d'un seul geste
   avec le jeu d'épreuve sous les yeux. *(≈ 250 lignes supprimées, aucune
   ajoutée)*

2. **Le contrôle des promesses commerciales ne contrôlait rien.** Les motifs de
   `INTERDITS_COMMERCIAUX`, dans `tests/emballage.py`, portaient des octets
   `0x08` — un caractère de retour arrière — là où le code voulait des `\b` de
   frontière de mot. Aucun de ces motifs ne pouvait donc correspondre à quoi que
   ce soit, et le contrôle passait au vert sur n'importe quel texte. Le défaut
   vient d'une écriture par document interstitiel de shell, où `\b` a été
   interprété. **Corrigé dans ce lot**, parce que ce lot ajoute neuf fichiers à
   la liste que ce contrôle surveille : laisser une garde morte en affirmant que
   les documents sont propres aurait été faux. *(1 ligne)*

**Un peu de travail :**

3. **La séance de prise elle-même** : 16 captures, §4. C'est la seule partie du
   livrable dont la justesse repose sur une transcription et non sur une
   exécution. *(≈ 1 heure)*

4. **Reprendre `09-plugin-rest-api-mcp.png`** en faisant défiler jusqu'au bloc
   de configuration, pour qu'on le voie. Confort, pas correction : le document
   dit déjà que le bloc est sous la ligne de pliure et qu'il se copie depuis
   l'écran. *(1 capture)*

**Dans le vault d'origine, donc hors périmètre :**

5. **Trois défauts d'images dans le guide d'installation du vault d'origine**,
   trouvés en regardant les 28 fichiers un par un :
   `16-file-hider-context-menu.png` ne montre pas le menu contextuel mais le
   panneau du graphe ; `11-all-plugins-installed.png` et
   `12-all-plugins-enabled.png` sont **le même fichier**, appelés à deux étapes ;
   `25-graph-groupes-config.png` et `26-graph-colore.png` de même. Ce lot n'écrit
   pas dans le vault d'origine — il l'a lu et en a copié des images. *(3 reprises,
   dans l'autre dépôt)*

6. **Le guide du vault d'origine annonce Obsidian 1.12.7 ; ses captures montrent
   1.13.7.** Même remarque de périmètre. *(1 ligne, dans l'autre dépôt)*

---

## 7. Le critère de ce lot, et comment il a été tenu

| Critère | Comment il est vérifié |
|---|---|
| le skill de documentation a été suivi | ossature du README (titre, pitch, bandeau de stack, sommaire, architecture, démarrage, tests, structure, licences), tableaux, mermaid, patron décisionnel, zéro pictogramme décoratif, tableau des licences. Contrôlé par le vérificateur du skill |
| la doc du kit couvre les six sujets demandés | installation `docs/03`, configuration d'Obsidian `docs/04`, premier usage `docs/05`, manuel `docs/06`, livraison hors ligne `docs/07`, et le cadrage et l'architecture qui les portent |
| un lecteur qui ne connaît rien installe et sème en la suivant seule | installation à blanc rejouée, §8 |
| le contrôle des images passe | `uv run outils/captures.py` — code 0 |
| les jeux d'épreuve restent verts | les dix, plus les trois outils de dépôt |
| le vault d'origine n'est pas touché | `git status` vide dans l'autre dépôt |

---

## 8. L'installation à blanc, rejouée

Le lot 10 avait rejoué son installation à blanc sur l'`INSTALL.md` généré et
trouvé **7 trous**. Celle-ci a été rejouée sur la nouvelle documentation, dans
`~/Documents/BrainKit-essais/blanc-lot12/`, en ne lisant que `docs/`.

**Le protocole, pour qu'on puisse le refaire.** Le kit a été obtenu par la forme
que `docs/03-installation.md` §2 recommande — un `git bundle`, cloné dans un
dossier vierge — puis les chapitres ont été suivis dans l'ordre annoncé par
`docs/README.md` : `03` (pré-requis, hooks, lancement, vérification) puis `05`
(entretien, composition, semis, garde-fous, vérification). Chaque commande a été
lancée telle qu'elle est écrite, et son code de sortie relevé. Le brain d'essai a
été composé par la **porte de service** de l'entretien
(`--reponses tests/blanc.reponses.yml`) : rejouer un entretien est le seul moyen
de le faire sans conversation, et c'est l'usage que le document prescrit pour ce
cas.

Ce qui a **marché du premier coup**, et vaut d'être noté parce que le reste ne
parle que des trous : la fabrication et le clonage du bundle, l'activation des
hooks du kit puis de l'instance, `brainkit` qui liste ses huit sous-commandes,
`schema/valider.py` et `tests/epreuve.py` verts, les onze passes de l'entretien,
la composition du manifeste, sa relecture contre le contrat, le semis en mode
lecture puis en écriture (48 fichiers, dépôt initialisé, premier commit), et le
verdict final du vault — **aucune violation dure, 14 artefacts concordants, arbre
propre**. Le chemin complet tient donc, et l'identité posée par le semis était la
bonne.

Les trous trouvés — et corrigés dans les documents avant l'écriture de ce
rapport. Les huit premiers sont sortis de la rédaction, les trois derniers de
l'exécution :

| # | Trou | Où il est corrigé |
|---|---|---|
| 1 | l'URL de clone du dépôt nomme un **alias SSH** (`github.com-perso`) défini dans le `~/.ssh/config` d'une seule machine. Un lecteur sur un poste neuf obtient un échec de résolution d'hôte, sans indice | `docs/03-installation.md` §2, encadré « Attention à un piège de forme » |
| 2 | rien ne disait comment retrouver l'URL depuis une copie déjà présente | `docs/03-installation.md` §2, `git -C … remote get-url origin` |
| 3 | `brainkit` sort en **code 2** quand il réussit à s'afficher. Un lecteur qui contrôle par le code de sortie croit à un échec | `docs/03-installation.md` §5, table des attendus |
| 4 | l'ordre des chapitres n'était pas dit : on règle Obsidian **après** avoir semé, et plusieurs étapes du réglage demandent le vault sous les yeux | `docs/README.md`, « la route complète » |
| 5 | les hooks du **kit** et ceux de l'**instance** s'activent par la même commande, dans deux dépôts différents. Rien ne le disait, et le lecteur qui l'a fait une fois croit avoir fini | `docs/03-installation.md` §3 (encadré final) et `docs/05-premier-brain.md` §5 |
| 6 | `BRAINKIT_RACINE` était nommée sans qu'on dise comment la poser durablement, ni comment sur Windows | `docs/03-installation.md` §4 |
| 7 | masquer un dossier avec File Hider ne le sort **pas** de la recherche. Le lecteur croit l'espace de l'agent écarté, et le retrouve dans tous ses résultats | `docs/04-obsidian.md` §6, et une entrée de dépannage |
| 8 | cinq des seize captures à prendre ne montrent rien sur un vault vide. Un opérateur qui suit le protocole sur un brain fraîchement semé prend cinq images inutiles | §4.1 de ce document, point 2, et colonne *Avant* de la table |
| 9 | le document affirmait qu'un clone de bundle atterrit **en HEAD détachée** et disait de faire `git switch -c main`. **Faux pour un bundle `--all`** : le clone arrive sur `main`, et la commande prescrite échoue avec `fatal: a branch named 'main' already exists`. Une instruction qui échoue au deuxième pas d'un guide d'installation coûte cher en confiance | `docs/03-installation.md` §2 — le cas est devenu conditionnel, avec le contrôle `git status \| head -1` et les deux réponses |
| 10 | **le trou le plus grave.** `docs/05` §6 donnait `brainkit valider` sans rappeler que la commande n'existe que si l'on a pris la façon **b** du §4. Un lecteur qui a pris la façon **a** obtient `Failed to spawn: brainkit — program not found` sur la commande qui devait couronner son installation | `docs/03-installation.md` §4 (la voie **a** dit maintenant qu'elle ne suffit pas depuis un vault, avec le message exact) et `docs/05-premier-brain.md` §6, qui donne en plus un repli `--vault` **vérifié** |
| 11 | les deux bouchons du trou « une instance ne sait pas où vit le kit » étaient présentés comme **équivalents** (« les deux bouchons sont bons »). Ils ne le sont pas : le résolveur `_pont_kit.py` est une **bibliothèque**, importée par des scripts de pont que le semis ne pose **que** si le manifeste déclare `agent.ponts`. Sur le brain d'essai, `AI/scripts/` ne contenait que le résolveur et un fichier d'explication — **rien à lancer** | `docs/03-installation.md` §4, encadré réécrit : le bouchon 1 est celui dont tout brain a besoin, le bouchon 2 est un confort pour un brain qui déclare ses ponts |
| 12 | le premier `uv run` construit le paquet et imprime deux lignes `Building brainkit @ …`, et il a besoin d'atteindre un index de paquets. « Obtenir le kit hors ligne » et « le lancer hors ligne » sont deux problèmes, et le document les confondait | `docs/03-installation.md` §4a |
| 13 | un brouillon neuf annonce « 0 réponse(s) sur **49** questions, **40** restante(s) ». Neuf questions sont conditionnelles ; un lecteur qui compte croit à un défaut | `docs/05-premier-brain.md` §2 |

**Treize trous, contre sept au lot 10.** Le compte plus élevé n'est pas un signe
de moindre soin : il vient de ce que la surface a grandi (neuf documents au lieu
d'un) et surtout de ce que le lot 10 rejouait un document **généré**, dont les
commandes avaient déjà été exercées par le jeu d'épreuve. Ici, quatre des cinq
trous trouvés à l'exécution (9 à 12) portent sur des **affirmations de prose**
qu'aucun test ne pouvait contredire : l'état de HEAD après un clone de bundle, la
portée d'une commande selon la voie d'installation choisie, l'équivalence de deux
bouchons. C'est précisément la raison d'être d'une installation à blanc, et la
raison pour laquelle une doc écrite à la main en a plus besoin qu'une doc
générée.
