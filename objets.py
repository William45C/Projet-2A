from personnage import *
from random import *
from donjon import *
from Projet_2A import *
### NE PAS OUBLIER DE SUPPRIMER LES POTIONS DE L'INVENTAIRE###

class ClassObjets:

    def pot_HP(self,personnage):
        self.shop_rate = 0.2
        self.shop_price = 10
        self.chest_rate = 0.4

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
        self.shop_rate = 0.2
        self.shop_price = 10
        self.chest_rate = 0.05

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
        self.shop_rate = 0.2
        self.shop_price = 10
        self.chest_rate = 0.4

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
        self.shop_rate = 0.2
        self.shop_price = 10
        self.chest_rate = 0.4


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
        self.shop_rate = 0.2
        self.shop_price = 10
        self.chest_rate = 0.4

        donjon.level += 1


    def pot_guarenteed_chest(self, ):

    def pot_guarenteed_mob(self, ):
    
    def pot_gold_rate_up(self, ):

