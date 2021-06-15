from important_variables import (
    screen_width,
    screen_height,
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
    return random.randint(screen_width * .1, screen_width * .04)


def generate_platform_width():
    return random.randint(screen_height * .05, screen_height * .1)


def generate_platform_x_coordinate(jump_seconds, player_movement,
                                   platform):

    max_space_apart = jump_seconds * player_movement
    min_space_apart = max_space_apart / 2
    platform_end = platform.x_coordinate + platform.length

    min_x_coordinate = (min_space_apart + platform_end // 1) * 1000
    max_x_coordinate = (max_space_apart + platform_end // 1) * 1000

    return random.randrange(min_x_coordinate,
                            max_x_coordinate) / 1000


def generate_platform_y_coordinate(player, platform):
    max_height = screen_height - platform.height
    min_height = player.height * 1.5
    return random.randrange(min_height, max_height)


def jump_seconds(player, gravity):
    change_in_y = 0
    time_jumping = 0
    is_falling = False
    while True:
        is_within_screen = player.y_coordinate <= screen_height
        is_bigger_than_max_jump = change_in_y >= player.max_jump_height
        can_jump = (is_within_screen and not is_bigger_than_max_jump
                    and not is_falling)

        if can_jump:
            change_in_y += player.jump_height
            time_jumping += 1

        if not can_jump:
            is_falling = True
            time_jumping += 1
            change_in_y -= gravity

        if change_in_y <= 0 and is_falling:
            return time_jumping


def needed_y_coordinate(x_coordinate, player, last_platform, gravity):
    movement = player.movement
    is_falling = False
    change_in_y = 0
    distance_traveled = 0

    platform_end = last_platform.x_coordinate + last_platform.length
    distance_needed = x_coordinate - platform_end

    while True:
        is_within_screen = player.y_coordinate <= screen_height
        is_bigger_than_max_jump = change_in_y >= player.max_jump_height
        can_jump = (is_within_screen and not is_bigger_than_max_jump
                    and not is_falling)

        if can_jump:
            change_in_y += player.jump_height
            distance_traveled += movement

        if not can_jump:
            is_falling = True
            change_in_y -= gravity
            distance_traveled += movement

        if distance_traveled >= distance_needed and is_falling:
            # So the player does not have to have a perfect jump to get to the platform
            min_player_buffer = player.movement * 200
            max_player_buffer = player.movement * 400
            
            player_buffer = random.randint(min_player_buffer, max_player_buffer)
            return last_platform.y_coordinate - change_in_y + player_buffer


class Generator:
    def generate_platform(platforms, player, gravity):
        last_platform = platforms[len(platforms) - 1]
        x_coordinate = generate_platform_x_coordinate(jump_seconds(player, gravity),
                                                      player.movement,
                                                      last_platform)
        new_platform = platform_copy(last_platform)

        new_platform.x_coordinate = x_coordinate
        new_platform.platform_color = (0, 250, 0)
        new_platform.y_coordinate = needed_y_coordinate(x_coordinate,
                                                        player, last_platform, gravity)

        platforms.append(new_platform)
        return platforms

    def generate_enemy(platform, enemies):
        new_enemy = SimpleEnemy()
        platform_end = platform.x_coordinate + platform.length

        new_enemy.x_coordinate = (platform.x_coordinate + platform_end) / 2

        new_enemy.y_coordinate = platform.y_coordinate - new_enemy.height

        enemies.append(new_enemy)

        return enemies

