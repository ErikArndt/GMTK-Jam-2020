import pygame
import const
import img
import sound
import background
from game import Game

pygame.mixer.pre_init(22050, -16, 2, 2048) # idk what this does but apparently I need it
pygame.mixer.init()
pygame.init()

WINDOW = pygame.display.set_mode((const.WIN_LENGTH, const.WIN_HEIGHT)) # defines the game window
pygame.display.set_caption('I Am Not On Fire Yet')
SURFACE = pygame.Surface((const.WIN_LENGTH, const.WIN_HEIGHT))

img.init_images() # must be done after setting display mode
sound.init_sounds()

def run_game(window, surface):
    clock = pygame.time.Clock()
    game_bg = background.Background(surface)
    game = Game(surface)

    running = True
    while running:
        clock.tick()
        pygame.time.delay(10) ## apparently this helps with inputs
        game_bg.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # what happens when X is pressed
                running = False
            if event.type == pygame.KEYDOWN:
                game.press_key(event.key)

            if event.type == pygame.MOUSEMOTION: # keeps track of mouse coords
                mouse_x, mouse_y = event.pos
                game.move_mouse(mouse_x, mouse_y)

            if event.type == pygame.MOUSEBUTTONDOWN:
                game.click_mouse()

        game.tick()
        game.draw()

        window.blit(surface, (0, 0))
        pygame.display.update()
    pygame.quit()

run_game(WINDOW, SURFACE)
