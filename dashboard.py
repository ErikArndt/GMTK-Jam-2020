import pygame
import const
from img import IMAGES

class Dashboard:
    def __init__(self, surface):
        self.surface = surface

    def draw(self):
        pygame.draw.rect(self.surface, (150, 50, 0), (10, const.WIN_HEIGHT*2/3, \
            const.WIN_LENGTH - 20, const.WIN_HEIGHT/3 - 10))
        cactus = IMAGES['cactus']
        self.surface.blit(cactus, (const.WIN_LENGTH - cactus.get_width(), const.WIN_HEIGHT - cactus.get_height()))
