import pygame
import os

size = width, height = 800, 500
screen = pygame.display.set_mode(size)
BLOCK_SIZE = 50
state = 'logo'


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_group, sheet, columns, rows, x, y):
        super().__init__(sprite_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group, image):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, x, y):
        self.rect.x, self.rect.y = (x, y)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2 - 120)


platforms = pygame.sprite.Group()
DieBlocks = pygame.sprite.Group()
characters = pygame.sprite.Group()
cam = Camera()


def build_level(file_name, ignore_player=False):
    global platforms
    global DieBlocks
    global characters
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
                a = Sprite(platforms, pygame.transform.scale(load_image('Platform.png'), (BLOCK_SIZE, BLOCK_SIZE)))
            elif sym == '@' and not ignore_player:
                a = Sprite(characters, pygame.transform.scale(load_image('Character.png'), (BLOCK_SIZE, BLOCK_SIZE)))
                character = a
            try:
                a.update(sym_num * BLOCK_SIZE, line_num * BLOCK_SIZE)
            except:
                pass
            platforms.draw(screen)
            DieBlocks.draw(screen)
            characters.draw(screen)
    return len(level_text[0]) * BLOCK_SIZE
