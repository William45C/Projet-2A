import speech_recognition as sr
def myCommand():
    r = sr.Recognizer()
    
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, phrase_time_limit=5)
            
            try:
                command = r.recognize_google(audio, language="fr-FR").lower()
                print("you said: " + command)
                return command
                
            except sr.UnknownValueError:
                print("Désolé, je n'ai pas compris. Réessayez...")
                
        except Exception as e:
            print(f"Erreur système micro : {e}")

def actionVocale(current_state,nbObjets,nbarmes):

    while True:
        print("Parle maintenant...")
        text = myCommand()
        print("fin")
        if text:
            if current_state == "SKILLS":
                print("Got skill text")
                return text
            if current_state == "EXPLORE":
                if "avance" in text.lower():
                    print("tout droit")
                    return 0
                if "droite" in text.lower() or "droit" in text.lower():
                    print("droite")
                    return 1
                if "gauche" in text.lower() or "gouche" in text.lower():
                    print("gauche")
                    return 2
                if "objet" in text.lower():
                    print("objet")
                    return 3
                if "inventaire" in text.lower():
                    print("inventaire")
                    return 4
            if current_state == "COMBAT":
                if "attaque" in text.lower():
                    print("utilise attack")
                    return 0
                if "fuite" in text.lower() or "8" in text.lower():
                    print("fuite")
                    return 1
                if "objet" in text.lower():
                    print("utilise objet")
                    return 2
                if "inventaire" in text.lower():
                    print("ouvre inventaire")
                    return 3
            if current_state == "CHEST":
                if "ouvrir" in text.lower():
                    print("ouvre coffre")
                    return 0
                if "laisser" in text.lower():
                    print("laisse coffre")
                    return 1
            if current_state == "COMBATBOSS" or current_state == "ATTACKBOSS":
                if "attaque" in text.lower():
                    return 0
                elif "esquive" in text.lower():
                    return 1
                elif "objet" in text.lower():
                    return 2
            if current_state == "SHOP":
                if "objet 1" in text.lower():
                    print("objet 1")
                    return 0
                if "objet 2" in text.lower():
                    print("objet 2")
                    return 1
                if "objet 3" in text.lower():
                    print("objet 3")
                    return 2
                if "partir" in text.lower():
                    print("part du shop")
                    return 3
            if current_state == "OBJECTS":
                if "objet" in text.lower():
                    try:
                        nbr = int(text.lower().split('objet ')[1][0])
                        if nbr > nbObjets:
                            print("non valable")
                            return nbObjets-1
                        else:
                            print(f"Objet {int(text.lower().split('objet ')[1][0])-1}")
                            return int(text.lower().split('objet ')[1][0])-1
                    except:
                        print(text.lower().split('objet ')[1][0], text.lower().split('objet '))
                if "partir" in text.lower():
                    return nbObjets-1
                
            if current_state == "INVENTORY":
                if "objet" in text.lower():
                    try:
                        nbr = int(text.lower().split('objet ')[1][0])
                        if nbr > nbarmes:
                            print("non valable")
                            return nbarmes-1
                        else:
                            print(f"Objet {int(text.lower().split('objet ')[1][0])-1}")
                            return int(text.lower().split('objet ')[1][0])-1
                    except:
                        print(text.lower().split('objet ')[1][0], text.lower().split('objet '))
                if "partir" in text.lower():
                    return nbarmes
            print("Commande:", text)
        else:
            print("no text")