# CI Lab1

import random
import lablib as ll
import hashlib
import logging


def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


def goal_test(state, N):
    all_numbers = list(range(N))
    for sl in state:
        for n in all_numbers:
            if n in sl:
                all_numbers.remove(n)
                if len(all_numbers) == 0:
                    break
    return len(all_numbers) == 0


def possible_actions(state, P):
    list_of_actions = list()
    for el in P:
        if el not in state:
            list_of_actions.append(el)
    return list_of_actions


def result(state, action):
    new_state = state.copy()
    new_state.append(action)
    return new_state


def cost_function(state):
    if len(state) == 0:
        return 0
    return sum(len(_) for _ in state)


def unit_cost(action):
    return len(action)


def priority_function(state):
    return cost_function(state)


def state_hash(state):
    # calculate the hash of a state by hashing its string representation
    h = hashlib.md5(str(state).encode())
    return h.hexdigest()


def search(N, P):  # initial state: [], goal state: one that contains all numbers
    state = list()
    state_cost = dict()
    frontier = ll.Frontier()  # priority queue
    state_cost[state_hash(state)] = 0
    FLIMIT = 1000/N

    while state is not None and not goal_test(state, N):
        count = 0  # limit number of actions
        for a in possible_actions(state, P):
            new_state = result(state, a)
            cost = unit_cost(a)  # unit cost of action a
            if state_hash(new_state) not in state_cost and new_state not in frontier:
                # update total cost for new state
                state_cost[state_hash(new_state)] = state_cost[state_hash(state)] + cost
                # put in frontier
                # limit length of frontier
                if frontier.length < FLIMIT:
                    frontier.push(new_state, p=priority_function(new_state))

            elif new_state in frontier and state_cost[state_hash(new_state)] > state_cost[state_hash(state)] + cost:
                # update node and solution
                state_cost[state_hash(new_state)] = state_cost[state_hash(state)] + cost
        if frontier:
            state = frontier.pop()
        else:
            state = None
    print(f"N={N}, visited: {len(state_cost)}")
    return state


if __name__ == "__main__":
    Ns = [5, 10, 20, 30, 50, 100, 500, 1000]
    for N in Ns:
        ls = problem(N, 42)
        all_lists = sorted(ls, key=lambda l: len(l))
        solution = search(N, all_lists)
        print(
            f"Solution for N={N}: w={sum(len(_) for _ in solution)} (bloat={(sum(len(_) for _ in solution) - N) / N * 100:.0f}%)"
        )
        print(f"{solution}")
        print("---------")

