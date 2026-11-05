import sys      # Module système
import time     # Module de mesure du temps
import re       # Module d'expressions régulières
import asyncio  # Module asynchrone pour la pause coopérative (asyncio.sleep)

def usage():
    """Affiche la syntaxe d'utilisation et arrête le script en cas d'argument manquant."""
    print(f"usage: {sys.argv[0]} fichier")
    sys.exit(1)


class Clients:
    """Lit et cadence la livraison des commandes à partir du fichier texte de simulation."""
    def __init__(self, fname):
        commandes = []
        fmt = re.compile(r"(\d+)\s+(.*)")
        with open(fname, "r") as f:
            for line in f:
                found = fmt.search(line)
                if found:
                    when = int(found.group(1))
                    what = found.group(2)
                    commandes.append((when, [boisson.strip() for boisson in what.split(",")]))
        self.commandes = commandes[::-1]  # Inversion de la liste pour extraction rapide via pop()

    async def commande(self):
        """
        Coroutine asynchrone : pause coopérative (await asyncio.sleep)
        pendant le délai prévu 'when' puis renvoie la commande.
        """
        if len(self.commandes) > 0:
            when, cmd = self.commandes.pop()
            await asyncio.sleep(when)  # Pause coopérative qui cède la main à la boucle
            return cmd
        return None