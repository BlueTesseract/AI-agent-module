import random
from copy import deepcopy

class AgentAI:
	def __init__(self, player_id):
		self.player_id = player_id

	def minimax(self, game, player, depth=0):
		if game.game_end():
			if game.is_winner(self):
				return 1
			elif game.is_winner(game.get_opponent(self)):
				return -1
			else:
				return 0

		moves = game.get_allowed_moves(player)
		res = []
		for m in moves:
			game_copy = deepcopy(game)
			game_copy.apply_move(player, m)
			res.append(self.minimax(game_copy, game.get_opponent(player), depth+1))

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

	def random_move(self, game, player):
		ml = game.get_allowed_moves(player)
		return random.choice(ml)


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

