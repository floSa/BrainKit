# HistoBrain — Manuel d'utilisateur

> **Document GÉNÉRÉ** depuis `brain.yml` par BrainKit `0.1.0`. Ne pas l'éditer à la main : il se régénère.

Ce document dit **ce qu'on a sous les yeux** en ouvrant le vault, et comment y retrouver quelque chose.

Voir aussi : [enrichir.md](enrichir.md) pour écrire dedans · [exploiter.md](exploiter.md) pour s'en servir · `../INSTALL.md` pour l'installer

---

## 1. Le vault en une phrase

**Un dossier par période à la racine, et une page qui dit ce qu'elle est.**

Il n'y a rien d'autre à comprendre. Pas de hiérarchie parallèle, pas de dossier d'attente, pas de galaxie. Le dossier porte la valeur de `categorie:` ; le champ `role:` porte ce que la page **est**. Les deux axes ne se recouvrent pas, et c'est ce qui permet à deux pages de nature différente de vivre dans le même dossier sans que rien ne soit ambigu.

---

## 2. Les 6 natures de page

C'est le champ `role:` du frontmatter qui porte la nature d'une page. **Il ne se devine pas depuis le chemin** : deux pages de nature différente et de même période vivent dans le même dossier, et un `ls` ne les distingue pas.

| `role:` | Ce que c'est | Rangée par | Protégée |
|---|---|---|---|
| `chronologie` | ce qui départage plusieurs pages d'un même thème | `categorie:` | non |
| `controverse` | un objet transverse par construction, qui ne dépend d'aucune valeur de l'axe de rangement | son rôle → `Controverses/` | non |
| `hub` | la page d'aiguillage d'un dossier — elle n'explique rien, elle oriente | elle **est** le rangement | non |
| `methode` | un objet transverse par construction, qui ne dépend d'aucune valeur de l'axe de rangement | son rôle → `Méthodes/` | non |
| `notion` | ce qu'il faut comprendre | `categorie:` | **oui** |
| `source` | ce qu'on vient chercher dans le brain | `categorie:` | non |

La colonne du milieu n'est pas une paraphrase du mot : c'est la **fonction** que le rôle déclare, prise dans une liste fermée de six. Le vault se lit dans les mots de son sujet ; le kit, lui, ne raisonne que sur ces six-là. Un seul endroit fait le pont, et c'est `brain.yml`.

Une page **protégée** est la mémoire personnelle du propriétaire du brain. On y ajoute volontiers ; on n'y réécrit pas sans qu'il l'ait demandé. La frontière se lit dans le frontmatter, page par page — jamais sur un chemin.

Les couleurs du graphe sont ce même axe, en visuel : une couleur par `role:`. La table est dans `../Documentation/graphe.md`.

---

## 3. Où vit une page

**Personne ne choisit un dossier.** Le chemin se dérive du champ `categorie:` — 8 valeurs de premier niveau, et le validateur le vérifie page par page : une page hors de son dossier dérivé est une violation, pas un rangement personnel.

Un sous-dossier apparaît quand une sous-valeur atteint **12** page(s), sauf s'il ne laisserait aucune page au niveau du parent — un dossier fils qui redouble son parent n'apporte rien. Changer ce seuil est une **migration** outillée, pas un réglage : elle déplace des pages, par `git mv`.

L'axe n'est **pas exclusif** : une page peut porter plusieurs valeurs de `categorie:`. Son dossier est alors celui de la valeur dominante — la valeur de l'axe est celle qui rassemble le plus de la page, et le préfixe `transversal` est réservé aux pages qu'aucune valeur ne rassemble.

| Période | Dossier | Portée |
|---|---|---|
| `prehistoire` | `Préhistoire/` | avant l'écriture |
| `antiquite` | `Antiquité/` | jusqu'à 476 |
| `medieval` | `Moyen Âge/` | 476 à 1492 |
| `moderne` | `Époque moderne/` | 1492 à 1789 |
| `revolutions` | `Révolutions et empires/` | 1789 à 1815 |
| `industriel` | `Âge industriel/` | 1815 à 1914 |
| `xxe` | `XXe siècle/` | après 1914 |
| `transversal` | `Transversal/` | les synthèses de longue durée, sans centre de gravité |

**L'axe transverse `themes:`** traverse l'arbre : un hub par valeur **portée**, dans `Thèmes/`. Un hub y naît quand une page porte la valeur, pas avant — une page vide dans un graphe est un nœud de plus qui ne rassemble rien.

**L'axe transverse `espaces:`** traverse l'arbre : un hub par valeur **portée**, dans `Espaces/`. Un hub y naît quand une page porte la valeur, pas avant — une page vide dans un graphe est un nœud de plus qui ne rassemble rien.

---

## 4. Lire une page `role: source`

Une source suit toujours le même gabarit. De haut en bas :

| Section | Ce qu'elle contient | Ce qu'elle ne contient pas |
|---|---|---|
| `<bandeau>` | les colonnes du haut de page, composées depuis le frontmatter | **rien d'écrit à la main** — la zone est générée |
| `Ce que c'est` | La SEULE section ou la prose est permise. | ce que le haut de page dit déjà |
| `Ce qu'elle établit / Ce qu'elle ne peut pas établir` | un tableau à deux colonnes : *Établit* et *N'établit pas* | de la prose |
| `Comment y accéder` | 5 étiquette(s) obligatoires : `Édition`, `Langue`, `Accès`, `Cote`, `Coût` | de la prose, et aucune étiquette hors de la liste |
| `Autour` | des puces, une idée par puce | — |
| `Contredit par` | une puce par cible, adossée à `contredit:` | un lien cité au milieu d'une phrase — ça ne LISTE pas |
| `Prolonge` | une puce par cible, adossée à `prolonge:` | un lien cité au milieu d'une phrase — ça ne LISTE pas |
| `Prolongée par` | une puce par cible, adossée à `prolonge_par:` | un lien cité au milieu d'une phrase — ça ne LISTE pas |
| `Voir aussi` | une puce par lien interne | un lien cité au milieu d'une phrase — ça ne LISTE pas |

**Une ligne, une étiquette, une idée.** La prose ne vit que dans la section qui la déclare ; partout ailleurs, des puces.

Et les sections **conditionnelles** — elles n'existent que si elles se remplissent. Une section conditionnelle vide se **supprime** :

- `Notes de lecture` — n'existe que si au moins une entrée datée.

### Le haut de page

| Colonne | Composée depuis |
|---|---|
| Nature | `nature` |
| Auteur et date | `auteur`, qualifié par `date_publication` |
| Langue | `langue` |
| Fiabilité | `fiabilite` |

**Une cellule vide est un fait, pas un oubli.** Une cellule sans source dans le frontmatter affiche un tiret cadratin, jamais une valeur plausible — une fiche vide honnêtement vaut mieux qu'une fiche remplie au jugé.

---

## 5. Lire une page `role: chronologie`

Deux fichiers portent le même nom : la **page** `.md` et la **vue** `.base`.

- La vue est une **requête**, rendue par `obsidian-bases`. Elle liste les pages qui remplissent son filtre et affiche leur frontmatter en tableau. Elle se remplit toute seule : une page ajoutée y entre sans que personne n'y touche.
- La page **embarque** ce tableau, et ajoute ce que le tableau ne peut pas dire.

**C'est là qu'est la valeur** : `Ce que la séquence montre`, `Voir aussi`. Un tableau dit que deux pages portent la même valeur — c'est vrai et ça n'apprend rien. La section écrite dit ce qui les distingue.

Toutes les pages `chronologie` sont réunies par le hub de `Chronologies/`, où qu'elles vivent dans l'arbre. **C'est le lien retour qui fait la grappe** : un hub qui cite N pages sans qu'aucune le cite ajoute un nœud et ne rassemble rien.

---

## 6. Trouver quelque chose

Par ordre d'efficacité :

1. **Tu sais quoi chercher** → ouvrir par le nom (`Ctrl+O`). Les liens du vault sont **nus** : le nom de fichier suffit, quel que soit le dossier.
2. **Tu hésites entre deux pages** → la page `chronologie` du dossier, et directement sa section écrite à la main.
3. **Tu explores** → le hub du dossier. Sa zone générée liste tout ce que le dossier contient ; son corps, écrit à la main, dit ce qui départage les sous-dossiers.
4. **Tu pars d'un axe transverse** → `Thèmes/`, un hub par valeur de `themes:`.
5. **Tu pars d'un axe transverse** → `Espaces/`, un hub par valeur de `espaces:`.
6. **Tu veux le catalogue entier** → `../AI/index/` : le catalogue machine, le document humain et la carte des liens, tous trois **générés**.
7. **Tu veux voir les liens** → le graphe, coloré par `role:`.

---

## 7. Ce qui est généré, et qu'on ne touche pas

| Quoi | Généré par |
|---|---|
| `AI/index/` | build_index |
| `zones AUTO des hubs` | build_mocs |
| `Thèmes/` | build_mocs, depuis `axes.transverses[themes]` |
| `Espaces/` | build_mocs, depuis `axes.transverses[espaces]` |
| `Chronologies/Chronologies.md` | build_mocs |
| `AI/index/liens.md` | build_links |
| `bandeaux des sources` | build_bandeau |
| `Documentation/periodes/taxonomie.md` | kit, depuis `axes` |
| `Templates/` | kit, depuis `roles[].champs et roles[].corps` |
| `docs/` | kit, depuis `tout le manifeste` |

Éditer l'un de ces blocs à la main, c'est écrire quelque chose que la prochaine régénération effacera. Le **corps** d'un hub, lui, s'écrit à la main — c'est la zone générée qui est intouchable, pas la page.

Le contrôle est une commande, et elle sort en 2 s'il reste un écart :

```bash
brainkit generer            # --check
```
