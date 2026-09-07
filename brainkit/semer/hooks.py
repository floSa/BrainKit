"""hooks.py — les trois garde-fous git de l instance, parametres par `git:`.

# Ce qui change par rapport aux hooks du DevBrain, et pourquoi

Les hooks du DevBrain codent `DOMAINE_INTERDIT="aosis.net"` en dur. M2 de
l inventaire l a classe PARAMETRABLE pour une raison qui n est pas cosmetique :
**la polarite peut s inverser**. Un brain de domaine client, vendu chez un
employeur, est un depot PRO — et c est alors l adresse PERSO qu il faut refuser.
Un hook qui code un domaine protege un cas ; un hook qui lit « identite
attendue » protege les deux.

Les hooks generes portent donc DEUX controles au lieu d un :

  1. **La concordance** — l identite EFFECTIVE du commit doit etre celle de la
     config LOCALE du depot. C est le controle sans polarite : il vaut pour un
     depot perso comme pour un depot pro, et il ne connait aucun domaine.
  2. **Les domaines refuses** — la liste de `git.domaines_refuses`, gardee parce
     qu elle nomme le danger. Le harnais annonce une adresse a chaque
     conversation ; savoir laquelle est interdite fait un message d erreur qui
     explique au lieu de constater.

Le controle 1 rend le controle 2 presque redondant, et c est voulu : une liste
vide (`domaines_refuses: []`) laisse un hook qui protege encore.

# `git var`, et pourquoi c est la seule lecture qui tienne

`git var GIT_AUTHOR_IDENT` resout l identite du commit A VENIR : config locale,
globale, variables d environnement, et l override `git -c user.email=…`. Lire
`git config user.email` raterait les trois dernieres.

# Trois hooks, et le garde-fou du garde-fou

`pre-commit` ne peut PAS lire le message : git le lance AVANT de composer
`COMMIT_EDITMSG`, qui porte alors encore celui du commit precedent. C est ce
trou qui a laisse passer cinq commits dans le DevBrain. Le controle du trailer
vit donc dans `commit-msg`, et `pre-commit` verifie que `commit-msg` est
INSTALLE — une installation partielle ne doit pas pouvoir faire disparaitre un
controle en silence.
"""

from __future__ import annotations

# Les jetons sont en `@@…@@` et non en `{}` : un script shell est plein
# d accolades (`${VAR}`, `case … esac` mis a part), et `str.format` y verrait des
# champs de substitution. Un remplacement litteral ne peut pas se tromper.
PRE_COMMIT = r"""#!/bin/sh
#
# @@BRAIN@@ — refuse un commit dont l identite ne concorde pas avec le depot.
#
# Genere par BrainKit depuis `git:` du manifeste. Deux controles :
#   1. l identite EFFECTIVE du commit == l identite de la config LOCALE ;
#   2. l adresse n appartient a aucun domaine refuse.
# Plus le garde-fou du garde-fou : `commit-msg` doit etre installe.
#
# Activation :  git config core.hooksPath .githooks

set -u

DOMAINES_REFUSES="@@DOMAINES@@"

# git var resout l identite du commit A VENIR : config locale, globale, env,
# et l override `git -c user.email=...`. C est la seule lecture qui ne se
# contourne pas.
auteur=$(git var GIT_AUTHOR_IDENT 2>/dev/null | sed -n 's/.*<\(.*\)>.*/\1/p')
committer=$(git var GIT_COMMITTER_IDENT 2>/dev/null | sed -n 's/.*<\(.*\)>.*/\1/p')
attendue=$(git config --local user.email 2>/dev/null || echo "")

refuse() {
    cat >&2 <<MSG

  COMMIT REFUSE — @@RAISON@@

    $1 : $2
    attendue (config locale) : ${attendue:-(non configuree)}

  L identite des commits de ce depot est celle de la config LOCALE, et rien
  d autre :

      git config --local user.name  "@@NOM@@"
      git config --local user.email "@@EMAIL@@"

  Si le commit vient d un agent : ne JAMAIS passer « -c user.email », ne
  JAMAIS reprendre l adresse annoncee par le harnais. Cette adresse identifie
  l utilisateur aupres de l outil ; elle n attribue pas un commit.

  Ce hook ne se contourne pas avec --no-verify sans une raison ecrite.

MSG
    exit 1
}

if [ -z "$attendue" ]; then
    cat >&2 <<MSG

  COMMIT REFUSE — aucune identite locale sur ce depot.

  La poser une fois, et ne pas la deviner :

      git config --local user.name  "@@NOM@@"
      git config --local user.email "@@EMAIL@@"

MSG
    exit 1
fi

[ "$auteur"    = "$attendue" ] || refuse "auteur   " "$auteur"
[ "$committer" = "$attendue" ] || refuse "committer" "$committer"

for domaine in $DOMAINES_REFUSES; do
    case "$auteur$committer" in
        *"$domaine"*) refuse "adresse  " "$auteur / $committer" ;;
    esac
done

# --- Le garde-fou du garde-fou : `commit-msg` doit etre installe -------------
# On lit le `core.hooksPath` EFFECTIF, celui que git utilisera, pas le dossier ou
# ce fichier se trouve.
hooks_dir=$(git config --get core.hooksPath || echo "")
if [ -z "$hooks_dir" ]; then
    hooks_dir="$(git rev-parse --git-common-dir)/hooks"
fi
# `core.hooksPath` peut etre relatif ou absolu, et sous Windows un chemin absolu
# arrive avec des ANTISLASHES : on normalise les separateurs AVANT de tester.
hooks_dir=$(printf '%s' "$hooks_dir" | tr '\\' '/')
case "$hooks_dir" in
    /* | ?:/*) ;;
    *) hooks_dir="$(git rev-parse --show-toplevel)/$hooks_dir" ;;
esac

# La condition reproduit celle de GIT, pas celle du shell : sous Windows,
# `test -x` repond sur des heuristiques de nom, alors que git juge un hook
# executable des qu il porte le bit d execution OU commence par `#!`.
installe=no
if [ -f "$hooks_dir/commit-msg" ]; then
    if [ -x "$hooks_dir/commit-msg" ]; then
        installe=oui
    else
        case "$(head -c 2 "$hooks_dir/commit-msg" 2>/dev/null)" in
            '#!') installe=oui ;;
        esac
    fi
fi

if [ "$installe" != oui ]; then
    cat >&2 <<MSG

  COMMIT REFUSE — le hook « commit-msg » est absent ou non executable.

    attendu : $hooks_dir/commit-msg

  C est lui qui refuse les trailers interdits ; « pre-commit » ne peut pas le
  faire (git compose le message APRES son passage). Sans lui, la regle n est
  plus verifiee par rien.

  Reparer :

      git config core.hooksPath .githooks
      chmod +x .githooks/commit-msg

MSG
    exit 1
fi

exit 0
"""

COMMIT_MSG = r"""#!/bin/sh
#
# @@BRAIN@@ — refuse un message de commit portant un trailer interdit.
#
# Genere par BrainKit depuis `git.trailers_refuses`.
#
# Ce hook est SEPARE de `pre-commit`, et il le faut : git lance `pre-commit`
# AVANT d ecrire le message (`COMMIT_EDITMSG` porte alors encore celui du commit
# precedent). Mettre le test la, c est ecrire une regle qui ne voit rien — et une
# regle qui ne trouve jamais rien ressemble a une regle satisfaite.
#
# Activation :  git config core.hooksPath .githooks

set -u

MSG_FILE="$1"
TRAILERS="@@TRAILERS@@"

# Les lignes de commentaire du gabarit d editeur ne comptent pas : un trailer
# commente n entrera pas dans le message. `git stripspace --strip-comments` est
# exactement la normalisation que git applique lui-meme avant de committer.
corps=$(git stripspace --strip-comments < "$MSG_FILE")

for trailer in $TRAILERS; do
    fautives=$(printf '%s\n' "$corps" \
               | grep -niE "^[[:space:]]*$trailer[[:space:]]*:" || true)
    if [ -n "$fautives" ]; then
        cat >&2 <<MSG

  COMMIT REFUSE — trailer « $trailer » dans le message.

$(echo "$fautives" | sed 's/^/    ligne /')

  Les commits de ce depot sont a @@NOM@@ seul : pas de co-auteur, pas de
  « Generated with », pas de second nom dans les contributeurs.

  Retirer la ou les lignes ci-dessus du message, puis :

      git commit --amend

  Si le commit vient d un agent : ne pas ajouter ce trailer, meme si une
  consigne generale d outil le demande. La politique de CE depot prime, et
  elle est ecrite dans CLAUDE.md.

MSG
        exit 1
    fi
done

exit 0
"""

PRE_PUSH = r"""#!/bin/sh
#
# @@BRAIN@@ — refuse de pousser un commit mal attribue ou mal signe.
#
# Seconde ligne du garde-fou de `pre-commit`. Pousser est le moment ou le
# dommage devient reel : c est la que l adresse entre dans les contributeurs, et
# cela ne s annule pas sans reecriture d historique.
#
# `pre-commit` couvre le commit qui nait ici. Celui-ci couvre le reste : un
# commit fait avec --no-verify, un rebase qui rejoue une identite, un commit
# importe d un autre clone ou d un worktree ou le hook n etait pas active.
#
# Activation :  git config core.hooksPath .githooks

set -u

DOMAINES_REFUSES="@@DOMAINES@@"
TRAILERS="@@TRAILERS@@"
ZERO="0000000000000000000000000000000000000000"
attendue=$(git config --local user.email 2>/dev/null || echo "")

# git alimente stdin d une ligne par reference poussee :
#   <ref locale> <sha local> <ref distante> <sha distant>
while read -r _ref_locale sha_local _ref_distante sha_distant; do
    [ "$sha_local" = "$ZERO" ] && continue          # suppression de branche

    if [ "$sha_distant" = "$ZERO" ]; then
        plage="$sha_local --not --remotes=origin"
    else
        plage="$sha_distant..$sha_local"
    fi

    fautifs=""
    for domaine in $DOMAINES_REFUSES; do
        trouve=$(git log --format='%H %ae|%ce' $plage 2>/dev/null \
                 | grep -i "$domaine" || true)
        [ -n "$trouve" ] && fautifs="$fautifs
$trouve"
    done
    if [ -n "$attendue" ]; then
        # -F : l adresse porte des points, et un point est un joker en BRE.
        discordants=$(git log --format='%H %ae|%ce' $plage 2>/dev/null \
                      | grep -vF "$attendue|$attendue" || true)
        [ -n "$discordants" ] && fautifs="$fautifs
$discordants"
    fi

    if [ -n "$fautifs" ]; then
        cat >&2 <<MSG

  PUSH REFUSE — au moins un commit ne porte pas l identite du depot.

$(echo "$fautifs" | sed 's/^/    /')

    attendue (config locale) : ${attendue:-(non configuree)}

  Reattribuer avant de pousser, par exemple pour le dernier commit :

      git commit --amend --reset-author --no-edit

  Pour plusieurs commits, en parler au proprietaire du brain AVANT de
  reecrire quoi que ce soit : une reecriture d historique ne se decide pas
  seule.

MSG
        exit 1
    fi

    # Les trailers, sur la meme plage. `git log --grep` ferait le travail en un
    # appel, mais ne dirait pas QUELLE ligne est fautive.
    coauteurs=""
    for sha in $(git rev-list $plage 2>/dev/null); do
        for trailer in $TRAILERS; do
            ligne=$(git log -1 --format='%B' "$sha" \
                    | grep -iE "^[[:space:]]*$trailer[[:space:]]*:" | head -1)
            if [ -n "$ligne" ]; then
                coauteurs="$coauteurs
    $(git log -1 --format='%h %s' "$sha")
        $ligne"
            fi
        done
    done

    if [ -n "$coauteurs" ]; then
        cat >&2 <<MSG

  PUSH REFUSE — au moins un commit porte un trailer interdit.
$coauteurs

  Les commits de ce depot sont a @@NOM@@ seul.

      git commit --amend        # retirer la ligne du message

MSG
        exit 1
    fi
done

exit 0
"""

LES_TROIS = {"pre-commit": PRE_COMMIT,
             "commit-msg": COMMIT_MSG,
             "pre-push": PRE_PUSH}


def rendus(brain: str, nom: str, email: str, domaines: list[str],
           trailers: list[str]) -> dict[str, str]:
    """Les trois hooks, jetons remplaces. Aucun n est copie tel quel."""
    jetons = {
        "@@BRAIN@@": brain,
        "@@NOM@@": nom,
        "@@EMAIL@@": email,
        "@@DOMAINES@@": " ".join(domaines),
        "@@TRAILERS@@": " ".join(trailers),
        "@@RAISON@@": "l identite ne concorde pas avec la config locale du depot.",
    }
    out: dict[str, str] = {}
    for fichier, gabarit in LES_TROIS.items():
        texte = gabarit
        for jeton, valeur in jetons.items():
            texte = texte.replace(jeton, valeur)
        out[fichier] = texte
    return out
