import sys

# Variable globale pour stocker le fichier de log
logf = None

class Logable:
    """Classe de base pour disposer d'une méthode log."""
    def __init__(self, name, verbose=True):
        self.name = name
        self.verbose = verbose

    def log(self, msg):
        if self.verbose and logf:
            print(f"[{self.name}] {msg}", file=logf, flush=True)


class Accessoire(list, Logable):
    """Classe de base pour les accessoires du bar, héritant de list et de Logable."""
    def __init__(self, name, verbose=True):
        list.__init__(self)
        Logable.__init__(self, name, verbose)


class Pic(Accessoire):
    """Contient les post-it des commandes à fabriquer."""
    def embrocher(self, postit):
        self.append(postit)
        self.log(f"post-it '{postit}' embroché, {len(self)} post-it(s) à traiter")

    def liberer(self):
        if self:
            postit = self.pop(0)
            self.log(f"post-it '{postit}' libéré, {len(self)} post-it(s) à traiter")
            return postit
        return None


class Bar(Accessoire):
    """Contient les consommations préparées prêtes à être servies."""
    def recevoir(self, commande):
        self.append(commande)
        self.log(f"'{commande}' posée, {len(self)} commande(s) à servir")

    def evacuer(self):
        if self:
            commande = self.pop(0)
            self.log(f"'{commande}' évacuée, {len(self)} commande(s) à servir")
            return commande
        return None