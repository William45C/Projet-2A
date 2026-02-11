""" ARMES """ 
statsArmes = {      # "nom arme" : (dégats)
    "epee" : (10),
    #"rapiere" : (10 + character.agilite),
}

""" PERSONNAGE """
class ClassPersonnage:
    def __init__(self):
        self.name = ""
        self.viemax = 20
        self.vie = 20
        self.attack = 3
        self.defense = 3
        self.agilite = 3
        self.Or = 10
        self.pointCompetencesRestant = 10

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

    def inventaire(self):
        self.objets = []
        self.arme = "epee"
    
    def attaque(self,monstre):
        degats = self.attack + int(statsArmes[self.arme])
        print(f"Coup avec {self.arme}")
        print(f"Dégats: {degats}")
        monstre.vie -= degats

