from tictactoe.game import Game
from tictactoe.tree import Node

def display(game: Game):
    for i in range(9):
        if game.state[i] == Game.P1:
            print('X', end=' ')
        elif game.state[i] == Game.P2:
            print('O', end=' ')
        else:
            print(i + 1, end=' ')
        if (i + 1) % 3 == 0:
            print()

def get_move_player(game: Game) -> int:
    display(game)
    if game.cp == Game.P1:
        return int(input('Player X turn(1-9): ')) - 1
    else:
        return int(input('Player O turn(1-9): ')) - 1

def get_optimal_move(head: Node) -> int:
    best_i = 0
    best_case = Node.LOSE
    for i in range(9):
        if head.children[i] != None and head.children[i].label > best_case:
            best_i = i
            best_case = head.children[i].label
    return best_i

def main():
    game = Game()
    first_move = get_move_player(game)
    head = Node(game, first_move, Game.P2, Game.P1)
    game.play(first_move)
    while True:
        if game.cp == Game.P1:
            player_move = get_move_player(game)
            result = game.play(player_move)
            if result == 0:
                head = head.children[player_move]
        else:
            computer_move = get_optimal_move(head)
            result = game.play(computer_move)
            if result == 0:
                head = head.children[computer_move]
        if result == Game.P1:
            print('Player X (human) has won!')
            return
        elif result == Game.P2:
            print('Player O (computer) has won!')
            return
        elif result == Game.TIE:
            print('It is a Tie!')
            return

if __name__ == '__main__':
    main()
