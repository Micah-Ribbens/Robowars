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
        buffer = character.movement
        platform_end = platform_x_coordinate + platform.length

        y_coordinate_collision = (character_bottom > platform_y_coordinate and
                                  platform_bottom > character_y_coordinate)

        left_side_collision = (character_right_edge >= platform_x_coordinate and
                               character_right_edge <= platform_x_coordinate + buffer)

        right_side_collision = (character_x_coordinate <= platform_end and
                                character_x_coordinate + buffer >= platform_end)

        player_right_side_collided = False
        player_left_side_collided = False

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

    def gravity(self, platform, character):
        self._improve_variables()
        collisions = CollisionsFinder()
        buffer = self.gravity_pull + character.movement_down
        on_platform = collisions.on_platform(platform, character, buffer)

        if not on_platform and not character.is_jumping:
            object_y_coordinate = character.get_y_coordinate() + self.gravity_pull
            character.change_y_coordinate(object_y_coordinate)

    def movement_possible(self, platform, character):
        collisions = CollisionsFinder()
        buffer = self.gravity_pull + character.movement_down
        on_platform = collisions.on_platform(platform, character, buffer)
        if on_platform:
            character.on_platform = True
            character.move_down = False
        else:
            character.on_platform = False
            character.move_down = True

    def boundaries(self, character, platform):
        collisions = CollisionsFinder()
        temp = collisions.platform_side_boundaries(character, platform)
        player_right_side_collided = temp[0]
        player_left_side_collided = temp[1]

        if character.get_x_coordinate() <= 0 or player_left_side_collided:
            character.can_move_left = False
        else:
            character.can_move_left = True

        if (character.get_x_coordinate() >= screen_width - character.get_length()
                or player_right_side_collided):

            character.can_move_right = False
        else:
            character.can_move_right = True

        if character.get_y_coordinate() <= 0:
            character.can_jump = False
        else:
            character.can_jump = True

        self.within_screen(character, platform.get_y_coordinate())

    def within_screen(self, character, platform_y_coordinate):
        if character.get_y_coordinate() >= screen_height:
            self.character_died = True

    def platform_side_scrolling(self, player, platform):
        if player.move_right:
            platform.move_left(player.movement)

    def enemy_side_scrolling(self, player, enemy):
        if player.move_right:
            enemy.side_scroll(player.movement)


class InteractionsFinder:
    def player_whip(self, player, whip):
        if player.throw_whip:
            whip.extend_whip()
        whip_x_coordinate = player.get_x_coordinate() + player.get_length()
        whip_y_coordinate = player.get_y_coordinate() + (
                             (player.get_height() * .5))
        whip.render(whip_x_coordinate, whip_y_coordinate, player.height)
