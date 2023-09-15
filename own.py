import pygame
from pygame import mixer
import math
import random


FPS = 60
WIDTH = 1200
HEIGHT = 450

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Super")
icon = pygame.image.load('champion-belt.png')
pygame.display.set_icon(icon)

mixer.music.load('moon.wav')
mixer.music.play(-1)

comet_img = pygame.image.load('comet.png')
cometX = random.randint(600, 1200)
cometY = random.randint(5, 445)
cometX_change = 0
cometY_change = 0

Hero_img = pygame.image.load('hero.png')
HeroX = 0
HeroY = 165
HeroX_change = 0
HeroY_change = 0

# laser
laser_img = pygame.image.load('laser.png')
laserX = HeroX
laserY = 0
laserX_change = 10
laserY_change = 0
laser_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 1000
textY = 380


def score(x, ys):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (textX, textY))


def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laser_img, (x + 16, y + 10))


def hero(x, y):
    screen.blit(Hero_img, (x, y))


def comet(x, y):
    screen.blit(comet_img, (x, y))


def laser_collision(cometX, cometY, laserX, laserY):
    distance_laser = math.sqrt((math.pow(cometX - laserX, 2)) + (math.pow(cometY - laserY, 2)))
    if distance_laser <= 75:
        return True
    else:
        return False


def comet_collision(x, y):
    if cometX <= -15:
        return True
    else:
        return False


def hero_collision(cometX, cometY, HeroX, HeroY):
    distance_hero = math.sqrt((math.pow(cometX - HeroX, 2)) + (math.pow(cometY - HeroY, 2)))
    if distance_hero <= 30:
        return True
    else:
        return False


running = True
while running:

    screen.fill((20, 200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                HeroY_change += 0.5
            if event.key == pygame.K_w:
                HeroY_change -= 0.5
            if event.key == pygame.K_a:
                HeroX_change -= 0.5
            if event.key == pygame.K_d:
                HeroX_change += 0.5
            if event.key == pygame.K_SPACE:
                if laser_state is "ready":
                    laserY = HeroY
                    fire_laser(laserX, laserY)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s or event.key == pygame.K_w or event.key == pygame.K_a or event.key == pygame.K_d:
                    HeroX_change = 0
                    HeroY_change = 0

    HeroX += HeroX_change
    HeroY += HeroY_change
    if HeroX >= 1072:
        HeroX = 1072
    if HeroX <= 0:
        HeroX = 0
    if HeroY >= 350:
        HeroY = 350
    if HeroY <= 0:
        HeroY = 0

    # laser movement
    if laserX >= 1200:
        laserX = HeroX
        laser_state = "ready"
    if laser_state is "fire":
        fire_laser(laserX, laserY)
        laserX += laserX_change

    if cometX >= -15:
        cometX -= 0.2

    collision_comet = comet_collision(cometX, cometY)
    if collision_comet:
        cometX = random.randint(600, 1200)
        cometY = random.randint(5, 445)

    collision_hero = hero_collision(cometX, cometY, HeroX, HeroY)
    # if collision_hero:

    collision_laser = laser_collision(cometX, cometY, laserX, laserY)
    if collision_laser:
        laserX = HeroX
        laser_state = "ready"
        score_value += 1
        cometX = random.randint(600, 1200)
        cometY = random.randint(5, 445)

    hero(HeroX, HeroY)
    comet(cometX, cometY)
    score(textX, textY)
    pygame.display.update()
