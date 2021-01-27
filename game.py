import logging
from args import Args

from map import Map
from players import RandomPlayer, HumanPlayer, QlearnPlayer


Args.instance().parser.add_argument("--map", help="Filepath to the map", default="./maps/simple.txt")
Args.instance().parser.add_argument("--player", help="Player", choices=["human", "random", "qlearn"], default="qlearn")
Args.instance().parser.add_argument("--n_turns", help="Maximum number of turns before halt", type=int, default=100)
Args.instance().parser.add_argument("--n_games", help="Number of games to run in total", type=int, default=8000)
Args.instance().parser.add_argument("--n_parallel", help="Number of games to run in parallel", type=int, default=8)
Args.instance().parser.add_argument("--log_level", help="Log level", default=logging.DEBUG)


class SokobanManager:
    def __init__(self, game_number):
        self.game_number = game_number

        logging.info("Initializing map for game %d", game_number)
        self.map: Map = Map(Args.instance().args().n_turns)
        self.map.load_from_file(Args.instance().args().map)

        self.player: Dict[str, RandomPlayer] = dict()
        for player_name in self.map.players.keys():
            logging.info(
                "Initializing player %s for game %s as %s" % (player_name, game_number, Args.instance().args().player))
            if Args.instance().args().player == "random":
                self.player[player_name] = RandomPlayer(player_name)
            elif Args.instance().args().player == "human":
                self.player[player_name] = HumanPlayer(player_name)
            elif Args.instance().args().player == "qlearn":
                self.player[player_name] = QlearnPlayer(player_name)

    def start(self):
        turn_number = 0
        action_result = None
        for _ in range(1, Args.instance().args().n_turns + 1):
            turn_number += 1
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

    logging.getLogger().setLevel(Args.instance().args().log_level)

    i = 0
    while i < Args.instance().args().n_games:
        b, e = i, min(i + Args.instance().args().n_parallel, Args.instance().args().n_games)
        for m in range(b, e):  # these are actually not running in parallel yet
            SokobanManager(m).start()
            i += 1
