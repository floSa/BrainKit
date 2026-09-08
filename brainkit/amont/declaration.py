"""declaration.py — le bloc `amont:` du manifeste, mis en forme. Rien de plus.

Aucune valeur d instance n est ecrite ici : ni un nom d hote, ni un nom de
champ, ni un seuil. Les seules constantes de ce module sont les deux listes que
le KIT ferme — les sondes qu il sait faire et les etats qu il sait deriver —
pour la meme raison que les six fonctions de role : une sonde est du code, et
une instance ne peut pas en inventer une en l ecrivant dans son manifeste.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Les sondes que le kit sait faire. FERMEE. Une valeur hors de cette liste est
# refusee par le schema et signalee par la coherence : `gitlab` est un nom de
# sonde parfaitement legitime, ce n est pas une sonde que ce kit possede.
SONDES = ("github", "pypi")

# La valeur par defaut du seuil, en jours, quand le manifeste declare le bloc
# sans declarer ses seuils. Deux ans : c est un DEFAUT DE FORME, pas une
# recommandation — le manifeste est cense l ecrire avec son motif, et le rapport
# de sondage dit quand il a fallu retomber la-dessus.
SEUIL_DEFAUT_JOURS = 730


@dataclass
class Amont:
    """Ce que le manifeste declare de l amont de ses unites. Vide = non declare."""

    declare: bool = False
    porte_par: list[str] = field(default_factory=list)
    champ_url: str = ""
    champ_confronte: str = ""
    side_car: str = ""
    fait_etat: str = ""
    fait_date: str = ""
    hotes: dict[str, str] = field(default_factory=dict)     # hote -> sonde
    registre: dict = field(default_factory=dict)            # {sonde, si, champs}
    seuils: dict = field(default_factory=dict)

    # ------------------------------------------------------------------ #
    def seuil(self, nom: str) -> int:
        try:
            return int(self.seuils[nom])
        except (KeyError, TypeError, ValueError):
            return SEUIL_DEFAUT_JOURS

    @property
    def seuil_declare(self) -> bool:
        """Le manifeste a-t-il ECRIT ses seuils, ou tombe-t-on sur le defaut ?

        La question se pose parce qu un seuil devine est exactement ce que le
        kit refuse ailleurs. Ici il ne s arrete pas — un sondage qui refuse de
        tourner faute de seuil ne rend service a personne — mais il le DIT.
        """
        return all(nom in self.seuils for nom in
                   ("release_ancienne_jours", "commit_ancien_jours"))

    def sonde_de_l_hote(self, hote: str) -> str | None:
        """La sonde declaree pour un hote, en tolerant un `www.` de tete."""
        h = hote.lower()
        return self.hotes.get(h) or self.hotes.get(h.removeprefix("www."))

    @property
    def sondes_utilisees(self) -> list[str]:
        lot = sorted(set(self.hotes.values()))
        r = str(self.registre.get("sonde") or "")
        return lot + ([r] if r and r not in lot else [])


def declaration(mo) -> Amont:
    """Le bloc `amont:` d un `Modele`, ou un `Amont` non declare.

    Un `Amont(declare=False)` n est pas une erreur et ne se signale pas : c est
    la reponse juste pour un brain dont les unites n ont pas d amont. Tout ce
    qui consomme ce paquet teste `declare` en premier et se tait sinon.
    """
    bloc = (mo.m.get("amont") or {}) if getattr(mo, "m", None) else {}
    if not bloc:
        return Amont()
    faits = bloc.get("faits") or {}
    hotes: dict[str, str] = {}
    for s in bloc.get("sondes") or []:
        hote = str(s.get("hote") or "").strip().lower()
        if hote:
            hotes[hote] = str(s.get("sonde") or "").strip()
    return Amont(
        declare=True,
        porte_par=[str(x) for x in (bloc.get("porte_par") or [])],
        champ_url=str(bloc.get("champ_url") or ""),
        champ_confronte=str(bloc.get("champ_confronte") or ""),
        side_car=str(bloc.get("side_car") or ""),
        fait_etat=str(faits.get("etat") or ""),
        fait_date=str(faits.get("date") or ""),
        hotes=hotes,
        registre=dict(bloc.get("registre") or {}),
        seuils=dict(bloc.get("seuils") or {}),
    )
