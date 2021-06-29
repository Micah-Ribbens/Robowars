import unittest
from wall_of_death import WallOfDeath
from engines import CollisionsFinder
from platforms import Platform
from players import Player
# d = Player()
class TestSum(unittest.TestCase):
    def test_move_backwards(self):
        starting_x_coordinate = WallOfDeath.x_coordinate
        amount = 9
        WallOfDeath.move_backwards(amount)
        end_x_coordinate = WallOfDeath.x_coordinate
        want = starting_x_coordinate - amount
        self.assertEquals(want, end_x_coordinate, "Move backwards by amount 9")

    def test_on_platform(self):
        # x is 100 and y is 400
        platform = Platform()
        player = Player()
        # Player bottom is 400 and x is 100
        player.y_coordinate = 400 - player.height
        # want = True
        # got = CollisionsFinder.on_platform(platform, player, 399)
        # print(platform.x_coordinate)
        self.assertEquals(True, CollisionsFinder.on_platform(platform, player, 399), "Want true since player on platform")
        self.assertEquals(False, CollisionsFinder.on_platform(platform, player, 400), "Want false since player not on platform")

        player.y_coordinate = 399 - player.height
        self.assertEquals(False, CollisionsFinder.on_platform(platform, player, 389), "Want false since player not on platform")

        player.x_coordinate = platform.x_coordinate - 1 - player.width
        player.y_coordinate = 400 - player.height
        self.assertEquals(False, CollisionsFinder.on_platform(platform, player, 399), f"Want false since player at ({player.x_coordinate},{player.y_coordinate}) and platform at ({platform.x_coordinate}, {platform.y_coordinate})")



unittest.main()