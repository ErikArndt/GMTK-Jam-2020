"""I wanted to make a class for the space background, and
I figured if I'm making a class, I might as well make a separate
file, too.
"""
import random
import pygame
import const

## Module-specific constants
NUM_INITIAL_STARS = 10
MAX_TIME_BETWEEN_STARS = 20

class Star:
    def __init__(self, x_pos=const.WIN_LENGTH):
        self.x_pos = x_pos
        self.y_pos = random.randint(0, const.WIN_HEIGHT)

    def draw(self, surface):
        """Draws the star. Currently just a square, but I might make it
        look cooler later.

        Args:
            surface (pygame.Surface): The surface to draw the star onto.
        """
        pygame.draw.rect(surface, const.WHITE, (self.x_pos, self.y_pos, 5, 5))

    def move(self):
        """Moves the star to the left.
        """
        self.x_pos -= 5

class Background:
    def __init__(self, surface):
        self.surface = surface
        self.stars = []
        self.bg_colour = const.BLACK
        self.time_to_next_star = 0

        for _ in range(NUM_INITIAL_STARS): # initialize with initial stars
            self.stars.append(Star(random.randint(50, const.WIN_LENGTH - 50)))

    def draw(self):
        """Draws a black background with white stars zooming by. Also moves the stars
        and prepares for the next frame.
        """
        pygame.draw.rect(self.surface, const.BLACK, (0, 0, const.WIN_LENGTH, const.WIN_HEIGHT))
        for star in self.stars:
            star.move()
            star.draw(self.surface)
        if self.time_to_next_star <= 0:
            self.stars.append(Star())
            self.time_to_next_star = random.randint(0, MAX_TIME_BETWEEN_STARS)
        else:
            self.time_to_next_star -= 1

        # remove stars off the edge of the screen
        i = 0
        while i < len(self.stars):
            if self.stars[i].x_pos <= 0:
                self.stars.pop(i)
            else:
                i += 1
