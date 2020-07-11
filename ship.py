import random
import room

room_list = [] # to be filled with room objects
temp_room = room.Room(50, 50, [1, 3])
room_list.append(temp_room)
temp_room = room.Room(150, 50, [0, 4])
room_list.append(temp_room)
temp_room = room.Room(250, 50, [5])
room_list.append(temp_room)
temp_room = room.Room(50, 150, [0, 4])
room_list.append(temp_room)
temp_room = room.Room(150, 150, [1, 3])
room_list.append(temp_room)
temp_room = room.Room(250, 150, [2])
room_list.append(temp_room)

room_list[0].fireLevel = 1

def fire_tick():
    for i in room_list:
        if i.fire_level == 0:
            for j in i.adjacent:
                if lookup(j).fire_level == 2:
                    if random.random() <= i.spreadChance:
                        i.fire_level = 1
                        break

        elif i.fire_level == 1:
            i.fire_level = 2
    return

def lookup(index):
    return room_list[index]
