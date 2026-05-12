from personnage import *
from objets import *
from random import *

def shop_item_selection(): ##Permet de sélectionner de manière aléatoire 3 objets à vendre dans la boutique, en fonction des taux d'apparition des objets dans la boutique.
    Random_Prob = [] ###Créer une liste de probabilité
    Id = ClassObjets.all_Id[:7]
    L = ClassObjets.all_shop_rates[:7]
    
    for i in range(len(L)):
        x=L[i]
        while x>0 :
            Random_Prob.append(Id[i])
            x-=1    ###Fin création liste proba
    shop_items = sample(Random_Prob, 3) ###Sélectionne 3 objets de manière aléatoire dans la liste de probabilité créée précédement.
    item1 = Id.index(shop_items[0])
    item2 = Id.index(shop_items[1])
    item3 = Id.index(shop_items[2])
    return [item1, item2, item3]

def prix(x): ##Permet d'obtenir le prix des 3 objets sélectionnés dans la boutique à partir de leur Id.
    prix = ClassObjets.all_shop_prices[:7]
    answer = x
    prix1 = prix[int(answer[0])]
    prix2 = prix[int(answer[1])]
    prix3 = prix[int(answer[2])]
    return [prix1,prix2,prix3]

def prix_select(x): ##Permet d'obtenir le prix de l'objet sélectionné par le joueur dans la boutique à partir de son Id.
    prix = ClassObjets.all_shop_prices[:7]
    answer = x
    prix1 = prix[int(answer)]
    return prix1

def names(x): ##Permet d'obtenir le nom des 3 objets sélectionnés dans la boutique à partir de leur Id.
    noms = ClassObjets.all_nom[:7]
    answer = x
    nom1 = noms[int(answer[0])]
    nom2 = noms[int(answer[1])]
    nom3 = noms[int(answer[2])]
    return [nom1,nom2,nom3]

def names_select(x): ##Permet d'obtenir le nom de l'objet sélectionné par le joueur dans la boutique à partir de son Id.
    noms = (ClassObjets.all_nom+armes.ClassArmes.all_nom)[:15]
    answer = x
    nom1 = noms[int(answer)]
    return nom1


def achat(select, Personnage): ##Permet d'acheter l'objet sélectionné par le joueur dans la boutique, en vérifiant que le joueur a assez d'or pour l'acheter et en ajoutant l'objet à l'inventaire du joueur.
    if select == 'X':
        return False

    if int(Personnage.Or) < prix_select(select): ##Vérifie que le joueur a assez d'or pour acheter l'objet sélectionné.
        print("Vous n'avez pas assez d'or")
        return False
    if int(Personnage.Or) >= prix_select(select): ##Si le joueur a assez d'or pour acheter l'objet sélectionné, on lui retire le prix de l'objet de son or et on ajoute l'objet à son inventaire.
        Personnage.Or -= round(prix_select(select), 1)
        Personnage.objets[names_select(select)] += 1
        print(f"Vous avez acheté {names_select(select)} pour {prix_select(select)} Or")
        return True
