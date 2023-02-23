from tictactoe.game import Game
import tictactoe.tree as tree

import pickle
import os


def get_optimal_move(head: tree.Node, game: Game) -> int:
    # favours the current turn
    favour = game.cp

    # gets optimal move for current player
    # assumes the tree is favouring Game.P1
    rot = tree.get_rot_of_earliest_symmetric_gamestate(game.state)
    moves = tree.find_node(tree.get_rotated_gamestate(game.state, rot), head).children
    if favour == Game.P1:
        # finds best label
        best_i = -1
        best_label = -99999999
    else:
        # finds worst label
        best_i = -1
        best_label = 99999999
    for i in range(9):
        if moves[i] is not None:
            if (favour == Game.P1 and moves[i].label > best_label) or (
                    favour == Game.P2 and moves[i].label < best_label):
                best_label = moves[i].label
                best_i = i

    return tree.get_rotated_index(best_i, rot - 4)


def display(game: Game):
    for i in range(9):
        if game.state[i] == Game.P1:
            print('[X]', end='')
        elif game.state[i] == Game.P2:
            print('(O)', end='')
        else:
            print(f' {i + 1} ', end='')
        if i == 8:
            print()
        elif (i + 1) % 3 == 0:
            print('\n - + - + -\n', end='')
        else:
            print('|', end='')


def turn_player(game: Game):
    # assuming current turn is players turn
    while True:
        display(game)
        try:
            if game.cp == Game.P1:
                move = int(input('Player X turn(1-9): ')) - 1
            else:
                move = int(input('Player O turn(1-9): ')) - 1
            result = game.play(move)
            if result == Game.INVALID:
                print('Invalid move')
            else:
                return result
        except ValueError:
            print('Invalid move')


def main():
    while True:
        ch = input('Play as X or O?\n')
        if ch == 'X' or ch == 'x':
            player = Game.P1
            break
        elif ch == 'O' or ch == 'o':
            player = Game.P2
            break
        else:
            print('Invalid choice. Enter either X or O.')

    # default tree (favours P1)
    if os.path.isfile('..\\decision_tree.object'):
        with open('..\\decision_tree.object', 'rb') as inp:
            head = pickle.load(inp)
    else:
        head = tree.Node(Game(), None, Game.P1, Game.P2, None)
        with open('..\\decision_tree.object', 'wb') as outp:
            pickle.dump(head, outp, -1)

    game = Game()

    while True:
        if player == Game.P1:
            # player is X
            result = turn_player(game)
            if result == 0:
                # normal result
                result = game.play(get_optimal_move(head, game))
        else:
            # computer is X
            result = game.play(get_optimal_move(head, game))
            if result == 0:
                # normal result
                result = turn_player(game)
        if result == player:
            display(game)
            print('Player has won!!')
            break
        elif result == Game.TIE:
            display(game)
            print('It is a tie!!')
            break
        elif result == 0:
            continue
        else:
            display(game)
            print('Computer has won!!')
            break
