import sys        # Module d'interaction système (sys.argv)
import re         # Module d'expressions régulières pour parser le fichier de simulation
import asyncio    # Module asynchrone pour la suspension coopérative (asyncio.sleep)

def usage():
    """Affiche la syntaxe d'utilisation et arrête le script en cas d'argument manquant."""
    print(f"usage: {sys.argv[0]} fichier")
    sys.exit(1)


class Clients:
    """
    Lit et cadence la livraison des commandes à partir du fichier texte de simulation.
    """
    def __init__(self, fname):
        commandes = []
        fmt = re.compile(r"(\d+)\s+(.*)")
        with open(fname, "r") as f:
            for line in f:
                found = fmt.search(line)
                if found:
                    when = int(found.group(1))
                    what = found.group(2)
                    # Enregistre le délai d'attente relatif 'when' et la liste des boissons
                    commandes.append((when, [boisson.strip() for boisson in what.split(",")]))
        self.commandes = commandes[::-1] # Inverse la liste pour dépiler en O(1) avec pop()

    async def commande(self):
        """
        Coroutine asynchrone : effectue une pause coopérative (await asyncio.sleep)
        pendant le délai 'when' avant de délivrer la commande suivante.
        """
        if len(self.commandes) > 0:
            when, cmd = self.commandes.pop()
            await asyncio.sleep(when)  # 👈 Suspension coopérative qui cède la main à l'Event Loop
            return cmd
        return None