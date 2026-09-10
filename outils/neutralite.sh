#!/usr/bin/env bash
# neutralite.sh — preuve que le depot ne nomme aucun sujet.
#
#     bash outils/neutralite.sh        # 0 occurrence attendue
#
# Deux exclusions, et les deux sont ECRITES :
#
#   1. `design/` — les archives du chantier. Elles citent le vault reel sur
#      lequel tout a ete prouve, et c est delibere : effacer les mesures
#      effacerait les preuves. Arbitrage ecrit dans AGENTS.md §6.
#   2. CE FICHIER — il porte la liste des mots interdits, donc il les contient
#      tous par construction. S auto-signaler ne prouverait rien.
#
# Ce qu il ne voit PAS : le contenu des images. Quatorze captures portent le nom
# du vault d origine dans leur barre de titre ; elles sont nommees comme A
# REPRENDRE dans docs/04-obsidian.md et design/12-captures.md §2.
set -u
cd "$(dirname "$0")/.." || exit 1

MOTIF='DevBrain|HistoBrain|CimeBrain|DroitBrain|Antiquité|Antiquite|XXe siècle|Herodote|Hérodote|Thucydide|Tacite|Suétone|Suetone|Braudel|Kennan|Duby|Bloch|Paxton|Kershaw|Hobsbawm|Le Roy Ladurie|Montaillou|Vichy|Guerre froide|Historiographie|Méditerranée|Mediterranee|Mont[- ]Blanc|Vanoise|Écrins|Ecrins|Vercors|Queyras|Ubaye|Pyrénées|Pyrenees|Chambeyron|Meije|Moucherolle|Veymont|Vignemale|Ossau|Gavarnie|URSSAF|CSE|convention collective|licenciement|salarié|salarie|Postgres|WrenAI|polars|pola-rs|scikit|sklearn|PyTorch|FastAPI|MLflow'

echo "=== fichiers SUIVIS par git, hors design/ et hors ce script ==="
FICHIERS=$(git ls-files | grep -v '^design/' | grep -v '^outils/neutralite.sh$')
echo "$FICHIERS" | wc -l | xargs echo "  fichiers examines :"

echo
echo "=== occurrences ==="
TROUVE=0
while IFS= read -r f; do
  case "$f" in
    *.png|*.jpg|*.jpeg|*.gif|*.pdf) continue ;;
  esac
  if grep -nEI "$MOTIF" "$f" >/dev/null 2>&1; then
    grep -nEI "$MOTIF" "$f" | sed "s|^|$f:|"
    TROUVE=1
  fi
done <<< "$FICHIERS"

if [ "$TROUVE" -eq 0 ]; then
  echo "  AUCUNE — 0 occurrence."
fi
