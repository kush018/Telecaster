import copy

from tictactoe.game import Game


class Node:
    WIN = 3
    TIE = 2
    LOSE = 1

    '''
    pos - position to play
    favour - which player we want to win
    disfavour - which player we want to lose
    '''

    def __init__(self, game: Game, pos: int, favour: int, disfavour: int, head):

        if pos is None:
            # is head node
            self.children: list[Node] = [None for _ in range(9)]
            for i in range(9):
                self.children[i] = Node(copy.deepcopy(game), i, favour, disfavour, self)
            return

        self.plr = game.cp
        self.pos = pos
        self.favour = favour
        self.result = game.play(pos)

        if self.result == Game.INVALID:
            return

        if self.result == favour:
            self.label = Node.WIN
        elif self.result == disfavour:
            self.label = Node.LOSE
        elif self.result == Game.TIE:
            self.label = Node.TIE
        else:
            rot = get_rot_of_earliest_symmetric_gamestate(game.state)
            identical = find_node(get_rotated_gamestate(game.state, rot), head)
            if identical is not None:
                # identical node exists somewhere in the tree
                self.label = identical.label
                return

            # if the identical node does not exist

            # no label yet, need to find label
            self.children: list[Node] = [None for _ in range(9)]

            if self.plr == disfavour:
                self.label = Node.LOSE
            else:
                self.label = Node.WIN

            for i in range(9):
                self.children[i] = Node(copy.deepcopy(game), i, favour, disfavour, head)

                if self.children[i].result != Game.INVALID:
                    if self.plr == disfavour:
                        if self.children[i].label > self.label:
                            self.label = self.children[i].label
                    else:
                        if self.children[i].label < self.label:
                            self.label = self.children[i].label
                else:
                    self.children[i] = None

    def get_number_of_nodes(self):
        sum = 1
        try:
            for node in self.children:
                if node is not None:
                    sum += Node.get_number_of_nodes(node)
        except AttributeError:
            pass
        return sum

    def get_number_of_leaf_nodes(self):
        sum = 0
        try:
            for node in self.children:
                if node is not None:
                    sum += Node.get_number_of_leaf_nodes(node)
        except AttributeError:
            return 1
        return sum


def find_node(game_state: list[int], head: Node) -> Node:
    node: Node = head

    last_P1 = -1
    last_P2 = -1

    while True:
        try:
            pos_P1 = game_state.index(Game.P1, last_P1 + 1)
        except ValueError:
            pos_P1 = -1
        if pos_P1 == -1:
            break
        else:
            node = node.children[pos_P1]
            last_P1 = pos_P1
            if node is None:
                break

        try:
            pos_P2 = game_state.index(Game.P2, last_P2 + 1)
        except ValueError:
            pos_P2 = -1
        if pos_P2 == -1:
            break
        else:
            node = node.children[pos_P2]
            last_P2 = pos_P2
            if node is None:
                break

    return node


def get_rotated_index(i: int, rot: int) -> int:
    """
    0 1 2 - rot 0/4
    3 4 5
    6 7 8

    6 3 0 - rot 1
    7 4 1
    8 5 2

    8 7 6 - rot 2
    5 4 3
    2 1 0

    2 5 8 - rot 3
    1 4 7
    0 3 6
    """
    if rot == 0:
        return i
    elif rot == 1:
        return [6, 3, 0, 7, 4, 1, 8, 5, 2][i]
    elif rot == 2:
        return [8, 7, 6, 5, 4, 3, 2, 1, 0][i]
    elif rot == 3:
        return [2, 5, 8, 1, 4, 7, 0, 3, 6][i]
    else:
        return get_rotated_index(i, rot % 4)


def get_rotated_gamestate(state, rot):
    rotated = [0 for _ in range(9)]

    for i in range(9):
        rotated[i] = state[get_rotated_index(i, rot)]

    return rotated


# returns 0 if both equal; +1, if state1 occurs earlier than state2
# and -1 if state2 occurs earlier than state1
def compare_gamestates(state1: list[int], state2: list[int]):
    last_x = -1
    last_o = -1

    try:
        while True:
            x1 = state1.index(Game.P1, last_x + 1)
            x2 = state2.index(Game.P1, last_x + 1)
            if x1 > x2:
                # x2 is earlier
                return -1
            elif x1 < x2:
                # x1 is earlier
                return +1
            # x1 == x2
            last_x = x1

            o1 = state1.index(Game.P2, last_o + 1)
            o2 = state2.index(Game.P2, last_o + 1)
            if o1 > o2:
                # o2 is earlier
                return -1
            elif o1 < o2:
                # o1 is earlier
                return +1
            # o1 == o2
            last_o = o1
    except ValueError:
        return 0

def get_rot_of_earliest_symmetric_gamestate(state):
    states = list()
    states.append(state)
    states.append(get_rotated_gamestate(state, 1))
    states.append(get_rotated_gamestate(state, 2))
    states.append(get_rotated_gamestate(state, 3))
    best_rot = 0
    for i in range(1, len(states)):
        if compare_gamestates(states[i], states[best_rot]) > 0:
            best_rot = i

    return best_rot
