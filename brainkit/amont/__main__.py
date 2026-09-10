# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""La passe de sondage de l amont, en ligne de commande.

    uv run brainkit/amont/__main__.py
    uv run brainkit/amont/__main__.py --limit 40
    uv run brainkit/amont/__main__.py --recalculer        # aucun appel reseau
    uv run brainkit/amont/__main__.py --vault <dossier> --manifeste <brain.yml>

Codes de sortie :

    0 — la passe est faite. **Y COMPRIS quand elle rapporte des amonts morts.**
        Un depot tiers archive, une release de 2019, une URL qui ne repond plus :
        ce sont des faits du monde, pas des fautes du vault. Bloquer une cloture
        dessus rendrait le brain otage de l amont — la regle vient du script
        d origine, et elle tient.
    2 — erreur d usage (vault ou manifeste introuvable), ou le manifeste ne
        declare AUCUN amont. Le second n est pas une faute : c est une commande
        sans objet sur ce brain, et le dire vaut mieux que rendre un rapport vide
        qui ressemblerait a « tout va bien ».

# Ce que cette commande n a pas, et n aura pas

Pas de `--fix`. Pas de `--token`, pas de lecture d une variable d environnement
de jeton, pas d ecriture d un jeton ou que ce soit. Pas d ecriture dans une
page : la seule sortie est le side-car declare par `amont.side_car`, et
`--rapport` si on le demande.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

RACINE_KIT = Path(__file__).resolve().parents[2]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit import defauts                            # noqa: E402
from brainkit.amont import sidecar                      # noqa: E402
from brainkit.amont.etat import ETATS                   # noqa: E402
from brainkit.amont.passe import Rapport, passe         # noqa: E402
from brainkit.valider import charge                     # noqa: E402

LIBELLE = {
    "recente": "amont vivant, dans le seuil",
    "ancienne": "amont au-delà du seuil",
    "archive": "dépôt archivé",
    "sans_amont": "aucun amont atteignable",
    "jamais_sonde": "jamais sondée",
}


def texte(rap: Rapport, amont, ecrit: Path | None, detail: int) -> list[str]:
    L = [f"sonder — {rap.pages} page(s) du/des rôle(s) "
         f"{', '.join(amont.porte_par) or '(aucun)'} · "
         f"{rap.sondees} sondée(s) sur cette passe · "
         f"{rap.fraiches} déjà fraîche(s), {rap.hors_limite} laissée(s) à la "
         f"passe suivante",
         f"  {rap.requetes} requête(s) HTTP anonyme(s), aucun jeton — sondes : "
         f"{', '.join(amont.sondes_utilisees) or '(aucune)'}",
         f"  seuils : release {amont.seuil('release_ancienne_jours')} j · "
         f"commit {amont.seuil('commit_ancien_jours')} j"
         + ("" if rap.seuil_declare
            else "   ← DÉFAUT DU KIT : le manifeste ne les déclare pas"),
         ""]
    L.append("état des pages :")
    for e in ETATS:
        L.append(f"  {e:14s} {rap.par_etat.get(e, 0):5d}   {LIBELLE[e]}")
    L += ["",
          f"faits datés : {rap.avec_release} release(s) de dépôt · "
          f"{rap.avec_registre} version(s) de registre · "
          f"{rap.avec_commit_seul} page(s) datée(s) par leur seul dernier commit"]

    if rap.sans_cible:
        L.append(f"\n{len(rap.sans_cible)} page(s) sans aucune cible à sonder — "
                 f"ni URL d'amont, ni nom de registre :")
        for c in rap.sans_cible[:detail]:
            L.append(f"  - {c}")
        if len(rap.sans_cible) > detail:
            L.append(f"  … {len(rap.sans_cible) - detail} autre(s)")
    if rap.archivage_inconnu:
        L.append(f"\n{len(rap.archivage_inconnu)} page(s) dont l'archivage n'a "
                 f"PAS pu être lu (marqueur non atteint sous le plafond) :")
        for c in rap.archivage_inconnu[:detail]:
            L.append(f"  - {c}")
    if rap.sous_arbres:
        L.append(f"\n{len(rap.sous_arbres)} URL vise(nt) un SOUS-ARBRE : les "
                 f"dates décrivent le dépôt entier, pas le sous-arbre.")
        for c in rap.sous_arbres[:detail]:
            L.append(f"  - {c}")
    if rap.orphelines:
        L.append(f"\n{len(rap.orphelines)} entrée(s) du side-car ne visent plus "
                 f"aucune page — page renommée, déplacée ou supprimée :")
        for c in rap.orphelines[:detail]:
            L.append(f"  - {c}")

    if rap.lignes:
        L.append(f"\n{len(rap.lignes)} page(s) dont l'amont est archivé ou "
                 f"au-delà du seuil :")
        L.append(f"  {'page':<58} {'état':<10} date")
        for chemin, e, d in sorted(rap.lignes, key=lambda x: (x[1], x[2] or "")):
            L.append(f"  {chemin[:57]:<58} {e:<10} {d or '—'}")
    if ecrit is not None:
        L.append(f"\nside-car écrit : {ecrit}")
    L.append("Rapport seul : aucune page n'a été touchée, rien n'a été corrigé.")
    return L


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(
        description="Sonde l'amont des unités d'un brain et date sa fraîcheur.")
    ap.add_argument("--manifeste", type=Path, default=None,
                    help="défaut : le `brain.yml` du vault visé")
    ap.add_argument("--vault", type=Path, default=None,
                    help="défaut : le dossier courant s'il porte un `brain.yml`")
    ap.add_argument("--limit", type=int, default=None,
                    help="nombre maximum de pages sondées sur cette passe")
    ap.add_argument("--age-max-jours", type=int, default=7,
                    help="reprise : ne pas re-sonder une page sondée depuis moins "
                         "de N jours")
    ap.add_argument("--recalculer", action="store_true",
                    help="rejoue la dérivation des états sur les faits déjà "
                         "sondés, SANS aucun appel réseau")
    ap.add_argument("--pause", type=float, default=0.0,
                    help="secondes d'attente entre deux pages sondées")
    ap.add_argument("--detail", type=int, default=12,
                    help="nombre d'entrées détaillées par liste")
    ap.add_argument("--rapport", type=Path, default=None,
                    help="dépose le rapport en texte à ce chemin")
    ns = ap.parse_args()

    vault = ns.vault if ns.vault is not None else defauts.vault_par_defaut()
    if not vault.is_dir():
        print(f"vault introuvable : {vault}")
        return 2
    manifeste, dits = defauts.resout(ns.manifeste, vault)
    for ligne in dits:
        print(ligne)
    if manifeste is None:
        return 2
    if not manifeste.exists():
        print(f"manifeste introuvable : {manifeste}")
        return 2
    if dits:
        print()

    mo = charge(manifeste)
    racine = vault.resolve()
    contenu, rap, amont = passe(mo, racine, limite=ns.limit,
                                age_max=ns.age_max_jours,
                                recalculer=ns.recalculer, pause=ns.pause)
    if not amont.declare:
        print(f"`{manifeste.name}` ne déclare aucun bloc `amont:` — ce brain n'a "
              f"pas d'amont à sonder.")
        print("    Ce n'est pas une faute : toutes les unités n'ont pas un "
              "amont qui vit. Sans ce bloc, le kit ne sonde rien, ne signale "
              "rien et n'affiche aucune colonne de fraîcheur.")
        return 2

    ecrit = sidecar.ecrit_side_car(amont, racine, contenu) if contenu else None
    lignes = texte(rap, amont, ecrit.relative_to(racine) if ecrit else None,
                   ns.detail)
    for ligne in lignes:
        print(ligne)
    if ns.rapport:
        ns.rapport.parent.mkdir(parents=True, exist_ok=True)
        ns.rapport.write_text("\n".join(lignes) + "\n", encoding="utf-8")
        print(f"\nrapport écrit : {ns.rapport}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
