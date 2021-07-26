import cProfile
from important_variables import (
    screen_width,
    screen_height,
    win
)
from velocity_calculator import VelocityCalculator
import pygame
pygame.init()


class HUD:
    y_coordinate = VelocityCalculator.give_measurement(screen_height, 1)
    x_coordinate_1 = screen_width - VelocityCalculator.give_measurement(screen_width, 4)
    x_coordinate_2 = x_coordinate_1 + VelocityCalculator.give_measurement(screen_width, 2)
    width = VelocityCalculator.give_measurement(screen_width, .7)
    height = VelocityCalculator.give_measurement(screen_height, 5)
    color = (250, 250, 250)
    font = pygame.font.Font('freesansbold.ttf', 15)
    pause_font = pygame.font.Font('freesansbold.ttf', 53)

    def render_pause_button(is_paused):
        if is_paused:
            HUD.show_pause_screen()

        pygame.draw.rect(win, (HUD.color), (HUD.x_coordinate_1,
                         HUD.y_coordinate, HUD.width, HUD.height))
        pygame.draw.rect(win, (HUD.color), (HUD.x_coordinate_2,
                         HUD.y_coordinate, HUD.width, HUD.height))

    def pause_clicked():
        width = (HUD.x_coordinate_2 - HUD.x_coordinate_1) + HUD.width
        area = pygame.Rect(HUD.x_coordinate_1, HUD.y_coordinate, width,
                           HUD.height)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]

        if area.collidepoint(mouse_x, mouse_y) and clicked:
            # print("CLICKEEEEEEEED")
            return True

        return False

    def show_pause_screen():
        message = "Paused"
        black = (0, 0, 0)
        white = (255, 255, 255)
        text = HUD.pause_font.render(message, True, white, black)
        text_rect = text.get_rect()
        text_rect.center = (screen_width / 2,
                            screen_height / 2)

        win.blit(text, text_rect)

    def show_character_health(full_health, health_remaining):
        if health_remaining == 0:
            return
        lost_health = full_health - health_remaining

        message = f"Health {health_remaining}/{full_health}"
        black = (0, 0, 0)
        white = (255, 255, 255)
        text = HUD.font.render(message, True, white, black)
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

    def show_enemy_health(enemy):
        if enemy.current_health == 0:
            return

        lost_health = enemy.full_health - enemy.current_health
        x_coordinate = enemy.x_coordinate
        y_coordinate = enemy.y_coordinate
        color = (0, 250, 0)
        ratio = enemy.width / enemy.full_health
        health_remaining_length = ratio * enemy.current_health
        lost_health_length = ratio * lost_health
        width = screen_height * .01
        pygame.draw.rect(win, (color), (x_coordinate, y_coordinate - width,
                         health_remaining_length, width))

        color = (250, 0, 0)
        pygame.draw.rect(win, (color), (x_coordinate + health_remaining_length,
                         y_coordinate - width, lost_health_length, width))
    
    def show_score(distance_traveled):
        message = f"Distance: {distance_traveled}"

        black = (0, 0, 0)
        white = (255, 255, 255)
        text = HUD.font.render(message, True, white, black)
        text_rect = text.get_rect()
        text_x_coordinate = 0 + screen_width * .008
        text_y_coordinate = 0 + screen_height * .15
        text_rect.left = (text_x_coordinate)
        text_rect.top = (text_y_coordinate)
        win.blit(text, text_rect)

     
