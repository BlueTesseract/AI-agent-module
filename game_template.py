from agent_module import AgentAI, print_game_result

class GameTemplate:
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.current_player = player1
		self.board = [ ['E', 'X', 'A', 'M', 'P', 'L', 'E']
		self.board = GameBoard(self.board)


	# get_allowed_moves must returns list of moves (apply_moves must understand that moves)
	def get_allowed_moves(self, player):
		pass

	# Get opponent of arg=player. Usually there is nothing to add/edit.
	def get_opponent(self, player):
		if player == self.player1:
			return self.player2
		else:
			return self.player1

	# this function applies arg=move (Usually, it is one of move from get_allowed_moves)
	def apply_move(self, player, move):
		pass

	# is_winner returns True if arg=player is winner
	def is_winner(self, player):
		pass

	# game_end returns True if there is end of game, otherwise False
	def game_end(self):
		pass

	# start_game is invoked to start game...
	def start_game(self):
		while not self.game_end():
			print()
			self.board.print_board()
			self.current_player.make_move(self)
			self.current_player = self.get_opponent(self.current_player)

		print()
		print("End of Game")
		self.board.print_board()
		print_game_result()


# RandomPlayer for visualization purposes
class NPCPlayer(AgentAI):
	def __init__(self, player_id):
		super().__init__(player_id)

	def make_move(self, game):
		move = self.random_move(game)
		game.apply_move(self, move)


game = GameTemplate(NPCPlayer('x'), NPCPlayer('o'))
game.start_game()
