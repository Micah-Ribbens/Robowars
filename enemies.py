from UtilityClasses import GameCharacters, Segment
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
    damage = 5
    is_on_platform = True
    platform_on = None
    def __init__(self):
        self.x_coordinate = 80
        self.length = VelocityCalculator.give_measurement(screen_length, 5)
        self.height = VelocityCalculator.give_measurement(screen_height, 15)
        self.y_coordinate = 80
        self.full_health = 20
        self.current_health = 20
        self.color = self.black
    def movement(self):
        self.change_direction_if_necessary()
        if not self.is_moving_left:
            self.x_coordinate += VelocityCalculator.calc_distance(self.velocity)

        if self.is_moving_left:
            self.x_coordinate -= VelocityCalculator.calc_distance(self.velocity)

    def change_direction_if_necessary(self):
        within_platform_length = (self.x_coordinate >= self.platform_on.x_coordinate 
                                  and self.right_edge <= self.platform_on.right_edge)
        if within_platform_length:
            return
        if self.is_moving_left:
            self.is_moving_left = False
            self.x_coordinate = self.platform_on.x_coordinate
        else:
            self.is_moving_left = True
            self.x_coordinate = self.platform_on.right_edge - self.length
    
    def draw(self):
        red_segment = Segment(
            is_percentage=True,
            color=(255, 42, 0),
            amount_from_top=30,
            amount_from_left=0,
            length_amount=100,
            width_amount=10
        )
        self.draw_in_segments([red_segment])


