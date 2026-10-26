class Accessoire(list):
    """Classe de base pour les accessoires du bar (Pic, Bar)."""
    pass


class Pic(Accessoire):
    """
    Un pic contient les commandes (post-it) à fabriquer.
    """
    def embrocher(self, postit):
        """Le serveur écrit et embroche un post-it sur le pic."""
        if postit:  # Vérifie si le post-it à embrocher n'est pas vide
            self.append(postit)
            return True
        return False

    def liberer(self):
        """Le bariste récupère le premier post-it disponible (FIFO)."""
        if self:  # Vérifie si la liste n'est pas vide avant de dépiler
            return self.pop(0)  # FIFO : premier entré, premier sorti
        return None


class Bar(Accessoire):
    """
    Un bar reçoit les consommations préparées par le bariste.
    """
    def recevoir(self, commande):
        """Le bariste dépose un plateau de boissons prêtes sur le bar."""
        if commande:  # Vérifie si le plateau à poser n'est pas vide
            self.append(commande)
            return True
        return None

    def evacuer(self):
        """Le serveur prend le premier plateau prêt sur le bar pour le servir."""
        if self:  # Vérifie si la liste n'est pas vide avant d'évacuer
            return self.pop(0)  # FIFO : premier entré, premier sorti
        return None