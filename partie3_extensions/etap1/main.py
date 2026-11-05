import sys
import asyncio
import accessoires
import employes
from accessoires import Pic, Bar
from employes import Bariste, Serveur
from clients import Clients, usage

async def main_async(fcommandes):
    # Configuration du fichier de log centralisé
    logfile = "/tmp/borabora.log"
    print(f"logging in {logfile}...")
    logf = open(logfile, "w")
    print("\n---", file=logf, flush=True)

    # Transmission de la variable globale logf aux modules
    accessoires.logf = logf
    employes.logf = logf

    # Instanciation des objets
    les_clients = Clients(fcommandes)
    le_pic = Pic(name="le_pic", verbose=False)
    le_bar = Bar(name="le_bar", verbose=False)

    # Partie 3 Extension 1 : Ajout de Charlie en second serveur
    bob = Bariste(le_pic, le_bar, les_clients, name="bob", verbose=True)
    alice = Serveur(le_pic, le_bar, les_clients, name="alice", verbose=True)
    charlie = Serveur(le_pic, le_bar, les_clients, name="charlie", verbose=True)

    # Lancement concourant de toutes les tâches
    await asyncio.gather(
        alice.run_prise_commande(),
        charlie.run_prise_commande(),
        bob.run(),
        alice.run_service(),
        charlie.run_service()
    )

    logf.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        
    asyncio.run(main_async(sys.argv[1]))