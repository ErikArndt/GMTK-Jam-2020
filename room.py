import pygame
class Room:
    def __init__(self, x, y, adjacent): # x and y are the canvas coordinates, used for drawing
        self.x_pos = x
        self.y_pos = y
        self.width = 50
        self.height = 50
        self.adjacent = adjacent # this is an array of integers

        self.fire_level = 0
        self.spread_chance = 0.5 # chance that an adjacent level 2 fire spreads to this room

        self.moused_over = False
        self.sprinkling = False

    def draw(self, surface): # will be updated once we have room visuals
        if self.fire_level == 0:
            r,g,b = (0, 225, 0)
        elif self.fire_level == 1:
            r,g,b = (225, 150, 0)
        else:
            r,g,b = (225, 0, 0)
        if self.moused_over:
            r += 30
            g += 30
            b += 30
        pygame.draw.rect(surface, (r,g,b), (self.x_pos, self.y_pos, 50, 50))

        if self.sprinkling:
            pygame.draw.rect(surface, (0, 0, 255), (self.x_pos+20, self.y_pos-5, 10, 10))
