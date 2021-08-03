from enemies import SimpleEnemy
from engines import (
    PhysicsEngine,
    CollisionsFinder,
    InteractionsFinder
)
from HUD import HUD
from history_keeper import HistoryKeeper
from players import Player


class GameRenderer:
    # TODO why on earth is there an "_"?
    def _render_enemy(enemy: SimpleEnemy, platform):
        HUD.show_enemy_health(enemy)
        if not CollisionsFinder.on_platform(platform, enemy, False):
            PhysicsEngine.do_gravity(enemy)
        else:
            enemy.is_on_platform = CollisionsFinder.on_platform(platform, enemy, False)
            enemy.platform_on = platform
            enemy.movement()
        enemy.draw()

    def render_enemies(enemies, platforms):
        for x in range(len(enemies)):
            # TODO how can enemy be None?
            if enemies[x].is_within_screen and enemies[x].current_health > 0:
                GameRenderer._render_enemy(enemies[x], platforms[x])

    def draw_everything(player: Player, enemies, platforms):
        player.draw()
        player.item.render()
        
        HistoryKeeper.add(player, "player")

        for x in range(len(platforms)):
            enemy = enemies[x]
            # TODO how can enemy and platform be None?
            if enemy.is_within_screen and enemy.current_health > 0:
                enemy.number = x
                HistoryKeeper.add(enemy, f"enemy{x}")
                enemy.draw()
        for x in range(len(platforms)):
            platform = platforms[x]
            if platform.is_within_screen:
                platform.number = x
                HistoryKeeper.add(platform, f"platform{x}")
                platform.draw()


    def interactions_runner(player, whip, enemies):
        for x in range(len(enemies) - 1):
            enemy = enemies[x]
            # TODO how can enemy be None
            if enemy.is_within_screen or enemy.current_health > 0:
                InteractionsFinder.enemy_whip_interactions(enemy, whip)
                InteractionsFinder.player_enemy_interactions(player, enemy)

    def render_players_and_platforms(platforms, player):
        # TODO why is this here?
        player_hit_platform_right_edge = False
        player_hit_platform_left_edge = False
        player_is_on_platform = False
        platform_player_on = None 
        platform_player_collided_into = None
        # TODO what is the point of this?
        times = 0
        for platform in platforms:
            # TODO how can platform be None
            if not platform.is_within_screen:
                continue
            times += 1
            if CollisionsFinder.platform_rightside_collision(player, platform):
                player_hit_platform_right_edge = True
                platform_player_collided_into = platform

            if CollisionsFinder.platform_leftside_collision(player, platform):
                player_hit_platform_left_edge = True
                platform_player_collided_into = platform

            if CollisionsFinder.on_platform(platform, player, True):
                player_is_on_platform = True
                platform_player_on = platform

        if player_hit_platform_left_edge:
            player.can_move_right = False
            player.x_coordinate = platform_player_collided_into.x_coordinate - player.length

        elif PhysicsEngine.is_beyond_screen_right(player):
            player.can_move_right = False
        
        else: 
            player.can_move_right = True
        
        if player_hit_platform_right_edge:
            player.can_move_left = False
            player.x_coordinate = platform_player_collided_into.x_coordinate + platform_player_collided_into.length
            
        elif PhysicsEngine.is_beyond_screen_left(player):
            player.can_move_left = False
            player.x_coordinate = 0

        else:
            player.can_move_left = True

        if not player_is_on_platform:
            player.can_move_down = True
            player.on_platform = False

        if not player_is_on_platform and not player.is_jumping:
            PhysicsEngine.do_gravity(player)
            
        if player_is_on_platform:
            player.can_move_down = False
            player.on_platform = True
        # TODO why does this need to be there?
        if not player.is_jumping and player_is_on_platform:
            player.y_coordinate = platform_player_on.y_coordinate - player.height
        # TODO what what does this do? This looks like it does nothing
        if player_is_on_platform and player.x_coordinate == platform_player_on.x_coordinate:
            player.x_coordinate = platform_player_on.x_coordinate

        player.movement()
        PhysicsEngine.screen_boundaries(player)

