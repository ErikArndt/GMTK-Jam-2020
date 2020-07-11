"""This module contains not only the code for the radar on the dashboard,
but also all the objects that can appear on the radar, such as alien
ships and asteroids.
"""
import time
import math
import pygame
import const

class Alien:
    def __init__(self, direction, is_waiting):
        self.direction = direction
        self.is_waiting = is_waiting
        self.distance = 3 # rings away from center

    def move(self):
        if not self.is_waiting:
            self.distance -= 1

class Asteroid:
    def __init__(self, direction):
        self.direction = direction
        self.distance = 3 # rings away from center

    def move(self):
        self.distance -= 1

class Radar:
    def __init__(self, x_pos, y_pos, radius):
        self.x_pos = x_pos # center
        self.y_pos = y_pos # center
        self.radius = radius
        self.animation_length = 2 # seconds it takes for a full rotation
        self.last_rotation_time = time.time()
        self.aliens = []
        self.asteroids = []
        self.disabled = False

    def radar_tick(self, shields_up):
        damage_taken = 0
        for alien in self.aliens:
            if alien.distance > 1:
                alien.move()
            else:
                damage_taken += 1
        for asteroid in self.asteroids:
            if asteroid.distance > 1:
                asteroid.move()
            elif shields_up:
                self.asteroids.remove(asteroid)
            else:
                damage_taken += 1
                self.asteroids.remove(asteroid)

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

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 50, 0), (self.x_pos, self.y_pos), self.radius)
        pygame.draw.circle(surface, (50, 100, 50), (self.x_pos, self.y_pos,), self.radius, 2)
        pygame.draw.circle(surface, (50, 100, 50), (self.x_pos, self.y_pos,), int(2*self.radius/3), 2)
        pygame.draw.circle(surface, (50, 100, 50), (self.x_pos, self.y_pos,), int(self.radius/3), 2)
        pygame.draw.line(surface, (50, 100, 50), (self.x_pos - self.radius, self.y_pos), (self.x_pos + self.radius, self.y_pos), 2)
        pygame.draw.line(surface, (50, 100, 50), (self.x_pos, self.y_pos - self.radius), (self.x_pos, self.y_pos + self.radius), 2)
        self.draw_radar_hand(surface)
