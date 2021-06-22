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


def generate_platform_x_coordinate(max_jump_time, player_movement,
                                   platform):
    # Little bit of a buffer, so jump isn't too hard
    max_space_apart = max_jump_time * player_movement * .6
    min_space_apart = max_space_apart / 1.3
    platform_end = platform.x_coordinate + platform.length
    platform_end = platform.x_coordinate + platform.length
    max_platform_end = screen_width - (platform.length / 2)

    # Gurrantees that when player is halfway across platform that he can see the entire
    # other platform
    if max_space_apart > max_platform_end - platform.length:
        max_space_apart = max_platform_end - platform.length
    
    if min_space_apart > (max_platform_end - platform.length) * .95:
        min_space_apart = (max_platform_end - platform.length) * .95 

    max_x_coordinate = max_space_apart + platform_end
    min_x_coordinate = min_space_apart + platform_end

    return random.randrange(int(min_x_coordinate), int(max_x_coordinate) + 1)


def generate_platform_y_coordinate(player, last_platform, platform_width):
    max_height = 0
    if last_platform.y_coordinate + player.jump_height >= screen_height * .75:
        max_height = screen_height * .6

    else: 
        max_height = 0 + (((player.max_jump_height + last_platform.y_coordinate) - player.height - platform_width) * .8)

    min_height = screen_height -  last_platform.width
    return random.randrange(int(max_height), int(min_height + 1))

class Generator:
    def generate_platform(platforms, player, gravity):
        new_platform = Platform()
        last_platform = platforms[len(platforms) - 1]
        new_platform.width = generate_platform_width()
        y_coordinate = generate_platform_y_coordinate(player, last_platform, new_platform.width)

        new_platform.length = generate_platform_length()
        new_platform.y_coordinate = y_coordinate
        new_platform.platform_color = (0, 250, 0)
        new_platform.x_coordinate = generate_platform_x_coordinate(player.max_jump_time(last_platform, gravity), player.movement, last_platform)

        platforms.append(new_platform)
        return platforms

    def generate_enemy(platform, enemies):
        new_enemy = SimpleEnemy()
        platform_end = platform.x_coordinate + platform.length

        new_enemy.x_coordinate = (platform.x_coordinate + platform_end) / 2

        new_enemy.y_coordinate = platform.y_coordinate - new_enemy.height

        enemies.append(new_enemy)

        return enemies
