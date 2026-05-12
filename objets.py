from personnage import *
from random import *
from donjon import *
import armes

class ClassObjets: ##Definit la classes de objets
    all_Id = [] ##Permet d'identifier de manière unique les objets
    all_shop_rates = [] ##Taux d'apparition des objets dans les shops
    all_shop_prices = [] ##Prix des objets dans les shops
    all_chest_rates = [] ##Taux d'apparition des objets dans les coffres
    all_boss_rates = [] ##Taux d'apparition des objets sur les boss
    all_nom = [] ##Nom des objets

    def __init__(self,Id=None,shop_rate=None,shop_price=None,chest_rate=0,boss_rate=None,nom=None):
        self.Id = Id
        self.shop_rate = shop_rate
        self.shop_price = shop_price
        self.chest_rate = chest_rate
        self.boss_rate = boss_rate
        self.nom = nom

        ClassObjets.all_Id.append(Id) ##Créer des listes de tous les Id, shop_rate, shop_price, chest_rate, boss_rate et nom de tous les objets créés pour pouvoir les utiliser dans les fonctions de loot des coffres et des shops.
        ClassObjets.all_shop_rates.append(shop_rate)
        ClassObjets.all_shop_prices.append(shop_price)
        ClassObjets.all_chest_rates.append(chest_rate)
        ClassObjets.all_boss_rates.append(boss_rate)
        ClassObjets.all_nom.append(nom)

    def GetEffect(self, potion, perso, donjon, current_state, inCombatBoss): ##Permet d'obtenir l'effet d'une potion en fonction de son nom
        effect = {
            "Potion de soin": lambda: self.pot_HP(perso),
            "Potion dorée": lambda: self.pot_guarenteed_up_stat(perso),
            "Potion douteuse": lambda: self.pot_random_stat1(perso),
            "Potion très douteuse": lambda: self.pot_random_stat2(perso),
            "Potion d'accélération temporel": lambda: self.skip_level(inCombatBoss, donjon),
            "Potion du coffre": lambda: self.guarenteed_chest(inCombatBoss, donjon),
            "Potion hostile": lambda: self.guarenteed_mob(inCombatBoss, donjon),
            "Potion de fortune": lambda: self.pot_gold_rate_up(perso)
        }
        return effect[potion]()

    def pot_HP(self,personnage): ##Effet de la potion de soin
        heal_value = personnage.viemax//5
        print(f"soin de {heal_value}")
        if personnage.vie == personnage.viemax : ###Si les HP du personnage sont déjà au maximum, la potion ne fait rien
            print("Vos HP sont déjà au maximum !")
        if personnage.viemax-personnage.vie < heal_value : ###Si les HP du personnage sont à moins de 20% de leur maximum, la potion ne soigne que la différence entre les HP actuels et les HP max, pour éviter de dépasser les HP max.
            diff_HP = personnage.viemax-personnage.vie
            personnage.vie = personnage.viemax
            ###Potion HP -1 inventaire###
            print(f"Vos HP ont augmenté de ",diff_HP,".\nVos HP sont à:", personnage.vie)
        else :
            personnage.vie += heal_value ###Sinon, la potion soigne 20% des HP max du personnage.
            ###Potion HP -1 inventaire###
            print(f"Vos HP ont augmenté de ",heal_value,".\nVos HP sont à:", personnage.vie)

    
    def pot_guarenteed_up_stat(self, personnage): ##Effet de la potion dorée

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

    def pot_random_stat1(self, personnage): ##Effet de la potion douteuse

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

    def pot_random_stat2(self, personnage): ##Effet de la potion très douteuse

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
    
    def skip_level(self, inCombatBoss, donjon): ##Effet de la potion d'accélération temporel
        if inCombatBoss: ##Empeche d'utiliser la potion pour éviter un niveau de boss, car cela rendrait le jeu trop facile et déséquilibré.
            print("Vous ne pouvez pas utiliser cette potion avant un niveau de boss !")
            return "COMBATBOSS"
        else:
            donjon.level += 1 ##Permet de passer directement au niveau supérieur du donjon.
        pass

    def guarenteed_chest(self, inCombatBoss, donjon): ##Effet de la potion du coffre
        if inCombatBoss: ##Empeche d'utiliser la potion pour éviter un niveau de boss, car cela rendrait le jeu trop facile et déséquilibré.
            print("Vous ne pouvez pas utiliser cette potion avant un niveau de boss !")
            return "COMBATBOSS"
        else:
            print("Vous avez utilisé une potion du coffre !\nLe coffre de la prochaine salle est garanti !")
            donjon.level += 1
        return "CHEST" ##Permet de garantir que le prochain événement sera un coffre

    def guarenteed_mob(self, inCombatBoss, donjon): ##Effet de la potion hostile
        if inCombatBoss: ##Empeche d'utiliser la potion pour éviter un niveau de boss, car cela rendrait le jeu trop facile et déséquilibré.
            print("Vous ne pouvez pas utiliser cette potion avant un niveau de boss !")
            return "COMBATBOSS"
        else:
            print("Vous avez utilisé une potion hostile !\nLe prochain mob que vous rencontrerez est garanti !")
            donjon.level += 1
        return "COMBAT" ##Permet de garantir que le prochain événement sera un combat contre un mob
    
    def pot_gold_rate_up(self, personnage): ##Effet de la potion de fortune
        if personnage.Or == 0: ##Si le personnage n'a pas d'or, la potion ne fait rien, car elle ne peut pas augmenter les chances d'obtenir de l'or dans les coffres.
            print("Vous n'avez pas d'or ! Cette potion ne peut pas être utilisée !")
        else:
            print("Vous avez utilisé une potion de fortune !\nVos chances d'obtenir de l'or dans les coffres ont augmenté de 20% pour les 5 prochains niveaux !")
            personnage.Or *= 1.2 ##Permet de multiplier l'or du personnage par 1.2.

def chest_loot(): ###Permet de déterminer de manière aléatoire quel objet le personnage obtient lorsqu'il ouvre un coffre, en fonction des taux d'apparition des objets dans les coffres.
    ids = (ClassObjets.all_Id + armes.ClassArmes.all_Id)[:14]
    rates = (ClassObjets.all_chest_rates + armes.ClassArmes.all_chest_rates)[:14]

    # Weighted random choice
    print(ids)
    total = sum(rates)
    r = randint(1, total)

    cumulative = 0
    for i in range(len(ids)): ##Parcourt la liste des objets et de leurs taux d'apparition pour déterminer quel objet est obtenu en fonction d'un nombre aléatoire compris entre 1 et la somme de tous les taux d'apparition.
        cumulative += rates[i]
        if r <= cumulative:
            return ids[i]

def chest_object_name(x): ###Permet d'obtenir le nom de l'objet obtenu dans un coffre à partir de son Id, en utilisant la liste de tous les noms d'objets créée dans la classe ClassObjets.
    noms = (ClassObjets.all_nom + armes.ClassArmes.all_nom)[:14]
    answer = x
    nom1 = noms[answer]
    return nom1


#nom_obj = ClassObjets(Id, shop_rate, shop_price, chest_rate, boss_rate, "nom")
potion_HP = ClassObjets(0,17,15,8,None,"Potion de soin") ##Potion de soin : soigne 20% des HP max du personnage, ne peut pas dépasser les HP max.
potion_guarenteed_up_stat = ClassObjets(1,3,40,8,None,"Potion dorée") ##Potion dorée : augmente aléatoirement une stat (attaque, défense ou agilité) de +1(80%) ou +2(20%).
potion_random_stat1 = ClassObjets(2,6,10,8,None,"Potion douteuse") ##Potion douteuse : augmente ou diminue aléatoirement une stat (attaque, défense ou agilité) de +1(50%) ou -1(50%), mais ne peut pas faire descendre une stat en dessous de 1.
potion_random_stat2 = ClassObjets(3,6,20,8,None,"Potion très douteuse") ##Potion très douteuse : augmente ou diminue aléatoirement une stat (attaque, défense ou agilité) de +2(25%) ou -2(75%), mais ne peut pas faire descendre une stat en dessous de 1.
potion_skip_level = ClassObjets(4,3,35,8,None,"Potion d'accélération temporel") ##Potion d'accélération temporel : permet de passer directement au niveau supérieur du donjon, mais ne peut pas être utilisée à un niveau de boss.
potion_guarenteed_chest = ClassObjets(5,3,30,8,None,"Potion du coffre") ##Potion du coffre : garantit que le coffre de la prochaine salle contiendra un objet, mais ne garantit pas le type d'objet (peut être une arme ou un objet). Ne peut pas être utilisé à un niveau de boss.
potion_guarenteed_mob = ClassObjets(6,7,20,8,None,"Potion hostile") ##Potion hostile : garantit que le prochain mob que vous rencontrerez sera un mob. Ne peut pas être utilisé à un niveau de boss.
potion_gold_rate_up = ClassObjets(7,5,25,8,None,"Potion de fortune") ##Potion de fortune : multiplie par 1.2 l'or du personnage
gold = ClassObjets(8,None,None,8,None,"Or x10") ##Or x10 : ajoute 10 pièces d'or à l'inventaire du personnage.
mimic = ClassObjets(9,None,None,8,0,"Oh mince, une mimique !") ##Mimique : un coffre piégé qui inflige des dégâts au personnage lorsqu'il est ouvert.



