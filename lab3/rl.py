from typing import Callable

from nim import Nim, Nimply
import numpy as np


class RLAgent:

    def __init__(self, alpha=0.15, random_factor=0.2):
        self.state_history = []  # state+action, reward
        self.alpha = alpha
        self.random_factor = random_factor
        # start the rewards table
        self.G = {}
        self.known_states = {}

    def give_reward(self, state: Nim):
        if not state:  # we won
            return 1
        return 0

    def give_negative_reward(self):
        return -1

    def update_state_history(self, state_key: str, move: Nimply, reward: int):
        self.state_history.append(((state_key, move), reward))

    def learn(self):
        target = 1  # we know the "ideal" reward
        a = self.alpha
        # print(self.state_history)
        for state, reward in reversed(self.state_history[:-1]):
            if state in self.G.keys():
                self.G[state] = self.G[state] + a * (target - self.G[state])

        self.state_history = []  # reset the state_history
        self.random_factor -= 10e-5  # decrease random_factor

    def choose_action(self, state: Nim):
        if str(state) not in self.known_states.keys():
            allowed_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1) if state.k is None or o <= state.k]
            self.known_states[str(state)] = list(allowed_moves)
        else:
            allowed_moves = self.known_states[str(state)]

        next_move = None
        n = np.random.random()
        if n < self.random_factor:
            next_move_idx = np.random.randint(len(allowed_moves))
            next_move = allowed_moves[next_move_idx]
        else:
            max_g = -10e15  # some tiny number
            for action in allowed_moves:
                new_state_str = str(state)
                if (new_state_str, action) not in self.G.keys():
                    next_move = action
                    self.G[(new_state_str, action)] = np.random.uniform(high=1.0, low=0.1)
                elif self.G[(new_state_str, action)] >= max_g:
                    next_move = action
                    max_g = self.G[(new_state_str, action)]

        return next_move

    def rl_strategy(self, state: Nim):
        return self.choose_action(state)


def train(size: int, k, other_strategy: Callable, alpha=0.25, random_factor=0.1, iters=1000):
    nim = Nim(size, k)
    agent = RLAgent(alpha=alpha, random_factor=random_factor)

    for i in range(iters):
        # if i % (iters/10) == 0:
        #     print(i)
        for first_player in (True, False):  # train both starting as first and second
            player = 0
            while nim:
                if first_player:
                    last_state, last_action = make_move(agent, nim)
                if nim:
                    other_strategy(nim)  # other player
                if not first_player:
                    last_state, last_action = make_move(agent, nim)
                player = 1 - player
            # at the end of the game: if agent lost assign -1
            if (first_player and player == 0) or (not first_player and player == 1):
                # agent lost
                agent.update_state_history(last_state, last_action, agent.give_negative_reward())
            agent.learn()
            nim = Nim(size, k)

    return agent  # G has been learned


def make_move(agent: RLAgent, state: Nim):
    action = agent.choose_action(state)  # choose an action (explore or exploit)
    old_state_str = str(state)
    state.nimming(action)
    reward = agent.give_reward(state)
    agent.update_state_history(old_state_str, action, reward)  # update agent's memory

    return old_state_str, action

