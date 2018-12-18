from agent_module import AgentAI, HumanPlayer

class OX:
	def __init__(self, player1, player2):
		self.board = [ ['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.'] ]
		self.player1 = player1
		self.player2 = player2
		self.current_player = player1

	def print_board(self):
		for r in self.board:
			print(''.join(r))

	def get_opponent(self, player):
		if player.player_id == self.player1.player_id:
			return self.player2
		else:
			return self.player1

	def get_allowed_moves(self, player=None):
		res = []
		for x in range(3):
			for y in range(3):
				if self.board[x][y] == '.':
					res.append((x,y))
		return res

	def apply_move(self, player, move):
		self.board[move[0]][move[1]] = player.player_id

	def is_winner(self, player):
		player_id = player.player_id
		for row in range(3):
			if self.board[row] == [player_id]*3:
				return True
			if [self.board[i][row] for i in range(3)] == [player_id]*3:
				return True
		if [self.board[i][i] for i in range(3)] == [player_id]*3:
			return True
		if [self.board[i][2-i] for i in range(3)] == [player_id]*3:
			return True
		return False

	def game_end(self):
		if not self.get_allowed_moves():
			return True
		if self.is_winner(self.player1):
			return True
		if self.is_winner(self.player2):
			return True
		return False

	def swap_player(self):
		if self.current_player.player_id == self.player1.player_id:
			self.current_player = self.player2
		else :
			self.current_player = self.player1

	def print_game_result(self):
		if self.is_winner(self.player1):
			print("Winner: Player1")
		elif self.is_winner(self.player2):
			print("Winner: Player2")
		else:
			print("Draw")

	def start_game(self):
		while not self.game_end():
			print()
			self.print_board()
			self.current_player.make_move(self)
			self.swap_player()

		print()
		print("End of Game")
		self.print_board()
		self.print_game_result()


class NPCPlayer(AgentAI):
	def __init__(self, player_id):
		super().__init__(player_id)

	def make_move(self, game):
		move = self.minimax_move(game)
		game.apply_move(self, move)


class NPCPlayerAlphaBeta(AgentAI):
	def __init__(self, player_id):
		super().__init__(player_id)

	def make_move(self, game):
		move = self.alpha_beta_move(game)
		game.apply_move(self, move)


game = OX(NPCPlayerAlphaBeta('x'), NPCPlayer('o'))
game.start_game()
