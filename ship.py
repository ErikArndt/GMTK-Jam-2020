import random

room_list = [] # to be filled with room objects

def fire_tick():
    for i in room_list:
        if i.fire_level == 0:
            for j in i.adjacent:
                if lookup(j).fire_level == 2:
                    if random.random() <= i.spreadChance:
                        i.fire_level = 1
                        break

        elif i.fire_level == 1:
            if random.random() <= i.growthChance:
                i.fire_level = 2
    return

def lookup(index):
    return room_list[index]
