from time import time
import pygame
from important_variables import (
    consistency_keeper
)
from items import (
    Whip,
)
from engines import (
    PhysicsEngine,
)
from platforms import (
    Platform
)
from players import (
    Player
)
from important_variables import (
    win
)
from HUD import HUD
from game_renderer import GameRenderer
from generator import Generator
# Up is down. Down is up.
# No spaces between functions in a class

nameOfGame = "robowars"
pygame.display.set_caption(f'{nameOfGame}')
background = (0, 0, 0)


def run_game():
    hud = HUD()
    run = True
    doggo = Player()
    whip = Whip()
    platform1 = Platform()
    physics = PhysicsEngine()
    platforms = [platform1]
    platforms = Generator.generate_platform(platforms, doggo, physics.gravity_pull)
    timesIterated = 0
    click_is_held_done = False
    times = []
    game_is_paused = False
    enemies = []
    for x in range(29):
        platorms = Generator.generate_platform(platforms, doggo, physics.gravity_pull)

    for x in range(29):
        enemies = Generator.generate_enemy(platforms[x], enemies)

    while run:
        timesIterated += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        start_time = time()
        win.fill(background)
        hud.render_pause_button(game_is_paused)
        hud.show_character_health(5000, 3000)

        delete_indexes = []
        for x in range(len(enemies)):
            enemy = enemies[x]
            if enemy.current_health == 0:
                delete_indexes.append(x)

            hud.show_enemy_health(enemy, enemy.full_health, enemy.current_health)

        for index in delete_indexes:
            del enemies[index]

        pause_clicked = hud.pause_clicked()
        can_pause = not click_is_held_done and pause_clicked

        if can_pause and game_is_paused:
            game_is_paused = False

        elif can_pause and not game_is_paused:
            game_is_paused = True

        if pause_clicked:
            click_is_held_done = True

        else:
            click_is_held_done = False

        if not game_is_paused:

            if not physics.is_within_screen(doggo):
                run = False

            GameRenderer.render_players_and_platforms(platforms, doggo, whip)
            GameRenderer.render_enemies(enemies, platforms, doggo)
            GameRenderer.interactions_runner(doggo, whip, enemies)
        # The draw and update are here so the game doesn't make them disappear,
        # so put draw functions here or both!
        GameRenderer.draw_everything(doggo, enemies, platforms)
        pygame.display.update()
        end_time = time()
        times.append(end_time - start_time)
        consistency_keeper.change_current_speed(end_time - start_time)
        consistency_keeper.change_new_speed(end_time - start_time)

    run_game()


def average(numbers):
    total = 0
    for number in numbers:
        total += number

    return total / len(numbers)
