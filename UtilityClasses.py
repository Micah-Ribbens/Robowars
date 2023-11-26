from important_variables import window
import pygame
from abc import abstractmethod
from velocity_calculator import VelocityCalculator
from important_variables import screen_height, background, screen_length, window
import random
from utility_functions import *
import pickle
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
    attributes = []

    def find_all_attributes(object):
        attributes = []
        for key in object.__dict__.keys():
            if not key.__contains__("__") and not callable(key):
                attributes.append(key)
        return attributes

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
    @property
    def y_midpoint(self):
        return self.y_coordinate + self.height * .5
    @property
    def x_midpoint(self):
        return self.x_coordinate + self.length * .5

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

    def time_based_activity_is_done(self, name, time_needed, restart_condition, start_condition=True):
        if restart_condition:
            HistoryKeeper.add(0, name, False)
            return False
        # if not start_condition:
        #     return True

        if HistoryKeeper.get_last(name) is None:
            HistoryKeeper.add(VelocityCalculator.time, name, False)

        current_time = HistoryKeeper.get_last(name)
        if current_time >= time_needed:
            HistoryKeeper.add(0, name, False)
            return True

        else:
            HistoryKeeper.add(current_time + VelocityCalculator.time, name, False)

        return False

class GameCharacters(GameObject):
    current_health = 0
    hit_during_item_cycle = False
    full_health = 0
    is_flinching = False
    time_spent_flinching = 0
    is_invincible = False
    invincibility__max_time = 0
    total_invincibility_time = 0
    is_blocking = False

    def __init__(self, x, y, length, height, current_health, full_health, is_invincible, is_flinching, is_blocking):
        self.x_cooridnate, self.y_coordinate, self.length = x, y, length
        self.height, self.current_health, self.full_health = height, current_health, full_health
        self.is_invincible, self.is_flinching, self.is_blocking = is_invincible, is_flinching, is_blocking

    def knockback(self, amount, damage=0, **kwargs):
        """One **kwargs should be direction_is_left"""
        UtilityFunctions.validate_kwargs_has_all_fields(["direction_is_left"], kwargs)
        if kwargs.get("direction_is_left"):
            self.x_coordinate -= amount
        else:
            self.x_coordinate += amount
        self.current_health -= damage

    @abstractmethod
    def movement(self):
        pass

    def do_block(self):
        self.is_blocking = not self.time_based_activity_is_done("blocking"+self.name, .2, False)

    def flinch(self):
        self.is_flinching = not self.time_based_activity_is_done("flinching"+self.name, 
                                                                 .5, False)

    def do_invincibility(self, time=None):
        time = self.invincibility__max_time if time == None else time
        self.is_invincible = not self.time_based_activity_is_done("invincibility"+self.name, 
                                                                  time, False)

class SideScrollableComponents:
    components = []

    def side_scroll_all(amount):
        for component in SideScrollableComponents.components:
            component.x_coordinate -= amount

class UtilityFunctions:
    def random_chance(numerator, denominator):
        return random.randint(numerator, denominator) == numerator

    def validate_kwargs_has_all_fields(kwargs_fields, kwargs):
        for field in kwargs_fields:
            if not kwargs.__contains__(field):
                raise ValueError(f"Field {field} was not provided for kwargs")
    
    def draw_font(message, font, **kwargs):
        """x_coordinate and y_coordinate or 
        is_center_of_screen"""
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
    def draw_health_bar(game_character, x_coordinate, 
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

# Delete unneeded times
class HistoryKeeper:
    memento_list = {}
    def reset():
        HistoryKeeper.memento_list = {}
    def copy(object):
        return pickle.loads(pickle.dumps(object, -1))
    def add(object, name, is_game_object):
        if is_game_object:
            object = deepcopy(object)

        HistoryKeeper._add(object, name)
        
    def _add(object, name):
        try: 
            HistoryKeeper.memento_list[name].append(object)
        except KeyError:
            HistoryKeeper.memento_list[name] = [object]


    def get(name):
        if HistoryKeeper.memento_list.get(name) is None:
            return []
        return HistoryKeeper.memento_list.get(name)

    def get_last(name):
        mementos = HistoryKeeper.get(name)
        if len(mementos) == 0:
            return None
        if len(mementos) == 1:
            return mementos[0]
        return mementos[len(mementos) - 2]
