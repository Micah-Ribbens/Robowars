import pygame
from important_variables import (
    win,
    screen_height,
    screen_width,
    consistency_keeper, 
    file
)
from players import Player


class Item:
    color = (0, 250, 0)
    x_coordinate = 0
    y_coordinate = 0
    base_length = 0.0125 * screen_width
    length = 0
    base_height = screen_height * 0.02
    height = base_height

    def draw(self):
        pygame.draw.rect(win, (self.color), (self.x_coordinate,
                         self.y_coordinate, self.length, self.height))


class Whip(Item):
    whip_is_extending = False
    secs_needed_to_extend = 0.12838726547426365
    secs_extended = 0
    whip_speed = screen_width * .0003
    whip_up_length = screen_height * 0.14
    whip_max_length = screen_width * .3
    player_is_facing_right = False
    whip_is_going_right = False

    def _improve_variables(self):
        self.whip_speed = screen_width * (
            consistency_keeper.calculate_new_speed(.0003))

    def extend_whip(self, player_is_facing_right):
        if not self.whip_is_extending:
            self.whip_is_extending = True
            self.player_is_facing_right = player_is_facing_right
            self.whip_is_going_right = player_is_facing_right

    def render(self, player: Player):
        if not self.whip_is_extending:
            return
        self._improve_variables()
        is_right_length = self.length == 0 or self.length == self.base_length
        whip_is_upwards = self.whip_is_extending and is_right_length and (
             self.secs_extended <= self.secs_needed_to_extend)
        player_right_edge = player.x_coordinate + player.width
        whip_y_coordiante = player.y_coordinate + (player.height * .5)
        if whip_is_upwards:
            self.y_coordinate = whip_y_coordiante - player.height
            self.height = self.whip_up_length
            self.length = self.base_length
            self.secs_extended += consistency_keeper.current_speed
            self.draw()

        if whip_is_upwards and self.player_is_facing_right:
            self.x_coordinate = player_right_edge
            return 

        if whip_is_upwards and not self.player_is_facing_right:
            self.x_coordinate = player.x_coordinate - self.length
            return

        if self.length >= 70 or self.length <= -70:
            self.whip_is_extending = False
            self.length = 0
            self.height = 0
            self.secs_extended = 0

        if self.whip_is_extending:
            self.height = self.base_height
            self.y_coordinate = whip_y_coordiante

        if self.whip_is_extending and self.player_is_facing_right:
            self.x_coordinate = player_right_edge
            self.length += self.whip_speed
            self.draw()
        
        if self.whip_is_extending and not self.player_is_facing_right:
            self.x_coordinate = player.x_coordinate
            self.length -= self.whip_speed
            self.draw()