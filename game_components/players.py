from base.utility_classes import GameCharacters, Segment, SideScrollableComponents, HistoryKeeper
from game_components.items import Shield, Whip, Sword
from base.engines import *
import pygame
from base.velocity_calculator import VelocityCalculator

class Player(GameCharacters):
    item = None
    running_velocity = VelocityCalculator.give_velocity(screen_length, 600)
    running_deceleration = -1200
    is_decelerating = False
    is_facing_right = False
    can_move_down = True
    on_platform = False
    can_move_left = True
    can_move_right = True
    can_jump = True
    is_jumping = False
    upwards_velocity = 1050
    max_jump_height = VelocityCalculator.give_measurement(screen_height, 40)
    jump_key_held_down = False
    space_held_in = False
    # So player hangs a bit in air when reaches max jump height
    stay_up_in_air = False
    apex_time = 0
    game_is_sidescrolling = False
    shield = None
    used_dodge = False
    apex_max_time = .1
    jump_time = 0
    last_y_unmoving = 0
    last_platform_on = None
    time_affected_by_gravity = 0
    x_before_decelerating = 0
    hit_shield_button_last_cycle = False
    hit_a_attack_button_last_cycle = False

    def __init__(self):
        self.controlls = pygame.key.get_pressed()
        self.item = Whip(self)
        self.shield = Shield(self)
        self.item.damage = 10
        self.shield.damage = 5
        self.current_health = 20
        self.full_health = 20
        self.color = self.light_gray
        self.x_coordinate = 100
        self.y_coordinate = screen_height - 200
        self.invincibility__max_time = .6
        self.length = VelocityCalculator.give_measurement(screen_length, 5)
        self.height = VelocityCalculator.give_measurement(screen_height, 15)
        self.time_affected_by_deceleration = 0

    def draw(self):
        eye_color = (0,0,255)
        mouth_color = GameObject.red

        eye1 = Segment(
            is_percentage=True, 
            color=eye_color, 
            amount_from_top=20, 
            amount_from_left=25, 
            length_amount=20, 
            width_amount=20)

        eye2 = Segment(
            is_percentage=True, 
            color=eye_color, 
            amount_from_top=eye1.amount_from_top, 
            amount_from_left=eye1.right_edge + 10, 
            length_amount=eye1.length_amount, 
            width_amount=eye1.width_amount)

        mouth = Segment(
            is_percentage=True, 
            color=mouth_color, 
            amount_from_top=60, 
            amount_from_left=10, 
            length_amount=80, 
            width_amount=10)

        self.draw_in_segments([eye1, eye2, mouth])
    
    def __str__(self):
        return self.y_coordinate

    # I.E. if the player holds in the up key and landsThe player would jump again, so this function 
    # tells if that is going to happen and if it is it allows the caller of function to prevent it
    def is_continuous_event(self, event, event_name):
        HistoryKeeper.add(event, event_name, False)
        if HistoryKeeper.get_last(event_name) and event:
            return True
        return False


    # For all functions that have movement syntax is "do" = always does it,
    # Otherwise logic inside function to figure out if that movement should be done
    def can_dodge(self):
        if self.used_dodge:
            if self.time_based_activity_is_done("dodge"+self.name, 2, False, self.used_dodge):
                self.used_dodge = False
                return True

        if self.is_flinching:
            return True

    def deceleration_figure_outter(self, key):
        if not self.on_platform:
            return
        last_player = HistoryKeeper.get_last("player")

        if last_player is not None and last_player.controlls[key] and not self.controlls[key]:
            self.is_decelerating = True
            self.x_before_decelerating = self.x_coordinate

    def rightwards_movement(self, right_key_is_held_down):
        self.deceleration_figure_outter(pygame.K_RIGHT)
        if not right_key_is_held_down or not self.can_move_right:
            self.game_is_sidescrolling = False
            return

        self.is_facing_right = True
        location_to_sidescroll = VelocityCalculator.give_measurement(screen_length, 20)
        self.game_is_sidescrolling = self.x_coordinate >= location_to_sidescroll
        if self.x_coordinate >= location_to_sidescroll:
            SideScrollableComponents.side_scroll_all(VelocityCalculator.calc_distance(self.running_velocity))

        else:
            self.x_coordinate += VelocityCalculator.calc_distance(self.running_velocity)

    def decelerate(self):
        self.time_affected_by_deceleration += VelocityCalculator.time
        current_change = PhysicsEngine.distance_change(self.running_velocity, self.running_deceleration, self.time_affected_by_deceleration)
        last_player = HistoryKeeper.get_last("player")
        prev_change = PhysicsEngine.distance_change(self.running_velocity, self.running_deceleration, last_player.time_affected_by_deceleration)
        if prev_change > current_change:
            self.is_decelerating = False
            self.time_affected_by_deceleration = 0
            return

        self.x_coordinate = (current_change + self.x_before_decelerating if self.is_facing_right 
                             else self.x_before_decelerating - current_change)

    def upwards_movement(self, jump_key_held_down):
        if not self.is_jumping and not self.on_platform:
            self.time_affected_by_gravity += VelocityCalculator.time
        else:
            self.time_affected_by_gravity = 0
        if self.on_platform:
            # Makes sure doesn't keep jumping up and down
            self.can_jump = not self.is_continuous_event(jump_key_held_down, "jump")

        if self.on_platform:
            self.last_y_unmoving = self.last_platform_on.y_coordinate
            
        if (self.can_jump and jump_key_held_down) or self.is_jumping:
            self.do_jump()

    def reset_jump(self):
        self.is_jumping = False
        self.jump_time = 0
        self.last_y_unmoving = self.y_coordinate
        self.can_jump = False

    def movement(self):
        self.controlls = pygame.key.get_pressed()
        # If the character gets hit and thus is flinching the character shouldn't be able to move
        if self.is_blocking:
            self.do_block()

        if self.controlls[pygame.K_LEFT] or self.controlls[pygame.K_RIGHT]:
            self.x_before_decelerating = self.x_coordinate
            self.is_decelerating = False

        if self.can_dodge() and self.controlls[pygame.K_DOWN]:
            self.do_invincibility(.2)
            self.used_dodge = True

        if self.is_flinching:
            self.item.stop_item_usage()
            self.flinch()
            self.color = (250, 0, 0)
        else:
            self.color = self.light_gray

        if self.hit_during_item_cycle:
            self.is_invincible = True

        if self.is_invincible:
            self.do_invincibility()
            self.color = self.white
        else:
            self.color = self.light_gray

        if self.is_flinching:
            return

        self.rightwards_movement(self.controlls[pygame.K_RIGHT])
        self.upwards_movement(self.controlls[pygame.K_UP])

        if self.controlls[pygame.K_LEFT] and self.can_move_left:
            self.x_coordinate -= VelocityCalculator.calc_distance(self.running_velocity)
            self.is_facing_right = False
        
        self.deceleration_figure_outter(pygame.K_LEFT)

        # If using whip shield can't be used
        if self.controlls[pygame.K_DOWN] and not self.item.whip_is_extending and not self.hit_shield_button_last_cycle:
            self.shield.use_item()
        self.hit_shield_button_last_cycle = self.controlls[pygame.K_DOWN]

        if self.is_decelerating:
            self.decelerate()
        
        # If using shield can't use item
        if not self.shield.is_being_used and not self.is_continuous_event(self.controlls[pygame.K_w] or self.controlls[pygame.K_s], "slash"):
            moves = {self.controlls[pygame.K_w]: self.item.UPWARDS_ATTACK,
                     self.controlls[pygame.K_s]: self.item.DOWNWARDS_ATTACK,
                     self.controlls[pygame.K_d]: self.item.RIGHT_ATTACK,
                     self.controlls[pygame.K_a]: self.item.LEFT_ATTACK}

            move = self.get_move(moves)
            if move != None and not self.hit_a_attack_button_last_cycle:
                self.item.use_item(self.get_move(moves))
            self.hit_a_attack_button_last_cycle = move != None

        if self.controlls[pygame.K_LEFT] or self.controlls[pygame.K_RIGHT]:
            self.is_decelerating = False

    def get_move(self, moves: dict):
        for key in moves.keys():
            if key:
                return moves[key]

        # If None of the keys were hit
        return moves.get(None)

    def do_jump(self):
        self.is_jumping = True
        self.jump_time += VelocityCalculator.time
        distance_change = PhysicsEngine.distance_change(self.upwards_velocity, PhysicsEngine.gravity_pull, self.jump_time)
        if distance_change < 0:
            self.is_jumping = False
            self.jump_time = 0
            self.last_y_unmoving = self.y_coordinate
            self.can_jump = False
            return

        self.y_coordinate = self.last_platform_on.y_coordinate - distance_change - self.height

    # TODO fix this
    def time_in_air(self, new_platform_y_coordinate, last_platform_y_coordinate, gravity):
        upwards_time = 0
        max_y_coordinate = 0
        # The players bottom is on the platform meaning once jumping the height has to be accounted
        # For since the top of player is the bottom - height
        jumping_change_in_y = self.max_jump_height - self.height
        if last_platform_y_coordinate - jumping_change_in_y <= 0:
            upwards_time = (last_platform_y_coordinate - self.height) / self.upwards_velocity
            max_y_coordinate = self.height

        else:
            max_y_coordinate = last_platform_y_coordinate - self.max_jump_height
            upwards_time = self.max_jump_height / self.upwards_velocity

        downwards_time = (new_platform_y_coordinate - max_y_coordinate) / gravity

        return upwards_time + downwards_time

    def reset(self):
        self.x_coordinate = 50
        self.y_coordinate = 50

