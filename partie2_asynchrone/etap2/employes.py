import asyncio  # Importé pour la gestion des opérations asynchrones
import accessoires  # Importé pour accéder à la variable globale logf
from accessoires import Logable  # Importation propre de Logable sans parenthèse parasite


class Employe(Logable):
    """Classe de base modélisant un employé du bar (Serveur ou Bariste).

    Hérite de Logable pour journaliser ses propres actions.
    """

    def __init__(self, pic, bar, clients, name, verbose=True):
        Logable.__init__(
            self, name, verbose
        )  # Initialise le nom de l'instance et le niveau de verbose
        self.pic = pic  # Référence vers l'instance de Pic
        self.bar = bar  # Référence vers l'instance de Bar
        self.clients = clients  # Référence vers l'instance de Clients
        self.log(
            "prêt pour le service"
        )  # Journalise automatiquement le message d'initialisation


class Serveur(Employe):
    """Modélise le rôle du serveur (prise de commande et service en salle)."""

    async def prendre_commande(self):
        """Prend une commande depuis l'instance clients et l'embroche sur le pic de manière asynchrone."""
        self.log(
            "prêt pour prendre une nouvelle commande...'"
        )  # Journalise l'attente de commande
        cmd = (
            self.clients.commande()
        )  # Récupère la commande suivante depuis clients (synchrone à l'Étape 2)
        if cmd is not None:
            self.log(
                f"j'ai la commande '{cmd}'"
            )  # Journalise la réception de la commande
            self.log(
                f"j'écris sur le post-it '{cmd}'"
            )  # Journalise l'écriture du post-it
            await (
                self.pic.embrocher(cmd)
            )  # Embroche le post-it sur le pic de manière asynchrone (asyncio.Queue)
            return True  # Indique que la prise de commande continue
        else:
            await self.pic.embrocher(
                None
            )  # Transmet le signal de fin (None) au bariste
            return False  # Indique la fin de la prise de commande

    async def servir(self):
        """Récupère un plateau disponible sur le bar et le sert aux clients de manière asynchrone."""
        cmd = (
            await self.bar.evacuer()
        )  # Tente de récupérer un plateau prêt sur le bar de manière asynchrone
        if cmd is not None:
            self.log(
                f"j'apporte la commande '{cmd}'"
            )  # Journalise le déplacement du plateau
            for cocktail in cmd:
                self.log(
                    f"je sers '{cocktail}'"
                )  # Journalise le service individuel de chaque verre
            return True
        return False

    async def run_prise_commande(self):
        """Boucle asynchrone de prise de commande."""
        while (
            await self.prendre_commande()
        ):  # Continue tant que prendre_commande() renvoie True
            pass

    async def run_service(self):
        """Boucle asynchrone de service des consommations."""
        while await self.servir():  # Continue tant que servir() renvoie True
            pass


class Bariste(Employe):
    """Modélise le rôle du bariste (préparation des cocktails au bar)."""

    async def preparer(self):
        """Récupère un post-it du pic, fabrique les boissons et dépose le plateau sur le bar de manière asynchrone."""
        postit = (
            await self.pic.liberer()
        )  # Tente de dépiler le premier post-it disponible de manière asynchrone
        if postit is not None:
            self.log(
                f"je commence la fabrication de '{postit}'"
            )  # Journalise le début de la fabrication
            for cocktail in postit:
                self.log(
                    f"je prépare '{cocktail}'"
                )  # Journalise la confection de chaque verre
            self.log(
                f"la commande {postit} est prête"
            )  # Journalise la fin de préparation
            await (
                self.bar.recevoir(postit)
            )  # Dépose le plateau prêt sur le bar de manière asynchrone
            return True
        else:
            await (
                self.bar.recevoir(None)
            )  # Transmet le signal de fin (None) sur le bar
            return False

    async def run(self):
        """Boucle asynchrone de travail du bariste."""
        while await self.preparer():  # Continue de boucler tant que preparer() renvoie True
            pass