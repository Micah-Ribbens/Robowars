from history_keeper import HistoryKeeper
from UtilityClasses import GameObject, SideScrollableComponents
from enemies import SimpleEnemy
import time
from velocity_calculator import VelocityCalculator
import pygame
from wall_of_death import WallOfDeath
from important_variables import (
    screen_length,
    background
)
from engines import InteractionEngine
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
    window
)
from HUD import HUD
from game_renderer import GameRenderer
from generator import Generator
from score_keeper import ScoreKeeper

nameOfGame = "robowars"
pygame.display.set_caption(f'{nameOfGame}')
class GameRunner:
    enemies = []
    platforms = [Platform()]
    doggo = Player()
    pause_is_held_down = False
    game_paused = False
    def reset_variables():
        enemy = SimpleEnemy()
        # TODO change back
        # enemy.is_within_screen = False
        GameRunner.enemies = [enemy]
        GameRunner.platforms = [Platform()]
        GameRunner.doggo = Player()
        GameRunner.doggo.y_coordinate = GameRunner.platforms[0].y_coordinate - GameRunner.doggo.height - 100
        WallOfDeath.reset()
        ScoreKeeper.reset()
        HistoryKeeper.reset()

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
        for x in range(len(GameRunner.enemies)):
            SideScrollableComponents.components.append(GameRunner.enemies[x])
            SideScrollableComponents.components.append(GameRunner.platforms[x])

    def delete_unneeded_objects():
        for x in range(len(GameRunner.platforms)):
            platform = GameRunner.platforms[x]
            if not platform.is_within_screen:
                continue
            if platform.right_edge <= 0:
                GameRunner.platforms[x].is_within_screen = False
                GameRunner.enemies[x].is_within_screen = False

    def generate_needed_objects():
        while True:
            last_platform = GameRunner.platforms[len(GameRunner.platforms) - 1]
            # If the end of the last_platform is goes beyond the screen end
            # Another platform isn't needed because it won't be visible
            if last_platform.right_edge > screen_length:
                return
            GameRunner.platforms = Generator.generate_platform(GameRunner.platforms, GameRunner.doggo, PhysicsEngine.gravity_pull)
            last_platform = GameRunner.platforms[len(GameRunner.platforms) - 1]
            GameRunner.enemies = Generator.generate_enemy(last_platform, GameRunner.enemies)

    def run_game():
        run = True
        GameRunner.reset_variables()
        while run:
            GameRunner.add_sidescroll_components()
            GameRunner.generate_needed_objects()
            GameRunner.delete_unneeded_objects()
            start_time = time.time()
            # If the player hits the exit button then the game closes
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            # Has to be above all the drawing because it paints the screen the color of the background
            window.fill(background)

            if GameRunner.doggo.current_health == 0:
                run = False

            # Draw Everything has to be here so it can populate history keeper allowing the engines to see the last_platform object
            WallOfDeath.draw()
            if not GameRunner.game_is_paused():
                GameRenderer.render_players_and_platforms(GameRunner.platforms, GameRunner.doggo)
                GameRenderer.render_enemies(GameRunner.enemies, GameRunner.platforms)
                GameRenderer.interaction_engine_runner(GameRunner.doggo, GameRunner.doggo.item, GameRunner.enemies)

            if PhysicsEngine.is_below_screen_bottom(GameRunner.doggo):
                run = False

            GameRenderer.draw_everything(GameRunner.doggo, GameRunner.enemies, GameRunner.platforms, GameRunner.game_is_paused())
            pygame.display.update()
            end_time = time.time()
            time_taken = end_time - start_time
            # Why is this needed?
            if time_taken > 0:
                VelocityCalculator.time = time_taken
        GameRunner.reset_variables()
        GameRunner.run_game()
