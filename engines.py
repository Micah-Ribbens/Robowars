from UtilityClasses import GameObject
from enemies import SimpleEnemy
from items import Whip
from players import Player
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
    # Player or Enemy for character
    def enemy_on_platform(platform: Platform, enemy: SimpleEnemy):
        if enemy.x_coordinate < platform.x_coordinate:
            return False
        if enemy.right_edge > platform.right_edge:
            return False
        return True
    def on_platform(platform, character, is_player):
        # last_character_bottom is None in the first iteration because there was no previous character_bottom before that
        is_platform_collision = CollisionsFinder.platform_collision(character, platform)
        if not is_player or len(HistoryKeeper.get("player")) <= 1:
            return is_platform_collision
        
        # If this logic isn't in place last_player_y_coordinate could be below the platform's y_coordinate, which would make it do gravity
        # EX: (platform y coordinate is 400) player's bottom goes from 399 to 401 putting it at 400, but last player bottom would be 401 causing gravity
        if character.bottom == platform.y_coordinate:
            return is_platform_collision

        last_player = HistoryKeeper.get_last("player")

        return is_platform_collision and last_player.bottom <= platform.y_coordinate

    def platform_collision(character, platform):
        within_platform_height = (character.bottom >= platform.y_coordinate and
                                  character.y_coordinate <= platform.bottom)
        within_platform_length = (character.x_coordinate <= platform.right_edge and
                               character.right_edge >= platform.x_coordinate)
        
        return within_platform_height and within_platform_length
    # TODO instead of boundary maybe do collision
    def platform_rightside_collision(character, platform):
        is_platform_collision = CollisionsFinder.platform_collision(character, platform)
        # So character doesn't go from in and out of platform see on_platform for me details
        if character.x_coordinate == platform.right_edge:
            return is_platform_collision
        last_player = HistoryKeeper.get_last("player")

        return is_platform_collision and last_player.x_coordinate >= platform.right_edge

    def platform_leftside_collision(character: GameObject, platform: GameObject):
        is_platform_collision = CollisionsFinder.platform_collision(character, platform)
        # So character doesn't go from in and out of platform see on_platform for me details
        if character.right_edge == platform.x_coordinate:
            return is_platform_collision
        last_character_right_edge = HistoryKeeper.get_last("player").right_edge
        last_platform = HistoryKeeper.get_last(f"platform{platform.number}")
        is_sidescrolling_collision = last_platform.x_coordinate > platform.x_coordinate and last_platform.x_coordinate > character.x_coordinate

        leftside_collision = last_character_right_edge <= platform.x_coordinate or is_sidescrolling_collision
        return is_platform_collision and leftside_collision

class PhysicsEngine:
    gravity_pull = y_velocities
    character_died = False
    
    def do_gravity(character):
        character.y_coordinate += VelocityCalculator.calc_distance(PhysicsEngine.gravity_pull)

    def is_beyond_screen_right(player: Player):
        if player.x_coordinate >= screen_length - player.length:
            return True

        return False

    def is_beyond_screen_left(player: Player):
        if player.x_coordinate <= 0:
            return True

        return False
    # TODO boundaries its only testing one boundary; what boundary?
    def screen_boundaries(player: Player):
        if player.y_coordinate <= 0:
            player.can_jump = False
    # TODO is within screen? there are four sides and its only testing one side
    def is_within_screen(player: Player):
        if player.y_coordinate >= screen_height:
            return False

        return True


class InteractionsFinder:
    # TODO just a bit of an annoyance but here and other places things are said in past tense I like present so player.is_throwing_whip and "is" in booleans
    # Makes them sound more boolean like but "throw_whip" sounds like a function but it isn't
    def player_enemy_interactions(player: Player, enemy: SimpleEnemy):
        # TODO technically not left and right side collision because other things still have to be accounted for like enemy and player last x_coordinates
        right_collision = (player.right_edge >=
                                  enemy.x_coordinate and player.x_coordinate <= enemy.right_edge)

        left_collision = (player.x_coordinate <= enemy.right_edge 
                          and player.x_coordinate  >= enemy.x_coordinate)

        y_coordinate_collision = (player.bottom >= enemy.y_coordinate
                                  and player.y_coordinate <= enemy.bottom)
        x_coordinate_collision = left_collision or right_collision
        if not (y_coordinate_collision and x_coordinate_collision):
            return
        # TODO maybe change to halfway_point because that sounds better?
        player_half = player.x_coordinate + .5 * player.length
        enemy_half = enemy.x_coordinate + .5 * enemy.length
        # print(enemy.number)
        last_enemy = HistoryKeeper.get_last(f"enemy{enemy.number}")
        last_player = HistoryKeeper.get_last("player")
        # TODO maybe explain the why this works
        if last_player.right_edge < last_enemy.x_coordinate:
            player.knockback(10, direction_is_left=True)

        elif last_player.x_coordinate > last_enemy.right_edge:
            player.knockback(10, direction_is_left=False)

        elif player_half >= enemy_half:
            player.knockback(10, direction_is_left=False)
        
        else:
            player.knockback(10, direction_is_left=True)
        

    def enemy_whip_interactions(enemy: SimpleEnemy, whip: Whip):
        if not whip.whip_is_extending:
            return
        # Since length is negative it draws from right to left
        whip_leftside_end = whip.x_coordinate + whip.length
        collision_left = whip.x_coordinate >= enemy.right_edge and whip_leftside_end <= enemy.right_edge
 
        collision_right = (whip.x_coordinate <= enemy.right_edge
                           and whip.right_edge >= enemy.x_coordinate)

        x_coordinate_collision = collision_left or collision_right

        y_coordinate_collision = (whip.bottom >= enemy.y_coordinate
                                  and whip.y_coordinate <= enemy.bottom)
        # TODO change this based on where the enemy is
        if y_coordinate_collision and x_coordinate_collision and enemy.right_edge <= whip.x_coordinate:
            enemy.knockback(10, direction_is_left=True)
        
        elif y_coordinate_collision and x_coordinate_collision:
            enemy.knockback(10, direction_is_left=False)
        

