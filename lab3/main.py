from nim import Nim, Nimply
from typing import Callable
import logging
import random
from copy import deepcopy
from itertools import accumulate
from operator import xor


NUM_MATCHES = 100
NIM_SIZE = 3


def cook_status(state: Nim) -> dict:
    # change this!
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
    # print(cooked_state)
    row = 0
    n_objects = 1
    if cooked_state["n_active_rows"] % 2 == 1:
        if len(cooked_state["rows_2_or_more"]) > 0:
            row = cooked_state["rows_2_or_more"][0][0]  # index of row
            n_objects = cooked_state["rows_2_or_more"][0][1]
        else:
            row = cooked_state["active_rows"][0][0]
            n_objects = 1
    else:
        # take all but one (temp. strategy)
        if len(cooked_state["rows_2_or_more"]) > 0:
            row = cooked_state["rows_2_or_more"][0][0]
            n_objects = cooked_state["rows_2_or_more"][0][1] - 1

    return Nimply(row, n_objects)


def evaluate(strategy: Callable) -> float:
    opponent = (strategy, random_strategy)
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


if __name__ == "__main__":
    mynim = Nim(3)
    # print(mynim.rows)
    print(f"Performance against random strategy, {NUM_MATCHES} games: {evaluate(my_strategy)*100}%")

