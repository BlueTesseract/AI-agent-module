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
		if player == self.player1:
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
			self.current_player.make_move(self)
			self.swap_player()

		self.print_board()
		print()
		print("End of Game")
		self.print_game_result()



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

game = Reversi(HumanPlayer('x'), HumanPlayer('o'))
game.start_game()
