from random import *
from donjon import *

class ClassArmes: ##Classe qui gère les armes du jeu
    all_Id = []
    all_boss_rates = []
    all_chest_rates = []
    all_nom = []

    def __init__(self, Id, shop_rate, shop_price, chest_rate=0, boss_rate=None, nom=None, affectation_personnage=None,donjon=None): ##Constructeur de la classe, prend en paramètres les caractéristiques de l'arme
        self.Id = Id
        self.boss_rate = boss_rate
        self.chest_rate = chest_rate
        self.nom = nom
        if donjon!=None: ##Si un donjon est spécifié, on calcule le modificateur de l'arme en fonction du niveau du donjon et de l'affectation du personnage
            self.mod = affectation_personnage*donjon.level*0.1

        ClassArmes.all_Id.append(Id)
        ClassArmes.all_boss_rates.append(boss_rate)
        ClassArmes.all_chest_rates.append(chest_rate)
        ClassArmes.all_nom.append(nom)
    
    def choix_darme(self, arme, personnage, donjon): ##Permet au joueur de choisir une arme parmi celles disponibles
        choix = input("Voulez-vous changer d'arme ?")
        if choix == "oui": ##Permet d'équiper une nouvelle arme si le joueur le souhaite, sinon l'arme actuelle reste équipée
            personnage.arme = arme
            self.stats_armes = self.statsArmes(donjon)[self.arme].mod
            print(f"Vous avez équipé : " + arme)
        elif choix == "non":
            print(f"Très bien, votre arme ne change donc pas.")
        else:
            print(f"Veuillez entrer 'oui' ou 'non'")

ClassArmes(10,0,0,6,25,"Epee"), ##Création de différentes armes avec leurs caractéristiques respectives
ClassArmes(11,0,0,6,10,"Rapiere"), ##shop_rate et shop_price sont à 0 car les armes ne sont pas achetables, elles sont trouvables dans les coffres ou sur les boss
ClassArmes(12,0,0,7,14,"Dague"), 
ClassArmes(13,0,0,1,1,"Poing duriche")
#nom = ClassArmes(id,shop_rate,shop_price,chest_rate,boss_rate,nom)

