from items import Whip
import unittest
from engines import CollisionsFinder, InteractionsFinder
from platforms import Platform
from players import Player
from enemies import SimpleEnemy

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
            player.x_coordinate = platform.x_coordinate - player.width - 1
            return player
        if number == 3:
            player.y_coordinate = platform.y_coordinate - platform.width - 1
            return player

    def test_enemy_on_platform(self):
        # x is 100 and y is 400
        platform = Platform()
        enemy = SimpleEnemy()
        enemy.y_coordinate = 400
        # Movement speed is 0.08
        enemy.x_coordinate = 100.07
        self.assertEquals(False, CollisionsFinder.enemy_on_platform(
            platform, enemy), "Shouldn't be on platform since enemy movement speed puts it off the platform beginning")

        enemy.x_coordinate = platform.x_coordinate + platform.length + enemy.width - .01
        self.assertEquals(False, CollisionsFinder.enemy_on_platform(platform, enemy), f"Shouldn't be on platform since enemy at {enemy.x_coordinate + enemy.width} movement"
                          + f"{enemy.velocity} speed puts it off the platform edge {platform.length + platform.x_coordinate}")

        enemy.x_coordinate = platform.x_coordinate + \
            platform.length - enemy.velocity * 1.2 - enemy.width
        self.assertEquals(True, CollisionsFinder.enemy_on_platform(platform, enemy), f"Enemy at {enemy.x_coordinate} is within the platforms coordinates of" +
                          f"({platform.x_coordinate}, {platform.x_coordinate + platform.length})")

    def test_on_platform(self):
        # x is 100 and y is 400
        platform = Platform()
        player = Player()
        # Player bottom is 400 and x is 100
        player.y_coordinate = 400 - player.height
        self.assertEquals(True, CollisionsFinder.on_platform(
            platform, player, 399), "Want true since player on platform")

        self.assertEquals(False, CollisionsFinder.on_platform(platform, player, 401),
                          f"Want false since last player bottom: 400 not less than platform x coordinate {platform.y_coordinate}")

        player.y_coordinate = 399 - player.height
        self.assertEquals(False, CollisionsFinder.on_platform(platform, player, 389),
                          f"Want false since player at ({player.x_coordinate},{player.y_coordinate}) and platform at ({platform.x_coordinate}, {platform.y_coordinate}) and last player bottom not less than platform x cooordinate")

        player.x_coordinate = platform.x_coordinate - 1 - player.width
        player.y_coordinate = 400 - player.height
        self.assertEquals(False, CollisionsFinder.on_platform(platform, player, 399),
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

        self.assertEquals(True, CollisionsFinder.platform_left_boundary(player, platform, last_player_x_coordinate - player.width), f"Should be True since last_player_x_coordinate" +
                          f" {last_player_x_coordinate - player.width} is less than platform start {platform.x_coordinate + player.width}")

        last_player_x_coordinate = platform.x_coordinate + platform.length + 3
        self.assertEquals(True, CollisionsFinder.platform_right_boundary(player, platform, last_player_x_coordinate), f"Should be True since last_player_x_coordinate" +
                          f" {last_player_x_coordinate} is greater than platforms right edge {platform.length + platform.x_coordinate}")

        self.assertEquals(False, CollisionsFinder.platform_left_boundary(player, platform, last_player_x_coordinate - player.width), f"Should be False since last_player_x_coordinate" +
                          f" {last_player_x_coordinate - player.width} is greater than platforms start {platform.x_coordinate}")

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
        InteractionsFinder.enemy_whip_interactions(enemy, whip)
        self.assertTrue(enemy.x_coordinate > last_enemy_x_coordinate,
                        f"Should have knocked enemy at ({enemy.x_coordinate + enemy.width} {last_enemy_x_coordinate}, {enemy.y_coordinate})right since whip is facing right whip being at x {whip.x_coordinate} length {whip.length + whip.x_coordinate}")

        whip.length = -70
        whip.player_is_facing_right = False
        enemy.x_coordinate = whip.x_coordinate + whip.length / 1.2

        last_enemy_x_coordinate = enemy.x_coordinate
        InteractionsFinder.enemy_whip_interactions(enemy, whip)
        self.assertTrue(enemy.x_coordinate < last_enemy_x_coordinate,
                        f"Should have knocked enemy left since whip is facing left {enemy.x_coordinate}, {last_enemy_x_coordinate}")

        enemy.x_coordinate = whip.x_coordinate + 1
        last_enemy_x_coordinate = enemy.x_coordinate
        InteractionsFinder.enemy_whip_interactions(enemy, whip)
        self.assertTrue(last_enemy_x_coordinate == enemy.x_coordinate,
                        "Enemy should not have moved since not within whip x coordinate and width")

    def test_player_enemy_interactions(self):
        player = Player()
        enemy = SimpleEnemy()
        player.x_coordinate = enemy.x_coordinate + enemy.width - 2
        player.y_coordinate = enemy.y_coordinate
        last_player_x_coordinate = player.x_coordinate
        prev_iteration_x_coordinate = enemy.x_coordinate - player.width - 1
        prev_iteration_enemy_x_coordinate = enemy.x_coordinate + 1
        InteractionsFinder.player_enemy_interactions(
            player, enemy, prev_iteration_x_coordinate, prev_iteration_enemy_x_coordinate)
        self.assertEquals(True, player.x_coordinate < last_player_x_coordinate, f"Should have knocked player left since player_x"
                          + f" {player.x_coordinate} and enemy_x {enemy.x_coordinate} {prev_iteration_x_coordinate} {prev_iteration_enemy_x_coordinate} {player.x_coordinate}")

        player.x_coordinate = enemy.x_coordinate + (enemy.width / 1.01)
        last_player_x_coordinate = player.x_coordinate
        prev_iteration_x_coordinate = enemy.x_coordinate + enemy.width + 1
        prev_iteration_enemy_x_coordinate = enemy.x_coordinate - 2
        InteractionsFinder.player_enemy_interactions(
            player, enemy, prev_iteration_x_coordinate, prev_iteration_enemy_x_coordinate)
        self.assertTrue(player.x_coordinate > last_player_x_coordinate, f"Should have knocked player right since player_x is " +
                        f"{prev_iteration_x_coordinate} and enemy_x is {enemy.x_coordinate} {prev_iteration_x_coordinate} {player.x_coordinate}")

unittest.main()
