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
    IMAGES['cactus'] = pygame.image.load('images/Cactus_coolboy.png').convert_alpha()

    # Ship
    IMAGES['ship'] = pygame.image.load('images/our_ship.png').convert_alpha()

    # Rooms
    IMAGES['empty_room'] = pygame.image.load('images/room_template.png').convert_alpha()
    IMAGES['empty_room'] = pygame.transform.scale(IMAGES['empty_room'], (70, 70))
    bridge_img = pygame.image.load('images/bridge.png').convert_alpha()
    IMAGES['bridge_room'] = pygame.transform.scale(bridge_img, (70, 70))

    # Fire
    IMAGES['fire_lvl_1'] = []
    IMAGES['fire_lvl_1'].append(pygame.image.load('images/lvl_1_frame_1.png').convert_alpha())
    IMAGES['fire_lvl_1'].append(pygame.image.load('images/lvl_1_frame_2.png').convert_alpha())
    IMAGES['fire_lvl_1'].append(pygame.image.load('images/lvl_1_frame_3.png').convert_alpha())

    IMAGES['fire_lvl_2'] = []
    IMAGES['fire_lvl_2'].append(pygame.image.load('images/FLAME lvl 2 frame 1.png').convert_alpha())
    IMAGES['fire_lvl_2'].append(pygame.image.load('images/FLAME lvl 2 frame 2.png').convert_alpha())
    IMAGES['fire_lvl_2'].append(pygame.image.load('images/FLAME lvl 2 frame 3.png').convert_alpha())

    for i in range(len(IMAGES['fire_lvl_1'])):
        IMAGES['fire_lvl_1'][i] = pygame.transform.scale(IMAGES['fire_lvl_1'][i], (70, 70))

    for i in range(len(IMAGES['fire_lvl_2'])):
        IMAGES['fire_lvl_2'][i] = pygame.transform.scale(IMAGES['fire_lvl_2'][i], (70, 70))

    # Sprinkler
    IMAGES['sprinkler'] = pygame.image.load('images/sprinkler transparent.png').convert_alpha()

    # Radar objects
    alien_ship_img = pygame.image.load('images/ship.png').convert_alpha()
    IMAGES['alien_ship'] = pygame.transform.scale(alien_ship_img, (20, 20))
    asteroid_img = pygame.image.load('images/asteroid.png').convert_alpha()
    IMAGES['asteroid'] = pygame.transform.scale(asteroid_img, (30, 30))

    # Room Symbols
    sensor_symbol = pygame.image.load('images/sensor transparent.png').convert_alpha()
    IMAGES['sensor_symbol'] = pygame.transform.scale(sensor_symbol, (40, 40))
    radar_symbol = pygame.image.load('images/radar transparent.png').convert_alpha()
    IMAGES['radar_symbol'] = pygame.transform.scale(radar_symbol, (40, 40))
    laser_symbol = pygame.image.load('images/laser transparent.png').convert_alpha()
    IMAGES['laser_symbol'] = pygame.transform.scale(laser_symbol, (40, 40))
    IMAGES['laser_symbol_180'] = pygame.transform.rotate(IMAGES['laser_symbol'], 180)
    shield_symbol = pygame.image.load('images/shield tansparent.png').convert_alpha()
    IMAGES['shield_symbol'] = pygame.transform.scale(shield_symbol, (40, 40))
    repair_symbol = pygame.image.load('images/repair transparent.png').convert_alpha()
    IMAGES['repair_symbol'] = pygame.transform.scale(repair_symbol, (40, 40))

    # Dashboard
    dashboard_nolever = pygame.image.load('images/dashboard_sans_lever.png').convert_alpha()
    IMAGES['dashboard_sans_lever'] = pygame.transform.scale(dashboard_nolever, (800, 200))
    dashboard_img = pygame.image.load('images/dashboard transparent.png').convert_alpha()
    IMAGES['dashboard'] = pygame.transform.scale(dashboard_img, (800, 200))
    flipped_lever = pygame.image.load('images/flipped lever.png').convert_alpha()
    IMAGES['lever'] = pygame.transform.scale(flipped_lever, (125, 45))
        