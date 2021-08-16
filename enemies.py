from UtilityClasses import GameCharacters
import pygame

from important_variables import (
    screen_length,
)
from velocity_calculator import (
    VelocityCalculator  
)
class Enemy(GameCharacters):
    def __init__(self):
        self.color = (25, 50, 25)
        self.x_coordinate = 80
        self.length = 40
        self.height = 40
        self.y_coordinate = 80
        self.current_health = 20
        self.full_health = 20

class SimpleEnemy(Enemy):
    velocity = VelocityCalculator.give_velocity(screen_length, 112)
    knockback_distance = VelocityCalculator.give_measurement(screen_length, 25)
    is_moving_left = True
    damage = 5
    is_on_platform = True
    platform_on = None
    def movement(self):
        self.change_direction_if_necessary()
        if not self.is_moving_left:
            self.x_coordinate += VelocityCalculator.calc_distance(self.velocity)

        if self.is_moving_left:
            self.x_coordinate -= VelocityCalculator.calc_distance(self.velocity)

    def change_direction_if_necessary(self):
        within_platform_length = (self.x_coordinate >= self.platform_on.x_coordinate 
                                  and self.right_edge <= self.platform_on.right_edge)
        if within_platform_length:
            return
        if self.is_moving_left:
            self.is_moving_left = False
            self.x_coordinate = self.platform_on.x_coordinate
        else:
            self.is_moving_left = True
            self.x_coordinate = self.platform_on.right_edge - self.length


