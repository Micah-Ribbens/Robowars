from important_variables import (
    screen_height,
    screen_width,
    consistency_keeper
)


# Fix the movements yeah!!
# Buffer is the character movement down or gravity whichever is greater
# The parameter "character" can be a player or an enemy
class CollisionsFinder:
    # Buffer is the character movement down or gravity whichever is greater
    # Player or Enemy for character
    def on_platform(self, platform, character, buffer):
        character_bottom = character.get_y_coordinate() + character.height
        platform_y_coordinate = platform.get_y_coordinate()
        platform_x_cordinate = platform.get_x_coordinate()
        character_x_coordinate = character.get_x_coordinate()

        within_platform_length = character_x_coordinate >= (
            platform_x_cordinate - character.get_length()) and (
            character_x_coordinate <= platform_x_cordinate + platform.length)

        return (character_bottom >= platform_y_coordinate and
                character_bottom <= platform_y_coordinate + buffer
                and within_platform_length)

    def platform_side_boundaries(self, character, platform):
        character_y_coordinate = character.get_y_coordinate()
        platform_y_coordinate = platform.get_y_coordinate()
        platform_x_coordinate = platform.get_x_coordinate()
        character_x_coordinate = character.get_x_coordinate()

        character_bottom = character_y_coordinate + character.height
        platform_bottom = platform_y_coordinate + platform.width
        character_right_edge = character_x_coordinate + character.length
        buffer = character.movement * 4
        platform_end = platform_x_coordinate + platform.length

        y_coordinate_collision = (character_bottom > platform_y_coordinate and
                                  platform_bottom > character_y_coordinate)

        left_side_collision = (character_right_edge >= platform_x_coordinate and
                               character_right_edge <= platform_x_coordinate + buffer)

        right_side_collision = (character_x_coordinate <= platform_end and
                                character_x_coordinate + buffer >= platform_end)

        player_right_side_collided = False
        player_left_side_collided = False
        if self.on_platform(platform, character, character.movement_down * 2):
            return [False, False]

        if y_coordinate_collision and left_side_collision:
            player_right_side_collided = True
        else:
            player_right_side_collided = False

        if y_coordinate_collision and right_side_collision:
            player_left_side_collided = True

        else:
            player_left_side_collided = False

        return [player_right_side_collided,
                player_left_side_collided]


class PhysicsEngine:
    gravity_pull = screen_height * .0005
    character_died = False

    def _improve_variables(self):
        self.gravity_pull = screen_height * consistency_keeper.calculate_new_speed(.0005)

    def set_gravity(self, gravity):
        self.gravity_pull = gravity

    def player_is_on_platform(self, platform, character):
        self._improve_variables()
        collisions = CollisionsFinder()
        buffer = self.gravity_pull + character.movement_down

        return collisions.on_platform(platform, character, buffer)

    def do_gravity(self, character):
        object_y_coordinate = character.get_y_coordinate() + self.gravity_pull
        character.change_y_coordinate(object_y_coordinate)

    def is_beyond_screen_right(self, player):
        if player.get_x_coordinate() >= screen_width - player.get_length():
            return True

        return False

    def is_beyond_screen_left(self, player):
        if player.get_x_coordinate() <= 0:
            return True

        return False

    def screen_boundaries(self, player):
        if player.get_y_coordinate() <= 0:
            player.can_jump = False

        else:
            player.can_jump = True

        self.within_screen(player)

    def platform_left_boundary(self, player, platform):
        collisions = CollisionsFinder()
        temp = collisions.platform_side_boundaries(player, platform)
        player_left_side_collided = temp[1]

        if player_left_side_collided:
            return True

        return False

    def platform_right_boundary(self, player, platform):
        collisions = CollisionsFinder()
        temp = collisions.platform_side_boundaries(player, platform)
        player_right_side_collided = temp[0]

        if player_right_side_collided:
            return True

        return False

    def is_within_screen(self, player):
        if player.get_y_coordinate() >= screen_height:
            return False

        return True

    def platform_side_scrolling(self, player, platform):
        if player.move_right:
            platform.move_left(player.movement)

    def enemy_side_scrolling(self, player, enemy):
        if player.move_right:
            enemy.side_scroll(player.movement)


class InteractionsFinder:
    def player_whip(player, whip):
        if player.throw_whip:
            whip.extend_whip()

        whip_x_coordinate = player.get_x_coordinate() + player.get_length()
        whip_y_coordinate = player.get_y_coordinate() + (
                             (player.get_height() * .5))

        whip.render(whip_x_coordinate, whip_y_coordinate, player.height)

    def player_enemy_interactions(player, enemy):
        player_y_coordinate = player.get_y_coordinate()
        player_x_coordinate = player.get_x_coordinate()
        player_height = player.get_height()
        player_length = player.get_length()

        enemy_y_coordinate = enemy.get_y_coordinate()
        enemy_height = enemy.get_height()
        enemy_length = enemy.get_length()
        enemy_right_side = enemy.x_coordinate + enemy_length
        player_bottom = player_y_coordinate + player_height
        enemy_bottom = enemy_y_coordinate + enemy_height

        x_coordinate_collision = (player_x_coordinate + player_length >=
                                  enemy.x_coordinate and player_x_coordinate <= enemy_right_side)

        y_coordinate_collision = (player_bottom >= enemy_y_coordinate
                                  and player_y_coordinate <= enemy_bottom)

        if x_coordinate_collision and y_coordinate_collision:
            if player_x_coordinate + player_length <= enemy.x_coordinate + 0.5 * enemy.width:
                player.x_coordinate -= 20
                player.knockback_left()
            else:
                player.x_coordinate += 20
                player.knockback_right()

    def enemy_whip_interactions(enemy, whip):
        collision_left = (whip.x_coordinate + whip.length >= enemy.x_coordinate
                          and whip.x_coordinate <= enemy.x_coordinate + enemy.width)

        collision_right = (whip.x_coordinate <= enemy.x_coordinate + enemy.width
                           and whip.x_coordinate - whip.length >= enemy.x_coordinate)

        y_coordinate_collision = (whip.y_coordinate + whip.height >= enemy.y_coordinate
                                  and whip.y_coordinate <= enemy.y_coordinate + enemy.height)

        if y_coordinate_collision and collision_left:
            enemy.knockback_left()

        if y_coordinate_collision and collision_right:
            enemy.knockback_right()
