import random as rnd
from time import sleep
import sys
import pygame as pg

# Initialization
pg.mixer.pre_init(44100,-16,2,512)
pg.init()
WIN_WIDTH = 800
WIN_HEIGHT = 600
window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption('Hangman')

# Constants
FPS = 25
XPOS = 20
YPOS = 20
Y_OFFSET = 26
GRAY = 64
BG_PLAYFIELD = pg.Color(GRAY, GRAY, GRAY, 240)
BG_COLOR = (0,191,255)
FONT_COLOR = pg.Color("black")
BG_FONT = pg.Color(0, 191, 255, 220)
TEXTFONT = pg.font.SysFont('comic sans', 20)
# BACKGROUND = pg.image.load('kaffeetasse.jpg', 'mainnbg').convert_alpha()
# BG_RECT = BACKGROUND.get_rect()
# CLOUD_BG = pg.image.load('onlyclouds.png', 'cloudbg').convert_alpha()
# CLOUD_BG_RECT = CLOUD_BG.get_rect()
# BG_BOTTOM = pg.image.load('ground.png', 'groundbg').convert_alpha()
# GROUND_RECT = BG_BOTTOM.get_rect()
PHOTO_BG = pg.image.load('wolken800x600.jpg', 'wolkenbg').convert_alpha()
PHOTO_BG_RECT = PHOTO_BG.get_rect()
GALGEN = [pg.image.load(f"galgen1{nr:d}.png").convert_alpha() for nr in range(1,9)]
GALGEN_RECT = pg.rect.Rect(0,0,250,300)

# Variables
clock = pg.time.Clock()
game_over = False
new_game = True
eingabe = None
versuche = 0
text_bisher = ""

def drawtext(x: int, y: int, text: str, color = FONT_COLOR) -> None:
    output = TEXTFONT.render(text, True, FONT_COLOR, BG_FONT)
    output_rect = output.get_rect()
    window.blit(output, (x, y), output_rect, pg.BLEND_PREMULTIPLIED) # BLEND_RGBA_ADD

while True:
    clock.tick(FPS)

    # Draw Background
    window.fill(BG_COLOR)
    # for x in range(9):
    #     for y in range(2):
    #         window.blit(BACKGROUND,(x*100,y*100), BG_RECT)
    # window.blit(CLOUD_BG,(0,200), CLOUD_BG_RECT)
    # window.blit(BG_BOTTOM,(0,WIN_HEIGHT - GROUND_RECT.height // 2), GROUND_RECT)
    window.blit(PHOTO_BG,(0,0), PHOTO_BG_RECT)

    # Get Player Input
    for event in pg.event.get():
        if event.type == pg.QUIT or \
            (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if isinstance(event.key, int):
                if pg.K_a <= event.key <= pg.K_z:
                    eingabe = chr(event.key).upper()
                    if not game_over:
                        geraten.add(eingabe)
                        if eingabe not in gesucht: versuche -= 1
                        if gesucht.issubset(geraten):
                            text_bisher = " ".join([f"{b if b in geraten else '_'}" for b in wort])
                            drawtext(XPOS, YPOS + Y_OFFSET * 3, text_bisher)
                            game_over = True
                    else:
                        if eingabe == chr(pg.K_n).upper():
                            pg.quit()
                            sys.exit()
                        elif eingabe == chr(pg.K_j).upper():
                            game_over = False
                            new_game = True

    # Draw Playfield
    playfield = pg.Surface((WIN_WIDTH - 20, 175))
    pg.draw.rect(playfield, BG_PLAYFIELD, rect=(0, 0, playfield.get_width(), 175), border_radius=10)
    window.blit(playfield, (XPOS - 10, YPOS - 10), playfield.get_rect(), pg.BLEND_RGBA_SUB) # pg.BLEND_PREMULTIPLIED)

    if new_game:
        with open("lexikon.txt", "r") as f:
            wort = rnd.choice([w.strip().upper() for w in f])
        versuche, gesucht, geraten = 8, set(b for b in wort), set()
        new_game = False
    elif versuche > 0 and not game_over:
        drawtext(XPOS, YPOS, f"Ihre Buchstaben bisher: {','.join([b for b in geraten])}")
        text = f"Noch {versuche:>2} Versuche: "
        text += " ".join([f"{b if b in geraten else '_'}" for b in wort])
        drawtext(XPOS, YPOS + Y_OFFSET * 2, text)
        drawtext(XPOS, YPOS + Y_OFFSET * 4, "Ihr Buchstabe?")
    else:
        game_over = True
        text = "GEWONNEN! " if versuche > 0 else "VERLOREN! "
        drawtext(XPOS, YPOS, text)
        text = f"Das gesuchte Wort war {wort.lower().capitalize()}"
        drawtext(XPOS, YPOS + Y_OFFSET, text)
        if gesucht.issubset(geraten):
            drawtext(XPOS, YPOS + Y_OFFSET * 4, f"Du hast {8-versuche} Versuche benötigt - Nochmal raten?")
        else:
            text_bisher = " ".join([f"{b if b in geraten else '_'}" for b in wort])
            drawtext(XPOS, YPOS + int(Y_OFFSET * 2.5), f"und Du hattest bisher {text_bisher}!")
            drawtext(XPOS, YPOS + Y_OFFSET * 4, "Das war's dann wohl! Du hängst leider. - Nochmal raten?")

    if versuche < 8:
        window.blit(GALGEN[7 - versuche], (280,250), GALGEN_RECT)

    pg.display.update()
