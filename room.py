import random
class Room:
    def __init__(self, x, y, adjacent): # x and y are the canvas coordinates, used for drawing
        self.x = x
        self.y = y
        self.adjacent = adjacent # this is an array of integers

        self.fireLevel = 0
        self.spreadChance = 0.4 # chance that an adjacent level 2 fire spreads to this room
        self.growthChance = 0.4 # chance that a level 1 fire grows to level 2

        self.sprinkling = False

    def fireTick(self):
        if self.fireLevel == 0:
            for i in self.adjacent:
                if lookUp(i).fireLevel == 2:
                    if random.random() <= self.spreadChance:
                        self.fireLevel = 1
                        break
                
        elif self.fireLevel == 1:
            if random.random() <= self.growthChance:
                self.fireLevel = 2
        return

