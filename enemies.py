import pygame
# from pygame.constants import CONTROLLER_AXIS_INVALID
# from engines import CollisionsFinder
from important_variables import (
    screen_width,
    # screen_height,
    win,
    # consistency_keeper, 
)
from velocity_calculator import (
    VelocityCalculator  
)
class Enemy:
    full_health = 20 
    current_health = 20
    color = (0, 0, 250)
    x_coordinate = 80
    width = 40
    height = 40
    y_coordinate = 80

    def draw(self):
        pygame.draw.rect(win, (self.color), (self.x_coordinate,
                         self.y_coordinate, self.width, self.height))

class SimpleEnemy(Enemy):
    velocity = VelocityCalculator.give_velocity(screen_width, 112)
    knockback_distance = VelocityCalculator.give_measurement(screen_width, 25)
    is_moving_left = True
    is_moving_right = False
    damage = 5

    # def _improve_variables(self):
    #     self.movement_speed = consistency_keeper.calculate_new_speed(self.base_speed)

    def movement(self, is_on_platform, platform):
        # self._improve_variables()
        if self.is_moving_right and not is_on_platform:
            self.is_moving_left = True
            # print("Teleport right")
            self.is_moving_right = False
            self.x_coordinate = platform.x_coordinate + platform.length - self.width

        elif self.is_moving_left and not is_on_platform:
            # print("Teleport left")
            self.is_moving_left = False
            self.is_moving_right = True
            self.x_coordinate = platform.x_coordinate

        if self.is_moving_right:
            self.x_coordinate += VelocityCalculator.calc_distance(self.velocity)

        if self.is_moving_left:
            self.x_coordinate -= VelocityCalculator.calc_distance(self.velocity)

    def side_scroll(self, change):
        self.x_coordinate -= change
    
    def knockback_right(self):
        self.x_coordinate += self.knockback_distance
        self.current_health -= 10

    def knockback_left(self):
        self.x_coordinate -= self.knockback_distance
        self.current_health -= 10

