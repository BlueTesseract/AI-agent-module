from agent_module import *

class Reversi:
	def __init__(self, player1, player2, rows=8, cols=8):
		self.rows = rows
		self.cols = cols
		self.board = [['.' for _ in range(cols)] for _ in range(rows)]
		self.board[3][3] = self.board[4][4] = player1.player_id
		self.board[3][4] = self.board[4][3] = player2.player_id
		self.player1 = player1
		self.player2 = player2
		self.current_player = player1

	def print_board(self):
		row = 0
		print("   0 1 2 3 4 5 6 7")
		for r in self.board:
			print(str(row),'|'+'|'.join(r)+'|')
			row += 1

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

	def is_empty(slef, field):
		if	field == '.':
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
					dir_list = getDirOfSymbolInNeighborhood(self.board, x, y, op.player_id)
					for d in dir_list:
						if isSymbolAfterSymbolSerie(x, y, d, self.board, player.player_id, op.player_id):
							res.append((x,y))
							break
		return res

	def apply_move(self, player, move):
		x = move[0]
		y = move[1]
		self.board[x][y] = player.player_id
		op = self.get_opponent(player)
		dir_list = getDirOfSymbolInNeighborhood(self.board, x, y, op.player_id)
		for d in dir_list:
			if isSymbolAfterSymbolSerie(x, y, d, self.board, player.player_id, op.player_id):
				replaceSymbolSerie(x, y, d, self.board, player.player_id, op.player_id)

	def get_opponent(self, player):
		if player.player_id == self.player1.player_id:
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
			if game.get_allowed_moves(self.current_player):
				self.current_player.make_move(self)
			else:
				print("Player:", self.current_player.player_id, "has lost his or her turn.")
			self.swap_player()

		print()
		self.print_board()
		print()
		print("End of Game")
		self.print_game_result()


class NPCPlayer(AgentAI):
	def __init__(self, player_id):
		super().__init__(player_id)

	def make_move(self, game):
		move = self.random_move(game, self)
		game.apply_move(self, move)


game = Reversi(HumanPlayer('x'), NPCPlayer('o'))
game.start_game()
