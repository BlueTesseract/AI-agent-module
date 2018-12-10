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

	def get_allowed_moves(self, player=None):
		res = []
		for x in range(3):
			for y in range(3):
				if self.board[x][y] == '.':
					res.append((x,y))
		return res

	def apply_move(self, player_id, move):
		self.board[move[0]][move[1]] = player_id

	def is_winner(self, player):
		for row in range(3):
			if self.board[row] == [player]*3:
				return True
			if [self.board[i][row] for i in range(3)] == [player]*3:
				return True
		if [self.board[i][i] for i in range(3)] == [player]*3:
			return True
		if [self.board[i][2-i] for i in range(3)] == [player]*3:
			return True
		return False


	def game_end(self):
		if not self.get_allowed_moves():
			return True
		if self.is_winner(self.player1.player_id):
			return True
		if self.is_winner(self.player2.player_id):
			return True

		return False

	def swap_player(self):
		if self.current_player == self.player1:
			self.current_player = self.player2
		else :
			self.current_player = self.player1

	def print_game_result(self):
		if self.is_winner(self.player1.player_id):
			print("Winner: Player1")
		elif self.is_winner(self.player2.player_id):
			print("Winner: Player2")
		else:
			print("Draw")

	def play(self):
		while not self.game_end():
			print()
			self.print_board()
			self.current_player.make_move(self)
			self.swap_player()

		print("End of Game")
		self.print_board()
		self.print_game_result()


class NPCPlayer(AgentAI):
	def __init__(self, player_id, oponent_id):
		self.player_id = player_id
		self.oponent_id = oponent_id
		super().__init__(player_id, oponent_id)

	def make_move(self, game):
		move = self.minimax(game, self.player_id)
		game.apply_move(self.player_id, move)

game = OX(NPCPlayer('x', 'o'), NPCPlayer('o', 'x'))
game.play()
