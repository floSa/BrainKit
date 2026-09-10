# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml>=6"]
# ///
"""emballage.py — le jeu d epreuve de L EMBALLAGE (lot 10).

    uv run tests/emballage.py
    uv run tests/emballage.py --vault-temoin <chemin d un vault reel>

Huit scenarios. Aucun n ecrit hors d un dossier temporaire, et le scenario 8 lit
un vault reel SANS l ouvrir en ecriture.

  1. DOCUMENTS   — les documents du depot concordent avec ce que le kit genere
                   (`outils/emballer.py --check` en code 0), la generation est
                   IDEMPOTENTE, et ce qui est interdit dans un document est
                   absent : aucun wikilink (il elargirait l atteignabilite d un
                   vault), aucune promesse commerciale.
  2. GENERICITE  — deux brains sans rien de commun, et le CONTROLE qui compte :
                   aucun mot de sujet du premier dans les documents du second.
                   Une phrase identique sur deux brains differents serait la
                   preuve qu elle est recopiee.
  3. PROFIL NU   — un brain semé en `profil: nu` est VERT aux deux validateurs,
                   et ce qu il perd est MESURE, fichier par fichier, contre le
                   meme brain en `profil: obsidian`.
  4. CROISE      — le test croise de §5.1 : la MEME instance, validee par le kit
                   BRANCHE puis par le kit FIGE. Meme verdict, a l octet.
  5. PONTS       — les huit cibles de `agent.ponts` sont posees, chacune TOURNE
                   pour de vrai, et une cible inventee est REFUSEE avant que le
                   semis ecrive un octet.
  6. VERSION     — `kit.version` et `manifeste:` sont enfin compares, DANS LES
                   DEUX SENS. Le cas negatif compte autant que le positif : un
                   mineur different refuse, un correctif different se DIT.
  7. DEFAUT      — lancees DANS un vault, `valider` et `generer` resolvent
                   `./brain.yml` sans option (remontee 3 du lot 5, close au
                   lot 6 — ce scenario le verifie plutot que de le croire).
  8. TEMOIN      — sur un vault reel, en lecture seule : les documents que le
                   kit genererait pour lui sont composables et ne contiennent
                   aucune valeur inventee. Saute si le vault n est pas la.
"""

from __future__ import annotations

import argparse
import copy
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

RACINE_KIT = Path(__file__).resolve().parents[1]
if str(RACINE_KIT) not in sys.path:
    sys.path.insert(0, str(RACINE_KIT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import temoin                                          # noqa: E402

from brainkit import contrat, emballer                             # noqa: E402
from brainkit.entretien import brouillon as _brouillon             # noqa: E402
from brainkit.entretien import composer                            # noqa: E402
from brainkit.generer import genere_tout                           # noqa: E402
from brainkit.generer.sortie import CHECK                          # noqa: E402
from brainkit.semer import figer, ponts, semis                     # noqa: E402
from brainkit.valider import valide                                # noqa: E402
from brainkit.valider.manifeste import Modele                      # noqa: E402

REFERENCE = RACINE_KIT / "gabarit" / "brain.yml"
REPONSES_DEUX = RACINE_KIT / "tests" / "deuxieme.reponses.yml"
REPONSES_TROIS = RACINE_KIT / "tests" / "troisieme.reponses.yml"

# Les mots de SUJET de chaque brain — repris du controle du lot 7, meme motif :
# les jetons portent leur ponctuation, parce qu un controle de genericite qui
# teste des mots courants mesure la langue et non la derivation.
MOTS_REF = ["role: unite", "role: sequence", "domaine", "Marqueur 1",
            "prolonge_par", "contredit:", "fiabilite", "BrainRef"]
MOTS_TROIS = ["role: jalon", "role: liste", "Moment 1", "BrainTrois",
              "conditionne_par", "va_avec:", "enjeu", "Partie 1"]

# Ce qu un document du depot ne doit JAMAIS porter. §5.7 et §5.8 du cadrage ne
# sont pas tranches, et un depot qui les trancherait a la place de son
# proprietaire trancherait mal.
#
# Les motifs sont des EXPRESSIONS A FRONTIERE DE MOT, et le premier jet ne
# l etait pas : « coffre » contient « offre », et le jeu d essai a signale onze
# fausses promesses commerciales dans un guide d installation d Obsidian. La
# lecon est celle du lot 7 — un controle qui teste des sous-chaines de mots
# courants mesure la langue, pas ce qu on veut controler.
#
# « prix » est sorti de la liste pour la meme raison, mais a l envers : il a un
# emploi legitime et frequent (« c est le prix, pas un defaut ») et aucun emploi
# commercial qui ne soit deja pris par un autre motif. Un motif qui ne peut que
# faire du bruit ne se garde pas.
INTERDITS_COMMERCIAUX = [
    r"\d\s*(?:€|EUR\b)", r"[$£]\s*\d", r"\btarifs?\b", r"\bfacturation\b",
    r"\bdevis\b", r"\babonnement\b", r"\bhonoraires\b", r"\bTJM\b",
    r"\bprestation\b", r"\boffre\b", r"\bà vendre\b", r"\bnos clients\b",
    r"\blicence commerciale\b",
]
# Les emplois LEGITIMES, dans un texte qui parle de licence et de livraison.
TOLERES = [
    "permissive, copyleft, commerciale, double",   # LICENSE : les issues, listees
    "commerciale, ou separer",
]

# Les huit cibles de pont, et comment on les EXERCE. `None` = une bibliotheque,
# elle s importe au lieu de se lancer.
PONTS_A_EXERCER = {
    "check_brain": "valider", "check_arbo": "structure",
    "build_index": "index", "build_mocs": "hubs", "build_links": "liens",
    "build_bandeau": "bandeau", "build_tout": "generer", "arbo": "chemins",
}

BRUIT_UV = ("warning:", "         If ", "Installed ", "Using ", "Resolved ",
            "Prepared ", "Audited ", "Built ", "Building ", " + ")


class Journal:
    def __init__(self) -> None:
        self.echecs: list[str] = []

    def verifie(self, nom: str, ok: bool, detail: str = "") -> None:
        print(f"  {'OK    ' if ok else 'ÉCHEC '} {nom}")
        if not ok:
            self.echecs.append(nom)
            for ligne in str(detail).splitlines()[:12]:
                print(f"         {ligne}")


def charge_dict(chemin: Path) -> dict:
    with chemin.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def compose(reponses: Path, dossier: Path) -> Modele:
    """Un manifeste RECOMPOSE depuis des reponses d entretien. Jamais copie."""
    lot = (charge_dict(reponses) or {}).get("reponses") or {}
    b = _brouillon.charge(dossier / "entretien.yml")
    for qid, val in lot.items():
        b.repond(str(qid), val)
    m, griefs = composer.compose(b)
    if m is None:
        raise SystemExit(f"{reponses.name} ne se compose pas : "
                         + " · ".join(griefs))
    return Modele(m, dossier / "brain.yml")


def _lance(cwd: Path, *args: str, env: dict | None = None) -> tuple[int, list[str]]:
    """Lance une commande et rend (code, lignes SANS le bruit de `uv`)."""
    import os
    plein = {**os.environ, **(env or {})}
    p = subprocess.run(args, cwd=str(cwd), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=plein)
    lignes = [l for l in (p.stdout + p.stderr).splitlines()
              if not l.startswith(BRUIT_UV)]
    return p.returncode, lignes


# --------------------------------------------------------------------------- #
def scenario_documents(j: Journal) -> None:
    print("\n1. DOCUMENTS — le dépôt concorde avec ce que le kit génère")
    outil = RACINE_KIT / "outils" / "emballer.py"
    code, lignes = _lance(RACINE_KIT, sys.executable, str(outil))
    j.verifie("`outils/emballer.py` (mode `--check`) sort en 0",
              code == 0, "\n".join(lignes[-8:]))

    # Idempotence : deux rendus du meme manifeste sont identiques a l octet.
    # Sans ca, `--check` signalerait un ecart a chaque appel et le contrat
    # « ce qui est genere n est jamais edite a la main » serait invérifiable.
    mo = Modele(charge_dict(REFERENCE), REFERENCE)
    a, b = emballer.rendus(mo), emballer.rendus(mo)
    j.verifie("la génération est idempotente (deux rendus identiques)", a == b,
              "\n".join(sorted(set(a) ^ set(b))))
    # AUCUN wikilink dans un document. Le validateur lit tout `.md` de la
    # racine du vault comme une SOURCE d atteignabilite : un `[[hub]]` dans
    # `INSTALL.md` rendrait un hub atteignable sans que la porte d entree le
    # cite, donc elargirait une regle en silence.
    for chemin, texte in a.items():
        if "/" in chemin:
            continue        # `docs/` est dans `genere.non_pages` : inerte
        liens = re.findall(r"\[\[[^\]]+\]\]", texte)
        j.verifie(f"aucun wikilink dans `{chemin}` (lu par `page_atteignable`)",
                  not liens, str(liens[:5]))

    # Aucune promesse commerciale, nulle part dans le depot documente.
    #
    # Les motifs de `INTERDITS_COMMERCIAUX` portaient, jusqu au lot 12, des
    # octets 0x08 (un retour arriere) la ou le code voulait des `\b` de
    # frontiere de mot — sequelle d une ecriture par document interstitiel de
    # shell. Aucun motif ne pouvait donc correspondre : le controle passait au
    # vert sur n importe quel texte. Corrige, et la liste des cibles a grandi
    # dans le meme geste.
    fautes: list[str] = []
    cibles = ["README.md", "LICENSE"]
    cibles += [f"docs/{p.name}" for p in (RACINE_KIT / "docs").glob("*.md")]
    cibles += [f"gabarit/rendu/{p.name}"
               for p in (RACINE_KIT / "gabarit" / "rendu").glob("*.md")]
    for chemin in cibles:
        for ligne in (RACINE_KIT / chemin).read_text(
                encoding="utf-8").splitlines():
            if any(tol in ligne for tol in TOLERES):
                continue
            for motif in INTERDITS_COMMERCIAUX:
                if re.search(motif, ligne, re.IGNORECASE):
                    fautes.append(f"{chemin} : /{motif}/ — {ligne.strip()[:90]}")
    j.verifie("aucune promesse commerciale dans les documents du dépôt",
              not fautes, "\n".join(fautes))

    # Le manifeste d images DECLARE et n embarque rien — dans un document
    # GENERE. La nuance a compte au lot 12 : la doc DU KIT, elle, est ecrite a
    # la main et porte ses captures. Le contrat « aucun appel d image en dur »
    # ne vaut que la ou le fichier n existe pas encore a la generation, c est-a
    # dire dans les documents qu une instance recoit.
    from brainkit.emballer import images
    j.verifie(f"{len(images.CAPTURES)} captures déclarées par le manifeste "
              f"d'instance", len(images.CAPTURES) > 0)
    for chemin, texte in a.items():
        if "![" in texte:
            j.verifie(f"aucun appel d'image en dur dans `{chemin}`", False,
                      "une image absente s'afficherait cassée")
    j.verifie("aucun appel d'image en dur dans un document GÉNÉRÉ",
              not any("![" in t for t in a.values()))

    # Et le controle des images de la doc du kit, dans les deux sens. Il ferme
    # la remontee 8 de ce lot : une capture declaree qui manque, un fichier pose
    # que personne ne declare.
    code, lignes = _lance(RACINE_KIT, sys.executable,
                          str(RACINE_KIT / "outils" / "captures.py"))
    j.verifie("`outils/captures.py` sort en 0 — aucune image manquante, "
              "aucune orpheline", code == 0, "\n".join(lignes[-10:]))


# --------------------------------------------------------------------------- #
def scenario_genericite(j: Journal, dossier: Path) -> None:
    print("\n2. GÉNÉRICITÉ — aucun mot de sujet ne traverse d'un brain à l'autre")
    ref = Modele(charge_dict(REFERENCE), REFERENCE)
    trois = compose(REPONSES_TROIS, dossier / "compose-trois")
    (dossier / "compose-trois").mkdir(parents=True, exist_ok=True)

    doc_h = emballer.rendus(ref)
    doc_b = emballer.rendus(trois)
    j.verifie("les deux brains produisent les mêmes CHEMINS de document",
              set(doc_h) == set(doc_b), str(set(doc_h) ^ set(doc_b)))

    for mots, cible, nom in ((MOTS_REF, doc_b, "BrainRef -> BrainTrois"),
                             (MOTS_TROIS, doc_h, "BrainTrois -> BrainRef")):
        fuites = [f"{c} : « {m} »" for m in mots
                  for c, t in cible.items() if m in t]
        j.verifie(f"aucune fuite {nom}", not fuites, "\n".join(fuites))

    # Et le controle inverse, qui prouve que le test n est pas vide : chaque
    # brain porte SES mots dans SES documents. Un jeu d essai qui ne verifie
    # que l absence passerait sur deux documents vides.
    for mots, cible, nom in ((MOTS_REF, doc_h, "BrainRef"),
                             (MOTS_TROIS, doc_b, "BrainTrois")):
        presents = [m for m in mots if any(m in t for t in cible.values())]
        j.verifie(f"… et {nom} porte bien ses propres mots ({len(presents)}"
                  f"/{len(mots)})", len(presents) >= len(mots) // 2,
                  f"trouvés : {presents}")


# --------------------------------------------------------------------------- #
def scenario_profil_nu(j: Journal, dossier: Path) -> None:
    print("\n3. PROFIL NU — un brain sans Obsidian, et ce qu'il perd, mesuré")
    base = charge_dict(REFERENCE)
    nu = copy.deepcopy(base)
    nu["brain"]["profil"] = "nu"
    nu["brain"]["nom"] = base["brain"]["nom"]

    mo_o = Modele(base, REFERENCE)
    mo_n = Modele(nu, REFERENCE)
    a = semis.seme(mo_o, dossier / "prof-obsidian", ecrire=True, avec_git=False)
    b = semis.seme(mo_n, dossier / "prof-nu", ecrire=True, avec_git=False)
    j.verifie("le semis `nu` ne refuse rien", not b.refuse,
              "\n".join(b.manques + b.plan.refus))
    if a.refuse or b.refuse:
        return

    v = valide(mo_n, dossier / "prof-nu")
    g = genere_tout(mo_n, dossier / "prof-nu", mode=CHECK)
    j.verifie("`nu` : 0 violation DURE", not v.dures,
              "\n".join(c.rendu() for c in v.dures))
    j.verifie("`nu` : 0 avertissement, 0 à mesurer",
              not v.avertissements and not v.a_mesurer,
              "\n".join(c.rendu() for c in (v.avertissements + v.a_mesurer)))
    j.verifie("`nu` : les générateurs concordent", not g.ecarts() and not g.refus,
              f"{len(g.ecarts())} écart(s)")

    fo = {f.chemin for f in a.plan.fichiers}
    fn = {f.chemin for f in b.plan.fichiers}
    perdus, gagnes = sorted(fo - fn), sorted(fn - fo)
    print(f"       `nu` perd {len(perdus)} fichier(s) : "
          + (", ".join(perdus) or "aucun"))
    j.verifie("`nu` perd la table de couleurs du graphe, et RIEN d'autre",
              perdus == ["Documentation/graphe.md"], str(perdus))
    j.verifie("… et il ne gagne aucun fichier", not gagnes, str(gagnes))

    # Le BANDEAU survit — c est le point de §5.5 : ce qui est perdu est la vue
    # filtree, pas la fiche.
    gab_o = (dossier / "prof-obsidian" / "Templates").glob("*.md")
    bandeaux = [p.name for p in gab_o
                if "AUTO:BANDEAU" in p.read_text(encoding="utf-8")]
    gab_n = [p.name for p in (dossier / "prof-nu" / "Templates").glob("*.md")
             if "AUTO:BANDEAU" in p.read_text(encoding="utf-8")]
    j.verifie(f"le haut de page survit au profil `nu` ({len(gab_n)} gabarit(s))",
              sorted(bandeaux) == sorted(gab_n), f"{bandeaux} vs {gab_n}")

    # Ce qui CHANGE dans les gabarits : le jeton de Templater, et l embed de vue.
    textes_o = {p.name: p.read_text(encoding="utf-8")
                for p in (dossier / "prof-obsidian" / "Templates").glob("*.md")}
    textes_n = {p.name: p.read_text(encoding="utf-8")
                for p in (dossier / "prof-nu" / "Templates").glob("*.md")}
    j.verifie("aucun jeton Templater dans un gabarit `nu`",
              not any("<% tp." in t for t in textes_n.values())
              and any("<% tp." in t for t in textes_o.values()),
              "le jeton est resté, ou il n'était pas là en `obsidian`")
    ext = mo_o.extension_de_vue() or ".base"
    j.verifie(f"aucun lien d'embed `{ext}` dans un gabarit `nu`",
              not any(f"{ext}]]" in t for t in textes_n.values())
              and any(f"{ext}]]" in t for t in textes_o.values()))

    # Et ce que le document DIT du profil concorde avec ce que le semis fait.
    doc = emballer.rendus(mo_n)["INSTALL.md"]
    j.verifie("l'`INSTALL.md` d'un brain `nu` ne demande aucun plugin",
              "Templater" not in doc and "File Hider" not in doc,
              "un plugin est demandé à un brain qui n'ouvre pas Obsidian")
    j.verifie("… et il dit qu'il est en profil `nu`", "profil `nu`" in doc)


# --------------------------------------------------------------------------- #
def scenario_croise(j: Journal, dossier: Path) -> None:
    print("\n4. CROISÉ — la même instance, kit BRANCHÉ puis kit FIGÉ")
    mo = Modele(charge_dict(REFERENCE), REFERENCE)
    cible = dossier / "croise"
    s = semis.seme(mo, cible, ecrire=True, avec_git=False)
    if s.refuse:
        j.verifie("le semis de l'instance croisée", False,
                  "\n".join(s.manques + s.plan.refus))
        return

    lanceur_v = str(RACINE_KIT / "brainkit" / "valider" / "__main__.py")
    lanceur_g = str(RACINE_KIT / "brainkit" / "generer" / "__main__.py")
    code_bv, br_v = _lance(cible, sys.executable, lanceur_v,
                           "--vault", str(cible), "--manifeste",
                           str(cible / "brain.yml"))
    code_bg, br_g = _lance(cible, sys.executable, lanceur_g,
                           "--vault", str(cible), "--manifeste",
                           str(cible / "brain.yml"))

    f = figer.fige(mo, cible, ecrire=True)
    j.verifie("`freeze` s'applique", f.applique and not f.refus, str(f.refus))
    j.verifie("`kit.mode` est passé à `fige`",
              "mode: fige" in (cible / "brain.yml").read_text(encoding="utf-8"))

    code_fv, fi_v = _lance(cible, sys.executable,
                           str(cible / "AI" / "scripts" / "valider.py"))
    code_fg, fi_g = _lance(cible, sys.executable,
                           str(cible / "AI" / "scripts" / "generer.py"))

    def sans_entete(lignes: list[str]) -> list[str]:
        # L en-tete nomme le manifeste et le vault : ce sont des CHEMINS, pas
        # un verdict. Tout le reste se compare a l octet.
        return [l for l in lignes
                if not l.startswith(("valider :", "générer", "generer"))]

    j.verifie(f"validation : même code de sortie ({code_bv} / {code_fv})",
              code_bv == code_fv)
    j.verifie("validation : même verdict, ligne pour ligne",
              sans_entete(br_v) == sans_entete(fi_v),
              "\n".join(f"branché: {a}\nfigé   : {b}"
                        for a, b in zip(sans_entete(br_v), sans_entete(fi_v))
                        if a != b))
    j.verifie(f"génération : même code de sortie ({code_bg} / {code_fg})",
              code_bg == code_fg)
    j.verifie("génération : même rapport, ligne pour ligne",
              sans_entete(br_g) == sans_entete(fi_g),
              "\n".join(f"branché: {a}\nfigé   : {b}"
                        for a, b in zip(sans_entete(br_g), sans_entete(fi_g))
                        if a != b))
    print(f"       branché : code {code_bv} · {len(sans_entete(br_v))} lignes "
          f"de verdict  |  figé : code {code_fv} · "
          f"{len(sans_entete(fi_v))} lignes")


# --------------------------------------------------------------------------- #
def scenario_ponts(j: Journal, dossier: Path) -> None:
    print("\n5. PONTS — la couche d'adaptation, posée et EXERCÉE")
    base = charge_dict(REFERENCE)
    avec = copy.deepcopy(base)
    avec["agent"]["ponts"] = dict(PONTS_A_EXERCER)
    mo = Modele(avec, REFERENCE)
    cible = dossier / "ponts"
    s = semis.seme(mo, cible, ecrire=True, avec_git=False)
    j.verifie("le semis avec ponts ne refuse rien", not s.refuse,
              "\n".join(s.manques + s.plan.refus))
    if s.refuse:
        return

    scripts = cible / "AI" / "scripts"
    poses = {p.name for p in scripts.glob("*.py")}
    attendus = {f"{n}.py" for n in PONTS_A_EXERCER} | {ponts.RESOLVEUR}
    j.verifie(f"les {len(attendus)} fichiers de la couche sont posés",
              poses == attendus, str(sorted(poses ^ attendus)))

    # `$BRAINKIT_RACINE` est la PREMIERE piste du resolveur, et c est celle
    # qu un jeu d epreuve doit employer : les deux autres dependent de l endroit
    # ou le dossier temporaire a ete cree.
    env = {"BRAINKIT_RACINE": str(RACINE_KIT)}
    for nom, cible_pont in sorted(PONTS_A_EXERCER.items()):
        if cible_pont == "chemins":
            continue                    # une bibliothèque : elle s'importe
        code, lignes = _lance(cible, sys.executable, str(scripts / f"{nom}.py"),
                              env=env)
        j.verifie(f"`{nom}.py` tourne (cible `{cible_pont}`) — code {code}",
                  code == 0, "\n".join(lignes[-6:]))

    # La bibliotheque s IMPORTE, et son API est celle que le lot 9 avait dû
    # adapter a la main : `promotions()` sur des VALEURS d axe.
    code, lignes = _lance(
        cible, sys.executable, "-c",
        "import sys; sys.path.insert(0, r'%s')\n"
        "import arbo\n"
        "assert arbo.SEUIL == %d, arbo.SEUIL\n"
        "p = arbo.promotions(['%s'] * 3)\n"
        "print('SEUIL', arbo.SEUIL, 'promus', p, 'tete',"
        " arbo.tete('%s'))\n"
        % (scripts, mo.seuil, next(iter(mo.sous_valeurs)),
           next(iter(mo.sous_valeurs))), env=env)
    j.verifie("`arbo.py` s'importe et expose l'API du lot 9", code == 0,
              "\n".join(lignes[-6:]))

    # Le CAS NEGATIF : une cible inventee est refusee AVANT toute ecriture.
    faux = copy.deepcopy(base)
    faux["agent"]["ponts"] = {"check_brain": "faire-le-cafe"}
    perdu = dossier / "ponts-refuses"
    s2 = semis.seme(Modele(faux, REFERENCE), perdu, ecrire=True, avec_git=False)
    j.verifie("une cible de pont inventée est REFUSÉE", bool(s2.manques),
              "aucun manque signalé")
    j.verifie("… et rien n'est écrit", not perdu.exists(),
              f"`{perdu}` a été créé")
    j.verifie("… et le refus NOMME les cibles connues",
              any("faire-le-cafe" in m and "valider" in m for m in s2.manques),
              str(s2.manques))


# --------------------------------------------------------------------------- #
def scenario_version(j: Journal) -> None:
    print("\n6. VERSION — comparée DANS LES DEUX SENS, cas négatif compris")
    from brainkit import __version__
    pyproject = (RACINE_KIT / "pyproject.toml").read_text(encoding="utf-8")
    j.verifie("`pyproject.toml` LIT la version, il ne la recopie pas",
              'dynamic = ["version"]' in pyproject
              and 'path = "brainkit/__init__.py"' in pyproject,
              "deux sources pour une version, c'est le constat E4")

    base = charge_dict(REFERENCE)
    majeur, mineur, correctif = (int(x) for x in __version__.split("."))

    cas = [
        ("le manifeste courant passe en silence", base, False, 0),
        ("`manifeste:` absent — REFUS",
         {**base, "manifeste": None}, True, 1),
        ("`manifeste:` d'une autre génération — REFUS",
         {**base, "manifeste": 2}, True, 1),
        ("`kit.version` d'un mineur plus RÉCENT — REFUS",
         {**base, "kit": {"version": f"{majeur}.{mineur + 1}.0",
                          "mode": "branche"}}, True, 1),
        ("`kit.version` d'un mineur plus ANCIEN — REFUS",
         {**base, "kit": {"version": f"{majeur}.{max(0, mineur - 1)}.0",
                          "mode": "branche"}}, mineur > 0, 1),
        ("`kit.version` d'un autre CORRECTIF — dit, pas refusé",
         {**base, "kit": {"version": f"{majeur}.{mineur}.{correctif + 1}",
                          "mode": "branche"}}, False, 1),
        ("bloc `kit:` absent — RIEN à dire (il est facultatif)",
         {k: v for k, v in base.items() if k != "kit"}, False, 0),
    ]
    for nom, m, refuse_attendu, dits_min in cas:
        dits, refuse = contrat.controle(m)
        ok = refuse == refuse_attendu and len(dits) >= (dits_min if refuse_attendu or dits_min == 0 else 1)
        j.verifie(nom, ok, f"refuse={refuse} (attendu {refuse_attendu}) ; "
                           f"dits={dits}")
    # Un refus doit NOMMER les deux versions : un message qui dit « non » sans
    # dire lesquelles laisse le lecteur sans issue.
    dits, _ = contrat.controle({**base, "kit": {"version": f"{majeur}.{mineur + 1}.0",
                                                "mode": "branche"}})
    j.verifie("le refus nomme les DEUX versions",
              any(f"{majeur}.{mineur + 1}.0" in d for d in dits)
              and any(__version__ in d for d in dits), str(dits))
    # Et il tourne dans le VRAI chemin de chargement, pas seulement en unitaire.
    j.verifie("le contrôle est branché sur `charge()`, l'entonnoir unique",
              "contrat" in (RACINE_KIT / "brainkit" / "valider" /
                            "manifeste.py").read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- #
def scenario_defaut(j: Journal, dossier: Path) -> None:
    print("\n7. DÉFAUT D'INSTANCE — `valider` et `generer` lancés DANS le vault")
    mo = Modele(charge_dict(REFERENCE), REFERENCE)
    cible = dossier / "defaut"
    s = semis.seme(mo, cible, ecrire=True, avec_git=False)
    if s.refuse:
        j.verifie("le semis de l'instance de contrôle", False, str(s.manques))
        return
    for nom, module in (("valider", "brainkit/valider/__main__.py"),
                        ("generer", "brainkit/generer/__main__.py")):
        code, lignes = _lance(cible, sys.executable, str(RACINE_KIT / module))
        j.verifie(f"`{nom}` sans aucune option — code {code}", code == 0,
                  "\n".join(lignes[-6:]))
        j.verifie(f"… et il a pris LE manifeste du vault",
                  any("brain.yml" in l for l in lignes)
                  and not any("gabarit/brain.yml" in l for l in lignes),
                  "\n".join(lignes[:4]))


# --------------------------------------------------------------------------- #
def scenario_temoin(j: Journal, vault: Path) -> None:
    print("\n8. TÉMOIN — les documents du vault réel, composés en LECTURE SEULE")
    manifeste = vault / "brain.yml"
    mo = Modele(charge_dict(manifeste), manifeste)
    docs = emballer.rendus(mo)
    j.verifie(f"{len(docs)} documents composés depuis le manifeste réel",
              len(docs) == 4, str(sorted(docs)))
    # Aucun trou de gabarit non rempli : un `{quelque_chose}` reste veut dire
    # qu un gabarit de prose attend une valeur que le manifeste ne donne pas.
    trous = [f"{c} : {t}" for c, texte in docs.items()
             for t in re.findall(r"\{[a-z_]+\}", texte)]
    j.verifie("aucun trou de gabarit non rempli", not trous,
              "\n".join(trous[:8]))
    # Et la composition est PURE : elle lit le manifeste, elle n ecrit pas un
    # octet dans le vault. Ce qui est controle ici est le KIT, pas l arbre de
    # travail du proprietaire du vault — celui-la bouge quand il travaille, et
    # un jeu d epreuve qui echouerait pour ca mesurerait la mauvaise chose.
    avant = {p.name for p in vault.glob("*")}
    emballer.rendus(mo)
    apres = {p.name for p in vault.glob("*")}
    j.verifie("composer les documents n'écrit RIEN dans le vault lu",
              avant == apres, str(sorted(apres - avant)))
    p = subprocess.run(["git", "-C", str(vault), "status", "--porcelain"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    if p.stdout.strip():
        print("       note — l'arbre de travail du vault n'est pas propre. Ce "
              "n'est pas un verdict du kit : c'est l'état du dépôt de son "
              "propriétaire, et il bouge quand il travaille.")
        for ligne in p.stdout.strip().splitlines()[:6]:
            print(f"         {ligne}")


# --------------------------------------------------------------------------- #
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):        # pragma: no cover
        pass
    ap = argparse.ArgumentParser(description="Le jeu d'épreuve de l'emballage.")
    ap.add_argument("--vault-temoin", type=Path, default=None,
                    help="un vault réel ; cf. tests/temoin.py")
    ap.add_argument("--garder", action="store_true")
    ns = ap.parse_args()

    print("épreuve — l'emballage de BrainKit, lot 10")
    j = Journal()
    tmp = Path(tempfile.mkdtemp(prefix="bk10-"))
    try:
        scenario_documents(j)
        scenario_genericite(j, tmp)
        scenario_profil_nu(j, tmp)
        scenario_croise(j, tmp)
        scenario_ponts(j, tmp)
        scenario_version(j)
        scenario_defaut(j, tmp)
        vault = temoin.resout(ns.vault_temoin)
        if vault is not None and (vault / ".git").exists():
            scenario_temoin(j, vault)
        else:
            print(f"\n8. TÉMOIN — sauté : {temoin.pourquoi_saute()}")
    finally:
        if ns.garder:
            print(f"\ndossier temporaire gardé : {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)

    print()
    if j.echecs:
        print(f"{len(j.echecs)} vérification(s) en échec :")
        for e in j.echecs:
            print(f"  - {e}")
        return 1
    print("OK — le jeu d'épreuve de l'emballage passe en entier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
