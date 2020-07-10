class Room:
    def __init__(self, x, y, adjacent): # x and y are the canvas coordinates, used for drawing
        self.x_pos = x
        self.y_pos = y
        self.adjacent = adjacent # this is an array of integers

        self.fire_level = 0
        self.spread_chance = 0.4 # chance that an adjacent level 2 fire spreads to this room
        self.growth_chance = 0.4 # chance that a level 1 fire grows to level 2

        self.sprinkling = False
