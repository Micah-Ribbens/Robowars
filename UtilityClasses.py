from important_variables import window
import pygame
from abc import abstractmethod
from velocity_calculator import VelocityCalculator
from important_variables import screen_height, screen_length, background
class Segment:
    is_percentage = False
    color = (0,0,0)
    amount_from_top = 0
    amount_from_left = 0
    length_amount = 0
    width_amount = 0
    def __init__(self, **kwargs):
        """is_percentage, color, amount_from_top, amount_from_left, length_amount, width_amount"""
        UtilityFunctions.validate_kwargs_has_all_fields(kwargs, ["is_percentage", "color", "amount_from_top", 
                                                                 "amount_from_left", "length_amount", "width_amount"])

        self.is_percentage, self.color = kwargs.get("is_percentage"), kwargs.get("color"), 
        self.amount_from_top, self.amount_from_left = kwargs.get("amount_from_top"), kwargs.get("amount_from_left")
        self.length_amount, self.width_amount = kwargs.get("length_amount"), kwargs.get("width_amount")
    @property
    def right_edge(self):
        return self.amount_from_left + self.length_amount
    @property 
    def bottom(self):
        return self.amount_from_top + self.width_amount

class GameObject:
    white = (255, 255, 255)
    light_gray = (190, 190, 190)
    gray = (127, 127, 127)
    dark_gray = (63, 63, 63)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    magenta = (255, 0, 255)
    cyan = (0, 255, 255)
    orange = (255, 100, 0)
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
        pygame.draw.rect(window, (self.color), (self.x_coordinate,
                        self.y_coordinate, self.length, self.height))
    def __str__(self):
        return f"x {self.x_coordinate} y {self.y_coordinate} height {self.height} length {self.length} right_edge {self.right_edge} bottom {self.bottom}"    
    # Equal signs used so the __init__ function is optional when creating an instance of the class
    def __init__(self, x_coordinate=0, y_coordinate=0, height=0, length=0, color=(0,0,0)):
        self.x_coordinate, self.y_coordinate = x_coordinate, y_coordinate
        self.height, self.length, self.color = height, length, color

    def draw_in_segments(self, segments):
        # Draws the base object and segments will be added to that base object in the for loop
        GameObject.draw(self)
        for segment in segments:
            if segment.is_percentage:
                x_coordinate = UtilityFunctions.percentage_to_number(segment.amount_from_left, self.length) + self.x_coordinate
                y_coordinate = UtilityFunctions.percentage_to_number(segment.amount_from_top, self.height) + self.y_coordinate
                height = UtilityFunctions.percentage_to_number(segment.width_amount, self.height)
                length = UtilityFunctions.percentage_to_number(segment.length_amount, self.length)
                GameObject.draw(GameObject(x_coordinate, y_coordinate, height, length, segment.color))
            else:
                x_coordinate = segment.amount_from_left + self.x_coordinate
                y_coordinate = segment.amount_from_top + self.y_coordinate
                height = segment.width_amount
                length = segment.length_amount
                GameObject.draw(GameObject(x_coordinate, y_coordinate, height, length, segment.color))


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
        current_health_color = (0, 255, 0)
        health_lost = game_character.full_health - game_character.current_health

        lost_health_segment = Segment(
            is_percentage=True,
            color=(255, 0, 0),
            amount_from_top=0,
            # Have to times by 100 to turn it from a fraction to a percentage
            amount_from_left=game_character.current_health / game_character.full_health * 100,
            length_amount=health_lost/game_character.full_health * 100,
            width_amount=100
        )

        GameObject.draw_in_segments(GameObject(x_coordinate, y_coordinate, width, health_bar_length, current_health_color), [lost_health_segment])

    def percentage_to_number(perecentage, percentage_of_number):
        return perecentage / 100 * percentage_of_number




