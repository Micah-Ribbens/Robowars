from UtilityClasses import GameObject
from enemies import SimpleEnemy
from items import Whip
from important_variables import (
    screen_height,
    screen_length,
    y_velocities
)
from history_keeper import HistoryKeeper
from velocity_calculator import VelocityCalculator
from wall_of_death import WallOfDeath
from platforms import Platform
from players import Player

class CollisionsFinder:
    def on_platform(platform, player, is_player):
        is_platform_collision = CollisionsFinder.object_collision(player, platform)
        if not is_player or len(HistoryKeeper.get("player")) <= 1:
            return is_platform_collision
        
        # If this logic isn't in place last_player_y_coordinate could be below the platform's y_coordinate, which would make it do gravity
        # EX: (platform y coordinate is 400) player's bottom goes from 399 to 401 putting it at 400, but last player bottom would be 401 causing gravity
        if player.bottom == platform.y_coordinate:
            return is_platform_collision

        last_player = HistoryKeeper.get_last("player")
        if last_player is None:
            return
        return is_platform_collision and last_player.bottom <= platform.y_coordinate

    def object_collision(object1, object2):
        within_platform_height = (object1.bottom >= object2.y_coordinate and
                                  object1.y_coordinate <= object2.bottom)
        within_platform_length = (object1.x_coordinate <= object2.right_edge and
                                  object1.right_edge >= object2.x_coordinate)
        
        return within_platform_height and within_platform_length

    def is_sidescrolling__collision(unmoving_object, sidescrolling_object):
        prev_object_iteration = HistoryKeeper.get_last(sidescrolling_object.name)
        if prev_object_iteration is None:
            return False
        object_sidescrolled = prev_object_iteration.x_coordinate > sidescrolling_object.x_coordinate
        return CollisionsFinder.object_collision(unmoving_object, sidescrolling_object) and object_sidescrolled

    def is_side_collision(player, platform):
        # So the player doesn't land on the platform and also can't move
        player_is_on_platform = CollisionsFinder.on_platform(platform, player, True)
        return CollisionsFinder.object_collision(platform, player) and not player_is_on_platform

    def platform_rightside_collision(player, platform):
        # So player doesn't go from in and out of platform see on_platform for me details
        if player.x_coordinate == platform.right_edge:
            return True
        last_player = HistoryKeeper.get_last("player")
        if last_player is None:
            return
        is_side_collision = CollisionsFinder.is_side_collision(player, platform)
        return is_side_collision and last_player.x_coordinate >= platform.right_edge

    def platform_leftside_collision(player: GameObject, platform: GameObject):
        # So player doesn't go from in and out of platform see on_platform for me details
        if player.right_edge == platform.x_coordinate:
            return True
        
        last_player = HistoryKeeper.get_last("player")
        if last_player is None:
            return
        if not CollisionsFinder.is_side_collision(player, platform):
            return
        leftside_collision = (last_player.right_edge <= platform.x_coordinate
                              or CollisionsFinder.is_sidescrolling__collision(player, platform))
        return leftside_collision

class PhysicsEngine:
    gravity_pull = y_velocities
    player_died = False
    
    def do_gravity(player):
        player.y_coordinate += VelocityCalculator.calc_distance(PhysicsEngine.gravity_pull)

    def is_beyond_screen_right(player: Player):
        if player.x_coordinate >= screen_length - player.length:
            return True

        return False

    def is_beyond_screen_left(player: Player):
        if player.x_coordinate <= 0:
            return True

        return False

    def player_hit_top_of_screen(player: Player):
        if player.y_coordinate <= 0:
            player.can_jump = False

    def is_below_screen_bottom(player: Player):
        if player.y_coordinate >= screen_height:
            return True

        return False


class InteractionEngine:
    def player_enemy_interactions(player: Player, enemy: SimpleEnemy):
        if not CollisionsFinder.object_collision(player, enemy):
            return

        player_halfway_point = player.x_coordinate + .5 * player.length
        enemy_halfway_point = enemy.x_coordinate + .5 * enemy.length
        last_enemy = HistoryKeeper.get_last(enemy.name)
        last_player = HistoryKeeper.get_last("player")
        if (last_enemy or last_player) is None:
            return
        is_sidescrolling_collision = CollisionsFinder.is_sidescrolling__collision(player, enemy)
        is_leftside_movement_collision = last_player.right_edge < last_enemy.x_coordinate
        landing_collision = player_halfway_point < enemy_halfway_point
        knockback_is_left = is_sidescrolling_collision or is_leftside_movement_collision or landing_collision
        
        player.knockback(10, direction_is_left=knockback_is_left)

    def enemy_whip_interactions(enemy: SimpleEnemy, whip: Whip):
        if not whip.whip_is_extending:
            return
        if not CollisionsFinder.object_collision(enemy, whip):
            return
        knockback_is_left = (enemy.x_coordinate <= whip.x_coordinate)
        enemy.knockback(10, direction_is_left=knockback_is_left)