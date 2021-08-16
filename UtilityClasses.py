from important_variables import window
import pygame
from abc import abstractmethod
from velocity_calculator import VelocityCalculator
from important_variables import screen_height, screen_length
class GameObject:
    x_coordinate = 0
    y_coordinate = 0
    height = 0
    length = 0
    color = (0, 0, 250)
    is_within_screen = True
    name = ""
    # @property automatically changes this "attribute" when the x_coordinate or length changes
    # Can be treated as an attribute
    @property 
    def right_edge(self):
        return self.x_coordinate + self.length
    @property
    def bottom(self):
        return self.y_coordinate + self.height
    def draw(self):
        # TODO change if both length and height are negative, but that shouldn't happen
        pygame.draw.rect(window, (self.color), (self.x_coordinate,
                        self.y_coordinate, self.length, self.height))
    def __str__(self):
        return f"x {self.x_coordinate} y {self.y_coordinate} height {self.height} length {self.length} right_edge {self.right_edge} bottom {self.bottom}"    
        
# TODO better name for something that encompasses all things that have some 
# sort of movement and can be knocked back (probably just enemies and players)
class GameCharacters(GameObject):
    current_health = 0
    full_health = 0
    def knockback(self, damage=0, **kwargs):
        """One **kwargs should be direction_is_left"""
        UtilityFunctions.validate_kwargs_has_all_fields(["direction_is_left"], kwargs)
        if kwargs.get("direction_is_left"):
            self.x_coordinate -= 200
        else:
            self.x_coordinate += 200
        self.current_health -= damage
    @abstractmethod
    def movement(self):
        pass


class SideScrollableComponents:
    components = []

    def side_scroll_all(amount):
        for component in SideScrollableComponents.components:
            component.x_coordinate -= amount


class UtilityFunctions:
    def validate_kwargs_has_all_fields(kwargs_fields, kwargs):
        for field in kwargs_fields:
            if not kwargs.__contains__(field):
                raise ValueError(f"Field {field} was not provided for kwargs")
    
    def draw_font(message, font, **kwargs):
        background = (0, 0, 0)
        foreground = (255, 255, 255)
        text = font.render(message, True, foreground, background)
        text_rect = text.get_rect()
        if not kwargs.get("is_center_of_screen"):
            UtilityFunctions.validate_kwargs_has_all_fields(["x_coordinate", "y_coordinate"], kwargs)
            text_rect.left = kwargs.get("x_coordinate")
            text_rect.top = kwargs.get("y_coordinate")
        if kwargs.get("is_center_of_screen"):
            text_rect.center = (screen_length / 2,
                                screen_height / 2)
        window.blit(text, text_rect)
    # Meaning what the current health and lost_health are multiplied
    def draw_health_bar(game_character: GameCharacters, x_coordinate, 
                        y_coordinate, width, health_bar_length):
        current_health = game_character.current_health
        health_lost = game_character.full_health - game_character.current_health
        current_health_length = (current_health / game_character.full_health) * health_bar_length
        current_health_color = (0, 255, 0)
            
        pygame.draw.rect(window, current_health_color, 
                         (x_coordinate, y_coordinate, current_health_length, width))
        lost_health_color = (255, 0, 0)
        lost_health_length = (health_lost / game_character.full_health) * health_bar_length
        pygame.draw.rect(window, lost_health_color, (x_coordinate + current_health_length, 
                         y_coordinate, lost_health_length, width))




