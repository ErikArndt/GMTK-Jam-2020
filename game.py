import time
import pygame
import const
from menu import draw_menu
from dashboard import Dashboard
from ship import Ship
from text import TextBox
from levels import LEVEL_DATA

SPRINKLER_LIMIT = 4

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.state = const.MENU
        self.level = 1
        self.dashboard = Dashboard(self.surface)
        self.ship = Ship(self.surface, LEVEL_DATA[self.level]['start_fire'])
        self.active_text_box = None # can only have one at a time

        self.f_tick_time = 5   # seconds between fire ticks
        self.f_anim_time = 0.4 # seconds between fire animation frames
        self.last_f_tick = time.time()
        self.last_f_anim = time.time()

        self.s_tick_time = 3   # seconds between sprinkler ticks
        self.last_s_tick = time.time() - 0.5 # offset so they don't happen simultaneously

        self.r_tick_time = 2   # seconds between radar ticks
        self.last_r_tick = time.time() - 1.5 # offset so they don't happen simultaneously

        self.lightyear_length = 10 # seconds it takes to travel 1 lightyear
        self.last_lightyear_tick = time.time()
        self.lightyears_left = 9

        self.is_paused = False
        self.time_paused = None

    def begin(self):
        """Resets game state and begins a new game.
        """
        self.__init__(self.surface)

    def level_up(self):
        self.level += 1
        self.state = const.PLAYING
        self.dashboard = Dashboard(self.surface) # reset dash
        self.ship = Ship(self.surface, LEVEL_DATA[self.level]['start_fire']) # reset ship
        self.active_text_box = None # clear text box

        self.last_f_tick = time.time()
        self.last_s_tick = time.time() - 0.5 # offset so they don't happen simultaneously

        self.lightyears_left = 9
        self.last_lightyear_tick = time.time()

        if self.level >= 2:
            self.ship.room_list[0].type = const.SHIELD # replace with room-picker

        self.is_paused = False
        self.time_paused = None

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
                self.level_up()
                return

    def pause(self):
        self.is_paused = True
        self.time_paused = time.time()

    def unpause(self):
        self.is_paused = False
        time_missed = time.time() - self.time_paused
        self.last_lightyear_tick += time_missed
        self.last_f_tick += time_missed
        self.last_f_anim += time_missed
        self.last_s_tick += time_missed

    def tick(self):
        """Checks if fire and sprinklers need to activate, checks if you've won or lost,
        and does whatever other things need to happen each frame.
        """
        if self.state == const.PLAYING:
            # Check if you've lost the game
            if self.ship.num_onfire == 0:
                self.state = const.FIRE_OUT
                self.pause()
                game_over_text = 'The fire went out! You\'re relieved for a moment, but then ' + \
                    'you feel your ship begin to stall. Your engines can no longer be powered. ' + \
                    'You and your cactus are screwed.'
                self.active_text_box = TextBox(game_over_text, const.MED, 'GAME OVER')
                self.active_text_box.add_button('Back to Title', const.RED)
            elif self.ship.is_bridge_burning():
                self.state = const.BRIDGE_OUT
                self.pause()
                game_over_text = 'The bridge has burned up, and you along with it! You were ' + \
                    'unable to control the flames, and they consumed you. Not even your brave ' + \
                    'cactus survived.'
                self.active_text_box = TextBox(game_over_text, const.MED, 'GAME OVER')
                self.active_text_box.add_button('Back to Title', const.RED)
            elif self.dashboard.get_health() <= 0:
                self.state = const.HULL_OUT
                self.pause()
                game_over_text = 'The hull is breached! The air in your space ship rushes out into ' + \
                    'the vacuum of space, sucking you out with it. Luckily, by some miracle, your ' + \
                    'cactus manages to survive, and lives to tell your tale.'
                self.active_text_box = TextBox(game_over_text, const.MED, 'GAME OVER')
                self.active_text_box.add_button('Back to Title', const.RED)

            # Check if you've won the game
            if self.lightyears_left <= 0:
                self.state = const.WIN
                self.pause()
                win_text = 'Your ship manages to reach the spaceport intact! You get a much-needed ' + \
                    'chance to refill your water, repair your hull, and catch your breath. But you are ' + \
                    'still a long way from home, so you must keep going!'
                self.active_text_box = TextBox(win_text, const.MED, 'SPACEPORT REACHED')
                self.active_text_box.add_button('Continue to level ' + str(self.level + 1), const.GREEN)

            # Check if you've travelled another lightyear
            current_time = time.time()
            if current_time - self.last_lightyear_tick >= self.lightyear_length:
                self.lightyears_left -= 1
                self.last_lightyear_tick = time.time()
                level_str = LEVEL_DATA[self.level][str(self.lightyears_left)]
                if 'event' in level_str:
                    ## do event thing here
                    print('event should have happened')
                if 'ship_n' in level_str:
                    self.dashboard.radar.add_alien(const.NORTH)
                if 'ship_s' in level_str:
                    self.dashboard.radar.add_alien(const.SOUTH)
                if 'ast_nw' in level_str:
                    self.dashboard.radar.add_asteroid(const.NORTHWEST)
                if 'ast_ne' in level_str:
                    self.dashboard.radar.add_asteroid(const.NORTHEAST)
                if 'ast_sw' in level_str:
                    self.dashboard.radar.add_asteroid(const.SOUTHWEST)
                if 'ast_se' in level_str:
                    self.dashboard.radar.add_asteroid(const.SOUTHEAST)
                if 'repair' in level_str:
                    # make a module break and require repairs
                    print('repair should have happened')

            # Check sprinklers, fire, and radar
            if current_time - self.last_f_tick >= self.f_tick_time:
                self.ship.fire_tick()
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

            if current_time - self.last_r_tick >= self.r_tick_time:
                shields_up = self.ship.is_disabled(const.SHIELD)
                damage_taken = self.dashboard.radar.radar_tick(shields_up)
                self.dashboard.take_damage(damage_taken)
                self.last_r_tick = current_time

    def draw(self):
        if self.state == const.MENU:
            draw_menu(self.surface)

        elif self.state == const.PLAYING:
            self.ship.draw()
            self.dashboard.draw(SPRINKLER_LIMIT - self.ship.num_sprinkling, self.lightyears_left)

        if self.state == const.FIRE_OUT or self.state == const.HULL_OUT or \
            self.state == const.BRIDGE_OUT or self.state == const.WIN:
            self.ship.draw()
            self.dashboard.draw(SPRINKLER_LIMIT - self.ship.num_sprinkling, self.lightyears_left)
            self.active_text_box.draw(self.surface) # these states should always have the text box
