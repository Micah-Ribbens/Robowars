import pygame

from important_variables import (
    screen_width,
    screen_height,
    win,
    consistency_keeper
)


class Enemy:
    health = 10
    color = (0, 0, 250)
    x_coordinate = 80
    width = 40
    height = 40
    y_coordinate = screen_height - 100 - height

    def get_x_coordinate(self):
        return self.x_coordinate

    def get_y_coordinate(self):
        return self.y_coordinate

    def get_length(self):
        return self.width

    def get_height(self):
        return self.height

    def draw(self):
        pygame.draw.rect(win, (self.color), (self.x_coordinate,
                         self.y_coordinate, self.width, self.height))


class Simple_Enemy(Enemy):
    movement_speed = screen_width * .00025
    is_moving_left = True
    is_moving_right = False
    damage = 5

    def get_x_coordinate(self):
        if self.is_moving_left:
            return self.x_coordinate - self.width
        elif self.is_moving_right:
            return self.x_coordinate + self.width

    def _improve_variables(self):
        self.movement_speed = screen_width * (
            consistency_keeper.calculate_new_speed(.00025))

    def movement(self, is_on_platform):
        self._improve_variables()
        if self.is_moving_right and not is_on_platform:
            self.is_moving_left = True
            self.is_moving_right = False
        elif self.is_moving_left and not is_on_platform:
            self.is_moving_left = False
            self.is_moving_right = True

        if self.is_moving_right:
            self.x_coordinate += self.movement_speed
        if self.is_moving_left:
            self.x_coordinate -= self.movement_speed

    def side_scroll(self, change):
        self.x_coordinate -= change
