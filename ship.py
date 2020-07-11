import random
import pygame
import room
import const

class Ship:
    def __init__(self, surface):
        self.surface = surface
        self.room_list = [
            room.Room(100, 120, [2, 3], const.EMPTY),
            room.Room(100, 210, [2, 3], const.EMPTY),
            room.Room(200, 120, [0, 3, 4, 5], const.EMPTY),
            room.Room(200, 210, [1, 2, 5, 6], const.EMPTY),
            room.Room(300, 75, [2, 5, 7], const.EMPTY),
            room.Room(300, 165, [2, 3, 4, 6, 8, 9], const.EMPTY),
            room.Room(300, 255, [3, 5, 10], const.EMPTY),
            room.Room(400, 30, [4, 8], const.EMPTY),
            room.Room(400, 120, [5, 7, 9, 11], const.EMPTY),
            room.Room(400, 210, [5, 8, 10, 12], const.EMPTY),
            room.Room(400, 300, [6, 9], const.EMPTY),
            room.Room(500, 120, [8, 13], const.EMPTY),
            room.Room(500, 210, [9, 13], const.EMPTY),
            room.Room(600, 165, [11, 12], const.BRIDGE)
        ]
        self.room_list[0].fire_level = 1

    def fire_tick(self):
        """Increases fire levels of rooms on fire, spreads fire to
        adjacent rooms at random, and returns the number of rooms on fire.

        Returns:
            int: Number of rooms on fire.
        """
        num_onfire = 0
        for i in self.room_list:
            if i.fire_level == 0:
                for j in i.adjacent:
                    if self.lookup(j).fire_level == 2:
                        if random.random() <= i.spread_chance:
                            i.fire_level = 1
                            num_onfire += 1
                            break

            elif i.fire_level == 1:
                i.fire_level = 2
                num_onfire += 1
            elif i.fire_level == 2:
                num_onfire += 1
        return num_onfire

    def sprinkler_tick(self):
        """Reduces fire levels of rooms where sprinklers are on, and returns
        the number of rooms that have sprinklers turned on.

        Returns:
            int: Number of rooms with sprinklers activated.
        """
        num_sprinkling = 0
        for i in self.room_list:
            if i.sprinkling:
                num_sprinkling += 1
                if i.fire_level > 0:
                    i.fire_level -= 1
        return num_sprinkling

    def lookup(self, index):
        return self.room_list[index]

    def draw(self):
        # Draw connections before drawing rooms
        for rm in self.room_list:
            for adj in rm.adjacent:
                adj_room = self.lookup(adj)
                end_pos = (adj_room.x_pos + adj_room.size/2, adj_room.y_pos + adj_room.size/2)
                pygame.draw.line(self.surface, (255, 255, 255), \
                    (rm.x_pos + rm.size/2, rm.y_pos + rm.size/2), end_pos, 4)
        for rm in self.room_list:
            rm.draw(self.surface)
