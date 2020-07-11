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