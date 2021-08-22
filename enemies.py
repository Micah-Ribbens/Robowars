from random import random
from engines import CollisionsFinder
from items import Whip
from UtilityClasses import GameCharacters, Segment, UtilityFunctions
from important_variables import (
    screen_length,
    screen_height
)
from velocity_calculator import (
    VelocityCalculator  
)
class SimpleEnemy(GameCharacters):
    velocity = VelocityCalculator.give_velocity(screen_length, 112)
    knockback_distance = VelocityCalculator.give_measurement(screen_length, 25)
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
    def __init__(self, player):
        self.x_coordinate = 80
        self.length = VelocityCalculator.give_measurement(screen_length, 5)
        self.height = VelocityCalculator.give_measurement(screen_height, 15)
        self.y_coordinate = 80
        self.full_health = 50
        self.current_health = self.full_health
        self.color = self.black
        self.item = Whip(self)
        self.player = player
        self.invincibility__max_time = .4

    def has_to_wait_to_use_again(self):
        max_wait_time = 2
        if self.total_wait_time > 0 and self.total_wait_time < max_wait_time:
            self.total_wait_time += VelocityCalculator.time
            return True

        elif self.total_wait_time >= max_wait_time:
            self.total_wait_time = 0
            return False

        if self.item.whip_is_extending:
            self.total_wait_time += VelocityCalculator.time
            return False

    # def close_enough_to_player(self):
    #     if self.player_is_within_range():
    #         self.time_next_to_player += VelocityCalculator.time
    #         return False
    #     else:
    #         self.time_next_to_player = 0

    #     if self.player_is_within_range() and self.time_next_to_player > .5:
    #         return True
    def can_use_item(self):
        needed_wait_time = 1
        if self.is_flinching:
            return False
        if self.time_wait_to_use_weapon > needed_wait_time:
            self.time_wait_to_use_weapon = 0
            self.color = self.black
            return not self.has_to_wait_to_use_again() and not self.is_flinching

        if self.player_is_within_range() or self.time_wait_to_use_weapon > 0:
            self.time_wait_to_use_weapon += VelocityCalculator.time
            self.color = self.yellow
        return False

    def movement(self):
        if not self.can_move:
            return

        if self.is_invincible: 
            self.color = self.white
            self.do_invincibility()
        else:
            self.color = self.black

        if self.is_flinching:
            self.flinch()
            self.item.stop_item_usage()
            return

        if self.can_use_item():
            self.item.use_item()
        
        self.change_direction_if_necessary()
        if CollisionsFinder.object_collision(self, self.player) and self.is_moving_left:
            self.x_coordinate = self.player.right_edge
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
        eye_1 = Segment(
            is_percentage=True,
            color=(255, 42, 42),
            amount_from_top=30,
            amount_from_left=30,
            length_amount=8,
            width_amount=10
        )
        eye_2 = Segment(
            is_percentage=True,
            color=(255, 42, 42),
            amount_from_top=30,
            amount_from_left=70,
            length_amount=8,
            width_amount=10
        )
        self.draw_in_segments([eye_1, eye_2])
