import math

from nim import Nim, Nimply
from collections import namedtuple

Minimax = namedtuple("Minimax", "row, n, score")

state_cache_min = dict()
state_cache_max = dict()


def get_moves(state: Nim) -> list:
    return list([Nimply(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k])


def minimax(state, depth, maximizing, prev_move: Nimply):
    minimax.counter += 1
    score = evaluate_position(state, maximizing)
    if depth == 0:  # if out of depth: make up some heuristic
        return Minimax(prev_move.row, prev_move.num_objects, 1)
    if score > 0:  # I win
        return Minimax(prev_move.row, prev_move.num_objects, score)
    if score < 0:  # opponent wins
        return Minimax(prev_move.row, prev_move.num_objects, score)

    all_moves = get_moves(state)
    if not maximizing:  # opponent's turn
        score = math.inf
        if str(state) not in state_cache_min.keys():
            for move in all_moves:
                state.nimming(move)  # make move
                # add to state cache
                result = minimax(state, depth - 1, True, move)
                best_move = Minimax(move.row, move.num_objects, score)
                best_move = min(best_move, result, key=lambda l: l.score)
                state_cache_min[str(state)] = best_move
                state.unnim(move)
        else:
            # state in cache already -- retrieve
            best_move = state_cache_min[str(state)]

    else:  # my turn
        score = -math.inf
        if str(state) not in state_cache_max.keys():
            for move in all_moves:
                state.nimming(move)  # make move
                # add to state cache
                result = minimax(state, depth - 1, False, move)
                best_move = Minimax(move.row, move.num_objects, score)
                best_move = max(best_move, result, key=lambda l: l.score)
                state_cache_max[str(state)] = best_move
                state.unnim(move)
        else:
            # state in cache already -- retrieve
            best_move = state_cache_max[str(state)]
    return best_move


def alpha_beta(state, depth, maximizing, alpha, beta, prev_move: Nimply):
    alpha_beta.counter += 1
    score = evaluate_position(state, maximizing)
    if score != 0 or depth == 0:  # the game is over or depth = 0
        if depth == 0:  # if out of depth: make up some heuristic
            return Minimax(prev_move.row, prev_move.num_objects, 1)
        return Minimax(prev_move.row, prev_move.num_objects, score)

    all_moves = get_moves(state)
    if not maximizing:  # opponent's turn
        score = math.inf
        if str(state) not in state_cache_min.keys():
            for move in all_moves:
                state.nimming(move)  # make move
                result = alpha_beta(state, depth - 1, True, alpha, beta, move)
                best_move = Minimax(move.row, move.num_objects, score)
                best_move = min(best_move, result, key=lambda l: l.score)
                beta = min(beta, best_move.score)
                if beta >= best_move.score:
                    state_cache_min[str(state)] = best_move
                state.unnim(move)
                if beta <= alpha:
                    break
        else:
            best_move = state_cache_min[str(state)]
    else:
        score = -math.inf
        if str(state) not in state_cache_max.keys():
            for move in all_moves:
                state.nimming(move)  # make move
                result = alpha_beta(state, depth - 1, False, alpha, beta, move)
                best_move = Minimax(move.row, move.num_objects, score)
                best_move = max(best_move, result, key=lambda l: l.score)
                alpha = max(alpha, best_move.score)
                if alpha <= best_move.score:
                    state_cache_max[str(state)] = best_move
                state.unnim(move)
                if beta <= alpha:
                    break
        else:
            best_move = state_cache_max[str(state)]
    return best_move


def make_best_move(state: Nim) -> Nimply:
    max_depth = math.inf
    minimax.counter = 0
    result = minimax(state, max_depth, True, Nimply(0, 0))
    best_move = Nimply(result.row, result.n)
    return best_move


def make_best_move_ab(state: Nim) -> Nimply:
    max_depth = math.inf
    alpha_beta.counter = 0
    a = -math.inf
    b = math.inf
    result = alpha_beta(state, max_depth, True, a, b, Nimply(0, 0))
    best_move = Nimply(result.row, result.n)
    return best_move


def evaluate_position(state: Nim, my_turn) -> int:
    if state:  # the game is not over
        return 0
    if my_turn:  # the game is over and the opponent won (made last move)
        return -1
    return 1  # the game is over and I won

