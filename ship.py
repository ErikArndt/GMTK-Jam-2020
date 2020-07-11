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
        for i in self.room_list:
            if i.fire_level == 0:
                for j in i.adjacent:
                    if self.lookup(j).fire_level == 2:
                        if random.random() <= i.spread_chance:
                            i.fire_level = 1
                            break

            elif i.fire_level == 1:
                i.fire_level = 2

    def sprinkler_tick(self):
        for i in self.room_list:
            if i.sprinkling and i.fire_level > 0:
                i.fire_level -= 1
                # also put code here for depleting water resources once we get that set up

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
