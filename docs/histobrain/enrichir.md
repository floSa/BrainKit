# HistoBrain — Enrichir le brain

> **Document GÉNÉRÉ** depuis `brain.yml` par BrainKit `0.1.0`. Ne pas l'éditer à la main : il se régénère.

Comment ajouter une page, et **ce que ça déclenche autour**.

Voir aussi : [manuel.md](manuel.md) pour lire le vault · [exploiter.md](exploiter.md) pour s'en servir

---

## 1. Tu ne crées pas une page, tu déclenches une propagation

**Le rayon de propagation d une insertion est le DOSSIER D ACCUEIL, plus ses HUBS PARENTS. Le voisinage d une page est `ls` de son dossier.**

C'est le point à avoir en tête avant tout le reste : **une page ne s'ajoute jamais seule.** Une page nouvelle change au moins 9 autres choses, et si on ne les change pas le vault ment.

> Une ligne sans objet se DECLARE sans objet, elle ne se tait pas.

Le skill **`enrichir-histobrain`** porte cette règle. On l'appelle en langage naturel, depuis un agent lancé **dans le dossier du vault**.

Il a un **mode lot** : capturer plusieurs pages d'un même dossier en une conversation, en n'appliquant la propagation qu'une fois à la fin. Sans lui, l'amorçage d'un brain neuf coûte une conversation par page, et personne ne le fait.

---

## 2. Le rayon — ce que le skill fait, et que tu n'as pas à faire

| # | Cible | Trouvée par | Par | Sans objet si |
|---|---|---|---|---|
| P1 | le hub du dossier d'accueil — `<D>/<D>.md` | `ls "$D"` : le dossier porte une page à son nom | généré (zone AUTO) — **le corps, lui, est à relire** | — |
| P2 | les hubs parents, jusqu'à la racine | remontée de chemin : chaque niveau de `$D` porte son hub | généré (zone AUTO) — **le corps, lui, est à relire** | la page atterrit directement dans le dossier de période : P1 et P2 désignent alors la même page, et il faut le DIRE |
| P3 | la chronologie du dossier — `role: chronologie` | `ls "$D"/'Chronologie - '*` | la vue `.base` : **automatique** si elle filtre sur `categorie` — la page y entre toute seule ; le fichier `.base` n'est PAS généré (`vue_embarquee.genere: false`) : il se lit, il ne se réécrit pas · « Ce que la séquence montre » · « Voir aussi » : à écrire | le dossier ne porte aucune page `role: chronologie` — et alors la question est : faut-il en créer une ? |
| P4 | la notion du dossier — `role: notion` | `ls "$D"/*.md`, puis lire `role:` dans chaque frontmatter | à écrire, **dans les deux sens** — et c'est un rôle **PROTÉGÉ** : la créer est normal (c'est cette ligne) ; **modifier une page `role: notion` qui existe déjà demande une demande explicite**. Sinon : proposer, et attendre | le dossier ne porte aucune page `role: notion` — et alors la question est : faut-il en créer une ? |
| P5 | les pairs — les autres `role: source` du dossier | `ls "$D"/*.md`, puis lire `role:` dans chaque frontmatter | à écrire, **réciprocité obligatoire** : `contredit:` (symétrique) et la **paire** `prolonge:` / `prolonge_par:` (inverse). Un pair écarté est un CHOIX, pas un oubli : le dire | le dossier ne porte aucune autre page `role: source` — la page est la première du dossier |
| P6 | les résumés réinjectés — le `apport:` recopié chez les pages citées | les cibles des champs à réciprocité, dans « Contredit par » · « Prolonge » · « Prolongée par » | à écrire — **copié depuis la cible, jamais retapé** | aucune puce n'a été ajoutée dans ces sections |
| P7 | le hub de ralliement `Chronologies/` — **hors du dossier**, à la racine | il ne se lit pas dans `ls "$D"` : il vit à la racine et réunit tous les `role: chronologie` du brain | sa zone AUTO est générée ; **le lien retour vers `[[Chronologies]]` dans « Voir aussi » de la page : à écrire** — c'est lui qui fait la grappe, pas la liste | cette capture ne crée aucune page `role: chronologie` — le hub n'est dans le rayon d'une insertion que si elle en CRÉE une |
| P8 | les hubs de `themes:` — `Thèmes/` | les valeurs de `themes:` que la page porte | généré — le hub d'une valeur naît quand une page la porte | la page ne porte aucune valeur de `themes:` |
| P9 | les hubs de `espaces:` — `Espaces/` | les valeurs de `espaces:` que la page porte | généré — le hub d'une valeur naît quand une page la porte | la page ne porte aucune valeur de `espaces:` |

Cette table est **dérivée** de `roles`, `axes` et `champs` du manifeste — pas écrite à la main, et pas recopiée d'un autre brain. Un manifeste différent donne une table différente ; une table identique sur deux brains différents serait la preuve qu'elle est recopiée.

**Une ligne sans objet se déclare sans objet, elle ne se tait pas.** Un silence se lit comme un oubli ; une ligne qui dit « sans objet ici, parce que ceci » se lit comme une décision.

---

## 3. Les valeurs que tu ne devines jamais

- **`categorie:`** — l'axe qui **range** (période) : *où ça se range*. C'est lui, et lui seul, qui décide du chemin.
- **`nature:`** — l'axe qui **qualifie** (nature) : *ce que c'est*, 9 valeurs fermées.

`Documentation/periodes/taxonomie.md` porte un **arbre de décision déterministe** : questions **fermées**, en **ordre strict**, la première réponse positive gagne. On le déroule, on ne tranche pas au jugé — et l'ordre des questions **est** la décision de conception, prise une fois, valable pour toutes les pages.

**Si aucune question ne tranche : laisser le champ vide et demander.** Un champ vide est une question ouverte ; une valeur inventée est une faute, et elle range la page au mauvais endroit pour toujours.

Un troisième champ, **`role:`**, dit ce que la page *est* — voir le manuel. Les deux axes ne se recouvrent pas.

---

## 4. Les frontières d'écriture


- **Libre** — AI/ hors index/ · Inbox.md
- **Sur confirmation** — toute page d'un rôle non protégé · Documentation/
- **Sur demande EXPLICITE** — toute page d'un rôle `protege: true` — ici les notions, et c'est la frontière la plus sensible du vault
- **Jamais à la main** — les chemins de `genere`
- **Jamais sans accord** — une suppression de page
- **Déplacement** — par `git mv`, JAMAIS par suppression + création

**La frontière se lit sur le champ `role:`, jamais sur un chemin.** `role: notion` — création libre dès qu'une capture en a besoin ; **modification d'une page qui existe déjà sur demande explicite** seulement. Une page voisine, dans le même dossier, sous le même hub, peut être protégée : **lire le frontmatter avant d'écrire.**

---

## 5. Mettre à jour une page qui existe

Jamais un patch improvisé. **Une page qu'on crée n'a pas de consommateurs ; une page qui existe en a.** C'est toute la différence entre créer et mettre à jour, et c'est pour ça que le skill a deux modes.

| Champ modifié | Qui le lit | Comment on vérifie |
|---|---|---|
| `role` | [D] il choisit le GABARIT que le validateur applique : changer ce champ change la liste des champs autorisés (`gabarit_par_role`) · [D] il peut changer le DOSSIER — un rôle `range_par: role` vit dans le sien (`chemin_categorie`) · [G] les zones AUTO des hubs, l'index, la carte des liens · [!] la couleur du nœud dans le graphe (`.obsidian/graph.json` n'est pas versionné) | `brainkit valider` |
| `nom` | [M] le NOM DU FICHIER : il suit, et par `git mv` — jamais par suppression + création, sinon l'historique est perdu · [D] les wikilinks du CORPS des pages qui la citent (`liens_resolus`) · [D] les wikilinks du FRONTMATTER — les champs `type: liens` (`reciprocite`) · [D] l'unicité du nom de fichier, à la casse près (`unicite_du_nom_de_fichier`) · [G] l'index, les zones AUTO des hubs, la carte des liens · [!] les vues `role: chronologie` : le champ est une colonne ou le tri — elles se lisent en direct, mais un filtre qui le vise change de membres | la même commande renvoie **0 ligne** ; `brainkit valider --regle liens_resolus` |
| `alias` | [D] la collision d'alias (`collision_alias`) · [!] la résolution des `[[alias]]` par Obsidian · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit valider --regle collision_alias` |
| `apport` | [M] les puces de « Contredit par » · « Prolonge » · « Prolongée par » chez **toutes** les pages qui citent la cible — le résumé se COPIE depuis la cible, il ne se retape pas · [G] la zone AUTO du bandeau — une cellule sans source affiche « — », jamais une valeur plausible · [!] les vues `role: chronologie` : le champ est une colonne ou le tri — elles se lisent en direct, mais un filtre qui le vise change de membres · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit valider --regle reinjection_du_resume` ; `brainkit generer --check` |
| `categorie` | [D] le CHEMIN doit suivre : la page **déménage**, par `git mv` (`chemin_categorie`) · [G] le hub quitté ET le hub d'accueil · [!] l'entrée / la sortie des vues filtrées sur `categorie` · [!] le SEUIL de promotion : la page change de population — un départ peut dépromouvoir un sous-dossier, une arrivée le promouvoir. C'est `brainkit re-seuiller`, pas une capture · [D] la valeur appartient au vocabulaire déclaré (`vocabulaire_ferme`) · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit valider --regle chemin_categorie` |
| `nature` | [D] la valeur appartient au vocabulaire déclaré (`vocabulaire_ferme`) · [D] les champs CONDITIONNELS qu'il commande — `langue_originale:`, `traduction:`, `cote:` : les retirer quand la condition cesse de tenir (`gabarit_par_role`) · [G] la zone AUTO du bandeau — une cellule sans source affiche « — », jamais une valeur plausible · [!] les vues `role: chronologie` : le champ est une colonne ou le tri — elles se lisent en direct, mais un filtre qui le vise change de membres · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit valider --regle gabarit_par_role` ; `brainkit generer --check` |
| `themes` | [G] les hubs de `Thèmes/` — un hub par valeur portée : celui qu'on quitte peut tomber à zéro page et disparaître · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit generer --check` |
| `espaces` | [G] les hubs de `Espaces/` — un hub par valeur portée : celui qu'on quitte peut tomber à zéro page et disparaître · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit generer --check` |
| `auteur` | [G] la zone AUTO du bandeau — une cellule sans source affiche « — », jamais une valeur plausible · [!] les vues `role: chronologie` : le champ est une colonne ou le tri — elles se lisent en direct, mais un filtre qui le vise change de membres · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit generer --check` |
| `date_publication` | [G] la zone AUTO du bandeau — une cellule sans source affiche « — », jamais une valeur plausible · [!] les vues `role: chronologie` : le champ est une colonne ou le tri — elles se lisent en direct, mais un filtre qui le vise change de membres · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit generer --check` |
| `langue` | [G] la zone AUTO du bandeau — une cellule sans source affiche « — », jamais une valeur plausible | `brainkit generer --check` |
| `fiabilite` | [G] la zone AUTO du bandeau — une cellule sans source affiche « — », jamais une valeur plausible · [!] les vues `role: chronologie` : le champ est une colonne ou le tri — elles se lisent en direct, mais un filtre qui le vise change de membres · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit generer --check` |
| `acces` | [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit valider` |
| `contredit` | [D] le `contredit:` de la cible, en retour (`reciprocite`) · [M] la section « Contredit par » des DEUX pages — le frontmatter et le corps disent la même chose, ou ils mentent tous les deux · [D] une même cible ne se liste QUE dans une section (`citation_unique`) · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page · [D] chaque cible doit exister : un lien mort en frontmatter ne se voit pas à la lecture de la page (`liens_resolus`) | `brainkit valider --regle reciprocite` ; `brainkit valider --regle liens_resolus` |
| `prolonge` | [D] l'INVERSE `prolonge_par:` de la cible — « A prolonge B » implique « B prolonge_par A », **pas** « B prolonge A » (`reciprocite`) · [M] la section « Prolonge » des DEUX pages — le frontmatter et le corps disent la même chose, ou ils mentent tous les deux · [D] une même cible ne se liste QUE dans une section (`citation_unique`) · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page · [D] chaque cible doit exister : un lien mort en frontmatter ne se voit pas à la lecture de la page (`liens_resolus`) | `brainkit valider --regle reciprocite` ; `brainkit valider --regle liens_resolus` |
| `prolonge_par` | [D] l'INVERSE `prolonge:` de la cible — « A prolonge_par B » implique « B prolonge A », **pas** « B prolonge_par A » (`reciprocite`) · [M] la section « Prolongée par » des DEUX pages — le frontmatter et le corps disent la même chose, ou ils mentent tous les deux · [D] une même cible ne se liste QUE dans une section (`citation_unique`) · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page · [D] chaque cible doit exister : un lien mort en frontmatter ne se voit pas à la lecture de la page (`liens_resolus`) | `brainkit valider --regle reciprocite` ; `brainkit valider --regle liens_resolus` |
| `tags` | [D] la valeur appartient à `Documentation/general/tags.md` (mode `ferme`) — une valeur manquante se **propose**, s'ajoute là-bas, PUIS s'utilise (`vocabulaire_ferme`) · [G] l'index — le champ y est publié, donc lu par le skill d'exploitation sans ouvrir la page | `brainkit valider --regle vocabulaire_ferme` |
| `sources_cles` | [D] chaque cible doit exister : un lien mort en frontmatter ne se voit pas à la lecture de la page (`liens_resolus`) | `brainkit valider --regle liens_resolus` |

Cette table est **dérivée** elle aussi : du bandeau, des vues, des champs réciproques, des conditionnels et des champs indexés. Elle est la même que celle du skill de capture — pas une seconde table qui lui ressemblerait.

Les champs qu'elle **ne** montre **pas** sont ceux dont aucun consommateur n'est déclaré : ni indexés, ni au haut de page, ni réciproques, ni adossés à un vocabulaire. Le skill les garde, parce qu'une liste de contrôle exhaustive a besoin de dire « rien à faire ici » ; un guide se lit en entier, et ces lignes-là y noieraient les autres.

---

## 6. Clôturer — la seule étape qu'on ne saute pas

**Toute** écriture dans une page du brain se clôt par le skill **`cloturer-histobrain`**.

1. régénérer les artefacts dérivés
1. passer les DEUX validateurs au vert
1. vérifier la divergence avec la branche distante AVANT tout commit
1. committer et intégrer en fast-forward

```bash
brainkit generer --ecrire
brainkit valider
```

C'est le **seul** endroit où la politique git du vault est écrite — à une exception, et elle est délibérée : la **règle d'identité git** vit aussi dans `CLAUDE.md`, parce que c'est le seul fichier chargé dans chaque conversation, au même moment que l'annonce de l'outil. Une contre-instruction qui arrive après coup arrive trop tard.

Trois hooks versionnés doublent la consigne, parce que la consigne seule n'a jamais suffi. **Un hook qui refuse n'est pas un incident à contourner : c'est la règle qui fonctionne.**

---

## 7. Ce qu'on n'écrit pas

- **Rien qui ne soit sourcé.** Une cellule sans source reste vide et se signale. Des pages remplies de plausible sont pires que des pages vides : on ne sait plus lesquelles croire.
- **Aucune valeur d'axe hors du vocabulaire.** Une famille nouvelle se pose dans `Documentation/periodes/taxonomie.md` — donc dans `brain.yml`, qui le génère — pas dans l'arborescence.
- **Aucune sévérité durcie sans mesure.** `brainkit mesurer` compte ce qu'une règle coûterait **avant** qu'on la durcisse. Porter une sévérité qu'on n'a pas mesurée, c'est porter la mesure d'un autre corpus.
- **Aucun `rm` improvisé.** Un déplacement se fait par `git mv`, sans quoi l'historique de la page est perdu — et l'historique est ce qui distingue un vault d'un dossier de fichiers.
