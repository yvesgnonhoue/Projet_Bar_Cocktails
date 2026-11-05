import sys          # Module d'interaction avec le système pour lire les arguments de la console (sys.argv)
import asyncio      # Module d'asynchronisme pour gérer la boucle d'événements et le lancement des coroutines
import accessoires  # Module contenant les classes Accessoire, Pic, Bar et Logable
import employes     # Module contenant les classes Employe, Serveur et Bariste
from accessoires import Pic, Bar           # Importation directe des sous-classes d'accessoires
from employes import Bariste, Serveur     # Importation directe des sous-classes d'employés
from clients import Clients, usage        # Importation du gestionnaire de simulation et de la fonction d'aide usage()


async def main_async(fcommandes):
    """
    Coroutine principale organisant l'exécution asynchrone parallèle du bar avec suspension coopérative.
    """
    # Configuration centralisée du fichier journal d'exécution (logs)
    logfile = "/tmp/borabora.log"              # Chemin vers le fichier de log partagé sur le système
    print(f"logging in {logfile}...")          # Message informatif affiché dans la console principale
    logf = open(logfile, "w")                  # Ouvre le fichier journal en mode écriture ("w")
    print("\n---", file=logf, flush=True)

    # Transmission du descripteur de fichier ouvert aux modules concernés
    accessoires.logf = logf  # Assigne le fichier ouvert à la variable globale logf du module accessoires
    employes.logf = logf     # Assigne le fichier ouvert à la variable globale logf du module employes

    # Chargement des données de simulation
    les_clients = Clients(fcommandes) # Lit et prépare les temporisations et boissons depuis le fichier fourni

    # Instanciation des accessoires (logs masqués avec verbose=False)
    le_pic = Pic(name="le_pic", verbose=False)  # Instancie le pic de post-it (asyncio.Queue)
    le_bar = Bar(name="le_bar", verbose=False)  # Instancie le bar de plateaux (asyncio.Queue)

    # Instanciation des employés avec filtrage des logs (Bob et Alice actifs)
    bob = Bariste(le_pic, le_bar, les_clients, name="bob", verbose=True)     # Bob génère des logs (verbose=True)
    alice = Serveur(le_pic, le_bar, les_clients, name="alice", verbose=True)  # Alice génère des logs (verbose=True)

    # Lancement concourant de toutes les coroutines dans la boucle d'événements (Event Loop) :
    # 1. Prise de commandes par Alice (run_prise_commande)
    # 2. Préparation des verres par Bob (run)
    # 3. Service des plateaux prêts par Alice (run_service)
    await asyncio.gather(
        alice.run_prise_commande(),
        bob.run(),
        alice.run_service()
    )

    # Fermeture propre du fichier de journalisation à la fin du programme
    logf.close()


if __name__ == "__main__":
    # Vérification des arguments donnés en ligne de commande
    if len(sys.argv) != 2: # Si l'utilisateur n'a pas fourni exactement 1 argument (le nom du fichier)
        usage()            # Affiche la bonne syntaxe d'utilisation et arrête le script

    fcommandes = sys.argv[1] # Récupère le nom du fichier de simulation (ex: "lundi.txt" ou "mardi.txt")

    # Point d'entrée principal : lance la coroutine main_async via la boucle d'événements asyncio
    asyncio.run(main_async(fcommandes))