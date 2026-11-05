import asyncio  # Importé pour la gestion des pauses (asyncio.sleep) et des verrous (asyncio.Lock)
import accessoires  # Importé pour accéder à la variable globale logf
from accessoires import Logable  # Importation de la classe de base Logable


class Employe(Logable):
    """
    Classe de base modélisant un employé du bar (Serveur ou Bariste).
    Hérite de Logable pour journaliser ses propres actions.
    """
    def __init__(self, pic, bar, clients, name, verbose=True):
        Logable.__init__(self, name, verbose)  # Initialise la partie Logable avec name et verbose
        self.pic = pic                         # Référence vers l'instance de Pic
        self.bar = bar                         # Référence vers l'instance de Bar
        self.clients = clients                 # Référence vers l'instance de Clients
        self.log("prêt pour le service")       # Journalise automatiquement l'initialisation


class Serveur(Employe):
    """
    Modélise le rôle du serveur (prise de commande et service en salle).
    Intègre un verrou asyncio.Lock pour empêcher le zappage entre tâches.
    """
    def __init__(self, pic, bar, clients, name, verbose=True):
        super().__init__(pic, bar, clients, name, verbose)
        self.lock = asyncio.Lock()  # Verrou d'exclusivité pour le serveur

    async def prendre_commande(self):
        """
        Prend une commande de façon asynchrone depuis les clients.
        """
        self.log("prêt pour prendre une nouvelle commande...'")
        cmd = await self.clients.commande()  # Attente passive de la commande (hors verrou pour ne pas bloquer inutilement)
        
        if cmd is not None:
            # 👈 On protège uniquement la phase active d'écriture et d'embrochage
            async with self.lock:
                self.log(f"j'ai la commande '{cmd}'")
                self.log(f"j'écris sur le post-it '{cmd}'")
                await self.pic.embrocher(cmd)  # Embrochement asynchrone sur le pic
                await asyncio.sleep(0.1)        # Pause coopérative simulant l'écriture
            return True
        else:
            async with self.lock:
                await self.pic.embrocher(None)  # Transmission du signal de fin au Bariste
            return False

    async def servir(self):
        """
        Récupère un plateau disponible et sert l'intégralité des cocktails de manière atomique.
        """
        # Récupération du plateau sur le bar
        cmd = await self.bar.evacuer()  # Évacuation asynchrone depuis le bar
        
        if cmd is not None:
            # Le verrou protège tout le service du plateau pour interdire le "zapping"
            async with self.lock:
                self.log(f"j'apporte la commande '{cmd}'")
                for cocktail in cmd:
                    self.log(f"je sers '{cocktail}'")
                    await asyncio.sleep(0.1)  # Pause coopérative pendant le service de chaque verre
            return True
        return False  # Si la commande vaut None, arrête la boucle de service

    async def run_prise_commande(self):
        """
        Boucle asynchrone de prise de commande.
        """
        while await self.prendre_commande():
            pass

    async def run_service(self):
        """
        Boucle asynchrone de service des plateaux prêts.
        """
        while await self.servir():  # S'arrête proprement dès que servir() renvoie False
            pass


class Bariste(Employe):
    """
    Modélise le rôle du bariste (préparation des cocktails au bar).
    """
    async def preparer(self):
        """
        Libère un post-it du pic, prépare les boissons et dépose le plateau sur le bar.
        """
        postit = await self.pic.liberer()  # Libération asynchrone depuis le pic
        if postit is not None:
            self.log(f"je commence la fabrication de '{postit}'")
            for cocktail in postit:
                self.log(f"je prépare '{cocktail}'")
                await asyncio.sleep(0.2)  # Suspension coopérative pendant la confection de chaque cocktail
            self.log(f"la commande {postit} est prête")
            await self.bar.recevoir(postit)  # Dépôt asynchrone du plateau sur le bar
            return True
        else:
            await self.bar.recevoir(None)  # Transmission du signal de fin au Serveur
            return False

    async def run(self):
        """
        Boucle asynchrone de préparation des boissons.
        """
        while await self.preparer():
            pass