# `docs/` — les documents générés du kit

> **Dossier GÉNÉRÉ** par `uv run outils/emballer.py --ecrire`. Ne rien éditer à la main ici : tout se régénère depuis le code du kit et depuis un manifeste.

## Ce que tu cherches probablement

| Tu veux | Va voir |
|---|---|
| installer le kit et créer un brain | `../INSTALL.md`, à la racine du dépôt |
| **voir** ce que le semis pose dans une instance | `histobrain/` |
| comprendre les décisions de conception | `../design/`, lot par lot |

## `histobrain/` — les documents d'une instance, rendus une fois

Une instance porte **ses** documents, écrits par `brainkit semer` depuis **son** manifeste. Ils n'ont donc rien à faire dans le dépôt du kit — sauf qu'un dépôt qui annonce « le semis pose un guide d'installation et trois guides d'usage » sans qu'on puisse les lire demande de le croire sur parole.

Ceux-ci sont rendus depuis `exemples/histobrain.brain.yml`, le manifeste de démonstration — un brain d'**histoire**, choisi parce que c'est le sujet le plus éloigné de celui dont le kit a été extrait. Un brain de développement logiciel aurait laissé planer le doute.

| Fichier | Ce que c'est |
|---|---|
| `histobrain/INSTALL.md` | installer **cette instance** sur une machine neuve |
| `histobrain/enrichir.md` | écrire dedans, et ce que ça déclenche autour |
| `histobrain/exploiter.md` | s'en servir depuis un travail, sans y écrire |
| `histobrain/manuel.md` | lire le brain — ce qu'on a sous les yeux |

> Ce sont des documents d'**exemple**. Ton instance porte les siens, avec tes mots, tes axes et tes règles — et si les deux se ressemblent quelque part, c'est que cet endroit-là est vraiment générique.
