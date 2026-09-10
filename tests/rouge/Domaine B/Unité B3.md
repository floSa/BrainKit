---
role: unite
nom: Unité B3
apport: "La troisième unité du second domaine."
domaine: domaine-b
nature: nature-2
option_permise: "une valeur que la nature 2 ne permet pas"
---

# Unité B3

## Ce que c'est

Deux défauts sur une page, et ils ne se recouvrent pas.

**DÉFAUT 5 — le cas qui ÉCHOUE pour le sens `permet`.** `option_permise:` est
présente alors que « nature == nature-1 » est FAUX : la page est de
`nature-2`. Le champ n'existe QUE si la condition tient. Attendu : un constat DUR
de `gabarit_par_role`, section `conditionnels`.

**DÉFAUT 6 — une redirection non sourcée.** La cellule négative ci-dessous porte
une flèche et nomme une page FICHÉE sans son wikilink. Attendu : un constat
DUR de `redirection_sourcee`. La conjonction est nécessaire : la première cellule
nomme aussi une borne, mais sans flèche, donc elle n'est pas une redirection et
la règle ne la regarde pas.

## Ce qu'elle fait / Ce qu'elle ne fait pas

| Fait | Ne fait pas |
|---|---|
| Deux défauts qui ne se recouvrent pas | Le sens `permet`, dont la condition ne tient pas |
| Une redirection, en seconde cellule | Le cas nu de l'axe → Unité A1 |

## Repères

- Repère A — a
- Repère B — b
- Repère C — c
- Repère D — d

## Voir aussi

- [[Domaine B]] — le hub du domaine
