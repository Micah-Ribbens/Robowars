from base.engines import CollisionsFinder
from game_components.items import Shield, Whip
from base.utility_classes import GameCharacters, Segment, UtilityFunctions
from base.important_variables import (
    screen_length,
    screen_height
)
from base.velocity_calculator import (
    VelocityCalculator  
)
class SimpleEnemy(GameCharacters):
    velocity = VelocityCalculator.give_velocity(screen_length, 60)
    knockback_distance = VelocityCalculator.give_measurement(screen_length, 5)
    is_moving_left = True
    is_facing_right = False
    damage = 5
    is_on_platform = True
    platform_on = None
    item = None
    player = None
    total_wait_time = 0 
    time_next_to_player = 0
    time_wait_to_use_weapon = 0
    can_move = True
    eye_color = (255, 42, 42)
    shield = None
    have_to_wait_to_use_again = False
    time_affected_by_gravity = 0
    last_y_unmoving = 0

    def __init__(self, player=None):
        self.x_coordinate = 80
        self.length = VelocityCalculator.give_measurement(screen_length, 5)
        self.height = VelocityCalculator.give_measurement(screen_height, 15)
        self.y_coordinate = 80
        self.full_health = 20
        self.current_health = self.full_health
        self.color = self.black
        self.item = Whip(self)
        self.item.damage = 10
        self.player = player
        self.invincibility__max_time = .4
        self.shield = Shield(self)

    def use_item_if_can(self):
        if self.is_flinching:
            return 

        if self.shield.caused_flinch:
            self.counter()
            return

        if self.time_based_activity_is_done("wait to use"+self.name, 2, self.shield.is_being_used, self.player_is_within_range()) and not self.shield.is_being_used:
            move_type = Whip.LEFT_ATTACK if self.is_moving_left else Whip.RIGHT_ATTACK
            self.item.use_item(move_type)

    def figure_out_blocking(self):
        # A rough amount; won't be exact since each iteration takes a different amount of time
        if VelocityCalculator.time == 0 or self.item.whip_is_extending or self.shield.caused_flinch:
            return
        iteration_in_a_second = 1 / VelocityCalculator.time
        can_use_shield = self.player_is_within_range() and UtilityFunctions.random_chance(1, int(iteration_in_a_second * 5))
        if can_use_shield:
            self.shield.use_item()

    def counter(self):
        if self.time_based_activity_is_done("wait to hit after block"+self.name, .3, False):
            self.shield.caused_flinch = False
            move_type = Whip.LEFT_ATTACK if self.is_moving_left else Whip.RIGHT_ATTACK
            self.item.use_item(move_type)
            self.shield.stop_usage()
        
    def movement(self):
        if not self.can_move:
            return

        if self.is_flinching:
            self.flinch()
            self.color = (250, 0, 0)
            self.item.stop_item_usage()
            self.shield.stop_item_usage()
            return
        
        else: 
            self.color = self.black

        self.figure_out_blocking()

        self.use_item_if_can()

        self.change_direction_if_necessary()

        if CollisionsFinder.object_collision(self, self.player):
            return

        elif CollisionsFinder.object_collision(self, self.player):
            self.x_coordinate = self.player.x_coordinate - self.length

        if not self.is_moving_left:
            self.x_coordinate += VelocityCalculator.calc_distance(self.velocity)

        if self.is_moving_left:
            self.x_coordinate -= VelocityCalculator.calc_distance(self.velocity)

    def player_is_within_range(self):
        length = self.length
        x_coordinate = self.x_coordinate
        # Setting it to max to see if it was the max_length would it hit the player
        self.length = self.item.max_length + length
        if not self.is_facing_right:
            self.x_coordinate -= self.item.max_length
        if CollisionsFinder.object_length_collision(self, self.player):
            self.length = length
            self.x_coordinate = x_coordinate
            return True
        else:
            self.length = length
            self.x_coordinate = x_coordinate
            return False

    def change_direction_if_necessary(self):
        self.change_direction_based_on_player()
        # Based of platform has to come last since they both change enemy direction and staying on platform is more important than following player
        self.change_direction_if_off_platform()

    def change_direction_based_on_player(self):
        player_on_enemy_platform = CollisionsFinder.on_platform(self.platform_on, self.player, True)
        # There should be a decent gap between the enemy and the player, so the enemy isn't inside the player
        min_gap = self.length * .13
        if not player_on_enemy_platform:
            return

        if self.right_edge + min_gap < self.player.right_edge:
            self.is_moving_left = False
            self.is_facing_right = True
        if self.x_coordinate - min_gap > self.player.right_edge:
            self.is_moving_left = True
            self.is_facing_right = False

    def change_direction_if_off_platform(self):
        within_platform_length = (self.x_coordinate >= self.platform_on.x_coordinate 
                                  and self.right_edge <= self.platform_on.right_edge)
        if within_platform_length:
            return
        if self.is_moving_left:
            self.is_moving_left = False
            self.is_facing_right = True
            self.x_coordinate = self.platform_on.x_coordinate
        else:
            self.is_moving_left = True
            self.is_facing_right = False
            self.x_coordinate = self.platform_on.right_edge - self.length

    def draw(self):
        eye_color = (255, 42, 42)
        if self.player_is_within_range():
            eye_color = self.yellow

        eye_1 = Segment(
            is_percentage=True,
            color=eye_color,
            amount_from_top=30,
            amount_from_left=30,
            length_amount=8,
            width_amount=10
        )
        eye_2 = Segment(
            is_percentage=True,
            color=eye_color,
            amount_from_top=30,
            amount_from_left=70,
            length_amount=8,
            width_amount=10
        )
        self.draw_in_segments([eye_1, eye_2])
