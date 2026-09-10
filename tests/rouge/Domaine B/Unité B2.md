---
role: unite
nom: Unité B2
apport: "La deuxième unité du second domaine."
domaine: [transverse, domaine-b]
nature: nature-1
---

# Unité B2

## Ce que c'est

**DÉFAUT 3 — le cas qui ÉCHOUE pour le PRÉFIXE TRANSVERSAL.** La page porte
`transverse` ET `domaine-b`, et vit dans `Domaine B/`. Le préfixe transversal
l'emporte : le dossier attendu est `Transverse/`. Attendu : un constat DUR de
`chemin_categorie` qui nomme le préfixe et le dossier visé.

Sans cette priorité, la règle de majorité accepterait `Domaine B/` — puisque
`domaine-b` est bien une valeur portée — et le préfixe transversal ne servirait à
rien.

## Ce qu'elle fait / Ce qu'elle ne fait pas

| Fait | Ne fait pas |
|---|---|
| L'axe NON EXCLUSIF, deux valeurs portées | Le choix entre les deux, qui appartient à l'auteur |

## Repères

- Repère A — a
- Repère B — b
- Repère C — c
- Repère D — d

## Voir aussi

- [[Domaine B]] — le hub du domaine
