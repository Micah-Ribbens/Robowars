from items import Whip
from players import Player
from important_variables import (
    screen_height,
    screen_width,
    consistency_keeper
)
from wall_of_death import WallOfDeath

class CollisionsFinder:
    # Player or Enemy for character
    def enemy_on_platform(platform, enemy):
        enemy_right_edge = enemy.x_coordinate + enemy.width
        platform_end = platform.x_coordinate + platform.length
        if enemy.x_coordinate + enemy.movement_speed < platform.x_coordinate:
            return False
        if enemy_right_edge + enemy.movement_speed > platform_end:
            return False

        return (not (enemy.x_coordinate < platform.x_coordinate)
               and not (enemy_right_edge > platform_end))

    def on_platform(platform, character, last_character_bottom=None):
        within_platform_length = character.x_coordinate >= (
            platform.x_coordinate - character.width) and (
            character.x_coordinate <= platform.x_coordinate + platform.length)
            
        character_bottom = character.y_coordinate + character.height
        # platform_bottom = platform.y_coordinate + platform.width

        within_platform_height = character_bottom >= platform.y_coordinate
        # Prevents character from clipping on top of platform
        # if last_character_bottom is not None:
        #     # print(last_character_bottom < platform.x_coordinate)
        #     return within_platform_height and within_platform_length and last_character_bottom < platform.y_coordinate

        return within_platform_height and within_platform_length
        
    def platform_right_boundary(character, platform, last_player_x_coordinate):
        character_bottom = character.y_coordinate + character.height
        platform_bottom = platform.y_coordinate + platform.width
        character_right_edge = character.x_coordinate + character.width
        platform_end = platform.x_coordinate + platform.length

        y_coordinate_collision = (character_bottom > platform.y_coordinate and
                                  platform_bottom > character.y_coordinate)
        # Depends what angle its coming from if its from the right edge it would have to be greater than the platforms end
        right_side_collision = (character.x_coordinate <= platform_end and
                               character_right_edge >= platform.x_coordinate
                               and last_player_x_coordinate >= platform_end - character.movement)
        
        return y_coordinate_collision and right_side_collision

    def platform_left_boundary(character, platform, last_player_x_coordinate):
        character_bottom = character.y_coordinate + character.height
        platform_bottom = platform.y_coordinate + platform.width
        character_right_edge = character.x_coordinate + character.width
        last_character_right_edge = last_player_x_coordinate + character.width
        platform_end = platform.x_coordinate + platform.length

        y_coordinate_collision = (character_bottom > platform.y_coordinate and
                                  platform_bottom > character.y_coordinate)
        left_side_collision = (character.x_coordinate <= platform_end and
                            character_right_edge >= platform.x_coordinate
                            and last_character_right_edge <= platform.x_coordinate + character.movement)
        return y_coordinate_collision and left_side_collision

class PhysicsEngine:
    gravity_pull = screen_height * .0005
    character_died = False
    def _improve_variables(self):
        self.gravity_pull = screen_height * consistency_keeper.calculate_new_speed(.0005)

    def set_gravity(self, gravity):
        PhysicsEngine.gravity_pull = gravity

    def do_gravity(self, character):
        character.y_coordinate += self.gravity_pull

    def is_beyond_screen_right(self, player):
        if player.x_coordinate >= screen_width - player.width:
            return True

        return False

    def is_beyond_screen_left(self, player):
        if player.x_coordinate <= 0:
            return True

        return False

    def screen_boundaries(self, player: Player):
        # print("I WAS CALLED")
        if player.y_coordinate <= 0:
            # print("NO MORE JUMPING!")
            player.can_jump = False

        # else:
        #     player.can_jump = True

        # self.is_within_screen(player)

    def is_within_screen(self, player):
        if player.y_coordinate >= screen_height:
            return False

        return True

    def platform_side_scrolling(self, player, platform):
        if player.move_right:
            platform.move_left(player.movement)

    def enemy_side_scrolling(self, player, enemy):
        if player.move_right:
            enemy.side_scroll(player.movement)


class InteractionsFinder:
    def player_whip(player: Player, whip: Whip):
        if player.throw_whip:
            whip.extend_whip(player.is_facing_right)

        whip.render(player)

    def player_enemy_interactions(player, enemy):
        enemy_right_side = enemy.x_coordinate + enemy.width
        player_bottom = player.y_coordinate + player.height
        enemy_bottom = enemy.y_coordinate + enemy.height

        x_coordinate_collision = (player.x_coordinate + player.width >=
                                  enemy.x_coordinate and player.x_coordinate <= enemy_right_side)

        y_coordinate_collision = (player_bottom >= enemy.y_coordinate
                                  and player.y_coordinate <= enemy_bottom)

        if x_coordinate_collision and y_coordinate_collision:
            if player.x_coordinate + player.width <= enemy.x_coordinate + 0.5 * enemy.width:
                player.x_coordinate -= 20
                player.knockback_left()
            else:
                player.x_coordinate += 20
                player.knockback_right()

    def enemy_whip_interactions(enemy, whip: Whip):
        if not whip.whip_is_extending:
            return
        enemy_right_edge = enemy.x_coordinate + enemy.width
        whip_left_start = whip.x_coordinate + whip.length
        # collision left and collision right don't work perfectly, so I just use what direction whip is going to figure out knockback
        collision_left = enemy_right_edge >= whip.x_coordinate and enemy_right_edge <= whip_left_start
 
        collision_right = (whip.x_coordinate <= enemy.x_coordinate + enemy.width
                           and whip.x_coordinate - whip.length >= enemy.x_coordinate)
        
        x_coordinate_collision = collision_left or collision_right

        y_coordinate_collision = (whip.y_coordinate + whip.height >= enemy.y_coordinate
                                  and whip.y_coordinate <= enemy.y_coordinate + enemy.height)
        if y_coordinate_collision and x_coordinate_collision and whip.whip_is_going_right:
            enemy.knockback_right()
        
        elif y_coordinate_collision and x_coordinate_collision and not whip.whip_is_going_right:
            enemy.knockback_left()
    
    def player_wall_of_death_interactions(player: Player):
        if player.move_right:
            WallOfDeath.move_backwards(player.movement)
        
        wall_of_death_end = WallOfDeath.x_coordinate + WallOfDeath.length
        if wall_of_death_end >= player.x_coordinate:
            player.current_health = 0
        

