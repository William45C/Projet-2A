from personnage import *
from random import *
from donjon import *
import armes

### NE PAS OUBLIER DE SUPPRIMER LES POTIONS DE L'INVENTAIRE###

class ClassObjets:
    all_Id = []
    all_shop_rates = []
    all_shop_prices = []
    all_chest_rates = []
    all_boss_rates = []
    all_nom = []

    def __init__(self,Id,shop_rate,shop_price,chest_rate,boss_rate,nom):
        self.Id = Id
        self.shop_rate = shop_rate
        self.shop_price = shop_price
        self.chest_rate = chest_rate
        self.boss_rate = boss_rate
        self.nom = nom

        ClassObjets.all_Id.append(Id)
        ClassObjets.all_shop_rates.append(shop_rate)
        ClassObjets.all_shop_prices.append(shop_price)
        ClassObjets.all_chest_rates.append(chest_rate)
        ClassObjets.all_boss_rates.append(boss_rate)
        ClassObjets.all_nom.append(nom)

    def pot_HP(self,personnage):

        heal_value = personnage.viemax//5
        if personnage.vie == personnage.viemax :
            print("Vos HP sont déjà au maximum !")
        if personnage.viemax-personnage.vie < heal_value :
            diff_HP = personnage.viemax-personnage.vie
            personnage.vie == personnage.viemax
            ###Potion HP -1 inventaire###
            print(f"""Vos HP ont augmenté de """,diff_HP,""".
            Vos HP sont à:""", personnage.vie)
        else :
            personnage.vie += heal_value
            ###Potion HP -1 inventaire###
            print(f"""Vos HP ont augmenté de """,heal_value,""".
            Vos HP sont à:""", personnage.vie)
            
    def pot_guarenteed_up_stat(self, personnage):

        rand1 = randint(0,4) ### Permet de choisir aléatoirement l'augmentation d'une stat entre +1(80%) et +2(20%)
        augm = 1
        if rand1 == 4:
            augm = 2
        
        rand2 = randint(0,2) ### Permet de choisir aléatoirement la stat qui subit une augmentation
        if rand2 == 0:
            personnage.attack += augm
        if rand2 == 1:
            personnage.defense += augm
        else:
            personnage.agilite += augm

    def pot_random_stat1(self, personnage):

        rand1 = randint(0,1) ### Permet de choisir aléatoirement l'augmentation/diminution d'une stat entre +1(50%) et -1(50%)
        augm = 0
        if rand1 == 0:
            augm = 1
        else :
            augm = -1

        rand2 = randint(0,2) ### Permet de choisir aléatoirement la stat qui subit une augmentation/diminution
        if rand2 == 0:
            personnage.attack += augm
        if rand2 == 1:
            personnage.defense += augm
        else:
            personnage.agilite += augm
        
    def pot_random_stat2(self, personnage):

        rand1 = randint(0,4) ### Permet de choisir aléatoirement l'augmentation/diminution d'une stat entre +2(25%) et -2(75%)
        augm = 0
        if rand1 == 4:
            augm = 2
        else :
            augm = -2

        rand2 = randint(0,2) ### Permet de choisir aléatoirement la stat qui subit une augmentation/diminution
        if rand2 == 0:
            personnage.attack += augm
        if rand2 == 1:
            personnage.defense += augm
        else:
            personnage.agilite += augm
    
    def skip_level(self, donjon):

        donjon.level += 1

def chest_loot():
        Random_Prob = [] ###Créer une liste de probabilité
        for i in range(4):
            ClassObjets.all_Id.append(armes.ClassArmes.all_Id[i])
            ClassObjets.all_chest_rates.append(armes.ClassArmes.all_chest_rates[i])
        Id = ClassObjets.all_Id
        L = ClassObjets.all_chest_rates

        for i in range(len(L)):
            x=L[i]
            while x>0 :
                Random_Prob.append(Id[i])
                x-=1    ###Fin création liste proba
        shop_items = sample(Random_Prob, 1)
        item1 = Id.index(shop_items[0])
        return item1

def chest_object_name(x):
    for i in range(4):
        ClassObjets.all_nom.append(armes.ClassArmes.all_nom[i])
    noms = ClassObjets.all_nom
    answer = x
    nom1 = noms[answer]
    return nom1
"""
    def pot_guarenteed_chest(self, ):

    def pot_guarenteed_mob(self, ):
    
    def pot_gold_rate_up(self, ):
"""

potion_HP = ClassObjets(0,17,15,4,None,"Potion de soin")
potion_guarenteed_up_stat = ClassObjets(1,3,40,4,None,"Potion dorée")
potion_random_stat1 = ClassObjets(2,6,10,4,None,"Potion douteuse")
potion_random_stat2 = ClassObjets(3,6,20,4,None,"Potion très douteuse")
potion_skip_level = ClassObjets(4,3,35,4,None,"Potion d'accélération temporel")
potion_guarenteed_chest = ClassObjets(5,3,30,4,None,"Potion du coffre")
potion_guarenteed_mob = ClassObjets(6,7,20,4,None,"Potion hostile")
potion_gold_rate_up = ClassObjets(7,5,25,4,None,"Potion de fortune")
gold = ClassObjets(8,None,None,4,None,"Or x10")
mimic = ClassObjets(9,None,None,4,0,"Oh mince MIMIC DANS TA MERE")