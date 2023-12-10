"""Ce module permet de travailler avec des séquences d'ADN sous forme de chaînes de caractères."""

from random import choice

BASES_ASSOCIEES = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}

def sequence_alea(n):
    """
	Renvoie une séquence ADN aléatoire de longueur n
	- Entrée : n (entier positif)
	- Sortie : brin (chaîne de caractères)
	"""
    brin = ""
    for _ in range(n):
        brin += choice(['A', 'T', 'C', 'G'])
    return brin

def complementaire(brin):
    """
    Détermine le brin d'ADN complémentaire d'un brin donné.
    - Entrée : brin (chaîne de caractères)
    - Sortie : brin_comp (chaîne de caractères)
    """
    brin_comp = ""
    for k in range(len(brin)):
        brin_comp += BASES_ASSOCIEES[brin[k]]
    return brin_comp

def proportionAT(brin):
    """
    Calcule la proportion de bases A ou T dans un brin donné.
    - Entrée : brin (chaîne de caractères)
    - Sortie : (flottant)
    """
    cpt = 0
    for k in range(len(brin)):
        if brin[k] in ['A', 'T']:
            cpt = cpt + 1
    return cpt / len(brin)