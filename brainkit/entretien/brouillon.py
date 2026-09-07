"""brouillon.py — le mode REPRISE : un entretien de cinquante questions ne tient
pas toujours en une seance.

# Pourquoi ce module existe

Les onze passes demandent une heure a une heure et demie de conversation reelle,
dont la passe 2 prend le tiers a elle seule (citer vingt pages, les ranger de sa
main, revenir sur celles qui debordent). Un entretien qui exigerait d aller au
bout d une traite ne serait pas mene : il serait abandonne en passe 3, et le
lendemain quelqu un recommencerait de zero — ou pire, se souviendrait mal.

Le brouillon est la memoire de l entretien. Il porte les REPONSES, pas le
manifeste : ce qui a ete dit, par qui, quand, et avec quelle provenance. Le
manifeste s en compose a la fin, et il peut se recomposer autant de fois qu on
veut sans reposer une question.

# Trois proprietes, et la troisieme est la moins evidente

1. **Rien ne se redemande.** `prochaine()` rend la premiere question sans
   reponse dont la condition est remplie. Une question deja repondue ne
   ressort pas, meme apres six reprises.
2. **Les questions conditionnelles se SAUTENT toutes seules.** 2.4 ne se pose
   que si 2.3 vaut « non » ; 3.2, 3.3 et 3.4 ne se posent que si 3.1 vaut
   « oui ». Un brouillon dont 3.1 vaut « non » compte donc moins de questions
   restantes, et l entretien n a pas a s en souvenir.
3. **La provenance se stocke avec la reponse, pas a cote.** C est ce qui rend
   le refus n° 1 verifiable APRES COUP : six mois plus tard, on peut relire le
   brouillon d une instance et voir que l identite git est bien venue de
   l utilisateur. Une provenance gardee en memoire vive n aurait rien prouve.

# Le brouillon survit au semis

Il est copie dans l instance, sous `AI/entretien/`. Ce n est pas un vestige :
c est la seule trace de POURQUOI la taxonomie est celle-la, au-dela des `motif:`
que le manifeste porte. Un brain repris dans un an se relit avec ses reponses
sous les yeux.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from .passes import ORDRE, PASSES, QUESTIONS, Question
from .refus import PROVENANCE_VALIDE, PROVENANCES_INTERDITES

VERSION = 1
NOM_PAR_DEFAUT = "entretien.yml"

_OUI = ("oui", "yes", "true", "vrai", "o")
_NON = ("non", "no", "false", "faux", "n")


@dataclass
class Brouillon:
    chemin: Path
    reponses: dict[str, dict] = field(default_factory=dict)
    ouvert_le: str = ""
    touche_le: str = ""
    notes: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------ #
    def valeur(self, qid: str) -> Any:
        r = self.reponses.get(qid)
        return r.get("valeur") if isinstance(r, dict) else None

    def a_repondu(self, qid: str) -> bool:
        return qid in self.reponses

    @property
    def brain(self) -> str:
        return str(self.valeur("0.2") or "")

    # ------------------------------------------------------------------ #
    def repond(self, qid: str, valeur: Any,
               provenance: str = PROVENANCE_VALIDE) -> list[str]:
        """Enregistre une reponse. Rend les griefs — vide si tout va bien."""
        griefs: list[str] = []
        if qid not in QUESTIONS:
            return [f"question inconnue : `{qid}` — les questions sont une liste "
                    f"fermée, cf. `brainkit entretien --questions`"]
        if provenance in PROVENANCES_INTERDITES:
            griefs.append(
                f"{qid} : provenance `{provenance}` REFUSÉE. Une réponse qui ne "
                f"vient pas de l'utilisateur n'est pas une réponse — c'est une "
                f"valeur devinée avec une étiquette.")
            return griefs
        if provenance != PROVENANCE_VALIDE:
            griefs.append(f"{qid} : provenance `{provenance}` inconnue — seule "
                          f"`{PROVENANCE_VALIDE}` est acceptée.")
            return griefs
        self.reponses[qid] = {
            "valeur": valeur,
            "provenance": provenance,
            "le": datetime.now().isoformat(timespec="seconds"),
        }
        return griefs

    def oublie(self, qid: str) -> None:
        """Reouvre une question — le seul moyen de la reposer."""
        self.reponses.pop(qid, None)

    # ------------------------------------------------------------------ #
    def posable(self, q: Question) -> bool:
        """Une question conditionnelle dont la condition n est pas remplie ne se pose pas."""
        if not q.condition:
            return True
        m = re.match(r"^(\d+\.\d+)\s*=\s*(oui|non)$", q.condition.strip())
        if m:
            qid, attendu = m.group(1), m.group(2)
            if not self.a_repondu(qid):
                return False          # on ne saute pas : on n a pas encore su
            return _est_oui(self.valeur(qid)) == (attendu == "oui")
        if q.condition.startswith("4.1"):
            return bool(self.valeur("4.1"))
        if "rôle `vue`" in q.condition:
            return _est_oui(self.valeur("8.1")) or bool(self.valeur("8.2"))
        # « par colonne », « par relation » : la question se pose autant de fois
        # qu il y a d objets, et c est le skill qui boucle. Elle est posable.
        return True

    def prochaine(self) -> Question | None:
        for qid in ORDRE:
            q = QUESTIONS[qid]
            if self.a_repondu(qid):
                continue
            if self.posable(q):
                return q
        return None

    def restantes(self) -> list[Question]:
        return [QUESTIONS[q] for q in ORDRE
                if not self.a_repondu(q) and self.posable(QUESTIONS[q])]

    def sautees(self) -> list[Question]:
        return [QUESTIONS[q] for q in ORDRE
                if not self.a_repondu(q) and not self.posable(QUESTIONS[q])
                and _condition_tranchee(self, QUESTIONS[q])]

    # ------------------------------------------------------------------ #
    def etat(self) -> str:
        L = [f"entretien « {self.brain or '(sans nom)'} » — "
             f"{len(self.reponses)} réponse(s) sur {len(QUESTIONS)} questions, "
             f"{len(self.restantes())} restante(s)"]
        if self.ouvert_le:
            L.append(f"ouvert le {self.ouvert_le}, touché le {self.touche_le}")
        L.append("")
        for p in PASSES:
            faits = sum(1 for q in p.questions if self.a_repondu(q.id))
            posables = [q for q in p.questions
                        if self.a_repondu(q.id) or self.posable(q)]
            sautees = len(p.questions) - len(posables)
            marque = "terminée" if faits == len(posables) and posables else \
                     ("non entamée" if not faits else "en cours")
            suffixe = f", {sautees} sautée(s)" if sautees else ""
            L.append(f"  Passe {p.n:2d} — {p.titre:28s} "
                     f"{faits}/{len(posables)} {marque}{suffixe}")
        q = self.prochaine()
        L.append("")
        if q is None:
            L.append("Toutes les questions posables ont une réponse. "
                     "`--composer` peut écrire le manifeste.")
        else:
            L.append(f"On reprend à la question {q.id} : {q.texte}")
        return "\n".join(L)

    def rappel(self, combien: int = 8) -> str:
        """Ce qui a deja ete dit, a relire A HAUTE VOIX en reprenant.

        Une reprise qui redemarrerait sans rappeler forcerait l utilisateur a
        se souvenir de ce qu il a repondu la semaine derniere — et il
        repondrait autrement, ce qui est pire qu une question reposee.
        """
        faits = [q for q in ORDRE if self.a_repondu(q)]
        L = [f"On avait dit — les {min(combien, len(faits))} dernières choses :"]
        for qid in faits[-combien:]:
            L.append(f"  {qid} · {QUESTIONS[qid].texte}")
            L.append(f"       -> {_court(self.valeur(qid))}")
        return "\n".join(L)


def _est_oui(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in _OUI
    return bool(v)


def _condition_tranchee(b: "Brouillon", q: Question) -> bool:
    """Une question sautee ne l est que si sa condition a VRAIMENT ete tranchee."""
    m = re.match(r"^(\d+\.\d+)\s*=\s*(oui|non)$", q.condition.strip())
    return bool(m) and b.a_repondu(m.group(1))


def _court(v: Any, n: int = 96) -> str:
    t = str(v)
    t = " ".join(t.split())
    return t if len(t) <= n else t[:n - 1] + "…"


# --------------------------------------------------------------------------- #
def charge(chemin: Path) -> Brouillon:
    """Le brouillon du chemin, ou un brouillon NEUF. Jamais une erreur."""
    chemin = Path(chemin)
    if not chemin.is_file():
        return Brouillon(chemin=chemin,
                         ouvert_le=date.today().isoformat())
    with chemin.open(encoding="utf-8") as f:
        d = yaml.safe_load(f) or {}
    if int(d.get("entretien") or 0) != VERSION:
        raise ValueError(
            f"{chemin} : `entretien: {d.get('entretien')}` — ce kit ne relit que "
            f"la version {VERSION}. Un brouillon d'une autre version ne se "
            f"devine pas : il se rejoue.")
    return Brouillon(
        chemin=chemin,
        reponses=dict(d.get("reponses") or {}),
        ouvert_le=str(d.get("ouvert_le") or ""),
        touche_le=str(d.get("touche_le") or ""),
        notes=list(d.get("notes") or []),
    )


def enregistre(b: Brouillon) -> Path:
    """Ecrit le brouillon. C est le SEUL chemin d ecriture du paquet `entretien`.

        grep -rnE 'write_text|open\\(' brainkit/entretien/
    """
    b.touche_le = datetime.now().isoformat(timespec="seconds")
    d = {
        "entretien": VERSION,
        "brain": b.brain,
        "ouvert_le": b.ouvert_le,
        "touche_le": b.touche_le,
        "reponses": b.reponses,
    }
    if b.notes:
        d["notes"] = b.notes
    entete = (
        "# Le brouillon de l'entretien — les RÉPONSES, pas le manifeste.\n"
        "#\n"
        "# Il se relit, il se reprend, il se recompose. Ce qui est écrit ici a\n"
        "# été DIT par l'utilisateur : chaque réponse porte sa provenance, et\n"
        "# `utilisateur` est la seule valeur acceptée — c'est ce qui rend le\n"
        "# refus n° 1 (l'identité git) vérifiable après coup.\n"
        "#\n"
        "#   uv run brainkit entretien --brouillon ce-fichier --etat\n"
        "#   uv run brainkit entretien --brouillon ce-fichier --composer brain.yml\n"
        "\n"
    )
    b.chemin.parent.mkdir(parents=True, exist_ok=True)
    with b.chemin.open("w", encoding="utf-8", newline="\n") as f:
        f.write(entete)
        yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=88)
    return b.chemin
