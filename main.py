import asyncio
import colorsys
import math
import random
import sys
import time

import pygame
import pygame.display as Display
from pygame import mixer
from pygame.locals import *
from pygame.mixer import Sound

from background import Background
from button import Button
from dreamis import Dreamis
from morkovka import Morkovka
from player import Player
from utils import *

pygame.init()
Display.set_caption('Барсик')
Display.set_icon(Dreamis.sprite)
DISPLAY = Display.set_mode((640, 480), pygame.RESIZABLE | pygame.SCALED, 32)
player = Player()
morkovka = Morkovka()
player = Player()
jumpfx = Sound("data/sfx/jump.wav")
indicators = ['data/gfx/jump_indicator.png', 'data/gfx/speed_indicator.png', 'data/gfx/dreamup_indicator.png']
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
if ['win64', 'win32', 'win', 'linux'].__contains__(sys.platform):
    sound_ext = '.wav'
else:
    sound_ext = '-pybag.ogg'
jumpfx = pygame.mixer.Sound("data/sfx/jump" + sound_ext)
upgradefx = pygame.mixer.Sound("data/sfx/upgrade" + sound_ext)
dreamisfx = pygame.mixer.Sound("data/sfx/dream" + sound_ext)
morkvsfx = pygame.mixer.Sound("Data/sfx/morkv.wav")
deadfx = pygame.mixer.Sound("data/sfx/dead" + sound_ext)

WHITE = (255, 255, 255)


def start():
    global dream_multiplier, dreamis, morkovka, morkva, buttons, last_time, clicked, jump, dt, mouse_x, mouse_y, scroll
    last_time = time.time()
    clicked = False
    jump = False
    scroll = True
    dream_multiplier = 5
    dt = 0
    dreamis = []
    morkovka = []
    buttons = []
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.reset()

    for i in range(3):
        buttons.append(Button(i, indicators[i]))
    buttons[2].set_price(30)

    for _ in range(5):
        dreamis.append(Dreamis())
    for i in range(5):
        dreamis.append(Dreamis(random.randrange(0, DISPLAY.get_width() - Dreamis().sprite.get_width()),
                               i * -200 - player.position.y))
    Sound.play(jumpfx)

    for _ in range(2):
        morkovka.append(Morkovka())
    for morkva in morkovka:
        morkva.position.xy = random.randrange(0, DISPLAY.get_width() - morkva.sprite.get_width()), morkovka.index(
            morkva) * -200 - player.position.y
    pygame.mixer.Sound.play(jumpfx)


def func_one(toggle: bool = True) -> None:
    global dt, last_time, mouse_x, mouse_y, clicked, jump
    dt = (time.time() - last_time) * 60
    last_time = time.time()
    if (toggle):
        clicked = jump = False
        clicked = False
        jump = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
    event_handler()


def event_handler() -> None:
    global jump, clicked
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == K_SPACE:
            jump = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True
        if clicked and mouse_y < DISPLAY.get_height() - 90:
            jump = True
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


async def main() -> None:
    global clicked, dream_multiplier, dreamis, scroll

    start()

    bg = [Background(), Background(), Background()]
    starting_height = player.position.y
    splash_screen_timer = 0
    while splash_screen_timer < 100:
        func_one(False)
        splash_screen_timer += dt
        DISPLAY.fill((231, 205, 183))
        start_message = font_small.render("Дмитрий Шекуров", True, (171, 145, 123))
        DISPLAY.blit(start_message, (DISPLAY.get_width() / 2 - start_message.get_width() / 2,
                                     DISPLAY.get_height() / 2 - start_message.get_height() / 2))
        Display.update()
        await asyncio.sleep(0)
        pygame.time.delay(10)

    title_screen = True
    Sound.play(jumpfx)
    while title_screen:
        func_one()
        if (clicked and check_collisions(mouse_x, mouse_y, 3, 3, DISPLAY.get_width() / 2 - retry_button.get_width() / 2,
                                         288, retry_button.get_width(), retry_button.get_height())):
            clicked = False
            Sound.play(upgradefx)
            title_screen = False

        DISPLAY.fill(WHITE)
        DISPLAY.blit(title_bg, (0, 0))
        DISPLAY.blit(shadow, (0, 0))
        DISPLAY.blit(logo, (DISPLAY.get_width() / 2 - logo.get_width() / 2,
                            DISPLAY.get_height() / 2 - logo.get_height() / 2 + math.sin(time.time() * 5) * 5 - 25))
        DISPLAY.blit(retry_button, (DISPLAY.get_width() / 2 - retry_button.get_width() / 2, 288))
        start_message = font_small.render("СТАРТ", True, (0, 0, 0))
        DISPLAY.blit(start_message, (DISPLAY.get_width() / 2 - start_message.get_width() / 2, 292))

        Display.update()
        await asyncio.sleep(0)
        pygame.time.delay(10)

    mixer.init()
    mixer.music.load('data/sfx/BARSIKNMMAS.wav')
    mixer.music.play(loops=-1)

    while True:
        func_one()

        cam_offset = -player.position.y + (DISPLAY.get_height() - player.current_sprite.get_size()[1]) / 2
        if (cam_offset <= 0):
            if (not player.dead):
                player.kill(deadfx)
            scroll = False
            cam_offset = 0

        DISPLAY.fill(WHITE)
        for o in bg:
            o.set_sprite(((player.position.y / 50) % 100) / 100)
            o.set_sprite(((player.position.y / 50) % 100) / 100)
            DISPLAY.blit(o.sprite, (0, o.position))
        color = colorsys.hsv_to_rgb(((player.position.y / 50) % 100) / 100, 0.5, 0.5)
        current_height_marker = font.render(str(player.height), True,
                                            (color[0] * 255, color[1] * 255, color[2] * 255, 50))
        DISPLAY.blit(current_height_marker, (DISPLAY.get_width() / 2 - current_height_marker.get_width() / 2,
                                             cam_offset + round((
                                                                            player.position.y - starting_height) / DISPLAY.get_height()) * DISPLAY.get_height() + player.current_sprite.get_height() - 40))

        for dream in dreamis:
            DISPLAY.blit(dream.sprite, (dream.position.x, dream.position.y + cam_offset))
        for morkva in morkovka:
            if morkva in dreamis:
                dreamis.remove(morkva)
            else:
                DISPLAY.blit(morkva.sprite, (morkva.position.x, morkva.position.y + cam_offset))

        DISPLAY.blit(
            pygame.transform.rotate(player.current_sprite, clamp(player.velocity.y, -10, 5) * player.rot_offset),
            (player.position.x, player.position.y + cam_offset))
        DISPLAY.blit(shop_bg, (0, 0))
        pygame.draw.rect(DISPLAY, (16, 209, 2), (21, 437, 150 * (player.health / 100), 25))
        DISPLAY.blit(shop, (0, 0))

        for button in buttons:
            DISPLAY.blit(button.sprite, (220 + (button.index * 125), 393))
            price_display = font_small.render(str(button.price), True, (0, 0, 0))
            DISPLAY.blit(price_display, (262 + (button.index * 125), 408))
            level_display = font_20.render(f'Lvl. {button.level}', True, (200, 200, 200))
            DISPLAY.blit(level_display, (234 + (button.index * 125), 441))
            DISPLAY.blit(button.type_indicator_sprite, (202 + (button.index * 125), 377))
        bean_count_display = font_small.render(str(player.dream_count).zfill(7), True, (0, 0, 0))
        DISPLAY.blit(bean_count_display, (72, 394))
        if player.dead:
            DISPLAY.blit(retry_button, (4, 4))
            death_message = font_small.render("RETRY", True, (0, 0, 0))
            DISPLAY.blit(death_message, (24, 8))

        if (scroll):
            player.set_height(round(-(player.position.y - starting_height) / DISPLAY.get_height()))
            player.position.x += player.velocity.x * dt
            if player.position.x < 0 or player.position.x + player.current_sprite.get_size()[0] > 640:
                player.flip()
            if jump and not player.dead:
                player.velocity.y = -player.jump_force
                Sound.play(jumpfx)
            player.position.y += player.velocity.y * dt
            player.velocity.y = clamp(player.velocity.y + player.acceleration * dt, -99999999999, 50)

        if not player.dead:
            player.health -= 0.2 * dt
            if player.health <= 0:
                player.kill(deadfx)

        for morkva in morkovka:
            if morkva.position.y + cam_offset + 90 > DISPLAY.get_height():
                morkva.position.y -= DISPLAY.get_height() * 2
                morkva.position.x = random.randrange(0, DISPLAY.get_width() - morkva.sprite.get_width())
            if (check_collisions(player.position.x, player.position.y, player.current_sprite.get_width(),
                                 player.current_sprite.get_height(), morkva.position.x, morkva.position.y,
                                 morkva.sprite.get_width(), morkva.sprite.get_height())):

                Sound.play(morkvsfx)
                if player.dream_count > 0 and player.dream_count != 0:
                    player.dream_count -= 1
                else:
                    player.health = player.health - 25
                morkva.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                morkva.position.x = random.randrange(0, DISPLAY.get_width() - morkva.sprite.get_width())

        for dream in dreamis:
            if dream.position.y + cam_offset + 90 > DISPLAY.get_height():
                dream.position.y -= DISPLAY.get_height() * 2
                dream.position.x = random.randrange(0, DISPLAY.get_width() - dream.sprite.get_width())
            if (check_collisions(player.position.x, player.position.y, player.current_sprite.get_width(),
                                 player.current_sprite.get_height(), dream.position.x, dream.position.y,

                                 dream.sprite.get_width(), dream.sprite.get_height())):
                Sound.play(dreamisfx)
                player.dream_count += 1
                player.health = 100
                dream.position.y -= DISPLAY.get_height() - random.randrange(0, 200)
                dream.position.x = random.randrange(0, DISPLAY.get_width() - dream.sprite.get_width())

        for button in buttons:
            if clicked and not player.dead and check_collisions(mouse_x, mouse_y, 3, 3, button.position.x,
                                                                button.position.y, button.sprite.get_width(),
                                                                button.sprite.get_height()):
                if (player.dream_count >= button.price):
                    Sound.play(upgradefx)
                    button.level += 1
                    player.dream_count -= button.price
                    button.price = round(button.price * 2.5)
                    if (button.index == 0):
                        player.jump_force *= 1.5
                    if (button.index == 1):
                        player.velocity.x *= 1.5
                    if (button.index == 2):
                        dream_multiplier += 5
                        for _ in range(dream_multiplier):
                            dreamis.append(
                                Dreamis(random.randrange(0, DISPLAY.get_width() - Dreamis().sprite.get_width()),
                                        player.position.y - DISPLAY.get_height() - random.randrange(0, 200)))

        if player.dead and clicked and check_collisions(mouse_x, mouse_y, 3, 3, 4, 4, retry_button.get_width(),
                                                        retry_button.get_height()):
            start()

        bg[0].position = cam_offset + round(player.position.y / DISPLAY.get_height()) * DISPLAY.get_height()
        bg[1].position = bg[0].position + DISPLAY.get_height()
        bg[2].position = bg[0].position - DISPLAY.get_height()

        Display.update()
        await asyncio.sleep(0)
        pygame.time.delay(10)


if __name__ == "__main__":
    asyncio.run(main())
