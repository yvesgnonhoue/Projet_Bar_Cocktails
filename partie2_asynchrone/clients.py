import sys
import time
import re
def usage():
    print(f"usage: {sys.argv[0]} fichier")
    exit(1)

class Clients:
    def __init__(self,fname):
        commandes = []

        start = time.time()
        fmt = re.compile(r"(\d+)\s+(.*)")
        with open(fname,"r") as f:
            for line in f:
                found = fmt.search(line)
                if found:
                    when = int(found.group(1))
                    what = found.group(2)
                    commandes.append((start+when,what.split(",")))
        self.commandes = commandes[::-1]

    def commande(self):
            if len(self.commandes)>0:
              while True:
                if time.time()>self.commandes[-1][0]:
                    return self.commandes.pop()[1]
            else:
                return None
