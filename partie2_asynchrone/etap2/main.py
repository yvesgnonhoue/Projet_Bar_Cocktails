import sys          # Module d'interaction avec le système pour lire les arguments de la console (sys.argv)[cite: 7, 10]
import asyncio      # Module d'asynchronisme pour gérer la boucle d'événements et le lancement des coroutines[cite: 7]
import accessoires  # Module contenant les classes Accessoire, Pic, Bar et Logable[cite: 7, 10]
import employes     # Module contenant les classes Employe, Serveur et Bariste[cite: 7, 10]
from accessoires import Pic, Bar           # Importation directe des sous-classes d'accessoires[cite: 7, 10]
from employes import Bariste, Serveur     # Importation directe des sous-classes d'employés[cite: 7, 10]
from clients import Clients, usage        # Importation du gestionnaire de simulation et de la fonction d'aide usage()[cite: 7, 10]


async def main_async(fcommandes):
    """
    Coroutine principale organisant l'exécution asynchrone parallèle du bar.[cite: 7]
    """
    # Configuration centralisée du fichier journal d'exécution (logs)[cite: 7, 10]
    logfile = "/tmp/borabora.log"              # Chemin vers le fichier de log partagé sur le système[cite: 7, 10]
    print(f"logging in {logfile}...")          # Message informatif affiché dans la console principale[cite: 7, 10]
    logf = open(logfile, "w")                  # Ouvre le fichier journal en mode écriture ("w")[cite: 7, 10]
    print("\n---", file=logf, flush=True)

    # Transmission du descripteur de fichier ouvert aux modules concernés[cite: 7, 10]
    accessoires.logf = logf  # Assigne le fichier ouvert à la variable globale logf du module accessoires[cite: 7, 10]
    employes.logf = logf     # Assigne le fichier ouvert à la variable globale logf du module employes[cite: 7, 10]

    # Chargement des données de simulation[cite: 7, 10]
    les_clients = Clients(fcommandes) # Lit et prépare les temporisations et boissons depuis le fichier fourni[cite: 7, 10]

    # Instanciation des accessoires (logs masqués avec verbose=False)[cite: 7, 10]
    le_pic = Pic(name="le_pic", verbose=False)  # Instancie le pic de post-it (asyncio.Queue)[cite: 7, 10]
    le_bar = Bar(name="le_bar", verbose=False)  # Instancie le bar de plateaux (asyncio.Queue)[cite: 7, 10]

    # Instanciation des employés avec filtrage des logs (Bob et Alice actifs)[cite: 7, 10]
    bob = Bariste(le_pic, le_bar, les_clients, name="bob", verbose=True)     # Bob génère des logs (verbose=True)[cite: 7, 10]
    alice = Serveur(le_pic, le_bar, les_clients, name="alice", verbose=True)  # Alice génère des logs (verbose=True)[cite: 7, 10]

    # Lancement concourant de toutes les coroutines dans la boucle d'événements (Event Loop) :[cite: 7]
    # 1. Prise de commandes par Alice (run_prise_commande)[cite: 7]
    # 2. Préparation des verres par Bob (run)[cite: 7]
    # 3. Service des plateaux prêts par Alice (run_service)[cite: 7]
    await asyncio.gather(
        alice.run_prise_commande(),
        bob.run(),
        alice.run_service()
    )

    # Fermeture propre du fichier de journalisation à la fin du programme[cite: 7, 10]
    logf.close()


if __name__ == "__main__":
    # Vérification des arguments donnés en ligne de commande[cite: 7, 10]
    if len(sys.argv) != 2: # Si l'utilisateur n'a pas fourni exactement 1 argument (le nom du fichier)[cite: 7, 10]
        usage()            # Affiche la bonne syntaxe d'utilisation et arrête le script[cite: 7, 10]

    fcommandes = sys.argv[1] # Récupère le nom du fichier de simulation (ex: "lundi.txt" ou "mardi.txt")[cite: 7, 10]

    # Point d'entrée principal : lance la coroutine main_async via la boucle d'événements asyncio[cite: 7]
    asyncio.run(main_async(fcommandes))