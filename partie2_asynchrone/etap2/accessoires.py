import sys  # Importé pour la cohérence des accès système

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
        if self.verbose and logf:  # Vérifie si le mode verbose est actif ET que le fichier log est bien ouvert
            print(f"[{self.name}] {msg}", file=logf, flush=True)  # Redirige le texte vers logf avec vidage immédiat


class Accessoire(list, Logable):
    """
    Classe de base pour les accessoires du bar (Pic et Bar).
    Hérite de list (structure FIFO) et de Logable (journalisation).
    """
    def __init__(self, name, verbose=True):
        list.__init__(self)                   # Initialise la partie structure de données (list)
        Logable.__init__(self, name, verbose) # Initialise la partie journalisation (Logable)


class Pic(Accessoire):
    """
    Un pic contient les commandes (post-it) à fabriquer.
    """
    def embrocher(self, postit):
        """
        Le serveur embroche un post-it sur le pic et enregistre l'action dans le log.
        """
        self.append(postit)  # Ajoute le post-it à la fin de la liste (file FIFO)
        self.log(f"post-it '{postit}' embroché, {len(self)} post-it(s) à traiter")  # Trace l'ajout dans le journal

    def liberer(self):
        """
        Le bariste récupère le premier post-it disponible et enregistre l'action dans le log.
        """
        if self:  # Vérifie si la liste n'est pas vide (équivalent à len(self) > 0)
            postit = self.pop(0)  # Retire et récupère le tout premier post-it entré (index 0, stratégie FIFO)
            self.log(f"post-it '{postit}' libéré, {len(self)} post-it(s) à traiter")  # Trace le retrait
            return postit         # Renvoie le post-it au bariste
        return None               # Renvoie None si le pic est vide


class Bar(Accessoire):
    """
    Un bar reçoit les consommations préparées par le bariste.
    """
    def recevoir(self, commande):
        """
        Le bariste dépose un plateau de boissons prêtes sur le bar et enregistre l'action.
        """
        self.append(commande)  # Ajoute le plateau de boissons à la fin de la liste du bar
        self.log(f"'{commande}' posée, {len(self)} commande(s) à servir")  # Trace le dépôt dans le journal

    def evacuer(self):
        """
        Le serveur récupère le premier plateau prêt sur le bar et enregistre l'action.
        """
        if self:  # Vérifie si la liste n'est pas vide
            commande = self.pop(0)  # Retire et récupère le premier plateau disponible (index 0, stratégie FIFO)
            self.log(f"'{commande}' évacuée, {len(self)} commande(s) à servir")  # Trace le retrait
            return commande         # Renvoie le plateau au serveur
        return None                 # Renvoie None si le bar est vide