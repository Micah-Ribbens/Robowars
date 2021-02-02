from important_variables import (
    screen_width,
    screen_height,
    win
)
import pygame
pygame.init()


class HUD:
    y_coordinate = 0 + (screen_height * .01)
    x_coordinate_1 = screen_width - screen_width * .04
    x_coordinate_2 = x_coordinate_1 + screen_width * .02
    width = screen_width * .007
    height = screen_height * .05
    color = (250, 250, 250)
    font = pygame.font.Font('freesansbold.ttf', 52)

    def render_pause_button(self, is_paused):
        if is_paused:
            self.show_pause_screen()

        else:
            pass

        pygame.draw.rect(win, (self.color), (self.x_coordinate_1,
                         self.y_coordinate, self.width, self.height))
        pygame.draw.rect(win, (self.color), (self.x_coordinate_2,
                         self.y_coordinate, self.width, self.height))

    def pause_clicked(self):
        width = (self.x_coordinate_2 - self.x_coordinate_1) + self.width
        area = pygame.Rect(self.x_coordinate_1, self.y_coordinate, width,
                           self.height)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]

        if area.collidepoint(mouse_x, mouse_y) and clicked:
            return True

        return False

    def show_pause_screen(self):
        message = "Paused"
        black = (0, 0, 0)
        white = (255, 255, 255)
        text = self.font.render(message, True, white, black)
        text_rect = text.get_rect()
        text_rect.center = (screen_width / 2,
                            screen_height / 2)

        win.blit(text, text_rect)

    def show_character_health(self, full_health, health_remaining):
        if health_remaining == 0:
            return
        lost_health = full_health - health_remaining

        font = pygame.font.Font('freesansbold.ttf', 15)
        message = f"Health {health_remaining}/{full_health}"
        black = (0, 0, 0)
        white = (255, 255, 255)
        text = font.render(message, True, white, black)
        text_rect = text.get_rect()
        text_x_coordinate = 0 + screen_width * .01
        text_y_coordinate = 0 + screen_height * .04
        text_rect.left = (text_x_coordinate)
        text_rect.top = (text_y_coordinate)
        win.blit(text, text_rect)

        color = (0, 250, 0)
        health_remaining_length = ((health_remaining / full_health) * 100 *
                                   (screen_height * .002))
        lost_health_length = ((lost_health / full_health) * 100 *
                              (screen_height * .002))
        pygame.draw.rect(win, (color), (text_x_coordinate,
                         text_y_coordinate + screen_height * .04,
                         health_remaining_length, screen_height * .04))
        color = (250, 0, 0)
        pygame.draw.rect(win, (color),
                         (text_x_coordinate + health_remaining_length,
                         text_y_coordinate + screen_height * .04,
                         lost_health_length, screen_height * .04))

    def show_enemy_health(self, enemy, full_health, health_remaining):
        if health_remaining == 0:
            return

        lost_health = full_health - health_remaining
        x_coordinate = enemy.x_coordinate
        y_coordinate = enemy.y_coordinate
        color = (0, 250, 0)
        ratio = enemy.width / full_health
        health_remaining_length = ratio * health_remaining
        lost_health_length = ratio * lost_health
        width = screen_height * .01
        pygame.draw.rect(win, (color), (x_coordinate, y_coordinate - width,
                         health_remaining_length, width))
        color = (250, 0, 0)
        pygame.draw.rect(win, (color), (x_coordinate + health_remaining_length,
                         y_coordinate - width, lost_health_length, width))
