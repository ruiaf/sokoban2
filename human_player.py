import random

from map import Action


class HumanPlayer(object):
    def __init__(self, name):
        self.name = name

    def set_state(self, state):
        print(state)

    def get_action(self):
        action = Action.from_key(input("What's your move (using wasd keys)?"))
        while action is None:
            action = Action.from_key(input("Wrong input, try again. What's your move (using wasd keys)?"))
        return action

    def set_action_result(self, action_result):
        pass
