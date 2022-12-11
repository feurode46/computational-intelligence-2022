from nim import Nim, Nimply
from typing import Callable
import logging
import random
from copy import deepcopy
from itertools import accumulate
from operator import xor
from EA import EvolutionaryModel
import minimax as mm
import rl

NUM_MATCHES = 1000
NIM_SIZE = 5
k = None


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["active_rows"] = list([o for o in enumerate(state.rows) if o[1] > 0])
    cooked["n_active_rows"] = len(cooked["active_rows"])
    cooked["rows_2_or_more"] = list([o for o in cooked["active_rows"] if o[1] > 1])
    cooked["nim_sum"] = nim_sum(state)

    brute_force = list()
    for m in cooked["possible_moves"]:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    cooked["brute_force"] = brute_force

    return cooked


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.rows, xor)
    return result


def optimal_strategy(state: Nim) -> Nimply:
    data = cook_status(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


def random_strategy(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    if k is not None:
        num_objects = random.randint(1, min(k, state.rows[row]))
    else:
        num_objects = random.randint(1, state.rows[row])

    return Nimply(row, num_objects)


def my_strategy(state: Nim) -> Nimply:
    # odd number of active rows: take whole row (more than 1 element if possible)
    cooked_state = cook_status(state)

    # default: take whole 1st row
    row = cooked_state["active_rows"][0][0]        # row index
    n_objects = cooked_state["active_rows"][0][1]  # row value

    if len(cooked_state["rows_2_or_more"]) > 0:
        row = cooked_state["rows_2_or_more"][0][0]
        if cooked_state["n_active_rows"] % 2 == 1:
            if k is not None:
                n_objects = min(k, cooked_state["rows_2_or_more"][0][1])
            else:
                n_objects = cooked_state["rows_2_or_more"][0][1]
        else:
            if k is not None:
                n_objects = min(k, cooked_state["rows_2_or_more"][0][1] - 1)
            else:
                n_objects = cooked_state["rows_2_or_more"][0][1] - 1

    return Nimply(row, n_objects)


def minimax_strategy(state: Nim) -> Nimply:
    return mm.make_best_move(state)  # my turn


def alpha_beta_strategy(state: Nim) -> Nimply:
    return mm.make_best_move_ab(state)  # my turn


def evaluate(strategy1: Callable, strategy2: Callable) -> float:
    opponent = (strategy1, strategy2)
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE, k)
        player = 0
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def evaluate_EA(ea_: EvolutionaryModel, strategy: Callable, reverse=False):
    # win rate over 100 matches
    won = 0
    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            if reverse:
                if player == 1:
                    ply = ea_.evolved_strategy(ea_.best_genome(), nim)
                else:
                    ply = strategy(nim)
            else:
                if player == 0:
                    ply = ea_.evolved_strategy(ea_.best_genome(), nim)
                else:
                    ply = strategy(nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def sample_game(n, strategy1: Callable, strategy2: Callable) -> None:
    strategy = (strategy1, strategy2)
    nim = Nim(n)
    print(f"status: Initial board  -> {nim}")
    print(f"Player 1: {strategy[0].__name__}")
    print(f"Player 2: {strategy[1].__name__}")
    player = 0
    while nim:
        ply = strategy[player](nim)
        nim.nimming(ply)
        print(f"status: After player {player + 1} -> {nim}")
        player = 1 - player
    winner = 1 - player
    print(f"status: Player {strategy[winner].__name__} won!")


def test_evolved_strategy(ea_: EvolutionaryModel):
    print("Training evolutionary algorithm...")
    ea_.simulate()
    best = ea_.best_genome()
    ea_strategies = [
        my_strategy,
        random_strategy,
        optimal_strategy
    ]
    print("Evolved strategy: ")
    print()
    for s in ea_strategies:
        print(f"{ea_.evolved_strategy.__name__} vs. {s.__name__}: winrate {evaluate_EA(ea_, s) * 100}%")
        print(f"{s.__name__} vs. {ea_.evolved_strategy.__name__}: winrate {evaluate_EA(ea_, s, reverse=True) * 100}%")
    print()


def test_fixed_strategy():
    print("Fixed strategy: ")
    print()

    strategy_pairs = [
        (my_strategy, random_strategy),
        (my_strategy, optimal_strategy)
    ]

    for p in strategy_pairs:
        print(f"{p[0].__name__} vs. {p[1].__name__}: winrate {evaluate(p[0], p[1]) * 100}%")
        print(f"{p[1].__name__} vs. {p[0].__name__}: winrate {evaluate(p[1], p[0]) * 100}%")
    print()


def test_minimax_strategy():
    print("Minimax strategy (might take a while): ")
    print()
    strategy_pairs = [
        (minimax_strategy, random_strategy),
        (minimax_strategy, optimal_strategy),
        (minimax_strategy, my_strategy),
    ]

    for p in strategy_pairs:
        print(f"{p[0].__name__} vs. {p[1].__name__}: winrate {evaluate(p[0], p[1]) * 100}%")
        print(f"{p[1].__name__} vs. {p[0].__name__}: winrate {evaluate(p[1], p[0]) * 100}%")

    print()


def test_alpha_beta_strategy():
    print("Minimax strategy with alpha-beta pruning:")
    print()
    strategy_pairs = [
        (alpha_beta_strategy, random_strategy),
        (alpha_beta_strategy, optimal_strategy),
        (alpha_beta_strategy, my_strategy),
    ]

    for p in strategy_pairs:
        print(f"{p[0].__name__} vs. {p[1].__name__}: winrate {evaluate(p[0], p[1]) * 100}%")
        print(f"{p[1].__name__} vs. {p[0].__name__}: winrate {evaluate(p[1], p[0]) * 100}%")

    print()


def test_rl_strategy():
    best_wr = 0
    best_agent = None
    num_iters = 5
    print(f"training RL agent... ({num_iters} iterations)")
    for i in range(num_iters):
        print(f"iteration: {i+1}/{num_iters}")
        if best_agent is None:
            rl_agent = rl.train(NIM_SIZE, k, random_strategy, alpha=0.4, random_factor=0.01, iters=5000)
        else:
            rl_agent = rl.train(NIM_SIZE, k, best_agent.rl_strategy, alpha=0.4, random_factor=0.01, iters=5000)

        wr = max(evaluate(rl_agent.rl_strategy, random_strategy), 1 - evaluate(random_strategy, rl_agent.rl_strategy))
        # print("winrate: ", wr)
        if wr >= best_wr:
            best_agent = rl_agent
            best_wr = wr

    print("Reinforcement learning strategy: ")
    print()
    strategy_pairs = [
        (best_agent.rl_strategy, random_strategy),
        (best_agent.rl_strategy, optimal_strategy),
        (best_agent.rl_strategy, my_strategy),
    ]

    for p in strategy_pairs:
        print(f"{p[0].__name__} vs. {p[1].__name__}: winrate {evaluate(p[0], p[1]) * 100}%")
        print(f"{p[1].__name__} vs. {p[0].__name__}: winrate {evaluate(p[1], p[0]) * 100}%")

    print()


if __name__ == "__main__":
    print(f"--- Size={NIM_SIZE}, games={NUM_MATCHES} ---")
    if k is not None:
        print(f"k={k}")
    ea = EvolutionaryModel(NIM_SIZE, k, 150, 100, 100, 10000, 0.2, 100)
    test_evolved_strategy(ea)
    test_fixed_strategy()
    # test_minimax_strategy()  # uncomment to use minimax strategy without pruning, better results but it's slow
    test_alpha_beta_strategy()
    test_rl_strategy()

    print("All done!")






