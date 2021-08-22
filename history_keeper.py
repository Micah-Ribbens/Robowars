from copy import deepcopy
class Memento:
    name = ""
    object = None
    def __init__(self, name, object):
        self.name = name
        # Needed so they are two independent objects so changing one won't change the other
        self.object = deepcopy(object)

class HistoryKeeper:
    memento_list = []
    def reset():
        HistoryKeeper.memento_list = []
    def add(object, name):
        memento = Memento(name, object)
        HistoryKeeper.memento_list.append(memento)

    def get(name):
        mementos = []
        for memento in HistoryKeeper.memento_list:
            if memento.name == name:
                mementos.append(memento.object)
        return mementos

    def get_last(name):
        mementos = HistoryKeeper.get(name)
        if len(mementos) == 0:
            return None
        if len(mementos) == 1:
            return mementos[0]
        return mementos[len(mementos) - 2]

