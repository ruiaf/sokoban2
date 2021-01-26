import argparse
import logging

from map import Map
from random_player import RandomPlayer
from human_player import HumanPlayer

parser = argparse.ArgumentParser(description="Run the game")
parser.add_argument("--map", help="Filepath to the map", default="./maps/simple_two_player.txt")
parser.add_argument("--player", help="Player type", choices=["human", "random"], default="human")
parser.add_argument("--n_turns", help="Maximum number of turns before halt", type=int, default=100)
parser.add_argument("--n_games", help="Number of games to run in total", type=int, default=1)
parser.add_argument("--n_parallel", help="Number of games to run in parallel", type=int, default=1)
parser.add_argument("--log_level", help="Log level", default=logging.ERROR)
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
            logging.info("Initializing player %s for game %s" % (player_name, game_number))
            if args.player == "random":
                self.player[player_name] = RandomPlayer(player_name)
            elif args.player == "human":
                self.player[player_name] = HumanPlayer(player_name)

    def start(self):
        for turn_number in range(args.n_turns):
            logging.debug("Turn %d in game %d" % (turn_number, self.game_number))
            print(self.map)
            for player_name, player in self.player.items():
                player.set_state(self.map)
                action = player.get_action()
                action_result = self.map.apply_action(player_name, action)
                player.set_action_result(action_result)


if __name__ == '__main__':  
    i = 0
    while i < args.n_games:
        b, e = i, min(i + args.n_parallel, args.n_games)
        for m in range(b, e): # these are actually not running in parallel yet
            SokobanManager(m).start()
            i += 1
