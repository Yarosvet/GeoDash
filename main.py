#!/usr/bin/env/python
# import pygame
# import os
import sys
# local
from config import *
import level_1

images = pygame.sprite.Group()
background = Sprite(images, pygame.transform.scale(load_image("menu_background.png"), size))
play = AnimatedSprite(images, load_image("play.png"), 1, 2, 310, 290)
logo = Sprite(images, load_image("logo.png"))
logo.update(185, 10)
clck = pygame.time.Clock()
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONUP and event.button in [1, 2]:
            if play.rect.collidepoint(*event.pos):
                for spr in images:
                    spr.kill()
                level_1.build_level('data/level_1.txt')

    clck.tick(6)
    play.update()
    images.draw(screen)
    pygame.display.flip()
