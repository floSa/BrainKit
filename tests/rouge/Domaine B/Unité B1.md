---
role: unite
nom: Unité B1
apport: "La première unité du second domaine."
domaine: domaine-b
nature: nature-3
---

# Unité B1

## Ce que c'est

**DÉFAUT 4 — le cas qui ÉCHOUE pour le sens `exige`.** La condition
« nature == nature-3 » tient, et `option_exigee:` est ABSENTE. Attendu : un
constat DUR de `gabarit_par_role`, section `conditionnels`.

C'est le sens que le contrat n'exprimait pas avant ce lot : `requis` est
inconditionnel, `conditionnels[]` ne faisait que PERMETTRE. Une obligation
conditionnelle n'avait aucun endroit où s'écrire.

## Ce qu'elle fait / Ce qu'elle ne fait pas

| Fait | Ne fait pas |
|---|---|
| Le sens `exige` d'un champ conditionnel | Le sens `permet`, qui est celui de l'unité A1 |

## Repères

- Repère A — a
- Repère B — b
- Repère C — c
- Repère D — d

## Voir aussi

- [[Domaine B]] — le hub du domaine
