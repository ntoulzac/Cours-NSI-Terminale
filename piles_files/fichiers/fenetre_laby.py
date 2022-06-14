import pygame
pygame.init()
pygame.font.init()

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)

COULEURS = {0 : BLANC, 1 : NOIR, 2 : BLEU, 3 : ROUGE}

class FenetreLaby:
    """
    Classe permettant de gérer une fenêtre pygame pour l'affichage d'un labyrinthe.
    """
    def __init__(self, laby):
        """
        Ouvre une fenêtre pygame aux dimensions d'un labyrinthe.
        - Entrée : laby (instance de la classe Labyrinthe)
        """
        self.t_c = min(800//laby.nb_c, 600//laby.nb_l)
        pygame.display.init()
        self.fen = pygame.display.set_mode((laby.nb_c*self.t_c, laby.nb_l*self.t_c))
        pygame.display.set_caption('Labyrinthe')

    def fermer(self):
        """
        Ferme la fenêtre pygame.
        """
        pygame.display.quit()

    def effacer(self):
        """
        Efface la fenêtre pygame en la remplissant de blanc.
        """
        self.fen.fill(BLANC)

    def afficher_case(self, pos, couleur, mise_a_jour = True):
        """
        Colorie une case.
        - Entrées : pos (p-uplet de la forme (L, C) correspondant à la position de la case à colorer)
                    couleur (p-uplet de la forme (R, G, B))
                    mise_a_jour (booléen optionnel, True pour que la case soit colorée immédiatement, False sinon)
        """
        L, C = pos
        pygame.draw.rect(self.fen, couleur, (C*self.t_c, L*self.t_c, self.t_c, self.t_c))
        if mise_a_jour:
            pygame.display.update()
    
    def actualiser(self, laby):
        """
        Affiche dans la fenêtre pygame un labyrinthe.
        - Entrée : laby (instance de la classe Labyrinthe)
        """
        for L in range(laby.nb_l):
            for C in range(laby.nb_c):
                self.afficher_case((L, C), COULEURS[laby.grille[L][C]], mise_a_jour = False)
        pygame.display.update()
