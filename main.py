import pygame
import const
import menu

pygame.init()

WINDOW = pygame.display.set_mode((const.WIN_LENGTH, const.WIN_HEIGHT)) # defines the game window
pygame.display.set_caption('Game name')
SURFACE = pygame.Surface((const.WIN_LENGTH, const.WIN_HEIGHT))

def run_game(window, surface):
    game_clock = pygame.time.Clock()
    running = True
    game_state = const.MENU
    while running:
        game_clock.tick()
        pygame.time.delay(10) ## apparently this helps with inputs
        pygame.draw.rect(surface, const.BLACK, (0, 0, const.WIN_LENGTH, const.WIN_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # what happens when X is pressed
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # spacebar
                    if game_state == const.MENU:
                        game_state = const.PLAYING

        if game_state == const.MENU:
            menu.draw_text(surface)

        window.blit(surface, (0, 0))
        pygame.display.update()
    pygame.quit()

run_game(WINDOW, SURFACE)
