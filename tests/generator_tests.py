from game_components.items import Whip
import unittest
from base.engines import CollisionsFinder, InteractionEngine
from game_components.platforms import Platform
from game_components.players import Player
from game_components.enemies import SimpleEnemy
from game_components.generator import *
import random

class TestEngines(unittest.TestCase):
    def test_generate_platform_x_coordinate(self):
        last_platform = Platform()
        last_platform.x_coordinate = 100
        new_platform = Platform()
        new_platform.length = 100
        for x in range(250):
            last_platform.length = random.randint(50, 340)
            time_spent_in_air = 1
            new_platform_x_coordinate = generate_platform_x_coordinate(time_spent_in_air, Player.running_velocity, last_platform, new_platform)
            max_distance = time_spent_in_air * Player.running_velocity
            got_distance = new_platform_x_coordinate - (last_platform.x_coordinate + last_platform.length)
            jump_makeable =  max_distance >= got_distance
            self.assertTrue(jump_makeable, f"The jump should be makeable for the player max: {max_distance} vs got: {got_distance}")
            
            players_location = screen_length * .2
            last_platform_midpoint = last_platform.length * .5
            max_space_apart = screen_length - players_location - new_platform.length - last_platform_midpoint
            gotten_space_apart = new_platform_x_coordinate - (last_platform.x_coordinate + last_platform.length)
            platform_on_screen = gotten_space_apart <= max_space_apart
            self.assertTrue(platform_on_screen, f"The next platform should be on the screen when the player reaches the halfway point of the first platform want: {max_space_apart} vs gotten: {gotten_space_apart}")


unittest.main()
