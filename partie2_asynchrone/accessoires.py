import asyncio

class Accessoires(asyncio.Queue):
    """Liste contenant l'ensemble des tickets/commandes déposés puis retirés un par un."""
    pass

class Pic(Accessoires):

    """ Ajout des tickets/commandes sur le pic par le serveur. """
    async def embrocher(self, postit):
            await self.put(postit)

    """ Le bariste retire les tickets/commandes un par un, dans l'ordre de dépôt."""
    async def liberer(self):
            return await self.get()

class Bar(Accessoires):

    """ Le bariste dépose les commandes sur le bar. """
    async def recevoir(self, commande):
        await self.put(commande)

    """ Le serveur retire les commandes usur le bar."""
    async def evacuer(self): 
        return await self.get()

