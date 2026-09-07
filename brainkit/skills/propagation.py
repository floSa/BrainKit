"""propagation.py — la table de propagation, DERIVEE du manifeste.

Ce module est le cœur du lot 7, et il tient en une phrase : **aucune ligne de la
table n est ecrite ici**. Les lignes sortent des roles, des axes et des champs
reciproques que le manifeste declare. Une table identique sur deux brains
differents serait la preuve qu elle est recopiee ; ici, deux manifestes
differents produisent deux tables differentes, et chacune est juste.

# L enonce, et pourquoi il ne depend d aucun sujet

    Le rayon de propagation d une insertion est le DOSSIER D ACCUEIL, plus ses
    HUBS PARENTS. Le voisinage d une page est `ls` de son dossier.

Il ne repose que sur un fait STRUCTUREL — le dossier porte la valeur de l axe de
rangement — donc tout brain construit sur l arbre l obtient gratuitement. C est
la brique J1 de l inventaire de separation, classee GENERIQUE, et la mesure le
confirme : elle passe d un brain de sources d histoire a un brain de courses de
montagne sans une retouche.

# Les six familles de lignes, et ce qui les fait naitre

| Famille                | Ce qui la fait naitre dans le manifeste                     |
|---|---|
| le hub du dossier      | un role `fonction: hub`                                     |
| les hubs parents       | un axe de rangement a plus d un niveau (`sous:` declarees)  |
| les autres roles du dossier | chaque role `range_par: axe` qui PORTE la valeur d axe  |
| les pairs              | le role qu on capture, confronte a lui-meme                 |
| les resumes reinjectes | un champ `fonction: resume_court` avec `reinjecte_dans`     |
| les hubs de ralliement | un role qui declare `hub_de_ralliement`                     |
| les hubs transverses   | UNE ligne par entree de `axes.transverses`                  |

La derniere est ecrite au pluriel a dessein : le DevBrain n a qu un axe
transverse et sa table n a qu une ligne ; HistoBrain en a deux et en obtient
deux, parce qu une page peut porter un theme sans porter d espace — et alors
l une des deux lignes est SANS OBJET, ce qui doit se declarer separement.

# La clause qui rend la table verifiable

    Une ligne sans objet se DECLARE sans objet, elle ne se tait pas.

C est elle, et elle seule, qui distingue « j ai propage » de « j ai ecrit une
page ». Chaque ligne porte donc un champ `sans_objet_si` : la condition ECRITE
dans laquelle elle n a rien a produire. Une ligne dont la condition n est pas
remplie et qui reste vide est un oubli, pas un choix.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..generer.prose import champ_du_role
from ..valider.manifeste import Modele

# L ordre dans lequel les roles VOISINS entrent dans la table. Il n est pas
# alphabetique : il va du plus mecanique au plus editorial, parce que c est
# l ordre dans lequel on les traite sans se tromper — la vue entre toute seule,
# la notion demande une decision, les pairs demandent une reciprocite.
ORDRE_DES_FONCTIONS = ("vue", "notion", "prescription", "unite", "transverse")

# Les quatre marqueurs de la colonne « par ». Vocabulaire FERME du kit : ils
# disent QUI fait le travail, et c est la seule chose qu un lecteur presse doit
# pouvoir lire d un coup d œil.
GENERE = "généré"
AUTOMATIQUE = "automatique"
A_ECRIRE = "à écrire"


# Le GENRE d une ligne. Il ne sert pas au rendu : il sert au CONTROLE, qui doit
# savoir comment trouver les objets de la ligne dans un vault reel. Vocabulaire
# ferme par le kit, parce que c est du code, pas une donnee.
G_HUB, G_PARENTS, G_VOISIN = "hub", "parents", "voisin"
G_PAIRS, G_RESUMES, G_RALLIEMENT, G_TRANSVERSE = (
    "pairs", "resumes", "ralliement", "transverse")


@dataclass
class Ligne:
    """Une ligne du rayon. `origine` dit CE QUI, dans le manifeste, l a produite."""

    n: str
    cible: str
    trouve_par: str
    par: str
    origine: str
    genre: str = G_VOISIN
    sans_objet_si: str = ""
    role: str | None = None          # le role vise, quand la ligne en vise un

    @property
    def toujours_un_objet(self) -> bool:
        return not self.sans_objet_si

    @property
    def a_ecrire(self) -> bool:
        """La ligne demande-t-elle un travail HUMAIN ?

        Les lignes generees sont deleguees : `generer --check` et
        `completude_du_hub` les tiennent, et un controle qui exigerait qu on les
        « touche » signalerait un faux defaut. Seules les lignes a ecrire
        peuvent etre TUES.
        """
        return A_ECRIRE in self.par


def _dossier_type(mo: Modele) -> str:
    """Un dossier d exemple, pour que les commandes du skill soient copiables.

    Le PREMIER prefixe declare, jamais un nom invente : un exemple pris dans le
    manifeste reste vrai, un exemple invente vieillit mal.
    """
    prefixes = mo.rangement.get("prefixes") or []
    return str(prefixes[0].get("dossier")) if prefixes else "<dossier>"


def _motif_de_role(mo: Modele, rid: str) -> str:
    r = mo.roles.get(rid) or {}
    return str((r.get("libelle") or {}).get("s") or rid)


def _pluriel(mo: Modele, rid: str) -> str:
    r = mo.roles.get(rid) or {}
    return str((r.get("libelle") or {}).get("p") or rid)


def _arbre_a_des_niveaux(mo: Modele) -> bool:
    """L arbre peut-il porter un sous-dossier ? Sinon P2 n a jamais d objet."""
    return bool(mo.sous_valeurs) and int(mo.rangement.get("niveaux") or 1) > 1


def _champs_reciproques_du_role(mo: Modele, rid: str) -> list[tuple[str, dict]]:
    """Les champs a reciprocite qu un role a le droit de porter, dans l ordre declare."""
    autorises = mo.autorises(rid)
    declares = mo.champs_a_reciprocite()
    return [(nom, declares[nom]) for nom in mo.champs
            if nom in declares and nom in autorises]


def paires_inverses(mo: Modele) -> list[tuple[str, str]]:
    """Les paires `mode: inverse`, DEDUPLIQUEES — (champ, son oppose).

    Le mode inverse n existe pas dans le DevBrain : « A prolonge B » n implique
    pas « B prolonge A », il implique « B EST PROLONGE PAR A ». Une paire se
    declare des DEUX cotes, et `paire_inverse_bien_declaree` refuse le contraire.
    """
    vues: set[frozenset[str]] = set()
    out: list[tuple[str, str]] = []
    for nom, rec in mo.champs_a_reciprocite().items():
        if rec.get("mode") != "inverse":
            continue
        oppose = str(rec.get("champ") or "")
        cle = frozenset((nom, oppose))
        if oppose and cle not in vues:
            vues.add(cle)
            out.append((nom, oppose))
    return out


def champ_resume(mo: Modele) -> str | None:
    return mo.champ_de_fonction("resume_court")


def sections_de_reinjection(mo: Modele) -> list[str]:
    """Les sections ou le resume court se RECOPIE. Dedupliquees, ordre declare.

    La deduplication n est pas de la coquetterie : `cimebrain.brain.yml` porte
    « Variantes » deux fois dans `reinjecte_dans`, parce que le champ a deux
    cotes qui visent la meme section. Une table qui la listerait deux fois
    ferait croire a deux travaux distincts.
    """
    champ = champ_resume(mo)
    if not champ:
        return []
    vues: set[str] = set()
    out: list[str] = []
    for titre in (mo.champ(champ).get("reinjecte_dans") or []):
        t = str(titre)
        if t not in vues:
            vues.add(t)
            out.append(t)
    return out


# --------------------------------------------------------------------------- #
#  LA DERIVATION
# --------------------------------------------------------------------------- #
def derive(mo: Modele, rid: str | None = None) -> list[Ligne]:
    """Le rayon d une insertion de role `rid`. Par defaut, le role d unite.

    La table DEPEND du role capture, et c est voulu : capturer une unite met a
    jour la notion du dossier ; capturer la notion met a jour les unites. La
    ligne « les pairs » designe toujours le role qu on capture ; les autres
    roles du dossier ont chacun la leur.
    """
    rid = rid or mo.role_unite
    lignes: list[Ligne] = []
    n = [0]

    def pose(**kw) -> None:
        n[0] += 1
        lignes.append(Ligne(n=f"P{n[0]}", **kw))

    dossier = _dossier_type(mo)
    mot_axe = mo.libelle_rangement.get("s") or "valeur d'axe"

    # --- 1. le hub du dossier ------------------------------------------- #
    if mo.role_hub:
        pose(genre=G_HUB, cible=f"le hub du dossier d'accueil — `<D>/<D>.md`",
             trouve_par=f'`ls "$D"` : le dossier porte une page à son nom',
             par=f"{GENERE} (zone AUTO) — **le corps, lui, est à relire**",
             origine=f"un rôle `fonction: hub` est déclaré (`{mo.role_hub}`)",
             role=mo.role_hub)

    # --- 2. les hubs parents -------------------------------------------- #
    if mo.role_hub:
        if _arbre_a_des_niveaux(mo):
            sans = (f"la page atterrit directement dans le dossier de "
                    f"{mot_axe} : P1 et P2 désignent alors la même page, et il "
                    f"faut le DIRE")
        else:
            sans = ("toujours, dans ce brain : l'arbre est plat — aucune "
                    "sous-valeur n'est déclarée, donc aucun dossier n'a de "
                    "parent. La ligne existe pour le jour où une le sera")
        pose(genre=G_PARENTS, cible="les hubs parents, jusqu'à la racine",
             trouve_par='remontée de chemin : chaque niveau de `$D` porte son hub',
             par=f"{GENERE} (zone AUTO) — **le corps, lui, est à relire**",
             origine=(f"`axes.rangement` : `niveaux: "
                      f"{mo.rangement.get('niveaux') or 1}` et "
                      f"{len(mo.sous_valeurs)} sous-valeur(s) déclarée(s) — "
                      f"c'est la conjonction des deux qui fait exister un "
                      f"dossier parent"),
             sans_objet_si=sans,
             role=mo.role_hub)

    # --- 3..n. les AUTRES roles du dossier ------------------------------ #
    voisins = [r for r in mo.roles_ranges_par_axe()
               if r != rid and mo.porte_l_axe_de_rangement(r)]
    voisins.sort(key=lambda r: (
        ORDRE_DES_FONCTIONS.index((mo.roles[r].get("fonction") or ""))
        if (mo.roles[r].get("fonction") or "") in ORDRE_DES_FONCTIONS
        else len(ORDRE_DES_FONCTIONS), r))
    for r in voisins:
        pose(**_ligne_de_voisin(mo, r))

    # --- les PAIRS — le role qu on capture ------------------------------- #
    if rid:
        pose(**_ligne_des_pairs(mo, rid))

    # --- les resumes reinjectes ------------------------------------------ #
    champ = champ_resume(mo)
    sections = sections_de_reinjection(mo)
    if champ and sections:
        pose(genre=G_RESUMES, cible=f"les résumés réinjectés — le `{champ}:` recopié chez les "
                   f"pages citées",
             trouve_par=(f"les cibles des champs à réciprocité, dans "
                         + " · ".join(f"« {s} »" for s in sections)),
             par=f"{A_ECRIRE} — **copié depuis la cible, jamais retapé**",
             origine=(f"`champs.{champ}.fonction: resume_court` et son "
                      f"`reinjecte_dans`"),
             sans_objet_si="aucune puce n'a été ajoutée dans ces sections")

    # --- les hubs de ralliement ------------------------------------------ #
    for r in sorted(mo.roles):
        ral = (mo.roles[r].get("hub_de_ralliement") or {})
        if not ral.get("dossier"):
            continue
        lien = str(ral.get("lien_retour") or "Voir aussi")
        pose(genre=G_RALLIEMENT, cible=(f"le hub de ralliement `{ral['dossier']}/` — **hors du "
                    f"dossier**, à la racine"),
             trouve_par=(f"il ne se lit pas dans `ls \"$D\"` : il vit à la "
                         f"racine et réunit tous les "
                         f"`{champ_du_role(mo)}: {r}` du brain"),
             par=(f"sa zone AUTO est {GENERE}e ; **le lien retour vers "
                  f"`[[{ral['dossier']}]]` dans « {lien} » de la page : "
                  f"{A_ECRIRE}** — c'est lui qui fait la grappe, pas la liste"),
             origine=f"`roles[{r}].hub_de_ralliement`",
             sans_objet_si=(f"cette capture ne crée aucune page "
                            f"`{champ_du_role(mo)}: {r}` — le hub n'est dans le rayon d'une "
                            f"insertion que si elle en CRÉE une"),
             role=r)

    # --- les hubs transverses — UNE ligne par axe ------------------------ #
    for t in mo.transverses:
        champ_t = str(t["champ"])
        pose(genre=G_TRANSVERSE, cible=f"les hubs de `{champ_t}:` — `{t['dossier']}/`",
             trouve_par=f"les valeurs de `{champ_t}:` que la page porte",
             par=f"{GENERE} — le hub d'une valeur naît quand une page la porte",
             origine=f"une entrée de `axes.transverses` (`{champ_t}`)",
             sans_objet_si=f"la page ne porte aucune valeur de `{champ_t}:`")

    return lignes


def _ligne_de_voisin(mo: Modele, r: str) -> dict:
    """La ligne d un role VOISIN — un role du dossier qui n est pas celui qu on capture."""
    decl = mo.roles[r]
    fonction = str(decl.get("fonction") or "")
    prefixe = str(decl.get("prefixe_nom") or "")
    ou = (f'`ls "$D"/\'{prefixe}\'*`' if prefixe
          else f'`ls "$D"/*.md`, puis lire `{champ_du_role(mo)}:` dans chaque frontmatter')
    commun = {
        "genre": G_VOISIN,
        "cible": f"la {_motif_de_role(mo, r)} du dossier — `{champ_du_role(mo)}: {r}`",
        "trouve_par": ou,
        "origine": f"`roles[{r}]` est `range_par: axe` et porte l'axe de rangement",
        "sans_objet_si": (f"le dossier ne porte aucune page `{champ_du_role(mo)}: {r}` — et "
                          f"alors la question est : faut-il en créer une ?"),
        "role": r,
    }

    if fonction == "vue":
        vue = decl.get("vue_embarquee") or {}
        ext = str(vue.get("extension") or ".base")
        genere = bool(vue.get("genere"))
        ecrites = [str(mo.titre(s)) for s in mo.corps(r)
                   if s.get("genre") not in ("auto",) and s.get("niveau") != 0]
        commun["par"] = (
            f"la vue `{ext}` : **{AUTOMATIQUE}** si elle filtre sur "
            f"`{mo.champ_rangement}` — la page y entre toute seule ; "
            + (f"le fichier `{ext}` est {GENERE}" if genere
               else f"le fichier `{ext}` n'est PAS généré (`vue_embarquee."
                    f"genere: false`) : il se lit, il ne se réécrit pas")
            + (f" · " + " · ".join(f"« {t} »" for t in ecrites)
               + f" : {A_ECRIRE}" if ecrites else ""))
        return commun

    if decl.get("protege"):
        commun["par"] = (
            f"{A_ECRIRE}, **dans les deux sens** — et c'est un rôle **PROTÉGÉ** : "
            f"la créer est normal (c'est cette ligne) ; **modifier une page "
            f"`{champ_du_role(mo)}: {r}` qui existe déjà demande une demande explicite**. "
            f"Sinon : proposer, et attendre")
        return commun

    commun["par"] = f"{A_ECRIRE}, dans les deux sens"
    return commun


def _ligne_des_pairs(mo: Modele, rid: str) -> dict:
    """La ligne des PAIRS — les autres pages du role qu on capture."""
    recs = _champs_reciproques_du_role(mo, rid)
    paires = {a for a, b in paires_inverses(mo)} | {b for a, b in paires_inverses(mo)}
    morceaux: list[str] = []
    for nom, rec in recs:
        if rec.get("mode") == "inverse":
            continue
        morceaux.append(f"`{nom}:` (symétrique)")
    for a, b in paires_inverses(mo):
        if a in {n for n, _ in recs} or b in {n for n, _ in recs}:
            morceaux.append(f"la **paire** `{a}:` / `{b}:` (inverse)")
    recip = (" et ".join(morceaux) if morceaux else
             "aucun champ à réciprocité n'est autorisé sur ce rôle")

    return {
        "genre": G_PAIRS,
        "cible": f"les pairs — les autres `{champ_du_role(mo)}: {rid}` du dossier",
        "trouve_par": f'`ls "$D"/*.md`, puis lire `{champ_du_role(mo)}:` dans chaque frontmatter',
        "par": (f"{A_ECRIRE}, **réciprocité obligatoire** : " + recip
                + ". Un pair écarté est un CHOIX, pas un oubli : le dire"),
        "origine": (f"le rôle capturé (`{rid}`) confronté à lui-même, plus ses "
                    f"champs `reciproque:`"),
        "sans_objet_si": (f"le dossier ne porte aucune autre page "
                          f"`{champ_du_role(mo)}: {rid}` — la page est la première du dossier"),
        "role": rid,
    }


# --------------------------------------------------------------------------- #
#  LA TABLE DES EFFETS DE BORD — le mode mise a jour
# --------------------------------------------------------------------------- #
# Les quatre marqueurs, repris du DevBrain et REDEFINIS pour un brain neuf :
#   [M] propagation MANUELLE obligatoire — rien ne la fera a votre place ;
#   [G] corrige par une relance de `brainkit generer --ecrire` ;
#   [D] DECLARE — une regle du validateur le controle. Sur un brain neuf, ces
#       regles sont en `a_mesurer` : elles COMPTENT, elles ne bloquent pas.
#       C est le lot 8 qui les durcit, apres mesure ;
#   [!] derive SILENCIEUSE — aucun controle n existe.
MANUEL, GENERATEUR, DECLARE, SILENCIEUX = "[M]", "[G]", "[D]", "[!]"


@dataclass
class Effet:
    champ: str
    rayon: str
    consommateurs: list[str] = field(default_factory=list)
    inventaire: str = "—"
    verification: str = "—"
    origine: str = ""


def _cite_par_le_bandeau(mo: Modele, champ: str) -> bool:
    for c in (mo.bandeau.get("colonnes") or []):
        if c.get("source") == champ or c.get("qualifie_par") == champ:
            return True
    return bool(mo.bandeau.get("porte_le_resume")
                and mo.champ(champ).get("fonction") == "resume_court")


def _cite_par_une_vue(mo: Modele, champ: str) -> str | None:
    for rid in mo.roles_de_fonction("vue"):
        vue = mo.roles[rid].get("vue_embarquee") or {}
        if champ in (vue.get("colonnes_par_defaut") or []):
            return rid
        if vue.get("tri_par") == champ:
            return rid
    return None


def _commande_les_conditionnels(mo: Modele, champ: str) -> list[str]:
    """Les champs conditionnels dont la condition CITE ce champ."""
    out: list[str] = []
    for rid in sorted(mo.roles):
        for c in mo.conditionnels(rid):
            if champ in str(c.get("si") or "") and c["champ"] not in out:
                out.append(str(c["champ"]))
    return out


def effets_de_bord(mo: Modele) -> list[Effet]:
    """Champ modifie -> consommateurs -> commande de verification. DERIVEE.

    Une modification de champ n est pas finie quand la page est enregistree :
    elle est finie quand ses CONSOMMATEURS sont a jour. Une page qui existe a
    des consommateurs ; une page qu on cree n en a pas. C est toute la
    difference entre le mode cible et le mode mise a jour.
    """
    out: list[Effet] = []
    idx = set((mo.m.get("genere") or {}).get("index", {}).get("champs") or [])
    voc = mo.vocabulaires or {}
    valider = "`brainkit valider --regle {}`"

    for champ in mo.champs:
        d = mo.champ(champ)
        cons: list[str] = []
        origines: list[str] = []
        rayon: list[str] = []
        inventaire = "—"
        verifs: list[str] = []
        fonction = str(d.get("fonction") or "aucune")
        source = str(d.get("source") or "")

        # --- fonction : identite / resume / alias ------------------------ #
        if fonction == "identite":
            rayon.append("tout le rayon")
            cons += [
                f"{MANUEL} le NOM DU FICHIER : il suit, et par `git mv` — "
                f"jamais par suppression + création, sinon l'historique est perdu",
                f"{DECLARE} les wikilinks du CORPS des pages qui la citent "
                f"(`liens_resolus`)",
                f"{DECLARE} les wikilinks du FRONTMATTER — les champs "
                f"`type: liens` (`reciprocite`)",
                f"{DECLARE} l'unicité du nom de fichier, à la casse près "
                f"(`unicite_du_nom_de_fichier`)",
                f"{GENERATEUR} l'index, les zones AUTO des hubs, la carte des liens",
            ]
            origines.append(f"`champs.{champ}.fonction: identite`")
            inventaire = ('grep -rn "<ancien nom>" --include="*.md"'
                          + (f' --include="*{mo.extension_de_vue()}"'
                             if mo.extension_de_vue() else "")
                          + " . | grep -v '/.git/'")
            verifs.append("la même commande renvoie **0 ligne**")
            verifs.append(valider.format("liens_resolus"))
        elif fonction == "resume_court":
            secs = sections_de_reinjection(mo)
            rayon.append("la ligne des résumés réinjectés")
            cons.append(
                f"{MANUEL} les puces de " +
                (" · ".join(f"« {s} »" for s in secs) if secs else "ses sections")
                + " chez **toutes** les pages qui citent la cible — le résumé se "
                  "COPIE depuis la cible, il ne se retape pas")
            origines.append(f"`champs.{champ}.fonction: resume_court`"
                            + (" et son `reinjecte_dans`" if secs else ""))
            verifs.append(valider.format("reinjection_du_resume"))
        elif fonction == "alias":
            cons += [f"{DECLARE} la collision d'alias (`collision_alias`)",
                     f"{SILENCIEUX} la résolution des `[[alias]]` par Obsidian"]
            origines.append(f"`champs.{champ}.fonction: alias`")
            verifs.append(valider.format("collision_alias"))

        # --- la source du vocabulaire ------------------------------------ #
        if source in ("axes.rangement", mo.champ_rangement) and source:
            rayon.append("**CHANGE de rayon**")
            cons += [
                f"{DECLARE} le CHEMIN doit suivre : la page **déménage**, par "
                f"`git mv` (`chemin_categorie`)",
                f"{GENERATEUR} le hub quitté ET le hub d'accueil",
                f"{SILENCIEUX} l'entrée / la sortie des vues filtrées sur "
                f"`{mo.champ_rangement}`",
                f"{SILENCIEUX} le SEUIL de promotion : la page change de "
                f"population — un départ peut dépromouvoir un sous-dossier, "
                f"une arrivée le promouvoir. C'est `brainkit re-seuiller`, pas "
                f"une capture",
                f"{DECLARE} la valeur appartient au vocabulaire déclaré "
                f"(`vocabulaire_ferme`)",
            ]
            origines.append(f"`champs.{champ}.source: {source}`")
            inventaire = "brainkit valider --regle chemin_categorie --tout"
            verifs.append(valider.format("chemin_categorie"))
        elif source in ("axes.nature", mo.champ_nature) and source:
            cond = _commande_les_conditionnels(mo, champ)
            cons.append(f"{DECLARE} la valeur appartient au vocabulaire déclaré "
                        f"(`vocabulaire_ferme`)")
            if cond:
                cons.append(
                    f"{DECLARE} les champs CONDITIONNELS qu'il commande — "
                    + ", ".join(f"`{c}:`" for c in cond)
                    + " : les retirer quand la condition cesse de tenir "
                      "(`gabarit_par_role`)")
            origines.append(f"`champs.{champ}.source: {source}`")
            verifs.append(valider.format("gabarit_par_role"))
        elif source.startswith("axes.transverses"):
            for t in mo.transverses:
                if t["champ"] == champ:
                    rayon.append(f"la ligne des hubs de `{champ}:`")
                    cons.append(f"{GENERATEUR} les hubs de `{t['dossier']}/` — "
                                f"un hub par valeur portée : celui qu'on quitte "
                                f"peut tomber à zéro page et disparaître")
            origines.append(f"`champs.{champ}.source: {source}`")
            verifs.append("`brainkit generer --check`")
        elif source.startswith("vocabulaires."):
            nom_voc = source.split(".", 1)[1]
            decl = voc.get(nom_voc) or {}
            cons.append(
                f"{DECLARE} la valeur appartient à `{decl.get('fichier', nom_voc)}` "
                f"(mode `{decl.get('mode', 'libre')}`) — une valeur manquante se "
                f"**propose**, s'ajoute là-bas, PUIS s'utilise "
                f"(`vocabulaire_ferme`)")
            origines.append(f"`champs.{champ}.source: {source}`")
            verifs.append(valider.format("vocabulaire_ferme"))
        elif source == "roles[].id":
            rayon.append("tout le rayon")
            cons += [
                f"{DECLARE} il choisit le GABARIT que le validateur applique : "
                f"changer ce champ change la liste des champs autorisés "
                f"(`gabarit_par_role`)",
                f"{DECLARE} il peut changer le DOSSIER — un rôle "
                f"`range_par: role` vit dans le sien (`chemin_categorie`)",
                f"{GENERATEUR} les zones AUTO des hubs, l'index, la carte des liens",
                f"{SILENCIEUX} la couleur du nœud dans le graphe "
                f"(`.obsidian/graph.json` n'est pas versionné)",
            ]
            origines.append(f"`champs.{champ}.source: roles[].id`")
            verifs.append("`brainkit valider`")

        # --- la reciprocite ---------------------------------------------- #
        rec = d.get("reciproque")
        if isinstance(rec, dict):
            mode = str(rec.get("mode"))
            oppose = str(rec.get("champ") or champ)
            rayon.append("la ligne des pairs")
            if mode == "inverse":
                cons.append(
                    f"{DECLARE} l'INVERSE `{oppose}:` de la cible — « A "
                    f"{champ} B » implique « B {oppose} A », **pas** « B "
                    f"{champ} A » (`reciprocite`)")
            else:
                cons.append(f"{DECLARE} le `{champ}:` de la cible, en retour "
                            f"(`reciprocite`)")
            if d.get("section"):
                cons.append(f"{MANUEL} la section « {d['section']} » des DEUX "
                            f"pages — le frontmatter et le corps disent la même "
                            f"chose, ou ils mentent tous les deux")
                cons.append(f"{DECLARE} une même cible ne se liste QUE dans une "
                            f"section (`citation_unique`)")
            origines.append(f"`champs.{champ}.reciproque.mode: {mode}`")
            inventaire = f'grep -rn "{champ}:" --include="*.md" . | grep -v "/.git/"'
            verifs.append(valider.format("reciprocite"))

        # --- les consommateurs machine ----------------------------------- #
        if _cite_par_le_bandeau(mo, champ):
            cons.append(f"{GENERATEUR} la zone AUTO du bandeau — une cellule "
                        f"sans source affiche « {mo.bandeau.get('vide', '—')} », "
                        f"jamais une valeur plausible")
            verifs.append("`brainkit generer --check`")
        rid_vue = _cite_par_une_vue(mo, champ)
        if rid_vue:
            cons.append(f"{SILENCIEUX} les vues `{champ_du_role(mo)}: {rid_vue}` : le champ est "
                        f"une colonne ou le tri — elles se lisent en direct, "
                        f"mais un filtre qui le vise change de membres")
        # L index n est cite QU UNE FOIS. Un champ d identite ou d axe l a deja
        # nomme dans sa propre ligne : le redire ferait croire a deux travaux.
        if champ in idx and not any("l'index" in c for c in cons):
            cons.append(f"{GENERATEUR} l'index — le champ y est publié, donc lu "
                        f"par le skill d'exploitation sans ouvrir la page")
        if d.get("type") == "liens":
            cons.append(f"{DECLARE} chaque cible doit exister : un lien mort en "
                        f"frontmatter ne se voit pas à la lecture de la page "
                        f"(`liens_resolus`)")
            verifs.append(valider.format("liens_resolus"))
            origines.append(f"`champs.{champ}.type: liens`")
        if d.get("eliminatoire"):
            cons.append(f"{DECLARE} le champ est ÉLIMINATOIRE : "
                        + ", ".join(f"`{v}`" for v in d["eliminatoire"])
                        + " disqualifie la page auprès du skill d'exploitation")

        if not cons:
            cons.append(f"{SILENCIEUX} aucun consommateur déclaré : le champ "
                        f"n'est ni indexé, ni au bandeau, ni réciproque, ni "
                        f"adossé à un vocabulaire. Il se lit en ouvrant la page")

        out.append(Effet(
            champ=champ,
            rayon=" · ".join(dict.fromkeys(rayon)) or "—",
            consommateurs=cons,
            inventaire=inventaire,
            verification=" ; ".join(dict.fromkeys(verifs)) or "`brainkit valider`",
            origine=" · ".join(origines) or f"`champs.{champ}` (aucune fonction)",
        ))
    return out


def effets_hors_champ(mo: Modele) -> list[Effet]:
    """Les deux effets qui ne sont PAS des modifications de champ.

    Un renommage et une suppression touchent tout le rayon et n ont aucune ligne
    dans `champs:`. Les omettre, c est laisser le cas le plus dangereux sans
    procedure — et c est ce cas-la qui laisse des liens morts.
    """
    ext = mo.extension_de_vue()
    inc = ' --include="*.md"' + (f' --include="*{ext}"' if ext else "")
    return [
        Effet(
            champ="**renommer ou déplacer une page**",
            rayon="tout le rayon, des DEUX côtés",
            consommateurs=[
                f"{MANUEL} `git mv` — **jamais** une suppression suivie d'une "
                f"création : l'historique de la page est perdu et ne revient pas",
                f"{DECLARE} `nom:` suit le nom du fichier (`nom_egal_fichier`)",
                f"{DECLARE} les wikilinks du corps ET du frontmatter "
                f"(`liens_resolus`)",
                f"{SILENCIEUX} un filtre de vue par LISTE DE NOMS codée en dur : "
                f"il ne suit pas",
                f"{GENERATEUR} l'index, les hubs, la carte des liens",
            ],
            inventaire=f'grep -rn "<ancien nom>"{inc} . | grep -v "/.git/"',
            verification="la même commande renvoie **0 ligne**, puis "
                         "`brainkit valider`",
            origine="`champs` de `fonction: identite` + `regles_de_socle."
                    "nom_egal_fichier`",
        ),
        Effet(
            champ="**supprimer une page**",
            rayon="tout le rayon",
            consommateurs=[
                f"{MANUEL} **une suppression se DEMANDE.** Elle n'est jamais "
                f"une conséquence d'une capture",
                f"{DECLARE} les liens morts chez ses citeurs, corps et "
                f"frontmatter (`liens_resolus`)",
                f"{DECLARE} les réciprocités orphelines : la moitié qui reste "
                f"pointe vers rien (`reciprocite`)",
                f"{SILENCIEUX} une vue peut tomber sous son seuil de membres",
                f"{GENERATEUR} l'index, les hubs, la carte des liens",
            ],
            inventaire=f'grep -rn "<nom>"{inc} . | grep -v "/.git/"',
            verification="la même commande renvoie **0 ligne**, puis "
                         "`brainkit valider`",
            origine="`frontieres_d_ecriture.jamais_sans_accord`",
        ),
    ]
