from UtilityClasses import SideScrollableComponents
from enemies import SimpleEnemy
import time
from velocity_calculator import VelocityCalculator
import pygame
from wall_of_death import WallOfDeath
from important_variables import (
    screen_length
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
    pause_is_held_down = False
    game_paused = False
    def reset_variables():
        GameRunner.enemies = [SimpleEnemy()]
        GameRunner.platforms = [Platform()]
        GameRunner.doggo = Player()
        GameRunner.doggo.y_coordinate = GameRunner.platforms[0].y_coordinate - GameRunner.doggo.height - 100
        WallOfDeath.reset()
        ScoreKeeper.reset()

    def game_is_paused():
        pause_clicked = HUD.pause_clicked()
        # TODO can_pause? Isn't this used to pause and unpause?
        can_pause = not GameRunner.pause_is_held_down and pause_clicked

        if pause_clicked:
            GameRunner.pause_is_held_down = True

        else:
            GameRunner.pause_is_held_down = False
        if can_pause:
            GameRunner.game_paused = not GameRunner.game_paused
        return GameRunner.game_paused

    def add_sidescroll_components():
        SideScrollableComponents.components = []
        # SideScrollableComponents.components.append(for enemy in)
        for x in range(len(GameRunner.enemies)):
            SideScrollableComponents.components.append(GameRunner.enemies[x])
            SideScrollableComponents.components.append(GameRunner.platforms[x])
    def generate_needed_objects():
        for x in range(len(GameRunner.platforms)):
            platform = GameRunner.platforms[x]
            # TODO how can a platform == None; change to is None
            if not platform.is_within_screen:
                continue
            # TODO explain what this does maybe make a seperate function
            if platform.right_edge <= 0:
                GameRunner.platforms[x].is_within_screen = False
                GameRunner.enemies[x].is_within_screen = False
                
        while True:
            last_platform = GameRunner.platforms[len(GameRunner.platforms) - 1]
            last_platform_end = last_platform.x_coordinate + last_platform.length
            # TODO why does this work?
            if last_platform_end > screen_length:
                return
            GameRunner.platforms = Generator.generate_platform(GameRunner.platforms, GameRunner.doggo, PhysicsEngine.gravity_pull)
            # TODO why does it need the last platform?
            platforms_length = len(GameRunner.platforms) - 1
            last_platform = GameRunner.platforms[platforms_length]
            last_platform_end = last_platform.x_coordinate + last_platform.length
            GameRunner.enemies = Generator.generate_enemy(last_platform, GameRunner.enemies)

    def run_game():
        run = True
        ScoreKeeper.set_player(GameRunner.doggo)
        GameRunner.reset_variables()
        while run:
            GameRunner.add_sidescroll_components()
            # TODO explain why start_time and end_time are needed
            start_time = time.time()
            GameRunner.generate_needed_objects()
            # TODO explain what this does
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # TODO explain why this has to be here
            win.fill(background)
            HUD.render_pause_button(GameRunner.game_is_paused())

            HUD.show_character_health(GameRunner.doggo.full_health, GameRunner.doggo.current_health)

            if GameRunner.doggo.current_health == 0:
                print("HEALTH GONE")
                run = False
            # Draw Everything has to be here so it can populate history keeper allowing the engines to see the last_platform object
            GameRenderer.draw_everything(GameRunner.doggo, GameRunner.enemies, GameRunner.platforms)
            ScoreKeeper.give_score(GameRunner.doggo, GameRunner.game_is_paused())
            WallOfDeath.draw()
            if not GameRunner.game_is_paused():
                GameRenderer.render_players_and_platforms(GameRunner.platforms, GameRunner.doggo)
                GameRenderer.render_enemies(GameRunner.enemies, GameRunner.platforms)
                GameRenderer.interactions_runner(GameRunner.doggo, GameRunner.doggo.item, GameRunner.enemies)

            if not PhysicsEngine.is_within_screen(GameRunner.doggo):
                run = False
                

            pygame.display.update()
            end_time = time.time()
            time_taken = end_time - start_time
            # Why is this needed?
            if time_taken > 0:
                VelocityCalculator.time = time_taken
        GameRunner.reset_variables()
        print("RESET GAME")
        GameRunner.run_game()
