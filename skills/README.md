# `skills/` — des enveloppes, et rien de plus

Ce dossier contient des fichiers au format de **Claude Code**. Chacun est une
enveloppe de quinze lignes qui pointe vers une recette de
[`../recettes/`](../recettes/README.md).

**Une seule source : la recette.** Le jour où un autre agent aura son propre
format, on ajoutera une enveloppe à côté — jamais une seconde version du
contenu. Deux fichiers qui décrivent la même chose divergent ; c'est le constat
qui a fait naître le manifeste, et il vaut aussi ici.

| Enveloppe | Recette |
|---|---|
| `entretien/SKILL.md` | [`recettes/mener-l-entretien.md`](../recettes/mener-l-entretien.md) |

Les autres recettes n'ont pas d'enveloppe, et ce n'est pas un oubli : elles
s'invoquent en langage naturel, et `AGENTS.md` suffit à les trouver. Une
enveloppe ne se justifie que là où le déclenchement automatique apporte quelque
chose — ici, reconnaître « je veux un second brain sur X » sans que personne ait
à nommer un fichier.

> **À ne pas confondre avec les skills d'une instance.** Un vault semé reçoit
> **ses** skills — capture, clôture, exploitation — **générés depuis son
> manifeste**, dans `<vault>/.claude/skills/`. Ceux-là nomment ses rôles et ses
> axes ; ils ne sont pas génériques, et ils ne vivent pas ici.
