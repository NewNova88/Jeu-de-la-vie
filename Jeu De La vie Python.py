#################### - Le Jeu De La Vie - ####################

'''
Ce jeu de la vie est aléatoire (on ne place pas les cellules à la souris).

Néanmoins, afin de ne pas etre limité par le cadre, j'utilise ici
un tableau torique. Cela permet par exemple qu'une structure mouvante partant vers l'extreme
droite se retrouvera à gauche pour continuer son mouvement (idéal pour étudier les planeurs)

On a donc les entrées de la hauteur et de la largeur au début 

Une fois les valeurs entrées, on a donc l'interface qui montre la table avec les cellules mortes et vivantes évoluant dans l'environnement.
On pourra avoir plusieurs résultats comme des structures stables (un carré de 2x2 cellules) ou instables (comme le clignotant ou le planeur,
un peu plus complexe).

Ici, on utilise l'interface intégrée tkinter, parce que dans ce TP/Projet, les librairies externes ne sont pas autorisées. On n'utilisera donc pas
pygame, et de toute façon il ne serait pas très efficace pour le jeu de la vie.

Le programme est commenté et trié, n'utilisant donc pas de variables globales, et utilisant des raccourcis Python mineurs (notamment
pour la création des matrices) afin d'atténuer la longueur du code.

On a en premier les deux importations, puis toutes les définitions des fonctions et procédures, pour enfin finir par le "MAIN", ou juste la partie
principale où l'on trouve les appels de fonctions.
'''

#Importations de tkinter pour l'interface et de random (ici on veut juste randrange) pour l'aléatoire
from tkinter import *
from random import randrange

########## - FONCTIONS ET PROCEDURES - ##########

#Calcule et dessine le nouveau tableau
def tableau():
    calculer()
    draw()
    window.after(1, tableau)

#Initialisation
def initialisation():
    for y in range(hauteur):
        for x in range(largeur):
            #on met les cellules mortes d'abord, et la variable temporaire à morte aussi.
            state[x][y] = mort
            temp[x][y] = mort
            cellule[x][y] = canvas.create_rectangle((x*cote, y*cote,(x+1)*cote, (y+1)*cote), outline="gray", fill="white") #création des rectangles blancs

    #On placeau hasard environ 25% de cellules en vie (permet d'éviter qu'il n'y aie qu'1 seule cellule, et donc de ne rien produire)
    for i in range(largeur*hauteur//4):
        state[randrange(largeur)][randrange(hauteur)] = vivant

#On applique les règles
def calculer():
    for y in range(hauteur):
        for x in range(largeur):
            nombre_voisins = compte_voisins(x,y) #on appelle la fonction permettant de connaître le nombre de voisins
            
            #Règle 1 - Mort d'isolement
            if state[x][y] == vivant and nombre_voisins < 2: #Si la cellule est vivante et qu'elle a un nombre de voisins inférieur à deux
                temp[x][y] = mort #alors elle meurt
            
            #Règle 2 - Toute cellule avec 2 ou 3 voisins survit.
            if state[x][y] == vivant and (nombre_voisins == 2 or nombre_voisins == 3): #Si une cellule est vivante et qu'elle a deux ou trois voisins
                temp[x][y] = vivant #alors elle reste en vie
            
            #Règle 3 - Mort par surpopulation
            if state[x][y] == vivant and nombre_voisins > 3: #si une cellule est vivante et qu'elle a plus de trois voisins
                temp[x][y] = mort #alors elle meurt
            
            #Règle 4 - Naissance
            if state[x][y] == mort and nombre_voisins == 3: #si une cellule est morte et qu'elle a trois voisins
                temp[x][y] = vivant #alors elle nait (son état est à vivant)
        
    for y in range(hauteur):
        for x in range(largeur):
            state[x][y] = temp[x][y] #l'état prend la valeur de la variable temporaire, définis par les tests des quatre règles ci-dessus

#On compte les voisins en vie (tableau torique, voir plus haut)
def compte_voisins(x,y):
    nombre_voisins = 0 #compteur du nombre de voisins à 0

    #on teste si chaque cellule à un voisin selon les 8 directions

    #diagonale haut-gauche
    if state[(x-1)%largeur][(y+1)%hauteur] == 1:
        nombre_voisins += 1

    #haut
    if state[x][(y+1)%hauteur] == 1:
        nombre_voisins += 1

    #Diagonale haut-droite
    if state[(x+1)%largeur][(y+1)%hauteur] == 1:
        nombre_voisins += 1

    #gauche
    if state[(x-1)%largeur][y] == 1:
        nombre_voisins += 1

    #droite
    if state[(x+1)%largeur][y] == 1:
        nombre_voisins += 1

    #Diagonale bas-gauche
    if state[(x-1)%largeur][(y-1)%hauteur] == 1:
        nombre_voisins += 1

    #bas
    if state[x][(y-1)%hauteur] == 1:
        nombre_voisins += 1

    #diagonale bas-droite
    if state[(x+1)%largeur][(y-1)%hauteur] == 1:
        nombre_voisins += 1
        
    return nombre_voisins #on retourne la valeur du nombre de voisins

#On dessine toute les cellules
def draw():
    for y in range(hauteur):
        for x in range(largeur):
            if state[x][y]==0: #si l'état est à 0 (donc cellule morte)
                couleur = "white" #on met la couleur blanche
            else: #sinon elle est vivante
                couleur = "black" #donc on met la couleur noire
            canvas.itemconfig(cellule[x][y], fill=couleur) #application du changement de couleur

########## - MAIN - ##########
            
#Définitions des variables
hauteur = int(input("Entrez le nombre de cellules à la verticale : ")) #Hauteur du tableau (fait donc varier le nombre de cellules à la verticale, plus il y en a, plus c'est lent)
largeur = int(input("Entrez le nombre de cellules à l'horizontale : ")) #Largeur du tableau (fait donc varier le nombre de cellules à l'horizontale, plus il y en a, plus c'est lent)
cote = 10  #Taille d'une cellule (fixe, car il ne sert à rien de la modifier)
vivant = 1 #L'état vivant est définit à 1 (comme le binaire, en "True")
mort = 0    #L'état mort est définit à 0 (comme en binaire, en "False")

#Créer les matrices
cellule = [[0 for row in range(hauteur)] for col in range(largeur)] #utilisation des raccourcis python (non obligatoire mais pratique)
state = [[mort for row in range(hauteur)] for col in range(largeur)]
temp = [[mort for row in range(hauteur)] for col in range(largeur)]


#Rassemblement des fonctions et procédures pour faire le programme
window = Tk()
window.title("Jeu de la vie")
canvas = Canvas(window, width=cote*largeur, height=cote*hauteur, highlightthickness=0)
canvas.pack()

initialisation()
tableau()

window.mainloop()
