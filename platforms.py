from important_variables import (
    screen_height,
    win
)
import pygame


class Platform:
    platform_color = (80, 21, 46)
    x_coordinate = 100
    y_coordinate = screen_height - 100
    length = 400
    width = 100

    def get_x_coordinate(self):
        return self.x_coordinate

    def get_y_coordinate(self):
        return self.y_coordinate

    def change_x_coordinate(self, x_coordinate):
        self.x_coordinate = x_coordinate

    def change_y_coordinate(self, y_coordinate):
        self.y_coordinate = y_coordinate

    def draw(self):
        pygame.draw.rect(win, (self.platform_color), (self.x_coordinate,
                         self.y_coordinate, self.length, self.width))

    def move_left(self, change):
        self.x_coordinate -= change
