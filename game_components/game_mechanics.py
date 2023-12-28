from base.utility_classes import GameObject, HistoryKeeper, SideScrollableComponents
from game_components.enemies import SimpleEnemy
import time
from base.velocity_calculator import VelocityCalculator
import pygame
from game_components.wall_of_death import WallOfDeath
from base.important_variables import (
    screen_length,
    background
)
from base.engines import (
    PhysicsEngine,
)
from game_components.platforms import (
    Platform
)
from game_components.players import (
    Player
)
from base.important_variables import (
    window
)
from gui_components.hud import HUD
from game_components.game_renderer import GameRenderer
from game_components.generator import Generator
from game_components.score_keeper import ScoreKeeper

nameOfGame = "Robowars"
pygame.display.set_caption(f'{nameOfGame}')
class GameRunner:
    enemies = []
    platforms = [Platform()]
    doggo = Player()
    pause_is_held_down = False
    game_paused = False

    def reset_variables():
        enemy = SimpleEnemy(GameRunner.doggo)
        enemy.is_within_screen = False
        GameRunner.enemies = []
        platform = Platform()
        platform.x_coordinate = 0

        enemy.platform_on = platform
        GameRunner.platforms = [platform]
        GameRunner.doggo = Player()
        GameRunner.doggo.y_coordinate = platform.y_coordinate + 70 + GameRunner.doggo.height
        Player.attributes = GameObject.find_all_attributes(Player())
        SimpleEnemy.attributes = GameObject.find_all_attributes(SimpleEnemy())
        Platform.attributes = GameObject.find_all_attributes(Platform())
        GameRunner.doggo.y_coordinate = GameRunner.platforms[0].y_coordinate - GameRunner.doggo.height - 100
        WallOfDeath.reset()
        ScoreKeeper.reset()
        HistoryKeeper.reset()

    def game_is_paused():
        pause_clicked = HUD.pause_clicked()
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
        for x in range(len(GameRunner.platforms)):
            SideScrollableComponents.components.append(GameRunner.platforms[x])

    def delete_unneeded_objects():
        for x in range(len(GameRunner.platforms)):
            platform = GameRunner.platforms[x]
            if platform.right_edge <= 0:
                GameRunner.platforms[x].is_within_screen = False
        for x in range(len(GameRunner.enemies)):
            enemy = GameRunner.enemies[x]
            if enemy.platform_on is None:
                continue
            if enemy.platform_on.right_edge <= 0:
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
            GameRunner.enemies = Generator.generate_enemy(last_platform, GameRunner.enemies, GameRunner.doggo)

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

            if GameRunner.doggo.current_health <= 0:
                run = False

            # Draw Everything has to be here so it can populate history keeper allowing the engines to see the last_platform object
            WallOfDeath.draw()
            if not GameRunner.game_is_paused():
                GameRenderer.render_players_and_platforms(GameRunner.platforms, GameRunner.doggo)
                GameRenderer.render_enemies(GameRunner.enemies, GameRunner.platforms)
                GameRenderer.interaction_engine_runner(GameRunner.doggo, GameRunner.enemies)

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
