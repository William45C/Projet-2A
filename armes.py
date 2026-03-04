from personnage import *
from random import *
from donjon import *

class ClassArmes: 
    all_Id = []
    all_boss_rates = []
    all_chest_rates = []
    all_nom = []

    def __init__(self, Id, shop_rate, shop_price, chest_rate, boss_rate, nom, affectation_personnage=None,donjon=None):
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

#nom = ClassArmes(id,shop_rate,shop_price,chest_rate,boss_rate,nom)
