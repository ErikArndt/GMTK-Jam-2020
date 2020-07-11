import pygame
import img
class Room:
    def __init__(self, x, y, adjacent, room_type): # x and y are the canvas coordinates, used for drawing
        self.x_pos = x
        self.y_pos = y
        self.size = 70
        self.adjacent = adjacent # this is an array of integers

        self.fire_level = 0
        self.spread_chance = 0.5 # chance that an adjacent level 2 fire spreads to this room
        self.fire_anim_state = 0

        self.moused_over = False
        self.sprinkling = False

        self.type = room_type

    def draw(self, surface):
        # if self.fire_level == 0:
        #     r,g,b = (0, 225, 0)
        # elif self.fire_level == 1:
        #     r,g,b = (225, 150, 0)
        # else:
        #     r,g,b = (225, 0, 0)
        # if self.moused_over:
        #     r += 30
        #     g += 30
        #     b += 30
        # pygame.draw.rect(surface, (r,g,b), (self.x_pos, self.y_pos, self.size, self.size))
        surface.blit(img.IMAGES['empty_room'], (self.x_pos, self.y_pos))
        if self.fire_level == 1:
            surface.blit(img.IMAGES['fire_lvl_1'][self.fire_anim_state], (self.x_pos, self.y_pos))
        elif self.fire_level == 2:
            surface.blit(img.IMAGES['fire_lvl_2'][self.fire_anim_state], (self.x_pos, self.y_pos))

        if self.sprinkling:
            pygame.draw.rect(surface, (0, 0, 255), (self.x_pos + self.size/2 - 5, \
                self.y_pos - 5, 10, 10))
