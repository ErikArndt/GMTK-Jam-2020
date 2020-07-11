import time
import pygame
import const
from menu import draw_menu
from dashboard import Dashboard
from ship import Ship
from text import TextBox

SPRINKLER_LIMIT = 4
LEVEL_CLEAR_TIME = 90 # seconds to survive

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

        self.level = 1
        self.level_start_time = time.time()

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

        self.level = 1
        self.level_start_time = time.time()

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
            # I know the first button of the GAME OVER text goes to the title screen.
            if self.active_text_box.buttons[0].moused_over and (self.state == const.FIRE_OUT or \
                self.state == const.HULL_OUT or self.state == const.BRIDGE_OUT):
                self.begin()
                return
            # The first button of the WIN text advances to the next level.
            if self.active_text_box.buttons[0].moused_over and self.state == const.WIN:
                self.state = const.PLAYING
                self.level += 1
                self.begin()
                return

    def calculate_lightyears(self):
        """Returns how many lightyears the ship must travel to complete the level.
        I haven't playtested this, but how about 10 seconds for 1 lightyear?

        Returns:
            int: lightyears remaining.
        """
        elapsed_time = time.time() - self.level_start_time
        return round((LEVEL_CLEAR_TIME - elapsed_time)/10)

    def tick(self):
        """Checks if fire and sprinklers need to activate, checks if you've won or lost, 
        and does whatever other things need to happen each frame.
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
            elif self.ship.is_bridge_burning():
                self.state = const.BRIDGE_OUT
                game_over_text = 'The bridge has burned up, and you along with it! You were ' + \
                    'unable to control the flames, and they consumed you. Not even your brave ' + \
                    'cactus survived.'
                self.active_text_box = TextBox(game_over_text, const.MED, 'GAME OVER')
                self.active_text_box.add_button('Back to Title', const.RED)
            elif self.dashboard.get_health() <= 0:
                self.state = const.HULL_OUT
                game_over_text = 'The hull is breached! The air in your space ship rushes out into ' + \
                    'the vacuum of space, sucking you out with it. Luckily, by some miracle, your ' + \
                    'cactus manages to survive, and lives to tell your tale.'
                self.active_text_box = TextBox(game_over_text, const.MED, 'GAME OVER')
                self.active_text_box.add_button('Back to Title', const.RED)

            # Check if you've won the game
            if self.calculate_lightyears() <= 0:
                self.state = const.WIN
                win_text = 'Your ship manages to reach the spaceport intact! You get a much-needed ' + \
                    'chance to refill your water, repair your hull, and catch your breath. But you are ' + \
                    'still a long way from home, so you must keep going!'
                self.active_text_box = TextBox(win_text, const.MED, 'SPACEPORT REACHED')
                self.active_text_box.add_button('Continue to level ' + str(self.level + 1), const.GREEN)

            # Check sprinklers and fire
            current_time = time.time()
            if current_time - self.last_f_tick >= self.f_tick_time:
                self.ship.fire_tick()
                self.dashboard.take_damage() # for testing
                self.last_f_tick = current_time

                # Update which systems are disabled
                self.ship.check_systems()
                self.dashboard.sensors.disabled = self.ship.disabled_systems[2]

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

                # Update which systems are disabled
                self.ship.check_systems()
                self.dashboard.sensors.disabled = self.ship.disabled_systems[2] 

    def draw(self):
        if self.state == const.MENU:
            draw_menu(self.surface)

        elif self.state == const.PLAYING:
            self.ship.draw()
            self.dashboard.draw(SPRINKLER_LIMIT - self.ship.num_sprinkling, self.calculate_lightyears())

        if self.state == const.FIRE_OUT or self.state == const.HULL_OUT or \
            self.state == const.BRIDGE_OUT or self.state == const.WIN:
            self.ship.draw()
            self.dashboard.draw(SPRINKLER_LIMIT - self.ship.num_sprinkling, self.calculate_lightyears())
            self.active_text_box.draw(self.surface) # these states should always have the text box
