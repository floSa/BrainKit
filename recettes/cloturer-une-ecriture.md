# Recette — clôturer une écriture

> **Pour qui** : un agent de code lancé **dans le dossier du vault**. Système de
> fichiers, terminal, git. Aucune clé d'API.
>
> **Quand** : après **TOUTE** écriture dans une page d'un vault — une capture,
> une correction, une édition faite à la main dans Obsidian. Sans exception.
>
> **Ce que ça produit** : les artefacts dérivés régénérés, les validateurs
> verts, et un commit intégré sur la branche principale.
>
> **Critère de fin** : `generer --check` muet, `valider` sans violation dure,
> `git status` vide, et l'historique local à jour du distant.
>
> **C'est le seul endroit où la politique git d'une instance est écrite.**
> Idempotent : relançable à tout moment sans dégât.

---

## 1. Régénérer — avant de valider, pas après

```bash
uv run brainkit generer --vault <vault> --ecrire
```

L'ordre compte. Le validateur lit les zones générées ; les valider avant de les
régénérer, c'est valider ce qu'on va remplacer.

La génération tourne jusqu'à un **point fixe** : une zone AUTO porte des liens,
et la carte des liens compte les liens — une passe ne suffit pas toujours. Le
kit le fait tout seul et dit combien de passes il a fallu.

Elle peut **refuser** deux choses, et un refus n'est pas un écart :

- un hub **sans zone AUTO** — la place d'une zone ne se devine pas dans une page
  qui n'en déclare aucune ;
- une page **sans titre de niveau 1** — la place du haut de page n'y est pas
  devinable, et l'inventer casserait la page.

Un refus se répare à la main, dans la page nommée. Il ne se contourne pas.

## 2. Valider — les deux passes, au vert

```bash
uv run brainkit valider --vault <vault>
```

Ce qui doit être vrai pour continuer : **zéro violation dure**. Les
avertissements, eux, se lisent : un avertissement nouveau depuis la dernière
clôture est un signal, pas un détail.

Si une violation dure apparaît, **répare-la, ne la contourne pas** — et surtout
ne désactive pas la règle. Une règle qui gêne une écriture a plus souvent
raison que l'écriture.

Puis, pour être sûr que rien n'a bougé pendant la réparation :

```bash
uv run brainkit generer --vault <vault>        # --check : doit être muet
```

## 3. Vérifier la divergence AVANT tout commit

C'est l'étape qu'on saute, et c'est celle qui coûte le plus cher quand on la
saute.

```bash
git -C <vault> fetch origin
git -C <vault> log HEAD..origin/<branche> --oneline   # commits distants absents ici
git -C <vault> merge-base HEAD origin/<branche>       # doit rendre un ancêtre commun
```

- si `origin/<branche>` porte des commits absents en local : **arrête-toi et
  signale l'écart**. Ne commite pas sur une base obsolète ;
- si `merge-base` ne trouve **aucun** ancêtre commun — historiques divergents ou
  republiés : **arrête-toi et demande**. C'est le cas qui fait perdre du travail
  déjà écrit, et il ne se répare pas tout seul.

La branche principale est celle que le manifeste déclare
(`git.branche_principale`). Ne la devine pas.

## 4. Committer — nu, et sans rien ajouter

```bash
git -C <vault> add -A
git -C <vault> commit -m "<un message court, en français, qui dit CE QUI change>"
```

**Commite nu.** Git lit l'identité dans la config **locale** du dépôt, que le
semis y a écrite depuis le manifeste. C'est exactement ce qu'on veut.

Ce que tu ne fais **jamais**, et les trois raisons sont mécaniques :

| Interdit | Pourquoi |
|---|---|
| `-c user.email`, `--author`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_EMAIL` | l'adresse que ton harnais t'annonce t'identifie auprès d'un outil ; elle n'attribue **jamais** un commit de ce dépôt |
| un trailer `Co-Authored-By`, ou le nom d'un outil dans le message | les commits du vault sont à son propriétaire, et ça doit rester vrai |
| `--no-verify` | trois hooks versionnés (`pre-commit`, `commit-msg`, `pre-push`) font respecter les deux lignes ci-dessus. **Un hook qui refuse n'est pas un incident à contourner : c'est la règle qui fonctionne** |

Si la config locale manque ou paraît fausse : **arrête-toi et demande**. Ne la
devine pas, ne la « répare » pas avec l'adresse que tu as sous la main.

## 5. Intégrer, en fast-forward

```bash
git -C <vault> push origin <branche>
```

Si tu travaillais sur une branche de travail :

```bash
git -C <vault> switch <branche principale>
git -C <vault> merge --ff-only <branche de travail>
git -C <vault> push origin <branche principale>
```

**Jamais de `--force`, jamais de `rebase` sans accord explicite.** Un
fast-forward qui refuse veut dire que la base a bougé : retour à l'étape 3.

## 6. Ce que tu annonces

Trois choses, chiffrées, pas résumées :

- ce que la génération a écrit (combien d'artefacts, combien de passes) ;
- le verdict du validateur : violations dures, et le compte d'avertissements —
  avec l'écart depuis la dernière clôture si tu le connais ;
- le commit : son sha court, son message, et sur quelle branche il est.

Et, s'il y en a : les refus de génération que tu as réparés, et les
avertissements nouveaux que tu n'as **pas** réparés, avec la raison.
