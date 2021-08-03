from UtilityClasses import GameCharacters, SideScrollableComponents
from important_variables import (
    screen_height,
    screen_length,
    win,
    y_velocities
    # consistency_keeper
)
from items import Whip
from engines import *
import pygame
from time import time
import math
from velocity_calculator import VelocityCalculator
# TODO create class to clean up attributes
class Player(GameCharacters):
    item = None
    running_velocity = VelocityCalculator.give_velocity(screen_length, 448)
    downwards_velocity = VelocityCalculator.give_velocity(screen_height, 1121)
    jumped = 0
    last_movement_direction = ""
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
    stationary_air_time = 0
    game_is_sidecrolling = False
        
    def __init__(self):
        self.item = Whip(self)
        self.current_health = 20
        self.full_health = 20
        self.color = (250, 0, 0)
        self.x_coordinate = 100
        self.y_coordinate = screen_height - 200
        self.length = VelocityCalculator.give_measurement(screen_length, 5)
        self.height = VelocityCalculator.give_measurement(screen_height, 15)
    def movement(self):
        controlls = pygame.key.get_pressed()
        # TODO why use this logic?
        if self.jump_key_held_down and self.on_platform:
            self.can_jump = False

        elif self.on_platform:
            self.can_jump = True
        # TODO possible this is used to move left
        player_moving_right = controlls[pygame.K_RIGHT] and self.can_move_right
            
        # TODO why screen_length * .2?
        player_location_to_start_sidescrolling = VelocityCalculator.give_measurement(screen_length, 20)
        if not player_moving_right or self.x_coordinate < player_location_to_start_sidescrolling:\
            self.game_is_sidecrolling = False
        if player_moving_right:
            self.last_movement_direction = "right"
        if player_moving_right and self.x_coordinate >= player_location_to_start_sidescrolling:
            SideScrollableComponents.side_scroll_all(VelocityCalculator.calc_distance(self.running_velocity))
            self.game_is_sidecrolling = True

        elif player_moving_right:
            self.x_coordinate += VelocityCalculator.calc_distance(self.running_velocity)

        if controlls[pygame.K_LEFT] and self.can_move_left:
            self.x_coordinate -= VelocityCalculator.calc_distance(self.running_velocity)
            self.last_movement_direction = "left"

        if controlls[pygame.K_UP]:
            self.jump_key_held_down = True

        else: 
            self.jump_key_held_down = False
        # TODO what is this doing?
        if self.is_jumping and not self.can_jump:
            self.stay_up_in_air = True
        
        elif self.can_jump and self.jump_key_held_down:
            self.jump()
        # TODO explain logic inside if statement
        if self.stay_up_in_air or (self.is_jumping and not self.jump_key_held_down):
            # print("DO A APEX")
            self.apex()

        if controlls[pygame.K_DOWN] and self.can_move_down:
            self.y_coordinate += VelocityCalculator.calc_distance(self.downwards_velocity)

        if controlls[pygame.K_SPACE] and not self.space_held_in:
            self.item.use_item()
            self.space_held_in = True

        if not controlls[pygame.K_SPACE]:
            self.space_held_in = False
    def apex(self):
        stationary_time_needed = .1
        if self.stationary_air_time >= stationary_time_needed:
            self.is_jumping = False
            self.stay_up_in_air = False
            self.stationary_air_time = 0

        else:
            self.stationary_air_time += VelocityCalculator.time

    def jump(self):
        if self.on_platform:
            self.jumped = 0 + VelocityCalculator.calc_distance(self.upwards_velocity)
            self.is_jumping = True

        if self.jumped <= self.max_jump_height and self.is_jumping:
            self.y_coordinate -= VelocityCalculator.calc_distance(self.upwards_velocity)
            self.jumped += VelocityCalculator.calc_distance(self.upwards_velocity)

        if self.jumped >= self.max_jump_height:
            self.can_jump = False
    # TODO why max should be be time_in_air from jumping from one platform to the next
    def max_time_in_air(self, new_platform_y_coordinate, last_platform_y_coordinate, gravity):
        upwards_time = 0
        max_y_coordinate = 0
        # TODO break up logic
        # Checks if the player once jumping hits the top of the screen, which is at 0
        if last_platform_y_coordinate - self.max_jump_height - self.height <= 0:
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

