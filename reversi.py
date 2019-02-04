#!/usr/bin/env python3
from colorama import Fore, Back, Style
import agent_module as am

class Reversi:
    def __init__(self, player1, player2, rows=8, cols=8):
        self.rows = rows
        self.cols = cols
        board = [['.' for _ in range(cols)] for _ in range(rows)]
        board[3][3] = board[4][4] = player1.player_id
        board[3][4] = board[4][3] = player2.player_id
        self.board = am.GameBoard(board, p1=['x'], p2=['o'])
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1

    def print_game_result(self):
        if self.is_winner(self.player1):
            print("Winner: Player X")
        elif self.is_winner(self.player2):
            print("Winner: Player O")
        else:
            print("Draw")

    def swap_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def is_empty(self, field):
        if    field == '.':
            return True
        else:
            return False

    def get_allowed_moves(self, player):
        res = []
        op = self.get_opponent(player)
        for x in range(self.rows):
            for y in range(self.cols):
                field = self.board[x][y]
                if self.is_empty(field):
                    dir_list = am.getDirOfSymbolInNeighborhood(self.board, x, y, op.player_id)
                    for d in dir_list:
                        if am.isSymbolAfterSymbolSerie(x, y, d, self.board, player.player_id, op.player_id):
                            res.append((x,y))
                            break
        return res

    def apply_move(self, player, move):
        x = move[0]
        y = move[1]
        self.board[x][y] = player.player_id
        op = self.get_opponent(player)
        dir_list = am.getDirOfSymbolInNeighborhood(self.board, x, y, op.player_id)
        for d in dir_list:
            if am.isSymbolAfterSymbolSerie(x, y, d, self.board, player.player_id, op.player_id):
                am.replaceSymbolSerie(x, y, d, self.board, player.player_id, op.player_id)

    def get_opponent(self, player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1

    def is_winner(self, player):
        if not self.game_end():
            return False
        op = self.get_opponent(player)
        my_points = self.board.count_symbol(player.player_id)
        op_points = self.board.count_symbol(op.player_id)

        if my_points > op_points:
            return True
        return False

    def game_end(self):
        if (len(self.get_allowed_moves(self.player1)) == 0 and
            len(self.get_allowed_moves(self.player2)) == 0):
            return True
        return False

    def start_game(self):
        while not self.game_end():
            print()
            self.board.print_board()
            if self.get_allowed_moves(self.current_player):
                self.current_player.make_move(self)
            else:
                print("Player:", self.current_player.player_id, "has lost his or her turn.")
            self.swap_player()

        print()
        self.board.print_board()
        print()
        print("End of Game")
        self.print_game_result()
        w1 = 1 if self.is_winner(self.player1) else 0
        w2 = 1 if self.is_winner(self.player2) else 0
        d = 1 if w1 == 0 and w2 == 0 else 0
        return w1, d, w2


class NPCPlayerAlphaBeta(am.AgentAI):
    def reversi_heuristic(self, game, player):
        field_weights = [[10,1,8,4,4,8,1,10],
                         [ 1,0,7,4,4,7,0,1],
                         [ 8,7,8,4,4,8,7,8],
                         [ 4,4,4,4,4,4,4,4],
                         [ 4,4,4,4,4,4,4,4],
                         [ 8,7,8,4,4,8,7,8],
                         [ 1,0,7,4,4,7,0,1],
                         [10,1,8,4,4,8,1,10]]

        res = 0
        for i in range(8):
            for j in range(8):
                if game.board[i][j] == self.player_id:
                    res += field_weights[i][j]

        return res

    def __init__(self, player_id):
        super().__init__(player_id, max_depth=7, game_heuristic=self.reversi_heuristic)

    def make_move(self, game):
        print("A-B is thinking")
        move = self.alpha_beta_move(game)
        game.apply_move(self, move)


class NPCPlayerMCTS(am.AgentAI):
    def __init__(self, player_id):
        super().__init__(player_id, number_simulations=300)

    def make_move(self, game):
        print("MCTS is thinking")
        move = self.mcts_move(game)
        game.apply_move(self, move)


game = Reversi(NPCPlayerMCTS('x'), NPCPlayerAlphaBeta('o'))
game.start_game()
