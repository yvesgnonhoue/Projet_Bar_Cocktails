import asyncio

class Employe:
    def __init__(self, pic, bar):
        self.pic = pic
        self.bar = bar
        print(f"{self.__class__.__name__} : prêt pour le service !")

class Serveur(Employe):

    async def prendre_commande(self):
        posit = await asyncio.get_event_loop().run_in_executor(None, input, "Serveur : Veuillez déposer votre commande : ")
        if posit:
            print(f"{self.__class__.__name__} : j'ai la commande {posit}")
            liste_commande = posit.split(',')
            await self.pic.embrocher(liste_commande)
            print(f"{self.__class__.__name__} : j'écris sur le post-it {liste_commande}")
            return True
        return False

    async def servir(self):
        commande = await self.bar.evacuer()
        if commande:
            print(f"{self.__class__.__name__} : j'apporte la commande : {commande}")
            for cocktail in commande:
                print(f"{self.__class__.__name__} : je sers :  {cocktail}")
            return True
        else:
            return False
    
    async def run(self):
        while await self.prendre_commande():
            pass

class Bariste(Employe):
    async def preparer(self):
        commande = await self.pic.liberer()
        if commande:
            print(f"{self.__class__.__name__} : je commence la fabrication de : {commande}")
            for cocktail in commande:
                print(f"{self.__class__.__name__} : je prépare :  {cocktail}")
            print(f"{self.__class__.__name__} : la commande : {commande} est prête.")
            await self.bar.recevoir(commande)
            return True
        else:
            return False


    async def run(self):
        while await self.preparer():
            pass