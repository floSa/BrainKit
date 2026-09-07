"""dix.py — LES DIX regles. La liste est FERMEE par le kit.

Le manifeste les BRANCHE (`active:`), leur donne leur SEVERITE (toujours un
resultat de mesure, jamais une intention) et leurs PARAMETRES (le champ, la
section, la colonne, le marqueur, le vocabulaire). Il ne les decrit pas : le kit
garde du code par regle, parce qu une regle est un algorithme et qu un algorithme
ne se met pas en configuration.

Une regle `active: false` ne tourne pas, et l inventaire le dit nommement — une
regle absente ne ressemble pas a une regle souple, elle ressemble a une regle
satisfaite.
"""

from __future__ import annotations

import collections
import re
import unicodedata

from . import chemins, constat, vault
from .constat import Rapport
from .contexte import Contexte
from .manifeste import (GENRE_DECISION, GENRE_ETIQUETEE, GENRE_LISTE,
                        GENRE_PROSE)


def _sans_accent(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "")
                   if unicodedata.category(c) != "Mn").lower()


# --------------------------------------------------------------------------- #
# 1 — reciprocite
# --------------------------------------------------------------------------- #
def reciprocite(ctx: Contexte, r: Rapport) -> None:
    """Si A cite B dans un champ a reciprocite, B cite A — ou son INVERSE declare.

    Deux modes, et le second n existe pas dans le DevBrain :

      `symetrique` — A.X contient B  <=>  B.X contient A ;
      `inverse`    — A.X contient B  <=>  B.Y contient A, ou Y est le champ
                     oppose declare. « A prolonge B » n implique pas « B
                     prolonge A » : il implique « B EST PROLONGE PAR A ».

    Traiter les champs par une TABLE et non par un bloc de code par champ est le
    correctif de fond : la version qui ne regardait qu un seul champ a laisse la
    reciprocite du second sans aucun controle, puis douze moities orphelines —
    un couple non reciproque ne se voit pas en relisant une seule page.
    """
    rid = "reciprocite"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    if ctx.champ_identite is None:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = mo.severite(rid)
    codes = tuple(mo.codes(rid))
    declares = mo.champs_a_reciprocite()
    champs = mo.regle(rid).get("champs") or sorted(declares)
    if not champs:
        r.etat(rid, constat.NON_APPLICABLE)
        return

    vues_pages, couples = 0, 0
    for p in ctx.lisibles:
        nom = str(p.fm.get(ctx.champ_identite) or p.chemin)
        porte = sum(len(vault.cibles_du_champ(p.fm, c)) for c in champs)
        if porte:
            vues_pages += 1
            couples += porte
        for champ in champs:
            rec = declares.get(champ) or {}
            mode = rec.get("mode", "symetrique")
            oppose = rec.get("champ", champ) if mode == "inverse" else champ
            for cible in sorted(vault.cibles_du_champ(p.fm, champ)):
                if cible not in ctx.par_identite:
                    r.ajoute(rid, sev,
                             f"`{champ}:` cite `{cible}`, absent de l'index (page "
                             f"inexistante, renommée ou hors périmètre)",
                             p.chemin, cle=champ, codes=codes)
                    continue
                retour = vault.cibles_du_champ(ctx.par_identite[cible], oppose)
                if nom not in retour:
                    mot = ("non réciproque" if mode == "symetrique"
                           else f"sans son inverse ({mode})")
                    r.ajoute(rid, sev,
                             f"`{champ}:` cite `{cible}` {mot} — manque `{nom}` "
                             f"dans son `{oppose}:`",
                             p.chemin, cle=champ, codes=codes)
    r.population(rid, vues_pages, objets=couples,
                 objet="couple cité dans un champ à réciprocité")


# --------------------------------------------------------------------------- #
# 2 — chemin_categorie
# --------------------------------------------------------------------------- #
def chemin_categorie(ctx: Contexte, r: Rapport) -> None:
    """Le dossier d une page correspond a sa valeur de l axe de rangement.

    Sur un axe EXCLUSIF, la comparaison est directe : une valeur, un dossier.
    Sur un axe NON EXCLUSIF, elle change de nature, et c est la rupture 3 :

      - le PREFIXE TRANSVERSAL, s il est porte, l emporte sur tout le reste ;
      - la REGLE DE MAJORITE dit que la page vit dans le dossier de la valeur
        qui la rassemble le plus. Cette phrase est editoriale ; ce que le
        validateur en verifie, c est que le dossier se derive d une valeur que la
        page PORTE VRAIMENT. Il refuse un dossier qui ne correspond a aucune, et
        laisse le choix a l auteur ;
      - une page SANS valeur d axe n a pas de chemin a deriver : elle est
        ECARTEE et COMPTEE comme telle, jamais ecartee en silence. Un role qui
        exige la valeur la fera echouer ailleurs — `gabarit_par_role`.
    """
    rid = "chemin_categorie"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    sev = mo.severite(rid)
    codes = tuple(mo.codes(rid))

    for message in ctx.promus_sans_libelle:
        r.ajoute(rid, sev, f"{message} — le dossier n'est pas dérivable",
                 cle="promotion", codes=codes)

    sans_valeur, confrontees = 0, 0
    for p in ctx.lisibles:
        if p.role not in mo.roles or not mo.porte_l_axe_de_rangement(p.role):
            continue
        vals = chemins.valeurs_d_axe(p.fm, mo)
        if not vals:
            sans_valeur += 1
            continue
        confrontees += 1
        if len(vals) > 1 and mo.exclusif:
            r.ajoute(rid, sev,
                     f"`{mo.champ_rangement}:` porte {len(vals)} valeurs alors que "
                     f"l'axe est déclaré exclusif : {vals}", p.chemin, codes=codes)
            continue
        if len(vals) > 1 and not mo.regle_de_majorite:
            r.ajoute(rid, sev,
                     f"`{mo.champ_rangement}:` porte {len(vals)} valeurs et l'axe "
                     f"ne déclare aucune règle de majorité — chemin indérivable",
                     p.chemin, codes=codes)
            continue

        transversales = [v for v in vals if chemins.est_transversale(v, mo)]
        retenues = transversales or vals
        attendus: list[str] = []
        inconnues: list[str] = []
        for v in retenues:
            d = chemins.dossier_attendu(v, ctx.promus, mo)
            if d is None:
                inconnues.append(v)
            else:
                attendus.append(d)
        if inconnues:
            r.ajoute(rid, sev,
                     f"`{mo.champ_rangement}: {', '.join(inconnues)}` hors des "
                     f"préfixes déclarés — dossier indérivable", p.chemin, codes=codes)
            continue
        if p.dossier in attendus:
            continue
        if transversales:
            r.ajoute(rid, sev,
                     f"porte le préfixe transversal `{mo.prefixe_transversal}` et "
                     f"attend `{attendus[0]}/` — déplacement à faire",
                     p.chemin, codes=codes)
        elif len(attendus) == 1:
            r.ajoute(rid, sev,
                     f"`{mo.champ_rangement}: {retenues[0]}` attend "
                     f"`{attendus[0]}/` — déplacement à faire", p.chemin, codes=codes)
        else:
            r.ajoute(rid, sev,
                     f"aucune de ses {len(retenues)} valeurs ne mène à son dossier "
                     f"— candidats : {sorted(set(attendus))}", p.chemin, codes=codes)
    r.population(rid, confrontees)
    if sans_valeur:
        r.note(f"{rid} : {sans_valeur} page(s) sans valeur d'axe de rangement — "
               f"écartées de la dérivation, jamais en silence")


# --------------------------------------------------------------------------- #
# 3 — completude_du_hub
# --------------------------------------------------------------------------- #
def completude_du_hub(ctx: Contexte, r: Rapport) -> None:
    """Toute page d un role `apparait_dans_le_hub` figure dans le hub de son dossier.

    Absente avant sa mesure : le validateur verifiait « atteignable depuis un
    hub », jamais « presente dans le hub de SON dossier ». La zone AUTO d un hub
    etant generee, ce que la regle attrape est un hub NON regenere, ou absent.
    """
    rid = "completude_du_hub"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    sev = mo.severite(rid)
    codes = tuple(mo.codes(rid))
    roles = mo.regle(rid).get("roles") or [rid_ for rid_ in mo.roles
                                           if mo.apparait_dans_le_hub(rid_)]
    r.population(rid, sum(len(ctx.pages_du_role(x)) for x in roles))
    for rid_role in roles:
        for p in ctx.pages_du_role(rid_role):
            hub = chemins.hub_du_dossier(p.dossier)
            if hub not in ctx.cibles_des_hubs:
                r.ajoute(rid, sev, f"aucun hub `{hub}` pour ce dossier",
                         p.chemin, codes=codes)
            elif p.stem not in ctx.cibles_des_hubs[hub]:
                r.ajoute(rid, sev, f"absente du hub de son dossier `{hub}`",
                         p.chemin, codes=codes)


# --------------------------------------------------------------------------- #
# 4 — voisinage_declare
# --------------------------------------------------------------------------- #
def voisinage_declare(ctx: Contexte, r: Rapport) -> None:
    """Un champ de voisinage vide dans un dossier peuple est SIGNALE.

    Le perimetre est l ensemble des roles dont le gabarit AUTORISE le champ : la
    regle nomme un champ, pas un role, et un champ dit deja qui le porte.
    """
    rid = "voisinage_declare"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    champ = mo.regle(rid).get("champ")
    if not champ:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = mo.severite(rid)
    codes = tuple(mo.codes(rid))
    # La population est le nombre de pages ou une violation etait POSSIBLE :
    # une page seule de son role dans son dossier n a pas de voisinage a
    # declarer, et la compter gonflerait le denominateur d une regle qui ne l a
    # jamais regardee.
    entourees = 0
    for rid_role in mo.roles_qui_portent(champ):
        for p in ctx.pages_du_role(rid_role):
            voisins = ctx.pages_par_dossier_et_role[(p.dossier, rid_role)] - 1
            if voisins > 0:
                entourees += 1
            if not p.fm.get(champ) and voisins > 0:
                r.ajoute(rid, sev,
                         f"`{champ}:` vide alors que le dossier porte {voisins} "
                         f"autre(s) page(s) du même rôle — voisinage non déclaré",
                         p.chemin, codes=codes)
    r.population(rid, entourees)


# --------------------------------------------------------------------------- #
# 5 — redirection_sourcee
# --------------------------------------------------------------------------- #
def redirection_sourcee(ctx: Contexte, r: Rapport) -> None:
    """Une cellule de la colonne negative qui REDIRIGE vers une page fichee la cite.

    La forme qui tient est une CONJONCTION, et c est le resultat d une mesure,
    pas d un gout : la POSITION (une redirection, marquee par la fleche) dit ou
    regarder, la CONDITION (la cible est couverte par une page du brain) dit
    quoi exiger. Les trois formulations plus simples ont ete mesurees et
    ecartees — le manifeste porte leurs comptes.
    """
    rid = "redirection_sourcee"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    regle = mo.regle(rid)
    marqueur = regle.get("marqueur")
    titres = regle.get("sections") or []
    colonne = regle.get("colonne")
    if not (marqueur and titres and colonne):
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = mo.severite(rid)
    codes = tuple(mo.codes(rid))
    re_marqueur = re.compile(marqueur)

    # Cette regle ne mesure pas des pages : elle mesure des CELLULES. Les deux
    # comptes sont declares, parce que « 1 violation sur 1 388 » et « 1
    # violation sur 337 » ne disent pas la meme chose, et que le plancher de
    # durcissement, lui, se lit en pages.
    porteuses, cellules = 0, 0
    for rid_role in sorted(mo.roles):
        section = mo.section_de_genre(rid_role, GENRE_DECISION)
        if section is None:
            continue
        positif = section.get("colonne_positive") or ""
        for p in ctx.pages_du_role(rid_role):
            vues_ici = sum(len(vault.cellules_de_colonne(p.sections.get(t),
                                                         positif, colonne))
                           for t in titres)
            if vues_ici:
                porteuses += 1
                cellules += vues_ici
            moi = {str(p.fm.get(ctx.champ_identite) or "").lower()}
            if ctx.champ_alias:
                moi |= {str(a).lower() for a in p.fm.get(ctx.champ_alias) or []}
            for titre in titres:
                sec = p.sections.get(titre)
                for cellule in vault.cellules_de_colonne(sec, positif, colonne):
                    if not re_marqueur.search(cellule):
                        continue                    # ce n est pas une redirection
                    apres = re_marqueur.split(cellule, maxsplit=1)[1]
                    if vault.LIEN_RE.search(apres):
                        continue                    # deja sourcee
                    for cle, canon in ctx.index_des_unites.items():
                        if cle in moi or canon.lower() in moi:
                            continue                # la page elle-meme
                        if re.search(r"(?<![\w.-])" + re.escape(cle) + r"(?![\w.-])",
                                     apres, re.I):
                            r.ajoute(rid, sev,
                                     f"redirection `{colonne}` vers `{canon}`, qui "
                                     f"est fiché, sans son wikilink — "
                                     f"« {cellule[:80]} »",
                                     p.chemin, codes=codes)
                            break
    r.population(rid, porteuses, objets=cellules,
                 objet=f"cellule de la colonne « {colonne} »")


# --------------------------------------------------------------------------- #
# 6 — reinjection_du_resume
# --------------------------------------------------------------------------- #
def reinjection_du_resume(ctx: Contexte, r: Rapport) -> None:
    """Chaque puce d une section adossee a un champ commence par le resume COURANT de sa cible.

    Le champ designe `fonction: resume_court` est RECOPIE, jamais retape, chez
    tous ses citeurs. Une puce dont l entree n est pas une cible du champ est
    EXEMPTEE : elle explique au lieu de lister, et c est une forme recommandee.
    """
    rid = "reinjection_du_resume"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    champ_resume = mo.regle(rid).get("champ_resume") or ctx.champ_resume
    if not champ_resume:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = mo.severite(rid)
    codes = tuple(mo.codes(rid))
    titres_vises = mo.regle(rid).get("sections")

    porteuses, puces = 0, 0
    for p in ctx.lisibles:
        if p.role not in mo.roles:
            continue
        vues_ici = 0
        for titre, champ in mo.sections_adossees(p.role):
            if titres_vises and titre not in titres_vises:
                continue
            cibles = vault.cibles_du_champ(p.fm, champ)
            if not cibles:
                continue
            sec = p.sections.get(titre) or ""
            for ligne in sec.splitlines():
                m = vault.PUCE_LIEN_RE.match(ligne)
                if not m:
                    continue
                cible = (m.group(2) or m.group(1)).split("/")[-1]
                if cible not in cibles:
                    continue                        # puce hors du champ — exemptee
                vues_ici += 1
                attendu = vault.normalise_resume(ctx.resume(cible))
                if attendu and not vault.normalise_resume(m.group(3)).startswith(attendu):
                    r.ajoute(rid, sev,
                             f"la puce de `{cible}` en `{titre}` ne commence pas "
                             f"par son `{champ_resume}:` courant « {attendu} »",
                             p.chemin, cle=titre, codes=codes)
        if vues_ici:
            porteuses += 1
            puces += vues_ici
    r.population(rid, porteuses, objets=puces,
                 objet="puce adossée à une cible du champ")


# --------------------------------------------------------------------------- #
# 7 — etiquettes_fermees
# --------------------------------------------------------------------------- #
def etiquettes_fermees(ctx: Contexte, r: Rapport) -> None:
    """Une section `genre: etiquetee` a un vocabulaire FERME.

    La severite se lit PAR SECTION quand le manifeste la declare ainsi : deux
    sections du meme genre peuvent etre l une a zero violation et l autre a
    cinq, et la seconde reste en avertissement AVEC SON MOTIF. Durcir en
    ouvrant le vocabulaire serait ajouter une exception pour faire passer la
    regle.
    """
    rid = "etiquettes_fermees"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    codes = tuple(mo.codes(rid))
    titres_vises = mo.regle(rid).get("sections")
    for rid_role in sorted(mo.roles):
        for section in mo.sections_de_genre(rid_role, GENRE_ETIQUETEE):
            titre = mo.titre(section)
            if titres_vises and titre not in titres_vises:
                continue
            permises = set(section.get("permises") or [])
            obligatoires = set(section.get("obligatoires") or [])
            sev = mo.severite(rid, titre)
            # La severite se lit par section, donc la population aussi : deux
            # sections du meme genre n ont ni le meme denominateur ni le meme
            # verdict, et melanger les deux rendrait la mesure inutilisable.
            porteuses, etiq = 0, 0
            for p in ctx.pages_du_role(rid_role):
                sec = p.sections.get(titre)
                vues = vault.etiquettes(sec)
                if sec is not None:
                    porteuses += 1
                    etiq += len(vues)
                for lab in vues:
                    if lab not in permises:
                        r.ajoute(rid, sev,
                                 f"`{titre}` porte l'étiquette `{lab}`, hors du "
                                 f"vocabulaire fermé {sorted(permises)}",
                                 p.chemin, cle=titre, codes=codes)
                manque = obligatoires - set(vues)
                if sec is not None and manque:
                    r.ajoute(rid, sev,
                             f"`{titre}` sans l'étiquette {sorted(manque)}",
                             p.chemin, cle=titre, codes=codes)
            r.population(rid, porteuses, cle=titre, objets=etiq,
                         objet=f"étiquette lue en `{titre}`")


# --------------------------------------------------------------------------- #
# 8 — citation_unique
# --------------------------------------------------------------------------- #
def citation_unique(ctx: Contexte, r: Rapport) -> None:
    """Une meme cible ne se LISTE pas dans deux sections de liste de liens.

    « Listee » veut dire ENTREE de puce, jamais lien cite dans une phrase. La
    restriction n est pas un assouplissement de confort : sans elle, la regle
    punirait la forme recommandee pour une section vide, ou le lien EXPLIQUE au
    lieu de LISTER — et le defaut d origine reste attrape.
    """
    rid = "citation_unique"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    titres_vises = mo.regle(rid).get("sections")
    if not titres_vises:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = mo.severite(rid)
    codes = tuple(mo.codes(rid))
    # Une page qui ne porte qu UNE des sections visees ne peut pas citer deux
    # fois : la population est celle des pages qui en portent au moins DEUX.
    exposees, entrees = 0, 0
    for rid_role in sorted(mo.roles):
        titres = [mo.titre(s) for s in mo.corps(rid_role)
                  if s.get("genre") == GENRE_LISTE and mo.titre(s) in titres_vises]
        if not titres:
            continue
        for p in ctx.pages_du_role(rid_role):
            listee: dict[str, set[str]] = collections.defaultdict(set)
            portees = 0
            for titre in titres:
                sec = p.sections.get(titre)
                if sec is None:
                    continue
                portees += 1
                for cible in vault.entrees_de_puces(sec):
                    listee[cible].add(titre)
            if portees > 1:
                exposees += 1
                entrees += sum(len(ou) for ou in listee.values())
            for cible, ou in sorted(listee.items()):
                if len(ou) > 1:
                    r.ajoute(rid, sev,
                             f"`{cible}` listé dans {sorted(ou)} — une cible ne se "
                             f"liste que dans une section", p.chemin, codes=codes)
    r.population(rid, exposees, objets=entrees, objet="entrée de puce")


# --------------------------------------------------------------------------- #
# 9 — bandeau_a_jour
# --------------------------------------------------------------------------- #
def bandeau_a_jour(ctx: Contexte, r: Rapport) -> None:
    """La zone AUTO du bandeau concorde avec le frontmatter — DELEGUEE.

    Le manifeste declare qui la porte : `porte_par:`. Verifier cette regle, c est
    REGENERER le bandeau et comparer les octets — donc posseder le generateur,
    qui vit dans `brainkit.generer`. Le validateur ne la reimplemente pas a
    moitie : il declare a haute voix qu il la delegue, et par qui. Une regle
    qu on croit tenue sans qu aucun code ne la tienne est le pire des deux
    mondes.

    Le porteur se LIT dans `porte_par:` depuis le lot 4, et non plus dans
    `code:`. C etait la remontee 10 du lot 3 : `code:` melangeait provenance et
    delegation, et le moteur devinait laquelle des deux par convention. Le repli
    sur `code:` reste, pour un manifeste ecrit avant l arbitrage.
    """
    rid = "bandeau_a_jour"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    porteur = mo.porte_par(rid) or ", ".join(mo.codes(rid)) or "un autre outil"
    r.etat(rid, f"{constat.DELEGUEE} — portée par `{porteur}`")


# --------------------------------------------------------------------------- #
# 10 — anti_repetition
# --------------------------------------------------------------------------- #
def anti_repetition(ctx: Contexte, r: Rapport) -> None:
    """La section de definition ne redit pas ce que le bandeau affiche deja.

    NON SCRIPTABLE, et le manifeste l ecrit : les valeurs rendues sont des mots
    ordinaires de la langue. La regle ne tourne donc que sur des MOTIFS BORNES,
    declares un par un, et chaque groupe de motifs est indexe PAR LA COLONNE DU
    BANDEAU qu il vise — c est la colonne qui dit quel champ lire. La colonne
    dont aucun motif n est declare est deliberement hors de la regle.

    Elle sert de relecture assistee, et c est tout ce qu elle peut etre.
    """
    rid = "anti_repetition"
    mo = ctx.mo
    if not mo.regle_active(rid):
        r.etat(rid, constat.INACTIVE)
        return
    bornes = mo.regle(rid).get("motifs_bornes") or {}
    colonnes = mo.bandeau.get("colonnes") or []
    porte_par = mo.bandeau.get("porte_par") or []
    if not (bornes and colonnes and porte_par):
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = mo.severite(rid)
    codes = tuple(mo.codes(rid))

    # {groupe de motifs : le champ que sa colonne de bandeau lit}
    par_colonne = {_sans_accent(str(c.get("titre"))): c.get("source")
                   for c in colonnes}
    groupes: list[tuple[str, str, dict]] = []
    for cle, table in bornes.items():
        if cle.startswith("motif") or cle.startswith("note"):
            continue
        champ = par_colonne.get(_sans_accent(cle))
        if not champ or not isinstance(table, dict):
            r.note(f"{rid} : le groupe de motifs `{cle}` ne correspond à aucune "
                   f"colonne de bandeau — non contrôlé")
            continue
        groupes.append((cle, champ, table))
    if not groupes:
        r.etat(rid, constat.NON_APPLICABLE)
        return

    # La population n est PAS « les pages qui portent la section » : c est
    # celles dont au moins une valeur de bandeau a un motif borne declare. Une
    # page dont la licence n est dans aucune table n a jamais ete regardee.
    exposees, controles = 0, 0
    for rid_role in porte_par:
        section = mo.section_de_genre(rid_role, GENRE_PROSE)
        if section is None:
            continue
        titre = mo.titre(section)
        for p in ctx.pages_du_role(rid_role):
            texte = p.sections.get(titre) or ""
            vus_ici = 0
            for _cle, champ, table in groupes:
                valeur = p.fm.get(champ)
                motif = table.get(valeur) if isinstance(valeur, str) else None
                if motif is None:
                    continue
                vus_ici += 1
                if re.search(motif, texte, re.I):
                    r.ajoute(rid, sev,
                             f"`{titre}` redit peut-être `{champ}: {valeur}`, déjà "
                             f"au bandeau — à relire", p.chemin, codes=codes)
            if vus_ici:
                exposees += 1
                controles += vus_ici
    r.population(rid, exposees, objets=controles,
                 objet="valeur de bandeau à motif borné déclaré")


IMPLEMENTEES = {
    "reciprocite": reciprocite,
    "chemin_categorie": chemin_categorie,
    "completude_du_hub": completude_du_hub,
    "voisinage_declare": voisinage_declare,
    "redirection_sourcee": redirection_sourcee,
    "reinjection_du_resume": reinjection_du_resume,
    "etiquettes_fermees": etiquettes_fermees,
    "citation_unique": citation_unique,
    "bandeau_a_jour": bandeau_a_jour,
    "anti_repetition": anti_repetition,
}
