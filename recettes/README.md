# Les recettes

Une recette par tâche. **Markdown pur** : elles s'exécutent avec un système de
fichiers et un terminal, et rien d'autre. Aucun format de skill propriétaire,
aucune clé d'API, aucun compte.

C'est la **source unique**. Les enveloppes de `skills/` (format Claude Code) ne
font que pointer ici ; si un autre agent a son propre format un jour, on ajoutera
une enveloppe, pas une seconde version du contenu. Une recette et un autre
document qui se contredisent : la recette gagne.

| Recette | Quand | Critère de fin |
|---|---|---|
| [mener-l-entretien.md](mener-l-entretien.md) | « je veux un second brain sur X » | un `brain.yml` valide, un vault vert, **zéro page de contenu** |
| [semer-une-instance.md](semer-une-instance.md) | un `brain.yml` existe, le vault non | le vault existe, `valider` et `generer --check` sont muets |
| [capturer-une-page.md](capturer-une-page.md) | « ajoute X au brain », « documente Y » | la page ET son rayon de propagation, clôturés |
| [cloturer-une-ecriture.md](cloturer-une-ecriture.md) | après TOUTE écriture dans un vault | artefacts régénérés, validateurs verts, commit intégré |
| [mesurer-et-durcir.md](mesurer-et-durcir.md) | « peut-on rendre cette règle dure ? » | une décision **chiffrée**, ou un refus qui dit ce qui manque |
| [livrer-une-instance-figee.md](livrer-une-instance-figee.md) | livraison hors ligne, ou sans le kit à côté | l'instance figée rend le **même verdict**, ligne pour ligne |

---

## Ce qui vaut dans toutes les recettes

**Rien ne se devine.** Ni un axe, ni une sévérité, ni un seuil, ni une identité
git, ni le libellé d'un dossier promu. Un champ vide est une question ouverte ;
une valeur inventée est une faute. Quand une recette dit « demander », elle veut
dire : poser la question à l'humain, et **attendre**.

**Une ligne sans objet se déclare sans objet, elle ne se tait pas.** Un silence
se lit comme un oubli ; une ligne qui dit « sans objet ici, parce que ceci » se
lit comme une décision.

**Tu ne durcis jamais une règle sans avoir compté ses violations**, et jamais
sous 30 pages d'unité : en dessous, zéro violation ne prouve rien.

**Tu n'assouplis jamais sans écrire le motif.** Le kit refuse un
`severite: avertissement` sans `motif:`.

**Un déplacement se fait par `git mv`**, jamais par suppression puis création :
sans quoi l'historique de la page est perdu.

**L'identité git ne se devine JAMAIS.** L'adresse que ton harnais t'annonce
t'identifie auprès d'un outil ; elle n'attribue pas un commit. Jamais de
`-c user.email`, de `--author`, de `GIT_AUTHOR_EMAIL`, ni de `--no-verify`.

---

## Deux choses que ces recettes ne remplacent pas

**Les documents d'une instance.** Un vault semé porte les siens, **générés
depuis son manifeste** : `INSTALL.md` à la racine, puis `docs/manuel.md`,
`docs/enrichir.md` et `docs/exploiter.md`. Ils nomment SES rôles, SES axes, SES
règles — ce qu'une recette générique ne peut pas faire. Quand tu travailles dans
un vault, **lis-les d'abord** ; les recettes d'ici donnent la méthode, ces
documents-là donnent les valeurs.

`gabarit/rendu/` en montre un exemplaire complet, rendu depuis le manifeste de
référence, pour qu'on puisse les lire sans avoir semé quoi que ce soit.

**Le journal de conception.** `design/` dit *pourquoi* chaque décision a été
prise, avec ses mesures. Ce sont des archives, pas la doc du produit — voir
`AGENTS.md` §6.
