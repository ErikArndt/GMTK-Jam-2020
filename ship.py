import random
import pygame
import room

class Ship:
    def __init__(self, surface):
        self.surface = surface
        self.room_list = [
            room.Room(50, 50, [1, 3]),
            room.Room(150, 50, [0, 4]),
            room.Room(250, 50, [5]),
            room.Room(50, 150, [0, 4]),
            room.Room(150, 150, [1, 3]),
            room.Room(250, 150, [2]),
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
                end_pos = (self.lookup(adj).x_pos + 25, self.lookup(adj).y_pos + 25)
                pygame.draw.line(self.surface, (255, 255, 255), \
                    (rm.x_pos + 25, rm.y_pos + 25), end_pos, 4)
        for rm in self.room_list:
            rm.draw(self.surface)
