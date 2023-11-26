from UtilityClasses import GameObject, HistoryKeeper
from items import Whip
from important_variables import (
    screen_height,
    screen_length,
    y_velocities
)
from velocity_calculator import VelocityCalculator
from wall_of_death import WallOfDeath
from platforms import Platform

class CollisionsFinder:
    def on_platform(platform, player, is_player):
        is_platform_collision = CollisionsFinder.object_collision(player, platform)
        if player.bottom == platform.y_coordinate:
            return is_platform_collision
        if not is_player or len(HistoryKeeper.get("player")) <= 1:
            return is_platform_collision
        
        # If this logic isn't in place last_player_y_coordinate could be below the platform's y_coordinate, which would make it do gravity
        # EX: (platform y coordinate is 400) player's bottom goes from 399 to 401 putting it at 400, but last player bottom would be 401 causing gravity

        last_player = HistoryKeeper.get_last("player")
        if last_player is None:
            return
        return is_platform_collision and last_player.bottom <= platform.y_coordinate

    def object_collision(object1, object2):
        return (CollisionsFinder.object_length_collision(object1, object2)
                and CollisionsFinder.object_height_collision(object1, object2))
    
    def object_length_collision(object1, object2):
        return (object1.x_coordinate <= object2.right_edge and
                object1.right_edge >= object2.x_coordinate)
    
    def object_height_collision(object1, object2):
        return (object1.bottom >= object2.y_coordinate and
                object1.y_coordinate <= object2.bottom)
        

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
            return False
        is_side_collision = CollisionsFinder.is_side_collision(player, platform)
        return is_side_collision and last_player.x_coordinate >= platform.right_edge

    def platform_leftside_collision(player: GameObject, platform: GameObject):
        # So player doesn't go from in and out of platform see on_platform for me details
        if player.right_edge == platform.x_coordinate:
            return True
        
        last_player = HistoryKeeper.get_last("player")
        if last_player is None:
            return False

        if not CollisionsFinder.is_side_collision(player, platform):
            return False

        leftside_collision = (last_player.right_edge <= platform.x_coordinate
                              or CollisionsFinder.is_sidescrolling__collision(player, platform))

        return leftside_collision

class PhysicsEngine:
    gravity_pull = -3500
    player_died = False
    
    def do_gravity(player):
        change = -PhysicsEngine.distance_change(0, PhysicsEngine.gravity_pull, player.time_affected_by_gravity)
        player.y_coordinate = change + player.last_y_unmoving

    def is_beyond_screen_right(player):
        if player.x_coordinate >= screen_length - player.length:
            return True

        return False

    def distance_change(velocity, acceleration, time):
        return velocity * time + (acceleration * time ** 2 / 2)

    def is_beyond_screen_left(player):
        if player.x_coordinate <= 0:
            return True

        return False

    def player_hit_top_of_screen(player):
        if player.y_coordinate <= 0:
            player.can_jump = False

    def is_below_screen_bottom(player):
        if player.y_coordinate >= screen_height:
            return True

        return False


class InteractionEngine:
    def player_enemy_interactions(player, enemy):
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
        
        player.knockback(enemy.knockback_distance, direction_is_left=knockback_is_left)
        if not player.is_invincible:
            player.current_health -= 5
            player.flinch()

    def object_whip_interactions(object, object_hitting):
        if not object_hitting.item.whip_is_extending:
            # As in if is thrown and hits the enemy it can't hit the enemy during that same hit
            object_hitting.hit_during_item_cycle = False
            return

        if not CollisionsFinder.object_collision(object, object_hitting.item):
            return

        if object.shield.is_being_used and InteractionEngine.shield_is_right_direction(object, object_hitting):
            object_hitting.flinch()
            object_hitting.current_health -= object.shield.damage
            object.shield.caused_flinch = True
            return

        # if object.is_invincible or object_hitting.hit_during_item_cycle:
        #     print(object.is_invincible, object_hitting.hit_during_item_cycle)

        if not object.is_invincible and not object_hitting.hit_during_item_cycle:
            object.flinch()
            object_hitting.hit_during_item_cycle = True
            object.current_health -= object_hitting.item.damage
    
    def shield_is_right_direction(object_blocking, object_hitting):
        if object_blocking.is_facing_right and object_hitting.x_coordinate >= object_blocking.right_edge:
            return True
        if not object_blocking.is_facing_right and object_hitting.right_edge <= object_blocking.x_coordinate:
            return True
        return False
        
