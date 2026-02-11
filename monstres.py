from random import *

def randomMonster(personnage):
    return choice([ClassGoblin(), ClassOgre(), ClassShapeshifter(personnage)])

class ClassGoblin:
    def __init__(self):
        self.name = "goblin"
        self.vie = 5
        self.attack = 2
        self.defense = 0
        self.agilite = 5

class ClassOgre:
    def __init__(self):
        self.name = "ogre"
        self.vie = 200
        self.attack = 50
        self.defense = 100
        self.agilite = 0

class ClassShapeshifter:
    def __init__(self, personnage):
        self.name = "shapeshifter"
        self.vie = personnage.vie
        self.attack = personnage.attack
        self.defense = personnage.defense
        self.agilite = personnage.agilite

