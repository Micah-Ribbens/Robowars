from abc import ABC, abstractmethod
import pygame
from items import (
    Whip,
)
from engines import (
    PhysicsEngine,
    CollisionsFinder,
    InteractionsFinder
)
from platforms import (
    Platform
)
from players import (
    Player
)
from important_variables import (
    screen_width,
    screen_height,
    win
)
from enemies import (
    Simple_Enemy
)
# Up is down. Down is up.
# No spaces between functions in a class

pygame.init()

nameOfGame = "robowars"
pygame.display.set_caption(f'{nameOfGame}')
background = (0, 0, 0)     
# Think of better name
class GameStatsShower:
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

        pygame.draw.rect(win, (self.color), (self.x_coordinate_1, self.y_coordinate, self.width, self.height))
        pygame.draw.rect(win, (self.color), (self.x_coordinate_2, self.y_coordinate, self.width, self.height))

    def pause_clicked(self):
        width = (self.x_coordinate_2 - self.x_coordinate_1) + self.width
        area = pygame.Rect(self.x_coordinate_1, self.y_coordinate, width, self.height)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]

        if area.collidepoint(mouse_x, mouse_y) and clicked:
            return True
        
        return False
    
    def show_pause_screen(self):
        message = f"Paused"
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
        text_y_coordinate =  0 + screen_height * .04
        text_rect.left = (text_x_coordinate)
        text_rect.top = (text_y_coordinate)
        win.blit(text, text_rect)

        color = (0, 250, 0)
        health_remaining_length = (health_remaining / full_health) * 100 * (screen_height * .002)
        lost_health_length = (lost_health /full_health) * 100 * (screen_height * .002)
        pygame.draw.rect(win, (color), (text_x_coordinate, text_y_coordinate + screen_height * .04, health_remaining_length, screen_height * .04))
        color = (250, 0, 0)
        pygame.draw.rect(win, (color), (text_x_coordinate + health_remaining_length, text_y_coordinate + screen_height * .04, lost_health_length, screen_height * .04))
    
    def show_enemy_health(self, x_coordinate, y_coordinate, full_health, health_remaining):
        if health_remaining == 0:
            return 
        lost_health = full_health - health_remaining
        color = (0, 250, 0)
        health_remaining_length = (health_remaining / full_health) * 100 * (screen_height * .001)
        lost_health_length = (lost_health /full_health) * 100 * (screen_height * .001)
        pygame.draw.rect(win, (color), (x_coordinate, y_coordinate, health_remaining_length, screen_height * .02))
        color = (250, 0, 0)
        pygame.draw.rect(win, (color), (x_coordinate + health_remaining_length, y_coordinate, lost_health_length, screen_height * .02))



    
def run_game():
    game_stats_shower = GameStatsShower()
    run = True
    enemy_1 = Simple_Enemy()
    doggo = Player()
    whip = Whip()
    platform1 = Platform()
    physics = PhysicsEngine()  
    interactions = InteractionsFinder()
    collisions = CollisionsFinder()
    timesIterated = 0
    click_is_held_done = False

    game_is_paused = False
    while run:
        timesIterated += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        win.fill(background)
        game_stats_shower.render_pause_button(game_is_paused)
        game_stats_shower.show_character_health(doggo.full_health, doggo.current_health)
        game_stats_shower.show_enemy_health(50, 100, 100, 10)
        pause_clicked = game_stats_shower.pause_clicked()
        can_pause = not click_is_held_done and pause_clicked

        if can_pause and game_is_paused:
            game_is_paused = False

        elif can_pause and not game_is_paused:
            game_is_paused = True

        if pause_clicked:
            click_is_held_done = True

        else:
            click_is_held_done = False

        if not game_is_paused:

            if physics.character_died:
                run = False
            if doggo.is_dead():
                run = False
            doggo.movements()
            physics.gravity(platform1, doggo)
            physics.boundaries(doggo, platform1)
            physics.movement_possible(platform1, doggo)
            physics.platform_side_scrolling(doggo, platform1)
            interactions.player_whip(doggo, whip)
            interactions.player_enemy_interactions(doggo, enemy_1)
            interactions.enemy_whip_interactions(enemy_1, whip)
            physics.enemy_side_scrolling(doggo, enemy_1)
            doggo.draw()
            enemy_1.movement(collisions.on_platform(platform1, enemy_1, 0))

        #The draw and update are here so the game doesn't make them disappear, so put draw functions here or both!
        platform1.draw()
        doggo.draw()
        enemy_1.draw()
        pygame.display.update()
        
    
    run_game()

