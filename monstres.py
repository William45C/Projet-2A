from random import *
from donjon import *

def randomMonster(personnage, donjon): ##fonction qui génère un monstre aléatoire*
    return choice([ClassGoblin(donjon), ClassOgre(donjon), ClassSkeleton(donjon), ClassSacDePieces()])

def randomBoss(personnage, donjon): ##fonction qui génère un boss aléatoire
    return choice([ClassDragonDeFeu(donjon), ClassDragonDeGlace(donjon)])


class ClassGoblin: ##classe du monstre Goblin
    def __init__(self, donjon):
        self.name = "Goblin"
        self.vie = 5 * (donjon.level/5)
        self.attack = round(2 * (donjon.level/5))
        self.defense = 0 * (donjon.level/5)
        self.agilite = 5 * (donjon.level/5)
        self.deathgold = round(3 + (donjon.level/5),1)

class ClassMimic: ##classe du monstre Mimic
    def __init__(self, donjon):
        self.name = "Mimic"
        self.vie = 10 + donjon.level / 2
        self.attack = round(5 + donjon.level / 2)
        self.defense = 0 + donjon.level / 2
        self.agilite = 0 + donjon.level / 2
        self.deathgold = round(10+(donjon.level/2),1)

class ClassSkeleton: ##classe du monstre Skeleton
    def __init__(self, donjon):
        self.name = "Skeleton"
        self.vie = 10 + donjon.level / 8
        self.attack = round(5 + donjon.level / 8)
        self.defense = 0 + donjon.level / 8
        self.agilite = 2 + donjon.level / 8
        self.deathgold = round(10+(donjon.level/2),1)

class ClassOgre: ##classe du monstre Ogre
    def __init__(self, donjon):
        self.name = "Ogre"
        self.vie = 200 + donjon.level / 5
        self.attack = round(50 + donjon.level / 5)
        self.defense = 100 + donjon.level / 5
        self.agilite = 0 + donjon.level / 5
        self.deathgold = round(10 + donjon.level / 5,1)

class ClassDragonDeGlace: ##classe du boss Dragon de Glace
    def __init__(self, donjon):
        self.name = "Dragon de Glace"
        self.vie = 10 + donjon.level*1.05
        self.attack = 10 + donjon.level*1.05
        self.defense = 10 + donjon.level*1.05
        self.agilite = 10 + donjon.level*1.05
        self.deathgold = round(50 + donjon.level / 2,1)

class ClassSacDePieces: ##classe du monstre Sac de pièces
    def __init__(self):
        self.name = "Sac de pièces"
        self.vie = 1
        self.attack = 0
        self.defense = 0
        self.agilite = 20
        self.deathgold = 1

class ClassDragonDeFeu: ##classe du boss Dragon de Feu
    def __init__(self, donjon):
        self.name = "Dragon de feu"
        self.vie = 10 + donjon.level*1.05
        self.attack = 10 + donjon.level*1.05
        self.defense = 10 + donjon.level*1.05
        self.agilite = 10 + donjon.level*1.05
        self.deathgold = round(50 + donjon.level / 2,1)