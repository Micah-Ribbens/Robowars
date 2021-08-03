from UtilityClasses import GameObject
from copy import deepcopy
class Memento:
    name = ""
    game_object = GameObject()
    def __init__(self, name, game_object):
        self.name = name
        # Needed so they are two independant objects so changing one won't change the other
        self.game_object = deepcopy(game_object)

class HistoryKeeper:
    memento_list = []
    def add(game_object, name):
        memento = Memento(name, game_object)
        HistoryKeeper.memento_list.append(memento)
    def get(name):
        mementos = []
        for memento in HistoryKeeper.memento_list:
            if memento.name == name:
                mementos.append(memento)
        return mementos
    def get_last(name):
        mementos = HistoryKeeper.get(name)
        # print(len(mementos))
        if len(mementos) == 1:
            return mementos[0].game_object
        return mementos[len(mementos) - 2].game_object

