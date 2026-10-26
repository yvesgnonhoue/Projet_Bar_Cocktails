from accessoires import Pic, Bar
from employes import Employe, Bariste, Serveur


if __name__ == "__main__":
    print("Bienvenue dans le programme de gestion des accessoires et des employés.")
    
    le_bar = Bar()
    le_pic = Pic()
    bob = Bariste(le_pic, le_bar)
    alice = Serveur(le_pic, le_bar)
    alice.run()
    bob.run()
    while le_bar:
        alice.servir()

