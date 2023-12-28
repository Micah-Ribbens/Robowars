from base.utility_classes import GameObject, Segment
from base.important_variables import (
    screen_height,
    screen_length,
    window
)
from base.velocity_calculator import VelocityCalculator
import pygame


class Platform(GameObject):
    number = 0
    def __init__(self):
        self.color = (150, 75, 0)
        self.x_coordinate = 100
        self.height = 100
        self.y_coordinate = screen_height - self.height
        self.length = VelocityCalculator.give_measurement(screen_length, 20)
    
    def draw(self):
        green_segment = Segment(
            is_percentage=False,
            color=(34, 204, 0),
            amount_from_top=0,
            amount_from_left=0,
            length_amount=self.length,
            width_amount=VelocityCalculator.give_measurement(screen_height, 4)
        )
        self.draw_in_segments([green_segment])
