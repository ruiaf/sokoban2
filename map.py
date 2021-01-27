from typing import List, Dict

from pieces import Piece, Pieces


class Position(object):
    def __init__(self, x, y):
        self.pos: (int, int) = (x, y)

    def next(self, action: 'Action'):
        return Position(
            self.pos[0] + action.pos[0],
            self.pos[1] + action.pos[1])

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return self.pos == other.pos


class Action(Position):
    def __init__(self, x, y):
        super().__init__(x, y)


class Actions:
    NORTH = Action(-1, 0)
    SOUTH = Action(1, 0)
    EAST = Action(0, 1)
    WEST = Action(0, -1)
    SKIP = Action(0, 0)

    ALL: List[Action] = [NORTH, SOUTH, EAST, WEST, SKIP]


class ActionResult(object):
    def __init__(self):
        self.player_moved = False
        self.box_moved = False
        self.box_moved_to_target = False
        self.box_moved_away_from_target = False
        self.box_is_stuck = False
        self.all_boxes_in_target = False
        self.max_turns_reached = False


class Map(object):
    def __init__(self, max_num_turns):
        self.map: List[List[Piece]] = list()
        self.width: int = None
        self.players: Dict[str, Position] = dict()
        self.open_boxes = 0
        self.num_turns_left = max_num_turns

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

            piece = Piece(c)
            if piece == Pieces.BOX:
                self.open_boxes += 1

            row.append(piece)

        self.num_turns_left *= len(self.players)

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
        self.num_turns_left -= 1
        result = ActionResult()

        if action == Actions.SKIP:
            return result

        cur_pos = self.players[player_name]
        next_pos = cur_pos.next(action)

        if self[next_pos] in [Pieces.EMPTY, Pieces.TARGET]:
            self.players[player_name] = next_pos
            result.player_moved = True
        elif self[next_pos] in [Pieces.BOX, Pieces.BOX_AT_TARGET]:
            next_box_pos = next_pos.next(action)
            if self[next_box_pos] in [Pieces.EMPTY, Pieces.TARGET]:
                result.player_moved = True
                result.box_moved = True
                result.box_moved_away_from_target = (self[next_pos] == Pieces.BOX_AT_TARGET)
                result.box_moved_to_target = (self[next_box_pos] == Pieces.TARGET)

                if result.box_moved_away_from_target:
                    self[next_pos] = Pieces.TARGET
                    self.open_boxes += 1
                else:
                    self[next_pos] = Pieces.EMPTY

                if result.box_moved_to_target:
                    self[next_box_pos] = Pieces.BOX_AT_TARGET
                    self.open_boxes -= 1
                else:
                    self[next_box_pos] = Pieces.BOX

                self.players[player_name] = next_pos

                if self.open_boxes == 0:
                    result.all_boxes_in_target = True

                # TODO: Detect stuck boxes early
                if not result.box_moved_to_target and False:
                    result.box_is_stuck = True

        if self.num_turns_left <= 0:
            result.max_turns_reached = True

        return result  # player tried to move but it can't move

    def __getitem__(self, position: Position) -> Piece:
        if position.pos[0] < 0 or \
                position.pos[0] >= len(self.map[0]) or \
                position.pos[1] < 0 or \
                position.pos[1] >= len(self.map):
            return None
        return self.map[position.pos[0]][position.pos[1]]

    def __setitem__(self, position: Position, piece: Piece):
        self.map[position.pos[0]][position.pos[1]] = piece
