import pygame
# from consistency_keeper import (
#     ConsistencyKeeper
# )
from velocity_calculator import VelocityCalculator
screen_length = 800
screen_height = 500
win = pygame.display.set_mode((screen_length, screen_height))
y_velocities = VelocityCalculator.give_velocity(screen_height, 500)
