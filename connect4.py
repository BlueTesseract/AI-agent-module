from agent_module import AgentAI, GameBoard
from colorama import Fore, Back

class Connect4:
    def __init__(self, player1, player2, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [['.' for _ in range(cols)] for _ in range(rows)]
        self.board = GameBoard(self.board, p1=[player1.player_id], p2=[player2.player_id])
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

    def print_board(self):
        f1 = f2 = Back.BLACK
        board_color = Back.BLUE
        sep = '|'
        p1 = Fore.RED
        p2 = Fore.YELLOW
        self.board.print_board(f1, f2, board_color, sep, p1, p2, left_label=False)

    def get_allowed_moves(self, player):
        res = []
        for index, top_field in enumerate(self.board[0]):
            if top_field == '.':
                res.append(index)

        return res

    def get_opponent(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def apply_move(self, player, move):
        for i in reversed(range(self.rows)):
            if self.board[i][move] == '.':
                self.board[i][move] = player.player_id
                break

    def print_game_result(self):
        if self.is_winner(self.player1):
            print("Winner: Player1")
        elif self.is_winner(self.player2):
            print("Winner: Player2")
        else:
            print("Draw")

    def is_winner(self, player):
        pid = player.player_id
        for row in self.board:
            if self.four_in_row(pid, row):
                return True

        for col_id in range(self.cols):
            col = [self.board[i][col_id] for i in range(self.rows)]
            if self.four_in_row(pid, col):
                return True

        for cid in range(self.cols):
            for rid in range(self.rows):
                line = []
                x, y = rid, cid
                while x < self.rows and y < self.cols:
                    line.append(self.board[x][y])
                    x += 1
                    y += 1
                if self.four_in_row(pid, line):
                    return True

        for cid in range(self.cols):
            for rid in range(self.rows):
                line = []
                x, y = rid, cid
                while x >= 0 and y < self.cols:
                    line.append(self.board[x][y])
                    x -= 1
                    y += 1
                if self.four_in_row(pid, line):
                    return True

        return False

    def four_in_row(self, pid, row):
        counter = 0
        for field in row:
            if field == pid:
                counter += 1
            else:
                counter = 0
            if counter == 4:
                return True
        return False

    def all_occupied(self):
        return list(filter(lambda x : x == '.', self.board[0])) == []

    def game_end(self):
        if self.is_winner(self.player1) or self.is_winner(self.player2) or self.all_occupied():
            return True
        return False

    def start_game(self):
        while not self.game_end():
            print()
            self.print_board()
            self.current_player.make_move(self)
            self.current_player = self.get_opponent(self.current_player)
        print()
        self.print_board()
        print()
        print("End of Game")
        self.print_game_result()


class NPCPlayerRandom(AgentAI):
    def __init__(self, player_id):
        super().__init__(player_id)

    def make_move(self, game):
        move = self.random_move(game)
        game.apply_move(self, move)


game = Connect4(NPCPlayerRandom('x'), NPCPlayerRandom('o'))
game.start_game()
