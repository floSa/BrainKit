"""socle.py — les regles de SOCLE : celles hors des dix, que le vault a exigees.

La liste des dix est FERMEE par le kit. Celle-ci est OUVERTE : ce sont les
regles qu un vault reel a rendues necessaires, declarees dans
`regles_de_socle[]` avec leur severite et leur enonce. Chacune ci-dessous est
branchee par son `id` : **une regle que le manifeste ne declare pas ne tourne
pas, et l inventaire le dit.**

Correspondance avec l ancien code — cf. `design/03-validation.md` pour la table
complete et pour ce qui a ete jete.
"""

from __future__ import annotations

import collections

from . import chemins, conditions, constat, vault
from .constat import Rapport
from .contexte import Contexte


# --------------------------------------------------------------------------- #
def frontmatter_lisible(ctx: Contexte, r: Rapport) -> None:
    """R17 — un frontmatter illisible est une ERREUR, jamais une absence.

    Ce n etait pas une regle souple a durcir, c etait L ABSENCE DE REGLE. Une
    page qui ne parsait pas etait silencieusement sautee par les DEUX
    validateurs : hors du total, hors de toutes les autres regles, liens non
    resolus, chemin non confronte a sa valeur d axe. Un resume non quote
    contenant « : » suffisait, et RIEN ne le signalait — le vault restait vert.
    """
    rid = "frontmatter_lisible"
    sev = ctx.mo.severite(rid)
    r.population(rid, len(ctx.pages))
    for p in ctx.pages:
        if p.illisible:
            r.ajoute(rid, sev, f"frontmatter illisible — {p.illisible}",
                     p.chemin, codes=("R17",))


# --------------------------------------------------------------------------- #
def gabarit_par_role(ctx: Contexte, r: Rapport) -> None:
    """R3 + R16 — le contrat de frontmatter d un role.

    Quatre choses, une seule regle, parce que le manifeste n en declare qu une :
      - un `role:` inconnu ou absent est refuse — plus de page sans gabarit ;
      - les champs `requis` sont presents et NON VIDES ;
      - `autorises` est EXACT : tout champ hors liste fait echouer la page ;
      - un champ `conditionnels[]` respecte le SENS de sa condition.

    Le sens par defaut est `permet` : le champ n existe QUE si la condition
    tient. `exige` est l autre sens, et il n est ecrit nulle part dans les deux
    remplissages — cf. `design/03-validation.md`, arbitrage 1.
    """
    rid = "gabarit_par_role"
    sev = ctx.mo.severite(rid)
    mo = ctx.mo
    r.population(rid, len(ctx.lisibles))
    for p in ctx.lisibles:
        if p.role not in mo.roles:
            r.ajoute(rid, sev,
                     f"`role: {p.role or '(absent)'}` sans gabarit déclaré "
                     f"(connus : {sorted(mo.roles)})", p.chemin, codes=("R3",))
            continue
        for champ in mo.requis(p.role):
            if not vault.non_vide(p.fm.get(champ)):
                r.ajoute(rid, sev, f"champ requis manquant `{champ}`",
                         p.chemin, codes=("R3",))
        extra = set(map(str, p.fm.keys())) - mo.autorises(p.role)
        if extra:
            r.ajoute(rid, sev, f"champ(s) hors du gabarit déclaré {sorted(extra)}",
                     p.chemin, codes=("R3",))

        for c in mo.conditionnels(p.role):
            champ, si, sens = c["champ"], c["si"], c["sens"]
            tient = conditions.evalue(si, p.fm)
            present = champ in p.fm
            if tient is None:
                r.note(f"{p.chemin} : condition `{si}` non évaluable — le champ "
                       f"`{champ}` n'est pas contrôlé sur cette page")
                continue
            if sens == "permet" and present and not tient:
                r.ajoute(rid, sev,
                         f"`{champ}:` présent alors que « {si} » est faux — le "
                         f"champ n'existe que si la condition tient",
                         p.chemin, cle="conditionnels", codes=("R16",))
            elif sens == "exige" and tient and not vault.non_vide(p.fm.get(champ)):
                r.ajoute(rid, sev,
                         f"`{champ}:` absent alors que « {si} » tient — la "
                         f"condition l'exige",
                         p.chemin, cle="conditionnels", codes=())


# --------------------------------------------------------------------------- #
def vocabulaire_ferme(ctx: Contexte, r: Rapport) -> None:
    """R4, R14 (+ R14b) — toute valeur d un champ enumere est declaree.

    Le vocabulaire se lit dans le MANIFESTE quand un axe le porte, dans un
    FICHIER quand `champs.<x>.source` pointe vers `vocabulaires.<nom>`. Un
    vocabulaire declare `ferme` et illisible est signale : traite comme vide il
    ferait passer n importe quoi.

    Le champ dont la source est `roles[].id` est ECARTE ici : son vocabulaire
    est celui des roles, et `gabarit_par_role` le refuse deja — le compter deux
    fois doublerait chaque violation.

    R14b, l ABSENCE d une valeur d axe de nature, est portee ici parce que le
    manifeste la range dans les codes de cette regle — mais sa severite se lit
    OU ELLE VIT : `axes.nature.vide_autorise`. Un champ vide est le seul signal
    prevu pour « l arbre de decision n a pas tranche » ; une valeur inventee est
    une faute, un champ vide est une question ouverte. Cf.
    `design/03-validation.md`, *Remontees*.
    """
    rid = "vocabulaire_ferme"
    sev = ctx.mo.severite(rid)
    mo = ctx.mo

    for nom, voc in ctx.vocabulaires.items():
        if voc.ferme and voc.illisible:
            r.ajoute(rid, sev,
                     f"vocabulaire fermé `{nom}` illisible — {voc.illisible}",
                     codes=("R4",))

    enumerees, valeurs_lues = 0, 0
    for p in ctx.lisibles:
        if p.role not in mo.roles:
            continue
        vues_ici = 0
        for champ in sorted(map(str, p.fm.keys())):
            d = mo.champ(champ)
            typ = d.get("type")
            if typ not in ("enum", "liste_enum"):
                continue
            if str(d.get("source") or "").strip() == "roles[].id":
                continue
            brut = p.fm.get(champ)
            if brut is None:
                continue
            vues_ici += len(vault.valeurs(brut)) or 1
            if typ == "liste_enum" and not isinstance(brut, list):
                r.ajoute(rid, sev,
                         f"`{champ}: {brut}` doit être une liste, pas un scalaire",
                         p.chemin, codes=("R14",))
                continue
            legales = mo.vocabulaire(champ)
            if legales is None:
                src = mo.source_de_vocabulaire(champ)
                voc = ctx.vocabulaires.get(src) if src else None
                if voc is None or not voc.ferme or voc.valeurs is None:
                    continue
                legales = voc.valeurs
            for v in vault.valeurs(brut):
                if v not in legales:
                    r.ajoute(rid, sev,
                             f"`{champ}: {v}` hors du vocabulaire déclaré",
                             p.chemin, codes=("R4",))
        if vues_ici:
            enumerees += 1
            valeurs_lues += vues_ici
    r.population(rid, enumerees, objets=valeurs_lues,
                 objet="valeur d'un champ énuméré")

    # --- R14b : l ABSENCE d une valeur d axe de nature -------------------- #
    if mo.champ_nature and mo.nature_portee_par:
        sev_vide = (constat.AVERTISSEMENT if mo.nature_vide_autorise
                    else ctx.mo.severite(rid))
        r.population(rid, sum(len(ctx.pages_du_role(x))
                              for x in mo.nature_portee_par), cle="axe_vide")
        for rid_role in mo.nature_portee_par:
            for p in ctx.pages_du_role(rid_role):
                if mo.champ_nature not in p.fm:
                    r.ajoute(rid, sev_vide,
                             f"aucune `{mo.champ_nature}:` — l'arbre de décision "
                             f"n'a pas tranché, ou n'a pas été déroulé",
                             p.chemin, cle="axe_vide", codes=("R14b",))


# --------------------------------------------------------------------------- #
def nom_egal_fichier(ctx: Contexte, r: Rapport) -> None:
    """R9 — le champ d IDENTITE est le nom du fichier.

    Exemption declaree par le manifeste (`champs.<x>.exemption`) : un nom
    portant un caractere illegal en nom de fichier NE PEUT PAS l etre.
    """
    rid = "nom_egal_fichier"
    if ctx.champ_identite is None:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = ctx.mo.severite(rid)
    r.population(rid, sum(1 for p in ctx.lisibles
                          if p.fm.get(ctx.champ_identite)))
    for p in ctx.lisibles:
        nom = p.fm.get(ctx.champ_identite)
        if not nom:
            continue
        nom = str(nom)
        if vault.FS_ILLEGAL & set(nom):
            continue
        if nom != p.stem:
            r.ajoute(rid, sev,
                     f"`{ctx.champ_identite}: {nom}` != nom de fichier `{p.stem}`",
                     p.chemin, codes=("R9",))


# --------------------------------------------------------------------------- #
def liens_resolus(ctx: Contexte, r: Rapport) -> None:
    """R2 — aucun wikilink mort, dans le corps ET dans le frontmatter.

    Le corps seul ne suffit pas : un renommage ou une suppression laissait un
    lien mort en frontmatter sans que rien ne le dise.
    """
    rid = "liens_resolus"
    sev = ctx.mo.severite(rid)
    liantes, liens = 0, 0
    for p in ctx.lisibles:
        n_ici = len(p.liens_du_corps()) + len(p.liens_du_frontmatter())
        if n_ici:
            liantes += 1
            liens += n_ici
        for t in p.liens_du_corps():
            if not vault.cible_resolue(t, ctx.noms_resolvables, ctx.racine,
                                       ctx.extensions):
                r.ajoute(rid, sev, f"lien mort [[{t}]]", p.chemin, codes=("R2",))
        for cle, t in p.liens_du_frontmatter():
            if not vault.cible_resolue(t, ctx.noms_resolvables, ctx.racine,
                                       ctx.extensions):
                r.ajoute(rid, sev, f"`{cle}:` lien mort [[{t}]]", p.chemin,
                         codes=("R2",))
    r.population(rid, liantes, objets=liens, objet="wikilink")


# --------------------------------------------------------------------------- #
def sources_d_aiguillage(ctx: Contexte) -> tuple[list, str]:
    """Les fichiers de la racine qui AIGUILLENT. Rend (chemins, comment on le sait).

    LOT 8 — remontee 1 du lot 5, tenue ouverte par la remontee 5 du lot 6. Le
    bloc `racine:` existe depuis le lot 5 ; aucune regle ne le lisait, et
    `page_atteignable` prenait `racine.glob("*.md")` : TOUT `.md` pose a la
    racine elargissait silencieusement l atteignabilite de tous les hubs de
    premier niveau. Un brouillon suffisait.

    Le perimetre se LIT maintenant dans `racine.pages[].aiguille`. Le repli sur
    le glob reste, et il n est pas une precaution de confort : un manifeste
    ecrit avant le lot 5 n a pas le bloc, et la regle doit y garder le
    comportement qu elle avait — un durcissement silencieux sur un manifeste
    muet serait exactement ce que le lot 8 interdit.

    Ce que le branchement a COUTE, mesure avant de le poser : sur le vault d'origine, 9
    `.md` a la racine dont UN seul aiguille (`Home.md`) — et ZERO page perd son
    atteignabilite quand les huit autres cessent de compter. Sur BrainRef, 4
    fichiers a la racine, un seul aiguille, et les 13 constats sont les MEMES
    dans les deux perimetres. Le durcissement etait gratuit, et c est parce
    qu il l etait qu il est pose.
    """
    bloc = ctx.mo.m.get("racine") or {}
    declarees = bloc.get("pages")
    if not declarees:
        return sorted(ctx.racine.glob("*.md")), "tout `.md` de la racine (aucun `racine.pages[]` déclaré)"
    chemins_ = [ctx.racine / e["fichier"] for e in declarees if e.get("aiguille")]
    return ([c for c in chemins_ if c.is_file()],
            "les pages `racine.pages[].aiguille: true` du manifeste")


def page_atteignable(ctx: Contexte, r: Rapport) -> None:
    """R7 — toute page est atteignable depuis un hub.

    Les pages d aiguillage sont les pages du role `fonction: hub`, PLUS les
    fichiers de la racine que le manifeste DECLARE aiguilleurs. La racine n est
    pas un dossier de pages — le perimetre s enumere par la negative — et c est
    la que le vault pose sa porte d entree : ce sont les hubs de premier niveau
    qui n ont pas de parent, et seule la porte d entree les cite.
    """
    rid = "page_atteignable"
    sev = ctx.mo.severite(rid)
    qualifies: set[str] = set()
    nus: set[str] = set()
    textes = [p.corps for p in ctx.lisibles if p.role == ctx.mo.role_hub]
    sources, comment = sources_d_aiguillage(ctx)
    for md in sources:
        textes.append(md.read_text(encoding="utf-8"))
    r.note(f"{rid} : périmètre d'aiguillage — {comment} ({len(sources)} fichier(s))")
    r.population(rid, len(ctx.lisibles))
    for txt in textes:
        for t in vault.LIEN_RE.findall(txt):
            t = t.strip().split("#")[0]
            (qualifies if "/" in t else nus).add(t.lower())
    for p in ctx.lisibles:
        if p.chemin[:-3].lower() in qualifies or p.stem.lower() in nus:
            continue
        r.ajoute(rid, sev, "atteignable depuis aucun hub", p.chemin, codes=("R7",))


# --------------------------------------------------------------------------- #
def hub_par_niveau(ctx: Contexte, r: Rapport) -> None:
    """TOUT niveau du chemin porte son hub, pas seulement la feuille."""
    rid = "hub_par_niveau"
    sev = ctx.mo.severite(rid)
    mo = ctx.mo
    dossiers = {p.dossier for p in ctx.lisibles
                if p.role in mo.roles and mo.porte_l_axe_de_rangement(p.role)}
    manquants: set[str] = set()
    niveaux_vus: set[str] = set()
    for d in dossiers:
        for niveau in chemins.niveaux(d):
            niveaux_vus.add(niveau)
            if niveau not in ctx.hubs:
                manquants.add(niveau)
    r.population(rid, len(dossiers), objets=len(niveaux_vus),
                 objet="niveau de chemin à couvrir")
    for niveau in sorted(manquants):
        r.ajoute(rid, sev,
                 f"`{niveau}/` : aucune page `{mo.role_hub}` à son nom",
                 codes=("check_arbo",))


# --------------------------------------------------------------------------- #
def unicite_du_nom_de_fichier(ctx: Contexte, r: Rapport) -> None:
    """Un nom de fichier est unique dans le vault, a la casse pres.

    C est la SEULE contrainte que la convention de wikilink NU impose, et elle
    vaut aussi pour chaque hub a creer. Un lien qualifie porte un chemin, donc
    casse au premier deplacement.

    L unicite se compte PAR EXTENSION, et ce n est pas un assouplissement : une
    vue embarquee porte le MEME nom que la page qui l embarque, par declaration
    du manifeste (`vue_embarquee.embed: "![[<meme nom>.base]]"`). C est
    l extension qui les distingue, et c est pour cette raison exacte qu un
    wikilink resout sur le nom COMPLET autant que sur le stem. Compter les deux
    ensemble ferait de la convention une violation, quarante-sept fois.
    """
    rid = "unicite_du_nom_de_fichier"
    sev = ctx.mo.severite(rid)
    lots: dict[str, dict[str, list[str]]] = {}
    lots[".md"] = collections.defaultdict(list)
    for p in ctx.pages:
        lots[".md"][p.stem.lower()].append(p.chemin)
    ext = ctx.mo.extension_de_vue()
    if ext:
        lots[ext] = collections.defaultdict(list)
        for f in sorted(ctx.racine.rglob(f"*{ext}")):
            parts = f.relative_to(ctx.racine).parts
            if parts and parts[0] in vault.HORS_VAULT:
                continue
            lots[ext][f.stem.lower()].append(f.relative_to(ctx.racine).as_posix())
    r.population(rid, len(ctx.pages),
                 objets=sum(len(x) for x in lots.values()),
                 objet="nom de fichier, par extension")
    for extension, par_nom in sorted(lots.items()):
        for nom, lot in sorted(par_nom.items()):
            if len(lot) > 1:
                r.ajoute(rid, sev,
                         f"`{nom}{extension}` porté par {len(lot)} fichiers : "
                         f"{sorted(lot)} — un lien nu ne résout plus de façon "
                         f"déterministe")


# --------------------------------------------------------------------------- #
def taille_avertissement(ctx: Contexte, r: Rapport) -> None:
    """Une page au-dela de `roles[].taille_avertissement` lignes suggere une scission."""
    rid = "taille_avertissement"
    sev = ctx.mo.severite(rid)
    r.population(rid, sum(1 for p in ctx.lisibles
                          if (ctx.mo.roles.get(p.role) or {}).get(
                              "taille_avertissement")))
    for p in ctx.lisibles:
        limite = (ctx.mo.roles.get(p.role) or {}).get("taille_avertissement")
        if not limite:
            continue
        n = p.corps.count("\n")
        if n > int(limite):
            r.ajoute(rid, sev, f"{n} lignes (> {limite}) → envisager une sous-note",
                     p.chemin)


# --------------------------------------------------------------------------- #
def collision_alias(ctx: Contexte, r: Rapport) -> None:
    """R5 — doublon interne d alias, ou alias qui est le nom d une autre page du MEME role.

    Souple par decision d audit : l unicite globale des alias detruirait des
    usages semantiques legitimes.
    """
    rid = "collision_alias"
    if ctx.champ_alias is None or ctx.champ_identite is None:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = ctx.mo.severite(rid)
    r.population(rid, sum(1 for p in ctx.lisibles
                          if p.fm.get(ctx.champ_alias)),
                 objets=sum(len(p.fm.get(ctx.champ_alias) or [])
                            for p in ctx.lisibles), objet="alias déclaré")
    noms: dict[tuple, str] = {}
    for p in ctx.lisibles:
        nom = p.fm.get(ctx.champ_identite)
        if nom:
            noms[(p.role, str(nom).lower())] = p.chemin
    for p in ctx.lisibles:
        bas = [str(a).lower() for a in (p.fm.get(ctx.champ_alias) or [])]
        dup = sorted({a for a in bas if bas.count(a) > 1})
        if dup:
            r.ajoute(rid, sev, f"alias en doublon interne {dup}", p.chemin,
                     codes=("R5",))
        for a in sorted(set(bas)):
            proprio = noms.get((p.role, a))
            if proprio and proprio != p.chemin:
                r.ajoute(rid, sev,
                         f"alias `{a}` est le `{ctx.champ_identite}:` de "
                         f"`{proprio}` (même rôle)", p.chemin, codes=("R5",))


# --------------------------------------------------------------------------- #
def champs_supprimes(ctx: Contexte, r: Rapport) -> None:
    """R25 — aucun champ supprime ne survit HORS de l arbre des pages.

    Cause de la regle : le perimetre des DEUX validateurs etait « les dossiers
    de premier niveau qui portent des pages ». Ni la racine, ni la gouvernance,
    ni les gabarits n y entraient — donc rien ne les relisait, et onze documents
    ont porte deux champs supprimes pendant deux jours sans qu aucune des
    quarante conversations de migration ne s en apercoive.

    Les champs se lisent dans le manifeste : `champs.<x>.deprecated: true` sur
    un champ qu AUCUN `autorises` ne cite. Le perimetre aussi : les `.md` de la
    racine, plus les dossiers de `genere.non_pages` qui ne sont ni caches ni la
    racine de l agent — celle-la porte les journaux de lot, qui CITENT ces
    champs pour raconter leur suppression.
    """
    rid = "champs_supprimes"
    morts = ctx.mo.champs_supprimes()
    if not morts:
        r.etat(rid, "branchée, aucun champ `deprecated: true` hors de tout "
                    "`autorises` — la règle ne peut rien trouver")
        return
    sev = ctx.mo.severite(rid)
    racine_agent = str(((ctx.mo.m.get("agent") or {}).get("racine") or "")).strip("/")
    cibles = sorted(ctx.racine.glob("*.md"))
    for nom in sorted(ctx.mo.non_pages):
        if nom.startswith(".") or nom == racine_agent:
            continue
        d = ctx.racine / nom
        if d.is_dir():
            cibles += sorted(d.rglob("*.md"))
    for md in cibles:
        texte = md.read_text(encoding="utf-8")
        if not texte.startswith("---"):
            continue
        fin = texte.find("---", 3)
        if fin == -1:
            continue
        for ligne in texte[3:fin].splitlines():
            cle = ligne.split(":", 1)[0].strip()
            if cle in morts:
                r.ajoute(rid, sev,
                         f"champ `{cle}:` supprimé par le contrat, encore présent "
                         f"dans le frontmatter",
                         md.relative_to(ctx.racine).as_posix(), codes=("R25",))


# --------------------------------------------------------------------------- #
def couverture_de_section(ctx: Contexte, r: Rapport) -> None:
    """R11, R22 — une section adossee a un champ couvre TOUTES ses cibles.

    Une section `genre: liste_liens` qui declare un `champ:` promet de lister ce
    que ce champ contient. Une cible declaree au frontmatter et absente de la
    section est un demi-lien : le graphe la porte, la page ne la montre pas.
    """
    rid = "couverture_de_section"
    sev = ctx.mo.severite(rid)
    adossees, promesses = 0, 0
    for p in ctx.lisibles:
        if p.role not in ctx.mo.roles:
            continue
        vues_ici = 0
        for titre, champ in ctx.mo.sections_adossees(p.role):
            cibles = vault.cibles_du_champ(p.fm, champ)
            if not cibles:
                continue
            vues_ici += len(cibles)
            en_section = vault.cibles_de_la_section(p.sections.get(titre) or "")
            manquants = sorted(cibles - en_section)
            if manquants:
                r.ajoute(rid, sev,
                         f"cible(s) de `{champ}:` absente(s) de la section "
                         f"`{titre}` {manquants}", p.chemin, codes=("R11", "R22"))
        if vues_ici:
            adossees += 1
            promesses += vues_ici
    r.population(rid, adossees, objets=promesses,
                 objet="cible déclarée qu'une section promet de lister")


# --------------------------------------------------------------------------- #
def lien_vers_une_page_a_comprendre(ctx: Contexte, r: Rapport) -> None:
    """R15 — une unite porte au moins un lien vers une page a COMPRENDRE.

    La cible attendue est une page dont la fonction est d expliquer : `notion`
    ou `hub` — un hub de domaine absorbe volontiers la notion chapeau homonyme,
    c est la meme page. Le couple unite <-> notion est impose par le skill de
    capture, mais rien ne le verifiait : le validateur controlait qu un lien n
    est pas mort, jamais qu il EXISTE.
    """
    rid = "lien_vers_une_page_a_comprendre"
    rid_unite = ctx.mo.role_unite
    if rid_unite is None or not ctx.stems_a_comprendre:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = ctx.mo.severite(rid)
    r.population(rid, len(ctx.pages_du_role(rid_unite)))
    for p in ctx.pages_du_role(rid_unite):
        cibles = {t.split("|")[0].split("/")[-1].strip().lower()
                  for t in p.liens_du_corps()}
        if not (cibles & ctx.stems_a_comprendre):
            r.ajoute(rid, sev,
                     "aucun lien vers une page à comprendre (notion ou hub)",
                     p.chemin, codes=("R15",))


# --------------------------------------------------------------------------- #
def paire_inverse_bien_declaree(ctx: Contexte, r: Rapport) -> None:
    """Un `reciproque: {mode: inverse, champ: Y}` exige que Y pointe en retour.

    Verifiable sur le MANIFESTE, sans lire une seule page. Dure d emblee, et
    pour la meme raison que `frontmatter_lisible` : ce n est pas une regle a
    durcir, c est un trou a ne pas ouvrir. Un `inverse` qui pointe vers un champ
    qui ne pointe pas en retour remplacerait un trou par un autre.
    """
    rid = "paire_inverse_bien_declaree"
    sev = ctx.mo.severite(rid)
    mo = ctx.mo
    trouve = False
    for nom, rec in mo.champs_a_reciprocite().items():
        if rec.get("mode") != "inverse":
            continue
        trouve = True
        cible = rec.get("champ")
        if not cible or cible not in mo.champs:
            r.ajoute(rid, sev,
                     f"`champs.{nom}.reciproque.champ` vaut `{cible}`, qui n'est "
                     f"pas un champ déclaré")
            continue
        retour = (mo.champ(cible).get("reciproque") or {})
        if retour.get("mode") != "inverse" or retour.get("champ") != nom:
            r.ajoute(rid, sev,
                     f"`{nom}` déclare l'inverse `{cible}`, qui ne déclare pas "
                     f"`{nom}` en retour")
    inverses = sum(1 for rec in mo.champs_a_reciprocite().values()
                   if rec.get("mode") == "inverse")
    r.population(rid, 0, objets=inverses, objet="champ `reciproque: inverse`",
                 sur_le_manifeste=True)
    if not trouve:
        r.etat(rid, constat.NON_APPLICABLE)


# --------------------------------------------------------------------------- #
def amont_concorde(ctx: Contexte, r: Rapport) -> None:
    """L amont sonde ne contredit pas ce que la page declare.

    Trois desaccords, un par sous-cle, et ils ne se confondent pas :

      - `archive`   — le proprietaire a ferme le depot, la page ne le dit pas ;
      - `ancien`    — la derniere trace datee de l amont depasse le seuil ;
      - `contredit` — l inverse, et il vaut autant : l amont publie encore alors
                      que la page porte une valeur ELIMINATOIRE. Une brique
                      declaree morte qui ressuscite est aussi trompeuse qu une
                      brique declaree vive qui ne l est plus, et personne ne
                      relit une fiche qu il croit enterree.

    **Jamais dure, et ce n est pas provisoire.** Une violation ici n est pas une
    faute de redaction : c est un desaccord entre le vault et un tiers, dont le
    tiers peut avoir tort (un depot miroir archive, un projet dont le vrai
    developpement a demenage). Le corriger appartient a l auteur ; l outil ne
    sait pas laquelle des deux sources dit vrai. Un vault ne doit pas etre otage
    de l amont — c est aussi pour cela que la sonde sort en 0 sur ses constats.

    Le denominateur est le nombre de pages REELLEMENT sondees. Une page jamais
    sondee n est pas conforme, elle est inconnue : la compter dans la population
    ferait passer un side-car vide pour un vault sain, ce qui est exactement
    « une regle absente ressemble a une regle satisfaite ».
    """
    rid = "amont_concorde"
    from .. import amont as _amont

    a = _amont.declaration(ctx.mo)
    if not a.declare:
        r.etat(rid, constat.NON_APPLICABLE)
        return
    sev = ctx.mo.severite(rid)
    contenu = _amont.lit_side_car(a, ctx.racine)
    champ = a.champ_confronte
    mortes = {str(v) for v in (ctx.mo.champ(champ).get("eliminatoire") or [])} \
        if champ else set()
    pages = [p for p in ctx.lisibles if p.role in a.porte_par]

    sondees = 0
    jamais = 0
    for p in pages:
        rec = contenu.get(p.chemin) or {}
        e = str(rec.get("etat") or "jamais_sonde")
        if e == "jamais_sonde":
            jamais += 1
            continue
        sondees += 1
        val = str(p.fm.get(champ) or "") if champ else ""
        dit = f"`{champ}: {val}`" if val else (f"`{champ}:` absent" if champ
                                               else "la page")
        quand = rec.get("date") or "date inconnue"
        if e == "archive" and val not in mortes:
            r.ajoute(rid, sev,
                     f"amont ARCHIVÉ ({quand}) et {dit}", p.chemin,
                     cle="archive")
        elif e == "ancienne" and val not in mortes:
            r.ajoute(rid, sev,
                     f"dernière trace datée de l'amont : {quand}, au-delà du "
                     f"seuil — {dit}", p.chemin, cle="ancien")
        elif e == "recente" and val in mortes:
            r.ajoute(rid, sev,
                     f"amont vivant ({quand}) et {dit}", p.chemin,
                     cle="contredit")
    r.population(rid, sondees)
    if jamais:
        r.note(f"{rid} : {jamais} page(s) du périmètre jamais sondée(s) — hors "
               f"population, parce qu'inconnu n'est pas conforme "
               f"(`brainkit sonder`)")


# --------------------------------------------------------------------------- #
# L aiguillage : {id de regle : la fonction qui la porte}. Une regle du
# manifeste sans entree ici n est pas implementee, et l inventaire le dit.
# --------------------------------------------------------------------------- #
IMPLEMENTEES = {
    "frontmatter_lisible": frontmatter_lisible,
    "gabarit_par_role": gabarit_par_role,
    "vocabulaire_ferme": vocabulaire_ferme,
    "nom_egal_fichier": nom_egal_fichier,
    "liens_resolus": liens_resolus,
    "page_atteignable": page_atteignable,
    "hub_par_niveau": hub_par_niveau,
    "unicite_du_nom_de_fichier": unicite_du_nom_de_fichier,
    "taille_avertissement": taille_avertissement,
    "collision_alias": collision_alias,
    "champs_supprimes": champs_supprimes,
    "couverture_de_section": couverture_de_section,
    "lien_vers_une_page_a_comprendre": lien_vers_une_page_a_comprendre,
    "paire_inverse_bien_declaree": paire_inverse_bien_declaree,
    "amont_concorde": amont_concorde,
}
