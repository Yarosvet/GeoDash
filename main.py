#!/usr/bin/env/python
# import pygame
# import os
import sys
# local
from config import *

images = pygame.sprite.Group()
background = Sprite(images, pygame.transform.scale(load_image("menu_background.png"), size))
play = AnimatedSprite(images, load_image("play.png"), 1, 2, 310, 290)
logo = Sprite(images, load_image("logo.png"))
logo.update(185, 10)
clock = pygame.time.Clock()
counter = 0


def define_character():
    global character
    for c in characters:
        character = c


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif state == 'logo':
            if event.type == pygame.MOUSEBUTTONUP and event.button in [1, 2]:
                if play.rect.collidepoint(*event.pos):
                    for spr in images:
                        spr.kill()
                    build_level('data/level_1.txt')
                    state = 'game'
    if state == 'game':
        print(1)
        #build_level('data/level_1.txt', True)
        print(0)
        define_character()
        character.update(character.rect.x + 1, character.rect.y)
        # cam.apply(character)
        # characters.draw(screen)

    clock.tick(60)
    if counter == 0:
        play.update()
        images.draw(screen)
    pygame.display.flip()
    counter += 1
    counter = counter % 10
