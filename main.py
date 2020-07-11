import time
import pygame
import const
import img
import background
import menu
import ship
import dashboard
import text

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
    active_text_box = None # can only have one active text box at a time

    running = True
    game_state = const.MENU

    f_tick_time = 5 # in seconds
    s_tick_time = 3 # ditto
    last_f_tick = 0 # declare this up front just in case
    last_s_tick = 0 # ditto

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

            if event.type == pygame.MOUSEMOTION: # keeps track of mouse coords
                mouse_x, mouse_y = event.pos
                for i in game_ship.room_list:
                    if mouse_x > i.x_pos and mouse_x < i.x_pos + i.width and mouse_y > i.y_pos and mouse_y < i.y_pos + i.height:
                        i.moused_over = True
                    else:
                        i.moused_over = False
                if active_text_box and len(active_text_box.buttons) > 0:
                    for btn in active_text_box.buttons:
                        btn.check_mouse_hover(mouse_x, mouse_y)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == const.MENU:
                    game_state = const.PLAYING

                # Should these be restricted to certain game states?
                for i in game_ship.room_list:
                    if i.moused_over:
                        if i.sprinkling:
                            i.sprinkling = False
                        elif not i.sprinkling:
                            i.sprinkling = True
                if active_text_box and len(active_text_box.buttons) > 0:
                    # Here is where I'll have to figure out how to add functionality
                    # to the buttons. I might just have to do this on a case-by-case basis.
                    # I know the first button of the FIRE_OUT text goes to the title screen.
                    if active_text_box.buttons[0].moused_over and game_state == const.FIRE_OUT:
                        game_state = const.MENU
                        active_text_box = None

        if game_state == const.MENU:
            menu.draw_menu(surface)

        if game_state == const.PLAYING:
            current_time = time.time()
            if current_time - last_f_tick >= f_tick_time:
                num_onfire = game_ship.fire_tick()
                game_dash.take_damage() # for testing
                if num_onfire == 0:
                    # There's probably a better way of detecting that the fire
                    # is out, but for now this works. It takes a few seconds, but it works.
                    game_state = const.FIRE_OUT
                    game_over_text = 'The fire went out! Your engines can no longer be powered. ' + \
                        'You and your cactus are screwed.'
                    active_text_box = text.TextBox(game_over_text, const.MED, 'GAME OVER')
                    active_text_box.add_button('Back to Title', const.RED)
                    # active_text_box.add_button('Play again', (50, 50, 255))
                    # active_text_box.add_button('Punch Cactus', (0, 255, 0))
                last_f_tick = current_time
            if current_time - last_s_tick >= s_tick_time:
                num_sprinkling = game_ship.sprinkler_tick()
                game_dash.lose_water(num_sprinkling)
                last_s_tick = current_time

            game_ship.draw()
            game_dash.draw()

        if game_state == const.FIRE_OUT:
            game_ship.draw()
            game_dash.draw()
            active_text_box.draw(surface) # this state should always have the text box

        window.blit(surface, (0, 0))
        pygame.display.update()
    pygame.quit()

run_game(WINDOW, SURFACE)
