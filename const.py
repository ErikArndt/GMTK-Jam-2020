"""Here's where we'll store useful constants
"""
import pygame

pygame.font.init()

## ******* GAME STATES *******
MENU = 0
PLAYING = 1
FIRE_OUT = 2
HULL_OUT = 3

## ******* COLOURS ***********
BLACK = (0, 0, 0) # could also use pygame.Color('white'), but idk the difference
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
RED = (255, 0, 0)

## ******* SETTINGS **********
WIN_LENGTH = 800 # arbitrary, feel free to change
WIN_HEIGHT = 600 # arbitrary, feel free to change

## ******* FONTS ************
DEFAULT_FONT = pygame.font.Font('nasalization-rg.ttf', 24)
DEFAULT_FONT_SM = pygame.font.Font('nasalization-rg.ttf', 16)
TITLE_FONT = pygame.font.Font('ethnocentric-rg.ttf', 60)
TITLE_FONT_SM = pygame.font.Font('ethnocentric-rg.ttf', 24)

## **** TEXT BOX SIZES ******
SMALL = 0
MED = 1
LARGE = 2
