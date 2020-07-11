import pygame
import ship
class Room:
    def __init__(self, x, y, adjacent): # x and y are the canvas coordinates, used for drawing
        self.x = x
        self.y = y
        self.adjacent = adjacent # this is an array of integers

        self.fireLevel = 0
        self.spreadChance = 0.2 # chance that an adjacent level 2 fire spreads to this room

        self.sprinkling = False

    def draw_room(self, surface): # will be replaced once we have room visuals
        if self.fireLevel == 0:
            colour = (0, 255, 0)
        elif self.fireLevel == 1:
            colour = (255, 150, 0)
        else:
            colour = (255, 0, 0)
        pygame.draw.rect(surface, colour, (self.x, self.y, 50, 50))
        for i in self.adjacent:
            end_pos = (ship.lookUp(i).x + 25, ship.lookUp(i).y + 25)
            pygame.draw.line(surface, (255, 255, 255), (self.x + 25, self.y + 25), end_pos, 4)

