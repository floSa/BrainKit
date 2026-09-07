"""composer.py — des reponses au `brain.yml`. Rien de plus, rien d autre.

# La ligne de partage, et c est la seule idee du module

Un manifeste porte deux choses qui n ont rien a voir :

| ce qui se DEMANDE | ce qui se DERIVE |
|---|---|
| le sujet, le nom, l identite git | les dix regles, toutes en `a_mesurer` |
| l unite, les roles, ce qui est protege | les regles de socle |
| les paquets, leur nom, leur ordre | le dictionnaire de champs |
| le volume cible | le seuil, la table de propagation |
| les natures et leurs frontieres | la table de couleurs du graphe |
| les colonnes du bandeau et leur source | les chemins generes, les non-pages |
| les sections du corps et leur genre | l espace de l agent, les gabarits |
| les relations et leur reciprocite | le vocabulaire de tags, VIDE |
| les frontieres d ecriture, le livrable | le plan d ecriture du semis |

Tout ce qui est a droite se calcule. Le poser en question serait pire qu inutile :
ce serait demander a l utilisateur de valider un choix qu il n a aucun moyen
d evaluer, et il repondrait oui.

Tout ce qui est a gauche se demande, et le refus de le deviner est la valeur du
kit. Un composeur qui completerait une seule case de gauche rendrait l entretien
decoratif.

# Ce que le module refuse d ecrire

Il rend `(manifeste, griefs)`. Un grief n est pas un avertissement : tant qu il
en reste un, `--composer` n ECRIT PAS. Les treize refus tournent sur le
manifeste compose — pas seulement sur les reponses — parce que certains ne se
voient qu une fois le manifeste assemble : une severite autre que `a_mesurer`,
une colonne de bandeau sans champ source, un axe transverse de plus que demande.

# Il n ecrit AUCUNE page

Le manifeste compose declare des dossiers, des hubs, des gabarits et des
vocabulaires vides. Il ne declare aucune page d unite, aucun exemple, aucune
demonstration. Les titres cites en passe 2.1 vont dans `racine.pages[].amorce`,
d ou le semis les pose en cases a cocher — ils ont servi a INDUIRE, ils ne sont
pas captures.
"""

from __future__ import annotations

from typing import Any

from . import induction, refus as _refus
from .brouillon import Brouillon, _est_oui

KIT_VERSION = "0.1.0"

#: La palette du kit, par FONCTION de role. Elle ne se demande pas : une couleur
#: de graphe est une convention de lecture, pas une decision de taxonomie — et
#: l entretien a de meilleures questions a poser. Elle se change dans Obsidian
#: en trois clics, et la table du manifeste reste la seule source.
PALETTE = {
    "unite": "#412CDD",
    "notion": "#7AB800",
    "hub": "#FF922B",
    "vue": "#EF4444",
    "prescription": "#94A3B8",
    "transverse": "#FFD43B",
}

BALISES_AUTO = ["<!-- AUTO:START -->", "<!-- AUTO:END -->"]
BALISES_BANDEAU = ["<!-- AUTO:BANDEAU:START -->", "<!-- AUTO:BANDEAU:END -->"]

LECTURE_TAGS = "colonne 1 des tableaux, en backticks"


def _rgb(hexa: str) -> int:
    return int(hexa.lstrip("#"), 16)


def _lib(v: Any, defaut_s: str = "", defaut_p: str = "") -> dict:
    if isinstance(v, dict) and v.get("s") and v.get("p"):
        return {"s": str(v["s"]), "p": str(v["p"])}
    return {"s": defaut_s, "p": defaut_p}


def _ident(texte: str) -> str:
    c = induction.cle(texte)
    return c if c[:1].isalpha() else "x-" + c


# --------------------------------------------------------------------------- #
def compose(b: Brouillon) -> tuple[dict | None, list[str]]:
    """Rend (manifeste, griefs). Un seul grief, et le manifeste ne s ecrit pas."""
    arret = _refus.arret(b.reponses)
    if arret:
        return None, [arret]

    griefs: list[str] = []
    m: dict[str, Any] = {}

    # ---------------------------------------------------------------- en-tete
    unite = _lib(b.valeur("1.2"))
    if not unite["s"]:
        return None, ["1.2 sans réponse — sans le nom de l'unité, rien ne se "
                      "compose : il fuit dans les gabarits, les hubs, les skills "
                      "et le routeur."]
    axe_r = _lib(b.valeur("2.5"), "domaine", "domaines")

    m["manifeste"] = 1
    m["kit"] = {"version": KIT_VERSION, "mode": "branche"}
    m["brain"] = {
        "nom": str(b.valeur("0.2") or "").strip(),
        "sujet": str(b.valeur("0.1") or "").strip(),
        "langue": "fr",
        "volume_cible": int(b.valeur("2.6") or 0),
        "usage": str(b.valeur("0.3") or "perso"),
        "profil": "obsidian",
        "proprietaire": {"nom": str((b.valeur("0.4") or {}).get("name") or "")},
    }

    identite = b.valeur("0.4") or {}
    refuses = b.valeur("0.5") or []
    if isinstance(refuses, str):
        refuses = [refuses]
    usage = m["brain"]["usage"]
    m["git"] = {
        "identite": {"name": str(identite.get("name")),
                     "email": str(identite.get("email"))},
        "domaines_refuses": [str(x).lstrip("@") for x in refuses],
        "trailers_refuses": ["Co-Authored-By"],
        "branche_principale": "main",
        "motif": (
            f"`usage: {usage}` — la POLARITÉ du garde-fou en découle : ce qui est "
            f"refusé ici est ce que la question 0.5 a nommé, et rien d'autre. "
            f"L'identité ne se devine JAMAIS : l'entretien s'arrête si la réponse "
            f"à 0.4 ne vient pas, et il ne lit jamais l'adresse annoncée par le "
            f"harnais. Les hooks lisent l'identité ATTENDUE (`git config --local "
            f"user.email`) plutôt qu'un domaine codé en dur, ce qui rend le "
            f"garde-fou valable dans les deux polarités."),
    }

    # ---------------------------------------------------------------- roles
    roles, notion_id, vue_id, prescriptions, griefs_roles = _roles(b, unite, axe_r)
    griefs += griefs_roles
    m["libelles"] = _libelles(b, unite, notion_id, vue_id, prescriptions, axe_r)
    m["roles"] = roles

    # ---------------------------------------------------------------- axes
    axes, griefs_axes, prefixes = _axes(b, unite, axe_r, roles)
    griefs += griefs_axes
    m["axes"] = axes

    # ---------------------------------------------------------------- champs
    m["champs"] = _champs(b, axes)

    # ---------------------------------------------------------------- bandeau
    bandeau = _bandeau(b, roles)
    if bandeau:
        m["bandeau"] = bandeau

    # ---------------------------------------------------------------- regles
    m["regles"] = _les_dix(b, m)
    m["regles_de_socle"] = _le_socle()
    m["seuils"] = {
        "vue_min_valeurs_axe": 3,
        "vue_min_membres": 2,
        "motif": "Des seuils de SENS, pas des mesures de corpus : une table qui "
                 "ne départage que deux valeurs, ou qui ne liste que deux "
                 "membres, ne vaut pas une page.",
    }

    # ------------------------------------------------- vocabulaires et graphe
    m["vocabulaires"] = _vocabulaires(b, axe_r)
    m["graphe"] = _graphe(roles, axes)
    m["genere"] = _genere(b, m, axe_r)
    m["propagation"] = _propagation(m, unite, notion_id, vue_id)
    m["skills"] = _skills(b, m)
    m["agent"] = _agent()
    m["racine"] = _racine(b, unite)
    m["frontieres_d_ecriture"] = _frontieres(b, roles)

    griefs += [f"refus n° {n} : {g}" for n, g in _refus.controle(b.reponses, m)]
    return m, griefs


# --------------------------------------------------------------------------- #
#  Le vocabulaire visible
# --------------------------------------------------------------------------- #
def _libelles(b: Brouillon, unite: dict, notion_id: str | None,
              vue_id: str | None, prescriptions: list[dict],
              axe_r: dict) -> dict:
    """Le SEUL endroit du kit où le mot de l unite existe.

    Il ne se traduit pas : il se recopie depuis la question 1.2. Le jour ou une
    valeur d ici est le mot d un autre brain, l entretien a echoue.
    """
    L: dict[str, Any] = {"unite": unite}
    if notion_id:
        n = b.valeur("1.3")
        L["notion"] = _lib(n if isinstance(n, dict) else {}, "notion", "notions")
    if vue_id:
        L["vue"] = _lib((b.valeur("8.2") or {}).get("libelle"))
    L["hub"] = {"s": "hub", "p": "hubs"}
    if prescriptions:
        L["prescription"] = prescriptions[0]
    L["axe_rangement"] = axe_r
    nature = b.valeur("3.2")
    if isinstance(nature, dict) and nature.get("libelle"):
        L["axe_nature"] = _lib(nature["libelle"])
    transverses = {}
    for t in (b.valeur("4.1") or []):
        if isinstance(t, dict) and t.get("champ") and t.get("libelle"):
            transverses[str(t["champ"])] = _lib(t["libelle"])
    if transverses:
        L["axe_transverse"] = transverses
    L["motif"] = (
        "Repris MOT POUR MOT des réponses 1.2, 1.3, 2.5, 3.2, 4.1 et 8.2. "
        "Aucun mot d'un autre brain n'entre ici : ni « brique », ni "
        "« comparatif », ni « source ». Si un de ces mots apparaissait, ce "
        "serait le signe que l'entretien a traduit au lieu d'écouter."
        + (f" `prescription` ne porte que le premier des "
           f"{len(prescriptions)} rôles de prescription : le champ est un "
           f"singulier, les rôles sont une liste, et c'est `roles[]` qui fait "
           f"foi." if len(prescriptions) > 1 else ""))
    return L


# --------------------------------------------------------------------------- #
#  Les roles
# --------------------------------------------------------------------------- #
def _roles(b: Brouillon, unite: dict, axe_r: dict):
    griefs: list[str] = []
    proteges = {str(x).strip().lower() for x in (b.valeur("1.4") or [])}
    corps_par_role = b.valeur("6.1")
    corps_dict = corps_par_role if isinstance(corps_par_role, dict) else {}

    unite_id = _ident(unite["s"])
    roles: list[dict] = []

    # --- l unite ---------------------------------------------------------- #
    champs_unite = _champs_du_role(b, "unite")
    roles.append({
        "id": unite_id,
        "fonction": "unite",
        "libelle": unite,
        "range_par": "axe",
        "protege": unite["s"].lower() in proteges,
        "pese_sur_le_seuil": True,
        "apparait_dans_le_hub": True,
        "couleur": PALETTE["unite"],
        "taille_avertissement": 150,
        "champs": champs_unite,
        "corps": _corps_unite(b, unite_id, corps_dict),
        "motif": (
            f"L'unité sort de la question 1.1 — ce que l'utilisateur ira "
            f"CHERCHER dans six mois — et de 1.2 pour le mot. L'entretien ne l'a "
            f"pas nommée : il l'a induite, puis fait confirmer. Le kit ne connaît "
            f"le mot « {unite['s']} » nulle part ailleurs que dans ce manifeste."),
    })

    # --- la notion -------------------------------------------------------- #
    notion_id = None
    n = b.valeur("1.3")
    if n and (not isinstance(n, str) or _est_oui(n)):
        lib = _lib(n if isinstance(n, dict) else {}, "notion", "notions")
        notion_id = _ident(lib["s"])
        protege = lib["s"].lower() in proteges or bool(
            isinstance(n, dict) and n.get("protege"))
        roles.append({
            "id": notion_id,
            "fonction": "notion",
            "libelle": lib,
            "range_par": "axe",
            "protege": protege,
            "pese_sur_le_seuil": True,
            "apparait_dans_le_hub": True,
            "couleur": PALETTE["notion"],
            "taille_avertissement": 200,
            "champs": _champs_du_role(b, "notion"),
            "corps": _corps_secondaire(corps_dict, notion_id, lib),
            "motif": (
                "Réponse « oui » à 1.3 : des pages qui n'expliquent pas quoi "
                "utiliser mais ce qu'il faut comprendre." +
                (" `protege: true` vient de 1.4, et il ne se pose jamais par "
                 "défaut : c'est l'utilisateur qui a dit que ces pages sont à "
                 "lui. La frontière est portée par le CHAMP `role:`, pas par un "
                 "chemin — donc lire le frontmatter avant d'écrire."
                 if protege else
                 " 1.4 n'a désigné aucun rôle protégé, et l'entretien n'en pose "
                 "pas d'office.")),
        })

    # --- le hub ----------------------------------------------------------- #
    roles.append(_role_hub(b, axe_r, unite, notion_id))

    # --- la vue ----------------------------------------------------------- #
    vue_id = None
    v = b.valeur("8.2") or (b.valeur("8.1") if isinstance(b.valeur("8.1"), dict)
                            else None)
    interchangeables = _est_oui(b.valeur("8.1"))
    if isinstance(v, dict) and v.get("libelle"):
        lib = _lib(v.get("libelle"))
        vue_id = _ident(lib["s"])
        roles.append({
            "id": vue_id,
            "fonction": "vue",
            "libelle": lib,
            "range_par": "axe",
            "prefixe_nom": str(v.get("prefixe_nom") or f"{lib['s'].capitalize()} - "),
            "protege": False,
            "pese_sur_le_seuil": False,
            "apparait_dans_le_hub": True,
            "couleur": PALETTE["vue"],
            "regle_de_categorie": "majorite",
            "vue_embarquee": {
                "extension": ".base",
                "moteur": "obsidian-bases",
                "embed": "![[<même nom>.base]]",
                "tri_par": str(v.get("tri_par") or ""),
                "direction": str(v.get("direction") or "asc"),
                "genere": False,
                "motif_non_genere": (
                    "Les vues sont du CONTENU : deux tables du même paquet "
                    "voudront deux filtres. Le générateur en amorce une par "
                    "dossier promu, avec l'ordre de colonnes par défaut, et "
                    "s'arrête là."),
                "colonnes_par_defaut": list(v.get("colonnes") or []),
            },
            "hub_de_ralliement": _ralliement(b, lib),
            "champs": _champs_du_role(b, "vue"),
            "corps": _corps_vue(lib),
            "motif": (
                ("8.1 = oui : les unités sont INTERCHANGEABLES, et la page les "
                 "départage. C'est la seule branche où le mot « comparatif » "
                 "aurait un sens — et il reste au vocabulaire de l'utilisateur, "
                 "pas à celui du kit."
                 if interchangeables else
                 "8.1 = NON : les unités ne sont pas interchangeables, donc "
                 "l'entretien n'a pas traduit le comparatif. Ce qui survit est "
                 "la PRIMITIVE — une page qui embarque une table filtrée sur "
                 "une valeur de l'axe, plus une section écrite à la main, plus "
                 "un hub de ralliement avec lien retour. L'intention "
                 "« départager des interchangeables » ne survit pas.")),
        })
    elif not interchangeables and b.a_repondu("8.2") and not b.valeur("8.2"):
        pass    # « non » aux deux : aucun role `vue`, et c est legal.

    # --- les prescriptions ------------------------------------------------ #
    prescriptions: list[dict] = []
    for p in (b.valeur("1.5") or []):
        if not isinstance(p, dict) or not p.get("libelle"):
            continue
        lib = _lib(p.get("libelle"))
        rid = _ident(lib["s"])
        prescriptions.append(lib)
        roles.append({
            "id": rid,
            "fonction": "prescription",
            "libelle": lib,
            "range_par": "role",
            "dossier": str(p.get("dossier") or lib["p"].capitalize()),
            "prefixe_nom": str(p.get("prefixe_nom") or f"{lib['s'].capitalize()} - "),
            "protege": lib["s"].lower() in proteges,
            "pese_sur_le_seuil": False,
            "apparait_dans_le_hub": True,
            "couleur": PALETTE["prescription"],
            "champs": _champs_du_role(b, "prescription", p),
            "corps": _corps_prescription(lib),
            "motif": (
                f"Réponse à 1.5 : une page qui PRESCRIT enjambe les "
                f"{axe_r['p']} par construction, donc elle ne porte aucune "
                f"valeur de l'axe de rangement, donc son chemin se lit sur son "
                f"rôle. `range_par: role`, et le dossier se déclare — il ne se "
                f"dérive pas d'une clé."),
        })

    ids = [r["id"] for r in roles]
    for rid in sorted(set(ids)):
        if ids.count(rid) > 1:
            griefs.append(f"deux rôles portent l'identifiant `{rid}` — deux rôles "
                          f"ne peuvent pas se nommer pareil, même au pluriel près.")
    return roles, notion_id, vue_id, prescriptions, griefs


def _ralliement(b: Brouillon, lib: dict) -> dict | None:
    r = b.valeur("8.3")
    if not r:
        return None
    if isinstance(r, str) and not _est_oui(r):
        return None
    d = r if isinstance(r, dict) else {}
    return {
        "dossier": str(d.get("dossier") or lib["p"].capitalize()),
        "lien_retour": str(d.get("lien_retour") or "Voir aussi"),
        "groupe_par": "premier segment du chemin",
        "motif": "C'est le LIEN RETOUR qui fait la grappe dans le graphe, pas le "
                 "dossier. Rappelé par l'entretien, question 8.3.",
    }


def _role_hub(b: Brouillon, axe_r: dict, unite: dict, notion_id: str | None) -> dict:
    """Le hub — entierement DERIVE. Aucune question ne le decrit, et c est juste :
    un hub n est pas un choix editorial, c est l aiguillage d un dossier."""
    return {
        "id": "hub",
        "fonction": "hub",
        "libelle": {"s": "hub", "p": "hubs"},
        "range_par": "axe",
        "porte_categorie": False,
        "protege": False,
        "pese_sur_le_seuil": False,
        "apparait_dans_le_hub": False,
        "couleur": PALETTE["hub"],
        "champs": {"requis": ["role", "nom", _resume(b)],
                   "autorises": ["role", "nom", "alias", _resume(b), "tags"]},
        "corps": [
            {"titre": "Ce qu'il faut comprendre", "niveau": 2, "genre": "libre",
             "ecrit_a_la_main": True},
            {"titre": "<AUTO>", "niveau": 0, "genre": "auto",
             "balises": list(BALISES_AUTO), "perimetre": "dossier",
             "sections": [],   # rempli par _sections_auto, une fois les rôles connus
             },
        ],
        "motif": "Un `role: hub` ne porte pas de valeur de l'axe de rangement : "
                 "un hub ne se range pas, il EST le rangement — son domaine est "
                 "son chemin. Les sous-titres de sa zone AUTO se DÉRIVENT de la "
                 "liste des rôles au pluriel : rien à écrire.",
    }


def _sections_auto(roles: list[dict], axe_r: dict) -> list[dict]:
    out = [{"titre": f"Sous-{axe_r['p']}",
            "source": "sous-dossiers portant un hub",
            "depuis": "sous_dossiers", "separateur": " · "}]
    for r in roles:
        if r["fonction"] == "hub" or not r.get("apparait_dans_le_hub"):
            continue
        out.append({"titre": r["libelle"]["p"].capitalize(),
                    "source": f"role: {r['id']} du dossier",
                    "depuis": "role", "role": r["id"]})
    return out


# --------------------------------------------------------------------------- #
#  Les champs d un role
# --------------------------------------------------------------------------- #
def _resume(b: Brouillon) -> str:
    v = b.valeur("7.4")
    if isinstance(v, dict):
        return str(v.get("champ") or "resume")
    return str(v or "resume")


def _champs_transverses(b: Brouillon) -> list[str]:
    return [str((t or {}).get("champ")) for t in (b.valeur("4.1") or [])
            if (t or {}).get("champ")]


def _champ_nature(b: Brouillon) -> str | None:
    v = b.valeur("3.2")
    if not _est_oui(b.valeur("3.1")) or not isinstance(v, dict):
        return None
    return str(v.get("champ") or "nature")


def _champs_de_liens(b: Brouillon) -> list[dict]:
    """Les relations de la passe 7, avec leur mode de reciprocite."""
    out: list[dict] = []
    for r in (b.valeur("7.1") or []):
        if not isinstance(r, dict) or not r.get("champ"):
            continue
        champ = str(r["champ"])
        sym = (b.valeur("7.2") or {}).get(champ)
        inv = (b.valeur("7.3") or {}).get(champ)
        entree = {"champ": champ, "section": str(r.get("section") or champ)}
        if inv:
            entree["mode"] = "inverse"
            entree["inverse"] = str(inv if isinstance(inv, str)
                                    else inv.get("champ"))
            entree["section_inverse"] = str(
                inv.get("section") if isinstance(inv, dict) else
                f"{champ.capitalize()} par")
        elif sym is None or _est_oui(sym):
            entree["mode"] = "symetrique"
        else:
            entree["mode"] = None
        out.append(entree)
    return out


def _champs_de_bandeau(b: Brouillon) -> dict[str, dict]:
    """{champ: declaration} pour les sources de colonnes qui ne sont pas déjà là."""
    out: dict[str, dict] = {}
    for titre, d in (b.valeur("5.2") or {}).items():
        d = d if isinstance(d, dict) else {"source": d}
        for cle in ("source", "qualifie_par"):
            champ = d.get(cle)
            if not champ:
                continue
            decl = {"type": str(d.get("type") or "ligne") if cle == "source"
                    else "ligne", "fonction": "aucune"}
            if cle == "source" and d.get("valeurs"):
                decl = {"type": "enum", "valeurs": list(d["valeurs"]),
                        "eliminatoire": [], "fonction": "aucune",
                        "motif": "Le champ `eliminatoire:` est VIDE, et "
                                 "délibérément : le kit n'a aucune intuition sur "
                                 "« quelle valeur d'énumération disqualifie ». "
                                 "Ce qui élimine se déclare."}
            out.setdefault(str(champ), decl)
    return out


def _champs_du_role(b: Brouillon, fonction: str, extra: dict | None = None) -> dict:
    resume = _resume(b)
    nature = _champ_nature(b)
    transverses = _champs_transverses(b)
    liens = _champs_de_liens(b)
    bandeau = list(_champs_de_bandeau(b))

    if fonction == "unite":
        requis = ["role", "nom", resume, "categorie"]
        autorises = ["role", "nom", "alias", resume, "categorie"]
        if nature:
            autorises.append(nature)
        autorises += transverses
        autorises += [c for c in bandeau if c not in autorises]
        for L in liens:
            autorises.append(L["champ"])
            if L.get("mode") == "inverse" and L.get("inverse"):
                autorises.append(L["inverse"])
        autorises += ["tags", "url"]
        champs = {"requis": requis,
                  "autorises": _uniques(autorises)}
        cond = [c for c in (b.valeur("3.4") or [])
                if isinstance(c, dict) and c.get("champ") and c.get("si")]
        if cond:
            champs["conditionnels"] = [{"champ": str(c["champ"]),
                                        "si": str(c["si"])} for c in cond]
            champs["motif_conditionnels"] = (
                "Un champ qui décrit 100 % des pages ne discrimine rien. Ceux-ci "
                "n'ont de sens que pour certaines valeurs de l'axe de nature, et "
                "le dire évite un frontmatter où la moitié des lignes sont vides "
                "sans qu'on sache si c'est un oubli ou une non-application.")
            for c in champs["conditionnels"]:
                if c["champ"] not in champs["autorises"]:
                    champs["autorises"].append(c["champ"])
        return champs

    if fonction == "notion":
        autorises = ["role", "nom", "alias", resume, "categorie"] + transverses
        return {"requis": ["role", "nom", "categorie"],
                "autorises": _uniques(autorises + ["tags"])}
    if fonction == "vue":
        return {"requis": ["role", "nom", "categorie"],
                "autorises": ["role", "nom", resume, "categorie", "tags"]}
    if fonction == "prescription":
        propres = [str(x) for x in ((extra or {}).get("champs") or [])]
        return {"requis": _uniques(["role", "nom", resume] + propres),
                "autorises": _uniques(["role", "nom", "alias", resume, "tags"]
                                      + propres)}
    return {"requis": ["role", "nom"], "autorises": ["role", "nom", "tags"]}


def _uniques(xs: list[str]) -> list[str]:
    out: list[str] = []
    for x in xs:
        if x and x not in out:
            out.append(x)
    return out


# --------------------------------------------------------------------------- #
#  Le corps
# --------------------------------------------------------------------------- #
def _corps_unite(b: Brouillon, unite_id: str, corps_dict: dict) -> list[dict]:
    brut = corps_dict.get(unite_id) if corps_dict else b.valeur("6.1")
    brut = brut or []
    prose = b.valeur("6.2")
    decision = b.valeur("6.3")
    listes = {str(x.get("titre")): x for x in (b.valeur("6.4") or [])
              if isinstance(x, dict)}
    etiquetee = b.valeur("6.5")

    corps: list[dict] = [{"titre": "<bandeau>", "niveau": 0, "genre": "bandeau"}]
    for s in brut:
        titre = str(s.get("titre") if isinstance(s, dict) else s)
        niveau = int(s.get("niveau", 2)) if isinstance(s, dict) else 2
        entree: dict[str, Any] = {"titre": titre, "niveau": niveau,
                                  "genre": "libre"}
        if prose and titre == str(prose):
            entree["genre"] = "prose"
            entree["doctrine"] = ("La SEULE section où la prose est permise. La "
                                  "doctrine a une raison mesurée : de la prose "
                                  "partout rend une page illisible en diagonale, "
                                  "et une page qu'on ne lit pas en diagonale ne "
                                  "se relit jamais.")
        elif isinstance(decision, dict) and titre == str(decision.get("titre")):
            entree["genre"] = "decision"
            entree["colonne_positive"] = str(decision.get("positive") or "Pour")
            entree["colonne_negative"] = str(decision.get("negative") or "Contre")
        elif titre in listes:
            entree["genre"] = "liste_liens"
            entree["champ"] = listes[titre].get("champ")
        elif isinstance(etiquetee, dict) and titre == str(etiquetee.get("titre")):
            entree["genre"] = "etiquetee"
            entree["obligatoires"] = list(etiquetee.get("obligatoires") or [])
            entree["permises"] = list(etiquetee.get("permises")
                                      or etiquetee.get("obligatoires") or [])
            entree["motif"] = ("Vocabulaire FERMÉ, et nommé par l'utilisateur. "
                               "L'entretien refuse de le compléter : cinq "
                               "étiquettes nommées valent mieux que sept dont "
                               "deux inventées.")
        if isinstance(s, dict) and s.get("existe_si"):
            entree["genre"] = "conditionnelle"
            entree["existe_si"] = str(s["existe_si"])
            entree["forme"] = str(s.get("forme") or "")
        corps.append(entree)

    for titre, d in listes.items():
        if not any(c["titre"] == titre for c in corps):
            corps.append({"titre": titre, "niveau": int(d.get("niveau", 2)),
                          "genre": "liste_liens", "champ": d.get("champ")})
    return corps


def _corps_secondaire(corps_dict: dict, rid: str, lib: dict) -> list[dict]:
    """Le corps d un role SECONDAIRE : celui de l utilisateur, ou un SQUELETTE.

    Ce n est pas une induction, et le manifeste le dit : la question 6.1 porte
    sur la page d unite. Si l utilisateur a decrit les autres roles (reponse en
    dictionnaire), c est la sienne qui passe ; sinon le kit pose trois sections
    minimales, marquees comme un squelette a EDITER — et non comme un choix.
    """
    if corps_dict and corps_dict.get(rid):
        return _brut(corps_dict[rid])
    return [
        {"titre": "Aperçu", "niveau": 2, "genre": "prose"},
        {"titre": "Ce qu'il faut retenir", "niveau": 2, "genre": "libre"},
        {"titre": "Voir aussi", "niveau": 2, "genre": "liste_liens",
         "champ": None},
        {"titre": "<squelette>", "niveau": 0, "genre": "libre",
         "motif": f"SQUELETTE, pas induction. La question 6.1 porte sur la page "
                  f"d'unité ; le corps d'une page « {lib['s']} » n'a pas été "
                  f"décrit. Trois sections minimales sont posées pour que le "
                  f"gabarit existe, et elles sont à réécrire au premier usage. "
                  f"Les laisser telles quelles six mois serait le signe qu'il "
                  f"fallait reposer la question."},
    ]


def _brut(sections: list) -> list[dict]:
    out: list[dict] = []
    for s in sections:
        if isinstance(s, dict):
            e = {"titre": str(s.get("titre")), "niveau": int(s.get("niveau", 2)),
                 "genre": str(s.get("genre") or "libre")}
            if s.get("champ") is not None or e["genre"] == "liste_liens":
                e["champ"] = s.get("champ")
            if s.get("existe_si"):
                e["genre"] = "conditionnelle"
                e["existe_si"] = str(s["existe_si"])
            out.append(e)
        else:
            out.append({"titre": str(s), "niveau": 2, "genre": "libre"})
    return out


def _corps_vue(lib: dict) -> list[dict]:
    return [
        {"titre": "<accroche>", "niveau": 0, "genre": "prose",
         "forme": "> La table : …"},
        {"titre": "<embed>", "niveau": 0, "genre": "auto"},
        {"titre": f"Ce que la {lib['s']} montre", "niveau": 2,
         "genre": "liste_liens", "champ": None},
        {"titre": "Voir aussi", "niveau": 2, "genre": "liste_liens",
         "champ": None},
    ]


def _corps_prescription(lib: dict) -> list[dict]:
    return [
        {"titre": "Principe", "niveau": 2, "genre": "prose"},
        {"titre": "En pratique", "niveau": 2, "genre": "libre"},
        {"titre": "Exceptions", "niveau": 2, "genre": "libre"},
        {"titre": "Voir aussi", "niveau": 2, "genre": "liste_liens",
         "champ": None},
    ]


# --------------------------------------------------------------------------- #
#  Les axes
# --------------------------------------------------------------------------- #
def _axes(b: Brouillon, unite: dict, axe_r: dict, roles: list[dict]):
    griefs: list[str] = []
    titres = b.valeur("2.1") or []
    paquets = b.valeur("2.2") or {}
    p = induction.induis_les_paquets(list(titres), dict(paquets))
    griefs += [d.rendu() for d in p.bloquants]

    exclusif = _est_oui(b.valeur("2.3")) if b.a_repondu("2.3") else p.exclusif
    deborde = b.valeur("2.4") or {}
    seuil, motif_seuil = induction.derive_le_seuil(int(b.valeur("2.6") or 0),
                                                   len(p.prefixes))

    prefixes = []
    for x in p.prefixes:
        prefixes.append({"cle": _ident(x["dossier"]), "dossier": x["dossier"],
                         "portee": "", "sous": {}})
    for pref in prefixes:
        if not pref["portee"]:
            pref.pop("portee")

    arbre = b.valeur("2.7") or {}
    branches = _branches(arbre)
    griefs += [d.rendu() for d in induction.verifie_l_arbre(branches, prefixes)
               if d.bloquant]

    rangement: dict[str, Any] = {
        "champ": "categorie",
        "exclusif": bool(exclusif),
        "seuil_promotion": seuil,
        "motif_seuil": motif_seuil,
        "plafond_promotion": True,
        "motif_plafond": "Un sous-dossier qui ne laisserait AUCUNE page au niveau "
                         "du parent redouble ce parent : il se refuse.",
        "niveaux": 2,
        "valeur_courte_autorisee": True,
        "motif_valeur_courte": (
            "Un paquet sans division interne porte une valeur NUE — pas une "
            "sous-valeur inventée pour satisfaire un format. Forcer "
            "`paquet/sous` quand le sous n'existe pas serait exactement le "
            "refus n° 3 appliqué au frontmatter."),
        "consequence_du_seuil": (
            "Changer le seuil RÉFORME l'arbre : les pages se déplacent. "
            "`brainkit re-seuiller` émet un `git mv` par page, refuse de tourner "
            "sur un arbre sale, et ne supprime jamais un hub devenu orphelin — "
            "il le signale."),
        "prefixes": prefixes,
        "rattachements": {},
        "motif_rattachements_vides": (
            "Aucun. Un rattachement est un sédiment : une exception NOMMÉE ET "
            "DATÉE qu'un arbitrage réel a produite. Un brain neuf n'en a aucune, "
            "et le mécanisme à transposer est la PLACE où elles s'écrivent."),
        "arbre_de_decision": branches,
        "motif_arbre": (
            "L'ORDRE est LA décision de conception, et il vient de l'utilisateur "
            "(question 2.7). Une page se range à la PREMIÈRE question qui répond "
            "oui : proposer les questions est légitime, en fixer le rang ne "
            "l'est pas."),
        "departages": [],
        "frontieres": [],
        "motif_listes_vides": (
            "NAISSENT VIDES, et l'entretien l'a dit à haute voix : ces deux "
            "listes se rempliront page par page, quand un arbitrage se répétera. "
            "Les remplir maintenant serait inventer des problèmes qu'on n'a pas."),
    }
    if not exclusif:
        transversal = str((deborde or {}).get("prefixe_transversal") or "")
        rangement["regle_de_majorite"] = True
        rangement["definition_de_la_majorite"] = (
            "la valeur de l'axe est celle qui rassemble le plus de la page")
        rangement["prefixe_transversal"] = _ident(transversal) if transversal \
            else ""
        rangement["motif_non_exclusif"] = (
            "Réponse « non » à 2.3 : des pages débordent. Deux mécanismes le "
            "réparent, et aucun n'invente : la règle de MAJORITÉ pour celles qui "
            "ont un centre de gravité, un préfixe DÉCLARÉ pour celles qui n'en "
            "ont pas. Sans eux, l'utilisateur MENTIRAIT dans le champ — et le "
            "validateur resterait vert, ce qui est le pire des résultats.")
        if not transversal:
            griefs.append(
                "2.4 : l'axe n'est pas exclusif et aucun paquet transversal n'est "
                "nommé. Une page sans centre de gravité n'aurait nulle part où "
                "aller — laquelle de tes pages qui débordent couvre VRAIMENT "
                "tout, et comment appelles-tu le paquet qui l'accueille ?")
        elif not any(x["cle"] == rangement["prefixe_transversal"]
                     for x in prefixes):
            griefs.append(
                f"le préfixe transversal `{rangement['prefixe_transversal']}` "
                f"n'est pas un des paquets rangés en 2.2.")

    axes: dict[str, Any] = {"rangement": rangement}

    # --- l axe de nature -------------------------------------------------- #
    nature = _axe_nature(b, roles)
    if nature:
        axes["nature"] = nature

    # --- les axes transverses --------------------------------------------- #
    transverses = _transverses(b)
    griefs += [d.rendu() for d in
               induction.verifie_les_transverses(transverses, prefixes)
               if d.bloquant]
    axes["transverses"] = transverses

    # Les sous-titres de la zone AUTO se derivent, une fois les roles connus.
    for r in roles:
        if r["fonction"] != "hub":
            continue
        for s in r["corps"]:
            if s.get("genre") == "auto":
                s["sections"] = _sections_auto(roles, axe_r)
    return axes, griefs, prefixes


def _branches(arbre: Any) -> list[dict]:
    brut = arbre.get("branches") if isinstance(arbre, dict) else arbre
    out: list[dict] = []
    for i, b_ in enumerate(brut or [], start=1):
        if not isinstance(b_, dict):
            continue
        e: dict[str, Any] = {
            "n": str(b_.get("n") or f"D{i}"),
            "question": str(b_.get("question") or ""),
            "si_oui": b_.get("si_oui") if b_.get("si_oui") is not None else [],
        }
        if b_.get("arret"):
            e["arret"] = True
            e["motif"] = str(b_.get("motif") or
                             "ARRÊT — demander. Une valeur manquante ne "
                             "s'invente jamais.")
        if b_.get("defaut"):
            e["defaut"] = True
        out.append(e)
    return out


def _axe_nature(b: Brouillon, roles: list[dict]) -> dict | None:
    if not _est_oui(b.valeur("3.1")):
        return None
    d = b.valeur("3.2")
    if not isinstance(d, dict):
        return None
    champ = str(d.get("champ") or "nature")
    valeurs = []
    for v in (d.get("valeurs") or []):
        if isinstance(v, dict) and v.get("cle"):
            valeurs.append({"cle": _ident(str(v["cle"])),
                            "definition": str(v.get("definition") or ""),
                            "frontiere": str(v.get("frontiere") or "")})
    if not valeurs:
        return None
    unite_id = next(r["id"] for r in roles if r["fonction"] == "unite")
    return {
        "champ": champ,
        "porte_par": [unite_id],
        "interdit_sur": [r["id"] for r in roles if r["fonction"] != "unite"],
        "vide_autorise": True,
        "motif_vide": (
            "Un champ vide est le SEUL signal prévu pour « l'arbre n'a pas "
            "tranché ». Une valeur inventée est une faute ; un champ vide est "
            "une question ouverte, qui se referme le jour où on écrit la page."),
        "valeurs": valeurs,
        "arbre_de_decision": _branches(b.valeur("3.3")),
        "departages": [],
        "frontieres": [],
        "motif_listes_vides": "Naissent vides, comme celles de l'axe de rangement.",
    }


def _transverses(b: Brouillon) -> list[dict]:
    multi = b.valeur("4.2") or {}
    dossiers = b.valeur("4.3") or {}
    out: list[dict] = []
    for t in (b.valeur("4.1") or []):
        if not isinstance(t, dict) or not t.get("champ"):
            continue
        champ = str(t["champ"])
        valeurs = [{"cle": _ident(str(v.get("cle"))),
                    "libelle": str(v.get("libelle") or v.get("cle"))}
                   for v in (t.get("valeurs") or []) if isinstance(v, dict)]
        if not valeurs:
            continue
        out.append({
            "champ": champ,
            "dossier": str(dossiers.get(champ) or t.get("dossier") or
                           champ.capitalize()),
            "multivalue": bool(multi.get(champ, t.get("multivalue", True))),
            "hub_par_valeur": True,
            "pointe_vers": "les sous-hubs, jamais les feuilles",
            "valeurs": valeurs,
        })
    return out


# --------------------------------------------------------------------------- #
#  Le dictionnaire de champs
# --------------------------------------------------------------------------- #
def _champs(b: Brouillon, axes: dict) -> dict:
    resume = _resume(b)
    champs: dict[str, Any] = {
        "role": {"type": "enum", "source": "roles[].id", "fonction": "aucune"},
        "nom": {"type": "ligne", "fonction": "identite",
                "exemption": "un `nom:` portant / \\ : * ? \" < > | ne peut pas "
                             "être un nom de fichier"},
        "alias": {"type": "liste", "fonction": "alias", "unicite": "souple"},
    }
    sections_reinjectees = [s["titre"] for s in _sections_liste_liens(b)
                            if s.get("champ")]
    champs[resume] = {
        "type": "ligne", "fonction": "resume_court", "section": None,
        "reinjecte_dans": sections_reinjectees,
        "motif": "Le champ désigné comme résumé d'une ligne est RECOPIÉ, jamais "
                 "retapé, chez tous ceux qui citent la page. Si la question 7.4 "
                 "n'avait désigné aucun champ, la règle 6 se serait DÉSACTIVÉE : "
                 "on n'en invente pas un.",
    }
    champs["categorie"] = {"type": "enum", "source": "axes.rangement",
                           "fonction": "aucune"}
    nature = _champ_nature(b)
    if nature:
        champs[nature] = {"type": "enum", "source": "axes.nature",
                          "fonction": "aucune"}
    for t in axes.get("transverses") or []:
        champs[t["champ"]] = {
            "type": "liste_enum" if t["multivalue"] else "enum",
            "source": f"axes.transverses[{t['champ']}]", "fonction": "aucune"}
    for champ, decl in _champs_de_bandeau(b).items():
        champs.setdefault(champ, decl)
    # Les champs CONDITIONNELS (question 3.4) sont des champs comme les autres :
    # ils entrent dans le dictionnaire, et c est `roles[].champs.conditionnels`
    # qui dit QUAND ils ont un sens. Les oublier ici ferait un `autorises` qui
    # cite un champ que personne ne definit.
    for c in (b.valeur("3.4") or []):
        if isinstance(c, dict) and c.get("champ"):
            champs.setdefault(str(c["champ"]), {
                "type": str(c.get("type") or "ligne"), "fonction": "aucune",
                "motif": f"Conditionnel : {c.get('si')}. Un champ qui décrirait "
                         f"100 % des pages ne discriminerait rien."})
    for L in _champs_de_liens(b):
        if L["mode"] == "symetrique":
            champs[L["champ"]] = {"type": "liens",
                                  "reciproque": {"mode": "symetrique"},
                                  "section": L["section"], "fonction": "aucune"}
        elif L["mode"] == "inverse":
            champs[L["champ"]] = {
                "type": "liens",
                "reciproque": {"mode": "inverse", "champ": L["inverse"]},
                "section": L["section"], "fonction": "aucune",
                "motif": "MODE INVERSE : « A " + L["champ"] + " B » n'implique "
                         "pas « B " + L["champ"] + " A ». La relation demande "
                         "une PAIRE de champs, pas un miroir — et le validateur "
                         "refuse une paire mal déclarée, sinon on remplacerait "
                         "un trou par un autre.",
            }
            champs[L["inverse"]] = {
                "type": "liens",
                "reciproque": {"mode": "inverse", "champ": L["champ"]},
                "section": L["section_inverse"], "fonction": "aucune"}
        else:
            champs[L["champ"]] = {"type": "liens", "reciproque": None,
                                  "section": L["section"], "fonction": "aucune"}
    for p in (b.valeur("1.5") or []):
        for c in ((p or {}).get("champs") or []):
            champs.setdefault(str(c), {"type": "ligne", "fonction": "aucune"})
    champs["tags"] = {"type": "liste_enum", "source": "vocabulaires.tags",
                      "fonction": "aucune"}
    champs["url"] = {"type": "url", "fonction": "aucune"}
    return champs


def _sections_liste_liens(b: Brouillon) -> list[dict]:
    out = [x for x in (b.valeur("6.4") or []) if isinstance(x, dict)]
    for L in _champs_de_liens(b):
        if L.get("mode") == "inverse":
            out.append({"titre": L["section_inverse"], "champ": L["inverse"]})
    return out


# --------------------------------------------------------------------------- #
def _bandeau(b: Brouillon, roles: list[dict]) -> dict | None:
    titres = b.valeur("5.1") or []
    sources = b.valeur("5.2") or {}
    if not titres:
        return None
    unite_id = next(r["id"] for r in roles if r["fonction"] == "unite")
    colonnes = []
    for t in titres:
        t = str(t)
        d = sources.get(t)
        d = d if isinstance(d, dict) else {"source": d}
        col: dict[str, Any] = {"titre": t, "source": str(d.get("source") or "")}
        if d.get("qualifie_par"):
            col["qualifie_par"] = str(d["qualifie_par"])
        if d.get("table"):
            col["table"] = dict(d["table"])
        colonnes.append(col)
    return {
        "porte_par": [unite_id],
        "vide": str(b.valeur("5.3") or "—"),
        "balises": list(BALISES_BANDEAU),
        "position": "juste sous le titre H1 ; une page sans H1 est SAUTÉE et "
                    "signalée, jamais devinée",
        "porte_le_resume": True,
        "regle_dure": "Une cellule sans source dans le frontmatter affiche "
                      "`vide`, JAMAIS une valeur plausible. Une fiche vide "
                      "honnêtement vaut mieux qu'une fiche remplie au juge.",
        "echappement": "`|` est échappé dans une cellule.",
        "colonnes": colonnes,
        "motif": f"{len(colonnes)} faits, pas plus. Le bandeau existe PARCE QUE "
                 f"trop de propriétés poussent le texte sous la ligne de "
                 f"flottaison ; au-delà de cinq colonnes l'entretien redemande, "
                 f"et il refuse une colonne sans champ source.",
    }


# --------------------------------------------------------------------------- #
#  Les dix regles, et le socle
# --------------------------------------------------------------------------- #
def _les_dix(b: Brouillon, m: dict) -> list[dict]:
    """Les dix, TOUTES en `a_mesurer`. L entretien ne sait pas ecrire `dure`."""
    unite = next(r for r in m["roles"] if r["fonction"] == "unite")
    corps = unite.get("corps") or []
    genres = {s["genre"] for s in corps}
    listes = [s["titre"] for s in corps if s["genre"] == "liste_liens"]
    decisions = [s for s in corps if s["genre"] == "decision"]
    etiquetees = [s["titre"] for s in corps if s["genre"] == "etiquetee"]
    liens = _champs_de_liens(b)
    resume = _resume(b)

    modes = {}
    for L in liens:
        if L["mode"] == "symetrique":
            modes[L["champ"]] = "symetrique"
        elif L["mode"] == "inverse":
            modes[L["champ"]] = "inverse"
            modes[L["inverse"]] = "inverse"

    dix = [
        {"id": "reciprocite",
         "enonce": "Si A cite B dans un champ à réciprocité, B cite A — ou son "
                   "inverse déclaré.",
         "active": bool(modes), "severite": "a_mesurer",
         "champs": list(modes), "modes": modes},
        {"id": "chemin_categorie",
         "enonce": "Le dossier d'une page correspond à sa valeur de l'axe de "
                   "rangement.",
         "active": True, "severite": "a_mesurer", "structurellement_dure": False,
         "motif": "Une violation y est une incohérence de STRUCTURE, pas un "
                  "défaut de rédaction : elle se livrerait volontiers dure. Le "
                  "point n'est pas tranché, donc elle sort en `a_mesurer` comme "
                  "les neuf autres — porter une sévérité, c'est porter une "
                  "mesure qu'on n'a pas faite."},
        {"id": "completude_du_hub",
         "enonce": "Toute page d'un rôle `apparait_dans_le_hub` présente dans le "
                   "dossier apparaît dans le hub du dossier.",
         "active": True, "severite": "a_mesurer",
         "roles": [r["id"] for r in m["roles"] if r.get("apparait_dans_le_hub")]},
        {"id": "voisinage_declare",
         "enonce": "Une page dont le dossier porte d'autres pages du même rôle "
                   "et dont le champ de voisinage est vide est signalée.",
         "active": False, "severite": "a_mesurer",
         "motif": "DÉSACTIVÉE au démarrage : personne n'a mesuré si, dans ce "
                  "brain, l'absence de voisin est l'exception ou la norme. La "
                  "signaler avant de le savoir produirait du bruit, et du bruit "
                  "au premier jour est ce qui fait ignorer un validateur pour "
                  "toujours."},
        {"id": "redirection_sourcee",
         "enonce": "Une cellule de la colonne négative qui REDIRIGE — qui porte "
                   "une flèche — et dont la cible est une page fichée porte le "
                   "wikilink de cette page.",
         "active": bool(decisions), "severite": "a_mesurer",
         "sections": [s["titre"] for s in decisions],
         "colonne": decisions[0]["colonne_negative"] if decisions else "",
         "marqueur": "→|->",
         "condition": "la cible est une page fichée"},
        {"id": "reinjection_du_resume",
         "enonce": "Chaque puce d'une section de liste de liens adossée à un "
                   "champ commence par le résumé COURANT de sa cible.",
         "active": bool(listes) and bool(resume), "severite": "a_mesurer",
         "champ_resume": resume,
         "sections": [s["titre"] for s in corps
                      if s["genre"] == "liste_liens" and s.get("champ")]},
        {"id": "etiquettes_fermees",
         "enonce": "Une section déclarée `genre: etiquetee` a un vocabulaire "
                   "FERMÉ.",
         "active": bool(etiquetees), "severite": "a_mesurer",
         "sections": etiquetees},
        {"id": "citation_unique",
         "enonce": "Une même cible ne se LISTE pas dans deux sections de liste "
                   "de liens.",
         "active": len(listes) >= 2, "severite": "a_mesurer",
         "sections": listes,
         "definition_de_liste": "entrée de puce, pas lien cité dans une phrase",
         "motif": "La distinction « entrée de puce » contre « lien cité dans une "
                  "phrase » n'est pas un détail : sans elle, la règle punit la "
                  "forme qu'on recommande."},
        {"id": "bandeau_a_jour",
         "enonce": "La zone AUTO du bandeau concorde avec le frontmatter.",
         "active": "bandeau" in genres, "severite": "a_mesurer",
         "structurellement_dure": False},
        {"id": "anti_repetition",
         "enonce": "La section de définition ne recontient pas les valeurs "
                   "affichées par le bandeau.",
         "active": False, "severite": "avertissement", "definitif": True,
         "scriptable": False,
         "motif": "NON LIVRÉE, et ce n'est pas un oubli : elle n'est pas "
                  "scriptable. Les mots des valeurs d'énumération sont aussi les "
                  "mots les plus fréquents du corpus, donc elle signalerait "
                  "surtout des faux positifs. Proposée comme relecture assistée "
                  "optionnelle, et rien de plus."},
    ]
    return dix


def _le_socle() -> list[dict]:
    return [
        {"id": "frontmatter_lisible", "severite": "dure",
         "enonce": "Un frontmatter illisible est une ERREUR, jamais une absence.",
         "motif": "La SEULE règle que le kit livre dure sans mesure, et ce n'est "
                  "pas une exception au principe : ce n'est pas une règle à "
                  "durcir, c'est l'absence de règle qu'on comble. Une page qui "
                  "ne parse pas sortait du total et de TOUTES les autres règles "
                  "— le vault restait vert en mentant."},
        {"id": "gabarit_par_role", "severite": "dure",
         "enonce": "`role:` inconnu ou absent refusé ; champs requis non vides ; "
                   "tout champ hors de `autorises` échoue."},
        {"id": "liens_resolus", "severite": "a_mesurer",
         "enonce": "Aucun wikilink mort, dans le corps ET dans le frontmatter."},
        {"id": "nom_egal_fichier", "severite": "a_mesurer",
         "enonce": "`nom:` identique au nom du fichier, sauf caractère illégal "
                   "en nom de fichier."},
        {"id": "page_atteignable", "severite": "a_mesurer",
         "enonce": "Toute page atteignable depuis un hub."},
        {"id": "hub_par_niveau", "severite": "dure",
         "enonce": "TOUT niveau du chemin porte son hub, pas seulement la "
                   "feuille."},
        {"id": "vocabulaire_ferme", "severite": "dure",
         "enonce": "Toute valeur d'un champ `enum` ou `liste_enum` appartient au "
                   "vocabulaire déclaré de son axe."},
        {"id": "unicite_du_nom_de_fichier", "severite": "dure",
         "enonce": "Un nom de fichier est unique dans le vault, à la casse près.",
         "motif": "La seule contrainte que le wikilink NU impose. À vérifier "
                  "AVANT de créer chaque page et chaque hub : un dossier, son "
                  "hub et une page peuvent vouloir le même nom."},
        {"id": "taille_avertissement", "severite": "a_mesurer",
         "enonce": "Une page au-delà de `roles[].taille_avertissement` lignes "
                   "suggère une scission."},
        {"id": "collision_alias", "severite": "a_mesurer",
         "enonce": "Doublon interne d'alias, ou alias qui est le `nom:` d'une "
                   "autre page du MÊME rôle."},
        {"id": "couverture_des_vues", "severite": "a_mesurer",
         "enonce": "Une valeur de l'axe de rangement assez peuplée sans vue."},
        {"id": "paire_inverse_bien_declaree", "severite": "dure",
         "enonce": "Un champ `reciproque: {mode: inverse, champ: Y}` exige que Y "
                   "déclare `reciproque: {mode: inverse, champ: X}`.",
         "motif": "Dure d'emblée, pour la même raison que `frontmatter_lisible` : "
                  "ce n'est pas une règle à durcir, c'est un trou à ne pas "
                  "ouvrir. Elle se vérifie sur le MANIFESTE, sans lire une page."},
    ]


# --------------------------------------------------------------------------- #
def _vocabulaires(b: Brouillon, axe_r: dict) -> dict:
    mode = str(b.valeur("9.1") or "ferme")
    dossier = induction.cle(axe_r["p"]) or "general"
    return {
        "tags": {
            "fichier": "Documentation/general/tags.md",
            "mode": mode if mode in ("ferme", "propose", "libre") else "ferme",
            "lecture": LECTURE_TAGS,
            "regle": "Le skill pioche, il n'invente JAMAIS. Un tag manquant se "
                     "propose, s'ajoute ici, puis s'utilise.",
            "vide": True,
            "motif_vide": "L'entretien laisse le fichier VIDE avec sa règle. Les "
                          "tags d'un autre brain sont ceux d'un autre sujet ; la "
                          "règle, elle, est générique.",
        },
        "taxonomie": {
            "fichier": f"Documentation/{dossier}/taxonomie.md",
            "mode": "ferme",
            "genere": True,
            "motif": "GÉNÉRÉ depuis `axes`, avec les places VIDES pour les "
                     "départages et les frontières. Le relire comme une source "
                     "recréerait le défaut que le manifeste supprime : deux "
                     "sources décrivant la même chose, dont l'une prend du "
                     "retard.",
        },
    }


def _graphe(roles: list[dict], axes: dict) -> dict:
    ordre = []
    for r in roles:
        if r.get("hub_de_ralliement"):
            ordre.append({"requete": f"path:{r['hub_de_ralliement']['dossier']}/",
                          "couleur": r["couleur"], "rgb": _rgb(r["couleur"])})
    for t in axes.get("transverses") or []:
        ordre.append({"requete": f"path:{t['dossier']}/",
                      "couleur": PALETTE["transverse"],
                      "rgb": _rgb(PALETTE["transverse"])})
    for r in roles:
        ordre.append({"requete": f'["role":"{r["id"]}"]', "couleur": r["couleur"],
                      "rgb": _rgb(r["couleur"])})
    return {
        "cible": ".obsidian/graph.json, clé `colorGroups`",
        "versionne": False,
        "motif_non_versionne": "Gitignoré : cette table est la seule source, à "
                               "réappliquer par poste. C'est une étape "
                               "d'installation, pas un fichier.",
        "motif_de_l_ordre": "Une requête `path:` passe AVANT une requête "
                            "`role:`, sinon un hub spécial prend la couleur des "
                            "hubs ordinaires.",
        "ordre": ordre,
        "note_base": "Un fichier de vue embarquée NE SE COLORE PAS : il n'a pas "
                     "de frontmatter, donc pas de `role:`.",
    }


def _genere(b: Brouillon, m: dict, axe_r: dict) -> dict:
    agent = "AI"
    chemins = [
        {"chemin": f"{agent}/index/", "par": "build_index"},
        {"chemin": "zones AUTO des hubs", "par": "build_mocs"},
    ]
    for t in m["axes"].get("transverses") or []:
        chemins.append({"chemin": f"{t['dossier']}/", "par": "build_mocs",
                        "depuis": f"axes.transverses[{t['champ']}]"})
    for r in m["roles"]:
        ral = r.get("hub_de_ralliement")
        if ral:
            chemins.append({"chemin": f"{ral['dossier']}/{ral['dossier']}.md",
                            "par": "build_mocs"})
    chemins += [
        {"chemin": f"{agent}/index/liens.md", "par": "build_links"},
        {"chemin": "bandeaux des pages d'unité", "par": "build_bandeau"},
        {"chemin": m["vocabulaires"]["taxonomie"]["fichier"], "par": "kit",
         "depuis": "axes"},
        {"chemin": "Templates/", "par": "kit",
         "depuis": "roles[].champs et roles[].corps"},
    ]
    non_pages = [".git", ".claude", ".obsidian", agent, "Documentation",
                 "Templates", "docs"]
    for d in (b.valeur("9.6") or []):
        chemin = str((d or {}).get("chemin") or "").strip("/")
        if chemin:
            non_pages.append(chemin.split("/")[0])
    champs_index = [c for c in m["champs"]
                    if c not in ("role", "url")] + ["role"]
    return {
        "chemins": chemins,
        "contrat": "Zone à balises dédiées, remplacement en bloc, idempotence, "
                   "`--check` en code 2, préservation de la zone manuelle. Ce "
                   "qui est généré n'est jamais édité à la main.",
        "non_pages": sorted(set(non_pages)),
        "index": {
            "fichiers": [f"{agent}/index/brain-index.json",
                         f"{agent}/index/brain-index.md"],
            "champs": champs_index,
            "plus": ["path"],
            "tri": "stable",
            "horodatage": False,
        },
        "liens": {
            "fichier": f"{agent}/index/liens.md",
            "sections": ["tags", "liens_sortants", "backlinks", "a_creer"],
            "masque_du_graphe": True,
        },
    }


def _propagation(m: dict, unite: dict, notion_id: str | None,
                 vue_id: str | None) -> dict:
    """L enonce et la clause. PAS la table — elle se DERIVE.

    ARBITRAGE DU LOT 8, remontee 2 du lot 7. Le schema rendait `table:`
    obligatoire et ce composeur l ecrivait, pendant que le lot 7 la DERIVAIT
    depuis les roles et les axes. Deux sources de la meme information, et elles
    divergeaient deja en longueur : sept lignes declarees contre neuf derivees
    pour HistoBrain, parce que la declaration repliait les deux axes transverses
    en une ligne et enfouissait le hub de ralliement.

    C est exactement le constat E4 que le manifeste existe pour supprimer. La
    declaration est donc RETIREE, et c est la plus simple des deux issues que le
    lot 7 proposait : un champ qu on regenere a chaque composition depuis la
    derivation ne serait pas une source non plus, il serait une copie — avec, en
    plus, le cout de la tenir a jour.

    Ce qui RESTE ici, et qui ne se derive de rien : l ENONCE de la regle et sa
    CLAUSE. Ce sont des phrases, pas des donnees ; c est le seul endroit ou
    elles sont ecrites, et le skill de capture les lit telles quelles.

    Un manifeste ecrit avant l arbitrage porte encore sa table : le schema la
    TOLERE (elle n est plus `required`), le kit ne la lit pas, et `mesurer` la
    confronte a la derivation sous le code `E4` de son backlog.
    """
    return {
        "enonce": "Le rayon de propagation d'une insertion est le DOSSIER "
                  "D'ACCUEIL, plus ses HUBS PARENTS. Le voisinage d'une page est "
                  "`ls` de son dossier.",
        "clause": "Une ligne sans objet se DÉCLARE sans objet, elle ne se tait "
                  "pas.",
        "derivee": True,
        "motif": "DÉRIVÉE des rôles et des axes : rien à écrire à la main, et "
                 "rien à écrire ICI. Elle ne dépend que d'un fait structurel — "
                 "le dossier porte la valeur de l'axe de rangement — donc tout "
                 "brain construit sur l'arbre l'obtient gratuitement.",
        "motif_sans_table": "Lot 8 : `table:` retirée. Une information déclarée "
                            "ici ET dérivée par le kit est une seconde source, "
                            "c'est-à-dire le constat E4. La table se lit dans le "
                            "skill de capture, qui la dérive.",
    }


def _skills(b: Brouillon, m: dict) -> dict:
    nom = induction.cle(m["brain"]["nom"]) or "brain"
    skills: dict[str, Any] = {
        "capture": {
            "nom": f"enrichir-{nom}",
            "ecrit_dans_le_brain": True,
            "mode_lot": True,
            "motif_mode_lot": "Un brain neuf en a besoin : sans lui, l'amorçage "
                              "coûte une conversation par page et personne ne le "
                              "fera. Les titres cités en 2.1 sont son premier "
                              "backlog — du travail déjà identifié, et pas une "
                              "page écrite.",
            "porte": ["la règle de propagation, dérivée",
                      "le mode mise à jour et sa table des effets de bord",
                      "la vérification de la réinjection du résumé"],
        },
        "cloture": {
            "nom": f"cloturer-{nom}",
            "ecrit_dans_le_brain": False,
            "etapes": ["régénérer les artefacts dérivés",
                       "passer les DEUX validateurs au vert",
                       "vérifier la divergence avec la branche distante AVANT "
                       "tout commit",
                       "committer et intégrer en fast-forward"],
        },
    }
    livrable_brut = b.valeur("10.1")
    livrable = str((livrable_brut or {}).get("livrable")
                   if isinstance(livrable_brut, dict) else
                   (livrable_brut or "")).strip()
    formes = b.valeur("10.2") or []
    if livrable:
        # Le NOM du skill se dérive du nom du brain, comme les deux autres —
        # `enrichir-x`, `cloturer-x`, `exploiter-x`. Un nom tiré des mots du
        # livrable donnerait « produire-une », et un nom inventé serait pire.
        # L'utilisateur peut le nommer lui-même en répondant `nom:` à 10.1.
        propose = (livrable_brut or {}).get("nom") \
            if isinstance(livrable_brut, dict) else None
        skills["exploitation"] = {
            "nom": str(propose or f"exploiter-{nom}"),
            "ecrit_dans_le_brain": False,
            "livrable": livrable,
            "archetypes": (" · ".join(str(x) for x in formes)
                           if isinstance(formes, list) and formes else
                           "aucun archétype au démarrage — zéro est légal, et "
                           "ils s'écriront quand un livrable se répétera"),
            "filtre_eliminatoire": None,
            "motif_filtre_nul": "Aucun champ ne DISQUALIFIE une page dans ce "
                                "brain, et c'est déclaré plutôt que supposé : le "
                                "kit n'a aucune intuition sur « quelle valeur "
                                "élimine ».",
            "forme": "Identifier l'usage -> poser SEULEMENT les questions "
                     "pertinentes -> interroger l'index -> produire un livrable "
                     "SOURCÉ qui contraint l'aval.",
            "questions": " · ".join(str(x) for x in (b.valeur("10.3") or [])),
        }
    else:
        skills["motif"] = ("Deux skills, pas trois : la question 10.1 n'a pas de "
                           "réponse, donc le skill d'exploitation n'est pas "
                           "généré. Mieux vaut deux skills que trois dont un "
                           "inventé.")
    return skills


def _agent() -> dict:
    return {
        "racine": "AI/",
        "sous": [
            {"chemin": "design/", "role": "les spécifications de référence"},
            {"chemin": "migration/",
             "role": "un fichier par lot, avec ses *Remontées* — le premier est "
                     "écrit VIDE par le semis"},
            {"chemin": "index/", "role": "généré, ne pas éditer à la main"},
            {"chemin": "entretien/",
             "role": "le brouillon de l'entretien qui a produit ce brain — les "
                     "questions et les réponses, pour qu'on sache POURQUOI la "
                     "taxonomie est celle-là"},
            {"chemin": "sessions/", "role": "résumés automatiques par le hook Stop"},
            {"chemin": "scripts/", "role": "vide sur une instance `kit.mode: branche`"},
            {"chemin": "backlog.md", "role": "ce qui reste à faire"},
        ],
        "hook_stop": "écrit un résumé de session dans AI/sessions/",
    }


def _racine(b: Brouillon, unite: dict) -> dict:
    d = b.valeur("9.5")
    amorce = [f"{unite['s']} : {t}" for t in (b.valeur("2.1") or [])]
    if isinstance(d, dict) and d.get("pages"):
        pages = []
        for p in d["pages"]:
            e = {"fichier": str(p.get("fichier")), "titre": str(p.get("titre")),
                 "aiguille": bool(p.get("aiguille")),
                 "role_editorial": str(p.get("role_editorial") or "note")}
            if e["role_editorial"] == "capture":
                e["amorce"] = amorce
            pages.append(e)
        porte = str(d.get("porte_d_entree") or pages[0]["fichier"])
    else:
        pages = [
            {"fichier": "Home.md", "titre": "Accueil", "aiguille": True,
             "role_editorial": "porte",
             "motif": "La seule page qui cite les hubs de premier niveau. Sans "
                      "elle, ils sont « atteignables depuis aucun hub »."},
            {"fichier": "Inbox.md", "titre": "Inbox", "aiguille": False,
             "role_editorial": "capture",
             "motif": "À la racine, mais elle n'aiguille PAS : une page qu'elle "
                      "mentionne ne devient pas atteignable pour autant. C'est "
                      "exactement ce que `aiguille:` existe pour porter.",
             "amorce": amorce},
        ]
        porte = "Home.md"
    bloc: dict[str, Any] = {"porte_d_entree": porte, "pages": pages}
    dossiers = []
    for x in (b.valeur("9.6") or []):
        if isinstance(x, dict) and x.get("chemin"):
            dossiers.append({"chemin": str(x["chemin"]).rstrip("/") + "/",
                             "role_editorial": str(x.get("role_editorial")
                                                   or "atelier"),
                             "motif": str(x.get("motif") or "")})
    if dossiers:
        bloc["dossiers"] = dossiers
    return bloc


def _frontieres(b: Brouillon, roles: list[dict]) -> dict:
    proteges = [r for r in roles if r.get("protege")]
    suppression = str(b.valeur("9.2") or "demander")
    second = b.valeur("9.3")
    f: dict[str, Any] = {
        "libre": ["AI/ hors index/", "Inbox.md"],
        "sur_confirmation": ["toute page d'un rôle non protégé", "Documentation/"],
        "sur_demande_explicite": [
            f"toute page d'un rôle `protege: true` — ici "
            f"{', '.join(r['libelle']['p'] for r in proteges)}"
        ] if proteges else [],
        "jamais_a_la_main": ["les chemins de `genere`"],
        "jamais_sans_accord": (["une suppression de page"]
                               if suppression.startswith("demand") else []),
        "deplacement": "par `git mv`, JAMAIS par suppression + création",
        "second_mode": bool(second) and _est_oui(second),
    }
    if not f["second_mode"]:
        f["motif_second_mode"] = (
            "Réponse « non » à 9.3, et elle est légale : un second mode ne se "
            "génère que si le brain a un consommateur qui vit ailleurs.")
    return f
