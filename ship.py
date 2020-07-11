import random
import room

roomArray = [] # to be filled with room objects
tempRoom = room.Room(50, 50, [1, 3])
roomArray.append(tempRoom)
tempRoom = room.Room(150, 50, [0, 4])
roomArray.append(tempRoom)
tempRoom = room.Room(250, 50, [5])
roomArray.append(tempRoom)
tempRoom = room.Room(50, 150, [0, 4])
roomArray.append(tempRoom)
tempRoom = room.Room(150, 150, [1, 3])
roomArray.append(tempRoom)
tempRoom = room.Room(250, 150, [2])
roomArray.append(tempRoom)

roomArray[0].fireLevel = 1

def fireTick():
    for i in roomArray:
        if i.fireLevel == 0:
            for j in i.adjacent:
                if lookUp(j).fireLevel == 2:
                    if random.random() <= i.spreadChance:
                        i.fireLevel = 1
                        break
                
        elif i.fireLevel == 1:
            i.fireLevel = 2
    return

def lookUp(index):
    return roomArray[index]