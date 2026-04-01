import pygame as pg
import random

# --- CONFIGURATION ---
WIDTH, HEIGHT = 800, 600
FPS = 60
BLACK = (0, 0, 0)

# --- INITIALIZATION ---
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
# Use a monospaced font for that terminal look
font = pg.font.SysFont("Courier", 20, bold=True)
header_font = pg.font.SysFont("Courier", 32, bold=True)

def draw_scanlines(surface):
    """Draws thin horizontal lines to mimic a CRT monitor."""
    for y in range(0, HEIGHT, 3):
        pg.draw.line(surface, (0, 0, 0, 100), (0, y), (WIDTH, y))

def draw_vignette(surface):
    """Optional: adds a slight dark gradient to the corners."""
    vignette = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
    # Drawing a simplified vignette using a large circle or manual overlay
    # For a terminal feel, we'll just dim the edges slightly
    pg.draw.rect(vignette, (0, 0, 0, 50), (0, 0, WIDTH, HEIGHT), 20)
    surface.blit(vignette, (0, 0))

def render_game(player, evenement, cmd_text, donjon, current_state, TERMINAL_GREEN):
    # Create a buffer surface for the game world
    display_buffer = pg.Surface((WIDTH, HEIGHT))
    display_buffer.fill(BLACK)

    # 1. DRAW HEADER
    header_text = header_font.render(current_state, True, TERMINAL_GREEN)
    display_buffer.blit(header_text, (50, 20))
    pg.draw.line(display_buffer, TERMINAL_GREEN, (50, 60), (750, 60), 2)

    # 3. DRAW UI BOXES
    # Stats Box
    pg.draw.rect(display_buffer, TERMINAL_GREEN, (500, 100, 250, 300), 2)
    stats = [f"NAME: {player.name}", f"HP: {player.vie}/{player.viemax}", f"ATTAQUE {player.attack}", f"DEFENSE {player.defense}", f"AGILITE {player.agilite}", f"OR: {player.Or}", f"LEVEL: {donjon.level}", f"ARME: {player.arme}"]
    for i, text in enumerate(stats):
        stat_img = font.render(text, True, TERMINAL_GREEN)
        display_buffer.blit(stat_img, (520, 120 + (i * 25)))

    # 4. LOG AREA
    log_text = f"{evenement}"
    height = 460
    display_buffer.blit(font.render(log_text, True, TERMINAL_GREEN), (50, height))
    if len(str(cmd_text).split(" | ")) == 3:
        display_buffer.blit(font.render(str(cmd_text).split(" | ")[0], True, TERMINAL_GREEN), (50, height+30))
        display_buffer.blit(font.render(str(cmd_text).split(" | ")[1], True, TERMINAL_GREEN), (50, height+60))
        display_buffer.blit(font.render(str(cmd_text).split(" | ")[2], True, TERMINAL_GREEN), (50, height+90))
    else:
        display_buffer.blit(font.render(cmd_text, True, TERMINAL_GREEN), (50, height+30))

    # 5. APPLY CRT EFFECTS
    draw_scanlines(display_buffer)
    draw_vignette(display_buffer)
    
    return display_buffer