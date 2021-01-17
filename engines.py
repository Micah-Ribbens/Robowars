from important_variables import (
    screen_height,
    screen_width
)
class CollisionsFinder:
    def on_platform(self, platform, character):
        character_y_coordinate = character.get_y_coordinate() + character.getHeight() 
        platform_y_coordinate = platform.get_y_coordinate()
        platform_x_cordinate = platform.get_x_coordinate()
        character_x_coordinate = character.get_x_coordinate()

        within_platform_length = character_x_coordinate >= platform_x_cordinate - character.getLength() and (
            character_x_coordinate <= platform_x_cordinate + platform.length
        )
        
        return (character_y_coordinate >= platform_y_coordinate and within_platform_length)
    

class PhysicsEngine:
    gravity_pull = screen_height * .002
    def set_gravity(self, gravity):
        self.gravity_pull = gravity_pull
    def gravity(self, platform, character):
        collisions = CollisionsFinder()
        on_solid_object = collisions.on_platform(platform, character)

        if not on_solid_object and not character.is_jumping:
            object_y_coordinate = character.get_y_coordinate() + self.gravity_pull
            character.change_y_coordinate(object_y_coordinate)

    def movement_possible(self, platform, character):
        collisions = CollisionsFinder()
        on_solid_object = collisions.on_platform(platform, character)
        if on_solid_object:
            character.on_platform = True
            character.move_down = False
        else:
            character.on_platform = False
            character.move_down = True
        
    def boundaries(self, character, platform):
        if character.get_x_coordinate() <= 0:
            character.can_move_left = False
        else:
            character.can_move_left = True

        if character.get_x_coordinate() >= screen_width - character.getLength():
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
            character.reset_character_location(platform_y_coordinate)
        
    def side_scrolling(self, character, platform):
        if character.move_right:
            platform.move_left(character.movement)

    
class InteractionsFinder:
    def player_whip(self, player, whip):
        if player.throw_whip:
            whip.extend_whip()
        whip_x_coordinate = player.get_x_coordinate() + player.getLength()
        whip_y_coordinate = player.get_y_coordinate() + (player.getHeight() * .5)
        whip.render(whip_x_coordinate, whip_y_coordinate)
            