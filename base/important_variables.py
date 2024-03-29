import pygame
from base.velocity_calculator import VelocityCalculator

screen_length = 800
screen_height = 500
background = (0, 200, 250)
window = pygame.display.set_mode((screen_length, screen_height))
y_velocities = VelocityCalculator.give_velocity(screen_height, 1000)
