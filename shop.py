from personnage import *
from objets import *
from random import *

def shop_item_selection():
    Random_Prob = [] ###Créer une liste de probabilité
    Id = ClassObjets.all_Id
    L = ClassObjets.all_shop_rates
    
    for i in range(len(L)):
        x=L[i]
        while x>0 :
            Random_Prob.append(Id[i])
            x-=1    ###Fin création liste proba
    shop_items = sample(Random_Prob, 3)
    item1 = Id.index(shop_items[0])
    item2 = Id.index(shop_items[1])
    item3 = Id.index(shop_items[2])
    return item1, item2, item3

def prix(x):
    prix = ClassObjets.all_shop_prices
    answer = x
    prix1 = prix[int(answer[0])]
    prix2 = prix[int(answer[1])]
    prix3 = prix[int(answer[2])]
    return prix1,prix2,prix3

def names(x):
    noms = ClassObjets.all_nom
    answer = x
    nom1 = noms[int(answer[0])]
    nom2 = noms[int(answer[1])]
    nom3 = noms[int(answer[2])]
    return nom1,nom2,nom3



"""
class ClassShop:



    def achat(self, personnage):


    def fermer_shop(self,):
"""
