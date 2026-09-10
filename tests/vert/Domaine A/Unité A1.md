---
role: unite
nom: Unité A1
apport: "La première unité du premier domaine."
domaine: domaine-a
nature: nature-1
option_permise: "la valeur que la nature 1 permet"
contredit: ["[[Unité A2]]"]
---

# Unité A1

## Ce que c'est

La page porte une valeur d'axe NUE — `domaine: domaine-a`, sans sous-valeur — ce
que `valeur_courte_autorisee: true` rend légal, et qu'un axe toujours composé de
`prefixe/sous` ne rencontre jamais.

Elle porte aussi `option_permise:`, et c'est le cas qui PASSE pour le sens
`permet` : la condition « nature == nature-1 » tient, donc le champ est autorisé.

## Ce qu'elle fait / Ce qu'elle ne fait pas

| Fait | Ne fait pas |
|---|---|
| Le cas NU de l'axe de rangement | Le cas composé, qui est celui du segment |

## Repères

- Repère A — a
- Repère B — b
- Repère C — c
- Repère D — d

## Autour

### Contredit par

- [[Unité A2]] — La deuxième unité du premier domaine. Deux unités que le manifeste oppose, et rien d'autre.

## Voir aussi

- [[Domaine A]] — le hub du domaine
