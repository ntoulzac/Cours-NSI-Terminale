"""
Ce module a été créé par M. Toulzac dans le cadre du chapitre 7 du cours de NSI Terminale.

Il met à disposition trois classes :
    - une classe Labyrinthe, qui permet de générer un labyrinthe aléatoire et d'en enregistrer l'image dans un fichier,
    - une classe FenetreLaby, qui permet de gérer une fenêtre Pygame pour l'affichage d'un labyrinthe à l'écran,
    - une classe Pion, qui permet de gérer les déplacements et l'affichage d'un pion dansun labyrinthe.

Version de janvier 2022
"""

from PIL import Image
from random import shuffle
import pygame
from pygame.locals import QUIT as _QUIT, KEYDOWN as _KEYDOWN, K_UP as _K_UP, K_DOWN as _K_DOWN, K_LEFT as _K_LEFT, K_RIGHT as _K_RIGHT

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
_COULEURS = [BLANC, NOIR]
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)

class Labyrinthe:
    """
    Classe permettant de créer un labyrinthe aléatoire.
    """
    def __init__(self, NB_L=21, NB_C=31, nom_fichier=None):
        """
        Crée un labyrinthe aléatoire.
        - Entrées : NB_L (entier, nombre de lignes du labyrinthe),
                    NB_C (entier, nomnre de colonnes du labyrinthe),
                    nom_fichier (chaîne de caractères, nom du fichier PNG dans
                                 lequel enregistrer l'image du labyrinthe)
        """
        self.generer(NB_L, NB_C)
        if nom_fichier is not None:
	        self.creer_png(nom_fichier)
    
    def generer(self, NB_L, NB_C):
        """
        Génère un labyrinthe par fusion aléatoire de chemins.
        https://fr.wikipedia.org/wiki/Modélisation_mathématique_de_labyrinthe#Fusion_aléatoire_de_chemins
        Entrées : NB_L, NB_C (entiers, nombre de lignes et de colonnes du labyrinthe)
        """
    
        def _creer_grille_vide():
            self.nb_l = 2*NB_L + 1
            self.nb_c = 2*NB_C + 1
            self.grille = [[1 for C in range(self.nb_c)] for L in range(self.nb_l)]
            for L in range(NB_L):
                for C in range(NB_C):
                    self.grille[2*L+1][2*C+1] = 0
        
        def _placer_entree_sortie(entree, sortie):
            self.entree = entree
            self.grille[entree[0]][entree[1]] = 0
            self.sortie = sortie
            self.grille[sortie[0]][sortie[1]] = 0
            
        def _ouvrir_chemins():
            chemins_potentiels = [(2*L+1, 2*C) for L in range(NB_L) for C in range(1, NB_C)] + [(2*L, 2*C+1) for L in range(1, NB_L) for C in range(NB_C)] 
            shuffle(chemins_potentiels)
            # union-find
            dico_noeud_famille = {(2*L+1, 2*C+1) : L*NB_C+C  for L in range(NB_L) for C in range(NB_C)}
            dico_famille_noeuds = {L*NB_C+C : [(2*L+1, 2*C+1)] for L in range(NB_L) for C in range(NB_C)}
            pos = len(chemins_potentiels) - 1
            while len(dico_famille_noeuds) > 1 and pos >= 0:
                L, C = chemins_potentiels[pos]
                pos = pos - 1
                # L pair : ouverture au dessus ou au dessous ; L impair : ouverture à gauche ou à droite
                fam1 = dico_noeud_famille[(L-1, C) if L % 2 == 0 else (L, C-1)]
                fam2 = dico_noeud_famille[(L+1, C) if L % 2 == 0 else (L, C+1)]
                if fam1 != fam2: # si les deux voisines ne sont pas encore reliées
                    self.grille[L][C] = 0
                    for k in dico_famille_noeuds[fam2]:
                        dico_noeud_famille[k] = fam1
                        dico_famille_noeuds[fam1].append(k)
                    del dico_famille_noeuds[fam2]
            
        _creer_grille_vide()
        _placer_entree_sortie((2*(NB_L//2)+1, 0), (2*(NB_L//2)+1, 2*NB_C))
        _ouvrir_chemins()         

    def creer_png(self, nom_de_fichier):
        """
        Enregistre l'image du labyrinthe dans un fichier PNG.
        - Entrée : nom_de_fichier (chaîne de caractères)
        """
        TAILLE_CASE = 8
        image_laby = Image.new('1', (self.nb_c*TAILLE_CASE, self.nb_l*TAILLE_CASE), color=1)
        for L in range(self.nb_l):
            for C in range(self.nb_c):
                if self.grille[L][C] == 1:
                    for x in range(C*TAILLE_CASE, (C+1)*TAILLE_CASE):
                        for y in range(L*TAILLE_CASE, (L+1)*TAILLE_CASE):
                            image_laby.putpixel((x, y), 0)
        image_laby.save(f"{nom_de_fichier}.png")

class FenetreLaby:
    """
    Classe permettant de gérer une fenêtre pygame pour l'affichage d'un labyrinthe.
    """
    def __init__(self, laby):
        """
        Ouvre une fenêtre pygame aux dimensions d'un labyrinthe.
        - Entrée : laby (instance de la classe Labyrinthe)
        """
        pygame.init()
        self.t_c = min(800//laby.nb_c, 600//laby.nb_l)
        pygame.display.init()
        self.fen = pygame.display.set_mode((laby.nb_c*self.t_c, laby.nb_l*self.t_c))
        pygame.display.set_caption('Labyrinthe')
        self.afficher_cases(laby)
        self.actualiser()

    def fermer(self):
        """
        Ferme la fenêtre pygame.
        """
        pygame.display.quit()
        
    def actualiser(self):
        """
        Actualise la fenêtre en réalisant les modifications demandées
        depuis la dernière actualisation.
        """
        pygame.display.update()

    def lire_fleche(self):
        """
        Renvoie une direction choisie par le joueur au clavier.
        - Sortie : chaîne de caractère dépendant de la touche enfoncée
                   ('gauche', 'droite', 'haut', 'bas' en cas d'appui sur une touche
                    ou 'stop' en cas de clic sur la croix de fermeture de la fenêtre)
        Attention : l'exécution du programme est suspendue tant que le joueur n'appuie pas
        sur une des 4 flèches du clavier !
        """
        while True:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == _KEYDOWN:
                    if event.key == _K_UP:
                        return 'haut'
                    elif event.key == _K_DOWN:
                        return 'bas'
                    elif event.key == _K_LEFT:    
                        return 'gauche'    
                    elif event.key == _K_RIGHT:
                        return 'droite'
                elif event.type == _QUIT:
                    return 'stop'
    
    def afficher_cases(self, laby):
        """
        Prépare l'affichage d'un labyrinthe dans la fenêtre pygame.
        - Entrée : laby (instance de la classe Labyrinthe)
        Attention : penser à actualiser la fenêtre !
        """
        for L in range(laby.nb_l):
            for C in range(laby.nb_c):
                coul = _COULEURS[laby.grille[L][C]]
                pygame.draw.rect(self.fen, coul, (C*self.t_c, L*self.t_c, self.t_c, self.t_c))
    
    def afficher_pion(self, pion):
        """
        Prépare l'affichage d'un pion dans la fenêtre pygame.
        - Entrée : pion (instance de la classe Pion)
        Attention : penser à actualiser la fenêtre !
        """
        L, C = pion.pos
        pygame.draw.circle(self.fen, pion.couleur, ((C+0.5)*self.t_c, (L+0.5)*self.t_c), self.t_c*0.4)
        
    def afficher_tout(self, laby, pion):
        """
        Prépare l'affichage d'un labyrinthe et d'un pion dans la fenêtre pygame.
        - Entrées : laby (instance de la classe Labyrinthe),
                    pion (instance de la classe Pion)
        Attention : penser à actualiser la fenêtre !
        """
        self.afficher_cases(laby)
        self.afficher_pion(pion)

class Pion:
    """
    Classe permettant de créer et déplacer un pion dans un labyrinthe.
    """
    def __init__(self, pos, couleur=ROUGE):
        """
        Crée un pion à une position donnée et dans une couleur donnée.
        - Entrées : pos (couple d'entiers au format (ligne, colonne)),
                    couleur (triplet d'entiers au format (R, V, B))
        """
        self.pos = pos
        self.couleur = couleur
        
    def est_positionne_sur(self, pos):
        """
        Détermine si le pion est à une position donnée.
        - Entrée : pos (couple d'entiers au format (ligne, colonne))
        - Sortie : (booléen)
        """
        return self.pos == pos
            
    def deplacer(self, laby, direction):
        """
        Déplace le pion dans une direction donnée.
        - Entrées : laby (instance de la classe Labyrinthe), direction (chaîne de caractères)
        """
        L, C = self.pos
        if direction == 'gauche' and C > 0 and laby.grille[L][C-1] == 0:
            self.pos = (L, C-1)
        elif direction == 'droite' and C < laby.nb_c-1 and laby.grille[L][C+1] == 0:
            self.pos = (L, C+1)
        elif direction == 'haut' and L > 0 and laby.grille[L-1][C] == 0:
            self.pos = (L-1, C)
        elif direction == 'bas' and L < laby.nb_l-1 and laby.grille[L+1][C] == 0:
            self.pos = (L+1, C)

if __name__ == "__main__":
    laby = Labyrinthe(9, 13, nom_fichier='laby')
    pion = Pion(laby.entree, BLEU)
    fenetre = FenetreLaby(laby)
    direction = "aucune"
    while direction != "stop" and not pion.est_positionne_sur(laby.sortie):
        fenetre.afficher_tout(laby, pion)
        fenetre.actualiser()
        direction = fenetre.lire_fleche()
        pion.deplacer(laby, direction)
    fenetre.afficher_tout(laby, pion)
    fenetre.actualiser()
    fenetre.fermer()
