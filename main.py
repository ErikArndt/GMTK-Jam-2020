import pygame

pygame.init()

window = pygame.display.set_mode((800, 600)) # defines the game window
pygame.display.set_caption('Game name')
surface = pygame.Surface((800, 600))
roomArray = [] # to be filled with room objects

def lookUp(index): # not sure if this should be here or in room.py
    return roomArray[index]

def run_game():
    game_clock = pygame.time.Clock()
    running = True
    while running:
        game_clock.tick()
        pygame.time.delay(10) ## apparently this helps with inputs
        pygame.draw.rect(surface, (0,0,0), (0,0,800,600)) # black background

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # what happens when X is pressed
                running = False

run_game()
