from HUD import HUD
from players import Player
from velocity_calculator import VelocityCalculator


class ScoreKeeper:
    last_player_location = 0

    distance_traveled = 0
    current_distance = 0

    def set_player(player: Player):
        ScoreKeeper.last_player_location = player.x_coordinate
    def reset():
        ScoreKeeper.last_player_location = 0
        ScoreKeeper.distance_traveled = 0
        ScoreKeeper.current_distance = 0
    def give_score(player: Player, game_is_paused):
        if game_is_paused:
            HUD.show_score(ScoreKeeper.distance_traveled // 10)
            return
        is_moving_left = False
        is_moving_right = False

        if ScoreKeeper.last_player_location > player.x_coordinate:
            is_moving_left = True

        if ScoreKeeper.last_player_location < player.x_coordinate:
            is_moving_right = True

        if is_moving_left:
            ScoreKeeper.last_player_location = player.x_coordinate
            ScoreKeeper.current_distance -= player.running_velocity

        if is_moving_right or player.move_right:
            ScoreKeeper.last_player_location = player.x_coordinate
            ScoreKeeper.current_distance += VelocityCalculator.calc_distance(player.running_velocity)

        if ScoreKeeper.current_distance > ScoreKeeper.distance_traveled:
            ScoreKeeper.distance_traveled = ScoreKeeper.current_distance

        HUD.show_score(ScoreKeeper.distance_traveled // 10)

