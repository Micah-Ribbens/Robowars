from UtilityClasses import GameObject
from velocity_calculator import VelocityCalculator
from important_variables import (
    screen_height,
    screen_length,
)
from abc import abstractmethod

class Item(GameObject):
    base_height = VelocityCalculator.give_measurement(screen_height, 2)
    base_length = VelocityCalculator.give_measurement(screen_length, 2)
    
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
    secs_needed_to_start_extending = .2
    secs_extended = 0
    velocity = VelocityCalculator.give_velocity(screen_length, 670)
    up_length = VelocityCalculator.give_measurement(screen_height, 14)
    max_length = VelocityCalculator.give_measurement(screen_length, 8.75)
    player = None

    def __init__(self, player):
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
        is_right_length = self.length == 0 or self.length == self.base_height
        time_is_too_long = self.secs_extended > self.secs_needed_to_start_extending
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