from engines import (
    PhysicsEngine,
    CollisionsFinder,
    InteractionsFinder
)
from HUD import HUD


class GameRenderer:
    last_player_x_coordinate = 0
    last_character_bottom = 0
    def player_platform_runner(player, platform):
        if platform == None:
            return
        physics_engine = PhysicsEngine()
        physics_engine.platform_side_scrolling(player, platform)

    def _render_enemy(enemy, platform, player):
        physics_engine = PhysicsEngine()
        physics_engine.enemy_side_scrolling(player, enemy)
        HUD.show_enemy_health(enemy)
        if not CollisionsFinder.on_platform(platform, enemy):
            physics_engine.do_gravity(enemy)
        else:
            enemy.movement(CollisionsFinder.enemy_on_platform(platform, enemy), platform)

    def render_enemies(enemies, platforms, player):
        for x in range(len(enemies)):
            if enemies[x] == None:
                continue
            GameRenderer._render_enemy(enemies[x], platforms[x], player)

    def draw_everything(player, enemies, platforms):
        player.draw()

        for enemy in enemies:
            if enemy == None:
                continue
            enemy.draw()

        for platform in platforms:
            if platform == None:
                continue
            platform.draw()

    def interactions_runner(player, whip, enemies):
        for enemy in enemies:
            if enemy == None:
                continue
            InteractionsFinder.enemy_whip_interactions(enemy, whip)
            InteractionsFinder.player_enemy_interactions(player, enemy)

    def render_players_and_platforms(platforms, player, whip):
        physics_engine = PhysicsEngine()
        InteractionsFinder.player_whip(player, whip)
        player_hit_platform_right_edge = False
        player_hit_platform_left_edge = False
        player_is_on_platform = False
        platform_player_on = None 
        platform_player_collided_into = None
        times = 0
        for platform in platforms:
            if platform == None:
                continue
            times += 1
            GameRenderer.player_platform_runner(player, platform)
            if CollisionsFinder.platform_right_boundary(player, platform, GameRenderer.last_player_x_coordinate):
                player_hit_platform_right_edge = True
                platform_player_collided_into = platform

            if CollisionsFinder.platform_left_boundary(player, platform, GameRenderer.last_player_x_coordinate):
                player_hit_platform_left_edge = True
                platform_player_collided_into = platform

            if CollisionsFinder.on_platform(platform, player, GameRenderer.last_character_bottom):
                player_is_on_platform = True
                platform_player_on = platform

        if player_hit_platform_left_edge:
            player.can_move_right = False
            player.x_coordinate = platform_player_collided_into.x_coordinate - player.width

        elif physics_engine.is_beyond_screen_right(player):
            player.can_move_right = False
        
        if player_hit_platform_right_edge:
            player.can_move_left = False
            player.x_coordinate = platform_player_collided_into.x_coordinate + platform_player_collided_into.length
            
        elif physics_engine.is_beyond_screen_left(player):
            player.can_move_left = False

        else:
            player.can_move_left = True

        if not player_is_on_platform:
            player.can_move_down = True
            player.on_platform = False

        if not player_is_on_platform and not player.is_jumping:
            physics_engine.do_gravity(player)
            
        if player_is_on_platform:
            player.can_move_down = False
            player.on_platform = True

        if not player.is_jumping and player_is_on_platform:
            player.y_coordinate = platform_player_on.y_coordinate - player.height
            # So no glitch where player on platform but collided into it on the right
            # Making the player not being able to move right and not falling
        
        if player_is_on_platform and player.x_coordinate == platform_player_on.x_coordinate:
            player.x_coordinate = platform_player_on.x_coordinate

        player.movements()
        GameRenderer.last_character_bottom = player.y_coordinate + player.height
        GameRenderer.last_player_x_coordinate = player.x_coordinate
