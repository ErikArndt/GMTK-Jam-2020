"""Here's where we'll store useful constants
"""
import pygame

pygame.font.init()

## ******* GAME STATES *******
MENU = 0
PLAYING = 1

## ******* COLOURS ***********
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

## ******* SETTINGS **********
WIN_LENGTH = 800 # arbitrary, feel free to change
WIN_HEIGHT = 600 # arbitrary, feel free to change

## ******* FONTS ************
DEFAULT_FONT = pygame.font.Font('nasalization-rg.ttf', 24)
TITLE_FONT = pygame.font.Font('ethnocentric-rg.ttf', 60)
TITLE_FONT_SM = pygame.font.Font('ethnocentric-rg.ttf', 24)
