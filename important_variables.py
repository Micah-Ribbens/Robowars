import pygame
from consistency_keeper import (
    ConsistencyKeeper
)
# screen_width = 1300
# screen_height = 700
screen_width = 800
screen_height = 500
win = pygame.display.set_mode((screen_width, screen_height))
consistency_keeper = ConsistencyKeeper(0.0008919363273713182)
