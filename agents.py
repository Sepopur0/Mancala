from data import *
# import numpy as np
# INIT_BOARD = np.full(12, 5)
# INT_MAX = np.iinfo(np.int32).max
# INT_MIN = np.iinfo(np.int32).min


class GamePointer():
    def __init__(self, id, direction):
        self.id = id
        self.direction = direction

    def __str__(self):
        return str((self.id, self.direction))

    def copy(self):
        return GamePointer(self.id, self.direction)

    def next(self):
        self.id = (self.id + self.direction) % 12


class GameState:
    def __init__(self, board=INIT_BOARD, call=-1, empty_1=False, empty_2=False, player1_score=0, player2_score=0, player1_debt=0, player2_debt=0):
        self.board = board
        self.empty_1 = empty_1
        self.empty_2 = empty_2
        self.call = call  # set to -99 if home option is called
        self.player1_score = player1_score
        self.player2_score = player2_score
        self.player1_debt = player1_debt
        self.player2_debt = player2_debt

    def __call__(self, other):
        self.board = other.board
        self.player1_score = other.player1_score
        self.player2_score = other.player2_score
        self.player1_debt = other.player1_debt
        self.player2_debt = other.player2_debt

    @property
    def player1_true_score(self):
        return self.player1_score - self.player1_debt + self.player2_debt

    @property
    def player2_true_score(self):
        return self.player2_score - self.player2_debt + self.player1_debt

    @property
    def player1_final_score(self):
        return self.player1_true_score + np.sum(self.board[1:6])

    @property
    def player2_final_score(self):
        return self.player2_true_score + np.sum(self.board[7:])

    @property
    def heuristic_score(self):
        winner = self.find_winner(inplace=False)

        if winner == "Player 1":
            return INT_MAX - 1
        elif winner == "Player 2":
            return INT_MIN + 1
        elif winner == "Draw":
            return 0
        else:
            return self.player1_true_score - self.player2_true_score

    def copy(self):
        return GameState(self.board.copy(), self.player1_score, self.player2_score, self.player1_debt, self.player2_debt)

    def find_winner(self, inplace=True):
        if self.is_end_state():
            # Handle debts
            p1_score = self.player1_final_score
            p2_score = self.player2_final_score

            if inplace:
                self.player1_score = p1_score
                self.player2_score = p2_score
                self.board[1:6] = self.board[7:] = 0
                self.player1_debt = self.player2_debt = 0

            # Find winner
            if p1_score > p2_score:
                return "Player 1"
            elif p1_score < p2_score:
                return "Player 2"
            else:
                return "Draw"
        else:
            return None

    def is_end_state(self):
        return self.board[0] == self.board[6] == 0

    def get_player_cells(self, is_upside):
        if is_upside:
            return self.board[1:6:1]
        else:
            return self.board[-1:-6:-1]

    def no_more_moves(self, is_upside):
        return not np.any(self.get_player_cells(is_upside))

    def possible_move(self, is_upside):
        player_cells = self.get_player_cells(is_upside)
        valid_id = np.nonzero(player_cells)[0] + 1
        if not is_upside:
            valid_id = 12 - valid_id
        return (GamePointer(id, dirt) for id in valid_id for dirt in [-1, 1])

    def scatter_stones(self, is_upside):
        if not self.is_end_state():
            if is_upside:
                self.player1_score -= 5
                if self.player1_score < 0:
                    self.player1_debt -= self.player1_score
                    self.player2_score += self.player1_score
                    self.player1_score = 0
                self.board[1:6] += 1
            else:
                self.player2_score -= 5
                if self.player2_score < 0:
                    self.player2_debt -= self.player2_score
                    self.player1_score += self.player2_score
                    self.player2_score = 0
                self.board[7:] += 1

    def to_next_state(self, pointer: GamePointer):
        score = 0
        is_upside = (pointer.id >= 1 and pointer.id <= 5)
        is_continue = True
        while is_continue:
            stones = self.board[pointer.id]
            self.board[pointer.id] = 0
            while stones > 0:
                pointer.next()
                self.board[pointer.id] += 1
                stones -= 1
            pointer.next()
            if pointer.id == 0 or pointer.id == 6:
                return self

            if self.board[pointer.id] == 0:
                while self.board[pointer.id] == 0:
                    pointer.next()
                    if self.board[pointer.id]:
                        score += self.board[pointer.id]
                        self.board[pointer.id] = 0
                        pointer.next()
                    else:
                        is_continue = False
                        break
                else:
                    break

        if is_upside:
            self.player1_score += score
        else:
            self.player2_score += score

        return self

    def expand(self, is_upside):
        if self.no_more_moves(is_upside):
            self.scatter_stones(is_upside)

        for pointer in self.possible_move(is_upside):
            yield pointer, self.copy().to_next_state(pointer.copy())

    # def print(self):
    #     print(
    #         "P1 --> %2d                  %2d <-- P2"
    #         % (self.player1_score, self.player2_score)
    #     )
    #     print(
    #         "D1 --> %2d                  %2d <-- D2"
    #         % (self.player1_debt, self.player2_debt)
    #     )
    #     print("          ", end="")
    #     print("|", end="")
    #     print(*["%2d" % x for x in self.board[1:6]], sep="|", end="")
    #     print("|")

    #     print("        %2d|" % self.board[0], end="")
    #     print("--------------", end="")
    #     print("|%2d" % self.board[6])

    #     print("          ", end="")
    #     print("|", end="")
    #     print(*["%2d" % x for x in reversed(self.board[7:])], sep="|", end="")
    #     print("|")

    #     print("")
    #     print("            ^  ^  ^  ^  ^")
    #     print("moves:      1  2  3  4  5")


class Agent:
    def __init__(self, gstate=GameState(), reversed=False):
        self.gstate = gstate
        self.reversed = reversed

    def __call__(self, gstate=GameState(), reversed=False):
        self.gstate = gstate
        self.reversed = reversed

    @property
    def is_upside(self):
        return not self.reversed

    def find_best_move(self):
        return GamePointer(), GameState()

    # def move(self):
    #     best_state = self.find_best_move()[1]
    #     self.gstate(best_state)

    # def perform(self, pointer: GamePointer):
    #     self.gstate.to_next_state(pointer)


class RandomAgent(Agent):
    def find_best_move(self):
        if self.gstate.no_more_moves(self.is_upside):
            self.gstate.scatter_stones(self.is_upside)
        moves = list(self.gstate.possible_move(self.is_upside))
        i = np.random.randint(len(moves))
        return moves[i], self.gstate.copy().to_next_state(moves[i].copy())


class GreedyAgent(Agent):
    def find_best_move(self):
        succersors = list(self.gstate.expand(self.is_upside))
        candidates = []
        if self.reversed:
            best_state = max(succersors, key=lambda x: x[1].player2_score)[1]
            best_score = best_state.player2_score
            candidates = [
                x for x in succersors if x[1].player2_score == best_score]
        else:
            best_state = max(succersors, key=lambda x: x[1].player1_score)[1]
            best_score = best_state.player1_score
            candidates = [
                x for x in succersors if x[1].player1_score == best_score]

        idx = np.random.randint(len(candidates))
        return candidates[idx]


class MinimaxAgent(Agent):
    def __init__(self, gstate=GameState(), reversed=False, dept=2):
        super().__init__(gstate, reversed)
        self.dept = dept

    def find_best_move(self):
        def minimax(gstate: GameState, dept=2, maximize=True):
            if dept == 0 or gstate.is_end_state():
                if gstate.no_more_moves(maximize):
                    gstate.scatter_stones(maximize)
                return None, gstate, gstate.heuristic_score

            best_score = 0
            best_move = None
            best_state = None
            candidates = []
            if maximize:
                best_score = INT_MIN
                for move, state in gstate.expand(maximize):
                    score = minimax(state, dept-1, not maximize)[-1]
                    if best_score < score:
                        best_score = score
                        best_move = move
                        best_state = state
                        if score == INT_MAX - 1:
                            break
                    elif score == best_score:
                        candidates.append((move, state, score))

            else:
                best_score = INT_MAX
                for move, state in gstate.expand(maximize):
                    score = minimax(state, dept-1, not maximize)[-1]
                    if best_score > score:
                        best_score = score
                        best_move = move
                        best_state = state
                        if score == INT_MIN + 1:
                            break
                    elif score == best_score:
                        candidates.append((move, state, score))

            if candidates:
                filtered = [x for x in candidates if x[-1] == best_score]
                filtered.append((best_move, best_state, best_score))
                idx = np.random.randint(len(filtered))
                best_move, best_state, best_score = filtered[idx]

            return best_move, best_state, best_score

        return minimax(self.gstate, self.dept, self.is_upside)[:2]


class AlphaBetaAgent(MinimaxAgent):
    def find_best_move(self):
        def minimax_alpha_beta(gstate: GameState, dept=2, maximize=True, alpha=INT_MIN, beta=INT_MAX):
            if dept == 0 or gstate.is_end_state():
                if gstate.no_more_moves(maximize):
                    gstate.scatter_stones(maximize)
                return None, gstate, gstate.heuristic_score

            best_score = 0
            best_move = None
            best_state = None
            candidates = []
            if maximize:
                best_score = INT_MIN
                for move, state in gstate.expand(maximize):
                    score = minimax_alpha_beta(
                        state, dept-1, not maximize, alpha, beta)[-1]
                    if best_score < score:
                        best_score = score
                        best_move = move
                        best_state = state
                        alpha = max(alpha, score)
                        if alpha > beta:
                            break
                    elif score == best_score:
                        candidates.append((move, state, score))
            else:
                best_score = INT_MAX
                for move, state in gstate.expand(maximize):
                    score = minimax_alpha_beta(
                        state, dept-1, not maximize, alpha, beta)[-1]
                    if best_score > score:
                        best_score = score
                        best_move = move
                        best_state = state
                        beta = min(beta, score)
                        if beta < alpha:
                            break
                    elif score == best_score:
                        candidates.append((move, state, score))

            if candidates:
                filtered = [x for x in candidates if x[-1] == best_score]
                filtered.append((best_move, best_state, best_score))
                idx = np.random.randint(len(filtered))
                best_move, best_state, best_score = filtered[idx]

            return best_move, best_state, best_score

        return minimax_alpha_beta(self.gstate, self.dept, self.is_upside)[:2]
