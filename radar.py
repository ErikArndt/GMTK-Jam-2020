"""This module contains not only the code for the radar on the dashboard,
but also all the objects that can appear on the radar, such as alien
ships and asteroids.
"""
import time
import math
import pygame
import const
from img import IMAGES
from sound import SOUNDS

class Alien:
    def __init__(self, direction):
        self.direction = direction
        self.distance = 4 # rings away from center

    def move(self):
        self.distance -= 1

class Asteroid:
    def __init__(self, direction):
        self.direction = direction
        self.distance = 4 # rings away from center

    def move(self):
        self.distance -= 1

class Radar:
    def __init__(self, x_pos, y_pos, radius):
        self.x_pos = x_pos # center
        self.y_pos = y_pos # center
        self.radius = radius
        self.animation_length = 2 # seconds it takes for a full rotation
        self.last_rotation_time = time.time()
        self.alien_queue_N = []
        self.alien_queue_S = []
        self.asteroids = []
        self.disabled = False
        self.broken = False

    def add_alien(self, direction):
        if direction == const.NORTH:
            self.alien_queue_N.append(Alien(direction))
        elif direction == const.SOUTH:
            self.alien_queue_S.append(Alien(direction))

    def add_asteroid(self, direction):
        self.asteroids.append(Asteroid(direction))

    def fire_laser(self, direction):
        SOUNDS['laser'].play()
        if direction == const.NORTH:
            if len(self.alien_queue_N) > 0:
                self.alien_queue_N.pop(0)
        elif direction == const.SOUTH:
            if len(self.alien_queue_S) > 0:
                self.alien_queue_S.pop(0)

    def radar_tick(self, shields_up):
        """Moves aliens and asteroids closer to the center of the radar, and
        returns the hull damage taken from alien gunfire and asteroid collisions.

        Args:
            shields_up (boolean): indicates whether the ship's shields are active or not.

        Returns:
            int: amount of damage taken.
        """
        damage_taken = 0
        if len(self.alien_queue_N) > 0:
            north_alien = self.alien_queue_N[0]
            if north_alien.distance > 1:
                north_alien.move()
            else:
                damage_taken += 1
        if len(self.alien_queue_S) > 0:
            south_alien = self.alien_queue_S[0]
            if south_alien.distance > 1:
                south_alien.move()
            else:
                damage_taken += 1
        # use while loop so you can properly remove asteroids
        i = 0
        while i < len(self.asteroids):
            asteroid = self.asteroids[i]
            if asteroid.distance > 1:
                asteroid.move()
                i += 1
            elif shields_up:
                self.asteroids.pop(i)
            else:
                damage_taken += 1
                self.asteroids.pop(i)
        return damage_taken

    def draw_radar_hand(self, surface):
        # keep time current
        if time.time() - self.last_rotation_time > self.animation_length:
            self.last_rotation_time -= self.animation_length
        # calculate hand position
        progress = (time.time() - self.last_rotation_time)*2*math.pi/self.animation_length
        hand_x = round(math.cos(progress)*self.radius)
        hand_y = round(math.sin(progress)*self.radius)
        # draw the line
        pygame.draw.line(surface, const.WHITE, (self.x_pos, self.y_pos), \
            (self.x_pos + hand_x, self.y_pos + hand_y))

    def draw_aliens(self, surface):
        if len(self.alien_queue_N) > 0 and self.alien_queue_N[0].distance < 4:
            alien_dist = self.alien_queue_N[0].distance
            alien_img = pygame.transform.flip(IMAGES['alien_ship'], False, True)
            surface.blit(alien_img, (self.x_pos - 10, self.y_pos - alien_dist*20))
        if len(self.alien_queue_S) > 0 and self.alien_queue_S[0].distance < 4:
            alien_dist = self.alien_queue_S[0].distance
            surface.blit(IMAGES['alien_ship'], (self.x_pos - 10, self.y_pos + (alien_dist - 1)*20))

    def draw_asteroids(self, surface):
        for asteroid in filter(lambda a: a.distance < 4, self.asteroids):
            # These might seem like magic numbers, and that's because they are.
            # Please don't change the size of the radar, it will completely screw this up.
            if asteroid.direction == const.NORTHWEST:
                asteroid_img = IMAGES['asteroid']
                surface.blit(asteroid_img, (self.x_pos - asteroid.distance*15 - 15, \
                    self.y_pos - asteroid.distance*15 - 15))
            elif asteroid.direction == const.NORTHEAST:
                asteroid_img = pygame.transform.flip(IMAGES['asteroid'], True, False)
                surface.blit(asteroid_img, (self.x_pos + (asteroid.distance - 1)*15, \
                    self.y_pos - asteroid.distance*15 - 15))
            elif asteroid.direction == const.SOUTHWEST:
                asteroid_img = pygame.transform.flip(IMAGES['asteroid'], False, True)
                surface.blit(asteroid_img, (self.x_pos - asteroid.distance*15 - 15, \
                    self.y_pos + (asteroid.distance - 1)*15))
            elif asteroid.direction == const.SOUTHEAST:
                asteroid_img = pygame.transform.flip(IMAGES['asteroid'], True, True)
                surface.blit(asteroid_img, (self.x_pos + (asteroid.distance - 1)*15, \
                    self.y_pos + (asteroid.distance - 1)*15))

    def draw(self, surface):
        if not (self.disabled or self.broken):
            pygame.draw.circle(surface, (0, 50, 0), (self.x_pos, self.y_pos), self.radius)
            pygame.draw.circle(surface, (50, 100, 50), (self.x_pos, self.y_pos,), self.radius, 2)
            pygame.draw.circle(surface, (50, 100, 50), (self.x_pos, self.y_pos,), int(2*self.radius/3), 2)
            pygame.draw.circle(surface, (50, 100, 50), (self.x_pos, self.y_pos,), int(self.radius/3), 2)
            pygame.draw.line(surface, (50, 100, 50), (self.x_pos - self.radius, self.y_pos), (self.x_pos + self.radius, self.y_pos), 2)
            pygame.draw.line(surface, (50, 100, 50), (self.x_pos, self.y_pos - self.radius), (self.x_pos, self.y_pos + self.radius), 2)
            self.draw_aliens(surface)
            self.draw_asteroids(surface)
            self.draw_radar_hand(surface)
        elif self.broken:
            pygame.draw.circle(surface, (50, 50, 50), (self.x_pos, self.y_pos), self.radius)
            fire_text = const.TITLE_FONT_SM.render("OUT", True, (255, 127, 0))
            surface.blit(fire_text, (self.x_pos - (fire_text.get_width()/2), self.y_pos - 12))
        else: # self.disabled
            pygame.draw.circle(surface, (50, 50, 50), (self.x_pos, self.y_pos), self.radius)
            fire_text = const.TITLE_FONT_SM.render("ON FIRE", True, (255, 127, 0))
            surface.blit(fire_text, (self.x_pos - (fire_text.get_width()/2), self.y_pos - 12))
