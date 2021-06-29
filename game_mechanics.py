import time
import pygame
import time

from pygame.sprite import LayeredUpdates
from wall_of_death import WallOfDeath
from important_variables import (
    consistency_keeper,
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
    physics = PhysicsEngine()
    pause_is_held_down = False
    game_is_paused = False
    def reset_variables():
        GameRunner.enemies = [None]
        # GameRunner.enemies.append()
        GameRunner.platforms = [Platform()]
        GameRunner.doggo = Player()
        GameRunner.doggo.y_coordinate = GameRunner.platforms[0].y_coordinate - GameRunner.doggo.height
        WallOfDeath.reset()
    def game_is_paused():
        pause_clicked = HUD.pause_clicked()
        can_pause = not GameRunner.pause_is_held_down and pause_clicked

        if can_pause and GameRunner.game_is_paused:
            GameRunner.game_is_paused = False
            return False

        elif can_pause and not GameRunner.game_is_paused:
            GameRunner.game_is_paused = True
            return True

        if pause_clicked:
            GameRunner.pause_is_held_down = True

        else:
            GameRunner.pause_is_held_down = False
    def generate_needed_objects():
        for x in range(len(GameRunner.platforms)):
            platform = GameRunner.platforms[x]
            if platform == None:
                continue
            platform_end = platform.x_coordinate + platform.length
            if platform_end <= 0:
                GameRunner.platforms = GameRunner.platforms[:x] + [None] + GameRunner.platforms[x + 1:]
                GameRunner.enemies = GameRunner.enemies[:x] + [None] + GameRunner.enemies[x + 1:]

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
                # print("BREAK")
                return
            # print("MAKE")
            GameRunner.platforms = Generator.generate_platform(GameRunner.platforms, GameRunner.doggo, GameRunner.physics.gravity_pull)
            last_platform = GameRunner.platforms[len(GameRunner.platforms) - 1]
            last_platform_end = last_platform.x_coordinate + last_platform.length
            GameRunner.enemies = Generator.generate_enemy(last_platform, GameRunner.enemies)

        


    def run_game():
        hud = HUD()
        run = True
        whip = Whip()
        timesIterated = 0
        click_is_held_done = False
        game_is_paused = False 
        score_keeper = ScoreKeeper(GameRunner.doggo)
        GameRunner.reset_variables()
        while run:
            start_time = time.time()
            GameRunner.generate_needed_objects()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            win.fill(background)
            HUD.render_pause_button(game_is_paused)

            HUD.show_character_health(GameRunner.doggo.full_health, GameRunner.doggo.current_health)

            if GameRunner.doggo.is_dead():
                run = False

            if not GameRunner.game_is_paused():

                if not GameRunner.physics.is_within_screen(GameRunner.doggo):
                    run = False

                GameRenderer.render_players_and_platforms(GameRunner.platforms, GameRunner.doggo, whip)
                GameRenderer.render_enemies(GameRunner.enemies, GameRunner.platforms, GameRunner.doggo)
                GameRenderer.interactions_runner(GameRunner.doggo, whip, GameRunner.enemies)
            # The draw and update are here so the game doesn't make them disappear,
            # so put draw functions here or both!
            score_keeper.give_score(GameRunner.doggo)
            GameRenderer.draw_everything(GameRunner.doggo, GameRunner.enemies, GameRunner.platforms)
            # WallOfDeath.move()
            InteractionsFinder.player_wall_of_death_interactions(GameRunner.doggo)
            # print(WallOfDeath.x_coordinate)
            # if WallOfDeath.x_coordinate == 0:
                # print(WallOfDeath.x_coordinate)
                # print(WallOfDeath.x_coordinate >= 0)
                # print("I CALLED")
                # print("DRAW")
            WallOfDeath.draw()

            pygame.display.update()
            end_time = time.time()
            time_taken = end_time - start_time
            if time_taken > 0:
                consistency_keeper.change_current_speed(time_taken)
                # consistency_keeper.change_new_speed(time_taken)
        # GameRunner.reset_variables()
        GameRunner.run_game()


def average(numbers):
    total = 0
    for number in numbers:
        total += number

    return total / len(numbers)
