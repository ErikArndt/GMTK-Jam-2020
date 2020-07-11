import pygame
import const

pygame.font.init()

# should these be in const?
DEFAULT_FONT = pygame.font.Font('nasalization-rg.ttf', 24)
SCIFI_FONT = pygame.font.Font('ethnocentric-rg.ttf', 24)
TITLE_FONT = pygame.font.Font('ethnocentric-rg.ttf', 60)

def draw_menu(surface):
    title_text = TITLE_FONT.render("Fireship", True, const.WHITE)
    surface.blit(title_text, (100, 100))
    wt_text = SCIFI_FONT.render("(Working Title)", True, const.WHITE)
    surface.blit(wt_text, (100, 100 + title_text.get_height()))
    start_text = DEFAULT_FONT.render("Press Space to start", True, const.WHITE)
    surface.blit(start_text, (const.WIN_LENGTH/2 - start_text.get_width()/2, 450))
