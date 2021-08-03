from typing import NewType
from important_variables import (
    screen_length,
    screen_height,
    # consistency_keeper
)
from platforms import Platform
from enemies import SimpleEnemy
import random
from players import Player
import cProfile
from velocity_calculator import VelocityCalculator

# TODO why is this needed?
def platform_copy(platform):
    copy = Platform()
    copy.y_coordinate = platform.y_coordinate
    return copy


def generate_platform_length():
    return random.randrange(int(screen_length * .3), int(screen_length * .4))


def generate_platform_height():
    return random.randrange(int(screen_height * .1), int(screen_height * .2))

    # Sees if whole platform on screen so it is screen_length minus where the player always is on the screen
    # Which is 20% of screen length - platform_length to see if the end of platform on screen
    # Has to acount for the gap between the platforms also
def give_space_apart_for_platform_visibility(players_location, new_platform_length, last_platform_midpoint):
    # TODO why does this work the way it does?
    return screen_length - players_location - last_platform_midpoint - new_platform_length

def generate_platform_x_coordinate(time_spent_in_air, player_velocity,
                                   last_platform, new_platform):
    # Little bit of a buffer, so jump isn't too hard
    max_space_apart = player_velocity * time_spent_in_air * .8
    min_space_apart = max_space_apart / 1.3
    # TODO maybe change players_location_on_screen and why the player is always there
    players_location = screen_length * .2
    # Makes sure that when the player is halfway across the platform the new platform is fully visible
    space_apart_for_platform_visibility = give_space_apart_for_platform_visibility(players_location, new_platform.length, last_platform.length * .5)
    # TODO explain this if statement a bit more like why include "not is_terrain"
    if max_space_apart >= space_apart_for_platform_visibility and not is_terrain(last_platform):
        space_apart = space_apart_for_platform_visibility
        return  space_apart + last_platform.right_edge * random.randint(9, 10) * .1
    # TODO why the plus 1?
    max_x_coordinate = max_space_apart + last_platform.right_edge + 1
    min_x_coordinate = min_space_apart + last_platform.right_edge
    return random.randrange(int(min_x_coordinate), int(max_x_coordinate))
# As in if the platform goes down 40% relative to the last platform that would be too big
# Caller of function desides what is too big based on too_big_of_change
def platform_change_too_big(last_platform_y_coordinate, current_platform_y_coordinate, too_big_of_change):
    return abs(last_platform_y_coordinate - current_platform_y_coordinate) > too_big_of_change
def generate_platform_y_coordinate(player, last_platform, current_platform):
    # So platform never higher than the players jump height and draws from top to bottom meaning 
    # Max height will be the smaller number
    max_y_coordiante = player.max_jump_height * .8
    # TODO explain this if statement and logic inside it
    if max_y_coordiante > last_platform.y_coordinate + (player.max_jump_height * .6):
        max_y_coordiante = last_platform.y_coordinate + player.max_jump_height
    min_y_coordinate = last_platform.y_coordinate + max_y_coordiante
    if min_y_coordinate > screen_height:
        # Makes the platform be a little above the bottom of screen
        min_y_coordinate = screen_height - (current_platform.height * 1.1)
    return random.randrange(int(max_y_coordiante), int(min_y_coordinate))

def randomize_platform_terrain(platform):
    is_terrain = random.randint(1, 2) == 1
    # TODO if add vertical scrolling fix this logic
    if is_terrain:
        platform.height = screen_height
        platform.length = random.randint(1, 2) * screen_length
def is_terrain(platform):
    # TODO change this if randomize_platform_terrain is changed
    return platform.length >= screen_length
class Generator:
    def generate_platform(platforms: Platform, player: Player, gravity):
        # TODO explain or change logic because certain logic has to be in a certain order
        new_platform = Platform()
        last_platform = platforms[len(platforms) - 1]
        new_platform.height = generate_platform_height()
        new_platform.length = generate_platform_length()
        y_coordinate = generate_platform_y_coordinate(player, last_platform, new_platform)

        new_platform.y_coordinate = y_coordinate
        new_platform.platform_color = (0, 250, 0)
        # TODO this is waaaaay tooo long
        new_platform.x_coordinate = generate_platform_x_coordinate(player.max_time_in_air(new_platform.y_coordinate, last_platform.y_coordinate, gravity), player.running_velocity, last_platform, new_platform)
        # randomize_platform_terrain(new_platform)

        platforms.append(new_platform)
        return platforms

    def generate_enemy(platform: Platform, enemies):
        # if random.randint(1, 2) == 1:
        #     # TODO why on earth append None?
        #     enemies.append(None)
        #     return enemies
        new_enemy = SimpleEnemy()
        # TODO where does this put the enemy?
        # platform_end = platform.x_coordinate + platform.length

        new_enemy.x_coordinate = platform.x_coordinate + (platform.length / 2)
        # print(new_enemy.x_coordinate, platform.x_coordinate, platform.length)

        new_enemy.y_coordinate = platform.y_coordinate - new_enemy.height

        enemies.append(new_enemy)

        return enemies