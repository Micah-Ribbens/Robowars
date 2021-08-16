from HUD import HUD
from players import Player
from velocity_calculator import VelocityCalculator
from history_keeper import HistoryKeeper


class ScoreKeeper:
    distance_traveled = 0
    current_distance = 0

    def reset():
        ScoreKeeper.distance_traveled = 0
        ScoreKeeper.current_distance = 0

    def give_score(player: Player):
        last_player = HistoryKeeper.get_last("player")
        if last_player.x_coordinate > player.x_coordinate:
            last_player.x_coordinate = player.x_coordinate
            ScoreKeeper.current_distance -= VelocityCalculator.calc_distance(player.running_velocity)

        is_moving_right = player.x_coordinate > last_player.x_coordinate
        if is_moving_right or player.game_is_sidescrolling:
            last_player.x_coordinate = player.x_coordinate
            ScoreKeeper.current_distance += VelocityCalculator.calc_distance(player.running_velocity)

        if ScoreKeeper.current_distance > ScoreKeeper.distance_traveled:
            ScoreKeeper.distance_traveled = ScoreKeeper.current_distance

        HUD.show_score(ScoreKeeper.distance_traveled // 10)

