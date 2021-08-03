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
        self.color = (0, 250, 0)
        self.x_coordinate = 0
        self.y_coordinate = 0
        self.length = 0
        self.height = self.base_height
    
    @abstractmethod
    def use_item(self):
        pass


class Whip(Item):
    whip_is_extending = False
    secs_needed_to_extend = .2
    secs_extended = 0
    velocity = VelocityCalculator.give_velocity(screen_length, 336)
    up_length = VelocityCalculator.give_measurement(screen_height, 14)
    max_length = VelocityCalculator.give_measurement(screen_length, 8.75)
    player = None
    def __init__(self, player):
        self.player = player
    def use_item(self):
        if not self.whip_is_extending:
            self.whip_is_extending = True
    # TODO break up this logic its doing too much
    def render(self):
        player_is_facing_right = self.player.last_movement_direction == "right"
        if not self.whip_is_extending:
            return
        # TODO right length for what?
        is_right_length = self.length == 0 or self.length == self.base_length
        whip_is_upwards = self.whip_is_extending and is_right_length and (
             self.secs_extended <= self.secs_needed_to_extend)
             
        player_right_edge = self.player.x_coordinate + self.player.length
        # Puts the whip at the halfway point of the player
        whip_y_coordiante = self.player.y_coordinate + (self.player.height * .5)
        # TODO explain this logic 
        if whip_is_upwards:
            self.y_coordinate = whip_y_coordiante - self.player.height
            self.height = self.up_length
            self.length = self.base_height
            self.secs_extended += VelocityCalculator.time
            self.draw()

        if whip_is_upwards and player_is_facing_right:
            self.x_coordinate = self.player.right_edge
            return 

        if whip_is_upwards and not player_is_facing_right:
            self.x_coordinate = self.player.x_coordinate - self.length
            return
        if self.length >= 70 or self.length <= -70:
            self.whip_is_extending = False
            self.length = 0
            self.height = 0
            self.secs_extended = 0

        if self.whip_is_extending and not whip_is_upwards:
            self.height = self.base_height
            self.y_coordinate = whip_y_coordiante
        # TODO if statements too long
        if self.whip_is_extending and player_is_facing_right and not whip_is_upwards:
            self.x_coordinate = player_right_edge
            self.length += VelocityCalculator.calc_distance(self.velocity)
        
        if self.whip_is_extending and not player_is_facing_right and not whip_is_upwards:
            self.x_coordinate = self.player.x_coordinate
            self.length -= VelocityCalculator.calc_distance(self.velocity)
        self.draw()