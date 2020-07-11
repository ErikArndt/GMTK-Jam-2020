import pygame
import const
from img import IMAGES

BORDER_SIZE = 10 # pixels around edge of dashboard
BAR_WIDTH = 25

# Not sure if I'll need classes for all of these, but it couldn't hurt
class Radar:
    def __init__(self, x_pos, y_pos, radius):
        self.x_pos = x_pos # center
        self.y_pos = y_pos # center
        self.radius = radius

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 50, 0), (self.x_pos, self.y_pos), self.radius)

class ResourceBar:
    def __init__(self, x_pos, y_pos, length, maximum, colour, vertical=False):
        self.x_pos = x_pos # top-left corner
        self.y_pos = y_pos # top-left corner
        self.length = length
        self.max = maximum # maximum value the bar can take (i.e. it's "full" value)
        self.value = maximum
        self.colour = colour
        self.vertical = vertical

    def change_value(self, modifier):
        """Add modifier to value of bar (or subtract it if modifier is negative)

        Args:
            modifier (integer): amount to change value by.
        """
        self.value += modifier

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

    def draw(self, surface):
        if self.vertical:
            # do what's below, but vertical
            return
        else:
            pygame.draw.rect(surface, (50, 50, 50), (self.x_pos, self.y_pos, self.length, BAR_WIDTH))
            bar_border = 5
            fill_ratio = round(self.value / self.max)*self.length - bar_border*2
            pygame.draw.rect(surface, (0, 0, 0), (self.x_pos + bar_border, self.y_pos + bar_border, \
                self.length - bar_border*2, BAR_WIDTH - bar_border*2))
            pygame.draw.rect(surface, self.colour, (self.x_pos + bar_border, self.y_pos + bar_border, \
                fill_ratio, BAR_WIDTH - bar_border*2))

class Dashboard:
    def __init__(self, surface):
        self.surface = surface
        self.x_pos = BORDER_SIZE
        self.y_pos = round(const.WIN_HEIGHT*2/3)
        self.width = const.WIN_LENGTH - 2*BORDER_SIZE
        self.height = round(const.WIN_HEIGHT/3 - BORDER_SIZE)

        radar_radius = round(self.height/2) - 20
        self.radar = Radar(self.x_pos + self.width - radar_radius - 10, \
            self.y_pos + round(self.height/2), radar_radius)

        self.hull_bar = ResourceBar(self.x_pos + 130, self.y_pos + 10, 150, 100, (255, 0, 0))
        self.water_bar = ResourceBar(self.x_pos + 130, self.y_pos + 20 + BAR_WIDTH, 150, 100, (50, 50, 255))

    def take_damage(self, damage=5):
        """Decreases the Hull bar by the amount given, or 5 if none is given.

        Args:
            damage (int, optional): Damage dealt. Defaults to 5.
        """
        self.hull_bar.change_value(damage*-1)

    def lose_water(self, water_loss=5):
        """Decreases the Water bar by the amount given, or 5 if none is given.

        Args:
            water_loss (int, optional): Water spent. Defaults to 5.
        """
        self.water_bar.change_value(water_loss*-1)

    def draw(self):
        pygame.draw.rect(self.surface, (150, 50, 0), (self.x_pos, self.y_pos, \
            self.width, self.height))
        self.radar.draw(self.surface)

        hull_text = const.TITLE_FONT_SM.render("HULL", True, const.BLACK)
        self.surface.blit(hull_text, (self.x_pos + 120 - hull_text.get_width(), self.y_pos + 5))
        self.hull_bar.draw(self.surface)

        water_text = const.TITLE_FONT_SM.render("WATER", True, const.BLACK)
        self.surface.blit(water_text, (self.x_pos + 120 - water_text.get_width(), self.y_pos + 15 + BAR_WIDTH))
        self.water_bar.draw(self.surface)

        cactus = pygame.transform.scale(IMAGES['cactus'], (55, 80))
        self.surface.blit(cactus, (BORDER_SIZE, \
            const.WIN_HEIGHT - BORDER_SIZE - cactus.get_height()))
