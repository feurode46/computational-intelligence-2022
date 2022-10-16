# CI Lab1

import random
import logging


def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


def goal_test(state, N):
    goal_state = list(range(N));
    return sorted(state) == goal_state


def possible_actions(state, P, solution):
    list_of_actions = list()
    for el in P:
        if el not in solution and el not in list_of_actions:
            for n in el:
                if n not in state:
                    list_of_actions.append(el)
    return list_of_actions


def result(state, action, solution):  # generate state from solution instead of updating
    new_state = list()
    new_solution = solution.copy()
    new_solution.append(action.copy())
    for el in new_solution:
        for n in el:
            if n not in new_state:
                new_state.append(n)
    return [new_state, new_solution]


def cost_function(solution):
    if len(solution) == 0:
        return float('inf')
    return sum(len(_) for _ in solution)


def add_to_frontier(frontier, state, cost, algo="dijkstra"):
    to_add = list([state.copy(), cost])
    if len(frontier) == 0:
        frontier.insert(0, to_add)
    else:
        if algo == "dijkstra":
            # dumb dijkstra algorithm
            inserted = False
            for i in range(len(frontier)):
                if cost < frontier[i][1]:
                    frontier.insert(i, to_add)
                    inserted = True
            if not inserted:
                frontier.append(to_add)


def is_state_in_frontier(frontier, state):
    for el in frontier:
        if el[0] == state:
            return True
    return False


def add_state_cost(state_hashes, state_cost, state, cost):
    # generate hash
    name = random.getrandbits(128)
    state_hashes[name] = state.copy()
    state_cost[name] = cost


def get_state_hash(state_hashes, state):
    for h in state_hashes.keys():
        if state == state_hashes[h]:
            return h
    return None


def get_state_cost(state_hashes, state_cost, state):
    for h in state_hashes.keys():
        if state == state_hashes[h]:
            return state_cost[h]
    return None


def update_state_cost(state_hashes, state_cost, state, cost):
    for h in state_hashes.keys():
        if state == state_hashes[h]:
            state_cost[h] = cost


def search(state, N, P):  # initial state: [], goal state: [0, 1, 2...N-1]
    solution = list()
    state_hashes = dict()  # associations hash : state
    state_cost = dict()  # associations state_hash : cost
    frontier = list()  # list of [state, cost] pairs

    while state is not None and not goal_test(state, N):
        for a in possible_actions(state, P, solution):
            [new_state, new_solution] = result(state, a, solution)
            if get_state_hash(state_hashes, new_state) is None and not is_state_in_frontier(frontier, new_state):
                add_state_cost(state_hashes, state_cost, new_state, cost_function(new_solution))
                add_to_frontier(frontier, new_state, get_state_cost(state_hashes, state_cost, new_state))
                # update solution
                solution = new_solution.copy()
            elif is_state_in_frontier(frontier, new_state) and cost_function(new_solution) < get_state_cost(
                    state_hashes, state_cost, new_state):
                # update node and solution
                update_state_cost(state_hashes, state_cost, new_state, cost_function(new_solution))
                solution = new_solution.copy()
        if len(frontier) > 0:
            state = frontier.pop(0)[0]
        else:
            state = None
    return solution


if __name__ == "__main__":
    Ns = [5, 10, 20, 30, 50, 100]
    for N in Ns:
        ls = problem(N, 42)
        all_lists = sorted(ls, key=lambda l: len(l))
        solution = search(list(), 5, all_lists)
        print(
            f"Solution for N={N}: w={sum(len(_) for _ in solution)} (bloat={(sum(len(_) for _ in solution) - N) / N * 100:.0f}%)"
        )
        print(f"{solution}")

