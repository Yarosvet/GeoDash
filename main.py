#!/usr/bin/env/python
import sys
import pygame
import os
# local
from Classes import *

# Переменные и константы
size = width, height = 800, 500
clock = pygame.time.Clock()
counter = 0
LEVEL_MUSIC = "data/BackOnTrack.mp3"
BLOCK_SIZE = 50
is_jumping = False
jump_counter = 0
JUMP_K = 5
K_FALL = 4
V = 4
FPS = 60
pos_character = 0
dead = False

# Группы спрайтов и объекты
images = pygame.sprite.Group()
platforms = pygame.sprite.Group()
DieBlocks = pygame.sprite.Group()
characters = pygame.sprite.Group()
level_menu = pygame.sprite.Group()
character = None
cam = Camera(width, height)

# Инициализация игры
screen = pygame.display.set_mode(size)
state = 'logo'
background = Sprite(images, pygame.transform.scale(load_image("menu_background.png"), size))
play = AnimatedSprite(images, load_image("play.png"), 1, 2, 310, 290)
logo = Sprite(images, load_image("logo.png"))
logo.update(185, 10)
# Музыка
pygame.mixer.init()
pygame.mixer.music.load('data/menuLoop.mp3')
pygame.mixer.music.play(-1)


def death():
    global background
    global play
    global state
    global dead
    for spr in level_menu:
        spr.kill()
    screen.fill((0, 0, 0))
    background = Sprite(images, pygame.transform.scale(load_image("menu_background.png"), size))
    play = AnimatedSprite(images, load_image("play.png"), 1, 2, 310, 290)
    logo = Sprite(images, load_image("logo.png"))
    logo.update(185, 10)
    images.draw(screen)
    pygame.mouse.set_visible(1)
    pygame.display.flip()
    state = 'logo'
    dead = True
    # Музыка в лого
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data/menuLoop.mp3')
    pygame.mixer.music.play(-1)


# Чтобы построить уровень по карте
def build_level(file_name):
    global platforms
    global DieBlocks
    global characters
    global character
    global pos_character
    screen.fill((31, 23, 28))
    pygame.mouse.set_visible(0)
    file = open(file_name)
    level_text = file.read().split('\n')
    file.close()
    for line_num in range(len(level_text)):
        line = level_text[line_num]
        for sym_num in range(len(line)):
            sym = line[sym_num]
            if sym == '*':
                a = None
                pass
            elif sym == '^':
                a = Sprite(DieBlocks, pygame.transform.scale(load_image('Spike.png'), (BLOCK_SIZE, BLOCK_SIZE)))
            elif sym == '#':
                a = Sprite(platforms, pygame.transform.scale(load_image('Block.png'), (BLOCK_SIZE, BLOCK_SIZE)))
            elif sym == '<':
                a = Sprite(DieBlocks, pygame.transform.scale(load_image('LSpike.png'), (BLOCK_SIZE, BLOCK_SIZE)))
            elif sym == '_':
                a = Sprite(platforms, pygame.transform.scale(load_image('Platform.png'), (BLOCK_SIZE, BLOCK_SIZE // 2)))
                a.update(sym_num * BLOCK_SIZE, line_num * BLOCK_SIZE + (BLOCK_SIZE // 2))
                continue
            elif sym == '@':
                a = Sprite(characters, pygame.transform.scale(load_image('Character.png'), (BLOCK_SIZE, BLOCK_SIZE)))
                character = a
                pos_character = sym_num * BLOCK_SIZE
            try:
                a.update(sym_num * BLOCK_SIZE, line_num * BLOCK_SIZE)
            except:
                pass
            platforms.draw(screen)
            DieBlocks.draw(screen)
            characters.draw(screen)
    return len(level_text[0]) * BLOCK_SIZE


# Главный игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif state == 'logo':
            if event.type == pygame.MOUSEBUTTONUP and event.button in [1, 2]:
                if play.rect.collidepoint(*event.pos):
                    play.kill()
                    logo.kill()
                    # Меню уровней
                    first = Sprite(level_menu, pygame.transform.scale(load_image("1.png"), (155, 135)))
                    first.update(265, 235)
                    second = Sprite(level_menu, pygame.transform.scale(load_image("2.png"), (100, 100)))
                    second.update(550, 250)
                    level_menu.draw(screen)
                    state = 'level_menu'
        elif state == 'level_menu':
            if event.type == pygame.MOUSEBUTTONUP and event.button in [1, 2] and \
                    (first.rect.collidepoint(*event.pos) or second.rect.collidepoint(*event.pos)):
                # Переход в игру
                is_jumping = False
                jump_counter = 0
                if dead:
                    platforms = pygame.sprite.Group()
                    DieBlocks = pygame.sprite.Group()
                    characters = pygame.sprite.Group()
                    character = None
                    cam = Camera(width, height)
                if first.rect.collidepoint(*event.pos):
                    len_level = build_level('data/level_1.txt')
                elif second.rect.collidepoint(*event.pos):
                    len_level = build_level('data/level_2.txt')
                # Музыка на уровне
                pygame.mixer.music.stop()
                pygame.mixer.music.load(LEVEL_MUSIC)
                pygame.mixer.music.play(-1)
                state = 'game'
    if state == 'game':
        # Движение персонажа
        character.update(character.rect.x + V, character.rect.y)
        pos_character += V
        # Прыжки
        if is_jumping or (
                pygame.key.get_pressed()[32] or pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]) \
                and pygame.sprite.spritecollideany(character, platforms):
            jump_counter += 1
            is_jumping = True
            screen.fill((31, 23, 28))
            # Вверх
            if jump_counter < 8:
                character.update(character.rect.x, character.rect.y - 2 * JUMP_K)
            elif jump_counter < 15 and not pygame.sprite.spritecollideany(character, platforms):
                character.update(character.rect.x, character.rect.y - 0.9 * JUMP_K)
            # Вниз
            elif jump_counter < 22 and not pygame.sprite.spritecollideany(character, platforms):
                character.update(character.rect.x, character.rect.y + 0.9 * JUMP_K)
            elif jump_counter < 29 and not pygame.sprite.spritecollideany(character, platforms):
                character.update(character.rect.x, character.rect.y + 2 * JUMP_K)
            # Конец прыжка
            else:
                is_jumping = False
                jump_counter = 0
                if not pygame.sprite.spritecollideany(character, platforms) and not is_jumping and \
                        not pygame.sprite.spritecollideany(character, DieBlocks):
                    character.update(character.rect.x, character.rect.y + 2)
            # Предохранение от бага пересечения кубика при приземлении на платформу
            while 21 < jump_counter and pygame.sprite.spritecollideany(character, platforms):
                character.update(character.rect.x, character.rect.y - 0.1)
        # Проверка свободного падения
        if not pygame.sprite.spritecollideany(character, platforms) and not is_jumping and \
                not pygame.sprite.spritecollideany(character, DieBlocks):
            character.update(character.rect.x, character.rect.y + K_FALL)
        # Проверка столкновения с платформами
        else:
            for spr in pygame.sprite.spritecollide(character, platforms, False):
                if character.rect.x + character.rect.width >= spr.rect.x and \
                        character.rect.y + character.rect.height >= spr.rect.y + 8:
                    death()
        # Проверка смерти или конца игры
        if pygame.sprite.spritecollideany(character,
                                          DieBlocks) or pos_character >= len_level:
            death()
            continue
        # Обновление камеры
        cam.update(character)
        cam.apply(character)
        for spr in platforms:
            cam.apply(spr)
        for spr in DieBlocks:
            cam.apply(spr)
        # Обновление экрана в игре
        screen.fill((31, 23, 28))
        platforms.draw(screen)
        DieBlocks.draw(screen)
        characters.draw(screen)

    clock.tick(FPS)
    if counter == 0 and state == 'logo' or state == 'level_menu':
        play.update()
        images.draw(screen)
        level_menu.draw(screen)
    pygame.display.flip()
    counter += 1
    counter = counter % 10
