import pygame
import os
from UtilityClasses import GameCharacters, GameObject, HistoryKeeper
import math
from velocity_calculator import VelocityCalculator
from important_variables import (
    screen_height,
    screen_length,
    window
)
# from players import Player
# TODO USE Trigonometry for drawing the item
from abc import abstractmethod

class Item(GameObject):
    base_height = int(VelocityCalculator.give_measurement(screen_height, 2))
    base_length = int(VelocityCalculator.give_measurement(screen_length, 2))
    damage = 0
    
    def __init__(self):
        self.x_coordinate = 0
        self.y_coordinate = 0
        self.length = 0
        self.height = self.base_height
    
    @abstractmethod
    def use_item(self):
        pass

    def stop_item_usage(self):
        self.whip_is_extending = False
        self.length = 0
        self.height = 0


class Whip(Item):
    whip_is_extending = False
    full_animation_time = .1
    secs_extended = 0
    velocity = VelocityCalculator.give_velocity(screen_length, 670)
    up_length = VelocityCalculator.give_measurement(screen_height, 14)
    max_length = VelocityCalculator.give_measurement(screen_length, 8.75)
    player = None
    full_length = 70

    def __init__(self, player=None):
        self.color = (77, 38, 0)
        self.player = player

    def use_item(self):
        if not self.whip_is_extending:
            self.whip_is_extending = True

    def draw_whip_upwards(self):
        player_midpoint = self.player.y_coordinate + (self.player.height * .5)
        self.y_coordinate = player_midpoint - self.up_length
        self.height = self.up_length
        self.length = self.base_height
        self.secs_extended += VelocityCalculator.time
        if self.player.is_facing_right:
            self.x_coordinate = self.player.right_edge
        else:
            self.x_coordinate = self.player.x_coordinate - self.length

    def whip_is_upwards(self):
        # If whip isn't drawn then its length is 0, and when it is upwards it is base_height
        # Because its base_height is the height of the whip when extending meaning if it is facing
        # Upwards the length should be the whips extending height
        secs_needed_to_start_extending = .05
        is_right_length = self.length == 0 or self.length == self.base_height
        time_is_too_long = self.secs_extended > secs_needed_to_start_extending
        return is_right_length and not time_is_too_long

    def draw_whip_extending(self):
        self.height = self.base_height
        player_midpoint = self.player.y_coordinate + (self.player.height * .5)
        self.y_coordinate = player_midpoint
        length_increase = VelocityCalculator.calc_distance(self.velocity)
        self.length += length_increase
        # TODO change it not t player but game object or something since both player and enemy use it and change stuff
        # Associated with that
        if self.player.is_facing_right:
            self.x_coordinate = self.player.right_edge
        else:
            # Since it draw from left to right the x_coordinate would have to move to the left
            # By the amount of the increase of length
            self.x_coordinate = self.player.x_coordinate - self.length

    def render(self):
        if not self.whip_is_extending:
            return
        whip_is_too_long = self.length >= 70

        if whip_is_too_long:
            self.whip_is_extending = False
            self.length = 0
            self.height = 0
            self.secs_extended = 0
            return

        if not self.whip_is_extending:
            return

        if self.whip_is_upwards():
            self.draw_whip_upwards()
        
        else:
            self.draw_whip_extending()

        self.draw()

class Sword(Item):
    def get_degrees(self):
        last_time = HistoryKeeper.get_last("whip drawing"+self.player.name)
        return (last_time / self.full_animation_time) * 180
    def get_radians(self):
        return math.radians(self.get_degrees())
    def draw(self):
        pygame.draw.line(window, self.color, (self.player.right_edge, self.player.y_midpoint), (self.get_x(), self.get_y()), self.base_height)

    def get_x(self):
        # Frames
        if self.get_degrees() >= 46 and self.get_degrees() <= 136:
            return self.player.right_edge + self.full_length
        return self.player.right_edge
        # No Frames
        whip_end = self.player.right_edge + self.full_length
        if self.get_degrees() > 180:
            return self.player.right_edge
        if self.get_degrees() > 90:
            return whip_end - math.sin(self.get_radians() - 90) * self.full_length
        # print("X sin", math.sin(self.get_radians()), self.get_radians())
        return self.player.right_edge + math.sin(self.get_radians()) * self.full_length

    def get_y(self):
        # Frames
        if self.get_degrees() >= 46 and self.get_degrees() <= 136:
            return self.player.y_midpoint
        if self.get_degrees() >= 137 and self.get_degrees():
            return self.player.y_midpoint + self.full_length
        return self.player.y_midpoint - self.full_length
        # No Frames
        if self.get_degrees() > 90:
            return self.player.y_midpoint + math.cos(self.get_radians() - 90) * self.full_length

        return self.player.y_midpoint - math.cos(self.get_radians()) * self.full_length

class Shield(Item):
    player = None
    is_being_used = False
    caused_flinch = False

    def __init__(self, player=None):
        self.player = player
        self.color = (250, 0, 0)

    def render(self):
        if not self.is_being_used:
            return

        shield_is_done = self.time_based_activity_is_done("shield"+self.player.name, .3, False)

        if shield_is_done:
            self.is_being_used = False

        if shield_is_done and not self.caused_flinch:
            self.player.flinch()

        self.set_dimensions()
        self.draw()

    def set_dimensions(self):
        self.length = 20
        self.height = self.player.height

        if self.player.is_facing_right:
            self.x_coordinate = self.player.right_edge

        else:
            self.x_coordinate = self.player.x_coordinate - self.length

        self.y_coordinate = self.player.y_coordinate

    def use_item(self):
        # was_being_used = self.is_being_used
        self.is_being_used = True

        # if was_being_used and not self.is_being_used and not self.caused_flinch:
        #     self.player.flinch()
            
    def stop_usage(self):
        print("CALLED")
        self.is_being_used = False

        
