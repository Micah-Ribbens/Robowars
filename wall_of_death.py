import pygame
from important_variables import (
    win,
    screen_height,
    screen_width, 
    # consistency_keeper
)
from velocity_calculator import VelocityCalculator
class WallOfDeath:
    color = (0, 0, 250)
    x_coordinate = -screen_width
    y_coordinate = 0
    height = screen_height
    length = screen_width
    velocity = VelocityCalculator.give_velocity(screen_width, 224)
    # def _improve_variables():
    #     WallOfDeath.movement = consistency_keeper.calculate_new_speed(WallOfDeath.movement)
    def draw():
        pygame.draw.rect(win, (WallOfDeath.color), (WallOfDeath.x_coordinate,
                                WallOfDeath.y_coordinate, WallOfDeath.length, WallOfDeath.height))
    def move():
        WallOfDeath.x_coordinate += VelocityCalculator.give_velocity(screen_width, 224)
    def reset():
        WallOfDeath.length = screen_width
        WallOfDeath.x_coordinate = -screen_width
    def move_backwards(amount):
        WallOfDeath.x_coordinate -= amount