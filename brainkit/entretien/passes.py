"""passes.py — les onze passes de l entretien, et leurs questions, EN DONNEES.

# Pourquoi les questions sont des donnees et non de la prose

Le skill (`skills/entretien/SKILL.md`) conduit l entretien ; ce module en porte
la LISTE. La separation n est pas cosmetique : une liste en prose se degrade —
une question saute, une autre change d ordre, et personne ne s en apercoit parce
que rien ne compte. Ici le jeu d epreuve compte, verifie l ordre, verifie que
chacun des treize refus de `00-cadrage.md` §3.5 est porte par au moins une
question, et verifie qu aucune question bloquante n est contournable.

# L ordre est contraint, il n est pas un gout

Chaque passe a besoin de la reponse de la precedente : on ne demande pas les
sections du corps avant de savoir quelle est l unite, ni le seuil de promotion
avant le volume cible. C est la seule decision de conception de l entretien, et
elle est ecrite au cadrage §3.1.

# Les quatre questions ajoutees au cadrage, et pourquoi

Le cadrage en compte quarante-cinq. Il en manque quatre, et le manque n est pas
theorique : sans elles, l entretien ne saurait produire NI le manifeste
DevBrain, NI le manifeste HistoBrain, qui sont les deux remplissages de
reference du kit.

| id | ce qu elle produit | pourquoi elle manquait |
|---|---|---|
| 0.6 | le dossier de l instance | l entretien finit par appeler le semis ; le chemin ne se devine pas plus qu une adresse |
| 1.5 | les roles `fonction: prescription` | AUCUNE question du cadrage ne les cree, et les deux remplissages de reference en portent deux chacun (`pattern`+`rule`, `controverse`+`methode`) |
| 9.5 | le bloc `racine:` | demande par le lot 5, §10 : « il porte une question de plus a poser » |
| 9.6 | `racine.dossiers[]` | l arbitrage `Projects/` (remontee 4 du lot 5), renvoye a ce lot |

Elles sont marquees `ajoutee:` et le jeu d epreuve verifie que ce champ est
rempli : une question hors cadrage sans motif ecrit serait une question inventee.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Question:
    """Une question, et surtout ce qu elle REFUSE de deviner."""

    id: str
    texte: str
    produit: str                 # le chemin de manifeste qu elle remplit
    refus: int | None = None     # le refus de §3.5 qui la garde
    condition: str = ""          # posee seulement si …
    bloquante: bool = False      # sans reponse, l entretien S ARRETE
    ajoutee: str = ""            # motif, si la question n est pas au cadrage
    note: str = ""               # ce que l entretien DIT en la posant

    @property
    def conditionnelle(self) -> bool:
        return bool(self.condition)


@dataclass(frozen=True)
class Passe:
    n: int
    titre: str
    propos: str
    questions: tuple[Question, ...] = field(default_factory=tuple)


PASSES: tuple[Passe, ...] = (
    # ---------------------------------------------------------------- 0 ---- #
    Passe(
        0, "Identité et dépôt",
        "Ce qui n'a rien à voir avec le sujet, et qui ne se devine sous aucune "
        "forme. La passe est indifférente au sujet — et c'est la seule.",
        (
            Question("0.1", "De quoi ce brain parle-t-il, en une phrase ?",
                     "brain.sujet",
                     note="La phrase de l'utilisateur est la bonne. Ne jamais la "
                          "reformuler en mieux."),
            Question("0.2", "Comment veux-tu l'appeler ?", "brain.nom"),
            Question("0.3", "Ce brain est-il personnel, professionnel, ou celui "
                            "d'un client ?", "brain.usage",
                     note="Décide la POLARITÉ du garde-fou d'identité : sur un "
                          "brain `client` hébergé chez un employeur, c'est "
                          "l'adresse perso qu'il faut refuser."),
            Question("0.4", "Sous quel nom et quelle adresse ses commits "
                            "doivent-ils être signés ?", "git.identite",
                     refus=1, bloquante=True,
                     note="REFUS ABSOLU de deviner. Ne JAMAIS reprendre l'adresse "
                          "annoncée par le harnais. Sans réponse, l'entretien "
                          "s'arrête ici — il ne sème rien."),
            Question("0.5", "Quelle adresse ne doit *jamais* apparaître dans un "
                            "commit ici ?", "git.domaines_refuses", refus=1),
            Question("0.6", "Dans quel dossier veux-tu que ce brain soit semé ?",
                     "(le chemin de l'instance)",
                     ajoutee="L'entretien finit par appeler le semis. Le dossier "
                             "cible ne se devine pas plus qu'une adresse, et les "
                             "quatre refus du plan d'écriture se rejouent à vide "
                             "dessus avant de le proposer."),
        )),
    # ---------------------------------------------------------------- 1 ---- #
    Passe(
        1, "L'unité",
        "La passe qui commande tout : le nom de l'unité fuit dans les gabarits, "
        "les hubs, les skills et le routeur. Le kit ne le connaît nulle part.",
        (
            Question("1.1", "Dans six mois, tu ouvres ce brain pour t'en servir. "
                            "Qu'est-ce que tu vas chercher ?",
                     "roles[fonction: unite]", refus=2,
                     note="Ne jamais nommer l'unité soi-même : elle s'induit de "
                          "la réponse, et on la fait confirmer."),
            Question("1.2", "Comment appelles-tu cette chose, au singulier et au "
                            "pluriel ?", "libelles.unite", refus=2,
                     note="REFUS de traduire depuis le dev : « brique » ne sort "
                          "jamais de la bouche de l'entretien."),
            Question("1.3", "Y a-t-il, à côté, des pages qui n'expliquent pas "
                            "*quoi utiliser* mais *ce qu'il faut comprendre* ?",
                     "roles[fonction: notion]", refus=2,
                     note="« Non » est une réponse légale : un brain sans notions "
                          "est valide."),
            Question("1.4", "Y a-t-il des pages que TU écris pour toi, et que "
                            "l'IA ne doit pas réécrire sans te demander ?",
                     "roles[].protege",
                     note="Ne jamais poser `protege: true` par défaut, ni le "
                          "refuser."),
            Question("1.5", "Y a-t-il des pages qui ne décrivent pas un(e) "
                            "<unité> mais qui PRESCRIVENT — une règle, une "
                            "méthode, un modèle à suivre — et qui traversent "
                            "tous les paquets par construction ?",
                     "roles[fonction: prescription]", refus=2,
                     ajoutee="Aucune question du cadrage ne crée ce rôle, et les "
                             "DEUX remplissages de référence en portent deux "
                             "chacun (`pattern` + `rule`, `controverse` + "
                             "`methode`). Sans elle, l'entretien ne saurait "
                             "produire ni l'un ni l'autre.",
                     note="« Non » est légal — et zéro rôle de prescription ne "
                          "crée aucun dossier."),
        )),
    # ---------------------------------------------------------------- 2 ---- #
    Passe(
        2, "L'axe qui range",
        "La passe la plus longue et la plus payante. C'est ici que l'induction "
        "travaille : vingt pages réelles, rangées à la main, et la taxonomie "
        "en sort.",
        (
            Question("2.1", "Cite-moi VINGT pages que tu voudrais dans ce brain. "
                            "Des vraies, pas des catégories.",
                     "(l'échantillon d'induction)", refus=3,
                     note="REFUS de proposer les vingt. L'entretien attend, quitte "
                          "à revenir. Moins de dix : il redemande — l'induction "
                          "ne tient pas."),
            Question("2.2", "Range ces vingt en paquets, DE TA MAIN. Combien de "
                            "paquets, et comment les appelles-tu ?",
                     "axes.rangement.prefixes[]", refus=3,
                     note="REFUS de proposer les paquets. Jamais de liste à "
                          "cocher : on coche par politesse."),
            Question("2.3", "Chacune de tes vingt pages tombe-t-elle dans "
                            "EXACTEMENT un paquet ?", "axes.rangement.exclusif",
                     note="Si « non » : ne pas passer outre, poser 2.4. C'est la "
                          "question qui distingue un axe de rangement d'un axe "
                          "transverse."),
            Question("2.4", "Pour celles qui débordent : est-ce qu'un paquet "
                            "DOMINE quand même, ou couvrent-elles vraiment tout ?",
                     "axes.rangement.regle_de_majorite / prefixe_transversal",
                     condition="2.3 = non",
                     note="Ne jamais forcer une valeur unique pour faire passer "
                          "la contrainte."),
            Question("2.5", "Comment appelles-tu ce que ces paquets sont ?",
                     "libelles.axe_rangement"),
            Question("2.6", "Combien de pages ce brain aura-t-il QUAND IL SERA "
                            "PLEIN ? Un ordre de grandeur suffit.",
                     "brain.volume_cible", refus=4,
                     note="REFUS de demander le seuil directement : l'utilisateur "
                          "n'a aucun moyen de le connaître, le volume si. Le "
                          "seuil se dérive, et le calcul s'écrit dans "
                          "`motif_seuil`."),
            Question("2.7", "Pour chaque paire de paquets qui pourrait se "
                            "disputer une page : quelle question FERMÉE tranche, "
                            "et laquelle passe en premier ?",
                     "axes.rangement.arbre_de_decision[]", refus=5,
                     note="L'IA peut proposer les questions, JAMAIS leur rang. "
                          "L'ordre est LA décision de conception, et l'entretien "
                          "l'annonce comme telle."),
        )),
    # ---------------------------------------------------------------- 3 ---- #
    Passe(
        3, "L'axe qui qualifie",
        "Deux pages du même paquet peuvent-elles être de deux natures ? "
        "« Non » est fréquent, légal, et l'entretien n'insiste pas.",
        (
            Question("3.1", "Deux pages du MÊME paquet peuvent-elles être de deux "
                            "natures très différentes ?", "axes.nature",
                     note="« Non » est légal ET fréquent : un brain sans axe de "
                          "nature est valide."),
            Question("3.2", "En regardant tes vingt pages : quelles natures "
                            "vois-tu ?", "axes.nature.valeurs[]", refus=8,
                     condition="3.1 = oui",
                     note="Induit de l'échantillon, jamais listé d'avance."),
            Question("3.3", "Dans quel ordre les questions fermées qui les "
                            "séparent ?", "axes.nature.arbre_de_decision[]",
                     refus=5, condition="3.1 = oui"),
            Question("3.4", "Y a-t-il des informations qui n'ont de sens que pour "
                            "CERTAINES de ces natures ?",
                     "roles[].champs.conditionnels", condition="3.1 = oui"),
        )),
    # ---------------------------------------------------------------- 4 ---- #
    Passe(
        4, "Les axes transverses",
        "Zéro est une réponse. L'entretien n'en invente aucun par analogie.",
        (
            Question("4.1", "Y a-t-il une question que tu poseras au brain et qui "
                            "TRAVERSE tous les paquets ?", "axes.transverses[]",
                     refus=10,
                     note="REFUS d'en inventer un. Zéro axe transverse est légal, "
                          "et le générateur ne crée alors aucun dossier."),
            Question("4.2", "Une page en porte-t-elle une seule valeur, ou "
                            "plusieurs ?", "axes.transverses[].multivalue",
                     condition="4.1 ≥ un axe"),
            Question("4.3", "Comment appelles-tu le dossier qui les rassemble ?",
                     "axes.transverses[].dossier", condition="4.1 ≥ un axe",
                     note="Vérifier qu'il ne redouble aucun nom de l'arbre — le "
                          "DevBrain a nommé `Métiers/` et non `Domaines/` pour "
                          "cette raison exacte."),
        )),
    # ---------------------------------------------------------------- 5 ---- #
    Passe(
        5, "Le haut de page",
        "Trois à cinq faits, et pas un de plus. Le bandeau existe PARCE QUE "
        "dix-huit propriétés poussaient le texte sous la ligne de flottaison.",
        (
            Question("5.1", "Tu ouvres une page. AVANT le texte, quels trois à "
                            "cinq faits veux-tu voir ?", "bandeau.colonnes[]",
                     note="Plus de cinq : redemander."),
            Question("5.2", "D'où vient ce fait — quel champ du frontmatter le "
                            "porte ?", "bandeau.colonnes[].source", refus=12,
                     condition="par colonne",
                     note="REFUS d'une colonne sans source : une colonne dérivée "
                          "d'un jugement n'entre pas dans le bandeau."),
            Question("5.3", "Et quand un de ces faits manque sur une page, on "
                            "affiche quoi ?", "bandeau.vide",
                     note="Proposer le tiret cadratin, et sa règle : une cellule "
                          "sans source affiche un tiret, jamais une valeur "
                          "plausible."),
        )),
    # ---------------------------------------------------------------- 6 ---- #
    Passe(
        6, "Le corps",
        "Les sections d'une page d'unité, dans l'ordre, et leur GENRE — c'est "
        "le genre qui branche les règles, pas le titre.",
        (
            Question("6.1", "Sur une page d'unité, que veux-tu lire, DANS "
                            "L'ORDRE ?", "roles[].corps[]",
                     note="Ne pas proposer les titres du DevBrain."),
            Question("6.2", "Laquelle de ces sections est une PROSE ?",
                     "corps[].genre: prose",
                     note="Une seule, en principe. Si l'utilisateur en veut "
                          "trois, le dire : la doctrine est « aucune prose hors "
                          "de la section de définition », et elle a une raison "
                          "mesurée."),
            Question("6.3", "Y a-t-il une section où tu DÉCIDES — d'un côté ce "
                            "qui va, de l'autre ce qui ne va pas ?",
                     "corps[].genre: decision",
                     note="« Non » est légal : la règle 5 se désactive alors, "
                          "elle ne se force pas."),
            Question("6.4", "Y a-t-il une section qui est une LISTE DE LIENS vers "
                            "d'autres pages ? Lesquelles ?",
                     "corps[].genre: liste_liens"),
            Question("6.5", "Y a-t-il une section ÉTIQUETÉE — des puces "
                            "« Étiquette — valeur » ? Quelles étiquettes "
                            "exactement, et lesquelles sont obligatoires ?",
                     "corps[].genre: etiquetee", refus=7,
                     note="REFUS de compléter le vocabulaire : cinq étiquettes "
                          "nommées valent mieux que sept dont deux inventées."),
        )),
    # ---------------------------------------------------------------- 7 ---- #
    Passe(
        7, "Les liens et le résumé",
        "La passe qui a coûté une ligne de code au kit : la réciprocité INVERSE, "
        "que le DevBrain n'a jamais eue.",
        (
            Question("7.1", "Deux pages peuvent-elles être en OPPOSITION ? En "
                            "COMPLÉMENT ? Autrement ?", "champs[type: liens]"),
            Question("7.2", "Si A est dans cette relation avec B, est-ce que B "
                            "est dans la MÊME relation avec A ?",
                     "champs[].reciproque.mode: symetrique",
                     condition="par relation"),
            Question("7.3", "Comment se dit la relation DANS L'AUTRE SENS ?",
                     "champs[].reciproque.mode: inverse", condition="7.2 = non",
                     note="REFUS de forcer la symétrie : « A prolonge B » n'est "
                          "pas « B prolonge A »."),
            Question("7.4", "Quel champ est le RÉSUMÉ D'UNE LIGNE qu'on "
                            "recopiera chez tous ceux qui citent la page ?",
                     "champs[].fonction: resume_court",
                     note="Si aucun : la règle 6 se désactive. Ne pas en inventer "
                          "un."),
        )),
    # ---------------------------------------------------------------- 8 ---- #
    Passe(
        8, "Ce qui rassemble",
        "La passe qui sauve le comparatif — ou qui refuse de le traduire. "
        "8.1 passe AVANT 8.2, sans quoi le comparatif reviendrait par réflexe.",
        (
            Question("8.1", "Tes <unités> sont-elles INTERCHANGEABLES ? En "
                            "choisit-on une CONTRE une autre ?",
                     "roles[fonction: vue] — orientation", refus=9),
            Question("8.2", "Y a-t-il quand même une TABLE que tu voudrais voir, "
                            "une liste filtrée sur un paquet, triée sur quelque "
                            "chose ?", "roles[fonction: vue] — tri_par",
                     refus=9, condition="8.1 = non",
                     note="REFUS de traduire le comparatif : si les unités ne "
                          "sont pas interchangeables, le mot ne doit pas "
                          "apparaître."),
            Question("8.3", "Veux-tu un dossier qui les rassemble tous ?",
                     "roles[].hub_de_ralliement", condition="un rôle `vue` existe",
                     note="Rappeler pourquoi : c'est le LIEN RETOUR qui fait la "
                          "grappe, pas le dossier."),
        )),
    # ---------------------------------------------------------------- 9 ---- #
    Passe(
        9, "Gouvernance et frontières",
        "Ce que l'IA a le droit de faire dans ce vault, et ce qu'elle doit "
        "demander. Plus les deux questions que le lot 5 a renvoyées ici.",
        (
            Question("9.1", "Les mots-clés transverses : vocabulaire FERMÉ (on "
                            "propose avant d'ajouter) ou libre ?",
                     "vocabulaires.tags.mode", refus=7,
                     note="Recommander `ferme` et dire pourquoi, mais accepter "
                          "`libre`. Le fichier naît VIDE dans les deux cas."),
            Question("9.2", "Une suppression de page : permise, ou toujours à te "
                            "demander ?", "frontieres_d_ecriture.jamais_sans_accord"),
            Question("9.3", "Y a-t-il un second mode — travailler DEPUIS ce "
                            "brain, dans un autre dépôt ?",
                     "frontieres_d_ecriture.second_mode",
                     note="« Non » est légal : le DevBrain en a un parce que son "
                          "consommateur est un dépôt de code."),
            Question("9.4", "Quels chemins ne doivent JAMAIS être édités à la "
                            "main ?", "genere.chemins[]",
                     note="Proposer la liste déduite du manifeste, la faire "
                          "confirmer."),
            Question("9.5", "Quels fichiers vis-tu à la racine du vault, et "
                            "lequel cite tes hubs de premier niveau ?",
                     "racine.pages[] / racine.porte_d_entree",
                     ajoutee="Demandée par le lot 5, §10 : « le bloc `racine:` "
                             "porte une question de plus à poser ». La réponse "
                             "par défaut — une porte et une inbox — est celle "
                             "des deux remplissages, mais elle ne se devine pas "
                             "plus qu'une autre.",
                     note="`aiguille: false` est la moitié qui compte : une inbox "
                          "vit à la racine SANS aiguiller."),
            Question("9.6", "Veux-tu un dossier d'atelier, vide dès le premier "
                            "jour, que le validateur ne lira pas — un journal de "
                            "projets, un brouillon ?", "racine.dossiers[]",
                     ajoutee="L'arbitrage `Projects/` — remontée 4 du lot 5, "
                             "renvoyée à ce lot. Posée UNE fois, avec son coût "
                             "annoncé, et le défaut est ZÉRO dossier.",
                     note="Dire la mesure avant la réponse : le `Projects/` du "
                          "DevBrain porte ZÉRO page en dix-huit mois. Un dossier "
                          "vide qu'on n'a pas demandé reste vide."),
        )),
    # --------------------------------------------------------------- 10 ---- #
    Passe(
        10, "L'exploitation",
        "Ce qu'on PRODUIT à partir du brain. Sans réponse, le troisième skill "
        "n'est pas généré — mieux vaut deux skills que trois dont un inventé.",
        (
            Question("10.1", "Que produiras-tu À PARTIR de ce brain ?",
                     "skills.exploitation.livrable", refus=13,
                     note="REFUS de deviner. C'est la question qui décide si le "
                          "troisième skill est un cadreur de projet, un "
                          "préparateur de propos, ou une note de synthèse."),
            Question("10.2", "Ce livrable a-t-il des FORMES TYPES ? Lesquelles ?",
                     "skills.exploitation.archetypes",
                     note="Zéro archétype est légal au démarrage."),
            Question("10.3", "Quelles questions faut-il te poser avant de "
                             "produire ce livrable ?",
                     "skills.exploitation — la check-list",
                     note="Induire des réponses précédentes, faire compléter."),
        )),
)


# --------------------------------------------------------------------------- #
QUESTIONS: dict[str, Question] = {
    q.id: q for p in PASSES for q in p.questions
}
ORDRE: tuple[str, ...] = tuple(QUESTIONS)

#: Les questions sans lesquelles l entretien ne peut pas composer un manifeste.
#: 0.4 est la seule qui ARRETE l entretien (refus n° 1) ; les autres se
#: redemandent jusqu a obtenir une reponse.
BLOQUANTES: tuple[str, ...] = tuple(q.id for q in QUESTIONS.values() if q.bloquante)

#: Les questions qui n existent pas au cadrage, chacune avec son motif ecrit.
AJOUTEES: tuple[str, ...] = tuple(q.id for q in QUESTIONS.values() if q.ajoutee)


def passe_de(qid: str) -> Passe:
    for p in PASSES:
        if any(q.id == qid for q in p.questions):
            return p
    raise KeyError(qid)


def total() -> int:
    return len(QUESTIONS)


def rendu() -> str:
    """Les onze passes et leurs questions, telles qu elles seront posees."""
    L: list[str] = [f"{len(PASSES)} passes, {total()} questions "
                    f"(dont {len(AJOUTEES)} ajoutées au cadrage, "
                    f"{len(BLOQUANTES)} bloquante).", ""]
    for p in PASSES:
        L.append(f"Passe {p.n} — {p.titre} ({len(p.questions)} questions)")
        L.append(f"    {p.propos}")
        for q in p.questions:
            marques = []
            if q.refus:
                marques.append(f"refus n° {q.refus}")
            if q.condition:
                marques.append(f"si {q.condition}")
            if q.bloquante:
                marques.append("BLOQUANTE")
            if q.ajoutee:
                marques.append("ajoutée")
            suffixe = f"   [{', '.join(marques)}]" if marques else ""
            L.append(f"  {q.id}  {q.texte}{suffixe}")
            L.append(f"        -> {q.produit}")
        L.append("")
    return "\n".join(L)
