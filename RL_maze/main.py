# Credit: https://towardsdatascience.com/hands-on-introduction-to-reinforcement-learning-in-python-da07f7aaca88

import numpy as np
from environment import Maze
from agent import Agent

if __name__ == '__main__':
    m = 6
    n = 6
    maze = Maze(m, n)
    maze.generate_standard_maze()
    generated_maze = maze.maze

    robot = Agent(maze.maze, alpha=0.07, random_factor=0.25)
    maze.print_maze()
    num_iterations = 5000
    for i in range(num_iterations):
        if i % 1000 == 0:
            print("iterations:", i)

        maze = Maze(m, n, given_maze=np.copy(generated_maze))  # reinitialize the maze
        while not maze.is_game_over():
            state, _ = maze.get_state_and_reward()  # get the current state
            action = robot.choose_action(state, maze.allowed_states[state])  # choose an action (explore or exploit)
            maze.update_maze(action)  # update the maze according to the action
            state, reward = maze.get_state_and_reward()  # get the new state and reward
            robot.update_state_history(state, reward)  # update the robot memory with state and reward
            if maze.steps > 1000:
                # end the robot if it takes too long to find the goal
                maze.robot_position = (5, 5)
        if i < num_iterations - 1:
            robot.learn()  # robot should learn after every episode

    print("iterations:", num_iterations)
    print()
    print(f"Number of steps to reach the end: {maze.steps}")
    print("Solution:")
    maze.trace_path(robot.state_history)
    maze.print_maze()

