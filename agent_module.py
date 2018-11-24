from copy import deepcopy

class AgentAI:
	def __init__(self, my_id, p2_id):
		self.my_id = my_id
		self.p2_id = p2_id

	def minimax(self, game, player, depth=0):
		if game.game_end():
			if game.winner(self.my_id):
				return 1
			elif game.winner(self.p2_id):
				return -1
			else :
				return 0

		moves = game.get_allowed_moves()
		res = []
		for m in moves:
			game_copy = deepcopy(game)
			game_copy.apply_move(player,m)
			if player == self.my_id:
				res.append(self.minimax(game_copy, self.p2_id, depth+1))
			else:
				res.append(self.minimax(game_copy, self.my_id, depth+1))

		if depth == 0:
			if player == self.my_id:
				return moves[res.index(max(res))]
			else:
				return moves[res.index(min(res))]
		else:
			if player == self.my_id:
				return max(res)
			else:
				return min(res)

