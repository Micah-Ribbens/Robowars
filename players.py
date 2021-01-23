from important_variables import (
    screen_height,
    screen_width,
    win,
    consistency_keeper
)
import pygame


class Player:
    player_color = (250, 0, 0)
    x_coordinate = 50
    y_coordinate = 50
    length = screen_width * .05
    height = screen_height * .15
    movement = screen_width * 0.0004
    movement_down = screen_height * .002
    jumped = 0
    move_down = True
    on_platform = False
    can_move_left = True
    can_move_right = True
    move_right = False
    can_jump = False
    is_jumping = False
    jump_height = screen_height * .002
    jump_key_held_down = False
    throw_whip = False
    space_held_in = False

    def _improve_variables(self):
        self.movement = screen_width * (
            consistency_keeper.calculate_new_speed(0.0004))

        self.movement_down = screen_height * (
            consistency_keeper.calculate_new_speed(.002))

        self.jump_height = screen_height * (
            consistency_keeper.calculate_new_speed(.002))

    def draw(self):
        pygame.draw.rect(win, (self.player_color), (self.x_coordinate,
                         self.y_coordinate, self.length, self.height))

    def get_height(self):
        return self.height

    def get_x_coordinate(self):
        return self.x_coordinate

    def get_y_coordinate(self):
        return self.y_coordinate

    def change_x_coordinate(self, x_coordinate):
        self.x_coordinate = x_coordinate

    def change_y_coordinate(self, y_coordinate):
        self.y_coordinate = y_coordinate

    def get_length(self):
        return self.length

    def movements(self):
        self._improve_variables()
        controlls = pygame.key.get_pressed()
        if self.jump_key_held_down and self.on_platform:
            self.can_jump = False

        if self.on_platform and not self.jump_key_held_down:
            self.can_jump = True

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

        if controlls[pygame.K_SPACE] and not self.space_held_in:
            self.throw_whip = True
            self.space_held_in = True

        else:
            self.throw_whip = False

        if not controlls[pygame.K_SPACE]:
            self.space_held_in = False

    def jump(self):
        if self.on_platform:
            self.jumped = 0 + self.jump_height
            self.is_jumping = True

        if self.jumped <= screen_height * .4 and self.is_jumping:
            self.y_coordinate -= self.jump_height
            self.jumped += self.jump_height

        if self.jumped >= screen_height * .4:
            self.is_jumping = False
            self.can_jump = False

    def controls(self):
        self.movements()

    def set_player_y_coordinates(self, x_coordinate, y_coordinate):
        self.y_coordinate = y_coordinate
        self.x_coordinate = x_coordinate

    def reset_player_location(self, platform_y_coordinate):
        self.x_coordinate = 50
        self.y_coordinate = 50
