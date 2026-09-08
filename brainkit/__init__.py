"""BrainKit — le noyau generique d un second brain, pilote par `brain.yml`.

Aucun module de ce paquet ne connait le sujet d une instance. Les mots du vault
(« brique », « domaine », « famille »), ses valeurs, ses sections, ses seuils et
la severite de ses regles vivent dans le manifeste — jamais ici.

# `__version__` est LA version du kit, et il n y en a qu une

Elle est ici, et `pyproject.toml` la LIT (`[tool.hatch.version]`, champ
`dynamic`). L inverse — la valeur dans `pyproject.toml`, recopiee ici — aurait
donne deux sources pour la meme chose, dont l une prend du retard : c est le
constat E4 du cadrage, et le kit existe pour le supprimer.

Ce qui la compare a `kit.version` d un manifeste vit dans `contrat.py`.
"""

__version__ = "0.1.0"
