from enum import Enum
from typing import List, Dict

from pieces import Piece, Pieces


class Position(object):
    def __init__(self, x, y):
        self.pos: (int, int) = (x, y)

    def next(self, action: 'Action'):
        return Position(
            self.pos[0] + action.pos[0],
            self.pos[1] + action.pos[1])


class Action(object):
    NORTH = Position(-1, 0)
    SOUTH = Position(1, 0)
    EAST = Position(0, 1)
    WEST = Position(0, -1)
    SKIP = Position(0, 0)

    @staticmethod
    def from_key(key: str):
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
        return None


class ActionResult(object):
    def __init__(self):
        pass


class Map(object):
    def __init__(self, max_num_turns):
        self.map: List[List[Piece]] = list()
        self.width: int = None
        self.players: Dict[str, Position] = dict()
        self.max_num_turns = max_num_turns

    def load_from_string(self, map_txt: str):
        map_txt += "\n"
        map_txt = map_txt.upper()
        row = list()
        for c in map_txt:
            if c == "\n":
                if len(row) == 0:
                    continue
                if self.width is not None and len(row) != self.width:
                    raise Exception("Invalid map width")

                self.width = len(row)
                self.map.append(row)
                row = list()
                continue

            if c.isdigit():
                self.players[c] = Position(len(self.map), len(row))
                c = " "

            row.append(Piece(c))

    def load_from_file(self, map_path):
        with open(map_path, "r") as map_file:
            self.load_from_string(map_file.read())

    def __str__(self) -> str:
        result = []
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                is_player = False
                for player_name, pos in self.players.items():
                    if pos.pos == (i, j):
                        result.append(player_name)
                        is_player = True
                        break
                if not is_player:
                    result.append(str(self.map[i][j]))
            result.append("\n")
        return "".join(result)

    def apply_action(self, player_name, action) -> ActionResult:
        cur_pos = self.players[player_name]
        next_pos = cur_pos.next(action)

        if self[next_pos] in [Pieces.EMPTY, Pieces.TARGET]:
            self.players[player_name] = next_pos
            return ActionResult()  # player moved
        elif self[next_pos] in [Pieces.BOX, Pieces.BOX_AT_TARGET]:
            next_box_pos = next_pos.next(action)
            if self[next_box_pos] in [Pieces.EMPTY, Pieces.TARGET]:
                self[next_box_pos] = Pieces.BOX if self[next_box_pos] == Pieces.EMPTY else Pieces.BOX_AT_TARGET
                self[next_pos] = Pieces.EMPTY if self[next_pos] == Pieces.BOX else Pieces.TARGET
                self.players[player_name] = next_pos
                return ActionResult()  # player moved box

        return ActionResult()  # player tried to move but it can't move

    def __getitem__(self, position: Position) -> Piece:
        if position.pos[0] < 0 or \
                position.pos[0] >= len(self.map[0]) or \
                position.pos[1] < 0 or \
                position.pos[1] >= len(self.map):
            return None
        return self.map[position.pos[0]][position.pos[1]]

    def __setitem__(self, position: Position, piece: Piece):
        self.map[position.pos[0]][position.pos[1]] = piece
