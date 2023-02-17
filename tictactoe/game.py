
class Game:

    '''
    0 1 2
    3 4 5
    6 7 8
    '''

    winpos = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    P1 = 1
    P2 = 2

    NORMAL = 0

    def __init__(self):
        self.state: list[int] = [0 for i in range(9)]
        self.cp: int = Game.P1

    def check_win(self) -> bool:
        for win in Game.winpos:
            if self.state[win[0]] == self.state[win[1]] == self.state[win[2]] == self.cp:
                return True
        return False

    def filled(self) -> bool:
        for cell in self.state:
            if cell == 0:
                return False
        return True

    INVALID = -1
    TIE = 3

    def play(self, choice: int) -> int:
        if 0 <= choice <= 8 and self.state[choice] == 0:
            self.state[choice] = self.cp
            if self.check_win():
                return self.cp
            elif self.filled():
                return Game.TIE
            else:
                if self.cp == Game.P1:
                    self.cp = Game.P2
                else:
                    self.cp = Game.P1
                return 0
        else:
            return Game.INVALID

