import time
import random
import pygame
import const
import util
from menu import draw_menu
from dashboard import Dashboard
from ship import Ship
from text import TextBox
from levels import LEVEL_DATA
from sound import SOUNDS
import tutorial

SPRINKLER_LIMIT = 3

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.state = const.MENU
        self.level = 3
        self.dashboard = Dashboard(self.surface)
        self.ship = Ship(self.surface, LEVEL_DATA[self.level]['start_fire'])
        self.active_text_box = None # can only have one at a time

        self.f_tick_time = 5   # seconds between fire ticks
        self.f_anim_time = 0.4 # seconds between fire animation frames
        self.last_f_tick = time.time()
        self.last_f_anim = time.time()

        self.s_tick_time = 2   # seconds between sprinkler ticks
        self.last_s_tick = time.time() - 0.5 # offset so they don't happen simultaneously
        self.event_room = None
        self.event_target_flvl = 0
        self.event_time = 20
        self.event_start_time = 0

        self.repair_room = None
        self.repair_time = 5
        self.repair_start_time = 0

        self.r_tick_time = 2   # seconds between radar ticks
        self.last_r_tick = time.time() - 1.5 # offset so they don't happen simultaneously

        self.lightyear_length = 10 # seconds it takes to travel 1 lightyear
        self.last_lightyear_tick = time.time()
        self.lightyears_left = 9

        self.damage_anim_start = 0

        self.is_paused = False
        self.time_paused = None

        self.shield_room_id = 0

        self.tut_progress = 0

    def begin(self):
        """Resets game state and begins a new game.
        """
        self.__init__(self.surface)

    def begin_level(self):
        if self.level == 1:
            self.state = const.TUTORIAL
            self.active_text_box = tutorial.get_text(self.tut_progress)
            self.pause()
        elif self.level == 2:
            self.state = const.INSTALLING
            self.pause()
            install_text = 'Seeing as there is an asteroid field between you and the next spaceport, you decide to purchase an ' + \
                'asteroid shield that will protect you from them as long as it\'s not burning. (Click on a room to place it there)'
            self.active_text_box = TextBox(install_text, const.MED, 'NEW SYSTEM')
            self.active_text_box.add_button("Resume", const.GREEN)
        elif self.level == 3:
            self.ship.room_list[self.shield_room_id].type = const.SHIELD
            self.state = const.INSTALLING
            self.pause()
            install_text = 'Antiipating that your systems will soon start breaking down from the fire, you buy a repair system. ' + \
                '(Click on a room to place it there)'
            self.active_text_box = TextBox(install_text, const.MED, 'NEW SYSTEM')
            self.active_text_box.add_button("Resume", const.GREEN)

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

        self.is_paused = False
        self.time_paused = None

        self.begin_level()

    def press_key(self, key):
        if key == pygame.K_SPACE: # spacebar
            if self.state == const.MENU:
                self.begin_level()
        if key == pygame.K_UP:
            if self.state == const.PLAYING and not self.ship.is_disabled(const.LASER_PORT):
                self.dashboard.radar.fire_laser(const.NORTH)
        if key == pygame.K_DOWN:
            if self.state == const.PLAYING and not self.ship.is_disabled(const.LASER_STBD):
                self.dashboard.radar.fire_laser(const.SOUTH)

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
        # dashboard buttons must be checked individually
        self.dashboard.laser_button_n.check_mouse_hover(mouse_x, mouse_y)
        self.dashboard.laser_button_s.check_mouse_hover(mouse_x, mouse_y)
        self.dashboard.cactus_button.check_mouse_hover(mouse_x, mouse_y)
        self.dashboard.repair_switch.check_mouse_hover(mouse_x, mouse_y)

    def click_mouse(self):
        # This function currently does not need mouse_x or mouse_y, but
        # it might need it in the future depending on what we use it for.
        if self.state == const.MENU:
            self.begin_level()
            return

        if self.state == const.PLAYING or self.state == const.REPAIRING:
            for room in self.ship.room_list:
                if room.moused_over:
                    if self.state == const.PLAYING:
                        if room.sprinkling:
                            room.sprinkling = False
                            self.ship.num_sprinkling -= 1
                            SOUNDS['press'].play()
                        elif not room.sprinkling and self.ship.num_sprinkling < SPRINKLER_LIMIT:
                            room.sprinkling = True
                            self.ship.num_sprinkling += 1
                            SOUNDS['press'].play()
                        elif not room.sprinkling: # sprinkler limit reached
                            SOUNDS['invalid'].play()
                    elif self.state == const.REPAIRING:
                        if room.is_breaking:
                            self.repair_room.is_breaking = False
                            self.repair_room = None
                            SOUNDS['press'].play()
                        else:
                            SOUNDS['invalid'].play()

            # dashboard buttons must be checked individually
            if self.dashboard.laser_button_n.moused_over and \
                not self.ship.is_disabled(const.LASER_PORT):
                self.dashboard.radar.fire_laser(const.NORTH)
            if self.dashboard.laser_button_s.moused_over and \
                not self.ship.is_disabled(const.LASER_STBD):
                self.dashboard.radar.fire_laser(const.SOUTH)
            if self.dashboard.cactus_button.moused_over:
                self.pause()
                self.tut_progress = 0
                self.state = const.TUTORIAL
                self.active_text_box = tutorial.get_text(self.tut_progress)
            if self.dashboard.repair_switch.moused_over and \
                not self.ship.is_disabled(const.REPAIR):
                if self.state == const.PLAYING:
                    self.state = const.REPAIRING
                elif self.state == const.REPAIRING:
                    self.state = const.PLAYING

        if self.state == const.INSTALLING:
            for room_id in range(len(self.ship.room_list)):
                if self.ship.room_list[room_id].moused_over and self.ship.room_list[room_id].type == const.EMPTY:
                    if self.level == 2:
                        self.ship.room_list[room_id].type = const.SHIELD
                        self.shield_room_id = room_id
                    elif self.level == 3:
                        self.ship.room_list[room_id].type = const.REPAIR
                    self.state = const.PLAYING
                    SOUNDS['press'].play()
                    self.unpause()
                elif self.ship.room_list[room_id].moused_over:
                    SOUNDS['invalid'].play()

        if self.active_text_box and len(self.active_text_box.buttons) > 0:
            # Here is where I'll have to figure out how to add functionality
            # to the buttons. I might just have to do this on a case-by-case basis.
            button_list = self.active_text_box.buttons
            # I know the first button of the GAME OVER text goes to the title screen.
            if button_list[0].moused_over and (self.state == const.FIRE_OUT or \
                self.state == const.HULL_OUT or self.state == const.BRIDGE_OUT):
                self.begin()
                return
            # The first button of the WIN_LEVEL text advances to the next level.
            if button_list[0].moused_over and self.state == const.WIN_LEVEL:
                self.level_up()
                return
            # The first button of the WIN_GAME text brings you back to the main menu
            if button_list[0].moused_over and self.state == const.WIN_GAME:
                self.begin()
                return
            # The first button of the event text returns to normal gameplay
            if button_list[0].moused_over and self.state == const.EVENT:
                self.unpause()
                self.state = const.PLAYING
                self.active_text_box = None
                return
            if button_list[0].moused_over and self.state == const.INSTALLING:
                self.active_text_box = None
            # The first button of tutorial text advances the tutorial, unless tutorial is finished.
            if button_list[0].moused_over and self.state == const.TUTORIAL:
                if self.tut_progress >= 10: # last tutorial text
                    self.unpause()
                    self.state = const.PLAYING
                    self.active_text_box = None
                    return
                else:
                    self.tut_progress += 1
                    self.active_text_box = tutorial.get_text(self.tut_progress)
                    return
            # The second button of tutorial text skips the tutorial.
            if len(button_list) >= 2 and button_list[1].moused_over and self.state == const.TUTORIAL:
                self.unpause()
                self.state = const.PLAYING
                self.active_text_box = None
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
        self.last_r_tick += time_missed
        self.event_start_time += time_missed
        self.repair_start_time += time_missed

    def start_event(self):
        if self.level == 1:
            num_systems = 4
        elif self.level == 2:
            num_systems = 5
        elif self.level == 3:
            num_systems = 6
        event_room_id = random.randint(2, num_systems)
        for i in self.ship.room_list:
            if i.type == event_room_id:
                self.event_room = i
                self.event_room.is_event = True
        if self.event_room.fire_level <= 1:
            self.event_target_flvl = 2
        elif self.event_room.fire_level == 2:
            self.event_target_flvl = 0
        self.event_start_time = time.time()
        self.state = const.EVENT
        self.pause()
        if self.event_target_flvl == 0:
            event_text = 'The fire in your ship\'s ' + const.ROOM_NAMES[event_room_id] + ' room is starting to wear down the hull. ' + \
                'If you don\'t extinguish it soon, the ship will take damage.'
        else:
            event_text = 'A particularly annoying species of space termites has infested the ' + const.ROOM_NAMES[event_room_id] + ' room! ' + \
                'You can exterminate them by setting the room on fire, but if you take too long they\'ll damage your hull. '
        self.active_text_box = TextBox(event_text, const.MED, 'EVENT')
        self.active_text_box.add_button('Resume', const.GREEN)

    def start_repair(self, room_id):
        for i in self.ship.room_list:
            if i.type == room_id:
                self.repair_room = i
                self.repair_room.is_breaking = True
        self.repair_start_time = time.time()
        self.state = const.EVENT
        self.pause()
        repair_text = 'The ' + const.ROOM_NAMES[room_id] + ' system is breaking! If it isn\'t fixed soon,' + \
            'it will become permanently disabled. (To repair it, click on the repair button and then ' + \
            'on the room you want to repair)'
        self.active_text_box = TextBox(repair_text, const.MED, 'EVENT')
        self.active_text_box.add_button("Resume", const.GREEN)

    def tick(self):
        """Checks if fire and sprinklers need to activate, checks if you've won or lost,
        and does whatever other things need to happen each frame.
        """
        if self.state == const.PLAYING or self.state == const.REPAIRING:
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

            # Check if you've won the level or game
            if self.lightyears_left <= 0:
                if self.level < 3:
                    self.state = const.WIN_LEVEL
                    self.pause()
                    win_text = 'Your ship manages to reach the spaceport intact! You get a much-needed ' + \
                        'chance to refill your water, repair your hull, and catch your breath. But you are ' + \
                        'still a long way from home, so you must keep going!'
                    self.active_text_box = TextBox(win_text, const.MED, 'SPACEPORT REACHED')
                    self.active_text_box.add_button('Continue to level ' + str(self.level + 1), const.GREEN)
                else:
                    self.state = const.WIN_GAME
                    self.pause()
                    win_text = 'You glance away from the hectic state of your ship for a moment only ' + \
                        'to be greeted by the blue and green planet you call home. You\'re finally back ' + \
                        'to Earth! You and your cactus will remember this journey forever.'
                    self.active_text_box = TextBox(win_text, const.MED, 'EARTH REACHED')
                    self.active_text_box.add_button('Woohoo!', const.GREEN)

            # Check if you've travelled another lightyear
            current_time = time.time()
            if current_time - self.last_lightyear_tick >= self.lightyear_length:
                self.lightyears_left -= 1
                self.last_lightyear_tick = time.time()
                level_str = LEVEL_DATA[self.level][str(self.lightyears_left)]
                if 'event' in level_str:
                    self.start_event()
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
                    if 'repair_sn' in level_str:
                        room_id = const.SENSORS
                    elif 'repair_rd' in level_str:
                        room_id = const.RADAR
                    elif 'repair_sh' in level_str:
                        room_id = const.SHIELD
                    # make a module break and require repairs
                    self.start_repair(room_id)
            if self.state == const.REPAIRING and self.ship.disabled_systems[7]:
                self.state = const.PLAYING

            # Check fire
            if current_time - self.last_f_tick >= self.f_tick_time:
                self.ship.fire_tick()
                self.last_f_tick = current_time
                # Update which systems are disabled
                self.ship.check_systems()
                self.dashboard.sensors.disabled = self.ship.disabled_systems[2]
                self.dashboard.radar.disabled = self.ship.disabled_systems[3]
                self.dashboard.laser_n_disabled = self.ship.disabled_systems[4]
                self.dashboard.laser_s_disabled = self.ship.disabled_systems[5]
                self.dashboard.repair_disabled = self.ship.disabled_systems[7]
                # Checks event goal
                if self.event_room is not None and self.event_target_flvl == 2 and self.event_room.fire_level == 2:
                    self.event_room.is_event = False
                    self.event_room = None
            if current_time - self.last_f_anim >= self.f_anim_time:
                for i in self.ship.room_list:
                    if i.fire_anim_state >= 2:
                        i.fire_anim_state = 0
                    else:
                        i.fire_anim_state += 1
                    self.last_f_anim = current_time

            # Check sprinklers
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
                self.dashboard.radar.disabled = self.ship.disabled_systems[3]
                self.dashboard.laser_n_disabled = self.ship.disabled_systems[4]
                self.dashboard.laser_s_disabled = self.ship.disabled_systems[5]
                self.dashboard.repair_disabled = self.ship.disabled_systems[7]
                # Checks event goal
                if self.event_room is not None and self.event_target_flvl == 0 and self.event_room.fire_level <= 1:
                    self.event_room.is_event = False
                    self.event_room = None
            # Check radar
            if current_time - self.last_r_tick >= self.r_tick_time:
                shields_up = not self.ship.is_disabled(const.SHIELD)
                damage_taken = self.dashboard.radar.radar_tick(shields_up)
                self.dashboard.take_damage(damage_taken)
                if damage_taken > 0:
                    self.damage_anim_start = time.time()
                self.last_r_tick = current_time

            # Check events
            if self.event_room is not None and current_time - self.event_start_time >= self.event_time:
                if self.event_target_flvl == 0 and self.event_room.fire_level == 2 or \
                    self.event_target_flvl == 2 and self.event_room.fire_level <= 1:
                    self.dashboard.take_damage(3)
                    self.damage_anim_start = time.time()
                self.event_room.is_event = False
                self.event_room = None

            # Check repair events
            if self.repair_room is not None and current_time - self.repair_start_time >= self.repair_time:
                self.repair_room.is_broken = True
                self.repair_room.is_breaking = False
                self.repair_room = None

    def draw(self):
        if self.state == const.MENU:
            draw_menu(self.surface)

        else:
            self.ship.draw()
            if self.state == const.REPAIRING:
                self.dashboard.draw(SPRINKLER_LIMIT - self.ship.num_sprinkling, self.lightyears_left, self.level, True)
            else:
                self.dashboard.draw(SPRINKLER_LIMIT - self.ship.num_sprinkling, self.lightyears_left, self.level, False)
            if self.active_text_box:
                self.active_text_box.draw(self.surface)
        # red flash when you take damage
        current_time = time.time()
        # from 0 to 0.1, transparency goes from 0 to 100, and then from 0.1 to 0.2 it goes back down
        if current_time - self.damage_anim_start <= 0.1:
            transparency = (current_time - self.damage_anim_start) * 1000
        else:
            transparency = (self.damage_anim_start - current_time + 0.2) * 1000
        
        if current_time - self.damage_anim_start <= 0.2:
            overlay_surface = pygame.Surface((const.WIN_LENGTH, const.WIN_HEIGHT), pygame.HWSURFACE)
            overlay_surface.set_alpha(transparency) # the surface is now semi-transparent
            util.bevelled_rect(overlay_surface, (255, 0, 0), (0, 0, const.WIN_LENGTH, const.WIN_HEIGHT), \
                15)
            self.surface.blit(overlay_surface, (0, 0))
