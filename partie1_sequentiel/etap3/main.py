import sys
import accessoires
import employes
from accessoires import Pic, Bar
from employes import Bariste, Serveur
from clients import Clients, usage

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        
    fcommandes = sys.argv[1]

    # 1. Ouverture du fichier de log
    logfile = "/tmp/borabora.log"
    print(f"logging in {logfile}...")
    logf = open(logfile, "w")
    
    # 2. Partage du descripteur de fichier avec les modules accessoires et employes
    accessoires.logf = logf
    employes.logf = logf

    # 3. Chargement des clients depuis le fichier (ex: lundi.txt)
    les_clients = Clients(fcommandes)

    # 4. Instanciation des accessoires et des employés
    le_pic = Pic(name="le_pic", verbose=False)
    le_bar = Bar(name="le_bar", verbose=False)
    
    # 👇 C'est ici qu'on active verbose=True pour Bob pour voir ses traces !
    bob = Bariste(le_pic, le_bar, les_clients, name="bob", verbose=True)
    alice = Serveur(le_pic, le_bar, les_clients, name="alice", verbose=False)

    # 5. Déroulement séquentiel du service
    alice.run()
    bob.run()
    while len(le_bar) > 0:
        alice.servir()

    logf.close()