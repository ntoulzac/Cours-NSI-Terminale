try:
    from graphviz import Graph
except:
    print('Problème d\'importation de graphviz')

class Noeud:
    def __init__(self, etiquette, gauche=None, droit=None):
        """
        Crée une instance de la classe Noeud.
        - Entrées : etiquette (type quelconque)
                    gauche, droit (instances de la classe Noeud, ou None en l'absence d'enfant)
        """
        self.etiquette = etiquette
        self.gauche = gauche
        self.droit = droit
        
    def est_feuille(self):
        """
        Détermine si le noeud est une feuille.
        - Sortie : (booléen, True si le noeud est une feuille, False sinon)
        """
        return self.gauche is None and self.droit is None

class ArbreBinaire:
    def __init__(self, racine):
        """
        Crée une instance de la classe ArbreBinaire.
        - Entrée : racine (instance de la classe Noeud, ou None pour un arbre vide)
        """
        self.racine = racine
    
    def est_vide(self):
        """
        Détermine si l'arbre est vide.
        - Sortie : (booléen, True si l'arbre est vide, False sinon)
        """
        return self.racine is None
    
    def sa_gauche(self):
        if self.est_vide():
            raise IndexError('l\'arbre est vide')
        return ArbreBinaire(self.racine.gauche)
    
    def sa_droit(self):
        if self.est_vide():
            raise IndexError('l\'arbre est vide')
        return ArbreBinaire(self.racine.droit)
    
    def est_feuille(self):
        """
        Détermine si l'arbre est réduit à sa racine.
        - Sortie : (booléen, True si l'arbre est une feuille, False sinon)
        """
        return self.sa_gauche().est_vide() and self.sa_droit().est_vide()

    def taille(self):
        """
        Détermine la taille d'un arbre binaire.
        - Sortie : (entier)
        """
        if arbre.est_vide():
            return 0
        else:
            return 1 + arbre.sa_gauche().taille() + arbre.sa_droit().taille()
    
    def hauteur(self):
        """
        Détermine la hauteur d'un arbre binaire.
        - Sortie : (entier)
        On considère que la hauteur d'un arbre réduit à sa racine est 1.
        """
        if arbre.est_vide():
            return 0
        else:
            return 1 + max(arbre.sa_gauche().hauteur(), arbre.sa_droit().hauteur())
	
    def enregistrer(self, nom_fichier):
        """
        Enregistre l'arbre binaire dans un fichier texte.
        - Entrée : nom_fichier (chaîne de caractères)
        - Effet de bord : enregistrement dans un fichier
        """
        def noeud_dans_tableau(noeud, tab, pos):
            if not (noeud is None or noeud.etiquette is None):
                tab[pos] = noeud.etiquette
                noeud_dans_tableau(noeud.gauche, tab, 2*pos)
                noeud_dans_tableau(noeud.droit, tab, 2*pos + 1)
        hauteur = self.hauteur()
        tableau = [''] * (2**hauteur)
        noeud_dans_tableau(self.racine, tableau, 1)
        chaine = ''
        for k in range(1, len(tableau)):
            chaine = chaine + str(tableau[k]) + '\n'
        with open(nom_fichier, 'w') as fichier:
            fichier.write(chaine)
	
    def charger(self, nom_fichier):
        """
        Charge un arbre binaire depuis un fichier texte.
        - Entrée : nom_fichier (chaîne de caractères)
        - Effet de bord : modification de l'arbre
        """
        def noeud_dans_arbre(tab, pos):
            if pos >= len(tab)//2:
                return Noeud(tab[pos])
            else:
                return Noeud(tab[pos], noeud_dans_arbre(tab, 2*pos), noeud_dans_arbre(tab, 2*pos+1))
        tableau = [None]
        with open(nom_fichier, 'r') as fichier:
            for ligne in fichier:
                if ligne == '\n':
                    tableau.append(None)
                else:
                    tableau.append(ligne[:-1])
        self.racine = noeud_dans_arbre(tableau, 1)

    def afficher(self, enregistrer=False, nom_fichier=None):
        """
        Dessine l'arbre binaire dans le notebook.
        - Entrées : enregistrer (booléen, True pour enregistrer le dessin dans un fichier PNG, False sinon)
                    nom_fichier (chaîne, nom du fichier PNG sans extension)
        - Sortie : dot (représentation de l'arbre au format DOT, pour affichage dans un Notebook)
        - Effet de bord : enregistre éventuellement l'arbre dans un fichier
        """
        def representation(dot, noeud, i):
            """
            Fonction pour ajouter de manière récursive les valeurs des noeuds et relier par des arètes chaque noeud
            """
            if noeud is None:
                dot.node(str(i), "", shape="box", color="grey", width="0.6")
            else:
                dot.node(str(i), str(noeud.etiquette), shape="box", fontname = 'courier-bold', fontsize='14', width="0.6")
                if noeud.gauche is not None or noeud.droit is not None:
                    representation(dot, noeud.gauche, 2*i)
                    if noeud.gauche is None:
	                    dot.edge(str(i), str(2*i), color="grey")
                    else:
                        dot.edge(str(i), str(2*i))
                    #dot.node('inv'+str(2*i), "", style="invis", width="0.0")
                    #dot.edge(str(i), "inv"+str(2*i), style="invis", weight="10")
                    representation(dot, noeud.droit, 2*i+1)
                    if noeud.droit is None:
                   	    dot.edge(str(i), str(2*i+1), color="grey")
                    else:
                        dot.edge(str(i), str(2*i+1))
        try:
            dot = Graph(format='png')
            representation(dot, self.racine, 1)
            if enregistrer:
                dot.render(nom_fichier)
            return dot
        except:
            print("Erreur !")
    
    def creer_png(self, nom_fichier):
        self.afficher(True, nom_fichier)

if __name__ == '__main__':
    Gsa_1 = Noeud('Δ', Noeud('Β', Noeud('Α'), Noeud('Γ')), Noeud('Ζ', Noeud('Ε'), Noeud('Η')))
    Gsa_2 = Noeud('Κ', Noeud('Ι'), Noeud('Λ'))
    Gsa_3 = Noeud('Π', Noeud('Ξ', Noeud('Ν'), Noeud('Ο')), Noeud('Σ', Noeud('Ρ'), Noeud('Τ')))
    Gsa_4 = Noeud('Ψ', Noeud('Χ', Noeud('Φ'), None), Noeud('Ω'))
    alpha_grc = ArbreBinaire(Noeud('Μ', Noeud('Θ', Gsa_1, Gsa_2), Noeud('Υ', Gsa_3, Gsa_4)))
    alpha_grc.creer_png('exemple_arbre1')
    
    sa_1 = Noeud(1, Noeud(0), Noeud(2))
    sa_2 = Noeud(4, None, Noeud(5))
    sa_3 = Noeud(8, Noeud(7), None)
    sa_4 = Noeud(11, Noeud(10), Noeud(12))
    arbre = ArbreBinaire(Noeud(6, Noeud(3, sa_1, sa_2), Noeud(9, sa_3, sa_4)))
    arbre.creer_png('exemple_arbre2')
