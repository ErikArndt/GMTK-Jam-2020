import pygame
import ship
class Room:
    def __init__(self, x, y, adjacent): # x and y are the canvas coordinates, used for drawing
        self.x_pos = x
        self.y_pos = y
        self.adjacent = adjacent # this is an array of integers

        self.fire_level = 0
        self.spread_chance = 0.2 # chance that an adjacent level 2 fire spreads to this room

        self.sprinkling = False

    def draw_room(self, surface): # will be replaced once we have room visuals
        if self.fire_level == 0:
            colour = (0, 255, 0)
        elif self.fire_level == 1:
            colour = (255, 150, 0)
        else:
            colour = (255, 0, 0)
        pygame.draw.rect(surface, colour, (self.x_pos, self.y_pos, 50, 50))
        for i in self.adjacent:
            end_pos = (ship.lookup(i).x + 25, ship.lookup(i).y + 25)
            pygame.draw.line(surface, (255, 255, 255), (self.x_pos + 25, self.y_pos + 25), end_pos, 4)

