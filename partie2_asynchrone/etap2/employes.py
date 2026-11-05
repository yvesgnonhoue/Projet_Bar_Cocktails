from accessoires import Logable  # Importation de la classe de base Logable depuis le module accessoires


class Employe(Logable):
    """
    Classe de base modélisant un employé du bar (Serveur ou Bariste).
    Hérite de Logable pour journaliser ses propres actions.
    """
    def __init__(self, pic, bar, clients, name, verbose=True):
        Logable.__init__(self, name, verbose)  # Initialise le nom de l'instance et le niveau de verbose
        self.pic = pic                         # Référence vers l'instance de Pic
        self.bar = bar                         # Référence vers l'instance de Bar
        self.clients = clients                 # Référence vers l'instance de Clients
        self.log("prêt pour le service")       # Journalise automatiquement le message d'initialisation


class Serveur(Employe):
    """
    Modélise le rôle du serveur (prise de commande et service en salle).
    """
    def prendre_commande(self):
        """
        Lit une commande depuis le fichier clients et l'embroche sur le pic.
        """
        self.log("prêt pour prendre une nouvelle commande...'")  # Journalise l'attente de commande
        cmd = self.clients.commande()                          # Récupère la commande suivante transmise par les clients
        if cmd is not None:
            self.log(f"j'ai la commande '{cmd}'")              # Journalise la réception de la commande
            self.log(f"j'écris sur le post-it '{cmd}'")         # Journalise l'écriture du post-it
            self.pic.embrocher(cmd)                            # Embroche le post-it sur le pic
            return True                                        # Indique que la prise de commande continue
        return False                                           # Indique qu'il n'y a plus de commandes (fin de boucle)

    def servir(self):
        """
        Récupère un plateau disponible sur le bar et le sert aux clients.
        """
        cmd = self.bar.evacuer()  # Tente de récupérer un plateau prêt sur le bar
        if cmd is not None:
            self.log(f"j'apporte la commande '{cmd}'")  # Journalise le déplacement du plateau
            for cocktail in cmd:
                self.log(f"je sers '{cocktail}'")        # Journalise le service individuel de chaque verre
            return True
        return False

    def run(self):
        """
        Boucle de travail : le serveur prend des commandes jusqu'à la fin du fichier.
        """
        while self.prendre_commande():  # Continue de boucler tant que prendre_commande() renvoie True
            pass                        # Ne fait rien à l'intérieur du corps de boucle


class Bariste(Employe):
    """
    Modélise le rôle du bariste (préparation des cocktails au bar).
    """
    def preparer(self):
        """
        Récupère un post-it du pic, fabrique les boissons et pose le plateau sur le bar.
        """
        postit = self.pic.liberer()  # Tente de dépiler le premier post-it disponible sur le pic
        if postit is not None:
            self.log(f"je commence la fabrication de '{postit}'")  # Journalise le début de la fabrication
            for cocktail in postit:
                self.log(f"je prépare '{cocktail}'")               # Journalise la confection de chaque verre
            self.log(f"la commande {postit} est prête")            # Journalise la fin de préparation
            self.bar.recevoir(postit)                              # Dépose le plateau prêt sur le bar
            return True
        return False

    def run(self):
        """
        Boucle de travail : le bariste prépare tant qu'il reste des post-it sur le pic.
        """
        while self.preparer():  # Continue de boucler tant que preparer() renvoie True
            pass                # Ne fait rien à l'intérieur du corps de boucle