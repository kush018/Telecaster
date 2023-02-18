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
            # no label yet, need to find label
            self.children: list[Node] = [None for _ in range(9)]

            if self.plr == disfavour:
                self.label = Node.LOSE
            else:
                self.label = Node.WIN

            for i in range(9):
                #
                if game.state[i] == 0:
                    # i is not taken
                    self.children[i] = find_node(game.state, head)
                    if self.children[i] is None:
                        self.children[i] = Node(copy.deepcopy(game), i, favour, disfavour, head)
                else:
                    self.children[i] = Node(copy.deepcopy(game), i, favour, disfavour, head)
                #
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

    last_P1 = -1
    last_P2 = -1

    node: Node = head

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
