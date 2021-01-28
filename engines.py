from important_variables import (
    screen_height,
    screen_width
)
#Fix the movements yeah!!
#Buffer is the character movement down or gravity whichever is greater
#The parameter "character" can be a player or an enemy


class CollisionsFinder:
    # Buffer is the character movement down or gravity whichever is greater
    # Player or Enemy for character
    def on_platform(self, platform, character, buffer):
        character_y_coordinate = character.get_y_coordinate() + character.get_height() 
        platform_y_coordinate = platform.get_y_coordinate()
        platform_x_cordinate = platform.get_x_coordinate()
        character_x_coordinate = character.get_x_coordinate()

        within_platform_length = character_x_coordinate >= platform_x_cordinate - character.get_length() and (
            character_x_coordinate <= platform_x_cordinate + platform.length
        )

        return (character_y_coordinate >= platform_y_coordinate and  
                character_y_coordinate <= platform_y_coordinate + buffer and within_platform_length)

    def platform_side_boundaries(self, character, platform):
        character_y_coordinate = character.get_y_coordinate()
        platform_y_coordinate = platform.get_y_coordinate()
        platform_x_coordinate = platform.get_x_coordinate()
        character_x_coordinate = character.get_x_coordinate()

        y_coordinate_collision = (character_y_coordinate + character.height > platform_y_coordinate and 
                                  platform_y_coordinate + platform.width > character_y_coordinate)
        x_coordinate_collision_left_side = (character_x_coordinate + character.length >= platform_x_coordinate and 
                                            character_x_coordinate + character.length <= platform_x_coordinate + character.movement)

        x_coordinate_collision_right_side = (character_x_coordinate <= platform_x_coordinate + platform.length and 
                                             character_x_coordinate + character.movement >= platform_x_coordinate + platform.length)

        is_not_within_platform_left_boundary = False
        is_not_within_platform_right_boundary = False

        if y_coordinate_collision and x_coordinate_collision_left_side:
            is_not_within_platform_left_boundary = True
        else:
            is_not_within_platform_left_boundary = False

        if y_coordinate_collision and x_coordinate_collision_right_side:
            is_not_within_platform_right_boundary = True

        else:
            is_not_within_platform_right_boundary = False

        return [is_not_within_platform_left_boundary, is_not_within_platform_right_boundary]

    def enemy_boundaries(self, player, enemy):
        enemy_side_boundaries = self.player.x_coordinate + self.player.lenght


class PhysicsEngine:
    gravity_pull = screen_height * .0009
    character_died = False

    def set_gravity(self, gravity):
        self.gravity_pull = gravity_pull

    def gravity(self, platform, character):
        collisions = CollisionsFinder()
        on_solid_object = collisions.on_platform(platform, character, self.gravity_pull + character.movement_down)

        if not on_solid_object and not character.is_jumping:
            object_y_coordinate = character.get_y_coordinate() + self.gravity_pull
            character.change_y_coordinate(object_y_coordinate)

    def movement_possible(self, platform, character):
        collisions = CollisionsFinder()
        on_solid_object = collisions.on_platform(platform, character, self.gravity_pull + character.movement_down)
        if on_solid_object:
            character.on_platform = True
            character.move_down = False
        else:
            character.on_platform = False
            character.move_down = True

    def boundaries(self, character, platform):
        collisions = CollisionsFinder()
        temp = collisions.platform_side_boundaries(character, platform)
        is_not_within_platform_left_boundary = temp[0]
        is_not_within_platform_right_boundary = temp[1]

        if character.get_x_coordinate() <= 0 or is_not_within_platform_right_boundary:
            character.can_move_left = False
        else:
            character.can_move_left = True

        if character.get_x_coordinate() >= screen_width - character.get_length() or is_not_within_platform_left_boundary:
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
        whip_y_coordinate = player.get_y_coordinate() + (player.get_height() * .5)
        whip.render(whip_x_coordinate, whip_y_coordinate)

    def player_enemy_interactions(self, player, enemy):
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
                player.collide_left()
            else:
                player.x_coordinate += 20
                player.collide_right()

    def enemy_whip_interactions(self, enemy, whip):
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
