import random
import pygame
from room import Room
import const

class Ship:
    def __init__(self, surface, starting_fire):
        self.surface = surface
        self.room_list = [
            Room(100, 120, [2, 3], const.EMPTY),
            Room(100, 210, [2, 3], const.RADAR),
            Room(200, 120, [0, 3, 4, 5], const.EMPTY),
            Room(200, 210, [1, 2, 5, 6], const.EMPTY),
            Room(300, 75, [2, 5, 7], const.SENSORS),
            Room(300, 165, [2, 3, 4, 6, 8, 9], const.EMPTY),
            Room(300, 255, [3, 5, 10], const.EMPTY),
            Room(400, 30, [4, 8], const.LASER_PORT),
            Room(400, 120, [5, 7, 9, 11], const.EMPTY),
            Room(400, 210, [5, 8, 10, 12], const.EMPTY),
            Room(400, 300, [6, 9], const.LASER_STBD),
            Room(500, 120, [8, 13], const.EMPTY),
            Room(500, 210, [9, 13], const.EMPTY),
            Room(600, 165, [11, 12], const.BRIDGE)
        ]
        self.room_list[starting_fire].fire_level = 1

        self.num_onfire = 2
        self.num_sprinkling = 0

        # empty, bridge, sensors, radar, laser (port / starboard)
        # see const.py
        self.disabled_systems = [False]*7

    def fire_tick(self):
        """Increases fire levels of rooms on fire, spreads fire to
        adjacent rooms at random.
        """
        for room in self.room_list:
            if room.fire_level == 0:
                for j in room.adjacent:
                    if self.lookup(j).fire_level == 2 and random.random() <= room.spread_chance:
                        room.fire_level = 1
                        self.num_onfire += 1
                        break
            elif room.fire_level == 1:
                room.fire_level = 2

    def sprinkler_tick(self, water_available=-1):
        """Reduces fire levels of rooms where sprinklers are on. If not enough
        water is provided, then only some sprinklers will activate.
        """
        # idk if Python uses pass by reference, so I'm copying this variable just to be safe
        available_water = water_available
        for room in self.room_list:
            if room.sprinkling and room.fire_level > 0 and available_water != 0:
                room.fire_level -= 1
                available_water -= 1
                ## decrement num_onfire if fire was fully extinguished
                if room.fire_level == 0:
                    self.num_onfire -= 1

    def lookup(self, index):
        return self.room_list[index]

    def is_bridge_burning(self):
        """Predicate that indicates whether the bridge is at fire level 2. I
        could instead check if that room is disabled, but, like, I already wrote
        this code, so whatever.

        Returns:
            boolean: True if bridge is at fire level 2, false otherwise.
        """
        # Bridge should be the last room in the list
        last_room = self.room_list[-1]
        if last_room.type == const.BRIDGE:
            return last_room.fire_level == 2
        # iterate through just in case it's not last in the list
        else:
            for room in self.room_list:
                if room.type == const.BRIDGE:
                    return room.fire_level == 2
        return False # if this is reached, then the ship doesn't have a bridge

    def check_systems(self):
        for i in self.room_list:
            if i.type != const.EMPTY:
                if i.fire_level == 2:
                    self.disabled_systems[i.type] = True
                else:
                    self.disabled_systems[i.type] = False

    def is_disabled(self, system):
        return self.disabled_systems[system]

    def draw(self):
        # Draw connections before drawing rooms
        for room in self.room_list:
            for adj in room.adjacent:
                adj_room = self.lookup(adj)
                end_pos = (adj_room.x_pos + adj_room.size/2, adj_room.y_pos + adj_room.size/2)
                pygame.draw.line(self.surface, (255, 255, 255), \
                    (room.x_pos + room.size/2, room.y_pos + room.size/2), end_pos, 4)
        for room in self.room_list:
            room.draw(self.surface)
