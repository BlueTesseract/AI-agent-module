from agent_module import *

class Reversi:
	def __init__(self, player1, player2, rows=8, cols=8):
		self.board = [['.' for _ in range(cols)] for _ in range(rows)]
		self.board[3][3] = self.board[4][4] = player1.player_id
		self.board[3][4] = self.board[4][3] = player2.player_id
		self.player1 = player1
		self.player2 = player2
		self.current_player = player1

	def print_board(self):
		for r in self.board:
			print(''.join(r))

	def print_game_result(self):
		if self.is_winner(self.player1):
			print("Winner: Player1")
		elif self.is_winner(self.player2):
			print("Winner: Player2")
		else:
			print("Draw")

	def swap_player(self):
		if self.current_player == self.player1:
			self.current_player = self.player2
		else:
			self.current_player = self.player1

	def get_allowed_moves(self, player):
		res = []
		
		return res

	def apply_move(self, player, move):
		pass

	def get_opponent(self, player):
		if player == self.player1:
			return self.player2
		else:
			return self.player1

	def is_winner(self, player):
		if not self.game_end():
			return False
		op = self.get_opponent(player)
		my_points = countSymbolOn2DBoard(player.player_id, self.board)
		op_points = countSymbolOn2DBoard(op.player_id, self.board)

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
			self.print_board()
			self.current_player.make_move(self)
			self.swap_player()

		self.print_board()
		print()
		print("End of Game")
		self.print_game_result()


game = Reversi(HumanPlayer('x'), HumanPlayer('o'))
game.start_game()
