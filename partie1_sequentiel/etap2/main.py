import sys
from accessoires import Pic, Bar
from employes import Bariste, Serveur
from clients import Clients, usage

if __name__ == "__main__":
    # 1. Vérification de la présence de l'argument dans le terminal (ex: python3 main.py lundi)
    if len(sys.argv) != 2:
        usage()
        
    fcommandes = sys.argv[1]

    # 2. Instanciation des accessoires
    le_bar = Bar()
    le_pic = Pic()

    # 3. Instanciation du gestionnaire de clients
    les_clients = Clients(fcommandes)

    # 4. Instanciation des employés avec l'injection des 3 dépendances (pic, bar, clients)
    # Les messages "[Nom]: prêt pour le service" s'affichent automatiquement à cette étape.
    bob = Bariste(le_pic, le_bar, les_clients)
    alice = Serveur(le_pic, le_bar, les_clients)

    # 5. Phase 1 : Prise des commandes par le serveur depuis le fichier text
    alice.run()

    # 6. Phase 2 : Fabrication de tous les post-it du pic par le bariste
    bob.run()

    # 7. Phase 3 : Service des plateaux prêts aux clients
    while len(le_bar) > 0:
        alice.servir()