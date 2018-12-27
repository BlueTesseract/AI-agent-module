from agent_module import *

class GameTemplate:
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.current_player = player1

	def get_allowed_moves(self, player):
		pass

	def get_opponent(self, player):
		if player == self.player1:
			return self.player2
		else:
			return self.player1

	def apply_move(self, player, move):
		pass

	def is_winner(self, player):
		pass

	def game_end(self):
		pass

	def start_game(self):
		pass


class NPCPlayer(AgentAI):
	def __init__(self, player_id):
		super().__init__(player_id)

	def make_move(self, game):
		move = self.random_move(game)
		game.apply_move(self, move)


game = GameTemplate(NPCPlayer('x'), NPCPlayer('o'))
game.start_game()
