from base.important_variables import (
    screen_length,
    screen_height,
)
from platforms import Platform
from enemies import SimpleEnemy
import random
from players import Player


def generate_platform_length():
    return random.randrange(int(screen_length * .3), int(screen_length * .4))


def generate_platform_height():
    return random.randrange(int(screen_height * .1), int(screen_height * .2))


def generate_platform_x_coordinate(time_spent_in_air, player_velocity,
                                   last_platform, new_platform):
    # Little bit of a buffer, so jump isn't too hard
    max_space_apart = player_velocity * time_spent_in_air * .8
    min_space_apart = max_space_apart / 1.3
    players_location_on_screen = screen_length * .2
    last_platform_midpoint = last_platform.length * .5
    space_taken_up_by_platforms = new_platform.length + last_platform_midpoint
    # Makes sure that when the player is halfway across the platform the new platform is fully visible
    max_space_apart_for_visibility = screen_length - space_taken_up_by_platforms - players_location_on_screen

    if max_space_apart >= max_space_apart_for_visibility and not platform_is_terrain(last_platform):
        return max_space_apart_for_visibility + last_platform.right_edge

    max_x_coordinate = max_space_apart + last_platform.right_edge
    min_x_coordinate = min_space_apart + last_platform.right_edge
    return random.randrange(int(min_x_coordinate), int(max_x_coordinate))


# Caller of function desides what is too big of a change from one platform y coordinate to the next
def platform_change_too_big(last_platform_y_coordinate, current_platform_y_coordinate, too_big_of_change):
    return abs(last_platform_y_coordinate - current_platform_y_coordinate) > too_big_of_change


def generate_platform_y_coordinate(player, last_platform, current_platform):
    # So platform never higher than the players jump height
    max_y_coordinate = last_platform.y_coordinate - player.max_jump_height * .8
    # So platform is always at the bottom 80% of screen
    if max_y_coordinate < screen_height * .2:
        max_y_coordinate = player.max_jump_height
    min_y_coordinate = last_platform.y_coordinate + max_y_coordinate
    if min_y_coordinate > screen_height:
        # Makes the platform be a little above the bottom of screen
        min_y_coordinate = screen_height - (current_platform.height * 1.1)

    return random.randrange(int(max_y_coordinate), int(min_y_coordinate))


def randomize_platform_terrain(platform):
    is_terrain = random.randint(1, 2) == 1
    if is_terrain:
        platform.height = screen_height
        platform.length = random.randint(1, 2) * screen_length


def platform_is_terrain(platform):
    return platform.length >= screen_length


class Generator:
    def generate_platform(platforms: Platform, player: Player, gravity):
        # IMPORTANT: order has to be height, lengths, y_coordinate, x_coordinate, randomize_platform_terrain()
        # Length and height dictate y_coordinate, y_coordinate dictates x_coordinate, and randomize_platform_terrain()
        # Changes the length so it can't be changed back by the generate_platform_length()
        new_platform = Platform()
        last_platform = platforms[len(platforms) - 1]
        new_platform.height = generate_platform_height()
        new_platform.length = generate_platform_length()
        new_platform.y_coordinate = generate_platform_y_coordinate(player, last_platform, new_platform)

        new_platform.platform_color = (0, 250, 0)
        players_time_in_air = player.time_in_air(new_platform.y_coordinate, last_platform.y_coordinate, gravity)
        new_platform.x_coordinate = generate_platform_x_coordinate(players_time_in_air, player.running_velocity, last_platform, new_platform)
        randomize_platform_terrain(new_platform)

        platforms.append(new_platform)
        return platforms

    def generate_enemy(platform: Platform, enemies, player):
        if platform_is_terrain(platform):
            for x in range(random.randint(1, 3)):
                new_enemy = SimpleEnemy(player)
                new_enemy.x_coordinate = (platform.x_coordinate + platform.right_edge) / 2 + (x * new_enemy.length * 3)
                new_enemy.y_coordinate = platform.y_coordinate - new_enemy.height
                new_enemy.platform_on = platform
                enemies.append(new_enemy)

            return enemies

        if random.randint(1, 6) == 1:
            return enemies

        new_enemy = SimpleEnemy(player)
        new_enemy.x_coordinate = platform.x_coordinate + (platform.length / 2)

        new_enemy.y_coordinate = platform.y_coordinate - new_enemy.height
        new_enemy.platform_on = platform

        enemies.append(new_enemy)

        return enemies
