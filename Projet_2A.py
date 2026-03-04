"""Trucs qu'on peut utiliser : 
https://codeberg.org/nohkumado/matrix_mud
https://codeberg.org/nohkumado/mud_editor
"""

""" INSTALLATION """

""" IMPORTATION LIBRAIRIES """
import os, keyboard
import speech_recognition as sr

""" IMPORTATION FICHIERS """
from personnage import *
from donjon import *
from monstres import *

r = sr.Recognizer()

""" CREATION PERSONNAGE """
character = ClassPersonnage()
character.assignerCompetences()

donjon = ClassDonjon()

""" JEU """
def progression():
    #print(donjon.level)
    if donjon.level%10==0:
        print("BOSS")
        input("Skip boss >")
        donjon.level += 1
    if donjon.level%5==0 and donjon.level%10!=0:
        print("SHOP")
        input("Skip shop >")
        donjon.level += 1
    else:
        donjon.salleAleatoire(donjon)
        evenement = randint(0,10)
        if evenement in [0,1,2,3,4,5]:
            #print("Vous tombez soudainement nez-à-nez avec un SDF random")
            monstre = randomMonster(character)
            underline = "══════════"+"═"*len(monstre.name)
            print(f"""
═════{str(monstre.name).upper()}═════
Vie : {monstre.vie}        
{underline}
                  """)
            input("Actions et combat")
        elif evenement in [6,7]:
            print("Vous trouvez un coffre")
        elif evenement in [9]:
            print("CHOCKBAR y avait un piège")
        print("actions")
    return progression()

progression() 
"""
while True:
    if keyboard.is_pressed("t"):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                
                r.adjust_for_ambient_noise(source, duration=2)
                audio = r.listen(source)
                text = r.recognize_google(audio)
                text = text.lower()  
                if 'attack' in text:
                    print('Attacking the npc')
                else:
                    print("You said:", text)
                
                if "exit" in text:
                    print("Exiting program...")
                    break

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("Could not understand audio")

        except KeyboardInterrupt:
            print("Program terminated by user")
            break
"""