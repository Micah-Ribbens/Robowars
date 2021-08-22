from UtilityClasses import GameCharacters, Segment, SideScrollableComponents
from important_variables import (
    screen_height,
    screen_length,
    window,
    y_velocities
    # consistency_keeper
)
from items import Whip
from engines import *
import pygame
from time import time
import math
from velocity_calculator import VelocityCalculator
from history_keeper import HistoryKeeper
# TODO create class to clean up attributes
class Player(GameCharacters):
    item = None
    running_velocity = VelocityCalculator.give_velocity(screen_length, 448)
    downwards_velocity = VelocityCalculator.give_velocity(screen_height, 1121)
    amount_jumped = 0
    is_facing_right = False
    can_move_down = True
    on_platform = False
    can_move_left = True
    can_move_right = True
    can_jump = True
    is_jumping = False
    upwards_velocity = y_velocities
    max_jump_height = VelocityCalculator.give_measurement(screen_height, 40)
    jump_key_held_down = False
    space_held_in = False
    # So player hangs a bit in air when reaches max jump height
    stay_up_in_air = False
    apex_time = 0
    game_is_sidescrolling = False
        
    def __init__(self):
        self.item = Whip(self)
        self.current_health = 20
        self.full_health = 20
        self.color = self.light_gray
        self.x_coordinate = 100
        self.y_coordinate = screen_height - 200
        self.invincibility__max_time = .6
        self.length = VelocityCalculator.give_measurement(screen_length, 5)
        self.height = VelocityCalculator.give_measurement(screen_height, 15)
    
    def draw(self):
        eye_color = (0,0,255)
        mouth_color = GameObject.red

        eye1 = Segment(
            is_percentage=True, 
            color=eye_color, 
            amount_from_top=20, 
            amount_from_left=25, 
            length_amount=20, 
            width_amount=20)

        eye2 = Segment(
            is_percentage=True, 
            color=eye_color, 
            amount_from_top=eye1.amount_from_top, 
            amount_from_left=eye1.right_edge + 10, 
            length_amount=eye1.length_amount, 
            width_amount=eye1.width_amount)

        mouth = Segment(
            is_percentage=True, 
            color=mouth_color, 
            amount_from_top=60, 
            amount_from_left=10, 
            length_amount=80, 
            width_amount=10)

        self.draw_in_segments([eye1, eye2, mouth])




    # I.E. if the player holds in the up key and landsThe player would jump again, so this function 
    # tells if that is going to happen and if it is it allows the caller of function to prevent it
    def is_continuous_event(self, event, event_name):
        HistoryKeeper.add(event, event_name)
        if HistoryKeeper.get_last(event_name) and event:
            return True
        return False

    def is_height_for_apex(self):
        return self.amount_jumped >= self.max_jump_height

    # For all functions that have movement syntax is "do" = always does it,
    # Otherwise logic inside function to figure out if that movement should be done
    def rightwards_movement(self, right_key_is_held_down):
        if not right_key_is_held_down or not self.can_move_right:
            self.game_is_sidescrolling = False
            return

        self.is_facing_right = True
        location_to_sidescroll = VelocityCalculator.give_measurement(screen_length, 20)
        self.game_is_sidescrolling = self.x_coordinate >= location_to_sidescroll

        if self.x_coordinate >= location_to_sidescroll:
            SideScrollableComponents.side_scroll_all(VelocityCalculator.calc_distance(self.running_velocity))

        else:
            self.x_coordinate += VelocityCalculator.calc_distance(self.running_velocity)

    def upwards_movement(self, jump_key_held_down):
        if self.on_platform:
            # Makes sure doesn't keep jumping up and down
            self.can_jump = not self.is_continuous_event(jump_key_held_down, "jump")
                                        
        # If the player is jumping and the jump_key isn't held down,
        # The player has to be in the apex
        jump_key_was_released = self.is_jumping and not jump_key_held_down
        last_player = HistoryKeeper.get_last("player")
        # In the first iteration there is no last player, so this protects code from NoneType Error
        if last_player is None:
            pass

        elif self.is_height_for_apex() or (last_player.can_jump and not self.can_jump) or self.apex_time > 0 or jump_key_was_released:
            self.can_jump = False
            self.do_apex()

        # If the player is at the apex, the player shouldn't be able to jump
        elif self.can_jump and jump_key_held_down:
            self.do_jump()

    def movement(self):
        # If the character gets hit and thus is flinching the character shouldn't be able to move
        if self.is_flinching:
            self.item.stop_item_usage()
            self.flinch()
            return
        if self.is_invincible:
            self.do_invincibility()
            self.color = self.white
        else:
            self.color = self.light_gray

        controlls = pygame.key.get_pressed()
        self.rightwards_movement(controlls[pygame.K_RIGHT])
        self.upwards_movement(controlls[pygame.K_UP])

        if controlls[pygame.K_LEFT] and self.can_move_left:
            self.x_coordinate -= VelocityCalculator.calc_distance(self.running_velocity)
            self.is_facing_right = False

        if controlls[pygame.K_DOWN] and self.can_move_down:
            self.y_coordinate += VelocityCalculator.calc_distance(self.downwards_velocity)

        use_item_key = pygame.K_SPACE
        if (not self.is_continuous_event(controlls[use_item_key], "use_item")
                and controlls[use_item_key]):

            self.item.use_item()

    def do_apex(self):
        apex_time_needed = .1
        if self.apex_time >= apex_time_needed:
            self.is_jumping = False
            self.apex_time = 0
            self.amount_jumped = 0

        else:
            self.apex_time += VelocityCalculator.time

    def do_jump(self):
        self.y_coordinate -= VelocityCalculator.calc_distance(self.upwards_velocity)
        self.amount_jumped += VelocityCalculator.calc_distance(self.upwards_velocity)
        self.is_jumping = True
        # if self.on_platform:
        #     self.amount_jumped = 0 + VelocityCalculator.calc_distance(self.upwards_velocity)

        # elif self.is_jumping:

    # TODO why max should be be time_in_air from jumping from one platform to the next
    def time_in_air(self, new_platform_y_coordinate, last_platform_y_coordinate, gravity):
        upwards_time = 0
        max_y_coordinate = 0
        # The players bottom is on the platform meaning once jumping the height has to be accounted
        # For since the top of player is the bottom - height
        jumping_change_in_y = self.max_jump_height - self.height
        if last_platform_y_coordinate - jumping_change_in_y <= 0:
            upwards_time = (last_platform_y_coordinate - self.height) / self.upwards_velocity
            max_y_coordinate = self.height

        else:
            max_y_coordinate = last_platform_y_coordinate - self.max_jump_height
            upwards_time = self.max_jump_height / self.upwards_velocity

        downwards_time = (new_platform_y_coordinate - max_y_coordinate) / gravity

        return upwards_time + downwards_time

    def reset(self):
        self.x_coordinate = 50
        self.y_coordinate = 50

