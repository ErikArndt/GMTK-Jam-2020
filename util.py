"""This module is for general use functions that can be used by any module.
"""
import pygame

def bevelled_rect(surface, colour, rect, border_radius):
    """pygame doesn't support rects with curved edges yet, so I had to write this myself.

    Args:
        surface (pygame.Surface): surface to draw the rect onto.
        colour (rgb value): colour of the rect
        rect ((x, y, width, height)): dimensions of the rect
        border_radius (int): radius of the circular corners of the rect. Must be less than
                            min(width/2, height/2)
    """
    if border_radius >= min(rect[2]/2, rect[3]/2):
        return
    # corners
    pygame.draw.circle(surface, colour, (rect[0] + border_radius, rect[1] + border_radius), border_radius)
    pygame.draw.circle(surface, colour, (rect[0] + rect[2] - border_radius, rect[1] + border_radius), border_radius)
    pygame.draw.circle(surface, colour, (rect[0] + border_radius, rect[1] + rect[3] - border_radius), border_radius)
    pygame.draw.circle(surface, colour, (rect[0] + rect[2] - border_radius, \
        rect[1] + rect[3] - border_radius), border_radius)
    # edges
    pygame.draw.rect(surface, colour, (rect[0] + border_radius, rect[1], \
        rect[2] - border_radius*2, border_radius))
    pygame.draw.rect(surface, colour, (rect[0] + border_radius, rect[1] + rect[3] - border_radius, \
        rect[2] - border_radius*2, border_radius))
    pygame.draw.rect(surface, colour, (rect[0], rect[1] + border_radius, \
        border_radius, rect[3] - border_radius*2))
    pygame.draw.rect(surface, colour, (rect[0] + rect[2] - border_radius, rect[1] + border_radius, \
        border_radius, rect[3] - border_radius*2))
    # center
    pygame.draw.rect(surface, colour, (rect[0] + border_radius, rect[1] + border_radius, \
        rect[2] - border_radius*2, rect[3] - border_radius*2))

def lighten(rgb, factor=30):
    """This function lightens an rgb value by the given factor, or by 30 if no factor is given.

    Args:
        rgb (rgb value): the rgb value to lighten.
        factor (int, optional): the amount to add to r, g, and b. Defaults to 30.

    Returns:
        rgb value: the lightened rgb value.
    """
    return (min(255, rgb[0] + factor), min(255, rgb[1] + factor), min(255, rgb[2] + factor))

def darken(rgb, factor=30):
    """This function darkens an rgb value by the given factor, or by 30 if no factor is given.

    Args:
        rgb (rgb value): the rgb value to darken.
        factor (int, optional): the amount to subtract from r, g, and b. Defaults to 30.

    Returns:
        rgb value: the darkened rgb value.
    """
    return (max(0, rgb[0] - factor), max(0, rgb[1] - factor), max(0, rgb[2] - factor))
