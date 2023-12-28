from base.history_keeper import HistoryKeeper
from game_components.items import Whip
import unittest
from base.engines import CollisionsFinder, InteractionEngine
from game_components.platforms import Platform
from game_components.players import Player
from game_components.enemies import SimpleEnemy

class TestEngines(unittest.TestCase):
    def get_test_players(self, number):
        """Number 1 is player that equals platform coordinates 2 is changed x coordinate
        3 is changed y coordinate"""
        player = Player()
        platform = Platform()
        player.x_coordinate = platform.x_coordinate
        player.y_coordinate = platform.y_coordinate
        if number == 1:
            return player
        if number == 2:
            player.x_coordinate = platform.x_coordinate - player.height - 1
            return player
        if number == 3:
            player.y_coordinate = platform.y_coordinate - platform.height - 1
            return player

    def test_on_platform(self):
        platform = Platform()
        player = Player()
        player.y_coordinate = 400 - player.height
        player.x_coordinate = platform.x_coordinate

        self.assertEquals(True, CollisionsFinder.on_platform(
            platform, player, 399), "Want true since player on platform")

        player.x_coordinate = platform.x_coordinate - 1
        player.y_coordinate = 400 - player.height - 1
        self.assertEquals(False, CollisionsFinder.on_platform(platform, player, False),
                          f"Want false since player at ({player.x_coordinate},{player.y_coordinate}) and platform at ({platform.x_coordinate}, {platform.y_coordinate})")

    def test_platform_collision(self):
        platform = Platform()
        self.assertEquals(True, CollisionsFinder.platform_collision(self.get_test_players(
            1), platform), "Should be a True because both x and y are inside/ right on platform")

        self.assertEquals(False, CollisionsFinder.platform_collision(self.get_test_players(
            2), platform), "Should be False becuase x coordinate is outside platform")

        self.assertEquals(False, CollisionsFinder.platform_collision(self.get_test_players(
            3), platform), "Should be False becuase y coordinate is outside platform")

    def test_platform_boundaries(self):
        platform = Platform()
        player = self.get_test_players(1)
        last_player_x_coordinate = platform.x_coordinate - 3
        self.assertEquals(False, CollisionsFinder.platform_right_boundary(player, platform, last_player_x_coordinate), f"Should be False since last_player_x_coordinate" +
                          f" {last_player_x_coordinate} is less than platform right edge {platform.length + platform.x_coordinate}")

        self.assertEquals(True, CollisionsFinder.platform_left_boundary(player, platform, last_player_x_coordinate - player.height), f"Should be True since last_player_x_coordinate" +
                          f" {last_player_x_coordinate - player.height} is less than platform start {platform.x_coordinate + player.height}")

        last_player_x_coordinate = platform.x_coordinate + platform.length + 3
        self.assertEquals(True, CollisionsFinder.platform_right_boundary(player, platform, last_player_x_coordinate), f"Should be True since last_player_x_coordinate" +
                          f" {last_player_x_coordinate} is greater than platforms right edge {platform.length + platform.x_coordinate}")

        self.assertEquals(False, CollisionsFinder.platform_left_boundary(player, platform, last_player_x_coordinate - player.height), f"Should be False since last_player_x_coordinate" +
                          f" {last_player_x_coordinate - player.height} is greater than platforms start {platform.x_coordinate}")

    def test_enemy_whip_interactions(self):
        whip = Whip()
        enemy = SimpleEnemy()
        whip.player_is_facing_right = True
        whip.x_coordinate = 200
        whip.length = 70
        whip.height = 10
        whip.whip_is_extending = True
        enemy.x_coordinate = whip.x_coordinate
        last_enemy_x_coordinate = enemy.x_coordinate
        enemy.y_coordinate = whip.y_coordinate
        InteractionEngine.enemy_whip_interactions(enemy, whip)
        self.assertTrue(enemy.x_coordinate > last_enemy_x_coordinate,
                        f"Should have knocked enemy at ({enemy.x_coordinate + enemy.height} {last_enemy_x_coordinate}, {enemy.y_coordinate})right since whip is facing right whip being at x {whip.x_coordinate} length {whip.length + whip.x_coordinate}")

        whip.length = -70
        whip.player_is_facing_right = False
        enemy.x_coordinate = whip.x_coordinate + whip.length / 1.2

        last_enemy_x_coordinate = enemy.x_coordinate
        InteractionEngine.enemy_whip_interactions(enemy, whip)
        self.assertTrue(enemy.x_coordinate < last_enemy_x_coordinate,
                        f"Should have knocked enemy left since whip is facing left {enemy.x_coordinate}, {last_enemy_x_coordinate}")

        enemy.x_coordinate = whip.x_coordinate + 1
        last_enemy_x_coordinate = enemy.x_coordinate
        InteractionEngine.enemy_whip_interactions(enemy, whip)
        self.assertTrue(last_enemy_x_coordinate == enemy.x_coordinate,
                        "Enemy should not have moved since not within whip x coordinate and height")


unittest.main()
