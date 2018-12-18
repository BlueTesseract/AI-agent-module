import random
import math
from copy import deepcopy

class AgentAI:
	def __init__(self, player_id, game_heuristic=None, number_simulations=100, max_depth=math.inf):
		self.player_id = player_id
		self.game_heuristic = game_heuristic
		self.number_simulations = number_simulations
		if game_heuristic == None:
			self.game_heuristic = self.random_simulate_heuristic
		self.max_depth = max_depth
		self.mcts_tree = None

	def minimax_move(self, game):
		return self._minimax(game, self)

	def random_move(self, game, player):
		ml = game.get_allowed_moves(player)
		return random.choice(ml)

	def alpha_beta_move(self, game, depth=0, alpha=-math.inf, beta=math.inf):
		return self.minimax_alpha(game, self, depth, alpha, beta)

# https://www.baeldung.com/java-monte-carlo-tree-search
	def mcts_move(self, game):
		if self.mcts_tree == None:
			self.mcts_tree = MCTSTree()
		move = self._mcts(game, self)
		self.mcts_tree = None


# Helper-Functions
	def _mcts(self, game, player):
		moves = game.get_allowed_moves(player)

	def _minimax(self, game, player, depth=0):
		if game.game_end():
			return self.return_minimax_game_end(game)

		if depth >= self.max_depth:
			return self.game_heuristic(game, player)

		moves = game.get_allowed_moves(player)
		res = []
		for m in moves:
			game_copy = deepcopy(game)
			game_copy.apply_move(player, m)
			res.append(self._minimax(game_copy, game.get_opponent(player), depth+1))
		return self.return_minimax(depth, player, moves, res)

	def minimax_alpha(self, game, player, depth, alpha, beta):
		if game.game_end():
			return self.return_minimax_game_end(game)

		if depth >= self.max_depth:
			return self.game_heuristic(game, player)

		moves = game.get_allowed_moves(player)
		if moves == []:
			return alpha

		res = []
		for m in moves:
			game_copy = deepcopy(game)
			game_copy.apply_move(player, m)
			alpha = max(alpha, self.minimax_beta(game_copy, game.get_opponent(player), depth+1, alpha, beta))
			res.append(alpha)
			if alpha >= beta:
				if depth == 0:
					return moves[res.index(max(res))]
				return beta
		return self.return_minimax(depth, player, moves, res)

	def minimax_beta(self, game, player, depth, alpha, beta):
		if game.game_end():
			return self.return_minimax_game_end(game)

		if depth >= self.max_depth:
			return self.game_heuristic(game, player)

		moves = game.get_allowed_moves(player)
		for m in moves:
			game_copy = deepcopy(game)
			game_copy.apply_move(player, m)
			beta = min(beta, self.minimax_alpha(game_copy, game.get_opponent(player), depth+1, alpha, beta))
			if alpha >= beta:
				return alpha
		return beta

	def return_minimax(self, depth, player, moves, res):
		if depth == 0:
			if player.player_id == self.player_id:
				return moves[res.index(max(res))]
			else:
				return moves[res.index(min(res))]
		else:
			if player.player_id == self.player_id:
				return max(res)
			else:
				return min(res)

	def return_minimax_game_end(self, game):
		if game.is_winner(self):
			return math.inf
		elif game.is_winner(game.get_opponent(self)):
			return -math.inf
		else:
			return 0

	def simulate_random_game(self, game, player):
		while not game.game_end():
			if game.get_allowed_moves(player):
				move = self.random_move(game, player)
				game.apply_move(player, move)
			player = game.get_opponent(player)

		if game.is_winner(self):
			return 1
		elif game.is_winner(game.get_opponent(self)):
			return -1
		return 0

	def simulate_n_random_games(self, game, player, n):
		summary = 0

		for i in range(n):
			game_copy = deepcopy(game)
			summary += self.simulate_random_game(game_copy, player)

		return summary

	def random_simulate_heuristic(self, game, player):
		return self.simulate_n_random_games(game, player, self.number_simulations)


def countSymbolOn2DBoard(symbol, board):
	counter = 0
	for x in board:
		for s in x:
			if s == symbol:
				counter += 1
	return counter


def isOnBoard(x, y, board2d):
	if x < 0 or y < 0:
		return False
	try:
		a = board2d[x][y]
	except IndexError:
		return False
	return True


def checkIfFieldEqSymbol(x, y, symbol, board2d):
	if isOnBoard(x, y, board2d) and board2d[x][y] == symbol:
		return True
	return False


def getDiffForDir(direction):
	# 0 1 2
	# 7 X 3
	# 6 5 4
	if direction == 0:
		return -1, -1
	if direction == 1:
		return -1, 0
	if direction == 2:
		return -1, 1
	if direction == 3:
		return 0, 1
	if direction == 4:
		return 1, 1
	if direction == 5:
		return 1, 0
	if direction == 6:
		return 1, -1
	if direction == 7:
		return 0, -1


def getDirOfSymbolInNeighborhood(board2d, r, c, symbol):
	res = []
	for d in range(8):
		rd,cd = getDiffForDir(d)
		if checkIfFieldEqSymbol(r+rd, c+cd, symbol, board2d):
			res.append(d)
	return res


def	applyFunInDirection(direction, apply_function, board2d, x, y):
	rd, cd = getDiffForDir(direction)
	cont = True
	while cont:
		x += rd
		y += cd
		if not isOnBoard(x, y, board2d):
			return
		cont = apply_function(x, y, board2d)


def replaceSymbolSerie(x, y, direction, board2d, replace_to, sym_in_serie):
	def to_apply(x, y, board, s=replace_to, ss=sym_in_serie):
		if board[x][y] == ss:
			board[x][y] = s
			return True
		else:
			return False
	applyFunInDirection(direction, to_apply, board2d, x, y)


def checkFunInDirection(direction, check_function, board2d, x, y):
	res = False
	rd, cd = getDiffForDir(direction)
	cont = True
	while cont:
		x += rd
		y += cd
		if not isOnBoard(x, y, board2d):
			return False
		cont, res = check_function(board2d[x][y])
	return res


def isSymbolAfterSymbolSerie(x, y, direction, board2d, sym, sym_in_serie):
	def to_check(field, s=sym, ss=sym_in_serie):
		if field == ss:
			return True, False
		if field == s:
			return False, True
		return False, False
	return checkFunInDirection(direction, to_check, board2d, x, y)


class HumanPlayer:
	def __init__(self, player_id):
		self.player_id = player_id

	def make_move(self, game):
		ml = game.get_allowed_moves(self)
		if ml :
			for index, m in enumerate(ml):
				print(str(index)+":", m)

			correct_move = False
			while correct_move == False:
				move = input("Select move: ")
				if not move or int(move) >= len(ml) or int(move) < 0:
					print("Wrong move_id. Enter correct id, please.")
					correct_move = False
				else:
					move = int(move)
					correct_move = True

			game.apply_move(self, ml[move])
		else:
			print("Player:", self.player_id, "has lost turn")
