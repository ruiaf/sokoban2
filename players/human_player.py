from map import Action


class HumanPlayer(object):
    def __init__(self, name):
        self.name = name

    def set_state(self, state):
        print(state)

    def get_action(self):
        # w->up, a->left, s->down, d->right, p->skip
        action = HumanPlayer.action_parse(
            input("Player %s: What's your move (using wasd keys)?" % self.name))
        while action is None:
            action = HumanPlayer.action_parse(
                input("Player %s: wrong move, try again. What's your move (using wasd keys)?" % self.name))
        return action

    def set_action_result(self, action_result):
        pass

    @staticmethod
    def action_parse(key: str):
        print("'%s'" % key)
        if len(key) < 1:
            return None
        if key[0] == "w":
            return Action.NORTH
        if key[0] == "a":
            return Action.WEST
        if key[0] == "s":
            return Action.SOUTH
        if key[0] == "d":
            return Action.EAST
        if key[0] == "p":
            return Action.SKIP
        return None
