from abc import ABC, abstractmethod
import pygame

# Up is down. Down is up.
# No spaces between functions in a class
screen_width = 800
screen_height= 500
nameOfGame = "robowars"
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(f'{nameOfGame}')
background = (0, 0, 0)

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
            



class Character:
    character_color = (250, 0, 0)
    x_coordinate = 50
    y_coordinate = 50
    length = screen_width * .05
    height = screen_height * .15
    movement = screen_width * .0005    
    movement_down = 5
    jumped = 0
    move_down = True
    on_platform = True
    can_move_left = True
    can_move_right = True
    can_jump = True
    is_jumping = False
    jump_height = screen_height * .002
    jump_key_held_down = False
    throw_whip = False


    def draw(self):
        pygame.draw.rect(win, (self.character_color), (self.x_coordinate, self.y_coordinate, self.length, self.height))
    def getHeight(self):
        return self.height


    def get_x_coordinate(self):
        return self.x_coordinate


    def get_y_coordinate(self):
        return self.y_coordinate


    def change_x_coordinate(self, x_coordinate):
        self.x_coordinate = x_coordinate


    def change_y_coordinate(self, y_coordinate):
        self.y_coordinate = y_coordinate


    def getLength(self):
        return self.length


    def movements(self):
        controlls = pygame.key.get_pressed()
        if self.jump_key_held_down and self.on_platform:
            self.can_jump = False
            self.character_color = (0, 250, 0)

        if self.on_platform and not self.jump_key_held_down:
            self.can_jump = True
            self.character_color = (250, 0, 0)

        if controlls[pygame.K_RIGHT] and self.can_move_right:
            self.x_coordinate += self.movement

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
        
        if controlls[pygame.K_SPACE]:
            self.throw_whip = True
        
        else:
            self.throw_whip = False


    def jump(self):
        if self.on_platform:
            self.jumped = 0 + self.jump_height
            self.is_jumping = True
        
        if self.jumped < 200 and self.is_jumping:
            self.y_coordinate -= self.jump_height
            self.jumped += self.jump_height
        
        if self.jumped > 190:
            self.is_jumping = False
            self.can_jump = False

    def controls(self):
        self.movements()


    def set_character_y_coordinates(self, x_coordinate, y_coordinate):
        self.y_coordinate = y_coordinate
        self.x_coordinate = x_coordinate


    def reset_character_location(self, platform_y_coordinate):
        self.x_coordinate = 50
        self.y_coordinate = 50


class Platform:
    platform_color = (80, 21, 46)
    x_coordinate = 60
    y_coordinate = screen_height - 100
    length = 400
    width = 100
    

    def get_x_coordinate(self):
        return self.x_coordinate

    def get_y_coordinate(self):
        return self.y_coordinate

    def change_x_coordinate(self, x_coordinate):
        self.x_coordinate = x_coordinate

    def change_y_coordinate(self, y_coordinate):
        self.y_coordinate = y_coordinate

    def draw(self):
        pygame.draw.rect(win, (self.platform_color), (self.x_coordinate, self.y_coordinate, self.length, self.width))


class CollisionsFinder:
    def on_platform(self, platform, character):
        character_y_coordinate = character.get_y_coordinate() + character.getHeight() 
        platform_y_coordinate = platform.get_y_coordinate()
        platform_x_cordinate = platform.get_x_coordinate()
        character_x_coordinate = character.get_x_coordinate()

        within_platform_length = character_x_coordinate >= platform_x_cordinate - character.getLength() and (
            character_x_coordinate <= platform_x_cordinate + platform.length
        )
        
        return (character_y_coordinate >= platform_y_coordinate and within_platform_length)
    



class PhysicsEngine:
    gravity_pull = screen_height * .002
    def set_gravity(self, gravity):
        self.gravity_pull = gravity_pull
    def gravity(self, platform, character):
        collisions = CollisionsFinder()
        on_solid_object = collisions.on_platform(platform, character)

        if not on_solid_object and not character.is_jumping:
            object_y_coordinate = character.get_y_coordinate() + self.gravity_pull
            character.change_y_coordinate(object_y_coordinate)

    def movement_possible(self, platform, character):
        collisions = CollisionsFinder()
        on_solid_object = collisions.on_platform(platform, character)
        if on_solid_object:
            character.on_platform = True
            character.move_down = False
        else:
            character.on_platform = False
            character.move_down = True
        
    def boundaries(self, character, platform):
        if character.get_x_coordinate() <= 0:
            character.can_move_left = False
        else:
            character.can_move_left = True

        if character.get_x_coordinate() >= screen_width - character.getLength():
            character.can_move_right = False
        else:
            character.can_move_right = True

        if character.get_y_coordinate() <= 0:
            character.can_jump = False
        else:
            character.can_jump = True
        
        self.within_screen(character, platform.get_y_coordinate())
    
    def within_screen(self, character: Character, platform_y_coordinate):
        if character.get_y_coordinate() >= screen_height:
            character.reset_character_location(platform_y_coordinate)

    
class InteractionsFinder:
    def player_whip(self, player, whip):
        if player.throw_whip:
            whip_x_coordinate = player.get_x_coordinate() + player.getLength()
            whip_y_coordinate = player.get_y_coordinate() + (player.getHeight() * .5)
            whip.render(whip_x_coordinate, whip_y_coordinate)

            



doggo = Character()
whip = Whip()
run = True
platform1 = Platform()
physics = PhysicsEngine()  
interactions = InteractionsFinder()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    win.fill(background)
    platform1.draw()
    doggo.movements()
    physics.gravity(platform1, doggo)
    physics.boundaries(doggo, platform1)
    physics.movement_possible(platform1, doggo)
    doggo.draw()
    interactions.player_whip(doggo, whip)
    pygame.display.update()

