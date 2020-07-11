import pygame
import const
import menu
import ship
import background
import dashboard
import img

pygame.init()

WINDOW = pygame.display.set_mode((const.WIN_LENGTH, const.WIN_HEIGHT)) # defines the game window
pygame.display.set_caption('Game name')
SURFACE = pygame.Surface((const.WIN_LENGTH, const.WIN_HEIGHT))

img.init_images() # must be done after setting display mode

def run_game(window, surface):
    game_clock = pygame.time.Clock()
    game_bg = background.Background(surface)
    game_dash = dashboard.Dashboard(surface)

    running = True
    game_state = const.MENU
    while running:
        game_clock.tick()
        pygame.time.delay(10) ## apparently this helps with inputs
        game_bg.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # what happens when X is pressed
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # spacebar
                    if game_state == const.MENU:
                        game_state = const.PLAYING

                    if game_state == const.PLAYING: # for testing
                        ship.fireTick()

        if game_state == const.MENU:
            menu.draw_menu(surface)
        if game_state == const.PLAYING:
            game_dash.draw()

        if game_state == const.PLAYING:
            for i in ship.roomArray:
                i.draw_room(surface)
                
                

        window.blit(surface, (0, 0))
        pygame.display.update()
    pygame.quit()

run_game(WINDOW, SURFACE)
