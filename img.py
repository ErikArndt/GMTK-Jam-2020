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
    IMAGES['fire_lvl_2'].append(pygame.image.load('FLAME lvl 2 frame 1.png').convert_alpha())
    IMAGES['fire_lvl_2'].append(pygame.image.load('FLAME lvl 2 frame 2.png').convert_alpha())
    IMAGES['fire_lvl_2'].append(pygame.image.load('FLAME lvl 2 frame 3.png').convert_alpha())

    for i in range(len(IMAGES['fire_lvl_1'])):
        IMAGES['fire_lvl_1'][i] = pygame.transform.scale(IMAGES['fire_lvl_1'][i], (70, 70))

    for i in range(len(IMAGES['fire_lvl_2'])):
        IMAGES['fire_lvl_2'][i] = pygame.transform.scale(IMAGES['fire_lvl_2'][i], (70, 70))

    # Sprinkler (Don't actually use this one, it's not technically ours)
    IMAGES['sprinkler'] = pygame.image.load('stardew_sprinkler.png').convert_alpha()

    # Radar objects
    alien_ship_img = pygame.image.load('ship.png').convert_alpha()
    IMAGES['alien_ship'] = pygame.transform.scale(alien_ship_img, (20, 20))
    asteroid_img = pygame.image.load('asteroid.png').convert_alpha()
    IMAGES['asteroid'] = pygame.transform.scale(asteroid_img, (30, 30))
