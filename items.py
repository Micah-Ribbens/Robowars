import pygame
from important_variables import (
    win, 
    screen_height,
    screen_width
)
class Item:
    color = (0, 250, 0) 
    x_coordinate = 0
    y_coordinate = 0
    length = 10
    height = 10

    def draw(self):
        pygame.draw.rect(win, (self.color), (self.x_coordinate, self.y_coordinate, self.length, self.height))

class Whip(Item):
    whip_is_extending = False
    secs_extended = 0
    
    def extend_whip(self):
        self.whip_is_extending = True
    
    def render(self, character_x_coordinate, character_y_coordinate):
        if self.whip_is_extending and self.length == 10 and self.secs_extended <= 100:
            self.y_coordinate = character_y_coordinate - 100
            self.x_coordinate = character_x_coordinate
            self.height = 70
            self.secs_extended += 1
            self.draw()


        elif self.length >= 70:
            self.whip_is_extending = False
            self.length = 10
            self.height = 10
            self.secs_extended = 0

        elif self.whip_is_extending:
            self.height = 10
            self.x_coordinate = character_x_coordinate
            self.y_coordinate = character_y_coordinate
            self.length += screen_width * .0003
            self.draw()
