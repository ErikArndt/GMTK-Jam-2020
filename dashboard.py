import pygame
import const
from img import IMAGES
from sound import SOUNDS
from radar import Radar

BORDER_SIZE = 10 # pixels around edge of dashboard
BAR_WIDTH = 25
BAR_BORDER = 5

class ResourceBar:
    def __init__(self, x_pos, y_pos, length, maximum, colour, vertical=False):
        self.x_pos = x_pos # top-left corner
        self.y_pos = y_pos # top-left corner
        self.length = length
        self.max = maximum # maximum value the bar can take (i.e. it's "full" value)
        self.value = maximum
        self.fill_width = self.length - BAR_BORDER*2
        self.colour = colour
        self.vertical = vertical

    def recalculate_fill_width(self):
        self.fill_width = round((self.value / self.max) * (self.length - BAR_BORDER*2))

    def change_value(self, modifier):
        """Add modifier to value of bar (or subtract it if modifier is negative). If
        amount is greater than max or less than zero, bar's value will be bounded.

        Args:
            modifier (integer): amount to change value by.
        Returns:
            integer: amount that value was set to.
        """
        self.set_value(self.value + modifier)
        return self.value

    def set_value(self, value):
        """Set bar's value to the given amount. If amount is greater than max or less
        than zero, bar's value will be bounded.

        Args:
            value (integer): Amount to set value to.
        """
        if value < 0:
            self.value = 0
        elif value > self.max:
            self.value = self.max
        else:
            self.value = value
        self.recalculate_fill_width()

    def draw(self, surface):
        if self.vertical:
            # do what's below, but vertical
            return
        else:
            pygame.draw.rect(surface, const.BLACK, (self.x_pos + BAR_BORDER, self.y_pos + BAR_BORDER, \
                self.length - BAR_BORDER*2, BAR_WIDTH - BAR_BORDER*2))
            pygame.draw.rect(surface, self.colour, (self.x_pos + BAR_BORDER, self.y_pos + BAR_BORDER, \
                self.fill_width, BAR_WIDTH - BAR_BORDER*2))

class Sensors:
    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.disabled = False
        self.broken = False

        self.hull_bar = ResourceBar(self.x_pos + 70, self.y_pos + 10, 150, 10, (255, 0, 0))
        self.water_bar = ResourceBar(self.x_pos + 70, self.y_pos + 20 + BAR_WIDTH, 150, 50, (50, 50, 255))

    def draw(self, surface):
        if self.broken:
            pygame.draw.rect(surface, (50, 50, 50), (self.x_pos + 70, self.y_pos + 10, 150, 10 + 2*BAR_WIDTH))
            fire_text = const.TITLE_FONT_SM.render("OUT", True, (255, 127, 0))
            surface.blit(fire_text, (self.x_pos + 70 + (150 - fire_text.get_width())/2, self.y_pos + 25))
        elif self.disabled:
            pygame.draw.rect(surface, (50, 50, 50), (self.x_pos + 70, self.y_pos + 10, 150, 10 + 2*BAR_WIDTH))
            fire_text = const.TITLE_FONT_SM.render("ON FIRE", True, (255, 127, 0))
            surface.blit(fire_text, (self.x_pos + 70 + (150 - fire_text.get_width())/2, self.y_pos + 25))
        else:
            self.hull_bar.draw(surface)
            self.water_bar.draw(surface)

class DashButton:
    def __init__(self, rect):
        self.rect = rect
        self.moused_over = False

    def check_mouse_hover(self, mouse_x, mouse_y):
        if mouse_x > self.rect[0] and mouse_x < self.rect[0] + self.rect[2] and \
            mouse_y > self.rect[1] and mouse_y < self.rect[1] + self.rect[3]:
            self.moused_over = True
        else:
            self.moused_over = False

class Dashboard:
    def __init__(self, surface):
        self.surface = surface
        self.x_pos = BORDER_SIZE
        self.y_pos = round(const.WIN_HEIGHT*2/3)
        self.width = const.WIN_LENGTH - 2*BORDER_SIZE
        self.height = round(const.WIN_HEIGHT/3 - BORDER_SIZE)

        radar_radius = round(self.height/2) - 20
        self.radar = Radar(self.x_pos + 5 + self.width - radar_radius - 10, \
            self.y_pos + round(self.height/2) + 2, radar_radius)

        self.sensors = Sensors(self.x_pos + 5, self.y_pos + 2)

        self.laser_button_n = DashButton((self.x_pos + 510, self.y_pos + 30, 70, 70))
        self.laser_button_s = DashButton((self.x_pos + 510, self.y_pos + 110, 70, 70))
        self.repair_switch = DashButton((self.x_pos + 350, self.y_pos + 70, 150, 100))
        self.laser_n_disabled = False
        self.laser_s_disabled = False
        self.repair_disabled = False
        self.cactus_button = DashButton((BORDER_SIZE, const.WIN_HEIGHT - BORDER_SIZE - 80, 55, 80))

    def take_damage(self, damage=1):
        """Decreases the Hull bar by the amount given, or 1 if none is given.

        Args:
            damage (int, optional): Damage dealt. Defaults to 1.
        """
        self.sensors.hull_bar.change_value(damage*-1)
        if damage is not 0:
            SOUNDS['damage'].play()

    def lose_water(self, water_loss=1):
        """Decreases the Water bar by the amount given, or 1 if none is given.

        Args:
            water_loss (int, optional): Water spent. Defaults to 1.
        """
        self.sensors.water_bar.change_value(water_loss*-1)
        if water_loss is not 0:
            SOUNDS['sprinkler'].play()

    def get_health(self):
        """Getter that returns the health of the hull.
        """
        return self.sensors.hull_bar.value

    def get_water(self):
        """Getter that returns the water left in the tank.
        """
        return self.sensors.water_bar.value

    def draw(self, sprinklers, lightyears, level, is_repairing=False):
        # Many values here are magic numbers. This layout will be pretty messed up if
        # we change WIN_LENGTH or WIN_HEIGHT
        self.radar.draw(self.surface)
        if not (self.sensors.disabled or self.sensors.broken):
            self.sensors.draw(self.surface)
        number_text = const.DIGITAL_FONT.render(str(lightyears), True, const.YELLOW)
        pygame.draw.rect(self.surface, const.BLACK, (self.x_pos + 75, self.y_pos + 115, \
            number_text.get_width() + 20, number_text.get_height() + 10))
        self.surface.blit(number_text, (self.x_pos + 85, self.y_pos + 125))

        if level <= 2:
            self.surface.blit(IMAGES['dashboard_sans_lever'], (self.x_pos-10, self.y_pos))
        elif level == 3:
            self.surface.blit(IMAGES['dashboard'], (self.x_pos-10, self.y_pos))
        if self.sensors.disabled or self.sensors.broken:
            self.sensors.draw(self.surface)

        hull_text = const.DEFAULT_FONT_SM.render("Hull", True, const.BLACK)
        self.surface.blit(hull_text, (self.x_pos + 68 - hull_text.get_width(), self.y_pos + 10))
        water_text = const.DEFAULT_FONT_SM.render("Water", True, const.BLACK)
        self.surface.blit(water_text, (self.x_pos + 68 - water_text.get_width(), self.y_pos + 20 + BAR_WIDTH))
        radar_text = const.DEFAULT_FONT_SM.render('Radar', True, const.BLACK)
        self.surface.blit(radar_text, (self.x_pos + 600, self.y_pos + BORDER_SIZE))

        cactus = pygame.transform.scale(IMAGES['cactus'], (55, 80))
        self.surface.blit(cactus, (BORDER_SIZE, \
            const.WIN_HEIGHT - BORDER_SIZE - cactus.get_height()))

        # available sprinklers
        sprinkler_text = const.DEFAULT_FONT_SM.render('Sprinklers Available', True, const.BLACK)
        self.surface.blit(sprinkler_text, (self.x_pos + 300, self.y_pos + BORDER_SIZE))
        for i in range(sprinklers):
            self.surface.blit(IMAGES['sprinkler'], (self.x_pos + 300 + i*50, \
                self.y_pos + BORDER_SIZE + sprinkler_text.get_height()))

        # lightyears to destination
        lightyear_text = const.DEFAULT_FONT_SM.render('Lightyears to', True, const.BLACK)
        spaceport_text = const.DEFAULT_FONT_SM.render('Next Spaceport', True, const.BLACK)
        self.surface.blit(lightyear_text, (self.x_pos + 130, self.y_pos + 120))
        self.surface.blit(spaceport_text, (self.x_pos + 130, self.y_pos + 120 + lightyear_text.get_height()))

        # lasers
        laser_text = const.DEFAULT_FONT_SM.render('Lasers', True, const.BLACK)
        self.surface.blit(laser_text, (self.x_pos + 515, self.y_pos + BORDER_SIZE))

        if self.laser_n_disabled:
            pygame.draw.rect(self.surface, (50, 50, 50), (self.x_pos + 510, self.y_pos + 38, 70, 70))
            fire_text = const.TITLE_FONT_SM.render("FIRE", True, (255, 127, 0))
            self.surface.blit(fire_text, (self.x_pos + 510 + (70 - fire_text.get_width())/2, self.y_pos + 53))

        if self.laser_s_disabled:
            pygame.draw.rect(self.surface, (50, 50, 50), (self.x_pos + 510, self.y_pos + 118, 70, 70))
            fire_text = const.TITLE_FONT_SM.render("FIRE", True, (255, 127, 0))
            self.surface.blit(fire_text, (self.x_pos + 510 + (70 - fire_text.get_width())/2, self.y_pos + 133))

        # repair button
        if level >= 3:
            repair_text = const.DEFAULT_FONT_SM.render('Repair Mode', True, const.BLACK)
            self.surface.blit(repair_text, (self.x_pos + 330, self.y_pos + 90))
            off_on_text = const.DEFAULT_FONT_SM.render('On            Off', True, const.BLACK)
            if not self.repair_disabled:
                self.surface.blit(off_on_text, (self.x_pos + 335, self.y_pos + 90 + repair_text.get_height()))
                if not is_repairing:
                    self.surface.blit(IMAGES['lever'], (self.x_pos + 320, self.y_pos + 133))
            else:
                pygame.draw.rect(self.surface, (50, 50, 50), (self.x_pos + 315, self.y_pos + 133, 135, 45))
                fire_text = const.TITLE_FONT_SM.render("ON FIRE", True, (255, 127, 0))
                self.surface.blit(fire_text, (self.x_pos + 315 + (135 - fire_text.get_width())/2, self.y_pos + 143))
