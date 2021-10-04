import pygame
from UtilityClasses import UtilityFunctions
from enemies import SimpleEnemy
from engines import (
    PhysicsEngine,
    CollisionsFinder,
    InteractionEngine
)
from HUD import HUD
from score_keeper import ScoreKeeper
from UtilityClasses import HistoryKeeper
from players import Player


class GameRenderer:
    def _render_enemy(enemy: SimpleEnemy):
        platform = enemy.platform_on
        if not CollisionsFinder.on_platform(platform, enemy, False):
            PhysicsEngine.do_gravity(enemy)
        else:
            enemy.is_on_platform = CollisionsFinder.on_platform(platform, enemy, False)
            enemy.platform_on = platform
            enemy.movement()

    def render_enemies(enemies, platforms):
        for x in range(len(enemies)):
            if enemies[x].is_within_screen and enemies[x].current_health > 0:
                # For each enemy in enemies it renders the enemy
                GameRenderer._render_enemy(enemies[x])

    def draw_everything(player: Player, enemies, platforms, game_is_paused):
        player.draw()
        player.item.render()
        player.shield.render()
        for x in range(len(enemies)):
            enemy = enemies[x]
            enemy.name = f"enemy{x}"
            HistoryKeeper.add(enemy, enemy.name, True)

            if enemy.is_within_screen and enemy.current_health > 0:
                enemy.player = player
                enemy.draw()
                enemy.item.render()
                enemy.shield.render()
                HUD.show_enemy_health(enemy)

            if HistoryKeeper.get_last(enemy.name).current_health > 0 and enemy.current_health <= 0:
                UtilityFunctions.draw_font("+100", pygame.font.Font('freesansbold.ttf', 10), x_coordinate=enemy.x_coordinate, y_coordinate=enemy.y_coordinate)
                ScoreKeeper.score += 100

        for x in range(len(platforms)):
            platform = platforms[x]
            if platform.is_within_screen:
                platform.name = f"platform{x}"
                HistoryKeeper.add(platform, platform.name, True)
                platform.draw()

        HistoryKeeper.add(player, "player", True)
        HUD.render_pause_button(game_is_paused)
        HUD.show_character_health(player)
        ScoreKeeper.give_score(player)

    def interaction_engine_runner(player, enemies):
        for x in range(len(enemies)):
            enemy = enemies[x]
            if enemy.is_within_screen and enemy.current_health > 0:
                InteractionEngine.object_whip_interactions(enemy, player)
                InteractionEngine.player_enemy_interactions(player, enemy)
                InteractionEngine.object_whip_interactions(player, enemy)

    def platform_side_collisions(player, platform_collided_into, is_rightside_collision, is_leftside_collision):
        if platform_collided_into is None:
            return

        if is_leftside_collision:
            player.can_move_right = False
            player.x_coordinate = platform_collided_into.x_coordinate - player.length

        elif PhysicsEngine.is_beyond_screen_right(player):
            player.can_move_right = False
        
        else: 
            player.can_move_right = True
        
        if is_rightside_collision:
            player.can_move_left = False
            player.x_coordinate = platform_collided_into.x_coordinate + platform_collided_into.length
            
        elif PhysicsEngine.is_beyond_screen_left(player):
            player.can_move_left = False
            player.x_coordinate = 0

        else:
            player.can_move_left = True
        
    # So that includes player jumping, gravity, and up and down movements, which all rely on if or not the player's on the platform
    def platform_top_mechanics(player: Player, platform_player_on, player_is_on_platform):
        if not player_is_on_platform:
            player.can_move_down = True
            player.on_platform = False

        if not player_is_on_platform and not player.is_jumping:
            PhysicsEngine.do_gravity(player)
            
        if PhysicsEngine.player_hit_top_of_screen(player):
            player.is_jumping = False
            player.can_jump = False

        if player_is_on_platform:
            player.can_move_down = False
            player.can_move_left = True
            player.can_move_right = True
            player.on_platform = True
            player.y_coordinate = platform_player_on.y_coordinate - player.height
            player.last_platform_on = platform_player_on
        
    def render_players_and_platforms(platforms, player):
        is_rightside_collision = False
        is_leftside_collision = False
        player_is_on_platform = False
        platform_player_on = None 
        platform_collided_into = None

        for x in range(len(platforms)):
            platform = platforms[x]
            if not platform.is_within_screen:
                continue
            if CollisionsFinder.platform_rightside_collision(player, platform):
                is_rightside_collision = True
                platform_collided_into = platform

            if CollisionsFinder.platform_leftside_collision(player, platform):
                is_leftside_collision = True
                platform_collided_into = platform

            if CollisionsFinder.on_platform(platform, player, True):
                player_is_on_platform = True
                platform_player_on = platform

        GameRenderer.platform_side_collisions(player, platform_collided_into,
                                              is_rightside_collision, is_leftside_collision)
        # Keep this after platform_side_collisions because
        GameRenderer.platform_top_mechanics(player, platform_player_on, player_is_on_platform)
        player.movement()

        


