from important_variables import win
import pygame
from abc import abstractmethod
from velocity_calculator import VelocityCalculator
class GameObject:
    x_coordinate = 0
    y_coordinate = 0
    height = 0
    length = 0
    color = (0, 0, 250)
    is_within_screen = True
    # @property automatically changes this "attribute" when the x_coordinate or length changes; which if defined as an attribute would not happen
    @property 
    def right_edge(self):
        return self.x_coordinate + self.length
    @property
    def bottom(self):
        return self.y_coordinate + self.height
    def draw(self):
        # TODO change if both length and height are negative, but that shouldn't happen
        pygame.draw.rect(win, (self.color), (self.x_coordinate,
                        self.y_coordinate, self.length, self.height))        
        
# TODO better name for something that encompasses all things that have some sort of movement and can be knocked back (probably just enemies and players)
# TODO Use memento pattern!
class GameCharacters(GameObject):
    current_health = 0
    full_health = 0
    def knockback(self, damage=0, **kwargs):
        """One **kwargs should be direction_is_left"""
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


