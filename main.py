import pygame
import const
import menu
import ship
import background
import dashboard
import img
import time

pygame.init()

WINDOW = pygame.display.set_mode((const.WIN_LENGTH, const.WIN_HEIGHT)) # defines the game window
pygame.display.set_caption('Game name')
SURFACE = pygame.Surface((const.WIN_LENGTH, const.WIN_HEIGHT))

img.init_images() # must be done after setting display mode

def run_game(window, surface):
    game_clock = pygame.time.Clock()
    game_bg = background.Background(surface)
    game_dash = dashboard.Dashboard(surface)
    game_ship = ship.Ship(surface)

    running = True
    game_state = const.MENU

    f_tick_time = 5 # in seconds
    s_tick_time = 3 # ditto

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
                        last_f_tick = time.time()
                        last_s_tick = time.time()

                    #if game_state == const.PLAYING: # for testing
                    #    game_ship.fire_tick()
            if event.type == pygame.MOUSEMOTION: # keeps track of mouse coords
                mouse_x, mouse_y = event.pos
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in game_ship.room_list:
                    if mouse_x > i.x_pos and mouse_x < i.x_pos + i.width and mouse_y > i.y_pos and mouse_y < i.y_pos + i.height:
                        if i.sprinkling:
                            i.sprinkling = False
                        elif not i.sprinkling:
                            i.sprinkling = True


        if game_state == const.MENU:
            menu.draw_menu(surface)

        if game_state == const.PLAYING:
            current_time = time.time()
            if current_time - last_f_tick >= f_tick_time:
                game_ship.fire_tick()
                last_f_tick = current_time
            if current_time - last_s_tick >= s_tick_time:
                game_ship.sprinkler_tick()
                last_s_tick = current_time

            game_ship.draw()
            game_dash.draw()            

        window.blit(surface, (0, 0))
        pygame.display.update()
    pygame.quit()

run_game(WINDOW, SURFACE)
