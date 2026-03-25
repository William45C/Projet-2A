import pygame
import gif_pygame
from random import *
import speech_recognition as sr
import pyttsx3
from time import * 

""" IMPORTATION FICHIERS (Assumed existing) """
from personnage import *
from donjon import *
from monstres import *
from GUI import *
from shop import *
from armes import *

endGame = False

while True:
    # --- INITIALIZATION ---
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    skeleton_gif = gif_pygame.load("skeleton.gif")
    #goblin_gif = gif_pygame.load("goblin.gif")

    engine.setProperty('voice', "com.apple.voice.compact.zh-CN.Tingting")
    FPS = 60
    GREEN = (50, 255, 80)
    MID_GREEN = (0, 100, 30)
    TERMINAL_GREEN = (51, 255, 51)
    DARK_GREEN = (0, 40, 0)
    DUNGEON_PREVIEW_DIMENSIONS = (400, 300)

    donjon = ClassDonjon()
    character = ClassPersonnage(donjon)
    pygame.key.set_repeat(0, 100)
    antiHold = False
    GameOver = False
    endGame = False

    # --- CONSTANTS & GLOBALS ---
    STATE_EXPLORE = "EXPLORE"
    STATE_COMBAT = "COMBAT"
    STATE_EVENT = "EVENT"
    STATE_CHEST = "CHEST"
    STATE_SHOP = "SHOP"
    STATE_OBJECTS = "OBJECTS"
    STATE_RUN = "RUN"
    STATE_ATTACK = "ATTACK"
    STATE_UPGRADE = "UPGRADE" #l 181
    STATE_ESQUIVE = "ESQUIVE"
    STATE_TANK = "TANK"
    STATE_ENNEMYATTACK = "ENNEMYATTACK"

    current_state = STATE_EXPLORE
    gameEvent = "STARTING ADVENTURE"
    cmd_text = ""
    attack_index = 0
    monstre = None
    inShop = False
    running = True
    hp_monstre = 0
    inCombat = False
    available1 = False
    available2 = False
    available3 = False

    def get_combat_text(index):
        options = [" [_] ATTACK", " [_] RUN", " [_] USE ITEM"]
        return " / ".join([opt.replace("_", ">") if i == index else opt for i, opt in enumerate(options)])

    def get_chest_text(index):
        options = [" [_] OPEN IT", " [_] LEAVE IT"]
        return " / ".join([opt.replace("_", ">") if i == index else opt for i, opt in enumerate(options)])
    
    def get_shop_text(index):
        options = [f"[_] {potionNames[0]} : {potionPrices[0]}", f"\n[_] {potionNames[1]} : {potionPrices[1]}", f"\n[_] {potionNames[2]} : {potionPrices[2]}", "\n[_] LEAVE"]
        return "".join([opt.replace("_", ">") if i == index else opt for i, opt in enumerate(options)])
    
    def get_inventory_text(index, perso):
        inventaire = perso.retrieveObjects()
        options = [f"[_] {objet}  " for objet in inventaire]
        options.append("[_] Close")

        formatted = []
        for i, opt in enumerate(options):
            text = opt.replace("_", ">") if i == index else opt
            formatted.append(text)

            if (i + 1) % 2 == 0 and i != len(options) - 1:
                formatted.append("\n")

        return "".join(formatted)

    """ LOGIQUE DU JEU (Non-blocking version) """
    def trigger_next_room():
        global current_state, gameEvent, monstre, donjon, hp_monstre, available1, available2, available3, attack_index
        
        if donjon.level % 10 == 0:
            gameEvent = "BOSS ENCOUNTER! (Press SPACE to skip)"
            current_state = STATE_EVENT
        else:
            donjon.generer_nouvelle_salle()
            if donjon.level%10 == 0:
                current_state = STATE_COMBAT # Boss
            elif donjon.level%5 == 0 and inShop == False:
                current_state = STATE_SHOP
                available1 = True
                available2 = True
                available3 = True
            
            if current_state != STATE_SHOP and current_state != STATE_COMBAT:
                evenement = randint(0, 10)
                if evenement <= 5: # Combat
                    monstre = randomMonster(character, donjon)
                    gameEvent = f"YOU ENCOUNTER A {monstre.name.upper()} !"
                    hp_monstre = monstre.vie
                    current_state = STATE_COMBAT
                elif evenement <= 7: # Chest
                    gameEvent = "YOU FOUND A CHEST! (Is it safe to open ?)"
                    current_state = STATE_CHEST
                    attack_index = 0
                else: # Trap
                    gameEvent = "IT'S A TRAP! (Press SPACE)"
                    current_state = STATE_EVENT
                
    def draw_perspective_brick_wall(surface,):
        _WIDTH, _HEIGHT = DUNGEON_PREVIEW_DIMENSIONS[0], DUNGEON_PREVIEW_DIMENSIONS[1] # Dimensions of the canva
        _offsetX, _offsetY = 50,100 # Offset of the canva
        cx, cy = _WIDTH // 2, _HEIGHT // 2 # Centers
        
        fw_w, fw_h = 240, 180 # Dimensions of the wall in the back
        f_left, f_right = cx - fw_w//2, cx + fw_w//2 # Corners of the back wall
        f_top, f_bottom = cy - fw_h//2, cy + fw_h//2

        segments = 12 # Bricks "Column"
        z_planes = []
        for i in range(segments + 1):
            t = (i / segments) ** 0.8
            z_l = int(f_left * t)
            z_r = int(_WIDTH - (_WIDTH - f_right) * t)
            z_t = int(f_top * t)
            z_b = int(_HEIGHT - (_HEIGHT - f_bottom) * t)
            z_planes.append((z_l, z_r, z_t, z_b))
        
        rows = 10 # Bricks "Row"
        for r in range(rows + 1):
            y_front = (_HEIGHT // rows) * r
            y_back = f_top + (r * (f_bottom - f_top) // rows)
            
            if donjon.tenter_deplacement('q') is None or donjon.tenter_deplacement('q') == False:
                pygame.draw.line(surface, MID_GREEN, (_offsetX, y_front+_offsetY), (f_left+_offsetX, y_back+_offsetY), 1) # Left wall lines
            if donjon.tenter_deplacement('d') is None or donjon.tenter_deplacement('d') == False:
                pygame.draw.line(surface, MID_GREEN, (_WIDTH+_offsetX, y_front+_offsetY), (f_right+_offsetX, y_back+_offsetY), 1) # Right wall lines
            #pygame.draw.line(surface, MID_GREEN, (f_left+_offsetX, y_back+_offsetY), (f_right+_offsetX, y_back+_offsetY), 1) # Center wall lines
                    
            if r < rows:
                # Next row's Y positions to bound the vertical cut
                y_next_front = (_HEIGHT // rows) * (r + 1)
                y_next_back = f_top + ((r + 1) * (f_bottom - f_top) // rows)
                
                for s in range(len(z_planes)):
                    is_offset_row = r % 2 == 0
                    if (s % 2 == 0) if is_offset_row else (s % 2 != 0):
                        z_l, z_r, z_t, z_b = z_planes[s]
                        
                        if not donjon.tenter_deplacement('q') is None or donjon.tenter_deplacement('q') == False:
                            row_top_y = y_front + (y_back - y_front) * (z_l / f_left)
                            row_bot_y = y_next_front + (y_next_back - y_next_front) * (z_l / f_left)
                            pygame.draw.line(surface, MID_GREEN, (z_l+_offsetX, int(row_top_y)+_offsetY), (z_l+_offsetX, int(row_bot_y)+_offsetY), 1)
                            
                        if not donjon.tenter_deplacement('d') is None or donjon.tenter_deplacement('d') == False:
                            ratio_r = (_WIDTH - z_r) / (_WIDTH - f_right)
                            row_top_y_r = y_front + (y_back - y_front) * ratio_r
                            row_bot_y_r = y_next_front + (y_next_back - y_next_front) * ratio_r
                            pygame.draw.line(surface, MID_GREEN, (z_r+_offsetX, int(row_top_y_r)+_offsetY), (z_r+_offsetX, int(row_bot_y_r)+_offsetY), 1)
                        
                        if not donjon.tenter_deplacement('z') is None or donjon.tenter_deplacement('z') == False:
                            pygame.draw.line(surface, MID_GREEN, (f_left+_offsetX, int(y_back)+_offsetY), (f_right+_offsetX, int(y_back)+_offsetY), 1)
                        
        for i in range(11):
            x_f = (_WIDTH // 10) * i
            x_b = f_left + (i * (fw_w // 10))
            pygame.draw.line(surface, MID_GREEN, (x_f+_offsetX, _offsetY), (x_b+_offsetX, f_top+_offsetY), 1)
            pygame.draw.line(surface, MID_GREEN, (x_f+_offsetX, _HEIGHT+_offsetY), (x_b+_offsetX, f_bottom+_offsetY), 1)

    """ MAIN LOOP """
    while not endGame:
        if character.vie <= 0:
            engine.say("GAME OVER")
            engine.runAndWait()
            GameOver = True
        if current_state == STATE_COMBAT:
            cmd_text = get_combat_text(attack_index)
        #elif current_state == STATE_OBJECTS:
        #elif current_state == STATE_OBJECTS:
        elif current_state == STATE_OBJECTS:
            cmd_text = get_inventory_text(attack_index, character)
            
        elif current_state == STATE_UPGRADE:
            engine.say("Tututut ut ut, augmente tes stats ici")
            engine.runAndWait()
            if character.pointCompetencesRestant > 0:
                assignAttack = True
                assignDefense = True
                assignAgilite = True

        elif current_state == STATE_SHOP:
            engine.say("Welcome to my shop")
            engine.runAndWait()
            if inShop == False:
                inShop = True
                shopItems = shop_item_selection()
                print(shopItems)
                potionNames = names(shopItems)
                potionPrices = prix(shopItems)
                print(potionNames, potionPrices)
            cmd_text = get_shop_text(attack_index)

        elif current_state == STATE_CHEST:
            cmd_text = get_chest_text(attack_index)
            
        elif current_state == STATE_EXPLORE:
            room = donjon.current_room
            cmd_text = f"[Z] Devant: {room['devant']} \n[Q] Gauche: {room['gauche']} \n[D] Droite: {room['droite']} \n[O] Objects: {None}"
        
        elif current_state == STATE_COMBAT:
            fuite = False

        elif current_state == STATE_ATTACK:
            if character.attack == "rapiere":
                d100 = randint(0,100) + character.agilite - monstre.defense/2
            else:
                d100 = randint(0,100) + character.attack - monstre.defense/2
            if d100 <= 85:
                engine.say("Ow")
                engine.runAndWait()
                print(f"Bien joué ! Le monstre est blessé")
                attaque = character.attack + character.stats_armes
                if attaque > 0:
                    monstre.vie -= attaque
                    print(f"dégats {attaque}, Vie {monstre.vie}")
                else:
                    print("Skill issue, LOSER !")
            else: 
                print(f"You failed to attack, fucking failure. Pathetic wench. Stupid dumb MFcker")
            current_state = STATE_ENNEMYATTACK
                    
        elif current_state == STATE_ENNEMYATTACK:
            if monstre.vie >= 0:
                engine.say("Je vais te détruire ton petit cul blanc")
                engine.runAndWait()
                if d100 <= 80 + monstre.attack/10 - character.agilite/10:
                    attaque = round(monstre.attack - character.defense,2)
                    if attaque > 0:
                        character.vie -= round(attaque,2)
                        if character.vie < 0:
                            character.vie = 0
                        print(f"dégats {round(attaque,2)}")
                else:
                    engine.say("Je... Je... Je me meurs")
                    engine.runAndWait()
                    print("Vous évitez l'attaque du monstre magnifiquement !")
                current_state = STATE_COMBAT
            else:
                inCombat = False
                current_state = STATE_EVENT
                gameEvent = "YOU WIN THE FIGHT"
                character.Or += monstre.deathgold
                cmd_text = "press space to continue"

        elif current_state == STATE_ESQUIVE:
            d100 = randint(0,100) + character.agilite - monstre.attack/2
            if d100 <= 80:
                print(f"Vous avez esquivé l'attaque d'une magnifique roulade. GOAT")
            else:
                character.vie -= monstre.attaque - character.defense
                print("Tu n'as même pas réussi à rouler pour éviter une attaque, pathétique. Skill issue. Small D.")
            current_state = STATE_COMBAT
        
        elif current_state == STATE_TANK:
            if character.arme == "shield":
                d100 = randint(0,100) + character.defense*2 - monstre.attack/2
            else:
                d100 = randint(0,100) + character.defense - monstre.attack/2
            if d100 <= 80:
                print(f"Vous endurez complètement le choc comme un chad. Une telle puissance et une telle aura n'ont encore jamais été vus possédés par un humain.")
            elif d100 <= 40:
                character.vie -= monstre.attack/2
                print(f"Vous endurez partiellement le choc. C'est efficace mais les points négatifs d'aura ne sont pas négligeables...")
            else:
                character.vie -= monstre.attack
                print(f"Tu bloque que dalle petit faible. Tu es si faible, tu t'attendait à quoi ? OMG j'ai honte pour toi.")
            current_state = STATE_COMBAT
        
        elif current_state == STATE_RUN:
            d100 = randint(0,100)
            if d100<=(80 + character.agilite/10 - monstre.agilite/10):
                print(f"You run")
                current_state = STATE_EXPLORE
                inCombat = False
            else:
                print(f"You failed to run, you fcking coward")
                current_state = STATE_ENNEMYATTACK
                attack_index = 0

            current_state = STATE_EXPLORE
            #donjon.generer_nouvelle_salle()

                        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN and GameOver:
                if event.key == pygame.K_SPACE:
                    endGame=True
            if event.type == pygame.KEYDOWN and not antiHold and not GameOver or inCombat and not antiHold and not GameOver:
                antiHold = True
                # --- COMBAT LOGIC ---
                if current_state == STATE_COMBAT or current_state == STATE_CHEST or current_state == STATE_SHOP or current_state == STATE_OBJECTS:
                    if (current_state == STATE_CHEST): max_index = 2
                    elif (current_state == STATE_SHOP): max_index = 4
                    elif (current_state == STATE_OBJECTS): max_index = len(character.retrieveObjects()) +1
                    else: max_index = 4
                    if event.key == pygame.K_LEFT:
                        attack_index = (attack_index - 1) % max_index
                    elif event.key == pygame.K_RIGHT:
                        attack_index = (attack_index + 1) % max_index
                    elif event.key == pygame.K_SPACE:
                        print(f"Executed action: {attack_index}")
                        if current_state == STATE_SHOP and inShop:
                            if attack_index == 0 and available1:
                                if achat(shopItems[0], character):
                                    available1 = False
                                    potionPrices[0] = 'X'
                            elif attack_index == 1 and available2:
                                if achat(shopItems[1], character):
                                    available2 = False
                                    potionPrices[1] = 'X'
                            elif attack_index == 2 and available3:
                                if achat(shopItems[2], character):
                                    available3 = False
                                    potionPrices[2] = 'X'
                            elif attack_index == 3:
                                current_state = STATE_EVENT
                                #donjon.level += 1
                                inShop = False 
                            else:
                                print("Object n'est plus disponible")
                        if current_state == STATE_OBJECTS:
                            if attack_index == len(character.retrieveObjects()):
                                if inCombat:
                                    current_state = STATE_COMBAT
                                else:
                                    current_state = STATE_EXPLORE
                            else:
                                print(f"Using {character.retrieveObjects()[attack_index]}")
                                NomPotion = str(str(character.retrieveObjects()[attack_index]).split(' : ')[0])
                                obj = ClassObjets()
                                obj.GetEffect(NomPotion, character, donjon)
                                character.objets[NomPotion] -= 1
                        if current_state == STATE_CHEST:
                            if attack_index == 0:
                                loot = chest_loot()
                                gameEvent = f"YOU FOUND {chest_object_name(loot)}"
                                print(f"YOU FOUND {chest_object_name(loot)}, {loot}")
                                if loot == 8:
                                    character.Or += 10
                                elif loot == 9:
                                     current_state = STATE_COMBAT
                                elif 10<loot<15:
                                    armes.choix_darme
                                else:
                                    character.objets[names_select(loot)] += 1
                                    print(character.objets)

                                current_state = STATE_EVENT
                            elif attack_index == 1:
                                current_state = STATE_EVENT
                        if current_state == STATE_COMBAT:
                            inCombat = True
                            if attack_index == 0:
                                current_state = STATE_ATTACK
                            elif attack_index == 1:
                                print("run")
                                current_state = STATE_RUN
                            elif attack_index == 2:
                                print("object")        
                                current_state = STATE_OBJECTS
                                attack_index = 0
                            elif attack_index == 3:
                                print("esquive")
                                current_state = STATE_ESQUIVE
                            elif attack_index == 4:
                                print("tank")        
                                current_state = STATE_TANK
                
                # --- EXPLORATION LOGIC (Z, Q, D) ---
                if current_state == STATE_EXPLORE:
                    direction = None
                    if event.key == pygame.K_z: direction = 'z'
                    elif event.key == pygame.K_q: direction = 'q'
                    elif event.key == pygame.K_d: direction = 'd'
                    elif event.key == pygame.K_o: direction = 'o'

                    if direction:
                        if donjon.tenter_deplacement(direction, True, character) is None:
                            current_state = STATE_OBJECTS
                            attack_index = 0
                        elif donjon.tenter_deplacement(direction, True, character):
                            donjon.level += 1
                            trigger_next_room()
                        else:
                            gameEvent = "C'est un mur ! Choisissez un autre chemin."

                if current_state == STATE_EVENT:
                    if event.key == pygame.K_SPACE:
                        #donjon.level += 1
                        current_state = STATE_EXPLORE
                        donjon.generer_nouvelle_salle()
                        gameEvent = "EXPLORATION..."
            if event.type == pygame.KEYUP:
                antiHold = False 

        
        # rendering
        game_surface = render_game(character, gameEvent, cmd_text, donjon, current_state, TERMINAL_GREEN)
        screen.blit(game_surface, (0, 0))
        if current_state == STATE_COMBAT and not GameOver:
            #if monstre.name == "skeleton":
            skeleton_gif.render(screen, (50+(DUNGEON_PREVIEW_DIMENSIONS[0] - skeleton_gif.get_width())/2, 100+(DUNGEON_PREVIEW_DIMENSIONS[1] - skeleton_gif.get_height())/2))
            #if monstre.name == "goblin":
                #goblin_gif.render(screen, ((DUNGEON_PREVIEW_DIMENSIONS[0] - goblin_gif.get_width())/2, (DUNGEON_PREVIEW_DIMENSIONS[1] - goblin_gif.get_height())/2))
            
        if inShop == False:    
            draw_perspective_brick_wall(screen)
        else:
            pass
            """
            dx = DUNGEON_PREVIEW_DIMENSIONS[0]
            dy = DUNGEON_PREVIEW_DIMENSIONS[0]
            Yoffset = 10
            rect1 = pygame.draw.rect(screen, TERMINAL_GREEN, (70, 0+Yoffset+150, dx-40, 50))
            rect_ = pygame.draw.rect(screen, (0,0,0), (70, 0+Yoffset-2+150, dx-40, 50-2))
            rect2 = pygame.draw.rect(screen, TERMINAL_GREEN, (70, dy/3+Yoffset+150, dx-40, 50))
            rect_ = pygame.draw.rect(screen, (0,0,0), (70, dy/3+Yoffset-2+150, dx-40, 50-2))
            rect3 = pygame.draw.rect(screen, TERMINAL_GREEN, (70, dy*(2/3)+Yoffset+150, dx-40, 50))
            rect_ = pygame.draw.rect(screen, (0,0,0), (70, dy*(2/3)+Yoffset-2+150, dx-40, 50-2))
            font = pygame.font.SysFont(None, 36)
            text1 = font.render("First Item", True, TERMINAL_GREEN)
            text2 = font.render("Second Item", True, TERMINAL_GREEN)
            text3 = font.render("Third Item", True, TERMINAL_GREEN)
            text1_rect = text1.get_rect(center=rect1.center)
            text2_rect = text2.get_rect(center=rect2.center)
            text3_rect = text3.get_rect(center=rect3.center)
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            screen.blit(text3, text3_rect)
            """
        if GameOver:
            GREEN = (12, 120, 12)
            MID_GREEN = (12, 120, 12)
            TERMINAL_GREEN = (12, 120, 12)
            DARK_GREEN = (12, 120, 12)
            font = pygame.font.Font(None, 100)
            font2 = pygame.font.Font(None, 50)
            GOtext = font.render("- GAMEOVER -", True, (30, 150, 60))
            text_rect = GOtext.get_rect(center=(800/2, 600/2-50))
            textRestart = font2.render("PRESS SPACE TO RESTART", True, (30, 150, 40))
            text_rect2 = textRestart.get_rect(center=(800/2, 600/2+20))
            screen.blit(GOtext, text_rect)
            screen.blit(textRestart, text_rect2)
            pygame.display.flip()

        pygame.display.flip()
        clock.tick(FPS)