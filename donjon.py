from random import *
import os
from objets import *

class ClassDonjon:
    def __init__(self):
        self.level = 1
        self.current_room = {"devant": "", "gauche": "", "droite": ""}
        self.devant = [
    "une porte suspecte",
    "un vieil escalier de style victorien",
    "une piscine",
    "un couloir faiblement éclairé",
    "une cave humide",
    "un grenier poussiéreux",
    "une bibliothèque silencieuse",
    "une tour en ruine",
    "une forêt brumeuse",
    "un marécage calme",
    "un pont suspendu",
    "une auberge tranquille",
    "une place de marché paisible",
    "un cimetière ancien",
    "une chapelle oubliée",
    "un laboratoire abandonné",
    "une salle du trône vide",
    "une prison déserte",
    "un tunnel de pierre",
    "une mine silencieuse",
    "un vieux moulin",
    "une serre envahie par les plantes",
    "un jardin labyrinthique",
    "une salle de bal déserte",
    "un théâtre poussiéreux",
    "une arène vide",
    "une caserne abandonnée",
    "une forge éteinte",
    "un port brumeux",
    "un phare isolé",
    "une falaise venteuse",
    "une plage déserte",
    "une grotte humide",
    "une caverne de cristal",
    "un volcan endormi",
    "une montagne enneigée",
    "un campement désert",
    "une cabane en bois",
    "un manoir silencieux",
    "une chambre verrouillée",
    "une salle aux miroirs",
    "une pièce secrète",
    "un sanctuaire ancien",
    "une salle aux mécanismes étranges",
    "un ascenseur immobile",
    "un toit sous la pluie",
    "une ruelle étroite",
    "une salle du trésor vide",
    "une salle inondée",
    "un aqueduc ancien",
    "un égout labyrinthique",
    "une salle aux statues fissurées",
    "une horloge géante intérieure",
    "un observatoire désert",
    "une salle des cartes",
    "un bureau abandonné",
    "une salle de classe poussiéreuse",
    "un réfectoire silencieux",
    "un dortoir vide",
    "une salle d'entraînement vide",
    "une salle des potions abandonnée",
    "un portail magique instable",
    "un cercle d'invocation éteint",
    "une dimension brumeuse",
    "une salle violette silencieuse",
    "une île flottante",
    "un navire échoué",
    "une cale sombre",
    "une salle des machines arrêtée",
    "un atelier d'alchimiste vide",
    "une armurerie verrouillée",
    "une salle aux pièges inactifs",
    "un couloir de portraits",
    "une salle figée dans le temps",
    "un miroir ancien",
    "une bibliothèque infinie",
    "une salle plongée dans l'obscurité",
    "une salle aux champignons lumineux",
    "un trône ancien",
    "une salle aux chaînes suspendues",
    "une armoire mystérieuse",
    "un puits profond",
    "un champ de ruines",
    "une clairière calme",
    "un arbre creux géant",
    "une maison ensablée",
    "une cité souterraine silencieuse",
    "une forteresse lointaine",
    "une salle aux runes brillantes",
    "une pièce changeante",
    "un escalier en colimaçon",
    "une porte couverte de symboles",
    "Polytech Nancy",
]

    def generer_nouvelle_salle(self):
        """Generates the layout of the next room without blocking the game."""
        murs = sample(range(0, 3), randint(1, 2))
        
        self.current_room["devant"] = "un mur" if 0 in murs else choice(self.devant)
        self.current_room["gauche"] = "un mur" if 1 in murs else choice(self.devant)
        self.current_room["droite"] = "un mur" if 2 in murs else choice(self.devant)
        
    def showRoom(self):
        print(self.current_room)
        
    def tenter_deplacement(self, direction, NextLevel=False, personnage=None):
        """
        Logic to check if movement is possible.
        Returns True if moved successfully, False if hit a wall.
        """
        if direction == 'o':
            return None
        else:
            mapping = {'z': 'devant', 'q': 'gauche', 'd': 'droite'}
            cible = mapping.get(direction)

            if cible and "mur" in self.current_room[cible]:
                return False
            elif NextLevel == True:
                return True


