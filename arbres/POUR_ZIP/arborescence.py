import os

def _mise_en_forme(chemin):
    chaines = chemin.split('/')
    n = len(chaines) - 1
    return '|____ '*n + chaines[n]
    
def arborescence(chemin):
    """
    Affiche l'arborescence d'un répertoire.
    - Entrée : chemin (chaîne)
    - Effet de bord : affichage à l'écran
    """
    print(_mise_en_forme(chemin))
    if os.path.isdir(chemin):
        for sous_chemin in sorted(os.listdir(chemin)):
            arborescence(chemin + '/' + sous_chemin)
