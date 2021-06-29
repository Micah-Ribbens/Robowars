from typing import NewType
from important_variables import (
    screen_width,
    screen_height,
    consistency_keeper
)
from platforms import Platform
from enemies import SimpleEnemy
import random
from players import Player
import cProfile


def platform_copy(platform):
    copy = Platform()
    copy.y_coordinate = platform.y_coordinate
    return copy


def generate_platform_length():
    return random.randrange(int(screen_width * .3), int(screen_width * .4))


def generate_platform_width():
    return random.randrange(int(screen_height * .1), int(screen_height * .2))

def platform_on_screen(players_location, space_apart, platform_length):
    # Sees if whole platform on screen so it is screen_width minus where the player always is on the screen
    # Which is 20% of screen width - platform_length to see if the end of platform on screen
    # Has to acount for the gap between the platforms also
    return screen_width - players_location - space_apart - platform_length >= 0
def generate_platform_x_coordinate(max_jump_time, player_movement,
                                   last_platform, new_platform):
    # Little bit of a buffer, so jump isn't too hard
    last_platform_end = last_platform.x_coordinate + last_platform.length
    # print("MAX JUMP TIME: ", max_jump_time)
    max_space_apart = max_jump_time * player_movement * .5
    players_location = screen_width * .2
    if not platform_on_screen(players_location, max_space_apart, new_platform.length):
        max_space_apart = screen_width - players_location - new_platform.length
        # print("I WAS CALLED TROUBLE")
    min_space_apart = max_space_apart / 1.3
    if not platform_on_screen(players_location, min_space_apart, new_platform.length):
        min_space_apart = (screen_width - players_location - new_platform.length) * .9

    max_x_coordinate = max_space_apart + last_platform_end
    min_x_coordinate = min_space_apart + last_platform_end + .1
    # print(min_x_coordinate)
    # print(max_x_coordinate)
    return random.randrange(int(min_x_coordinate), int(max_x_coordinate))
    # return random.randrange(int(min_x_coordinate), int(max_x_coordinate))
# As in if the platform goes down 40% relative to the last platform that would be too big
# Caller of function desides what is too big based on too_big_of_change
def platform_change_too_big(last_platform_y_coordinate, current_platform_y_coordinate, too_big_of_change):
    return abs(last_platform_y_coordinate - current_platform_y_coordinate) > too_big_of_change
def generate_platform_y_coordinate(player, last_platform, current_platform):
    # print("I WAS CALLED")
    # So platform never higher than the players jump height and draws from top to bottom meaning 
    # Max height will be the smaller number
    max_y_coordiante = player.max_jump_height + .01
    if max_y_coordiante > last_platform.y_coordinate + (player.max_jump_height * .6):
        max_y_coordiante = last_platform.y_coordinate + player.max_jump_height
    # min_y_coordinate = screen_height + (current_platform.width * 1.3)
    # if platform_change_too_big(last_platform.y_coordinate, min_y_coordinate, screen_height * .4):
    max_y_coordiante_change = screen_height * .4
    min_y_coordinate = last_platform.y_coordinate + max_y_coordiante
    if min_y_coordinate > screen_height:
        # Makes the platform be a little above the bottom of screen
        min_y_coordinate = screen_height - (current_platform.width)
        # print(min_y_coordinate)
    return random.randrange(int(max_y_coordiante), int(min_y_coordinate))
    # if platform_change_too_big(last_platform, max_y_coordiante):

        
    # max_height = 0
    # if last_platform.y_coordinate + player.max_jump_height >= screen_height * .75:
    #     max_height = screen_height * .75

    # else: 
    #     max_height = (player.max_jump_height * .8) + last_platform.y_coordinate
    
    # # print(max_height)
    # # So player doesn't hit top of screen
    # min_height = last_platform.y_coordinate - (player.max_jump_height * .6)
    # if min_height <= player.max_jump_height:
    #     min_height = player.max_jump_height - .01
    # return random.randrange(int(max_height), int(min_height + 1))
    # print("max jump : ", player.max_jump_height)
    # print("last platform y: ", last_platform.y_coordinate)
    # print("new platform y: ", max_height)
    # return min_height

class Generator:
    def generate_platform(platforms, player, gravity):
        new_platform = Platform()
        last_platform = platforms[len(platforms) - 1]
        new_platform.width = generate_platform_width()
        y_coordinate = generate_platform_y_coordinate(player, last_platform, new_platform)

        new_platform.length = generate_platform_length()
        new_platform.y_coordinate = y_coordinate
        new_platform.platform_color = (0, 250, 0)
        new_platform.x_coordinate = generate_platform_x_coordinate(player.max_jump_time(new_platform.y_coordinate, last_platform.y_coordinate, gravity), player.movement, last_platform, new_platform)

        platforms.append(new_platform)
        return platforms

    def generate_enemy(platform, enemies):
        if random.randint(1, 2) == 1:
            enemies.append(None)
            return enemies
        new_enemy = SimpleEnemy()
        platform_end = platform.x_coordinate + platform.length

        new_enemy.x_coordinate = (platform.x_coordinate + platform_end) / 2

        new_enemy.y_coordinate = platform.y_coordinate - new_enemy.height

        enemies.append(new_enemy)
        print(platform.y_coordinate)

        return enemies
