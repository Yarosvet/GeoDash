from config import *


def build_level(file_name):
    pygame.mouse.set_visible(0)
    file = open(file_name)
    level_text = list(file.readlines())[::-1]
    file.close()
    platforms = pygame.sprite.Group()
    DieBlocks = pygame.sprite.Group()
    background = pygame.sprite.Group()
    for line in level_text:
        for object in line:
            pass  # доделать
