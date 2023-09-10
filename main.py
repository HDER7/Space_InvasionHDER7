import pygame
import random
import math
from pygame import mixer

# Start pygame library and show screen
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Musica
mixer.music.load('uuuuu.mp3')
mixer.music.set_volume(1)
mixer.music.play(-1)

# Put the title, icon and wallpaper
pygame.display.set_caption('Space Invasion by HDER7')
icon = pygame.image.load("asteroide.png")
pygame.display.set_icon(icon)
wallpaper = pygame.image.load('earth.jpg')

# Spacecraft
spacecraft = pygame.image.load("astronave.png")
pos_x = 368  # (800/2) - spacecraft_size
pos_y = 520  # 600 - spacecraft_size
change_x = 0


def player(x, y):
    screen.blit(spacecraft, (x, y))


# Enemies
enemy = []
pos_x_e = []
pos_y_e = []
change_x_e = []
change_y_e = []
n_enemies = 8
for e in range(n_enemies):
    enemy.append(pygame.image.load("bad.png"))
    pos_x_e.append(random.randint(0, 736))
    pos_y_e.append(random.randint(50, 200))
    change_x_e.append(0.5)
    change_y_e.append(50)


def enemies(x, y, ene):
    screen.blit(enemy[ene], (x, y))


# Blast
blasts = []
blast = pygame.image.load("misil.png")
pos_x_b = 0
pos_y_b = 520
change_x_b = 0
change_y_b = 2
blast_visible = False


def bullet(x, y):
    global blast_visible
    blast_visible = True
    screen.blit(blast, (x + 16, y + 10))


# Kick enemy
def kick(x1, x2, y1, y2):
    cal_x = math.pow((x2-x1), 2)
    cal_y = math.pow((y2 - y1), 2)
    distance = math.sqrt(cal_x + cal_y)
    if distance < 27:
        return True
    else:
        return False


# Points in screen
point = 0
font = pygame.font.Font('STJEDISE.TTF', 32)
text_x = 10
text_y = 10


def points(x, y):
    text = font.render(f"Points: {point}", True, (255, 255, 255))
    screen.blit(text, (x, y))


final = pygame.font.Font('Starjhol.ttf', 90)


def game_over():
    over = final.render("GAME 0VER", True, (255, 255, 255))
    screen.blit(over, (110, 200))


# Screen show while don't close the window
run = True
while run:

    # Change the screen color and put the wallpaper
    screen.fill((6, 0, 98))
    screen.blit(wallpaper, (0, 0))

    for event in pygame.event.get():

        # Close window
        if event.type == pygame.QUIT:
            run = False

        # Move spacecraft and launch missile
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_x = -0.4
            if event.key == pygame.K_RIGHT:
                change_x = 0.4
            if event.key == pygame.K_SPACE:
                blast_s = mixer.Sound('SD_TOY_EXPLOSION.mp3')
                blast_s.set_volume(0.5)
                blast_s.play()
                nueva_bala = {
                    "x": pos_x,
                    "y": pos_y,
                    "speed": -5
                }
                blasts.append(nueva_bala)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_x = 0

    # spacecraft position and don't pass border
    pos_x += change_x
    player(pos_x, pos_y)
    if pos_x <= 0:
        pos_x = 0
    elif pos_x >= 736:
        pos_x = 736

    # Missile move
    for b in blasts:
        b["y"] += b["speed"]
        screen.blit(blast, (b["x"] + 16, b["y"] + 10))
        if b["y"] < 0:
            blasts.remove(b)
    if blast_visible:
        bullet(pos_x_b, pos_y_b)
        pos_y_b -= change_y_b

    # Enemies position
    for e in range(n_enemies):

        # Game Over
        if pos_y_e[e] > 470:
            for k in range(n_enemies):
                pos_y_e[k] = 1000
            game_over()

        pos_x_e[e] += change_x_e[e]
        enemies(pos_x_e[e], pos_y_e[e], e)
        if pos_x_e[e] <= 0:
            change_x_e[e] = 0.5
            pos_y_e[e] += change_y_e[e]
        elif pos_x_e[e] >= 736:
            change_x_e[e] = -0.5
            pos_y_e[e] += change_y_e[e]
        # Kick enemy
        for b in blasts:
            collision = kick(pos_x_e[e], b["x"], pos_y_e[e], b["y"])
            if collision:
                collision_s = mixer.Sound('explosion.mp3')
                collision_s.set_volume(0.1)
                collision_s.play()
                blasts.remove(b)
                point += 1
                pos_x_e[e] = random.randint(0, 736)
                pos_y_e[e] = random.randint(50, 200)
                blasts.clear()
                break
        enemies(pos_x_e[e], pos_y_e[e], e)
    points(text_x, text_y)
    pygame.display.update()
