class ConsistencyKeeper:
    # The more code that is added to while loop in the run_game() in
    # game_mechanics.py the slower the less times the while loop executes
    # The code so this variable is what we based all the game movements off of
    # to figure out what the new_speed movments should be
    # Increased by.
    streamlined_speed = 0
    new_speed = 0
    current_speed = 0

    def __init__(self, streamlined_speed):
        self.streamlined_speed = streamlined_speed

    # def change_new_speed(self, new_speed):

    #     self.new_speed = new_speed

    def calculate_new_speed(self, movement):
        if self.current_speed / self.streamlined_speed == 0:
            return movement
        return (self.current_speed / self.streamlined_speed) * movement

    def change_current_speed(self, current_speed):
        # if current_speed / self.streamlined_speed == 0:
        #     return
        self.current_speed = current_speed
