from agent_module import *

class GameTemplate:
	def __init__(self, player1, player2):
		pass

	def get_allowed_moves(self, player):
		pass

	def get_opponent(self, player):
		if player.player_id == self.player1.player_id:
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


