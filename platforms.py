from UtilityClasses import GameObject
from important_variables import (
    screen_height,
    screen_length,
    win
)
from velocity_calculator import VelocityCalculator
import pygame


class Platform(GameObject):
    number = 0
    
    def __init__(self):
        self.color = (80, 21, 46)
        self.x_coordinate = 100
        self.height = 100
        self.y_coordinate = screen_height - self.height
        self.length = VelocityCalculator.give_measurement(screen_length, 50)

    def move_left(self, change):
        self.x_coordinate -= change
