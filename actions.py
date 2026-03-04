"""
Fonctionnement : 
monstre
=> attaque (arme)
=> éviter (agilité)
=> bloquer (défense)
=> utiliser un objet
=> fuir

coffre
=> ouvrir le coffre
=> attaquer le coffre (arme)

piège
=> test pour éviter le piège

Vide
=> attendre un moment (récupère 1-2 HP)
=> skip la salle
=> invoquer une maison close pour se détendre un peu
"""

class Actions:
    def __init__(self):
        self.action = input("Quelle action prendre ?")
    def monstre(monstre):
        if Actions.action == "attaque":
            pass
            #utiliser une arme = test de force (ou agilité en fonction de l'arme)
            #si réussite : monstre.vie -= dégats de l'arme
        elif action == "esquive":
            pass
            #jet avec difficulté pour voir si on y arrive
            #si pas évité, character.vie -= monstre.attaque
        elif action == "bloque":
            pass
            #test pour voir si on endure le choc
            #si raté, character.vie -= monstre.attaque
        elif action == "utiliser un objet":
            pass
            #sortir l'inventaire
            #utiliser un objet
            #effets de l'objet
        elif action == "fuir":
            pass
            #test d'agilité
            #si réussi, stage suivant (mais pas de récompense)
        else : 
            print("action non valide")

    def coffre(coffre):
        if Actions.action == "":
            pass




