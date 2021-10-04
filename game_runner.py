import cProfile
from game_mechanics import GameRunner
cProfile.run("GameRunner.run_game()", None, "cumtime")
print()