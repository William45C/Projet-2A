from armes import *


""" PERSONNAGE """
class ClassPersonnage:
    def __init__(self,donjon):
        self.name = ""
        self.viemax = 200
        self.vie = 180
        self.attack = 60
        self.defense = 30
        self.agilite = 30
        self.Or = 1000
        self.objets = {
            "Potion de soin": 0,
            "Potion dorée": 0,
            "Potion douteuse": 0,
            "Potion très douteuse": 0,
            "Potion d'accélération temporel": 0,
            "Potion du coffre": 0,
            "Potion hostile": 0,
            "Potion de fortune": 0
        }
        self.arme = "epee"
        self.stats_armes = self.statsArmes(donjon)[self.arme].mod
        self.pointCompetencesRestant = 10

    def retrieveObjects(self):
        objects = list(self.objets.keys())
        inventaire = []
        for i in range(len(objects)):
            if self.objets[objects[i]] > 0:
                inventaire.append(f"{str(objects[i])} : {self.objets[objects[i]]}")
        return inventaire
    
    def statsArmes(self,donjon):
        """ ARMES """ 
        return {      # "nom arme" : (dégats)
            #"nom arme", 
            "epee" : ClassArmes(0,0,0,6,25,"Epee",self.attack,donjon),
            "rapier" : ClassArmes(0,0,0,6,10,"Rapiere", self.agilite,donjon),
            "shield" : ClassArmes(0,0,0,7,14,"Shield", self.defense,donjon),
            "goldKnuckles" : ClassArmes(0,0,0,1,1,"Poing duriche", self.Or,donjon)
        }

    def displayStats(self):
        print(f"""
═════STATS═════
Vie : {self.vie}  
Attaque : {self.attack}     
Defense : {self.defense}    
Agilite : {self.agilite}    
═══════════════
              """)
        
    def assignerCompetences(self):
        while self.pointCompetencesRestant > 0:
            assignAttack = True
            assignDefense = True
            assignAgilite = True

            while assignAttack:
                self.displayStats()
                print(f"Points restants {self.pointCompetencesRestant}")
                attack = int(input("Nombre de point a mettre dans attack >"))
                if self.pointCompetencesRestant >= attack:
                    self.pointCompetencesRestant -= attack
                    self.attack += attack
                    assignAttack = False
                else:
                    print("Sacrebleu! tu n'as pas assez de point")
            if int(self.pointCompetencesRestant) == 0:
                break
            while assignDefense:
                self.displayStats()
                print(f"Points restants {self.pointCompetencesRestant}")
                defense = int(input("Nombre de point a mettre dans defense >"))
                if self.pointCompetencesRestant >= defense:
                    self.pointCompetencesRestant -= defense
                    self.defense += defense
                    assignDefense = False
                else:
                    print("Traitre! tu n'as pas assez de point")
            if int(self.pointCompetencesRestant) == 0:
                break
            while assignAgilite:
                self.displayStats()
                print(f"Points restants {self.pointCompetencesRestant}")
                agilite = int(input("Nombre de point a mettre dans agilite >"))
                if self.pointCompetencesRestant >= agilite:
                    self.pointCompetencesRestant -= agilite
                    self.agilite += agilite
                    assignAgilite = False
                else:
                    print("Sacripant! tu n'as pas assez de point")
        self.displayStats()


