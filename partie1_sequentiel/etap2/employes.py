class Employe:
    """
    Classe de base modélisant un employé (Bariste ou Serveur).
    """
    def __init__(self, pic, bar, clients=None):
        self.pic = pic
        self.bar = bar
        self.clients = clients
        # Affiche automatiquement le nom de la sous-classe ("Bariste" ou "Serveur")
        print(f"{self.__class__.__name__}: prêt pour le service")


class Serveur(Employe):
    def prendre_commande(self):
        """Prend une commande lue depuis le fichier via la classe Clients."""
        print(f"{self.__class__.__name__} : Prêt pour nouvelle commande ...'")
        posit = self.clients.commande()
        if posit:
            print(f"{self.__class__.__name__} : j'ai la commande {posit}")
            liste_commande = [boisson.strip() for boisson in posit]
            self.pic.embrocher(liste_commande)
            print(f"{self.__class__.__name__} : j'écris sur le post-it {liste_commande}")
            return True
        return False

    def servir(self):
        """Prend un plateau disponible sur le bar et le sert au client."""
        commande = self.bar.evacuer()
        if commande:
            print(f"{self.__class__.__name__} : j'apporte la commande : {commande}")
            for cocktail in commande:
                print(f"{self.__class__.__name__} : je sers : {cocktail}")
            return True
        return False

    def run(self):
        """Le serveur prend toutes les commandes jusqu'à ce que le fichier soit vide."""
        while self.prendre_commande():
            pass


class Bariste(Employe):
    def preparer(self):
        """Dépile un post-it du pic, fabrique les boissons et dépose le plateau sur le bar."""
        commande = self.pic.liberer()
        if commande:
            print(f"{self.__class__.__name__} : je commence la fabrication de : {commande}")
            for cocktail in commande:
                print(f"{self.__class__.__name__} : je prépare : {cocktail}")
            print(f"{self.__class__.__name__} : la commande : {commande} est prête.")
            self.bar.recevoir(commande)
            return True
        return False

    def run(self):
        """Le bariste prépare tant qu'il y a des post-it sur le pic."""
        while self.preparer():
            pass