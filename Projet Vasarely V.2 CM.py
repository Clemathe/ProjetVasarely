"""
Projet Vasarely, apprendre à coder en Python, Fun Mooc
Auteur : Clément M.
Date : 21/04/2020
Le programme dessine un pavage d'hexagone regulier.
Ce pavage peut-etre déformé par une pseudo sphère.
  Entrées : les dimensions du pavage (inf_gauche et sup_droit),
            la longueur d'un segment de l'hexagone ( longueur),
            les trois couleurs de l'hexagone (col = col1, col2, col3)
            les coordonnées du cercle de déformation (centre = x_c, y_c, z_c)
            le rayon du cercle de déformation (rayon)
  Résultat : Le programme dessine un pavage d'hexagone regulier composé de
             trois couleurs par tiers et qui en fonction des paramètres
             d'entrée sera déformé par une pseudo sphère
"""

import turtle  # module de dessin
from math import pi, sin, cos, sqrt, acos, asin, atan2
import re


def deformation(p, centre, rayon):
    """ Calcul des coordonnées d'un point suite à la déformation engendrée par la sphère émergeante
        Entrées :
          p : coordonnées (x, y, z) du point du dalage à tracer (z = 0) AVANT déformation
          centre : coordonnées (X0, Y0, Z0) du centre de la sphère
          rayon : rayon de la sphère
        Sorties : coordonnées (xprim, yprim, zprim) du point du dallage à tracer APRÈS déformation
     """
    x, y, z = p
    xprim, yprim, zprim = x, y, z
    xc, yc, zc = centre
    if rayon**2 > zc**2:
        zc = zc if zc <= 0 else -zc
        r = sqrt((x - xc) ** 2 + (y - yc) ** 2)
        # distance horizontale depuis le point à dessiner jusqu'à l'axe de la sphère
        rayon_emerge = sqrt(rayon ** 2 - zc ** 2) # rayon de la partie émergée de la sphère
        rprim = rayon * sin(acos(-zc / rayon) * r / rayon_emerge)
        if 0 < r <= rayon_emerge: # calcul de la déformation dans les autres cas
            xprim = xc + (x - xc) * rprim / r # les nouvelles coordonnées sont proportionnelles aux anciennes
            yprim = yc + (y - yc) * rprim / r
        if r <= rayon_emerge:
            beta = asin(rprim / rayon)
            zprim = zc + rayon * cos(beta)
            if centre[2] > 0:
                zprim = -zprim
    return (xprim, yprim, zprim)



def hexagone(point, longueur, col, centre, rayon):
    """ Dessine avec le module turtle un pave hexagonal regulier ou pas dans
        un repere orthonormé
        Entrées :
          point : tuple des coordonnées d'origine (x, y,z) de l'hexagone
          longueur : longueur d'une arrête de l'hexagone
          col : tuple de trois couleurs. Un tiers de l'air de l'hexagone par
                couleur
          centre : tuple des coordonnées de la "sphere" déformante
          rayon : rayon de la "sphère déformante
        Résultats : Tracage et remplissage d'un pave hexagonal déformé ou pas
                    par la sphère et comportant des coordonnées spécifiques
    """

    x, y, z = point
    a, b = pi / 3, pi / 3  # pour le calcul des coordonnées, cos(a) et sin(b)

    # initialisation
    turtle.hideturtle()
    turtle.up()
    turtle.goto(deformation((x, y, z), centre, rayon)[0],
                deformation((x, y, z), centre, rayon)[1])
    turtle.down()
    # dessine un hexagone divisé en 3 parties égales de couleurs différentes
    for i in range(3):
        a -= pi / 3
        b -= pi / 3
        turtle.goto(deformation((x, y, z), centre, rayon)[0],
                    deformation((x, y, z), centre, rayon)[1])
        turtle.color(col[i])
        turtle.begin_fill()
        for j in range(3):  # dessine 4 arrêtes
            coordonnees = deformation((x + longueur * cos(a),
                                       y + longueur * sin(b), z), centre, rayon)
            turtle.goto(coordonnees[0], coordonnees[1])
            a += pi / 3
            b += pi / 3

        turtle.end_fill()
    return None


def pavage(inf_gauche, sup_droit, longueur, col, centre, rayon):
    """
    Effectue un pavage dans un cadre de taille définie
    Entrées :
        inf_gauche: Coordonnées inférieurs gauche du bord du cadre
        sup_droit: Coordonnées supérieurs gauche du bord du cadre
        longueur: longueur d'une arrête de l'hexagone
        col: tuple de 3 couleurs. Un tiers de l'aire de l'hexagone par couleurs
        centre: tuple des coordonnées de la "sphere" déformante
        rayon: rayon de la "sphère déformante
    Résultats :
    """

    coordo = inf_gauche
    compteur_parite = 0  # afin de changer les paramètres une fois sur deux
    m_1, m_2 = 1, 2  # Multiplicateur pour les coordonnées de 'coordo'
    pave_par_ligne = int((sqrt(
        (inf_gauche[0] - sup_droit[0]) ** 2 + (inf_gauche[1] - sup_droit[1])
        ** 2)) / 2) // (longueur * 2)  # Calcul le nombre de pavé par ligne

    while coordo[1] < sup_droit[1]:
        turtle.tracer(2, 5)
        for pave in range(pave_par_ligne):
            hexagone(coordo, longueur, col, centre, rayon)
            # écart entre les pavés d'une même ligne
            coordo = (coordo[0] + longueur * 3, coordo[1], 0)

        if compteur_parite % 2 == 0:  # condition de parité
            # initie un decalage à droite et en hauteur pour une nouvelle ligne
            coordo = (inf_gauche[0] + longueur * 1.5, inf_gauche[1] +
                      (sqrt(longueur ** 2 - (longueur / 2) ** 2)) * m_1, 0)
            m_1 += 2
            compteur_parite += 1  # iter le compteur de parité
        else:  # Décalage à droite et en hauteur
            coordo = (inf_gauche[0], inf_gauche[1] +
                      (sqrt(longueur ** 2 - (longueur / 2) ** 2)) * m_2, 0)
            m_2 += 2
            compteur_parite += 1  # iter le compteur de parité
    return None


def parametre_cadre():
    """Récupère les inputs pour les dimensions de la zone de pavage et retourne ces dernières"""
    def control_cadre(point_cadre):
        """ Controle les inputs, construit les coordonnées et retourne ces dernières"""
        while point_cadre.strip('-+').isnumeric() is not True:
            point_cadre = (input("  la valeur doit être un nombre entier positif ou négatif : "))
        point_cadre = (int(point_cadre), int(point_cadre), 0)
        return point_cadre

    temoin1 = False
    while not temoin1:
        inf_gauche_p = control_cadre(input("Coin inférieur gauche du pavage (val, val) : "))
        sup_droit_p = control_cadre(input("Coin supérieur droit du pavage (val, val): "))

        if int(int(sup_droit_p[0])- inf_gauche_p[0])   <= 0:
            print(" le coin supérieur droit doit avoir une valeur supérieure au coin inférieur gauche")
        else:
            temoin1 = True
        return inf_gauche_p, sup_droit_p

def couleur():
    """Récupère les inputs des couleurs et les retournent"""
    def control_couleur():
        """ Contrôle la couleur selon une liste prédéfinie et retourne cette dernière"""
        liste_couleur = ["black", "white", "grey", "red", "orange", "green", "blue", "navy", "yellow", "gold",
                         "tan", "brown", "sienna", "wheat", "cyan", "pink", "salmon", "violet", "purple"]
        color = input("Entrez une couleur (blue, red ou yellow...) : ")
        while color not in liste_couleur:
            color = input('  la couleur doit être : black, white, grey, red, orange, green, blue, navy,'
                          ' yellow, gold, tan, brown, sienna, wheat, cyan, pink, salmon, violet, purple : ')
        return color
    col1 = control_couleur()
    col2 = control_couleur()
    col3 = control_couleur()
    return col1, col2, col3

def longueur():
    """ Contrôle l'input de la longueur demandée et retourne cette dernière"""
    longueur = input("Longueur d'une arrête de pavage : ")
    while longueur.strip('+').isdigit() is not True:
        longueur = input("  la valeur doit être un nombre entier positif : ")
    longueur = int(longueur)
    return longueur

def sphere():
    """Parametrage des coordonnées de la sphère de déformation,
    Retourne les coordonnées et le rayon"""
    def control_point(point):
        """ Contrôle l'input d'un point et retourne un point valide de type int"""
        while point.strip('+-').isdigit() is not True:
            point = (input("  la valeur doit être un nombre entier positif ou négatif : "))
        point = int(point)
        return point

    x_c = control_point(input("Abscisse du centre de la sphère : "))
    y_c = control_point(input("Ordonnée du centre de la sphère : "))
    z_c = control_point(input("Hauteur du centre de la sphère : "))
    centre = (x_c, y_c, z_c)  # Coordonnées du centre de la sphère

    rayon = input("Rayon de la sphère : ")  # Rayon de la sphère
    while rayon.strip("+").isdigit() is not True:   # Contrôle de l'input
        rayon = (input("  la valeur doit être un nombre entier positif : "))
    rayon = int(rayon)
    return centre, rayon

# Code principal
# En-tête et choix du parametrage ou non
print("\n  --| PROJET VASARELY |--\n")
ask = input("Voulez vous personnaliser les paramètres pour "
            "la création de l'artwork ?\n  Entrez O ou N : ")
# Code pour le parametrage
if ask == 'O' or ask == 'o':
    # Parametrage de la dimension du pavage et vérification des input
    inf_gauche, sup_droit = parametre_cadre()
    # Parametrage des couleurs et vérifications des input
    col = couleur()
    # Parametrage et verification de la longueur d'un coté de l'hexagone
    longueur = longueur()
    # Parametrage de la sphère de déformation
    centre, r = sphere()
    pavage(inf_gauche, sup_droit, longueur, col, centre, r)
    turtle.done()
# Code pour le parametrage automatique
elif ask == "N".strip() or ask == 'n':
    pavage((-300, -300, 0), (300, 300, 0), 30, ("#222527", "#E2D50B", '#096AB5'), (-50, -50, -30), 230)
    turtle.done()
else:
    ask = input("Je n'ai pas compris votre réponse.\n"
                "  Voulez vous personnaliser les paramètres ? Entrez O ou N : ")



