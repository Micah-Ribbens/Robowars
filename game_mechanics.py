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

def run_game():
    run = True
    doggo = Character()
    whip = Whip()
    platform1 = Platform()
    physics = PhysicsEngine()  
    interactions = InteractionsFinder()
    collisions = CollisionsFinder()

    controlls = pygame.key.get_pressed()
    game_is_paused = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        if controlls[pygame.K_k]:
            game_is_paused = True
            platform1.platform_color = (0, 0, 250)
            run = False
        
        if game_is_paused:
            continue

        win.fill(background)

        if physics.character_died:
            run = False
        platform1.draw()
        doggo.movements()
        physics.gravity(platform1, doggo)
        physics.boundaries(doggo, platform1)
        physics.movement_possible(platform1, doggo)
        physics.side_scrolling(doggo, platform1)
        doggo.draw()
        interactions.player_whip(doggo, whip)
        pygame.display.update()
    
    run_game()

