import pygame
from time import sleep
import requests

class Fenetre:
    def __init__(self, N):
        self.N = N
        pygame.init()
        self.t_c = 600 // self.N  # Taille maxi de la fenêtre : 600 px
        pygame.display.init()
        self.fen = pygame.display.set_mode((self.N * self.t_c, self.N * self.t_c))
        pygame.display.set_caption(f'Le problème des {self.N} reines')
        self.charger_image_reine()

    def charger_image_reine(self):
        with open("reine.png", "wb") as fichier:
            fichier.write(requests.get("https://ntoulzac.github.io/Cours-NSI-Terminale/mise_au_point/images/reine.png").content)
        reine = pygame.image.load("reine.png")
        self.images_reines = [pygame.transform.scale(reine, (self.t_c, self.t_c)), pygame.transform.scale(reine, (self.t_c, self.t_c))]
        for x in range(self.images_reines[1].get_width()):       #
            for y in range(self.images_reines[1].get_height()):  # 
                RGBA = self.images_reines[1].get_at((x,y))       # Inversion des couleurs
                for i in range(3):                               # de l'image de la reine
                    RGBA[i] = 255 - RGBA[i]                      # 
                self.images_reines[1].set_at((x,y), RGBA)        #
    
    def afficher_plateau(self, reines, coups_impossibles, coups_injouables_visibles=True):
        self.fen.fill((0, 0, 0))  # La fenêtre est remplie de noir
        for L in range(self.N):
            for C in range(self.N):
                if (L+C) % 2 == 0:  # Une case sur deux est blanche
                    pygame.draw.rect(self.fen, (255, 255, 255), (C*self.t_c, L*self.t_c, self.t_c, self.t_c))
        for (L, C) in reines:
            if (L+C) % 2 == 0:  # Sur les cases blanches, la reine a des couleurs normales
                self.fen.blit(self.images_reines[0], (C*self.t_c, L*self.t_c))
            else:  ## Sur les cases noires, la reine a des couleurs inversées
                self.fen.blit(self.images_reines[1], (C*self.t_c, L*self.t_c))
        if coups_injouables_visibles:
            for (L, C) in coups_impossibles:  # Les coups impossibles sont représentés par des carrés rouges
                pygame.draw.rect(self.fen, (255, 0, 0), ((C+0.4)*self.t_c, (L+0.4)*self.t_c, 0.2*self.t_c, 0.2*self.t_c))
        pygame.display.flip()

    def recuperer_clic(self, coups_impossibles):
        while True:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.fermer_fenetre()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    C, L = x // self.t_c, y // self.t_c
                    if (L, C) not in coups_impossibles:  # On ne récupère pas les clics correspondant à des coups impossibles
                        return (L, C)

    def enregistrer_image(self):
        pygame.image.save(self.fen, f'victoire_{self.N}_reines.png')

    def fermer_fenetre(self):
        pygame.quit()
        
class N_Reines:
    def __init__(self, N):
        self.N = N
        self.fenetre = Fenetre(N)
        self.reines = []
        self.coups_impossibles = []
        self.fenetre.afficher_plateau(self.reines, self.coups_impossibles)
        
    def jouer(self):
        while len(self.reines) < self.N:
            self.jouer_coup()
        self.enregistrer_victoire()
        self.fenetre.fermer_fenetre()
        
    def calculer_coups_injouables(self):
        self.coups_impossibles = []
        for (L, C) in self.reines:
            for a in range(self.N):
                for b in range(self.N):
                    if (L, C) != (a, b) and (a == L or b == C or abs(a-L) == abs(b-C)):
                        self.coups_impossibles.append((a, b))
    
    def jouer_coup(self):
        (L, C) = self.fenetre.recuperer_clic(self.coups_impossibles)
        if (L, C) not in self.reines:  # Si on clique sur une case vide, on y place une reine
            self.reines.append((L, C))
        else:  # Si on clique sur une case occupée par une reine, on la retire
            k = 0
            while self.reines[k] != (L, C):
                k = k + 1
            del self.reines[k]
        self.calculer_coups_injouables()
        self.fenetre.afficher_plateau(self.reines, self.coups_impossibles)
        
    def enregistrer_victoire(self):
        self.fenetre.afficher_plateau(self.reines, self.coups_impossibles, False)
        sleep(1)
        self.fenetre.enregistrer_image()
    
jeu = N_Reines(8)
jeu.jouer()