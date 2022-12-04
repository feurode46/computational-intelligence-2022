from nim import Nim, Nimply
from typing import Callable
import logging
import random
from copy import deepcopy
from itertools import accumulate
from operator import xor
from EA import EvolutionaryModel

NUM_MATCHES = 100
NIM_SIZE = 5


def cook_status(state: Nim) -> dict:
    cooked = dict()
    cooked["possible_moves"] = [
        (r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k
    ]
    cooked["active_rows"] = list([o for o in enumerate(state.rows) if o[1] > 0])
    cooked["n_active_rows"] = len(cooked["active_rows"])
    cooked["rows_2_or_more"] = list([o for o in cooked["active_rows"] if o[1] > 1])
    cooked["shortest_row"] = min((x for x in enumerate(state.rows) if x[1] > 0), key=lambda y: y[1])[0]
    cooked["longest_row"] = max((x for x in enumerate(state.rows)), key=lambda y: y[1])[0]
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
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


def my_strategy(state: Nim) -> Nimply:
    # odd number of active rows: take whole row (more than 1 element if possible)
    cooked_state = cook_status(state)

    # default: take whole 1st row
    row = cooked_state["active_rows"][0][0]        # row index
    n_objects = cooked_state["active_rows"][0][1]  # row value

    if len(cooked_state["rows_2_or_more"]) > 0:
        if cooked_state["n_active_rows"] % 2 == 1:
            row = cooked_state["rows_2_or_more"][0][0]
            n_objects = cooked_state["rows_2_or_more"][0][1]
        else:
            row = cooked_state["rows_2_or_more"][0][0]
            n_objects = cooked_state["rows_2_or_more"][0][1] - 1

    return Nimply(row, n_objects)


def evaluate(strategy1: Callable, strategy2: Callable) -> float:
    opponent = (strategy1, strategy2)
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def evaluate_EA(ea, strategy, reverse=False):

    # win rate over 100 matches
    won = 0
    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            if reverse:
                if player == 1:
                    ply = ea.evolved_strategy(ea.best_genome(), nim)
                else:
                    ply = strategy(nim)
            else:
                if player == 0:
                    ply = ea.evolved_strategy(ea.best_genome(), nim)
                else:
                    ply = strategy(nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def make_strategy(genome: dict) -> Callable:
    # change this!
    def evolvable(state: Nim) -> Nimply:
        data = cook_status(state)

        if random.random() < genome["p"]:
            ply = Nimply(data["shortest_row"], random.randint(1, state.rows[data["shortest_row"]]))
        else:
            ply = Nimply(data["longest_row"], random.randint(1, state.rows[data["longest_row"]]))

        return ply

    return evolvable


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


if __name__ == "__main__":
    print("Training evolutionary algorithm...")
    ea = EvolutionaryModel(NIM_SIZE, 150, 100, 100, 10000, 0.2, NUM_MATCHES)
    ea.simulate()
    best = ea.best_genome()
    print(best)
    ea_strategies = [
        my_strategy,
        random_strategy,
        optimal_strategy
    ]

    for s in ea_strategies:
        print(f"{ea.evolved_strategy.__name__} vs. {s.__name__} {evaluate_EA(ea, s) * 100}%")
        print(f"{s.__name__} vs. {ea.evolved_strategy.__name__} {evaluate_EA(ea, s, reverse=True) * 100}%")

    strategy_pairs = [
        (my_strategy, random_strategy),
        (my_strategy, optimal_strategy)
    ]
    # sample_game(NIM_SIZE, my_strategy, random_strategy)

    print(f"--- Size={NIM_SIZE}, games={NUM_MATCHES} ---")
    for p in strategy_pairs:
        print(f"{p[0].__name__} vs. {p[1].__name__} {evaluate(p[0], p[1]) * 100}%")
        print(f"{p[1].__name__} vs. {p[0].__name__} {evaluate(p[1], p[0]) * 100}%")




