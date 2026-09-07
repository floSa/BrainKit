# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""epreuve.py — le jeu d epreuve du moteur de validation (lot 3).

    uv run tests/epreuve.py
    uv run tests/epreuve.py --vault-devbrain ../DevBrain

Six scenarios. Les quatre premiers opposent deux vaults JUMEAUX — `tests/vert/`
et `tests/rouge/` — qui ne different que par les sept defauts que le rouge porte
volontairement. Un jeu d epreuve qui n aurait qu un vault fautif prouverait
qu une regle CRIE, jamais qu elle se taise quand il faut.

  1. VERT     — le vault conforme : zero violation dure, et la NOTE qui declare
                la page ecartee de la derivation de chemin.
  2. ROUGE    — les sept defauts, chacun sur la regle attendue et sur la page
                attendue. La liste est EXACTE : un constat de plus ou de moins
                fait echouer le scenario, parce qu une regle qui deborde est
                aussi fausse qu une regle qui se taise.
  3. EXCLUSIF — le meme vault VERT, avec `axes.rangement.exclusif` retourne a
                `true` EN MEMOIRE. Les deux pages a valeurs multiples, legales
                sur un axe non exclusif, deviennent deux violations. C est la
                preuve que les deux branches de la regle existent, et qu aucune
                des deux n est le repli de l autre.
  4. PAIRE    — la declaration `reciproque: inverse` de `prolonge_par` retiree
                EN MEMOIRE. La regle qui verifie la PAIRE mord sur le manifeste,
                sans lire une page.
  5. CONTRAT  — `tests/epreuve.brain.yml` passe le schema du lot 1.
  6. DEVBRAIN — facultatif : le critere d acceptation du lot, sur le vrai vault.
                Zero violation dure, 111 avertissements, et le compte exact par
                regle. Saute si le vault n est pas la.

Les deux mutations EN MEMOIRE (scenarios 3 et 4) ne touchent aucun fichier :
elles modifient le dictionnaire charge, une cle chacune, et le disent.
"""

from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))

from brainkit.valider import valide                    # noqa: E402
from brainkit.valider.manifeste import Modele          # noqa: E402

MANIFESTE = RACINE_KIT / "tests" / "epreuve.brain.yml"
VERT = RACINE_KIT / "tests" / "vert"
ROUGE = RACINE_KIT / "tests" / "rouge"

# --------------------------------------------------------------------------- #
# Les SEPT defauts du vault rouge, un par mecanisme sous test. Chaque entree est
# (regle, cle, page) — la cle porte la section ou le sous-cas quand la regle en
# a un. La comparaison est un ENSEMBLE exact.
# --------------------------------------------------------------------------- #
ROUGE_ATTENDU = {
    # 1 — mode `reciproque: inverse` : la page qui AFFIRME la relation
    ("reciprocite", "prolonge",
     "Antiquité/Rome/Suetone - Vies des Cesars.md"),
    # 2 — axe ABSENT sur un role qui l exige
    ("gabarit_par_role", "",
     "XXe siècle/Anonyme - Note sans periode.md"),
    # 3 — PREFIXE TRANSVERSAL ignore : la page vit dans une periode qu elle traverse
    ("chemin_categorie", "",
     "XXe siècle/Kennan - Le long telegramme.md"),
    # 4 — sens `exige` : la condition tient, le champ manque
    ("gabarit_par_role", "conditionnels",
     "XXe siècle/Fonds Moscou.md"),
    # 5 — sens `permet` : le champ est la, la condition ne tient pas
    ("gabarit_par_role", "conditionnels",
     "XXe siècle/Braudel - La Mediterranee.md"),
    # 6 — redirection non sourcee vers une page fichee
    ("redirection_sourcee", "",
     "XXe siècle/Braudel - La Mediterranee.md"),
    # 7 — axe MULTIPLE : aucune valeur portee ne mene au dossier
    ("chemin_categorie", "",
     "Transversal/Histoire de France.md"),
}

# Les deux pages du vault VERT qui portent plusieurs valeurs d axe. Legales tant
# que l axe n est pas exclusif ; fautives des qu il l est.
VERT_MULTIVALUES = {
    "XXe siècle/Kennan - Le long telegramme.md",
    "Transversal/Histoire de France.md",
}

# Le critere d acceptation du lot, mesure sur les deux validateurs actuels du
# DevBrain le 2026-09-07 : `uv run AI/scripts/check_brain.py` (0 dure, 111
# avertissements) et `uv run AI/scripts/check_arbo.py` (0 ecart).
DEVBRAIN_ATTENDU = {
    ("voisinage_declare", ""): 62,
    ("collision_alias", ""): 13,
    ("couverture_des_vues", "a"): 13,
    ("couverture_des_vues", "e"): 11,
    ("etiquettes_fermees", "Ressources"): 5,
    ("anti_repetition", ""): 4,
    ("couverture_des_vues", "b"): 1,
    ("couverture_des_vues", "d"): 1,
    ("vocabulaire_ferme", "axe_vide"): 1,
}


def charge_dict() -> dict:
    with MANIFESTE.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def constats(verdict, severite: str) -> set[tuple[str, str, str]]:
    return {(c.regle, c.cle, c.page) for c in verdict.rapport.constats
            if c.severite == severite}


class Journal:
    def __init__(self) -> None:
        self.echecs: list[str] = []

    def verifie(self, nom: str, ok: bool, detail: str = "") -> None:
        print(f"  {'OK    ' if ok else 'ÉCHEC '} {nom}")
        if not ok:
            self.echecs.append(nom)
            for ligne in detail.splitlines():
                print(f"         {ligne}")


# --------------------------------------------------------------------------- #
def scenario_vert(j: Journal) -> None:
    print("\n1. VERT — le vault conforme")
    mo = Modele(charge_dict(), MANIFESTE)
    v = valide(mo, VERT)
    dures = constats(v, "dure")
    j.verifie("zéro violation dure", not dures,
              "\n".join(sorted(f"{r}/{c} — {p}" for r, c, p in dures)))
    j.verifie("aucun avertissement non plus — le vert est vert", not v.avertissements,
              "\n".join(sorted(c.rendu() for c in v.avertissements)))
    note = any("sans valeur d'axe" in n for n in v.rapport.notes)
    j.verifie("la page sans valeur d'axe est DÉCLARÉE écartée, pas tue", note,
              f"notes : {v.rapport.notes}")


def scenario_rouge(j: Journal) -> None:
    print("\n2. ROUGE — les sept défauts, exactement")
    mo = Modele(charge_dict(), MANIFESTE)
    v = valide(mo, ROUGE)
    dures = constats(v, "dure")
    manquants = ROUGE_ATTENDU - dures
    en_trop = dures - ROUGE_ATTENDU
    detail = ""
    if manquants:
        detail += "attendus et absents :\n" + "\n".join(
            sorted(f"  {r}/{c} — {p}" for r, c, p in manquants)) + "\n"
    if en_trop:
        detail += "trouvés et non attendus :\n" + "\n".join(
            sorted(f"  {r}/{c} — {p}" for r, c, p in en_trop))
    j.verifie(f"les {len(ROUGE_ATTENDU)} défauts, et eux seuls",
              dures == ROUGE_ATTENDU, detail)
    # Le defaut 2 ne doit PAS produire un second constat sur la regle de chemin :
    # une page sans valeur d axe est ecartee de la derivation, pas doublee.
    double = any(p.endswith("Anonyme - Note sans periode.md")
                 for r, _c, p in dures if r == "chemin_categorie")
    j.verifie("l'axe absent échoue sur le GABARIT, pas sur le chemin", not double)


def scenario_exclusif(j: Journal) -> None:
    print("\n3. EXCLUSIF — le même vault vert, l'axe retourné en mémoire")
    brut = charge_dict()
    brut["axes"]["rangement"]["exclusif"] = True        # LA mutation, une clé
    mo = Modele(brut, MANIFESTE)
    v = valide(mo, VERT)
    dures = constats(v, "dure")
    attendu = {("chemin_categorie", "", p) for p in VERT_MULTIVALUES}
    j.verifie("les 2 pages à valeurs multiples deviennent 2 violations",
              dures == attendu,
              "trouvé : " + "\n".join(sorted(f"{r}/{c} — {p}"
                                             for r, c, p in dures)))


def scenario_paire(j: Journal) -> None:
    print("\n4. PAIRE — la moitié de la paire inverse retirée en mémoire")
    brut = charge_dict()
    del brut["champs"]["prolonge_par"]["reciproque"]    # LA mutation, une clé
    mo = Modele(brut, MANIFESTE)
    v = valide(mo, VERT)
    n = v.rapport.compte("paire_inverse_bien_declaree", "dure")
    j.verifie("la paire mal déclarée est refusée sur le MANIFESTE seul", n == 1,
              f"{n} constat(s) au lieu de 1")
    # Elle est verifiable sans lire une page : le meme constat sort sur le vault
    # rouge, qui n a rien a voir avec la faute.
    v2 = valide(Modele(copy.deepcopy(brut), MANIFESTE), ROUGE)
    j.verifie("le même constat sort sur l'autre vault — c'est bien le manifeste",
              v2.rapport.compte("paire_inverse_bien_declaree", "dure") == 1)


def scenario_contrat(j: Journal) -> None:
    print("\n5. CONTRAT — le manifeste du jeu d'épreuve passe le schéma du lot 1")
    try:
        import jsonschema  # noqa: F401
    except ModuleNotFoundError:
        print("        (jsonschema absent — lancer `uv run schema/valider.py "
              "tests/epreuve.brain.yml`)")
        return
    sys.path.insert(0, str(RACINE_KIT / "schema"))
    import json
    import valider as v1                                # noqa: E402
    schema = json.loads((RACINE_KIT / "schema" / "brain.schema.json")
                        .read_text(encoding="utf-8"))
    viol = v1.valide(MANIFESTE, schema)
    j.verifie("schéma + les dix contraintes de cohérence", not viol,
              "\n".join(viol))


def scenario_devbrain(j: Journal, vault: Path) -> None:
    print(f"\n6. DEVBRAIN — le critère d'acceptation, sur `{vault.name}`")
    mo = Modele(yaml.safe_load(
        (RACINE_KIT / "exemples" / "devbrain.brain.yml").read_text(
            encoding="utf-8")), RACINE_KIT / "exemples" / "devbrain.brain.yml")
    v = valide(mo, vault)
    dures = constats(v, "dure")
    j.verifie("0 violation dure", not dures,
              "\n".join(sorted(f"{r}/{c} — {p}" for r, c, p in dures)))
    j.verifie("111 avertissements", len(v.avertissements) == 111,
              f"{len(v.avertissements)} au lieu de 111")
    reel = {(r, c): n for (r, c, s), n in v.rapport.compte_par_regle().items()
            if s == "avertissement"}
    ecarts = [f"{r}/{c} : {reel.get((r, c), 0)} au lieu de {n}"
              for (r, c), n in sorted(DEVBRAIN_ATTENDU.items())
              if reel.get((r, c), 0) != n]
    ecarts += [f"{r}/{c} : {n} avertissement(s) non attendu(s)"
               for (r, c), n in sorted(reel.items())
               if (r, c) not in DEVBRAIN_ATTENDU]
    j.verifie("le compte exact, RÈGLE PAR RÈGLE", not ecarts, "\n".join(ecarts))


# --------------------------------------------------------------------------- #
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(description="Le jeu d'épreuve du lot 3.")
    ap.add_argument("--vault-devbrain", type=Path,
                    default=RACINE_KIT.parent / "DevBrain")
    ns = ap.parse_args()

    print("épreuve — le moteur de validation de BrainKit, lot 3")
    j = Journal()
    scenario_vert(j)
    scenario_rouge(j)
    scenario_exclusif(j)
    scenario_paire(j)
    scenario_contrat(j)
    if ns.vault_devbrain.is_dir():
        scenario_devbrain(j, ns.vault_devbrain.resolve())
    else:
        print(f"\n6. DEVBRAIN — sauté : `{ns.vault_devbrain}` introuvable")

    print()
    if j.echecs:
        print(f"{len(j.echecs)} vérification(s) en échec :")
        for e in j.echecs:
            print(f"  - {e}")
        return 1
    print("OK — le jeu d'épreuve passe en entier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
