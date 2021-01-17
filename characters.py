from important_variables import (
    screen_height,
    screen_width,
    win
)
import pygame
class Character:
    character_color = (250, 0, 0)
    x_coordinate = 50
    y_coordinate = 50
    length = screen_width * .05
    height = screen_height * .15
    movement = screen_width * .0005    
    movement_down = 5
    jumped = 0
    move_down = True
    on_platform = True
    can_move_left = True
    can_move_right = True
    move_right = False
    can_jump = True
    is_jumping = False
    jump_height = screen_height * .002
    jump_key_held_down = False
    throw_whip = False


    def draw(self):
        pygame.draw.rect(win, (self.character_color), (self.x_coordinate, self.y_coordinate, self.length, self.height))
    def getHeight(self):
        return self.height


    def get_x_coordinate(self):
        return self.x_coordinate


    def get_y_coordinate(self):
        return self.y_coordinate


    def change_x_coordinate(self, x_coordinate):
        self.x_coordinate = x_coordinate


    def change_y_coordinate(self, y_coordinate):
        self.y_coordinate = y_coordinate


    def getLength(self):
        return self.length


    def movements(self):
        controlls = pygame.key.get_pressed()
        if self.jump_key_held_down and self.on_platform:
            self.can_jump = False
            self.character_color = (0, 250, 0)

        if self.on_platform and not self.jump_key_held_down:
            self.can_jump = True
            self.character_color = (250, 0, 0)

        move_right_possible = controlls[pygame.K_RIGHT] and self.can_move_right
        if move_right_possible and self.x_coordinate >= screen_width * .35:
            self.move_right = True
        
        elif move_right_possible:
            self.x_coordinate += self.movement
        
        else:
            self.move_right = False

        if controlls[pygame.K_LEFT] and self.can_move_left:
            self.x_coordinate -= self.movement

        if controlls[pygame.K_UP]:
            self.jump_key_held_down = True
           
        else:
            self.is_jumping = False
            self.jump_key_held_down = False

        if self.jump_key_held_down and self.can_jump:
            self.jump()
        
        
        if controlls[pygame.K_DOWN] and self.move_down:
            self.y_coordinate += self.movement_down
        
        if controlls[pygame.K_SPACE]:
            self.throw_whip = True
        
        else:
            self.throw_whip = False


    def jump(self):
        if self.on_platform:
            self.jumped = 0 + self.jump_height
            self.is_jumping = True
        
        if self.jumped < 200 and self.is_jumping:
            self.y_coordinate -= self.jump_height
            self.jumped += self.jump_height
        
        if self.jumped > 190:
            self.is_jumping = False
            self.can_jump = False

    def controls(self):
        self.movements()


    def set_character_y_coordinates(self, x_coordinate, y_coordinate):
        self.y_coordinate = y_coordinate
        self.x_coordinate = x_coordinate


    def reset_character_location(self, platform_y_coordinate):
        self.x_coordinate = 50
        self.y_coordinate = 50
