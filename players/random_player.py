import random

from map import Action


class RandomPlayer(object):
    def __init__(self, name):
        self.name = name
        self.possible_actions = [Action.NORTH, Action.SOUTH, Action.WEST, Action.EAST]

    def set_state(self, state):
        print(state)

    def get_action(self) -> Action:
        return random.choice(self.possible_actions)

    def set_action_result(self, action_result):
        pass
