from time import sleep

NORMAL = "\033[0;0m"
NOIR_GRAS = "\033[1;30m"
ROUGE_GRAS = "\033[1;31m"
BLEU_GRAS = "\033[1;34m"
VERT_GRAS = "\033[1;32m"

def correspond(motif, chaine, k, dec, compt):
    n = len(motif)
    print(chr(13) + "Motif  : " + " "*(k-dec) + ">"*dec + motif + f"  ({compt} comparaison{'s' if compt > 1 else ''})" + " "*20, end="")
    sleep(0.5)
    for i in range(n):
        compt += 1
        if chaine[k+i] != motif[i]:
            print(chr(13) + "Motif  : " + " "*k + VERT_GRAS + motif[:i] + ROUGE_GRAS + motif[i] + NORMAL + motif[i+1:] + f"  ({compt} comparaison{'s' if compt > 1 else ''})" + " "*20, end="")
            return False, compt
        else:
            print(chr(13) + "Motif  : " + " "*k + VERT_GRAS + motif[:i+1] + NORMAL + motif[i+1:] + f"  ({compt} comparaison{'s' if compt > 1 else ''})" + " "*20, end="")        
        sleep(0.5)
    return True, compt

def animation_algo_naif(motif, chaine):
    n = len(motif)
    print("Chaîne :", chaine)
    dec = 0
    compt = 0
    for k in range(len(chaine)-n+1):
        bool, compt = correspond(motif, chaine, k, dec, compt)
        if bool:
            print("\n         " + " "*k + VERT_GRAS + "motif trouvé !" + NORMAL)
            return
        sleep(1)
        dec = 1

def pretraitement(motif):
    dico = {}
    for k in range(len(motif)-1):
        dico[motif[k]] = len(motif) - 1 - k
    return dico

def correspond_renv(motif, chaine, k, dec, compt):
    n = len(motif)
    print(chr(13) + "Motif  : " + " "*(k-dec) + ">"*dec + motif + f"  ({compt} comparaison{'s' if compt > 1 else ''})" + " "*20, end="")
    sleep(0.5)
    for i in range(n-1, -1, -1):
        compt += 1
        if chaine[k+i] != motif[i]:
            print(chr(13) + "Motif  : " + " "*k + motif[:i] + ROUGE_GRAS + motif[i] + VERT_GRAS + motif[i+1:] + NORMAL + f"  ({compt} comparaison{'s' if compt > 1 else ''})" + " "*20, end="")
            return False, compt
        else:
            print(chr(13) + "Motif  : " + " "*k + motif[:i] + VERT_GRAS + motif[i:] + NORMAL + f"  ({compt} comparaison{'s' if compt > 1 else ''})" + " "*20, end="")
        sleep(0.5)
    return True, compt

def animation_boyer_moore_horspool(motif, chaine):
    c = len(chaine)
    m = len(motif)
    dico = pretraitement(motif)
    k = 0
    print("Chaîne :", chaine)
    dec = 0
    compt = 0
    while k <= c - m:
        bool, compt = correspond_renv(motif, chaine, k, dec, compt)
        if bool:
            print("\n         " + " "*k + VERT_GRAS + "motif trouvé !" + NORMAL)
            return
        sleep(1)
        if chaine[k+m-1] in dico:
            dec = dico[chaine[k+m-1]]
        else:
            dec = m
        k = k + dec
        sleep(1)