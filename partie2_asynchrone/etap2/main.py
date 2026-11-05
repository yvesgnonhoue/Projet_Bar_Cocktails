import sys          # Module d'interaction avec le système pour lire les arguments de la console (sys.argv)
import accessoires  # Module contenant les classes Accessoire, Pic, Bar et Logable
import employes     # Module contenant les classes Employe, Serveur et Bariste
from accessoires import Pic, Bar           # Importation directe des sous-classes d'accessoires
from employes import Bariste, Serveur     # Importation directe des sous-classes d'employés
from clients import Clients, usage        # Importation du gestionnaire de simulation et de la fonction d'aide usage()

if __name__ == "__main__":
    # Vérification des arguments donnés en ligne de commande
    if len(sys.argv) != 2: # Si l'utilisateur n'a pas fourni exactement 1 argument (le nom du fichier)
        usage()            # Affiche la bonne syntaxe d'utilisation et arrête le script

    fcommandes = sys.argv[1] # Récupère le nom du fichier de simulation (ex: "lundi.txt" ou "mardi.txt")

    # Configuration centralisée du fichier journal d'exécution (logs)
    logfile = "/tmp/borabora.log"              # Chemin vers le fichier de log partagé sur le système
    print(f"logging in {logfile}...")          # Message informatif affiché dans la console principale
    logf = open(logfile, "w")                  # Ouvre le fichier journal en mode écriture ("w")

    # Transmission du descripteur de fichier ouvert aux modules concernés
    accessoires.logf = logf  # Assigne le fichier ouvert à la variable globale logf du module accessoires
    employes.logf = logf     # Assigne le fichier ouvert à la variable globale logf du module employes

    # Chargement des données de simulation
    les_clients = Clients(fcommandes) # Lit et prépare les temporisations et boissons depuis le fichier fourni

    # Instanciation des accessoires (logs masqués avec verbose=False)
    le_pic = Pic(name="le_pic", verbose=False)  # Instancie le pic de post-it
    le_bar = Bar(name="le_bar", verbose=False)  # Instancie le bar de plateaux

    # Instanciation des employés avec filtrage des logs (Bob actif, Alice masquée)
    bob = Bariste(le_pic, le_bar, les_clients, name="bob", verbose=True)     # Bob génère des logs (verbose=True)
    alice = Serveur(le_pic, le_bar, les_clients, name="alice", verbose=False) # Alice est masquée (verbose=False)

    # Séquence d'exécution synchrone du service
    alice.run()   # Phase 1 : Le serveur lit et écrit toutes les commandes sur le pic
    bob.run()     # Phase 2 : Le bariste prépare l'intégralité des post-it du pic

    while len(le_bar) > 0:  # Phase 3 : Tant qu'il reste des plateaux prêts sur le bar...
        alice.servir()      # ... le serveur apporte et sert chaque commande aux clients

    # 8. Fermeture propre du fichier de journalisation à la fin du programme
    logf.close()