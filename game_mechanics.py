from abc import ABC, abstractmethod
import pygame
from items import (
    Whip,
)
from engines import (
    PhysicsEngine,
    CollisionsFinder,
    InteractionsFinder
)
from platforms import (
    Platform
)
from characters import (
    Character
)
from important_variables import (
    screen_width,
    screen_height,
    win
)
# Up is down. Down is up.
# No spaces between functions in a class


nameOfGame = "robowars"
pygame.display.set_caption(f'{nameOfGame}')
background = (0, 0, 0)     

doggo = Character()
whip = Whip()
run = True
platform1 = Platform()
physics = PhysicsEngine()  
interactions = InteractionsFinder()
collisions = CollisionsFinder()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    win.fill(background)
    platform1.draw()
    doggo.movements()
    physics.gravity(platform1, doggo)
    physics.boundaries(doggo, platform1)
    physics.movement_possible(platform1, doggo)
    physics.side_scrolling(doggo, platform1)
    doggo.draw()
    interactions.player_whip(doggo, whip)
    pygame.display.update()

