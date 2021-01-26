from map import Action


class HumanPlayer(object):
    def __init__(self, name):
        self.name = name

    def set_state(self, state):
        print(state)

    def get_action(self):
        action = Action.from_key(
            input("Player %s: What's your move (using wasd keys)?" % self.name))
        while action is None:
            action = Action.from_key(
                input("Player %s: wrong move, try again. What's your move (using wasd keys)?" % self.name))
        return action

    def set_action_result(self, action_result):
        pass
