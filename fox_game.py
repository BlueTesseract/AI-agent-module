from agent_module import *

class FoxGame:
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
		self.player2.x = 9
		self.player2.y = 9
		self.current_player = player1

		self.board = [	'      .--.--.      ',
						'      |\ | /|      ',
						'      | \|/ |      ',
						'      .--.--.      ',
						'      | /|\ |      ',
						'      |/ | \|      ',
						'.--.--.--.--.--.--.',
						'|\ | /|\ | /|\ | /|',
						'| \|/ | \|/ | \|/ |',
						'.--.--.--x--.--.--.',
						'| /|\ | /|\ | /|\ |',
						'|/ | \|/ | \|/ | \|',
						'o--o--o--o--o--o--o',
						'      |\ | /|      ',
						'      | \|/ |      ',
						'      o--o--o      ',
						'      | /|\ |      ',
						'      |/ | \|      ',
						'      o--o--o      ']
		self.board = list(map(list, self.board))
		self.board = GameBoard(self.board, out_of_board_symbols = [' '])

	def get_allowed_moves(self, player):
		if player == self.player1:
			return self.get_player1_moves()
		else:
			return self.get_player2_moves()

	def get_player1_moves(self):
		res = []
		for x in range(len(self.board)):
			for y in range(len(self.board[x])):
				if self.board[x][y] == self.player1.player_id:
					for field in self.get_neigh_fields(x, y):
						if self.board.is_unoccupied(field[0], field[1]):
							res.append(((x,y), field))
		return res

	def get_after_next_cords(self, start_cords, next_cords):
		diff_x = next_cords[0] - start_cords[0]
		diff_y = next_cords[1] - start_cords[1]
		return (next_cords[0]+diff_x, next_cords[1]+diff_y)

	def get_player2_moves(self):
		res = []
		current_pos = (self.player2.x, self.player2.y)
		for field in self.get_neigh_fields(self.player2.x, self.player2.y):
			if self.board.is_unoccupied(field[0], field[1]):
				res.append(('move', current_pos, field))
			else:
				res += self.get_capture_moves(current_pos)
		return res

	def get_capture_moves(self, current_pos):
		return self.__get_capture_moves(current_pos, [], [current_pos])

	def __get_capture_moves(self, current_pos, captured_fields, empty_fields):
		res = []
		for field in self.get_neigh_fields(current_pos[0], current_pos[1]):
			if not (self.board.is_unoccupied(field[0], field[1]) or (field in empty_fields)):
				x, y = self.get_after_next_cords(current_pos, field)
				if self.board.is_on_board(x, y):
					if self.board.is_unoccupied(x,y) or ((x,y) in empty_fields):
						res.append(('capture', (self.player2.x, self.player2.y), captured_fields+[field], (x,y)))
						res += self.__get_capture_moves((x,y), captured_fields+[field], empty_fields+[field])
		return res

	def get_neigh_fields(self, x, y):
		res = []
		if self.board.is_on_board(x-3, y):
			res.append((x-3, y))

		if self.board.is_on_board(x+3, y):
			res.append((x+3, y))

		if self.board.is_on_board(x, y+3):
			res.append((x, y-3))

		if self.board.is_on_board(x, y+3):
			res.append((x, y+3))

		if self.board.is_on_board(x+1, y+1) and self.board[x+1][y+1] == '\\':
			res.append((x+3, y+3))

		if self.board.is_on_board(x+1, y-1) and self.board[x+1][y-1] == '/':
			res.append((x+3, y-3))

		if self.board.is_on_board(x-1, y+1) and self.board[x-1][y+1] == '/':
			res.append((x-3, y+3))

		if self.board.is_on_board(x-1, y-1) and self.board[x-1][y-1] == '\\':
			res.append((x-3, y-3))

		return res

	def get_opponent(self, player):
		if player == self.player1:
			return self.player2
		else:
			return self.player1

	def apply_move(self, player, move):
		if player == self.player1:
			self.apply_player1_move(move)
		else:
			self.apply_player2_move(move)

	def apply_player1_move(self, move):
		from_field = move[0]
		to_field = move[1]
		self.board[from_field[0]][from_field[1]] = '.'
		self.board[to_field[0]][to_field[1]] = self.player1.player_id

	def apply_player2_move(self, move):
		if move[0] == 'capture':
			self.apply_capture_move(move)
		else:
			self.apply_move_move(move)

	def apply_capture_move(self, move):
		from_field = move[1]
		capture_list = move[2]
		to_field = move[3]
		self.board[from_field[0]][from_field[1]] = '.'
		self.board[to_field[0]][to_field[1]] = self.player2.player_id
		self.player2.x = to_field[0]
		self.player2.y = to_field[1]

		for to_capture in capture_list:
			self.board[to_capture[0]][to_capture[1]] = '.'

	def apply_move_move(self, move):
		from_field = move[1]
		to_field = move[2]
		self.board[from_field[0]][from_field[1]] = '.'
		self.board[to_field[0]][to_field[1]] = self.player2.player_id
		self.player2.x = to_field[0]
		self.player2.y = to_field[1]

	def is_winner(self, player):
		p2_moves = self.get_allowed_moves(self.player2)
		p2_win = (p2_moves != [])
		if player == self.player2:
			return p2_win
		else:
			return not p2_win

	def game_end(self):
		if self.get_allowed_moves(self.player2) == []:
			return True
		if self.board.count_symbol(self.player1.player_id) <= 5:
			return True

	def swap_player(self):
		if self.current_player == self.player1:
			self.current_player = self.player2
		else:
			self.current_player = self.player1

	def start_game(self):
		while not self.game_end():
			print()
			print_board(self)
			self.current_player.make_move(self)
			self.swap_player()

		print()
		print("End of Game")
		print_board(self)
		print_game_result(self)


class NPCPlayer(AgentAI):
	def __init__(self, player_id):
		super().__init__(player_id)

	def make_move(self, game):
		move = self.random_move(game)
		game.apply_move(self, move)


game = FoxGame(HumanPlayer('o'), HumanPlayer('x'))
game.start_game()
