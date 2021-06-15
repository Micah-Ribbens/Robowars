from engines import (
    PhysicsEngine,
    CollisionsFinder,
    InteractionsFinder
)


class GameRenderer:
    def player_platform_runner(player, platform):
        physics_engine = PhysicsEngine()
        physics_engine.platform_side_scrolling(player, platform)

    def _render_enemy(enemy, platform, player):
        collisions_finder = CollisionsFinder()
        physics_engine = PhysicsEngine()
        enemy.movement(collisions_finder.on_platform(platform, enemy, 0))
        physics_engine.enemy_side_scrolling(player, enemy)

    def render_enemies(enemies, platforms, player):
        for x in range(len(enemies)):
            GameRenderer._render_enemy(enemies[x], platforms[x], player)

    def draw_everything(player, enemies, platforms):
        player.draw()

        for enemy in enemies:
            enemy.draw()

        for platform in platforms:
            platform.draw()

    def interactions_runner(player, whip, enemies):
        for enemy in enemies:
            InteractionsFinder.enemy_whip_interactions(enemy, whip)
            InteractionsFinder.player_enemy_interactions(player, enemy)

    def render_players_and_platforms(platforms, player, whip):
        physics_engine = PhysicsEngine()
        InteractionsFinder.player_whip(player, whip)
        player_can_move_right = True
        player_can_move_left = True
        player_is_on_platform = False

        for platform in platforms:
            GameRenderer.player_platform_runner(player, platform)

            if physics_engine.platform_right_boundary(player, platform):
                player_can_move_right = False

            if physics_engine.platform_left_boundary(player, platform):
                player_can_move_left = False

            if physics_engine.player_is_on_platform(platform, player):
                player_is_on_platform = True

        if not player_can_move_left or physics_engine.is_beyond_screen_left(player):
            player.can_move_left = False

        else:
            player.can_move_left = True

        if not player_can_move_right or physics_engine.is_beyond_screen_right(player):
            player.can_move_right = False

        else:
            player.can_move_right = True

        if not player_is_on_platform:
            physics_engine.do_gravity(player)
            player.can_move_down = True
            player.on_platform = False

        else:
            player.can_move_down = False
            player.on_platform = True

        player.movements()
