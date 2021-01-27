import argparse
import logging

from map import Map
from players import RandomPlayer, HumanPlayer, QlearnPlayer

parser = argparse.ArgumentParser(description="Run the game")
parser.add_argument("--map", help="Filepath to the map", default="./maps/classic.txt")
parser.add_argument("--player", help="Player type", choices=["human", "random", "qlearn"], default="human")
parser.add_argument("--n_turns", help="Maximum number of turns before halt", type=int, default=100)
parser.add_argument("--n_games", help="Number of games to run in total", type=int, default=1)
parser.add_argument("--n_parallel", help="Number of games to run in parallel", type=int, default=1)
parser.add_argument("--log_level", help="Log level", default=logging.DEBUG)
args = parser.parse_args()

logging.getLogger().setLevel(args.log_level)


class SokobanManager:
    def __init__(self, game_number):
        self.game_number = game_number

        logging.info("Initializing map for game %d", game_number)
        self.map: Map = Map(args.n_turns)
        self.map.load_from_file(args.map)

        self.player: dict(str, RandomPlayer) = dict()
        for player_name in self.map.players.keys():
            logging.info("Initializing player %s for game %s as %s" % (player_name, game_number, args.player))
            if args.player == "random":
                self.player[player_name] = RandomPlayer(player_name)
            elif args.player == "human":
                self.player[player_name] = HumanPlayer(player_name)
            elif args.player == "qlearn":
                self.player[player_name] = QlearnPlayer(player_name)

    def start(self):
        for turn_number in range(1, args.n_turns + 1):
            logging.debug("Turn %d in game %d" % (turn_number, self.game_number))
            for player_name, player in self.player.items():
                player.set_state(self.map)
                action = player.get_action()
                action_result = self.map.apply_action(player_name, action)
                player.set_action_result(action_result)

            if action_result.all_boxes_in_target:
                logging.debug("Game %d was won in turn %d" % (self.game_number, turn_number))
                break

        if action_result.max_turns_reached:
            logging.debug("Game %d was lost at turn %d" % (self.game_number, turn_number))

        logging.debug("Game %d final position at turn %d was:\n%s" % (self.game_number, turn_number, self.map))


if __name__ == '__main__':
    i = 0
    while i < args.n_games:
        b, e = i, min(i + args.n_parallel, args.n_games)
        for m in range(b, e): # these are actually not running in parallel yet
            SokobanManager(m).start()
            i += 1
