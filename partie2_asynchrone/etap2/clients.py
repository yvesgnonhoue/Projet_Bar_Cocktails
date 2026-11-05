import sys   # Importe le module 'sys' pour interagir avec le système (ex: récupérer les arguments sys.argv)
import time  # Importe le module 'time' pour gérer les temporisations et mesurer le temps écoulé
import re    # Importe le module 're' pour traiter les expressions régulières

def usage():
    """
    Fonction de sécurité : affiche la bonne syntaxe dans le terminal
    si l'argument (nom du fichier) est omis, puis stoppe l'exécution.
    """
    print(f"usage: {sys.argv[0]} fichier")  # Affiche la syntaxe attendue (ex: usage: main.py fichier)
    exit(1)                                # Quitte immédiatement le programme avec un code d'erreur 1


class Clients:
    """
    Classe permettant de simuler l'arrivée cadencée des commandes depuis un fichier texte.
    """
    def __init__(self, fname):
        """
        Constructeur : ouvre le fichier, extrait les temporisations et calcule les horodatages.
        """
        commandes = []                      # Initialise une liste temporaire pour stocker les commandes lues
        start = time.time()                 # Enregistre le temps de départ du service en secondes
        fmt = re.compile(r"(\d+)\s+(.*)")   # Expression régulière : capture (délai en chiffres) + (espace) + (boissons)

        with open(fname, "r") as f:         # Ouvre le fichier spécifié en mode lecture de façon sécurisée
            for line in f:                  # Parcourt le fichier ligne par ligne
                found = fmt.search(line)    # Applique la Regex sur la ligne courante
                if found:
                    when = int(found.group(1))                  # Convertit le délai extrait en entier (ex: 0, 4, 2)
                    what = found.group(2)                       # Extrait la chaîne de caractères représentant les boissons.
                    commandes.append((start + when, what.split(","))) # Stocke le tuple (heure_absolue, [liste_boissons])

        self.commandes = commandes[::-1]    # Inverse la liste pour placer la première commande à la fin (pop O(1) rapide)

    def commande(self):
        """
        Renvoie la commande suivante une fois que le délai spécifié est écoulé.
        Renvoie None lorsqu'il n'y a plus aucune commande à traiter dans le fichier.
        """
        if len(self.commandes) > 0:         # Vérifie s'il reste au moins une commande dans la pile
            while True:                     # Boucle d'attente active (busy waiting)
                if time.time() > self.commandes[-1][0]: # Vérifie si le temps réel a dépassé l'heure cible
                    return self.commandes.pop()[1]      # Dépile le dernier élément et renvoie la liste des boissons
        else:
            return None                     # Renvoie None quand toutes les commandes du fichier ont été distribuées