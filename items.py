
class Item:
    color = (0, 250, 0) 
    x_coordinate = 0
    y_coordinate = 0
    length = 50
    height = 10

    def draw(self):
        pygame.draw.rect(win, (self.color), (self.x_coordinate, self.y_coordinate, self.length, self.height))

class Whip(Item):
    whip_is_extending = False
    # def __init__(self):
    #     super.__init__()
    
    def extend_whip(self):
        whip_is_extending = True
    
    def render(self, character_x_coordinate, character_y_coordinate):
        # if self.length >= 70:
        #     self.whip_is_extending = False

        # if self.whip_is_extending:
        self.x_coordinate = character_x_coordinate
        self.y_coordinate = character_y_coordinate
        self.length = 100
        self.draw()