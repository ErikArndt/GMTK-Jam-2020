import pygame
import img
import util
import const
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
        self.is_event = False
        self.sprinkling = False

        self.type = room_type

    def draw(self, surface):
        surface.blit(img.IMAGES['empty_room'], (self.x_pos, self.y_pos))
        if self.fire_level > 0:
            if self.fire_level == 1:
                surface.blit(img.IMAGES['fire_lvl_1'][self.fire_anim_state], (self.x_pos, self.y_pos))
                r,g,b = (225, 150, 0)
            elif self.fire_level == 2:
                surface.blit(img.IMAGES['fire_lvl_2'][self.fire_anim_state], (self.x_pos, self.y_pos))
                r,g,b = (225, 0, 0)
            if self.moused_over:
                r,g,b = util.lighten((r, g, b))
            overlay_surface = pygame.Surface((self.size, self.size), pygame.HWSURFACE)
            overlay_surface.set_alpha(50) # the surface is now semi-transparent
            util.bevelled_rect(overlay_surface, (r, g, b), (0, 0, self.size, self.size), \
                15)
            surface.blit(overlay_surface, (self.x_pos, self.y_pos))
        if self.type != const.EMPTY:
            if self.type == const.BRIDGE:
                letter = "B"
            elif self.type == const.SENSORS:
                letter = "S"
            elif self.type == const.RADAR:
                letter = "R"
            elif self.type == const.LASER_PORT:
                letter = "L"
            elif self.type == const.LASER_STBD:
                letter = "L"
            elif self.type == const.SHIELD:
                letter = "SH"
            room_text = const.TITLE_FONT_SM.render(letter, True, const.BLACK)
            surface.blit(room_text, (self.x_pos + (70 - room_text.get_width())/2, self.y_pos + 23))
        if self.is_event:
            overlay_surface = pygame.Surface((self.size, self.size), pygame.HWSURFACE)
            overlay_surface.set_alpha(50) # the surface is now semi-transparent
            util.bevelled_rect(overlay_surface, (0, 255, 0), (0, 0, self.size, self.size), \
                15)
            surface.blit(overlay_surface, (self.x_pos, self.y_pos))



        if self.sprinkling:
            pygame.draw.rect(surface, (0, 0, 255), (self.x_pos + self.size/2 - 5, \
                self.y_pos - 5, 10, 10))
