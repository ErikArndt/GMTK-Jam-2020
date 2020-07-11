import time
import pygame
import const
from menu import draw_menu
from dashboard import Dashboard
from ship import Ship
from text import TextBox

SPRINKLER_LIMIT = 4

class Game:
    def __init__(self, surface):
        self.surface = surface
        # technically I could just call self.begin() here, but pylint
        # gets mad at me when I don't define all fields in __init__
        self.state = const.MENU
        self.dashboard = Dashboard(self.surface)
        self.ship = Ship(self.surface)
        self.active_text_box = None # can only have one at a time

        self.f_tick_time = 5   # seconds between fire ticks
        self.f_anim_time = 0.4 # seconds between fire animation frames
        self.s_tick_time = 3   # seconds between sprinkler ticks
        self.last_f_tick = time.time()
        self.last_f_anim = time.time()
        self.last_s_tick = time.time() - 0.5 # offset so they don't happen simultaneously

    def begin(self):
        """Resets game state and begins a new game.
        """
        self.state = const.MENU
        self.dashboard = Dashboard(self.surface)
        self.ship = Ship(self.surface)
        self.active_text_box = None # can only have one at a time

        self.f_tick_time = 5 # seconds between fire ticks
        self.s_tick_time = 3 # seconds between sprinkler ticks
        self.last_f_tick = time.time()
        self.last_s_tick = time.time() - 0.5 # offset so they don't happen simultaneously

    def press_key(self, key):
        if key == pygame.K_SPACE: # spacebar
            if self.state == const.MENU:
                self.state = const.PLAYING

    def move_mouse(self, mouse_x, mouse_y):
        for room in self.ship.room_list:
            if mouse_x > room.x_pos and mouse_x < room.x_pos + room.size and \
                mouse_y > room.y_pos and mouse_y < room.y_pos + room.size:
                room.moused_over = True
            else:
                room.moused_over = False
        if self.active_text_box and len(self.active_text_box.buttons) > 0:
            for btn in self.active_text_box.buttons:
                btn.check_mouse_hover(mouse_x, mouse_y)

    def click_mouse(self):
        # This function currently does not need mouse_x or mouse_y, but
        # it might need it in the future depending on what we use it for.
        if self.state == const.MENU:
            self.state = const.PLAYING

        # Should these be restricted to certain game states?
        for room in self.ship.room_list:
            if room.moused_over:
                if room.sprinkling:
                    room.sprinkling = False
                    self.ship.num_sprinkling -= 1
                elif not room.sprinkling and self.ship.num_sprinkling < SPRINKLER_LIMIT:
                    room.sprinkling = True
                    self.ship.num_sprinkling += 1
        if self.active_text_box and len(self.active_text_box.buttons) > 0:
            # Here is where I'll have to figure out how to add functionality
            # to the buttons. I might just have to do this on a case-by-case basis.
            # I know the first button of the FIRE_OUT text goes to the title screen.
            if self.active_text_box.buttons[0].moused_over and self.state == const.FIRE_OUT:
                self.begin()

    def tick(self):
        """Checks if fire and sprinklers need to activate, and whatever other things need
        to happen each frame.
        """
        if self.state == const.PLAYING:
            # Check if you've lost the game
            if self.ship.num_onfire == 0:
                self.state = const.FIRE_OUT
                game_over_text = 'The fire went out! You\'re relieved for a moment, but then ' + \
                    'you feel your ship begin to stall. Your engines can no longer be powered. ' + \
                    'You and your cactus are screwed.'
                self.active_text_box = TextBox(game_over_text, const.MED, 'GAME OVER')
                self.active_text_box.add_button('Back to Title', const.RED)
                # self.active_text_box.add_button('Play again', (50, 50, 255))
                # self.active_text_box.add_button('Punch Cactus', (0, 255, 0))

            # Update which systems are disabled
            self.ship.check_systems()
            self.dashboard.sensors.disabled = self.ship.disabled_systems[2]

            # Check sprinklers and fire
            current_time = time.time()
            if current_time - self.last_f_tick >= self.f_tick_time:
                self.ship.fire_tick()
                self.dashboard.take_damage() # for testing
                self.last_f_tick = current_time
            if current_time - self.last_f_anim >= self.f_anim_time:
                for i in self.ship.room_list:
                    if i.fire_anim_state >= 2:
                        i.fire_anim_state = 0
                    else:
                        i.fire_anim_state += 1
                    self.last_f_anim = current_time
            if current_time - self.last_s_tick >= self.s_tick_time:
                if self.ship.num_sprinkling <= self.dashboard.get_water():
                    self.ship.sprinkler_tick()
                    self.dashboard.lose_water(self.ship.num_sprinkling)
                    self.last_s_tick = current_time
                else:
                    self.ship.sprinkler_tick(self.dashboard.get_water())
                    self.dashboard.lose_water(self.dashboard.get_water())
                    self.last_s_tick = current_time

    def draw(self):
        if self.state == const.MENU:
            draw_menu(self.surface)

        elif self.state == const.PLAYING:
            self.ship.draw()
            self.dashboard.draw()

        if self.state == const.FIRE_OUT:
            self.ship.draw()
            self.dashboard.draw()
            self.active_text_box.draw(self.surface) # this state should always have the text box
