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

    def __init__(self,Id=None,shop_rate=None,shop_price=None,chest_rate=0,boss_rate=None,nom=None):
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

    def GetEffect(self, potion, perso, donjon, current_state):
        effect = {
            "Potion de soin": lambda: self.pot_HP(perso),
            "Potion dorée": lambda: self.pot_guarenteed_up_stat(perso),
            "Potion douteuse": lambda: self.pot_random_stat1(perso),
            "Potion très douteuse": lambda: self.pot_random_stat2(perso),
            "Potion d'accélération temporel": lambda: self.skip_level(donjon),
            "Potion du coffre": lambda: self.guarenteed_chest(current_state, donjon),
            "Potion hostile": lambda: self.guarenteed_mob(current_state, donjon),
        }
        return effect[potion]()

    def pot_HP(self,personnage):
        heal_value = personnage.viemax//5
        print(f"soin de {heal_value}")
        if personnage.vie == personnage.viemax :
            print("Vos HP sont déjà au maximum !")
        if personnage.viemax-personnage.vie < heal_value :
            diff_HP = personnage.viemax-personnage.vie
            personnage.vie = personnage.viemax
            ###Potion HP -1 inventaire###
            print(f"Vos HP ont augmenté de ",diff_HP,".\nVos HP sont à:", personnage.vie)
        else :
            personnage.vie += heal_value
            ###Potion HP -1 inventaire###
            print(f"Vos HP ont augmenté de ",heal_value,".\nVos HP sont à:", personnage.vie)

    
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
            if personnage.attack - augm < 1:
                personnage.attack = 1
            else:
                personnage.attack += augm
        if rand2 == 1:
            if personnage.defense - augm < 1:
                personnage.defense = 1
            else:    
                personnage.defense += augm
        else:
            if personnage.agilite - augm < 1:
                personnage.agilite = 1
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
            if personnage.attack - augm < 1:
                personnage.attack = 1
            else:
                personnage.attack += augm
        if rand2 == 1:
            if personnage.defense - augm < 1:
                personnage.defense = 1
            else:
                personnage.defense += augm
        else:
            if personnage.agilite - augm < 1:
                personnage.agilite = 1
            else:
                personnage.agilite += augm
    
    def skip_level(self, donjon):
        donjon.level += 1
        pass

    def guarenteed_chest(self, current_state, donjon):
        print("Vous avez utilisé une potion du coffre !\nLe coffre de la prochaine salle est garanti !")
        donjon.level += 1
        return "CHEST"

    def guarenteed_mob(self, current_state, donjon):
        print("Vous avez utilisé une potion hostile !\nLe prochain mob que vous rencontrerez est garanti !")
        donjon.level += 1
        return "COMBAT"

def chest_loot():
    ids = (ClassObjets.all_Id + armes.ClassArmes.all_Id)[:14]
    rates = (ClassObjets.all_chest_rates + armes.ClassArmes.all_chest_rates)[:14]

    # Weighted random choice
    print(ids)
    total = sum(rates)
    r = randint(1, total)

    cumulative = 0
    for i in range(len(ids)):
        cumulative += rates[i]
        if r <= cumulative:
            return ids[i]

def chest_object_name(x):
    noms = (ClassObjets.all_nom + armes.ClassArmes.all_nom)[:14]
    answer = x
    nom1 = noms[answer]
    return nom1


#nom_obj = ClassObjets(Id, shop_rate, shop_price, chest_rate, boss_rate, "nom")
potion_HP = ClassObjets(0,17,15,8,None,"Potion de soin")
potion_guarenteed_up_stat = ClassObjets(1,3,40,8,None,"Potion dorée")
potion_random_stat1 = ClassObjets(2,6,10,8,None,"Potion douteuse")
potion_random_stat2 = ClassObjets(3,6,20,8,None,"Potion très douteuse")
potion_skip_level = ClassObjets(4,3,35,8,None,"Potion d'accélération temporel")
potion_guarenteed_chest = ClassObjets(5,3,30,8,None,"Potion du coffre")
potion_guarenteed_mob = ClassObjets(6,7,20,8,None,"Potion hostile")
potion_gold_rate_up = ClassObjets(7,5,25,8,None,"Potion de fortune")
gold = ClassObjets(8,None,None,8,None,"Or x10")
mimic = ClassObjets(9,None,None,8,0,"Oh mince MIMIC DANS TA MERE")



