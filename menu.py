import pygame
import const

pygame.font.init()

DEFAULT_FONT = pygame.font.SysFont('timesnewroman', 60)

def draw_menu(surface):
    basic_text = DEFAULT_FONT.render('Hello World', False, const.WHITE)
    surface.blit(basic_text, (100, 100))
