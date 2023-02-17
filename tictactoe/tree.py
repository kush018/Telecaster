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
    def __init__(self, game: Game, pos: int, favour: int, disfavour: int):
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
                self.children[i] = Node(copy.deepcopy(game), i, favour, disfavour)
                if self.children[i].result != Game.INVALID:
                    if self.plr == disfavour:
                        if self.children[i].label > self.label:
                            self.label = self.children[i].label
                    else:
                        if self.children[i].label < self.label:
                            self.label = self.children[i].label
                else:
                    self.children[i] = None

