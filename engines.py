from enemies import SimpleEnemy
from math import inf
from items import Whip
from players import Player
from important_variables import (
    screen_height,
    screen_width,
    y_velocities
    # consistency_keeper
)
from velocity_calculator import VelocityCalculator
from wall_of_death import WallOfDeath
from platforms import Platform

class CollisionsFinder:
    # Player or Enemy for character
    def enemy_on_platform(platform: Platform, enemy: SimpleEnemy):
        enemy_right_edge = enemy.x_coordinate + enemy.width
        platform_end = platform.x_coordinate + platform.length
        if enemy.x_coordinate < platform.x_coordinate:
            # print("Teleport Left: ", enemy.x_coordinate - enemy.velocity, platform.x_coordinate)
            return False
        if enemy_right_edge > platform_end:
            # print("Teleport Right: ", enemy_right_edge + enemy.velocity, platform_end)
            return False
        return True
    def on_platform(platform, character, last_character_bottom=None):
        within_platform_length = character.x_coordinate >= (
            platform.x_coordinate - character.width) and (
            character.x_coordinate <= platform.x_coordinate + platform.length)
            
        character_bottom = character.y_coordinate + character.height
        within_platform_height = character_bottom >= platform.y_coordinate
        # Prevents character from clipping on top of platform
        if last_character_bottom is not None:
            return within_platform_height and within_platform_length and last_character_bottom <= platform.y_coordinate

        return within_platform_height and within_platform_length
    def platform_collision(character, platform):
        character_bottom = character.y_coordinate + character.height
        platform_bottom = platform.y_coordinate + platform.width
        character_right_edge = character.x_coordinate + character.width
        platform_end = platform.x_coordinate + platform.length

        y_coordinate_collision = (character_bottom > platform.y_coordinate and
                                  platform_bottom > character.y_coordinate)
        # Depends what angle its coming from if its from the right edge it would have to be greater than the platforms end
        right_side_collision = (character.x_coordinate <= platform_end and
                               character_right_edge >= platform.x_coordinate)
        
        return y_coordinate_collision and right_side_collision
    def platform_right_boundary(character, platform, last_player_x_coordinate):
        platform_end = platform.length + platform.width
        return CollisionsFinder.platform_collision(character, platform) and last_player_x_coordinate >= platform_end

    def platform_left_boundary(character, platform, last_player_x_coordinate):
        last_character_right_edge = last_player_x_coordinate + character.width
        return CollisionsFinder.platform_collision(character, platform) and last_character_right_edge < platform.x_coordinate

class PhysicsEngine:
    gravity_pull = y_velocities
    character_died = False
    
    def do_gravity(character):
        character.y_coordinate += VelocityCalculator.calc_distance(PhysicsEngine.gravity_pull)

    def is_beyond_screen_right(player: Player):
        if player.x_coordinate >= screen_width - player.width:
            return True

        return False

    def is_beyond_screen_left(player: Player):
        if player.x_coordinate <= 0:
            return True

        return False

    def screen_boundaries(player: Player):
        if player.y_coordinate <= 0:
            player.can_jump = False

    def is_within_screen(player: Player):
        if player.y_coordinate >= screen_height:
            return False

        return True

    def platform_side_scrolling(player: Player, platform: Platform):
        if player.move_right:
            platform.move_left(VelocityCalculator.calc_distance(player.running_velocity))

    def enemy_side_scrolling(player: Player, enemy: SimpleEnemy):
        if player.move_right:
            enemy.side_scroll(VelocityCalculator.calc_distance(player.running_velocity))


class InteractionsFinder:
    def player_whip(player: Player, whip: Whip):
        if player.throw_whip:
            whip.extend_whip(player.is_facing_right)

        whip.render(player)

    def player_enemy_interactions(player: Player, enemy: SimpleEnemy, last_player_x_coordinate, last_enemy_x_coordinate):
        enemy_right_side = enemy.x_coordinate + enemy.width
        player_bottom = player.y_coordinate + player.height
        enemy_bottom = enemy.y_coordinate + enemy.height

        right_collision = (player.x_coordinate + player.width >=
                                  enemy.x_coordinate and player.x_coordinate <= enemy_right_side)

        left_collision = (player.x_coordinate <= enemy_right_side 
                          and player.x_coordinate  >= enemy.x_coordinate)

        y_coordinate_collision = (player_bottom >= enemy.y_coordinate
                                  and player.y_coordinate <= enemy_bottom)
        x_coordinate_collision = left_collision or right_collision
        if not (y_coordinate_collision and x_coordinate_collision):
            return
        player_half = player.x_coordinate + .5 * player.width
        enemy_half = enemy.x_coordinate + .5 * enemy.width
        if last_player_x_coordinate + player.width < last_enemy_x_coordinate:
            player.knockback_left()

        elif last_player_x_coordinate > last_enemy_x_coordinate + enemy.width:
            player.knockback_right()

        elif player_half >= enemy_half:
            player.knockback_right()
        
        else:
            player.knockback_left()
        

    def enemy_whip_interactions(enemy: SimpleEnemy, whip: Whip):
        if not whip.whip_is_extending:
            return
        enemy_right_edge = enemy.x_coordinate + enemy.width
        whip_left_end = whip.x_coordinate + whip.length
        collision_left = whip.x_coordinate >= enemy_right_edge and whip_left_end <= enemy_right_edge
 
        collision_right = (whip.x_coordinate <= enemy.x_coordinate + enemy.width
                           and whip.x_coordinate + whip.length >= enemy_right_edge)

        x_coordinate_collision = collision_left or collision_right

        y_coordinate_collision = (whip.y_coordinate + whip.height >= enemy.y_coordinate
                                  and whip.y_coordinate <= enemy.y_coordinate + enemy.height)
        if y_coordinate_collision and x_coordinate_collision and whip.player_is_facing_right:
            enemy.knockback_right()
        
        elif y_coordinate_collision and x_coordinate_collision and not whip.player_is_facing_right:
            enemy.knockback_left()
    
    def player_wall_of_death_interactions(player: Player):
        if player.move_right:
            WallOfDeath.move_backwards(VelocityCalculator.calc_distance(player.running_velocity))
        
        wall_of_death_end = WallOfDeath.x_coordinate + WallOfDeath.length
        if wall_of_death_end >= player.x_coordinate:
            player.current_health = 0
        

