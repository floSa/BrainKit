"""induction.py — le coeur difficile : de vingt titres reels a une taxonomie.

# Le probleme, et pourquoi la solution evidente est la mauvaise

L utilisateur ne connait pas sa taxonomie. Il ne sait pas nommer ses domaines,
et si on les lui propose il en cochera — par politesse, par fatigue, parce que
la liste a l air raisonnable. Le brain heritera alors d une taxonomie qui n est
pas la sienne, et il s en apercevra a la trentieme page, quand il ne saura plus
ou ranger.

L entretien fait l inverse : il lui fait citer **vingt pages reelles**, puis il
lui fait **ranger ces vingt de sa main**. La taxonomie n est pas proposee, elle
est LUE dans un geste. Ce module fait la lecture.

Le test a blanc « histoire » l a demontre a la question 2.2 : l utilisateur a
range par PERIODE, spontanement, parce que c est l axe qui EXCLUT — une source
antique n est pas une source moderne — alors que le theme et l espace se
cumulent. Personne n a discute de l axe : le geste l a donne.

# Ce que l induction produit, et ce qu elle REFUSE de produire

| Elle produit | Elle refuse |
|---|---|
| les prefixes, leur cle, leur dossier, leur population dans l echantillon | de nommer un paquet a la place de l utilisateur |
| le seuil de promotion, DERIVE, avec son calcul ecrit | de demander le seuil |
| les QUESTIONS fermees candidates de l arbre de decision | l ORDRE de ces questions |
| les valeurs de l axe de nature, LUES dans l etiquetage de l echantillon | une valeur pour un titre que l utilisateur n a pas etiquete |
| les diagnostics — ce qui deborde, ce qui est trop maigre, ce qui colle | de reparer un diagnostic en silence |

# Ce qu elle fait quand les reponses ne suffisent pas

Elle ne complete pas : elle RENVOIE A UNE QUESTION. Chaque diagnostic porte
l identifiant de la question a reposer et la phrase a dire. C est la difference
entre un entretien et un formulaire — un formulaire accepte un champ vide et
continue ; un entretien y revient.

Quatre insuffisances sont nommees, et chacune a sa reprise :

  · moins de dix titres cites            -> 2.1, on redemande, l induction ne tient pas
  · un titre range nulle part            -> 2.2, on le fait ranger, on ne le jette pas
  · un titre range dans deux paquets     -> 2.3 puis 2.4, l axe n est pas exclusif
  · un paquet a une seule page           -> 2.2, « garder ou fondre » est SA decision
"""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass, field

#: Bornes du seuil derive. En dessous de trois, un « sous-dossier » de deux
#: pages n est pas un rangement ; au-dessus de vingt, plus rien ne se promeut
#: jamais et l arbre reste plat pour toujours.
SEUIL_MIN, SEUIL_MAX = 3, 20


def cle(texte: str) -> str:
    """Un nom de paquet -> une cle de manifeste. Sans accent, sans espace.

    La cle est technique, le DOSSIER garde le nom exact de l utilisateur — y
    compris ses accents et ses majuscules. Confondre les deux ferait ecrire
    « Epoque moderne » sur le disque de quelqu un qui a tape « Époque moderne ».
    """
    plat = unicodedata.normalize("NFKD", texte)
    plat = "".join(c for c in plat if not unicodedata.combining(c))
    plat = re.sub(r"[^A-Za-z0-9]+", "-", plat).strip("-").lower()
    return plat or "sans-nom"


@dataclass
class Diagnostic:
    """Ce que l induction a vu, et la question a reposer pour le regler."""

    question: str          # l id de la question a reposer
    quoi: str              # ce qui ne va pas
    a_dire: str            # la phrase que l entretien prononce
    bloquant: bool = False # composer sans l avoir regle serait une faute

    def rendu(self) -> str:
        marque = "BLOQUANT" if self.bloquant else "à dire"
        return f"[{marque}] ({self.question}) {self.quoi}\n    « {self.a_dire} »"


@dataclass
class Paquets:
    """Le resultat de la lecture du geste de rangement."""

    prefixes: list[dict] = field(default_factory=list)
    exclusif: bool = True
    debordent: dict[str, list[str]] = field(default_factory=dict)
    orphelins: list[str] = field(default_factory=list)
    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def bloquants(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.bloquant]


# --------------------------------------------------------------------------- #
def induis_les_paquets(titres: list[str], paquets: dict[str, list[str]]) -> Paquets:
    """Lit les paquets DANS le geste de rangement. N en propose aucun.

    `paquets` est {nom donne par l utilisateur: [titres]}. L ordre du
    dictionnaire est celui dans lequel il les a nommes, et il est conserve :
    c est souvent l ordre qui a du sens pour lui (chronologique, geographique),
    et le reordonner alphabetiquement serait deja une opinion.
    """
    p = Paquets()

    if len(titres) < 10:
        p.diagnostics.append(Diagnostic(
            "2.1", f"{len(titres)} titre(s) cité(s), il en faut au moins dix",
            "Je n'ai pas assez de matière pour induire quoi que ce soit. "
            "Cite-m'en d'autres — des pages réelles, celles que tu ouvrirais "
            "vraiment. Je ne vais pas les inventer à ta place.",
            bloquant=True))

    vus: dict[str, list[str]] = {}
    for nom, membres in paquets.items():
        for t in membres:
            vus.setdefault(t, []).append(nom)

    p.orphelins = [t for t in titres if t not in vus]
    if p.orphelins:
        p.diagnostics.append(Diagnostic(
            "2.2", f"{len(p.orphelins)} titre(s) rangé(s) nulle part",
            "Ceux-là ne sont dans aucun paquet : " +
            " · ".join(p.orphelins[:5]) +
            (" …" if len(p.orphelins) > 5 else "") +
            ". Où les mets-tu ? S'ils n'entrent nulle part, c'est peut-être "
            "qu'il manque un paquet — et c'est à toi de le nommer.",
            bloquant=True))

    p.debordent = {t: ns for t, ns in vus.items() if len(ns) > 1}
    if p.debordent:
        p.exclusif = False
        p.diagnostics.append(Diagnostic(
            "2.3", f"{len(p.debordent)} titre(s) dans plusieurs paquets",
            "Ces pages débordent : " +
            " · ".join(f"{t} ({', '.join(ns)})"
                       for t, ns in list(p.debordent.items())[:4]) +
            ". Ton axe n'est donc pas exclusif. Pour chacune : est-ce qu'un "
            "paquet DOMINE quand même, ou est-ce qu'elle couvre vraiment tout ? "
            "La différence décide entre une règle de majorité et un paquet "
            "transversal — et je ne la trancherai pas pour toi."))

    for nom, membres in paquets.items():
        uniques = [t for t in membres]
        p.prefixes.append({
            "cle": cle(nom),
            "dossier": nom,
            "portee": "",
            "sous": {},
            "_population": len(uniques),
            "_membres": uniques,
        })
        if len(uniques) <= 1:
            p.diagnostics.append(Diagnostic(
                "2.2", f"le paquet « {nom} » ne tient que par {len(uniques)} page",
                f"« {nom} » n'a qu'une page dans ton échantillon. Un paquet qui "
                f"tient par une seule page n'en est pas encore un. Le garder "
                f"parce que tu sais qu'il se remplira, ou le fondre dans un "
                f"autre : c'est ta décision, pas la mienne."))

    doublons = [c for c in {x["cle"] for x in p.prefixes}
                if sum(1 for x in p.prefixes if x["cle"] == c) > 1]
    for c in doublons:
        noms = [x["dossier"] for x in p.prefixes if x["cle"] == c]
        p.diagnostics.append(Diagnostic(
            "2.2", f"deux paquets donnent la même clé `{c}`",
            f"« {' » et « '.join(noms)} » se réduisent à la même clé technique. "
            f"Renomme l'un des deux — deux dossiers ne peuvent pas porter la "
            f"même valeur de rangement.", bloquant=True))
    return p


# --------------------------------------------------------------------------- #
def derive_le_seuil(volume_cible: int, nb_paquets: int) -> tuple[int, str]:
    """Le seuil de promotion, DERIVE du volume. Jamais demande (refus n° 4).

    La loi : le seuil croît comme la RACINE CUBIQUE de la population d un
    paquet. Un paquet dix fois plus peuple ne veut pas dix fois plus de pages
    par sous-dossier — il en veut environ deux fois plus, sinon l arbre se
    reforme en liste.

        seuil = arrondi( 1.6 x (volume_cible / nb_paquets) ^ (1/3) ),
                borne a [3, 20]

    Elle est CALIBREE sur les deux seuls points qui existent, et le dire est
    plus honnete que de la presenter comme une science :

        le vault d'origine    700 pages /  20 paquets ->  35 par paquet -> 5,2  -> 5  (le seuil reel)
        BrainRef 3000 pages /   8 paquets -> 375 par paquet -> 11,5 -> 12 (le seuil ecrit)

    Deux points ne font pas une loi. C est pour ca que `re-seuiller` existe, et
    c est pour ca que le motif ecrit dans le manifeste dit que le nombre est une
    PROPOSITION mesuree, pas une verite. Un brain qui grandit autrement que
    prevu se re-seuille — c est une migration, elle est outillee, et elle est
    moins couteuse qu un seuil choisi au doigt mouille.
    """
    nb_paquets = max(1, int(nb_paquets))
    par_paquet = max(1.0, float(volume_cible) / nb_paquets)
    brut = 1.6 * (par_paquet ** (1.0 / 3.0))
    seuil = int(max(SEUIL_MIN, min(SEUIL_MAX, math.floor(brut + 0.5))))
    motif = (
        f"DÉRIVÉ du volume cible, jamais tapé à la main (refus n° 4 de "
        f"l'entretien) : {volume_cible} pages visées / {nb_paquets} paquets "
        f"= {par_paquet:.0f} pages par paquet ; seuil = arrondi(1,6 × "
        f"{par_paquet:.0f}^(1/3)) = {brut:.1f} -> {seuil}. La loi en racine "
        f"cubique est calibrée sur les deux seuls points qui existent — "
        f"le vault d'origine (700/20 -> 5) et BrainRef (3000/8 -> 12) — et deux points "
        f"ne font pas une loi. Ce nombre est une PROPOSITION mesurée : si le "
        f"brain grandit autrement, `brainkit re-seuiller` refait l'arbre par "
        f"`git mv`, et c'est pour cela qu'il existe."
    )
    return seuil, motif


# --------------------------------------------------------------------------- #
def propose_les_questions(prefixes: list[dict], libelle_unite: str,
                          libelle_axe: str) -> list[dict]:
    """Une question FERMEE candidate par paquet — et AUCUN ordre.

    Le refus n° 5 est ici, et il est mecanique : chaque entree sort avec
    `n: None`. Le composeur refuse un arbre dont les rangs n ont pas ete
    donnes par l utilisateur, donc cette liste n est pas semable telle quelle.
    L IA a le droit de proposer les questions ; le rang est LA decision de
    conception, et il reste a l utilisateur.
    """
    out: list[dict] = []
    for p in prefixes:
        out.append({
            "n": None,
            "question": f"Cette {libelle_unite} relève-t-elle "
                        f"{_article(p['dossier'])} ?",
            "si_oui": [p["cle"]],
            "_paquet": p["dossier"],
        })
    out.append({
        "n": None,
        "question": "Aucun des précédents",
        "si_oui": [],
        "arret": True,
        "motif": f"ARRÊT — demander. Un(e) {libelle_axe} manquant(e) ne "
                 f"s'invente jamais.",
    })
    return out


def _article(nom: str) -> str:
    """« de la Vanoise », « du Vercors », « des Écrins ». Approximatif, et assumé.

    L entretien FAIT RELIRE la question a l utilisateur : une preposition fausse
    se corrige en une seconde, et proposer une phrase imparfaite vaut mieux que
    de lui demander d ecrire dix questions depuis la page blanche.
    """
    return f"de « {nom} »"


def verifie_l_arbre(arbre: list[dict], prefixes: list[dict]) -> list[Diagnostic]:
    """Un arbre est complet quand il atteint chaque paquet et se termine par un ARRET."""
    d: list[Diagnostic] = []
    cles = {p["cle"] for p in prefixes}
    atteintes: set[str] = set()
    for b in arbre:
        for v in (b or {}).get("si_oui") or []:
            atteintes.add(str(v).split("/")[0])
    manquantes = sorted(cles - atteintes)
    if manquantes:
        d.append(Diagnostic(
            "2.7", f"{len(manquantes)} paquet(s) qu'aucune question n'atteint",
            "Aucune question de ton arbre ne mène à : " +
            ", ".join(manquantes) +
            ". Une page qui devrait y aller tomberait dans le premier paquet "
            "qui la touche. Quelle question fermée l'y envoie, et à quel rang ?",
            bloquant=True))
    if not any((b or {}).get("arret") for b in arbre):
        d.append(Diagnostic(
            "2.7", "l'arbre n'a pas de branche d'ARRÊT",
            "Que fait-on d'une page qu'aucune de tes questions ne classe ? La "
            "dernière branche doit être un arrêt : on demande, on n'invente "
            "pas une valeur.", bloquant=True))
    rangs = [b.get("n") for b in arbre]
    if any(r is None for r in rangs):
        d.append(Diagnostic(
            "2.7", "l'arbre est proposé sans rangs",
            "J'ai écrit les questions ; leur ORDRE est à toi. C'est la seule "
            "décision de conception de ta taxonomie : une page se range à la "
            "PREMIÈRE question qui répond oui, donc l'ordre décide. Numérote-les.",
            bloquant=True))
    return d


# --------------------------------------------------------------------------- #
def induis_les_natures(etiquetes: dict[str, str],
                       titres: list[str]) -> tuple[list[dict], list[Diagnostic]]:
    """Les natures se LISENT dans l etiquetage de l echantillon.

    `etiquetes` est {titre: nature donnee par l utilisateur}. Un titre non
    etiquete n en recoit AUCUNE — c est le refus n° 8, et le champ vide est le
    signal prevu pour « l arbre n a pas tranche ».
    """
    d: list[Diagnostic] = []
    ordre: list[str] = []
    for t in titres:
        v = (etiquetes.get(t) or "").strip()
        if v and v not in ordre:
            ordre.append(v)

    sans = [t for t in titres if not (etiquetes.get(t) or "").strip()]
    if sans:
        d.append(Diagnostic(
            "3.2", f"{len(sans)} titre(s) sans nature",
            "Je laisse leur `nature:` VIDE, et c'est volontaire : un champ vide "
            "est le seul signal prévu pour « on n'a pas tranché ». Une valeur "
            "inventée serait une faute ; un champ vide est une question "
            "ouverte, qui se referme le jour où tu écris la page."))

    valeurs = []
    for v in ordre:
        membres = [t for t in titres if (etiquetes.get(t) or "").strip() == v]
        valeurs.append({"cle": cle(v), "definition": "", "frontiere": "",
                        "_population": len(membres)})
        if len(membres) == 1:
            d.append(Diagnostic(
                "3.2", f"la nature « {v} » ne repose que sur une page",
                f"« {v} » n'apparaît qu'une fois dans ton échantillon. Est-ce "
                f"une vraie nature, ou un cas isolé ? Une valeur d'énumération "
                f"qui ne sert qu'une fois coûte une question dans l'arbre pour "
                f"rien."))
    for v in valeurs:
        if not v["definition"]:
            d.append(Diagnostic(
                "3.2", f"la nature `{v['cle']}` n'a pas de définition",
                f"Comment définis-tu « {v['cle']} », et surtout : qu'est-ce qui "
                f"la distingue de sa voisine la plus proche ? C'est la "
                f"FRONTIÈRE qui sert, pas la définition — c'est elle qu'on "
                f"relit quand on hésite."))
    return valeurs, d


# --------------------------------------------------------------------------- #
def verifie_les_transverses(transverses: list[dict],
                            prefixes: list[dict]) -> list[Diagnostic]:
    """Aucun dossier d axe transverse ne peut porter le nom d un dossier de l arbre."""
    d: list[Diagnostic] = []
    arbre = {p["dossier"] for p in prefixes}
    vus: dict[str, str] = {}
    for t in transverses:
        dossier = str((t or {}).get("dossier") or "")
        champ = str((t or {}).get("champ") or "")
        if dossier in arbre:
            d.append(Diagnostic(
                "4.3", f"le dossier `{dossier}` est déjà un dossier de l'arbre",
                f"Tu veux appeler « {dossier} » le dossier qui rassemble tes "
                f"{champ} — mais c'est déjà le nom d'un de tes paquets. Le "
                f"le vault d'origine a nommé son dossier transverse « Métiers » et non "
                f"« Domaines » pour cette raison exacte. Quel autre nom ?",
                bloquant=True))
        if dossier in vus:
            d.append(Diagnostic(
                "4.3", f"deux axes transverses veulent le dossier `{dossier}`",
                f"« {vus[dossier]} » et « {champ} » ne peuvent pas partager le "
                f"même dossier.", bloquant=True))
        vus[dossier] = champ
    return d


# --------------------------------------------------------------------------- #
def rapport(p: Paquets, seuil: int, motif: str) -> str:
    """Ce que l entretien REND A HAUTE VOIX apres la passe 2.

    Pas un dump : une lecture. L utilisateur doit reconnaitre son geste dedans,
    sinon l induction s est trompee et il faut y revenir tout de suite — pas
    apres avoir construit huit blocs par-dessus.
    """
    L = [f"Voilà ce que je lis dans ton rangement — {len(p.prefixes)} paquets, "
         f"{sum(x['_population'] for x in p.prefixes)} pages placées :", ""]
    for x in p.prefixes:
        L.append(f"  · {x['dossier']}  ({x['_population']} page(s)) "
                 f"-> dossier `{x['dossier']}/`, valeur `{x['cle']}`")
    L.append("")
    L.append(f"Ton axe {'EXCLUT' if p.exclusif else 'NE PEUT PAS EXCLURE'} : "
             + ("chaque page tombe dans exactement un paquet, c'est ce qui en "
                "fait un axe de rangement et non un axe transverse."
                if p.exclusif else
                f"{len(p.debordent)} page(s) débordent. Ce n'est pas un défaut "
                f"— c'est un fait de ton sujet, et il se déclare."))
    L.append("")
    L.append(f"Seuil de promotion d'un sous-dossier : {seuil}.")
    L.append(f"  {motif}")
    if p.diagnostics:
        L.append("")
        L.append("Ce sur quoi je reviens vers toi :")
        for d in p.diagnostics:
            L.append("  " + d.rendu().replace("\n", "\n  "))
    return "\n".join(L)
