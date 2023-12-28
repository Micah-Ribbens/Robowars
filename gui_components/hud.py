from base.utility_classes import UtilityFunctions
import cProfile
from base.important_variables import (
    screen_length,
    screen_height,
    window
)
from base.velocity_calculator import VelocityCalculator
import pygame
pygame.init()

class HUD:
    y_coordinate = VelocityCalculator.give_measurement(screen_height, 1)
    x_coordinate_1 = screen_length - VelocityCalculator.give_measurement(screen_length, 4)
    x_coordinate_2 = x_coordinate_1 + VelocityCalculator.give_measurement(screen_length, 2)
    length = VelocityCalculator.give_measurement(screen_length, .7)
    height = VelocityCalculator.give_measurement(screen_height, 5)
    color = (250, 250, 250)

    pause_font = pygame.font.Font('freesansbold.ttf', 53)
    normal_font = pygame.font.Font('freesansbold.ttf', 15)

    def render_pause_button(is_paused):
        if is_paused:
            HUD.show_pause_screen()

        pygame.draw.rect(window, (HUD.color), (HUD.x_coordinate_1,
                         HUD.y_coordinate, HUD.length, HUD.height))
        pygame.draw.rect(window, (HUD.color), (HUD.x_coordinate_2,
                         HUD.y_coordinate, HUD.length, HUD.height))

    def pause_clicked():
        length = (HUD.x_coordinate_2 - HUD.x_coordinate_1) + HUD.length
        area = pygame.Rect(HUD.x_coordinate_1, HUD.y_coordinate, length,
                           HUD.height)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]

        if area.collidepoint(mouse_x, mouse_y) and clicked:
            return True

        return False

    def show_pause_screen():
        message = "Paused"
        UtilityFunctions.draw_font(message, HUD.pause_font, is_center_of_screen=True)

    def show_character_health(player):
        if player.current_health == 0:
            return
        message = f"Health {player.current_health}/{player.full_health}"
        text_x_coordinate = VelocityCalculator.give_measurement(screen_length, 1)
        text_y_coordinate = VelocityCalculator.give_measurement(screen_height, 4)

        UtilityFunctions.draw_font(message, HUD.normal_font, x_coordinate=text_x_coordinate,
                                   y_coordinate=text_y_coordinate)

        health_bar_length = VelocityCalculator.give_measurement(screen_length, 13)
        distance_from_text = VelocityCalculator.give_measurement(screen_height, 4)
        width = VelocityCalculator.give_measurement(screen_height, 4)

        UtilityFunctions.draw_health_bar(player, text_x_coordinate,     
                                         text_y_coordinate + distance_from_text, 
                                         width, health_bar_length)
    def show_enemy_health(enemy):
        if enemy.current_health == 0:
            return
        width = VelocityCalculator.give_measurement(screen_height, 1)
        UtilityFunctions.draw_health_bar(enemy, enemy.x_coordinate, 
                                         enemy.y_coordinate, width, enemy.length)
    def show_score(distance_traveled):
        x_coordinate = VelocityCalculator.give_measurement(screen_length, 1)
        y_coordinate = VelocityCalculator.give_measurement(screen_height, 15)
        UtilityFunctions.draw_font(f"distance: {distance_traveled}", HUD.normal_font,
                                   x_coordinate=x_coordinate, y_coordinate=y_coordinate)
