from random import *
from donjon import *

class ClassArmes: 
    all_Id = []
    all_boss_rates = []
    all_chest_rates = []
    all_nom = []

    def __init__(self, Id, shop_rate, shop_price, chest_rate=0, boss_rate=None, nom=None, affectation_personnage=None,donjon=None):
        self.Id = Id
        self.boss_rate = boss_rate
        self.chest_rate = chest_rate
        self.nom = nom
        if donjon!=None:
            self.mod = affectation_personnage*donjon.level*0.1

        ClassArmes.all_Id.append(Id)
        ClassArmes.all_boss_rates.append(boss_rate)
        ClassArmes.all_chest_rates.append(chest_rate)
        ClassArmes.all_nom.append(nom)
    
    def choix_darme(self, arme, personnage, donjon):
        choix = input("Voulez-vous changer d'arme ?")
        if choix == "oui":
            personnage.arme = arme
            self.stats_armes = self.statsArmes(donjon)[self.arme].mod
            print(f"Vous avez équipé : " + arme)
        elif choix == "non":
            print(f"Très bien, votre arme ne change donc pas.")
        else:
            print(f"Veuillez entrer 'oui' ou 'non'")

ClassArmes(10,0,0,6,25,"Epee"),
ClassArmes(11,0,0,6,10,"Rapiere"),
ClassArmes(12,0,0,7,14,"Shield"),
ClassArmes(13,0,0,1,1,"Poing duriche")
#nom = ClassArmes(id,shop_rate,shop_price,chest_rate,boss_rate,nom)

