"""Here's where we'll store useful constants
"""
import pygame

pygame.font.init()

## ******* GAME STATES *******
MENU = 0
PLAYING = 1
FIRE_OUT = 2
HULL_OUT = 3
BRIDGE_OUT = 4
WIN_LEVEL = 5
EVENT = 6
WIN_GAME = 7

## ******* ROOM TYPES *******
EMPTY = 0
BRIDGE = 1
SENSORS = 2
RADAR = 3
LASER_PORT = 4
LASER_STBD = 5
SHIELD = 6

room_names = ['empty', 'bridge', 'sensors', 'radar', 'port laser', 'starboard laser', 'shield']

## ******* COLOURS ***********
BLACK = (0, 0, 0) # could also use pygame.Color('white'), but idk the difference
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (50, 50, 255)
ORANGE = (255, 127, 0)

## ******* SETTINGS **********
WIN_LENGTH = 800 # arbitrary, feel free to change
WIN_HEIGHT = 600 # arbitrary, feel free to change

## ******* FONTS ************
DEFAULT_FONT = pygame.font.Font('fonts/nasalization-rg.ttf', 24)
DEFAULT_FONT_SM = pygame.font.Font('fonts/nasalization-rg.ttf', 16)
TITLE_FONT = pygame.font.Font('fonts/ethnocentric-rg.ttf', 48)
TITLE_FONT_SM = pygame.font.Font('fonts/ethnocentric-rg.ttf', 24)
DIGITAL_FONT = pygame.font.Font('fonts/digital-readout-rg.ttf', 60) # mainly used for numbers

## **** TEXT BOX SIZES ******
SMALL = 0
MED = 1
LARGE = 2

## **** RADAR DIRECTIONS ****
NORTH = 0
SOUTH = 1 # we don't currently have anything that comes from east or west
NORTHEAST = 2
SOUTHEAST = 3
SOUTHWEST = 4
NORTHWEST = 5
