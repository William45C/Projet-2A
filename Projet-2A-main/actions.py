from random import *
from projet_2A_GUI import *
from personnage import *
from objets import *


class Actions:
    def __init__(self):
        self.action = input(f"""Quelle action prendre ?
                            Combat : 
                            -> attaque
                            -> esquive
                            -> bloque
                            -> utiliser un objet
                            -> fuir

                            Coffre : 
                            -> ouvrir
                            -> attaquer

                            Piège
                            -> esquive
                            -> tank

                            Salle vide : 
                            -> attendre
                            -> invocation
                            -> skip""")

    def monstre(monstre, personnage, current_state):
        if Actions.action == "attaque":
            if personnage.attack == "rapiere":
                jet = randint(0,100) + personnage.agilite - monstre.defense/2
                print(f"Bien joué ! Le monstre est blessé")
            else:
                jet = randint(0,100) + personnage.attack - monstre.defense/2
            if jet <= 85:
                monstre.vie -= personnage.attack
            else: 
                print(f"You failed to attack, fucking failure. Pathetic wench. Stupid dumb MFcker")
            
        elif Actions.action == "esquive":
            jet = randint(0,100) + personnage.agilite - monstre.attack/2
            if jet <= 80:
                print(f"Vous avez esquivé l'attaque d'une magnifique roulade. GOAT")
            else:
                personnage.vie -= monstre.attaque - personnage.defense
                print("Tu n'as même pas réussi à rouler pour éviter une attaque, pathétique. Skill issue. Small D.")

        elif Actions.action == "bloque":
            if personnage.arme == "shield":
                jet = randint(0,100) + personnage.defense*2 - monstre.attack/2
            else:
                jet = randint(0,100) + personnage.defense - monstre.attack/2
            if jet <= 80:
                print(f"Vous endurez complètement le choc comme un chad. Une telle puissance et une telle aura n'ont encore jamais été vus possédés par un humain.")
            elif jet <= 40:
                personnage.vie -= monstre.attack/2
                print(f"Vous endurez partiellement le choc. C'est efficace mais les points négatifs d'aura ne sont pas négligeables...")
            else:
                personnage.vie -= monstre.attack
                print(f"Tu bloque que dalle petit faible. Tu es si faible, tu t'attendait à quoi ? OMG j'ai honte pour toi.")

        elif Actions.action == "utiliser un objet":
            print(f"Cette fonction n'est pas disponible pour le moment, fais-toi bien enculer")
            #sortir l'inventaire
            #utiliser un objet
            #effets de l'objet
        elif Actions.action == "fuir":
            pass
            jet = randint(0,100) + personnage.agilite

            if jet <= (80 + personnage.agilite/10 - monstre.agilite/10):
            current_state = "RUN"
            #test d'agilité
            #si réussi, stage suivant (mais pas de récompense)
        else : 
            print("action non valide")

    def coffre(coffre):
        liste = ClassObjets.all_chest_rates[] + ClassArmes.all_chest_rates[]
        contenu = liste[randint(len(liste))]
        if Actions.action == "attaquer":
            if contenu == "potion_*":
                print(f"Vous avez brisé la potion dans le coffre...")
            elif contenu == "mimic":
                print(f"Et BAM ! Mimic dans ta gueule !")
                monstre = "mimic"
                current_state = "COMBAT"
        if Actions.action == "ouvrir":
            personnage.append(contenu)

"""
1-8 : potion_HP
9-16 : potion_guarenteed_up_stat
17-24 : potion_random_stat1
25-32 : potion_random_stat2
33-40 : potion_skip_level
41-48 : potion_guarenteed_chest
49-56 : potion_guarenteed_mob
57-64 : potion_gold_rate_up
65-72 : gold
73-80 : mimic
81-86 : epee
87-92 : rapier
93-99 : shield
100 : goldKnuckles
"""

    def piege():
        if Actions.action == "esquive":
            pass
        elif Actions.action == "tank":
            pass

    def vide():
        if Actions.action == "attendre":
            pass
        elif Actions.action == "invocation":
            pass
        elif Actions.action == "skip":
            pass





