import pygame
import gif_pygame
from random import *
import speech_recognition as sr
from time import *
import threading
import queue

""" IMPORTATION FICHIERS """
from personnage import *
from donjon import *
from monstres import *
from GUI import *
from shop import *
from armes import *
import VoiceControl as vc

""" SPEECH TO TEXT """
_vocal_paused = threading.Event() #Threading to prevent speech recognition from blocking the whole script
_vocal_paused.set()

"""
def vocal_thread_function():
    while True:
        _vocal_paused.wait()
        try:
            command = vc.myCommand()
            if command:
                speech_queue.put(command)
        except Exception as e:
            print(f"[VOCAL ERROR] {e}")
            sleep(1)

thread_vocal = threading.Thread(target=vocal_thread_function, daemon=True)
thread_vocal.start()
"""
_vc_result = queue.Queue()
_vc_running = False

def _vc_worker(state, n_objects, nbarmes):
    try:
        _vocal_paused.clear()
        try:
            result = vc.actionVocale(state, n_objects, nbarmes)
        except Exception:
            result = None
        finally:
            _vocal_paused.set()
        _vc_result.put(result)
    except Exception as e:
        print(e)

#speech_queue = queue.Queue()
    
def start_voice_recognition(state, n_objects, nbarmes):
    """Launch voice recognition in background.  Non-blocking."""
    global _vc_running
    if _vc_running:
        return
    _vc_running = True
    t = threading.Thread(target=_vc_worker, args=(state, n_objects, nbarmes), daemon=True)
    t.start()

def poll_voice_result(): # Return the text translated from speech
    global _vc_running
    try:
        val = _vc_result.get_nowait()
        _vc_running = False
        return True, val
    except queue.Empty:
        return False, None

# timer used for pacing
_timer_end = 0.0

def set_timer(seconds):
    global _timer_end
    _timer_end = time() + seconds

def timer_done():
    return time() >= _timer_end

endGame = False

# --- INITIALIZATION ---
pygame.init()
pygame.mixer.init()
themesong = pygame.mixer.music.load("newbattle.wav")
pygame.mixer.music.play(-1,0.0)
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

SkillAssignement = pygame.image.load('SkillAssignement.png')
SkillAssignement = pygame.transform.scale(SkillAssignement, (1000, 692))
r2 = SkillAssignement.get_rect()
r2.center = screen.get_rect().center
    
Underline = pygame.image.load('Underline.png')
Underline = pygame.transform.scale(Underline, (223, 35))
    
MuteMic = pygame.image.load('MuteMic.png')
MuteMic = pygame.transform.scale(MuteMic, (220/2, 236/2))
OpenMic = pygame.image.load('OpenMic.png')
OpenMic = pygame.transform.scale(OpenMic, (234/2, 246/2))

MuteMic = pygame.image.load('MuteMic.png')
MuteMic = pygame.transform.scale(MuteMic, (220/2, 236/2))
OpenMic = pygame.image.load('OpenMic.png')
OpenMic = pygame.transform.scale(OpenMic, (234/2, 246/2))
    
skeleton_gif = gif_pygame.load("skeleton.gif")
#goblin_gif = gif_pygame.load("goblin.gif")

FPS = 60
GREEN = (87, 229, 121)
MID_GREEN = (87, 229, 121)
TERMINAL_GREEN = (87, 229, 121)
DARK_GREEN = (0, 40, 0)
DUNGEON_PREVIEW_DIMENSIONS = (400, 300)

donjon = ClassDonjon()
character = ClassPersonnage(donjon)
pygame.key.set_repeat(0, 100)


def get_combat_text(index):
        options = [" [_] ATTAQUE", " [_] FUITE", " [_] OBJET"]
        return " / ".join([opt.replace("_", ">") if i == index else opt for i, opt in enumerate(options)])

def get_combatboss_text(index):
        options = [" [_] ATTAQUE", " [_] DUCK", " [_] OBJET"]
        return " / ".join([opt.replace("_", ">") if i == index else opt for i, opt in enumerate(options)])

def get_chest_text(index):
        options = [" [_] OUVRIR", " [_] LAISSER"]
        return " / ".join([opt.replace("_", ">") if i == index else opt for i, opt in enumerate(options)])

def get_shop_text(index):
        if not potionNames or not potionPrices:
            return ""
        else:
            options = [f"[_] {potionNames[0]} : {potionPrices[0]}", f"\n[_] {potionNames[1]} : {potionPrices[1]}", f"\n[_] {potionNames[2]} : {potionPrices[2]}", "\n[_] PARTIR"]
            return "".join([opt.replace("_", ">") if i == index else opt for i, opt in enumerate(options)])

def get_objects_text(index, perso):
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
        
def get_inventory_text(index, perso):
        inventaire = perso.weapons
        options = [f"[_] {chest_object_name(objet)}  " for objet in inventaire]
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
        global current_state, gameEvent, monstre, donjon, hp_monstre, available1, available2, available3, attack_index, game_surface, cmd_text, hp_boss, hp_max_boss, boss, inShop
        global pending_state, pending_cmd, pending_event

        if donjon.level % 10 == 0:
            boss = randomBoss(character, donjon)
            gameEvent = f"BOSS {boss.name.upper()}"
            # Show the boss intro for 5 s then enter boss combat
            pending_state = STATE_COMBATBOSS
            pending_cmd   = cmd_text
            pending_event = gameEvent
            set_timer(2)
            current_state = STATE_PENDING
            print(f"BOSS {boss.name.upper()}")
            hp_boss = boss.vie
            hp_max_boss = boss.vie
        else:
            donjon.generer_nouvelle_salle()
            if donjon.level % 5 == 0 and inShop == False:
                current_state = STATE_SHOP
                available1 = True
                available2 = True
                available3 = True

            if current_state != STATE_SHOP and current_state != STATE_COMBAT:
                evenement = randint(0, 10)
                if evenement <= 5:  # Combat
                    print(" !!! NEW MONSTER !!!")
                    monstre = randomMonster(character, donjon)
                    gameEvent = f"YOU ENCOUNTER A {monstre.name.upper()} !"
                    cmd_text = f"Vous entrez en confrontation"
                    hp_monstre = monstre.vie
                    # Show encounter message for 5 s then start combat
                    pending_state = STATE_COMBAT
                    pending_cmd   = cmd_text
                    pending_event = gameEvent
                    set_timer(2)
                    current_state = STATE_PENDING
                    print(f"YOU ENCOUNTER A {monstre.name.upper()} !")
                elif evenement <= 7:  # Chest
                    gameEvent = "YOU FOUND A CHEST! (Is it safe to open ?)"
                    current_state = STATE_CHEST
                    attack_index = 0
                else:  # Trap
                    gameEvent = "IT'S A TRAP! (Press SPACE)"
                    current_state = STATE_EVENT

def draw_perspective_brick_wall(surface,):
        _WIDTH, _HEIGHT = DUNGEON_PREVIEW_DIMENSIONS[0], DUNGEON_PREVIEW_DIMENSIONS[1]
        _offsetX, _offsetY = 50, 100
        cx, cy = _WIDTH // 2, _HEIGHT // 2

        fw_w, fw_h = 240, 180
        f_left, f_right = cx - fw_w//2, cx + fw_w//2
        f_top, f_bottom = cy - fw_h//2, cy + fw_h//2

        segments = 12
        z_planes = []
        for i in range(segments + 1):
            t = (i / segments) ** 0.8
            z_l = int(f_left * t)
            z_r = int(_WIDTH - (_WIDTH - f_right) * t)
            z_t = int(f_top * t)
            z_b = int(_HEIGHT - (_HEIGHT - f_bottom) * t)
            z_planes.append((z_l, z_r, z_t, z_b))

        rows = 10
        for r in range(rows + 1):
            y_front = (_HEIGHT // rows) * r
            y_back = f_top + (r * (f_bottom - f_top) // rows)

            left_is_wall  = "mur" in str(donjon.current_room.get('gauche', '')).lower()
            right_is_wall = "mur" in str(donjon.current_room.get('droite', '')).lower()
            front_is_wall = "mur" in str(donjon.current_room.get('devant', '')).lower()
            
            if left_is_wall:
                pygame.draw.line(surface, MID_GREEN, (_offsetX, y_front+_offsetY), (f_left+_offsetX, y_back+_offsetY), 1)
            if right_is_wall:
                pygame.draw.line(surface, MID_GREEN, (_WIDTH+_offsetX, y_front+_offsetY), (f_right+_offsetX, y_back+_offsetY), 1)

            if r < rows:
                y_next_front = (_HEIGHT // rows) * (r + 1)
                y_next_back = f_top + ((r + 1) * (f_bottom - f_top) // rows)

                for s in range(len(z_planes)):
                    is_offset_row = r % 2 == 0
                    if (s % 2 == 0) if is_offset_row else (s % 2 != 0):
                        z_l, z_r, z_t, z_b = z_planes[s]

                        if left_is_wall:
                            row_top_y = y_front + (y_back - y_front) * (z_l / f_left)
                            row_bot_y = y_next_front + (y_next_back - y_next_front) * (z_l / f_left)
                            pygame.draw.line(surface, MID_GREEN, (z_l+_offsetX, int(row_top_y)+_offsetY), (z_l+_offsetX, int(row_bot_y)+_offsetY), 1)

                        if right_is_wall:
                            ratio_r = (_WIDTH - z_r) / (_WIDTH - f_right)
                            row_top_y_r = y_front + (y_back - y_front) * ratio_r
                            row_bot_y_r = y_next_front + (y_next_back - y_next_front) * ratio_r
                            pygame.draw.line(surface, MID_GREEN, (z_r+_offsetX, int(row_top_y_r)+_offsetY), (z_r+_offsetX, int(row_bot_y_r)+_offsetY), 1)

                        if front_is_wall:
                            pygame.draw.line(surface, MID_GREEN, (f_left+_offsetX, int(y_back)+_offsetY), (f_right+_offsetX, int(y_back)+_offsetY), 1)

        for i in range(11):
            x_f = (_WIDTH // 10) * i
            x_b = f_left + (i * (fw_w // 10))
            pygame.draw.line(surface, MID_GREEN, (x_f+_offsetX, _offsetY), (x_b+_offsetX, f_top+_offsetY), 1)
            pygame.draw.line(surface, MID_GREEN, (x_f+_offsetX, _HEIGHT+_offsetY), (x_b+_offsetX, f_bottom+_offsetY), 1)

font_text = pygame.font.SysFont("Courier", 40, bold=True)
font_val = pygame.font.SysFont("Courier", 30, bold=True)
font_small = pygame.font.SysFont("Courier", 20, bold=True)

def draw_interface():
        
        # Upper text
        txt_points = font_text.render(f"{character.pointCompetencesRestant} points d'aptitudes restants", True, TERMINAL_GREEN)
        screen.blit(txt_points, (SCREEN_WIDTH // 2 - txt_points.get_width() // 2, 50))

        # Displaying aptitudes values
        rect_width, rect_height = 150, 100
        spacing = 100
        start_x = (SCREEN_WIDTH - (3 * rect_width + 2 * spacing)) // 2
        y_pos = (SCREEN_HEIGHT // 2) - (rect_height // 2)

        # avaiable skills linked to the character
        skills = [
            {"name": "ATTAQUE", "val": character.attack, "id": 1},
            {"name": "DÉFENSE", "val": character.defense, "id": 2},
            {"name": "AGILITÉ", "val": character.agilite, "id": 3}
        ]

        # display the selected skill
        for i, skill in enumerate(skills):
            rect_x = start_x + i * (rect_width + spacing)
            
            if current_skill == skill["id"]:
                screen.blit(Underline, (rect_x-40, 450))
                
            # Display the value
            txt_val = font_val.render(str(skill["val"]), True, BLACK)
            screen.blit(txt_val, (rect_x + rect_width//2 - txt_val.get_width()//2, y_pos + 35))

        # bottom instructions
        instruction_str = "Prononcez le nom d'une aptitude pour la sélectionner ou 'ajoute X'\npour ajouter des points"
        txt_instr = font_small.render(instruction_str, True, TERMINAL_GREEN)
        screen.blit(txt_instr, (SCREEN_WIDTH // 2 - txt_instr.get_width() // 2, SCREEN_HEIGHT - 60))

def cancel_voice():
    global _vc_running
    _vc_running = False
    # drain stale result if any
    try:
        _vc_result.get_nowait()
    except queue.Empty:
        pass
    
def clamp_index(idx, max_exclusive):
    return max(0, min(idx, max_exclusive - 1))

# load main screen   
img = pygame.image.load('MainScreen.png')
img = pygame.transform.scale(img, (200*3, 152*3))

# main loop to restart when losing the game  
while True:
    antiHold = False
    GameOver = False
    endGame = False
    micOpen = False

    # different game states
    STATE_EXPLORE = "EXPLORE"
    STATE_COMBAT = "COMBAT"
    STATE_COMBATBOSS = "COMBATBOSS"
    STATE_EVENT = "EVENT"
    STATE_CHEST = "CHEST"
    STATE_SHOP = "SHOP"
    STATE_OBJECTS = "OBJECTS"
    STATE_INVENTORY = "INVENTORY"
    STATE_RUN = "RUN"
    STATE_ATTACK = "ATTACK"
    STATE_ATTACKBOSS = "ATTACKBOSS"
    STATE_UPGRADE = "UPGRADE"
    STATE_ESQUIVE = "ESQUIVE"
    STATE_ESQUIVEBOSS = "ESQUIVEBOSS"
    STATE_TANK = "TANK"
    STATE_ENNEMYATTACK = "ENNEMYATTACK"
    STATE_BOSSATTACK = "BOSSATTACK"
    STATE_SKILLS = "SKILLS"
    
    # state to create pacing
    STATE_PENDING = "PENDING"
    pending_state = None
    pending_cmd   = ""
    pending_event = ""

    # default values
    current_state = STATE_SKILLS
    gameEvent = "STARTING ADVENTURE"
    cmd_text = ""
    attack_index = 0
    monstre = None
    boss = None
    d100 = 0
    inShop = False
    running = True
    hp_monstre = 0
    hp_boss = 0
    hp_max_boss = 0
    inCombat = False
    inCombatBoss = False
    available1 = False
    available2 = False
    available3 = False
    upgradeAnnounced = False

    
    voice_listening = False
    
    """ SKILLS ASSIGNATION """
    current_skill = 1

    """ MAIN SCREEN """
    startGame = False
    
    while not startGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startGame = True
        
        r = img.get_rect()
        r.center = screen.get_rect().center
        screen.blit(img, r)
        pygame.display.flip()

    print("Starting game...")
    
    """ INITIALISATION """
    # show skills menu
    screen.fill((0,0,0))
    screen.blit(SkillAssignement, (r2[0]+5,r2[1]))
    draw_interface()
    pygame.display.flip()   
    
    """ MAIN LOOP """
    while not endGame and running:
            
        # exploration
        if not GameOver or inCombat and not GameOver and current_skill != STATE_SKILLS:
            if current_state == STATE_EVENT:
                sleep(1)
                donjon.generer_nouvelle_salle()
                current_state = STATE_EXPLORE
                gameEvent = "EXPLORATION..."
                room = donjon.current_room
                cmd_text = f"[Z] Devant: {room['devant']} \n[Q] Gauche: {room['gauche']} \n[D] Droite: {room['droite']} \n[O] Objects: {None}"
                        
        # announce upgrade
        if current_state != STATE_UPGRADE:
            upgradeAnnounced = False
        
        # waiting state
        if current_state == STATE_PENDING:
            if timer_done():
                current_state = pending_state
                gameEvent     = pending_event
                cmd_text      = pending_cmd

        # check if player has remaining health points
        elif character.vie <= 0:
            #say("GAME OVER")
            GameOver = True

        # display fight text
        elif current_state == STATE_COMBAT:
            cmd_text = get_combat_text(attack_index)

        # display boss fight text
        elif current_state == STATE_COMBATBOSS:
            cmd_text = get_combatboss_text(attack_index)

        # display objects that the player has
        elif current_state == STATE_OBJECTS:
            cmd_text = get_objects_text(attack_index, character)
        
        # display weapons that the player has
        elif current_state == STATE_INVENTORY:
            cmd_text = get_inventory_text(attack_index, character)

        # upgrade stats
        elif current_state == STATE_UPGRADE:
            if not upgradeAnnounced:
                #say("Tututut ut ut, augmente tes stats ici")
                upgradeAnnounced = True
            if character.pointCompetencesRestant > 0:
                assignAttack = True
                assignDefense = True
                assignAgilite = True

        # open shop
        elif current_state == STATE_SHOP:
            try:
                if inShop == False:
                    #say("Welcome to my shop")
                    inShop = True
                    shopItems = shop_item_selection()
                    print(shopItems)
                    potionNames = names(shopItems)
                    potionPrices = prix(shopItems)
                    print(potionNames, potionPrices)
                cmd_text = get_shop_text(attack_index)
            except Exception as e:
                print(e)

        # found a chest !
        elif current_state == STATE_CHEST:
            cmd_text = get_chest_text(attack_index)

        # exploration state
        elif current_state == STATE_EXPLORE:
            room = donjon.current_room
            cmd_text = f"[Z] Devant: {room['devant']} \n[Q] Gauche: {room['gauche']} \n[D] Droite: {room['droite']} \n[O] Objects: {None}"

        # fighting an ennemy
        elif current_state == STATE_ATTACK:
            if character.attack == "rapiere":
                d100 = randint(0, 100) #- character.agilite + monstre.defense/2
            else:
                d100 = randint(0, 100) #- character.attack + monstre.defense/2
            
            if d100 <= 85:
                #say("Ow")
                attaque = character.attack + character.stats_armes
                if attaque > 0:
                    if monstre == None:
                        monstre = randomMonster(character, donjon)
                    monstre.vie -= attaque
                    cmd_text = f"dégats {attaque}, Vie {monstre.vie}"
                    print(f"Bien joué ! Le monstre est blessé – dégats {attaque}, Vie {monstre.vie}")
                else:
                    cmd_text = "You failed..."
                    print("You failed...")
            else:
                cmd_text = "You failed to attack"
                print(cmd_text)

            pending_state = STATE_ENNEMYATTACK
            pending_cmd   = cmd_text
            pending_event = gameEvent
            set_timer(3)
            current_state = STATE_PENDING

        # attack on boss
        elif current_state == STATE_ATTACKBOSS:
            if character.attack == "rapiere":
                d100 = randint(0, 100) #- character.agilite + boss.defense/2
            else:
                d100 = randint(0, 100) #- character.attack + boss.defense/2
            print(d100, character.attack, boss.defense)

            if d100 <= 80:
                #say("Ow")
                attaque = character.attack + character.stats_armes
                if attaque > 0:
                    boss.vie -= attaque
                    cmd_text = f"dégats {attaque}, Vie {boss.vie}"
                    print(f"Bien joué ! Le boss est blessé – dégats {attaque}, Vie {boss.vie}")
                    hp_boss = boss.vie
                else:
                    cmd_text = "You fail..."
                    print("You fail...")
            else:
                cmd_text = "You failed to attack..."
                print(cmd_text)

            pending_state = STATE_BOSSATTACK
            pending_cmd   = cmd_text
            pending_event = gameEvent
            set_timer(3)
            current_state = STATE_PENDING

        # state where the ennemy attack the player
        elif current_state == STATE_ENNEMYATTACK:
            if monstre.vie >= 0:
                #say("MOUAHAHA")
                if d100 <= 80 + monstre.attack/10 - character.agilite/10:
                    attaque = round(monstre.attack - character.defense, 2)
                    if attaque > 0:
                        character.vie -= round(attaque, 2)
                        if character.vie < 0:
                            character.vie = 0
                        cmd_text = f"dégats {round(attaque, 2)}"
                        print(f"dégats {round(attaque, 2)}")
                else:
                    #say("Je... Je... Je me meurs")
                    cmd_text = "Vous évitez l'attaque du monstre magnifiquement !"
                    print(cmd_text)

                pending_state = STATE_COMBAT
                pending_cmd   = cmd_text
                pending_event = gameEvent
                set_timer(1)
                current_state = STATE_PENDING
            else:
                inCombat = False
                current_state = STATE_EVENT
                gameEvent = "YOU WIN THE FIGHT"
                character.Or += monstre.deathgold
                cmd_text = "press space to continue"

        # boss attack the player
        elif current_state == STATE_BOSSATTACK:
            if boss.vie >= 0:
                #say("MOUAHAHAH")
                if d100 <= 80 + boss.attack/10 - character.agilite/10:
                    attaque = round(boss.attack - character.defense, 2)
                    if attaque > 0:
                        character.vie -= round(attaque, 2)
                        if character.vie < 0:
                            character.vie = 0
                        cmd_text = f"dégats boss {round(attaque, 2)}"
                        print(f"dégats boss {round(attaque, 2)}")
                else:
                    #say("Je... Je... Je me meurs")
                    cmd_text = "Vous évitez l'attaque du boss magnifiquement !"
                    print(cmd_text)

                pending_state = STATE_COMBATBOSS
                pending_cmd   = cmd_text
                pending_event = gameEvent
                set_timer(1)
                current_state = STATE_PENDING
            else:
                inCombatBoss = False
                current_state = STATE_SKILLS
                character.pointCompetencesRestant+=5
                gameEvent = "YOU DEFEATED THE BOSS!"
                character.Or += boss.deathgold
                cmd_text = "press space to continue"

        # dodging state
        elif current_state == STATE_ESQUIVE:
            d100 = randint(0, 100) + character.agilite - monstre.attack/2
            if d100 <= 80:
                print("Vous avez esquivé l'attaque d'une magnifique roulade. GOAT")
            else:
                character.vie -= monstre.attack - character.defense
                print("Tu n'as même pas réussi à rouler pour éviter une attaque")
            current_state = STATE_COMBAT

        # dodging the boss
        elif current_state == STATE_ESQUIVEBOSS:
            d100 = randint(0, 100) + character.agilite - boss.attack/2
            if d100 <= 80:
                print("Vous avez esquivé l'attaque")
            else:
                character.vie -= boss.attack - character.defense
                print("Vous n'avez pas réussi à esquiver.")
            current_state = STATE_COMBATBOSS

        # trying to tank the attack
        elif current_state == STATE_TANK:
            if character.arme == "shield":
                d100 = randint(0, 100) + character.defense*2 - monstre.attack/2
            else:
                d100 = randint(0, 100) + character.defense - monstre.attack/2
            if d100 <= 40:
                character.vie -= monstre.attack/2
                print("Vous endurez partiellement le choc.")
            elif d100 <= 80:
                print("Vous endurez complètement le choc comme un chad.")
            else:
                character.vie -= monstre.attack
                print("Tu bloque que dalle petit faible.")
            current_state = STATE_COMBAT

        # run away
        elif current_state == STATE_RUN:
            d100 = randint(0, 100)
            if d100 <= (80 + character.agilite/10 - monstre.agilite/10):
                cmd_text = f"You run"
                print("You run")
                pending_state = STATE_EXPLORE
                pending_cmd   = cmd_text
                pending_event = gameEvent
                set_timer(3)
                current_state = STATE_PENDING
                inCombat = False
            else:
                cmd_text = f"You failed to run"
                print(cmd_text)
                pending_state = STATE_ENNEMYATTACK
                pending_cmd   = cmd_text
                pending_event = gameEvent
                set_timer(3)
                current_state = STATE_PENDING
                attack_index = 0
        
        # handelign the exiting command
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and GameOver:
                # restart key
                if event.key == pygame.K_SPACE:
                    endGame = True
                if event.type == pygame.KEYUP:
                    antiHold = False

        # States that accept voice input
        voice_states = (STATE_COMBAT, STATE_COMBATBOSS, STATE_CHEST,
                        STATE_SHOP, STATE_OBJECTS, STATE_EXPLORE, STATE_INVENTORY, STATE_SKILLS)

        if current_state in voice_states and not GameOver:
            # start listening if not already
            if not _vc_running:
                start_voice_recognition(current_state, len(character.retrieveObjects()) + 1, len(character.weapons))
                micOpen = True
            else:
                micOpen = True

            # get results
            got_result, commandeVocale = poll_voice_result()
            if not got_result:              
                got_result, commandeVocale = poll_voice_result()
            
            if got_result:
                micOpen = False
                
                # state to assign skills
                if current_state == STATE_SKILLS:
                    # if there are no reamining skill points we go to the game
                    if character.pointCompetencesRestant == 0:
                        sleep(1)
                        current_state = STATE_EXPLORE
                    
                    try:
                            # debug output
                            print(f"Commande reçue : {commandeVocale}")
                            
                            # detect spoken ability
                            if "attaque" in commandeVocale or "aba" in commandeVocale:
                                current_skill = 1
                            elif "défense" in commandeVocale:
                                current_skill = 2
                            elif "agilité" in commandeVocale:
                                current_skill = 3
                            
                            # extract number of points to extract
                            parts = commandeVocale.split(' ')
                            if len(parts) > 1 and parts[1].isdigit():
                                nb = int(parts[1])
                                if nb <= character.pointCompetencesRestant:
                                    if current_skill == 1: character.attack += nb
                                    elif current_skill == 2: character.defense += nb
                                    elif current_skill == 3: character.agilite += nb
                                    character.pointCompetencesRestant -= nb

                    except queue.Empty:
                        pass

                    screen.fill((0, 0, 0))
                    screen.blit(SkillAssignement, r2)
                    draw_interface()
                    pygame.display.flip()
                        
                if current_state == STATE_CHEST:
                    max_index = 2
                elif current_state == STATE_SHOP:
                    max_index = 4
                elif current_state == STATE_OBJECTS:
                    max_index = len(character.retrieveObjects()) + 1
                elif current_state == STATE_INVENTORY:
                    max_index = len(character.weapons)
                else:
                    max_index = 4

                if type(commandeVocale) == int:
                    attack_index = commandeVocale
                    print(f"Executed action: {attack_index}")

                    # travel the dungeon
                    if current_state == STATE_EXPLORE:
                        direction = None
                        if attack_index == 0:
                            direction = 'z'
                        if attack_index == 1:
                            direction = 'd'
                        if attack_index == 2:
                            direction = 'g'
                        if attack_index == 3:
                            direction = 'o'
                        if attack_index == 4:
                            direction = 'i'
                        if direction:
                            # see objects
                            if donjon.tenter_deplacement(direction, True, character) == "object":
                                current_state = STATE_OBJECTS
                                attack_index = 0
                            # see inventory
                            elif donjon.tenter_deplacement(direction, True, character) == "inventory":
                                current_state = STATE_INVENTORY
                                attack_index = 0
                            # go forward, left pr right
                            elif donjon.tenter_deplacement(direction, True, character):
                                donjon.level += 1
                                trigger_next_room()
                            else:
                                gameEvent = "C'est un mur ! Choisissez un autre chemin."
                    
                    # shop system
                    elif current_state == STATE_SHOP and inShop:
                        # Purchasing object 1
                        if attack_index == 0 and available1:
                            if achat(shopItems[0], character):
                                available1 = False
                                potionPrices[0] = 'X'
                        # Purchasing object 2
                        elif attack_index == 1 and available2:
                            if achat(shopItems[1], character):
                                available2 = False
                                potionPrices[1] = 'X'
                        # Purchasing object 3
                        elif attack_index == 2 and available3:
                            if achat(shopItems[2], character):
                                available3 = False
                                potionPrices[2] = 'X'
                        # leave shop
                        elif attack_index == 3:
                            current_state = STATE_EVENT
                            inShop = False
                        else:
                            print("Object n'est plus disponible")

                    # allow usage of potions
                    elif current_state == STATE_OBJECTS:
                        print("entered object state")
                        objects = character.retrieveObjects()
                        attack_index = clamp_index(attack_index, len(objects) + 1)
                        if attack_index == len(character.retrieveObjects()):
                            if inCombat:
                                current_state = STATE_COMBAT
                            elif inCombatBoss:
                                current_state = STATE_ATTACKBOSS
                            else:
                                current_state = STATE_EXPLORE
                        else:
                            cmd_text = f"Using {character.retrieveObjects()[attack_index]}"
                            print(f"Using {character.retrieveObjects()[attack_index]}")
                            NomPotion = str(str(character.retrieveObjects()[attack_index]).split(' : ')[0])
                            obj = ClassObjets()
                            effet = obj.GetEffect(NomPotion, character, donjon, current_state, inCombatBoss)
                            if effet is not None:
                                current_state = effet
                            character.objets[NomPotion] -= 1
                            # Show "Using X" for 3s then continue
                            pending_state = current_state
                            pending_cmd   = cmd_text
                            pending_event = gameEvent
                            set_timer(3)
                            current_state = STATE_PENDING
                    elif current_state == STATE_INVENTORY:
                        print("entered inventory state")
                        attack_index = clamp_index(attack_index, len(character.weapons) + 1)
                        print("weapons:", character.weapons)
                        if attack_index == len(character.weapons):
                            if inCombat:
                                current_state = STATE_COMBAT
                            elif inCombatBoss:
                                current_state = STATE_ATTACKBOSS
                            else:
                                current_state = STATE_EXPLORE
                        else:
                            cmd_text = f"Equipping {chest_object_name(character.weapons[attack_index])}"
                            print(f"Equipping {chest_object_name(character.weapons[attack_index])}")
                            character.arme = str(chest_object_name(character.weapons[attack_index]))
                            pending_state = current_state
                            pending_cmd   = cmd_text
                            pending_event = gameEvent
                            set_timer(3)
                            current_state = STATE_PENDING
                        
                    elif current_state == STATE_CHEST:
                        # looting a chest
                        if attack_index == 0:
                            looting = True
                            while looting:
                                loot = chest_loot()
                                gameEvent = f"YOU FOUND {chest_object_name(loot)}"
                                print(f"YOU FOUND {chest_object_name(loot)}, {loot}")
                                if loot == 8:
                                    character.Or += 10
                                    looting = False
                                elif loot == 9:
                                    current_state = STATE_COMBAT
                                    looting = False
                                # looting a weapon
                                elif 10 < loot < 15:
                                    character.weapons.append(loot)
                                    looting = False
                                else:
                                    try:
                                        character.objets[names_select(loot)] += 1
                                        looting = False
                                        print(character.objets)
                                    except:
                                        pass
                                current_state = STATE_EVENT
                        # leaving chest closed
                        elif attack_index == 1:
                            current_state = STATE_EVENT

                    elif current_state == STATE_COMBAT:
                        inCombat = True
                        if attack_index == 0:
                            current_state = STATE_ATTACK
                        # run away from fight
                        elif attack_index == 1:
                            print("run")
                            current_state = STATE_RUN
                        # see possessed object
                        elif attack_index == 2:
                            print("object")
                            cancel_voice()
                            current_state = STATE_OBJECTS
                            attack_index = 0
                        # dodge an attack
                        elif attack_index == 3:
                            print("esquive")
                            current_state = STATE_ESQUIVE
                        # tank the attack
                        elif attack_index == 4:
                            print("tank")
                            current_state = STATE_TANK

                    # Boss fight
                    elif current_state == STATE_COMBATBOSS:
                        inCombatBoss = True
                        # attack the boss
                        if attack_index == 0:
                            current_state = STATE_ATTACKBOSS
                        # dodge attack
                        elif attack_index == 1:
                            print("duck")
                            current_state = STATE_ESQUIVEBOSS
                        # see possessed object
                        elif attack_index == 2:
                            print("object")
                            current_state = STATE_OBJECTS
                            attack_index = 0

        # hide mic icon in skill menu
        elif current_state != STATE_SKILLS:
            screen.blit(MuteMic, (800-220/2-10, 600-236/2-10))

        # display game layout
        if current_state != STATE_SKILLS:
            game_surface = render_game(character, gameEvent, cmd_text, donjon, current_state, TERMINAL_GREEN)
            screen.blit(game_surface, (0, 0))
            if micOpen: screen.blit(OpenMic, (800-234/2-50, 600-246/2-20))
            else: screen.blit(MuteMic, (800-220/2-53, 600-236/2-23))
                
        # draw current room layout
        if inShop == False and current_state != STATE_SKILLS:
            draw_perspective_brick_wall(screen)
        else:
            pass

        # show boss health bar
        if hp_boss > 0 and not GameOver:
            pygame.draw.rect(screen, TERMINAL_GREEN, pygame.Rect(50+16, 80, 350+16, 90-40))  
            pygame.draw.rect(screen, (0,0,0), pygame.Rect(52+16, 82, 346+16, 86-40)) 
            boss_life = round(hp_boss/hp_max_boss*354)
            pygame.draw.rect(screen, TERMINAL_GREEN, pygame.Rect(56+16, 86, boss_life, 78-40)) 
            pygame.display.flip()
        
        #show skeleton gif
        if current_state == STATE_COMBAT and not GameOver:
            skeleton_gif.render(screen, (50+(DUNGEON_PREVIEW_DIMENSIONS[0] - skeleton_gif.get_width())/2, 100+(DUNGEON_PREVIEW_DIMENSIONS[1] - skeleton_gif.get_height())/2))

        # displaying the game over screen
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

    if not running:
        break