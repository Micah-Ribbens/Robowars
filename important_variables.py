import pygame
# from consistency_keeper import (
#     ConsistencyKeeper
# )
from velocity_calculator import VelocityCalculator
screen_width = 800
screen_height = 500
win = pygame.display.set_mode((screen_width, screen_height))
y_velocities = VelocityCalculator.give_velocity(screen_height, 500)
# consistency_keeper = ConsistencyKeeper(0.0008919363273713182)
# Multiply decimal with screen width then times that by 5/4
print(1/0.0008919363273713182)