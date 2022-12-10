from copy import deepcopy

from nim import Nim, Nimply
import numpy as np


class RLAgent:

    def __init__(self, initial_state: Nim, alpha=0.15, random_factor=0.2):
        self.state_history = []  # state+action, reward
        self.alpha = alpha
        self.random_factor = random_factor
        # start the rewards table
        self.G = {}
        self.allowed_states = self.construct_allowed_states(initial_state)
        self.init_reward()

    def init_reward(self):
        for i, state in enumerate(self.allowed_states):
            # print("I AND ROW:", i, state)
            for j, move in enumerate(self.allowed_states[state]):
                # print(j, move)
                self.G[(state, move)] = np.random.uniform(high=1.0, low=0.1)  # reward of action j in

    def construct_allowed_states(self, state):
        allowed_states = {}
        k = state.k
        if k is None:
            k = max(state.rows)
        if sum(state.rows) == 0:
            return allowed_states
        for i, row in enumerate(state.rows):
            for j in range(1, min(row+1, k+1)):
                # take j objects
                if str(state) not in allowed_states.keys():
                    allowed_states[str(state)] = list()
                move = Nimply(i, j)
                allowed_states[str(state)].append(move)
                state.nimming(move)
                entry = self.construct_allowed_states(state)
                allowed_states = {**allowed_states, **entry}
                state.unnim(move)
        return allowed_states

    def give_reward(self, state):
        if not state:  # we won
            return 1
        return 0

    def update_state_history(self, state: Nim, move: Nimply, reward):
        self.state_history.append(((str(state), move), reward))

    def learn(self):
        target = 1  # we know the "ideal" reward

        a = self.alpha
        # print(self.state_history)
        for state, reward in reversed(self.state_history[:-1]):
            self.G[state] = self.G[state] + a * (target - self.G[state])

        self.state_history = []  # reset the state_history
        self.random_factor -= 10e-5  # decrease random_factor

    def choose_action(self, state: Nim):
        allowed_moves = self.allowed_states[str(state)]
        # print("Allowed moves:", allowed_moves)
        next_move = None
        n = np.random.random()
        if n < self.random_factor:
            next_move_idx = np.random.randint(len(allowed_moves))
            next_move = allowed_moves[next_move_idx]
        else:
            max_g = -10e15  # some tiny random number
            for action in allowed_moves:
                new_state = deepcopy(state)
                if self.G[(str(new_state), action)] >= max_g:
                    next_move = action
                    max_g = self.G[(str(new_state), action)]

        return next_move

    def rl_strategy(self, state: Nim):
        return self.choose_action(state)


def train(size, k, alpha=0.25, random_factor=0.1, iters=1000):
    nim = Nim(size, k)
    agent = RLAgent(nim, alpha=alpha, random_factor=random_factor)

    for i in range(iters):
        if i % iters/10 == 0:
            print(i)

        while nim:
            action = agent.choose_action(nim)  # choose an action (explore or exploit)
            old_state = deepcopy(nim)
            nim.nimming(action)  # update the maze according to the action
            reward = agent.give_reward(nim)
            agent.update_state_history(old_state, action, reward)  # update the robot memory with state and reward

        agent.learn()  # robot should learn after every episode
        nim = Nim(size, k)

    return agent  # G has been learned


