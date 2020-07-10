import random

roomArray = [] # to be filled with room objects

def fireTick():
    for i in roomArray:
        if i.fireLevel == 0:
            for j in i.adjacent:
                if lookUp(j).fireLevel == 2:
                    if random.random() <= i.spreadChance:
                        i.fireLevel = 1
                        break
                
        elif i.fireLevel == 1:
            if random.random() <= i.growthChance:
                i.fireLevel = 2
    return

def lookUp(index):
    return roomArray[index]