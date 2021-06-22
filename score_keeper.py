from HUD import HUD


class ScoreKeeper:
    last_player_location = 0

    distance_traveled = 0
    current_distance = 0

    def __init__(self, player):
        self.last_player_location = player.x_coordinate

    def give_score(self, player):
        hud = HUD()
        is_moving_left = False
        is_moving_right = False

        if self.last_player_location > player.x_coordinate:
            is_moving_left = True

        if self.last_player_location < player.x_coordinate:
            is_moving_right = True

        if is_moving_left:
            self.last_player_location = player.x_coordinate
            self.current_distance -= player.movement

        if is_moving_right or player.move_right:
            self.last_player_location = player.x_coordinate
            self.current_distance += player.movement

        if self.current_distance > self.distance_traveled:
            self.distance_traveled = self.current_distance

        HUD.show_score(self.distance_traveled // 10)
