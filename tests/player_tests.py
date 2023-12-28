from game_components.items import Whip
import unittest
from base.engines import CollisionsFinder, InteractionsFinder, PhysicsEngine
from game_components.platforms import Platform
from game_components.players import Player
from game_components.enemies import SimpleEnemy
from base.important_variables import screen_height
class TestPlayers(unittest.TestCase):
    def test_max_time_in_air(self):
        player = Player()
        new_platform_y_coordinate = 200
        last_platform_y_coordinate = 400

        upwards_time = player.max_jump_height / player.upwards_velocity
        max_y_coordinate = last_platform_y_coordinate - player.max_jump_height
        downwards_time = (new_platform_y_coordinate - max_y_coordinate) / PhysicsEngine.gravity_pull
        got = player.max_time_in_air(new_platform_y_coordinate, last_platform_y_coordinate, PhysicsEngine.gravity_pull)
        self.assertEquals(upwards_time + downwards_time, got, "Should get the time it takes to jump and down onto the next platform")
        print("START OF TEST")
        last_platform_y_coordinate = player.height + (player.max_jump_height * .8)
        print(last_platform_y_coordinate - player.max_jump_height - player.height <= 0)
        upwards_time = (last_platform_y_coordinate - player.height) / player.upwards_velocity
        max_y_coordinate = player.height
        downwards_time = (new_platform_y_coordinate - max_y_coordinate) / PhysicsEngine.gravity_pull
        got = player.max_time_in_air(new_platform_y_coordinate, last_platform_y_coordinate, PhysicsEngine.gravity_pull)
        self.assertEquals(upwards_time + downwards_time, got, "Should account for the fact that the player hits the top of screen making the max_y_coordinte smaller")

unittest.main()
