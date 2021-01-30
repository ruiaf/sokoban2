import random
from typing import Tuple, Dict
import math

from args import Args
from map import Action, ActionResult, Map, Actions

Args.instance().parser.add_argument("--learning_rate", help="Learning rate", type=float, default=0.1)
Args.instance().parser.add_argument("--discount_factor", help="Discount factor", type=float, default=0.9)
Args.instance().parser.add_argument("--epsilon", help="Epsilon-greedy exploration prob", type=float, default=0.1)


class StateKey:
    def __init__(self, state: Map):
        self.key = str(state)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key


class QlearnPlayer(object):
    q_map: Dict[Tuple[StateKey, Action], float] = dict()

    def __init__(self, name):
        self.turn = 1
        self.name = name
        self.last_state_key = None
        self.last_action = None
        self.last_reward = 0.0
        self.last_q_value = 0.0
        self.action_values: Dict[Action, float] = None
        self.best_action: Tuple[float, Action] = None

    def set_state(self, new_state: Map):
        new_state_key = StateKey(new_state)

        self.action_values = dict()
        self.best_action = None
        for action in Actions.ALL:
            self.action_values[action] = self.get_q_value(new_state_key, action)
            if self.best_action is None or self.best_action[0] < self.action_values[action]:
                self.best_action = (self.action_values[action], action)

        if self.last_state_key is not None:
            next_q_val = max(self.action_values.values())
            updated_q_val = self.last_q_value + Args.instance().args().learning_rate * (
                self.last_reward +
                Args.instance().args().discount_factor * (next_q_val - self.last_q_value)
            )
            self.set_q_value(self.last_state_key, self.last_action, updated_q_val)
            self.last_q_value = updated_q_val

        self.last_state_key = new_state_key

    def get_q_value(self, state_key, action: Action) -> float:
        return self.q_map.get((state_key, action), 0.0)

    def set_q_value(self, state_key, action: Action, value: float):
        self.q_map[(state_key, action)] = value

    def get_action(self) -> Action:
        if random.random() < Args.instance().args().epsilon:
            self.last_action = random.choice(Actions.ALL)
        else:
            self.last_action = self.best_action[1]
        return self.last_action

    def set_action_result(self, action_result):
        self.turn += 1
        self.last_reward = self.reward(action_result)

    def reward(self, action_result: ActionResult):
        r = 0.0

        if action_result.player_moved:
            r += 0.0001

        if action_result.box_moved:
            r += 0.001

        if action_result.box_moved_to_target:
            r += 0.01

        if action_result.box_moved_away_from_target:
            r -= 0.01

        if action_result.box_is_stuck and not action_result.box_moved_to_target:
            r -= 1000.0

        if action_result.all_boxes_in_target:
            r += 1000.0

        return r / math.log(self.turn + 1)
