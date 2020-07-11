"""With Captain Wifi we ended up needing a lot of different
images, so I figured it would be handy to put them in a separate
file.
Import the IMAGES dict from this module, and retrieve an image like so:
IMAGES['cactus']
"""
import pygame

IMAGES = {}

def init_images():
    """Images must be loaded after creating the pygame display, so we need
    a method to call that loads images at the right time. This is that method.
    """
    # Placeholder image
    IMAGES['cactus'] = pygame.image.load('Cactus_coolboy.png').convert_alpha()

    # Rooms
    IMAGES['empty_room'] = pygame.image.load('room_template.png').convert_alpha()
    IMAGES['empty_room'] = pygame.transform.scale(IMAGES['empty_room'], (70, 70))

    # Fire
    IMAGES['fire_lvl_1'] = []
    IMAGES['fire_lvl_1'].append(pygame.image.load('lvl_1_frame_1.png').convert_alpha())
    IMAGES['fire_lvl_1'].append(pygame.image.load('lvl_1_frame_2.png').convert_alpha())
    IMAGES['fire_lvl_1'].append(pygame.image.load('lvl_1_frame_3.png').convert_alpha())

    IMAGES['fire_lvl_2'] = []
    IMAGES['fire_lvl_2'].append(pygame.image.load('lvl_1_frame_1.png').convert_alpha())
    IMAGES['fire_lvl_2'].append(pygame.image.load('lvl_1_frame_1.png').convert_alpha())
    IMAGES['fire_lvl_2'].append(pygame.image.load('lvl_1_frame_1.png').convert_alpha()) # will change these once we get the lvl 2 fire images

    for i in range(len(IMAGES['fire_lvl_1'])):
        IMAGES['fire_lvl_1'][i] = pygame.transform.scale(IMAGES['fire_lvl_1'][i], (70, 70))
    
    for i in range(len(IMAGES['fire_lvl_2'])):
        IMAGES['fire_lvl_2'][i] = pygame.transform.scale(IMAGES['fire_lvl_2'][i], (70, 70))