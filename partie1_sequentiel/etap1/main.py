from accessoires import Pic, Bar
from employes import Bariste, Serveur

if __name__ == "__main__":
    print("Bienvenue dans le programme de gestion des accessoires et des employés.")

    # 1. Instanciation des accessoires (files FIFO)
    le_bar = Bar()
    le_pic = Pic()

    # 2. Instanciation des employés (les messages "prêt pour le service" s'affichent automatiquement)
    bob = Bariste(le_pic, le_bar)
    alice = Serveur(le_pic, le_bar)

    # 3. Phase 1 : Prise des commandes par le serveur via la console
    alice.run()

    # 4. Phase 2 : Fabrication de tous les post-it du pic par le bariste
    bob.run()

    # 5. Phase 3 : Service des plateaux prêts aux clients
    while len(le_bar) > 0:
        alice.servir()