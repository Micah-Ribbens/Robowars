import pygame
from important_variables import (
    win,
    screen_height,
    screen_width,
    consistency_keeper
)


class Item:
    color = (0, 250, 0)
    x_coordinate = 0
    y_coordinate = 0
    base_length = 0.0125 * screen_width
    length = base_length
    base_height = screen_height * 0.02
    height = base_height

    def draw(self):
        pygame.draw.rect(win, (self.color), (self.x_coordinate,
                         self.y_coordinate, self.length, self.height))


class Whip(Item):
    whip_is_extending = False
    secs_needed = 0.12838726547426365
    secs_extended = 0
    whip_speed = screen_width * .0003
    whip_up_length = screen_height * 0.14

    def _improve_variables(self):
        self.whip_speed = screen_width * (
            consistency_keeper.calculate_new_speed(.0003))

    def extend_whip(self):
        self.whip_is_extending = True

    def render(self, character_x_coordinate, character_y_coordinate,
               character_height):
        self._improve_variables()
        if self.whip_is_extending and self.length == self.base_height and (
             self.secs_extended <= self.secs_needed):

            self.y_coordinate = character_y_coordinate - character_height
            self.x_coordinate = character_x_coordinate
            self.height = self.whip_up_length
            self.secs_extended += consistency_keeper.current_speed
            self.draw()

        elif self.length >= self.whip_up_length:
            self.whip_is_extending = False
            self.length = self.base_length
            self.height = self.base_height
            self.secs_extended = 0

        elif self.whip_is_extending:
            self.height = self.base_height
            self.x_coordinate = character_x_coordinate
            self.y_coordinate = character_y_coordinate
            self.length += self.whip_speed
            self.draw()
