"""Similar to images, sounds must be added after initialization
"""
import pygame

SOUNDS = {}

def init_sounds():
    SOUNDS['fire'] = pygame.mixer.Sound('sounds/fire.wav')
    SOUNDS['sprinkler'] = pygame.mixer.Sound('sounds/sprinkler.wav')
    SOUNDS['laser'] = pygame.mixer.Sound('sounds/laser.wav')
    SOUNDS['damage'] = pygame.mixer.Sound('sounds/damage.wav')
    SOUNDS['press'] = pygame.mixer.Sound('sounds/press.wav')
    SOUNDS['invalid'] = pygame.mixer.Sound('sounds/invalid.wav')
