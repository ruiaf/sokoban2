import random
import logging

from map import Action, ActionResult


class QlearnPlayer(object):
    def __init__(self, name):
        self.name = name
        self.possible_actions = [Action.NORTH, Action.SOUTH, Action.WEST, Action.EAST, Action.SKIP]

    def set_state(self, state):
        pass

    def get_action(self) -> Action:
        return random.choice(self.possible_actions)

    def set_action_result(self, action_result):
        reward = self.reward(action_result)
        logging.debug("Reward was %f", reward)

    def reward(self, action_result: ActionResult):
        r = 0.0

        if action_result.player_moved:
            r += 0.001

        if action_result.box_moved:
            r += 0.002

        if action_result.box_moved_to_target:
            r += 0.05

        if action_result.box_moved_away_from_target:
            r += -0.06

        if action_result.box_is_stuck:
            r += -1.0

        if action_result.all_boxes_in_target:
            r += 1.0

        return r
