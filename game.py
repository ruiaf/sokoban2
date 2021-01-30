import logging
import logging.handlers
from multiprocessing import Pool, Manager
from threading import Thread
import itertools

from args import Args
from map import Map
from players import RandomPlayer, HumanPlayer, QlearnPlayer

Args.instance().parser.add_argument("--map", help="Filepath to the map", default="./maps/simple.txt")
Args.instance().parser.add_argument("--player", help="Player", choices=["human", "random", "qlearn"], default="qlearn")
Args.instance().parser.add_argument("--n_turns", help="Maximum number of turns before halt", type=int, default=1000)
Args.instance().parser.add_argument("--n_games", help="Number of games to run in total", type=int, default=1000000)
Args.instance().parser.add_argument("--n_parallel", help="Number of games to run in parallel", type=int, default=7)
Args.instance().parser.add_argument("--log_level", help="Log level", default=logging.INFO)


class SokobanManager:
    def __init__(self, game_number):
        self.game_number = game_number

        logging.debug("Initializing map for game %d", game_number)
        self.map: Map = Map(Args.instance().args().n_turns)
        self.map.load_from_file(Args.instance().args().map)

        self.player: Dict[str, RandomPlayer] = dict()
        for player_name in self.map.players.keys():
            logging.debug("Initializing player %s for game %s as %s", player_name, game_number, Args.instance().args().player)
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
                logging.info("Game %d was won in turn %d", self.game_number, turn_number)
                print("yes")
                break

        if action_result.max_turns_reached:
            logging.info("Game %d was lost at turn %d", self.game_number, turn_number)

        logging.debug("Game %d final position at turn %d was:\n%s", self.game_number, turn_number, self.map)

    @staticmethod
    def go(xargs):
        game_index, log_queue = xargs
        logging.getLogger().setLevel(Args.instance().args().log_level)
        logging.getLogger().handlers.clear()
        logging.getLogger().addHandler(logging.handlers.QueueHandler(log_queue))
        SokobanManager.logger_set = True
        SokobanManager(game_index).start()


class MultiGameManager:
    @staticmethod
    def logger_thread(log_queue):
        logging.getLogger().setLevel(Args.instance().args().log_level)
        while True:
            record = log_queue.get()
            if record is None:
                break
            logging.log(record.levelno, record.message)

    @staticmethod
    def go():
        # setup logging
        log_queue = Manager().Queue(-1)
        log_thread = Thread(target=MultiGameManager.logger_thread, args=(log_queue,))
        log_thread.start()

        # process pool
        args = ((i, log_queue) for i in range(Args.instance().args().n_games))
        with Pool(Args.instance().args().n_parallel) as pool:
            while True:
                res = pool.map(SokobanManager.go, itertools.islice(args, 20))
                if res is None:
                    breaks


if __name__ == '__main__':
    MultiGameManager.go()
