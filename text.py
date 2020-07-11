import pygame
import const
import util

BUTTON_HEIGHT = 50
MARGIN = 5 # pixels around text/buttons

class TextBoxButton:
    def __init__(self, text, colour, rect):
        self.text = text
        self.colour = colour
        self.rect = rect
        self.moused_over = False

    def check_mouse_hover(self, mouse_x, mouse_y):
        """Updates the moused_over field based on whether the given x and y
        coordinates are over the button.

        Args:
            mouse_x (int): x coordinate of the mouse.
            mouse_y (int): y coordinate of the mouse.
        """
        if mouse_x > self.rect[0] and mouse_x < self.rect[0] + self.rect[2] and \
            mouse_y > self.rect[1] and mouse_y < self.rect[1] + self.rect[3]:
            self.moused_over = True
        else:
            self.moused_over = False

    def draw(self, surface):
        # Use a lighter colour if mouse is hovering over button
        if self.moused_over:
            light_colour = util.lighten(self.colour)
            pygame.draw.rect(surface, light_colour, self.rect)
        else:
            pygame.draw.rect(surface, self.colour, self.rect)
        button_text = const.DEFAULT_FONT.render(self.text, True, const.BLACK)
        surface.blit(button_text, (self.rect[0] + self.rect[2]/2 - button_text.get_width()/2, \
            self.rect[1] + self.rect[3]/2 - button_text.get_height()/2))

class TextBox:
    def __init__(self, text, size, title=None):
        self.text = text
        # The following values haven't been tweaked yet
        if size == const.SMALL:
            self.width = 200
            self.height = 150
            self.font = const.DEFAULT_FONT_SM
        elif size == const.LARGE:
            self.width = 600
            self.height = 400
            self.font = const.DEFAULT_FONT
        else: # size == const.MED
            self.width = 400
            self.height = 300
            self.font = const.DEFAULT_FONT
        self.x_pos = const.WIN_LENGTH/2 - self.width/2
        self.y_pos = const.WIN_HEIGHT/2 - self.height/2
        self.buttons = [] # must be added with add_button method
        self.title = title

    def add_button(self, text, colour):
        """Adds a button to the bottom of the text box. No more than 3 buttons can
        be added. (Might have to set different limits based on text box size)

        Args:
            text (string): The word or words on the button
            colour (rgb value): The colour of the button

        Returns:
            boolean: True if button was successfully added, false otherwise
        """
        button_x = self.x_pos + MARGIN
        button_y = self.y_pos + self.height - BUTTON_HEIGHT + MARGIN
        button_width = self.width # margins will be subtracted later
        button_height = BUTTON_HEIGHT - MARGIN*2
        if len(self.buttons) >= 3:
            return False
        elif len(self.buttons) == 2:
            ## shift buttons over and calculate new rect
            button_width = round(self.width/3)
            self.buttons[0].rect = (button_x, button_y, button_width - MARGIN*2, button_height)
            self.buttons[1].rect = (button_x + button_width, button_y, button_width - MARGIN*2, button_height)
            new_button_rect = (button_x + button_width*2, button_y, button_width - MARGIN*2, button_height)
        elif len(self.buttons) == 1:
            ## shift button over and calculate new rect
            button_width = round(self.width/2)
            self.buttons[0].rect = (button_x, button_y, button_width - MARGIN*2, button_height)
            new_button_rect = (button_x + button_width, button_y, button_width - MARGIN*2, button_height)
        else: # len(self.buttons) == 0
            new_button_rect = (button_x, button_y, button_width - MARGIN*2, button_height)
        self.buttons.append(TextBoxButton(text, colour, new_button_rect))
        return True

    def set_position(self, x_pos, y_pos):
        """Sets the text box position on the screen. (Default position is center)

        Args:
            x_pos (int): Left edge of the text box
            y_pos (int): Top edge of the text box
        """
        self.x_pos = x_pos
        self.y_pos = y_pos

    def draw(self, surface):
        """Draws the text box on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw the text box onto.
        """
        # Until I have a real image, a white rectangle with a gray border will have to do
        pygame.draw.rect(surface, const.GRAY, (self.x_pos - 5, self.y_pos - 5, \
            self.width + 10, self.height + 10), 10)
        pygame.draw.rect(surface, const.WHITE, (self.x_pos, self.y_pos, self.width, self.height))

        if len(self.buttons) > 0:
            text_rect = (self.x_pos + MARGIN, self.y_pos + MARGIN, \
                self.width - MARGIN*2, self.height - MARGIN*2 - BUTTON_HEIGHT)
        else:
            text_rect = (self.x_pos + MARGIN, self.y_pos + MARGIN, \
                self.width - MARGIN*2, self.height - MARGIN*2)
        draw_text(surface, self.text, const.BLACK, text_rect, self.font, True)
        for button in self.buttons:
            button.draw(surface)

        # again, until I have a real image, a white rectangle is the best title you're getting
        title_text = const.TITLE_FONT_SM.render(self.title, True, const.BLACK)
        title_x = round(self.x_pos + self.width/2 - title_text.get_width()/2)
        title_y = round(self.y_pos - title_text.get_height())
        pygame.draw.rect(surface, const.GRAY, (title_x - 5, title_y - 5, title_text.get_width() + 10, \
            title_text.get_height() + 10), 10)
        pygame.draw.rect(surface, const.WHITE, (title_x, title_y, title_text.get_width(), \
            title_text.get_height()))
        surface.blit(title_text, (title_x, title_y))

def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    '''
    draw some text into an area of a surface
    automatically wraps words
    returns any text that didn't get blitted

    drawText: pygame surface, string, rgb value, rect, pygame font -> string
    '''
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = -2

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text
