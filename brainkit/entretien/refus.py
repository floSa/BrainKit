"""refus.py — les TREIZE refus de deviner, en liste FERMEE et en controles.

`00-cadrage.md` §3.5 les enumere, et dit pourquoi ils sont ecrits comme une
liste fermee : *c est la partie du skill qui se degrade le plus vite si elle
n est pas ecrite comme une liste fermee*. Une consigne en prose se dilue — au
bout de trois conversations, « ne devine pas le seuil » devient « propose un
seuil raisonnable ». Ici chaque refus porte un CONTROLE, et le controle tourne
sur le brouillon et sur le manifeste compose. Ce qui n est pas controlable
mecaniquement est marque comme tel, plutot que d etre affirme.

# Le refus n° 1 est d une autre nature que les douze autres

Les douze autres protegent la QUALITE du manifeste : une valeur inventee y
serait une faute reparable. Le premier protege une signature : une adresse
inventee entre dans l historique d un depot, et elle n en sort pas sans
reecriture. C est le seul refus qui ARRETE l entretien, et il porte TROIS
filets, parce qu un seul a deja lache :

  1. la PROVENANCE — une reponse dont la provenance n est pas `utilisateur` est
     refusee ; `harnais` est nomme explicitement dans la liste des provenances
     interdites, parce que c est celle-la qui se presente ;
  2. le DOMAINE — l identite ne peut pas porter un domaine que la question 0.5
     vient de nommer comme interdit ; c est exactement l accident qu on protege
     (l adresse pro annoncee par le harnais est celle que 0.5 nomme) ;
  3. l ENVIRONNEMENT — l identite ne peut pas etre egale a une valeur trouvee
     dans `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_EMAIL` ou `EMAIL`, ni au
     `user.email` de la config git GLOBALE de la machine.

Le troisieme filet a l air paranoiaque. Il ne l est pas : c est la seule facon
de distinguer « l utilisateur a repondu cette adresse » de « quelque chose l a
lue quelque part et l a recopiee », quand la provenance, elle, se declare.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from typing import Any, Callable

#: Les provenances qu une reponse peut porter. Une seule est acceptee.
PROVENANCE_VALIDE = "utilisateur"
PROVENANCES_INTERDITES = ("harnais", "environnement", "git-global", "devine",
                          "kit", "exemple")

#: Les mots que le kit ne connait QUE parce qu il a lu le DevBrain. Ils ne
#: sortent jamais de la bouche de l entretien. Un utilisateur qui les emploie
#: de lui-meme les impose en marquant sa reponse `assume: true` — la sortie de
#: secours est ecrite, elle laisse une trace, et elle est a lui.
LEXIQUE_DU_DEV = ("brique", "briques", "comparatif", "comparatifs", "pitch",
                  "galaxie", "galaxies", "famille", "familles", "métier",
                  "métiers")


@dataclass(frozen=True)
class Refus:
    n: int
    objet: str                    # ce qu il ne devine jamais
    a_la_place: str               # ce qu il fait
    question: str                 # la question qui l honore
    mecanique: bool               # un controle le verifie-t-il vraiment ?
    controle: Callable[..., list[str]] | None = None


# --------------------------------------------------------------------------- #
# Les controles. Chacun prend (reponses, manifeste) et rend ses griefs.
# `reponses` est le dictionnaire {id: valeur} du brouillon ; `manifeste` est le
# dictionnaire compose, ou None quand le controle tourne AVANT composition.
# --------------------------------------------------------------------------- #
def _valeur(reponses: dict, qid: str) -> Any:
    r = reponses.get(qid)
    return r.get("valeur") if isinstance(r, dict) else r


def _provenance(reponses: dict, qid: str) -> str:
    r = reponses.get(qid)
    return str(r.get("provenance", PROVENANCE_VALIDE)) if isinstance(r, dict) \
        else PROVENANCE_VALIDE


def _email_global() -> str:
    try:
        p = subprocess.run(["git", "config", "--global", "user.email"],
                           capture_output=True, text=True, timeout=5)
        return p.stdout.strip()
    except Exception:                                   # pragma: no cover
        return ""


def _c1_identite(reponses: dict, manifeste: dict | None = None) -> list[str]:
    """Refus n° 1 — l identite git, et ses trois filets."""
    r: list[str] = []
    val = _valeur(reponses, "0.4")
    if not isinstance(val, dict) or not str(val.get("name") or "").strip() \
            or not str(val.get("email") or "").strip():
        return ["0.4 sans réponse — l'entretien S'ARRÊTE. L'identité d'un dépôt "
                "ne se devine sous aucune forme, et surtout pas depuis l'adresse "
                "annoncée par le harnais. Rien n'est semé."]

    prov = _provenance(reponses, "0.4")
    if prov != PROVENANCE_VALIDE:
        r.append(f"0.4 porte la provenance `{prov}` — refusée. Seule "
                 f"`{PROVENANCE_VALIDE}` vaut : une identité lue ailleurs "
                 f"qu'auprès de l'utilisateur n'est pas une réponse.")

    email = str(val["email"]).strip().lower()
    refuses = _valeur(reponses, "0.5") or []
    if isinstance(refuses, str):
        refuses = [refuses]
    for d in refuses:
        d = str(d).strip().lower().lstrip("@")
        if d and (email.endswith("@" + d) or email == d):
            r.append(f"l'identité `{email}` porte le domaine `{d}`, que la "
                     f"question 0.5 vient de nommer comme INTERDIT ici. C'est "
                     f"exactement l'accident que le refus n° 1 protège.")

    trouvees = {n: os.environ.get(n, "").strip().lower()
                for n in ("GIT_AUTHOR_EMAIL", "GIT_COMMITTER_EMAIL", "EMAIL")}
    trouvees["git config --global user.email"] = _email_global().lower()
    for source, v in trouvees.items():
        if v and v == email:
            r.append(f"l'identité `{email}` est exactement la valeur de "
                     f"`{source}` — refusée. Une adresse que l'environnement "
                     f"portait déjà n'est pas une réponse de l'utilisateur : "
                     f"redemander, et attendre.")
    return r


def _c2_unite(reponses: dict, manifeste: dict | None = None) -> list[str]:
    r: list[str] = []
    val = _valeur(reponses, "1.2")
    if not isinstance(val, dict) or not val.get("s") or not val.get("p"):
        return ["1.2 sans réponse — le nom de l'unité ne se traduit pas depuis "
                "le dev, il se demande au singulier et au pluriel."]
    if val.get("assume"):
        return r
    for mot in (str(val["s"]), str(val["p"])):
        if mot.strip().lower() in LEXIQUE_DU_DEV:
            r.append(f"« {mot} » appartient au lexique que le kit ne connaît que "
                     f"pour avoir lu le DevBrain. Si c'est bien le mot de "
                     f"l'utilisateur, marquer la réponse `assume: true` — la "
                     f"sortie de secours laisse une trace, et elle est à lui.")
    return r


def _c3_paquets(reponses: dict, manifeste: dict | None = None) -> list[str]:
    r: list[str] = []
    titres = _valeur(reponses, "2.1") or []
    if len(titres) < 10:
        r.append(f"2.1 : {len(titres)} titre(s) cité(s). Sous DIX, l'induction "
                 f"ne tient pas — redemander, et attendre. Ne JAMAIS proposer "
                 f"les titres soi-même.")
    paquets = _valeur(reponses, "2.2") or {}
    if not paquets:
        r.append("2.2 sans réponse — les paquets se rangent DE LA MAIN de "
                 "l'utilisateur. Jamais de liste à cocher : on coche par "
                 "politesse, et le brain hérite d'une taxonomie qui n'est pas "
                 "la sienne.")
    return r


def _c4_seuil(reponses: dict, manifeste: dict | None = None) -> list[str]:
    r: list[str] = []
    if _valeur(reponses, "2.6") in (None, "", 0):
        r.append("2.6 sans réponse — le volume cible est la SEULE entrée du "
                 "seuil. Demander le seuil directement est le refus n° 4 : "
                 "l'utilisateur n'a aucun moyen de le connaître.")
    if manifeste is None:
        return r
    rang = (manifeste.get("axes") or {}).get("rangement") or {}
    if rang.get("seuil_promotion") and not str(rang.get("motif_seuil") or "").strip():
        r.append("`seuil_promotion` est écrit sans `motif_seuil` — le calcul "
                 "s'écrit, sinon le nombre est tombé du ciel.")
    return r


def _c5_ordre(reponses: dict, manifeste: dict | None = None) -> list[str]:
    r: list[str] = []
    for qid, quoi in (("2.7", "l'axe de rangement"), ("3.3", "l'axe de nature")):
        val = _valeur(reponses, qid)
        if val is None:
            continue
        if isinstance(val, dict) and not val.get("ordre_de_l_utilisateur"):
            r.append(f"{qid} : l'arbre de décision de {quoi} est proposé sans "
                     f"que l'ORDRE vienne de l'utilisateur. L'IA peut proposer "
                     f"les questions, jamais leur rang — l'ordre EST la décision "
                     f"de conception.")
    return r


def _c6_severites(reponses: dict, manifeste: dict | None = None) -> list[str]:
    if manifeste is None:
        return []
    r: list[str] = []
    for regle in manifeste.get("regles") or []:
        sev = (regle or {}).get("severite")
        if sev != "a_mesurer" and (regle or {}).get("active", True):
            r.append(f"la règle `{regle.get('id')}` sort en `{sev}` — l'entretien "
                     f"ne sait pas écrire autre chose que `a_mesurer`. Porter une "
                     f"sévérité, c'est porter une mesure qu'on n'a pas faite.")
    return r


def _c7_tags(reponses: dict, manifeste: dict | None = None) -> list[str]:
    if manifeste is None:
        return []
    tags = ((manifeste.get("vocabulaires") or {}).get("tags") or {})
    if tags and not tags.get("vide"):
        return ["le vocabulaire de tags ne naît pas `vide: true` — l'entretien "
                "laisse le fichier VIDE avec sa règle. Les tags d'un autre brain "
                "sont ceux d'un autre sujet."]
    return []


def _c8_nature_vide(reponses: dict, manifeste: dict | None = None) -> list[str]:
    if manifeste is None:
        return []
    nature = (manifeste.get("axes") or {}).get("nature")
    if nature and not nature.get("vide_autorise"):
        return ["`axes.nature.vide_autorise` n'est pas vrai — un champ vide est "
                "le SEUL signal prévu pour « l'arbre n'a pas tranché ». Une "
                "valeur inventée est une faute, un champ vide est une question "
                "ouverte."]
    return []


def _c9_vue(reponses: dict, manifeste: dict | None = None) -> list[str]:
    if manifeste is None:
        return []
    a_une_vue = any((x or {}).get("fonction") == "vue"
                    for x in manifeste.get("roles") or [])
    voulue = bool(_valeur(reponses, "8.1")) or bool(_valeur(reponses, "8.2"))
    if a_une_vue and not voulue:
        return ["un rôle `fonction: vue` existe alors que ni 8.1 ni 8.2 ne l'ont "
                "demandé — c'est le comparatif traduit par réflexe, refus n° 9."]
    return []


def _c10_transverse(reponses: dict, manifeste: dict | None = None) -> list[str]:
    if manifeste is None:
        return []
    declares = (manifeste.get("axes") or {}).get("transverses") or []
    demandes = _valeur(reponses, "4.1") or []
    if len(declares) > len(demandes):
        return [f"{len(declares)} axe(s) transverse(s) déclaré(s) pour "
                f"{len(demandes)} demandé(s) en 4.1 — zéro est une réponse, et "
                f"aucun axe ne se crée par analogie avec un autre brain."]
    return []


def _c11_listes_vides(reponses: dict, manifeste: dict | None = None) -> list[str]:
    if manifeste is None:
        return []
    r: list[str] = []
    axes = manifeste.get("axes") or {}
    for nom in ("rangement", "nature"):
        axe = axes.get(nom) or {}
        for liste in ("departages", "frontieres"):
            if axe.get(liste):
                r.append(f"`axes.{nom}.{liste}` n'est pas vide — ces listes se "
                         f"remplissent page par page, quand un arbitrage se "
                         f"répète. Les remplir maintenant serait inventer des "
                         f"problèmes qu'on n'a pas.")
    return r


def _c12_bandeau(reponses: dict, manifeste: dict | None = None) -> list[str]:
    if manifeste is None:
        return []
    r: list[str] = []
    bandeau = manifeste.get("bandeau") or {}
    champs = set(manifeste.get("champs") or {})
    for col in bandeau.get("colonnes") or []:
        col = col or {}
        src = col.get("source")
        if not src:
            r.append(f"la colonne « {col.get('titre')} » n'a pas de `source:` — "
                     f"une colonne dérivée d'un jugement, et non d'un champ, "
                     f"n'entre pas dans le bandeau.")
        elif src not in champs:
            r.append(f"la colonne « {col.get('titre')} » cite le champ `{src}`, "
                     f"absent du dictionnaire de champs.")
    if len(bandeau.get("colonnes") or []) > 5:
        r.append(f"{len(bandeau['colonnes'])} colonnes de bandeau — au-delà de "
                 f"cinq, redemander : le bandeau existe PARCE QUE dix-huit "
                 f"propriétés poussaient le texte sous la ligne de flottaison.")
    return r


def _c13_exploitation(reponses: dict, manifeste: dict | None = None) -> list[str]:
    if manifeste is None:
        return []
    expl = (manifeste.get("skills") or {}).get("exploitation")
    if expl and not str(_valeur(reponses, "10.1") or "").strip():
        return ["un skill d'exploitation est déclaré sans que 10.1 ait de "
                "réponse — sans livrable nommé, le skill n'est pas généré. "
                "Mieux vaut deux skills que trois dont un inventé."]
    return []


# --------------------------------------------------------------------------- #
LES_TREIZE: tuple[Refus, ...] = (
    Refus(1, "L'identité git, sous aucune forme",
          "Redemande, et S'ARRÊTE si la réponse ne vient pas. Ne lit JAMAIS "
          "l'adresse annoncée par le harnais.",
          "0.4", True, _c1_identite),
    Refus(2, "Le nom de l'unité et la liste des rôles",
          "Fait décrire l'usage (1.1) et reprend les mots de l'utilisateur.",
          "1.1 / 1.2", True, _c2_unite),
    Refus(3, "Les paquets de l'axe de rangement",
          "Fait citer vingt pages réelles et les fait ranger à la main. Jamais "
          "de liste à cocher.",
          "2.1 / 2.2", True, _c3_paquets),
    Refus(4, "Le seuil de promotion",
          "Demande le volume cible et DÉRIVE, en écrivant le calcul dans "
          "`motif_seuil`.",
          "2.6", True, _c4_seuil),
    Refus(5, "L'ordre des arbres de décision",
          "Peut proposer les questions ; l'ordre reste à l'utilisateur, et "
          "l'entretien l'annonce comme LA décision de conception.",
          "2.7 / 3.3", True, _c5_ordre),
    Refus(6, "Toute sévérité de règle",
          "Écrit `a_mesurer` partout. Ne sait pas écrire `dure`.",
          "(aucune — c'est une invariante)", True, _c6_severites),
    Refus(7, "Le vocabulaire de tags",
          "Laisse le fichier vide avec sa règle.",
          "9.1", True, _c7_tags),
    Refus(8, "Une valeur de l'axe de nature quand l'arbre ne tranche pas",
          "Laisse le champ vide — c'est le signal prévu — et le dit.",
          "3.2", True, _c8_nature_vide),
    Refus(9, "L'existence d'un rôle `vue`",
          "Passe 8. Si les unités ne sont pas interchangeables, ne traduit pas "
          "le comparatif.",
          "8.1 / 8.2", True, _c9_vue),
    Refus(10, "L'existence d'un axe transverse",
          "Zéro est une réponse. Ne crée aucun dossier par analogie.",
          "4.1", True, _c10_transverse),
    Refus(11, "Les règles de départage et les frontières",
          "Les laisse vides, et dit qu'elles se rempliront page par page.",
          "(aucune — c'est une invariante)", True, _c11_listes_vides),
    Refus(12, "Une colonne de bandeau sans champ source",
          "Refuse la colonne et redemande d'où vient le fait.",
          "5.2", True, _c12_bandeau),
    Refus(13, "Le livrable du skill d'exploitation",
          "Passe 10.1. Sans réponse, le skill n'est pas généré.",
          "10.1", True, _c13_exploitation),
)


def controle(reponses: dict, manifeste: dict | None = None) -> list[tuple[int, str]]:
    """Tous les refus, d un coup. Rend [(n° du refus, grief), …]."""
    out: list[tuple[int, str]] = []
    for r in LES_TREIZE:
        if r.controle is None:
            continue
        for grief in r.controle(reponses, manifeste):
            out.append((r.n, grief))
    return out


def arret(reponses: dict) -> str | None:
    """Le refus n° 1 seul : ce qui ARRETE l entretien, et rien d autre.

    Rend le motif d arret, ou None. Le semis ne doit PAS etre appele quand
    cette fonction rend quelque chose — c est le controle negatif du lot.
    """
    griefs = _c1_identite(reponses, None)
    if not griefs:
        return None
    return ("ARRÊT — refus n° 1, l'identité git.\n" +
            "\n".join(f"  · {g}" for g in griefs) +
            "\n  Rien n'est composé, rien n'est semé, aucun dépôt n'est créé.")
