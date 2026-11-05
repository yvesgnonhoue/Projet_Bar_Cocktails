import sys  # Importé pour la gestion des accès système
import asyncio  # Importé pour la gestion des files d'attente asynchrones (asyncio.Queue)

# Variable globale destinée à recevoir le descripteur du fichier journal ouvert dans main.py
logf = None


class Logable:
    """
    Classe de base permettant d'activer la journalisation (logs) pour une instance.
    """
    def __init__(self, name, verbose=True):
        self.name = name        # Nom personnalisé attribué à l'instance (ex: 'alice', 'bob', 'le_pic')
        self.verbose = verbose  # Booléen (True/False) activant ou masquant l'affichage des logs

    def log(self, msg):
        """
        Écrit le message identifié par le nom de l'instance dans /tmp/borabora.log si verbose est True.
        """
        if self.verbose and logf:  # Vérifie si le mode verbose est actif ET que le fichier log est ouvert
            print(f"[{self.name}] {msg}", file=logf, flush=True)  # Redirection vers logf avec vidage immédiat


class Accessoire(asyncio.Queue, Logable):
    """
    Classe de base pour les accessoires du bar (Pic et Bar).
    Hérite de asyncio.Queue (file FIFO asynchrone) et de Logable (journalisation).
    """
    def __init__(self, name, verbose=True):
        asyncio.Queue.__init__(self)           # Initialise la file d'attente asynchrone (asyncio.Queue)
        Logable.__init__(self, name, verbose) # Initialise la partie journalisation (Logable)


class Pic(Accessoire):
    """
    Un pic contient les commandes (post-it) à fabriquer.
    """
    async def embrocher(self, postit):
        """
        Le serveur embroche un post-it sur le pic de manière asynchrone et enregistre l'action.
        """
        await self.put(postit)  # Ajoute le post-it dans la file asynchrone
        if postit is not None:  # Ne logue pas le signal de fin de service (None)
            self.log(f"post-it '{postit}' embroché, {self.qsize()} post-it(s) à traiter")  # Trace l'ajout

    async def liberer(self):
        """
        Le bariste récupère le premier post-it disponible dans la file asynchrone.
        """
        postit = await self.get()  # Récupère de manière non-bloquante le premier post-it
        if postit is not None:     # Ne logue pas le signal de fin de service (None)
            self.log(f"post-it '{postit}' libéré, {self.qsize()} post-it(s) à traiter")  # Trace le retrait
        return postit              # Renvoie le post-it au bariste (ou None pour arrêter la boucle)


class Bar(Accessoire):
    """
    Un bar reçoit les consommations préparées par le bariste.
    """
    async def recevoir(self, commande):
        """
        Le bariste dépose un plateau de boissons prêtes sur le bar et enregistre l'action.
        """
        await self.put(commande)  # Ajoute le plateau dans la file asynchrone
        if commande is not None:  # Ne logue pas le signal de fin de service (None)
            self.log(f"'{commande}' posée, {self.qsize()} commande(s) à servir")  # Trace le dépôt

    async def evacuer(self):
        """
        Le serveur récupère le premier plateau prêt sur le bar de manière asynchrone.
        """
        commande = await self.get()  # Récupère de manière non-bloquante le premier plateau
        if commande is not None:     # Ne logue pas le signal de fin de service (None)
            self.log(f"'{commande}' évacuée, {self.qsize()} commande(s) à servir")  # Trace le retrait
        return commande              # Renvoie le plateau au serveur (ou None pour arrêter le service)