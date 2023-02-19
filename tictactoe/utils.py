from tictactoe.game import Game

import tictactoe.tree as tree


def get_optimal_move(head: tree.Node, game: Game) -> int:
    # gets optimal move for current player
    # assumes the tree is favouring the current player
    moves = tree.find_node(game.state, head).children
    best_label = -99999999
    best_i = -1
    for i in range(9):
        if moves[i] is not None:
            if moves[i].label > best_label:
                best_label = moves[i].label
                best_i = i

    return best_i
