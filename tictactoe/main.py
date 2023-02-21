from tictactoe.game import Game
from tictactoe.tree import Node
import tictactoe.utils as utils

import pickle

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

    if player == Game.P1:
        # tree that favours P2
        with open('..\\tree_P2.object', 'rb') as inp:
            head = pickle.load(inp)
    else:
        # tree that favours P1
        with open('..\\tree_P1.object', 'rb') as inp:
            head = pickle.load(inp)

    game = Game()

    while True:
        if player == Game.P1:
            # player is X
            result = turn_player(game)
            if result == 0:
                # normal result
                result = game.play(utils.get_optimal_move(head, game))
        else:
            # computer is X
            result = game.play(utils.get_optimal_move(head, game))
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


if __name__ == '__main__':
    main()
