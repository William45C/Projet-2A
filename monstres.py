from random import *
from donjon import *

def randomMonster(personnage, donjon):
    return choice([ClassGoblin(donjon), ClassOgre(donjon), ClassShapeshifter(personnage, donjon), ClassSkeleton(donjon), ClassIbrahim(), ClassDuez(donjon)])

class ClassGoblin:
    def __init__(self, donjon):
        self.name = "goblin"
        self.vie = 5 * (donjon.level/5)
        self.attack = round(2 * (donjon.level/5))
        self.defense = 0 * (donjon.level/5)
        self.agilite = 5 * (donjon.level/5)
        self.deathgold = round(3 + (donjon.level/5),1)

class ClassMimic:
    def __init__(self, donjon):
        self.name = "little mfcker"
        self.vie = 10 + donjon.level / 2
        self.attack = round(5 + donjon.level / 2)
        self.defense = 0 + donjon.level / 2
        self.agilite = 0 + donjon.level / 2
        self.deathgold = round(10+(donjon.level/2),1)

class ClassSkeleton:
    def __init__(self, donjon):
        self.name = "skeleton"
        self.vie = 10 + donjon.level / 8
        self.attack = round(5 + donjon.level / 8)
        self.defense = 0 + donjon.level / 8
        self.agilite = 2 + donjon.level / 8
        self.deathgold = round(10+(donjon.level/2),1)

class ClassOgre:
    def __init__(self, donjon):
        self.name = "ogre"
        self.vie = 200 + donjon.level / 5
        self.attack = round(50 + donjon.level / 5)
        self.defense = 100 + donjon.level / 5
        self.agilite = 0 + donjon.level / 5
        self.deathgold = round(10 + donjon.level / 5,1)

class ClassShapeshifter:
    def __init__(self, personnage, donjon):
        self.name = "shapeshifter"
        self.vie = personnage.vie*0.9
        self.attack = personnage.attack*0.9
        self.defense = personnage.defense*0.9
        self.agilite = personnage.agilite*0.9
        self.deathgold = round(10 + donjon.level / 2,1)

class ClassIbrahim:
    def __init__(self):
        self.name = "Ibrahim"
        self.vie = 1
        self.attack = 0
        self.defense = 0
        self.agilite = 100
        self.deathgold = 1

class ClassDuez:
    def __init__(self, donjon):
        self.name = "Duez"
        self.vie = 1000 + donjon.level
        self.attack = 200 + donjon.level
        self.defense = 300 + donjon.level
        self.agilite = 100 + donjon.level
        self.deathgold = 100 + donjon.level