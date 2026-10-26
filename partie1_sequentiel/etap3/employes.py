from accessoires import Logable

class Employe(Logable):
    """Classe de base modélisant un employé."""
    def __init__(self, pic, bar, clients, name, verbose=True):
        Logable.__init__(self, name, verbose)
        self.pic = pic
        self.bar = bar
        self.clients = clients
        self.log("prêt pour le service")


class Serveur(Employe):
    def prendre_commande(self):
        self.log("prêt pour prendre une nouvelle commande...'")
        liste_commande = self.clients.commande()
        if liste_commande :
            self.log(f"j'ai la commande '{liste_commande}'")
            self.log(f"j'écris sur le post-it '{liste_commande}'")
            self.pic.embrocher(liste_commande)
            return True
        return False

    def servir(self):
        cmd = self.bar.evacuer()
        if cmd is not None:
            self.log(f"j'apporte la commande '{cmd}'")
            for cocktail in cmd:
                self.log(f"je sers '{cocktail}'")
            return True
        return False

    def run(self):
        while self.prendre_commande():
            pass


class Bariste(Employe):
    def preparer(self):
        postit = self.pic.liberer()
        if postit is not None:
            self.log(f"je commence la fabrication de '{postit}'")
            for cocktail in postit:
                self.log(f"je prépare '{cocktail}'")
            self.log(f"la commande {postit} est prête")
            self.bar.recevoir(postit)
            return True
        return False

    def run(self):
        while self.preparer():
            pass