class Pile:
    def __init__(self):
        """
        Crée une pile vide.
        """
        self.liste = [] # Création d'une liste vide
    
    def est_vide(self):
        """
        Détermine si la pile est vide ou non.
        - Sortie : (booléen, True si la pile est vide, False sinon)
        """
        return self.liste == []

    def empiler(self, elem):
        """
        Ajoute un élément au sommet de la pile.
        - Entrée : elem (élément à ajouter)
        """
        self.liste.append(elem) # Ajout d'un élément à la fin de la liste
    
    def depiler(self):
        """
        Retire un élément du sommet de la pile et le renvoie.
        - Sortie : (élément retiré)
        """
        if self.est_vide():
            raise ValueError('la pile est vide')
        return self.liste.pop() # Retrait d'un élément à la fin de la liste
    
    def __str__(self):
        """
        Permet un affichage de la pile via la fonction print.
        """
        chaine = '|'
        for k in range(len(self.liste)):
            chaine += f" {self.liste[k]} |"
        return chaine


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
    
    def __str__(self):
        """
        Permet un affichage de la file via la fonction print.
        """
        chaine = '|'
        for k in range(len(self.liste)):
            chaine += f" {self.liste[k]} |"
        return chaine
 
if __name__ == '__main__':
    L = Liste(None)
    for k in range(10):
        L.inserer_en_tete(k)
    print(L)
    L.renverser()
    print(L)
    P = Pile()
    for k in range(20):
        P.empiler(k**2)
    print(P)
    for k in range(10):
        P.depiler()
    print(P)
    F = File()
    for k in range(20):
        F.enfiler(k**2)
    print(F)
    for k in range(10):
        F.defiler()
    print(F)
