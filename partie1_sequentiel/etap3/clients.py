import sys   # Module système : permet notamment d'accéder aux arguments de la ligne de commande (sys.argv)
import time  # Module temporel : permet de mesurer le temps qui s'écoule avec time.time()
import re    # Module d'expressions régulières : permet de découper et parser le texte du fichier de test


def usage():
    """
    Fonction de sécurité appelée si l'utilisateur lance le programme sans préciser de fichier.
    Elle affiche la syntaxe d'utilisation correcte et stoppe immédiatement le script.
    """
    print(f"usage: {sys.argv[0]} fichier")  # Affiche le nom du script
    exit(1)                                 # Arrête immédiatement l'exécution du programme avec un code d'erreur


class Clients:
    """
    Classe simulant la venue des clients et la génération progressive des commandes
    à partir d'un fichier texte (ex: lundi, mardi).
    """

    def __init__(self, fname):
        """
        Constructeur : lit et parse le fichier de commandes spécifié par fname.
        """
        commandes = []  # Liste temporaire qui va stocker toutes les commandes lues dans le fichier

        start = time.time()  # Enregistre l'horodatage précis (en secondes) du lancement de l'application
        
        # Expression régulière pour séparer le délai (chiffres) de la liste des boissons :
        # (\d+)  -> capture un ou plusieurs chiffres représentant le délai relatif en secondes.
        # \s+    -> capture l'espace séparateur entre le délai et la liste des boissons.
        # (.*)   -> capture la liste des boissons (tout le reste de la ligne après l'espace).
        fmt = re.compile(r"(\d+)\s+(.*)")

        with open(fname, "r") as f: 
            for line in f:
                found = fmt.search(line)  # Applique la regex sur la ligne courante
                if found:                 # Si la ligne correspond bien au format attendu
                    when = int(found.group(1))  # Extrait le délai relatif en secondes
                    what = found.group(2)       # Extrait la chaîne de caractères des boissons
                    
                    # Convertit le délai relatif en horodatage absolu (start + when)
                    # et transforme la chaîne de boissons en une liste Python via .split(",")
                    commandes.append((start + when, what.split(",")))

        # Inverse la liste pour optimiser l'extraction FIFO :
        # La première commande du fichier se retrouve à la fin de la liste Python,
        # ce qui permet d'utiliser pop() en temps constant O(1).
        self.commandes = commandes[::-1]

    def commande(self):
        """
        Dépile et renvoie la commande suivante si son heure de livraison est atteinte.
        Renvoie None s'il n'y a plus aucune commande à traiter dans le fichier.
        """
        if len(self.commandes) > 0:  # Vérifie s'il reste au moins une commande à distribuer
            while True:              # Boucle d'attente active jusqu'à ce que le délai soit dépassé
                # self.commandes[-1][0] est l'horodatage absolu de la prochaine commande à sortir
                if time.time() > self.commandes[-1][0]:  # Si le temps actuel dépasse l'horodatage prévu
                    return self.commandes.pop()[1]      # Dépile la commande et renvoie la liste de boissons
        else:
            return None  # Plus de commande disponible dans le fichier