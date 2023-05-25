import colorsys
import math
import random
import sys
import time

import pygame
from pygame import mixer
from pygame.locals import *

from background import Background
from button import Button
from dreamis import Dreamis
from player import Player
from utils import checkCollisions
from utils import clamp
from morkovka import Morkovka


def main():
    pygame.init()
    DISPLAY = pygame.display.set_mode((853, 480), 0, 32)
    pygame.display.set_caption('Барсик')
    pygame.display.set_icon(Dreamis().sprite)
    font = pygame.font.Font('data/fonts/font.otf', 100)
    font_small = pygame.font.Font('data/fonts/font.otf', 32)
    font_20 = pygame.font.Font('data/fonts/font.otf', 20)
    shop = pygame.image.load('data/gfx/shop.png')
    shop_bg = pygame.image.load('data/gfx/shop_bg.png')
    retry_button = pygame.image.load('data/gfx/retry_button.png')
    logo = pygame.image.load('data/gfx/logo.png')
    title_bg = pygame.image.load('data/gfx/bg.png')
    title_bg.fill((255, 30.599999999999998, 0.0), special_flags=pygame.BLEND_ADD)
    shadow = pygame.image.load('data/gfx/shadow.png')
    jumpfx = pygame.mixer.Sound("data/sfx/jump.wav")
    upgradefx = pygame.mixer.Sound("data/sfx/upgrade.wav")
    dreamisfx = pygame.mixer.Sound("data/sfx/dream.wav")
    morkvsfx = pygame.mixer.Sound("data/sfx/morkv.wav")
    deadfx = pygame.mixer.Sound("data/sfx/dead.wav")
    morkovka = Morkovka()
    WHITE = (255, 255, 255)
    rotOffset = -5
    player = Player()
    dreamis = []
    morkovka = []
    buttons = []
    for i in range(3): buttons.append(Button())
    buttons[0].typeIndicatorSprite = pygame.image.load('data/gfx/jump_indicator.png')
    buttons[0].price = 5
    buttons[1].typeIndicatorSprite = pygame.image.load('data/gfx/speed_indicator.png')
    buttons[1].price = 5
    buttons[2].typeIndicatorSprite = pygame.image.load('data/gfx/dreamup_indicator.png')
    buttons[2].price = 30
    for i in range(5): dreamis.append(Dreamis())
    for dream in dreamis:
        dream.position.xy = random.randrange(0, DISPLAY.get_width() - dream.sprite.get_width()), dreamis.index(
            dream) * -200 - player.position.y
    for i in range(2): morkovka.append(Morkovka())
    for morkva in morkovka:
        morkva.position.xy = random.randrange(0, DISPLAY.get_width() - morkva.sprite.get_width()), morkovka.index(morkva) * -200 - player.position.y
    bg = [Background(), Background(), Background()]
    dreamCount = 0
    startingHeight = player.position.y
    height = 0
    health = 125
    jump_force = 3
    dreamMultiplier = 5
    dead = False
    framerate = 60
    last_time = time.time()
    splashScreenTimer = 0
    pygame.mixer.Sound.play(jumpfx)
    while splashScreenTimer < 100:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        splashScreenTimer += dt
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        DISPLAY.fill((231, 205, 183))
        startMessage = font_small.render("Дмитрий Шекуров", True, (171, 145, 123))
        DISPLAY.blit(startMessage, (DISPLAY.get_width() / 2 - startMessage.get_width() / 2,
                                    DISPLAY.get_height() / 2 - startMessage.get_height() / 2))
        pygame.display.update()
        pygame.time.delay(10)

    titleScreen = True
    pygame.mixer.Sound.play(jumpfx)
    while titleScreen:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        mouseX, mouseY = pygame.mouse.get_pos()
        clicked = False
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if (clicked and checkCollisions(mouseX, mouseY, 3, 3, DISPLAY.get_width() / 2 - retry_button.get_width() / 2,
                                        288, retry_button.get_width(), retry_button.get_height())):
            clicked = False
            pygame.mixer.Sound.play(upgradefx)
            titleScreen = False

        DISPLAY.fill(WHITE)
        DISPLAY.blit(title_bg, (0, 0))
        DISPLAY.blit(shadow, (0, 0))
        DISPLAY.blit(logo, (DISPLAY.get_width() / 2 - logo.get_width() / 2,
                            DISPLAY.get_height() / 2 - logo.get_height() / 2 + math.sin(time.time() * 5) * 5 - 25))
        DISPLAY.blit(retry_button, (DISPLAY.get_width() / 2 - retry_button.get_width() / 2, 288))
        startMessage = font_small.render("СТАРТ", True, (0, 0, 0))
        DISPLAY.blit(startMessage, (DISPLAY.get_width() / 2 - startMessage.get_width() / 2, 292))

        pygame.display.update()
        pygame.time.delay(10)

    mixer.init()
    mixer.music.load('data/sfx/BARSIKNMMAS.wav')
    mixer.music.play(loops=-1)

    while True:
        dt = time.time() - last_time
        dt *= 60
        last_time = time.time()
        mouseX, mouseY = pygame.mouse.get_pos()
        jump = False
        clicked = False
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                jump = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
            if clicked and mouseY < DISPLAY.get_height() - 90:
                jump = True
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        camOffset = -player.position.y + DISPLAY.get_height() / 2 - player.currentSprite.get_size()[1] / 2

        DISPLAY.fill(WHITE)
        for o in bg:
            o.setSprite(((player.position.y / 50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))

        color = colorsys.hsv_to_rgb(((player.position.y / 50) % 100) / 100, 0.5, 0.5)
        currentHeightMarker = font.render(str(height), True, (color[0] * 255, color[1] * 255, color[2] * 255, 50))
        DISPLAY.blit(currentHeightMarker, (DISPLAY.get_width() / 2 - currentHeightMarker.get_width() / 2,
                                           camOffset + round((
                                                                     player.position.y - startingHeight) / DISPLAY.get_height()) * DISPLAY.get_height() + player.currentSprite.get_height() - 40))

        for dream in dreamis:
            DISPLAY.blit(dream.sprite, (dream.position.x, dream.position.y + camOffset))
        for morkva in morkovka:
            DISPLAY.blit(morkva.sprite, (morkva.position.x, morkva.position.y + camOffset))

        DISPLAY.blit(pygame.transform.rotate(player.currentSprite, clamp(player.velocity.y, -10, 5) * rotOffset),
                     (player.position.x, player.position.y + camOffset))
        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY, (16, 209, 2), (21, 437, 150 * (health / 125), 25))
        DISPLAY.blit(shop, (0, 0))

        for button in buttons:
            DISPLAY.blit(button.sprite, (220 + (buttons.index(button) * 125), 393))
            priceDisplay = font_small.render(str(button.price), True, (0, 0, 0))
            DISPLAY.blit(priceDisplay, (262 + (buttons.index(button) * 125), 408))
            levelDisplay = font_20.render('Лвл. ' + str(button.level), True, (200, 200, 200))
            DISPLAY.blit(levelDisplay, (234 + (buttons.index(button) * 125), 441))
            DISPLAY.blit(button.typeIndicatorSprite, (202 + (buttons.index(button) * 125), 377))
        dreamCountDisplay = font_small.render(str(dreamCount).zfill(7), True, (0, 0, 0))
        DISPLAY.blit(dreamCountDisplay, (72, 394))
        if dead:
            DISPLAY.blit(retry_button, (4, 4))
            deathMessage = font_small.render("RETRY", True, (0, 0, 0))
            DISPLAY.blit(deathMessage, (24, 8))

        height = round(-(player.position.y - startingHeight) / DISPLAY.get_height())

        player.position.x += player.velocity.x * dt
        if player.position.x + player.currentSprite.get_size()[0] > 853:
            player.velocity.x = -abs(player.velocity.x)
            player.currentSprite = player.leftSprite
            rotOffset = 5
        if player.position.x < 0:
            player.velocity.x = abs(player.velocity.x)
            player.currentSprite = player.rightSprite
            rotOffset = -5
        if jump and not dead:
            player.velocity.y = -jump_force
            pygame.mixer.Sound.play(jumpfx)
        player.position.y += player.velocity.y * dt
        player.velocity.y = clamp(player.velocity.y + player.acceleration * dt, -99999999999, 50)

        health -= 0.2 * dt
        if health <= 0 and not dead:
            dead = True
            pygame.mixer.Sound.play(deadfx)

        for morkva in morkovka:
            if morkva.position.y + camOffset + 90 > DISPLAY.get_height():
                morkva.position.y -= DISPLAY.get_height() * 2
                morkva.position.x = random.randrange(0, DISPLAY.get_width() - morkva.sprite.get_width())
            if (checkCollisions(player.position.x, player.position.y, player.currentSprite.get_width(),
                               player.currentSprite.get_height(), morkva.position.x, morkva.position.y,
                               morkva.sprite.get_width(), morkva.sprite.get_height())):

                dead = False
                pygame.mixer.Sound.play(morkvsfx)
                if dreamCount > 0 and dreamCount != 0:
                    dreamCount -= 1
                else:
                    health = health - 25
                morkva.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                morkva.position.x = random.randrange(0, DISPLAY.get_width() - morkva.sprite.get_width())

        for dream in dreamis:
            if dream.position.y + camOffset + 90 > DISPLAY.get_height():
                dream.position.y -= DISPLAY.get_height() * 2
                dream.position.x = random.randrange(0, DISPLAY.get_width() - dream.sprite.get_width())
            if checkCollisions(player.position.x, player.position.y, player.currentSprite.get_width(),
                               player.currentSprite.get_height(), dream.position.x, dream.position.y,

                               dream.sprite.get_width(), dream.sprite.get_height()):
                dead = False
                pygame.mixer.Sound.play(dreamisfx)
                dreamCount += 1
                health = 125
                dream.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                dream.position.x = random.randrange(0, DISPLAY.get_width() - dream.sprite.get_width())

        for button in buttons:
            buttonX, buttonY = 220 + (buttons.index(button) * 125), 393
            if clicked and not dead and checkCollisions(mouseX, mouseY, 3, 3, buttonX, buttonY,
                                                        button.sprite.get_width(), button.sprite.get_height()):
                if (dreamCount >= button.price):
                    pygame.mixer.Sound.play(upgradefx)
                    button.level += 1
                    dreamCount -= button.price
                    button.price = round(button.price * 2.5)
                    if (buttons.index(button) == 0):
                        jump_force *= 1.5
                    if (buttons.index(button) == 1):
                        player.velocity.x *= 1.5
                    if (buttons.index(button) == 2):
                        olddreamMultipler = dreamMultiplier
                        dreamMultiplier += 10
                        for i in range(dreamMultiplier):
                            dreamis.append(Dreamis())
                            dreamis[-1].position.xy = random.randrange(0,
                                                                       DISPLAY.get_width() - dream.sprite.get_width()), player.position.y - DISPLAY.get_height() - random.randrange(
                                0, 200)

        if dead and clicked and checkCollisions(mouseX, mouseY, 3, 3, 4, 4, retry_button.get_width(),
                                                retry_button.get_height()):
            health = 125
            player.velocity.xy = 3, 0
            player.position.xy = 295, 100
            player.currentSprite = player.rightSprite
            dreamCount = 0
            height = 0
            jump_force = 3
            dreamMultiplier = 5
            buttons = []
            for i in range(3): buttons.append(Button())
            buttons[0].typeIndicatorSprite = pygame.image.load('data/gfx/jump_indicator.png')
            buttons[0].price = 5
            buttons[1].typeIndicatorSprite = pygame.image.load('data/gfx/speed_indicator.png')
            buttons[1].price = 5
            buttons[2].typeIndicatorSprite = pygame.image.load('data/gfx/dreamup_indicator.png')
            buttons[2].price = 30
            dreamis = []
            for i in range(5): dreamis.append(Dreamis())
            for dream in dreamis:
                dream.position.xy = random.randrange(0, DISPLAY.get_width() - dream.sprite.get_width()), dreamis.index(
                    dream) * -200 - player.position.y
            pygame.mixer.Sound.play(upgradefx)
            dead = False

        bg[0].position = camOffset + round(player.position.y / DISPLAY.get_height()) * DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height()
        bg[2].position = bg[0].position - DISPLAY.get_height()

        pygame.display.update()
        pygame.time.delay(10)


if __name__ == "__main__":
    main()
