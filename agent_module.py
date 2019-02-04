import random
import math
from copy import deepcopy
from colorama import Fore, Back, Style

class GameBoard:
    def __init__(self, board, unoccupied_symbols=['.'], out_of_board_symbols=[], p1=[], p2=[]):
        self.board = board
        self.out_of_board_symbols = out_of_board_symbols
        self.unoccupied_symbols = unoccupied_symbols
        self.p1 = p1
        self.p2 = p2

    def __getitem__(self, index):
        return self.board[index]

    def __len__(self):
        return len(self.board)

    def is_on_board(self, x, y):
        if x < 0 or y < 0:
            return False
        try:
            field = self.board[x][y]
            if field in self.out_of_board_symbols:
                return False
        except IndexError:
            return False
        return True

    def count_symbol(self, symbol):
        counter = 0
        for x in self.board:
            for s in x:
                if s == symbol:
                    counter += 1
        return counter

    def is_unoccupied(self, x, y):
        if not self.is_on_board(x, y):
            return False
        if self.board[x][y] in self.unoccupied_symbols:
            return True
        return False

    def is_occupied(self, x, y):
        if not self.is_on_board(x, y):
            return False
        if self.board[x][y] in self.unoccupied_symbols:
            return False
        return True

    def get_fore_color(self, field, p1_color, p2_color, default_color=Fore.RESET):
        if field in self.p1:
            return p1_color+field
        elif field in self.p2:
            return p2_color+field
        elif field in self.unoccupied_symbols:
            return ' '
        else:
            return default_color+field


    def print_board(self, f1=Back.GREEN, f2=Back.YELLOW, board_color=Back.RESET, sep='', p1=Fore.BLACK, p2=Fore.WHITE, default=Fore.RESET):
        board_sep = Style.RESET_ALL+board_color+sep
        row = 0
        offset = " "
        # Top Label
        print(offset + " "*len(sep) + (" "*len(sep)).join(map(lambda x: str(x%10), range(len(self.board[0])))))

        for r in self.board:
            print(
                Style.RESET_ALL
                +str(row%10)
                +board_sep
                +board_sep.join(
                    map(lambda x: f1+x[1] if (x[0]+row)%2 else f2+x[1],
                        enumerate(
                            map(lambda field: self.get_fore_color(field, p1, p2, default), r))
                        )
                               )
                    +board_sep
                    +Style.RESET_ALL
                  )
            row += 1


class MCTSNode:
    def __init__(self, parent, game, move, player):
        self.parent = parent
        self.children = []
        self.uninitialized_children = []
        self.simulations = 0
        self.win_playouts = 0
        self.game = game
        self.player = player
        self.move = move

class MCTSTree:
    def __init__(self, game, player, exploration_parameter=1.41, max_loops=10):
        self.total_simulations = 0
        self.max_loops = max_loops
        self.exploration_parameter = exploration_parameter
        game_copy = deepcopy(game)
        self.root = MCTSNode(None, game_copy, None, player)

    def uct(self, mcts_node):
        a = mcts_node.win_playouts / mcts_node.simulations
        b = self.exploration_parameter * math.sqrt(math.log(self.total_simulations)/mcts_node.simulations)
        return a+b

    def is_leaf(self, node):
        if node.children == []:
            return True
        else:
            return False

    def is_uninitialized_children(self, node):
        if node.uninitialized_children == []:
            return False
        else:
            return True

    def selection(self, node):
        if self.is_leaf(node) or self.is_uninitialized_children(node):
            return node

        current_max_node = None
        current_max_uct = -1
        for n in node.children:
            if self.uct(n) > current_max_uct:
                current_max_node = n
                current_max_uct = self.uct(n)
        return self.selection(current_max_node)

    def expansion(self, node):
        if self.is_leaf(node):
            node.uninitialized_children = node.game.get_allowed_moves(node.player)
            if node.game.game_end() == True:
                return node
            if not self.is_uninitialized_children(node):
                node.player = node.game.get_opponent(node.player)
                node.uninitialized_children = node.game.get_allowed_moves(node.player)
        next_player = node.game.get_opponent(node.player)

        move = random.choice(node.uninitialized_children)
        node.uninitialized_children.remove(move)
        game_copy = deepcopy(node.game)
        game_copy.apply_move(node.player, move)
        new_node = MCTSNode(node, game_copy, move, next_player)
        node.children.append(new_node)
        return new_node

    def simulation(self, node):
        game_copy = deepcopy(node.game)
        point = self.root.player.simulate_random_game(game_copy, node.player)
        self.total_simulations += 1
        if point != 1:
            point = 0
        return point

    def back_propagation(self, node, point, simulations=1):
        if node == None:
            return
        node.win_playouts += point
        node.simulations += simulations
        self.back_propagation(node.parent, point, simulations)

    def mcts_move(self):
        loops = self.max_loops

        while loops:
            loops -= 1
            node = self.selection(self.root)
            node = self.expansion(node)
            win = self.simulation(node)
            self.back_propagation(node, win)

        current_max_node = None
        current_max_simulations = -1
        for node in self.root.children:
            if node.simulations > current_max_simulations:
                current_max_node = node
                current_max_simulations = node.simulations

        return current_max_node.move


class AgentAI:
    def __init__(self, player_id, game_heuristic=None, number_simulations=10, max_depth=math.inf):
        self.player_id = player_id
        self.game_heuristic = game_heuristic
        self.number_simulations = number_simulations
        if game_heuristic == None:
            self.game_heuristic = self.random_simulate_heuristic
        self.max_depth = max_depth
        self.mcts_tree = None

    def minimax_move(self, game):
        return self._minimax(game, self)

    def random_move(self, game):
        ml = game.get_allowed_moves(self)
        return random.choice(ml)

    def alpha_beta_move(self, game, depth=0, alpha=-math.inf, beta=math.inf):
        return self.minimax_alpha(game, self, depth, alpha, beta)

    def mcts_move(self, game):
        mcts_tree = MCTSTree(game, self, max_loops=self.number_simulations)
        return mcts_tree.mcts_move()

# Helper-Functions
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
            if player == self:
                return moves[res.index(max(res))]
            else:
                return moves[res.index(min(res))]
        else:
            if player == self:
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
                move = player.random_move(game)
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

    def __eq__(self,other):
        return self.player_id == other.player_id


class HumanPlayer(AgentAI):
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


def print_game_result(game):
    if game.is_winner(game.player1):
        print("Winner: Player1")
    elif game.is_winner(game.player2):
        print("Winner: Player2")
    else:
        print("Draw")


def checkIfFieldEqSymbol(x, y, symbol, board2d):
    if board2d.is_on_board(x, y) and board2d[x][y] == symbol:
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


def    applyFunInDirection(direction, apply_function, board2d, x, y):
    rd, cd = getDiffForDir(direction)
    cont = True
    while cont:
        x += rd
        y += cd
        if not board2d.is_on_board(x, y):
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
        if not board2d.is_on_board(x, y):
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
