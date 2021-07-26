from important_variables import (
    screen_height,
    screen_width,
    win
)
from velocity_calculator import VelocityCalculator
import pygame


class Platform:
    platform_color = (80, 21, 46)
    x_coordinate = 100
    width = 100
    y_coordinate = screen_height - width
    length = VelocityCalculator.give_measurement(screen_width, 50)
    
    def draw(self):
        pygame.draw.rect(win, (self.platform_color), (self.x_coordinate,
                         self.y_coordinate, self.length, self.width))

    def move_left(self, change):
        self.x_coordinate -= change
