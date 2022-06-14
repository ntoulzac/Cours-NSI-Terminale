import pygame
from math import pi, cos, sin
from time import sleep
from PIL import Image

pygame.init()
pygame.font.init()

NOIR = (0, 0, 0)
BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)

class File:
    def __init__(self):
        """
        Crée une file vide.
        """
        self.liste = [] # Création d'une liste vide
    
    def est_vide(self):
        """
        Détermine si la file est vide ou non.
        - Sortie : (booléen, True si la pile est vide, False sinon)
        """
        return self.liste == []

    def enfiler(self, elem):
        """
        Ajoute un élément en queue de file.
        - Entrée : elem (élément à ajouter)
        """
        self.liste.insert(0, elem) # Ajout d'un élément au début de la liste
    
    def defiler(self):
        """
        Retire un élément de la tête de la file et le renvoie.
        - Sortie : (élément retiré)
        """
        if self.est_vide():
            raise ValueError('la file est vide')
        return self.liste.pop() # Retrait d'un élément à la fin de la liste

class FenetreJosephe:
    """
    Classe permettant de gérer une fenêtre pygame pour l'affichage du problème de Josèphe.
    """
    def __init__(self):
        """
        Ouvre une fenêtre pygame.
        """
        pygame.display.init()
        self.taille = 600
        self.fen = pygame.display.set_mode((self.taille, self.taille))
        pygame.display.set_caption('Problème de Josèphe')
        taille_police = self.taille//30
        self.police = pygame.font.SysFont('Courier New', taille_police)
        self.R = self.taille*0.4

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

    def afficher_nombre(self, k, n, couleur):
        """
        Affiche la valeur k en couleur parmi n valeurs autour d'un cercle.
        - Entrées : k (entier, valeur à afficher autour du cercle)
                    n (entier, nombre initial de valeurs autour du cercle)
                    couleur (triplet RGB, couleur pour l'affichage de k)
        """
        texte = self.police.render(str(k), True, couleur, BLANC)
        angle = pi/2 - k/n*2*pi
        posH = self.taille/2+self.R*cos(angle)-texte.get_width()/2
        posV = self.taille/2-self.R*sin(angle)-texte.get_height()/2
        self.fen.blit(texte, (posH, posV))
    
    def actualiser(self, liste, n, en_rouge = None):
        """
        Affiche une liste de valeurs parmi n valeurs autour d'un cercle.
        - Entrées : liste (liste de valeurs à afficher en noir)
                    n (entier, nombre initial de valeurs autour du cercle)
                    en_rouge (entier, valeur éventuelle à afficher en rouge)
        """
        self.effacer()
        for valeur in liste:
            self.afficher_nombre(valeur, n, NOIR)
        if en_rouge:
            self.afficher_nombre(en_rouge, n, ROUGE)
        pygame.display.update()

def visualiser(n, p, gif = False):
	"""
	Affiche la solution du problème de Josèphe pour n et p dans une fenêtre pygame.
	- Entrées : n, p (entiers strictement positifs)
	            gif (booléen, True pour enregistrer la solution sous forme de gif, False par défaut)
	"""
	if gif:
		images = []
		nb_im = 0
	fil = File()
	for k in range(n):
		fil.enfiler(k+1)
	fenetre = FenetreJosephe()
	fenetre.actualiser(fil.liste, n)
	if gif:
		pygame.image.save(fenetre.fen, f"A_JETER/im{nb_im}.png")
		images.append(Image.open(f"A_JETER/im{nb_im}.png"))
		nb_im += 1
	for _ in range(n-1):
		sleep(1)
		for k in range(p-1):
			fil.enfiler(fil.defiler())
		elimine = fil.defiler()
		fenetre.actualiser(fil.liste, n, elimine)
		if gif:
			pygame.image.save(fenetre.fen, f"A_JETER/im{nb_im}.png")
			images.append(Image.open(f"A_JETER/im{nb_im}.png"))
			nb_im += 1
	sleep(1)
	fenetre.actualiser(fil.liste, n)
	if gif:
		pygame.image.save(fenetre.fen, f"A_JETER/im{nb_im}.png")
		images.append(Image.open(f"A_JETER/im{nb_im}.png"))
		nb_im += 1
		images[0].save(f"josephe_{n}_{p}.gif", save_all = True, append_images = images[1:], duration = 1000, loop = 0)
	sleep(1)
	fenetre.fermer()
