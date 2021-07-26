import time
from velocity_calculator import VelocityCalculator
import pygame
import time

from pygame.sprite import LayeredUpdates
from wall_of_death import WallOfDeath
from important_variables import (
    # consistency_keeper,
    screen_width
)
from engines import InteractionsFinder
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
from score_keeper import ScoreKeeper

nameOfGame = "robowars"
pygame.display.set_caption(f'{nameOfGame}')
background = (0, 0, 0)
class GameRunner:
    enter = """
"""
    enemies = []
    platforms = [Platform()]
    doggo = Player()
    # physics = PhysicsEngine()
    pause_is_held_down = False
    game_paused = False
    def reset_variables():
        GameRunner.enemies = [None]
        GameRunner.platforms = [Platform()]
        GameRunner.doggo = Player()
        GameRunner.doggo.y_coordinate = GameRunner.platforms[0].y_coordinate - GameRunner.doggo.height - 1
        WallOfDeath.reset()
        ScoreKeeper.reset()

    def game_is_paused():
        pause_clicked = HUD.pause_clicked()
        can_pause = not GameRunner.pause_is_held_down and pause_clicked

        if pause_clicked:
            GameRunner.pause_is_held_down = True

        else:
            GameRunner.pause_is_held_down = False
        if can_pause:
            print("CLICKED")
            GameRunner.game_paused = not GameRunner.game_paused
        return GameRunner.game_paused


    def generate_needed_objects():
        for x in range(len(GameRunner.platforms)):
            platform = GameRunner.platforms[x]
            if platform == None:
                continue
            platform_end = platform.x_coordinate + platform.length
            if platform_end <= 0:
                GameRunner.platforms = GameRunner.platforms[:x] + [None] + GameRunner.platforms[x + 1:]
                GameRunner.enemies = GameRunner.enemies[:x] + [None] + GameRunner.enemies[x + 1:]
                # GameRenderer.last_enemy_x_coordiantes.append(0)

        for x in range(len(GameRunner.enemies)):
            enemy = GameRunner.enemies[x]
            if enemy == None:
                continue
            if enemy.current_health <= 0:
                GameRunner.enemies = GameRunner.enemies[:x] + [None] + GameRunner.enemies[x + 1:]
                
        while True:
            last_platform = GameRunner.platforms[len(GameRunner.platforms) - 1]
            last_platform_end = last_platform.x_coordinate + last_platform.length
            if last_platform_end > screen_width:
                return
            GameRunner.platforms = Generator.generate_platform(GameRunner.platforms, GameRunner.doggo, PhysicsEngine.gravity_pull)
            last_platform = GameRunner.platforms[len(GameRunner.platforms) - 1]
            last_platform_end = last_platform.x_coordinate + last_platform.length
            GameRunner.enemies = Generator.generate_enemy(last_platform, GameRunner.enemies)
            GameRenderer.last_enemy_x_coordiantes.append(0)

        


    def run_game():
        player_x_coordinates = []
        run = True
        whip = Whip()
        game_paused = False 
        ScoreKeeper.set_player(GameRunner.doggo)
        GameRunner.reset_variables()
        while run:
            start_time = time.time()
            GameRunner.generate_needed_objects()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            win.fill(background)
            HUD.render_pause_button(GameRunner.game_is_paused())

            HUD.show_character_health(GameRunner.doggo.full_health, GameRunner.doggo.current_health)

            if GameRunner.doggo.is_dead():
                run = False

            if not GameRunner.game_is_paused():
                GameRenderer.render_players_and_platforms(GameRunner.platforms, GameRunner.doggo, whip)
                GameRenderer.render_enemies(GameRunner.enemies, GameRunner.platforms, GameRunner.doggo)
                GameRenderer.interactions_runner(GameRunner.doggo, whip, GameRunner.enemies)
                GameRenderer.last_character_bottom = GameRunner.doggo.y_coordinate
                player_x_coordinates.append(GameRunner.doggo.x_coordinate)
                GameRenderer.last_player_x_coordinate = GameRunner.doggo.x_coordinate

            if not PhysicsEngine.is_within_screen(GameRunner.doggo):
                run = False

            # The draw and update are here so the game doesn't make them disappear,
            # so put draw functions here or both!
            ScoreKeeper.give_score(GameRunner.doggo, GameRunner.game_is_paused())
            GameRenderer.draw_everything(GameRunner.doggo, GameRunner.enemies, GameRunner.platforms)
            # WallOfDeath.move()
            InteractionsFinder.player_wall_of_death_interactions(GameRunner.doggo)
            WallOfDeath.draw()

            pygame.display.update()
            end_time = time.time()
            time_taken = end_time - start_time
            if time_taken > 0:
                VelocityCalculator.time = time_taken
        GameRunner.reset_variables()
        GameRunner.run_game()


def average(numbers):
    total = 0
    for number in numbers:
        total += number

    return total / len(numbers)
