from agent_module import AgentAI

class OX:
	def __init__(self, player1, player2):
		self.board = [ ['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.'] ]
		self.player1 = player1
		self.player2 = player2
		self.current_player = player1

	def print_board(self):
		for r in self.board:
			print(''.join(r))

	def get_allowed_moves(self):
		res = []
		for x in range(3):
			for y in range(3):
				if self.board[x][y] == '.':
					res.append((x,y))
		return res

	def apply_move(self, player, move):
		self.board[move[0]][move[1]] = player

	def winner(self, player):
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
		if self.winner(self.player1.player_id):
			return True
		if self.winner(self.player2.player_id):
			return True

		return False

	def swap_player(self):
		if self.current_player == self.player1:
			self.current_player = self.player2
		else :
			self.current_player = self.player1

	def play(self):
		while not self.game_end():
			print()
			self.print_board()
			self.current_player.make_move(self)
			self.swap_player()

		print("End of Game")
		self.print_board()


class HumanPlayer:
	def __init__(self, player_id):
		self.player_id = player_id

	def make_move(self, game):
		ml = game.get_allowed_moves()
		print(ml)
		move = int(input("Select move: "))
		game.apply_move( self.player_id, ml[move])


class NPCPlayer(AgentAI):
	def __init__(self, player_id, oponent_id):
		self.player_id = player_id
		self.oponent_id = oponent_id
		super().__init__(player_id, oponent_id)

	def make_move(self, game):
		move = self.minimax(game, self.player_id)
		game.apply_move(self.player_id, move)

game = OX(HumanPlayer('x'), NPCPlayer('o', 'x'))
game.play()
