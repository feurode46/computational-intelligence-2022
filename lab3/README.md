# Lab 3: Policy Search
## Task
    
Write agents able to play [*Nim*](https://en.wikipedia.org/wiki/Nim), with an arbitrary number of rows and an upper bound $k$ on the number of objects that can be removed in a turn (a.k.a., *subtraction game*).

The player **taking the last object wins**.

* Task3.1: An agent using fixed rules based on *nim-sum* (i.e., an *expert system*)
* Task3.2: An agent using evolved rules
* Task3.3: An agent using minmax
* Task3.4: An agent using reinforcement learning

## Solution

## Task 3.1 - Fixed rules

As the main task (implementing nim-sum) had already been solved by the professor, I opted to come up with my own expert system. The strategy operates based on the following principle:

Imagine a finished game of Nim. There is only one row that can be picked up by the last move (suppose only one object.)

    |
    
Which means that your opponent's turn looked probably like this:

    |
    |

So the goal of the strategy is to make your opponent end up in that state.

The strategy is based on a decision tree, in which if the number of active rows in a given turn is even, then pick the first one and remove all excluding one object (inspired by the situation above). If the active rows are in odd number, then take all of the objects in the first available row (again, to hopefully bring the opponent in the above state). This really only takes into consideration the last few phases of the game. 

This strategy, albeit being extremely simple and deduced by playing some games by myself, is able to beat an opponent using random moves around 95% of the time, and it seems to scale quite well with increasing game size.

When $k$ is introduced, my strategy is able to beat the optimal strategy with a winrate that increases with a lower k. With $k=3$ it is able to win around 20% of the time.

## Task 3.2 - Evolved rules

The evolved agent is based on a fixed decision tree structure, with probabilities of taking certain actions under certain conditions. (Again, ignoring the existence of nim-sum).

The chosen conditions are:

- Even number of active rows (active: >=1 object)
- Odd number of active rows
- There are rows with more that one object
- There are no rows with more than one object (forced move: take one object)

And the possible actions are:

- Take all objects in a row
- Take all but one object in a row

The genome consists of two alleles, which correspond to probabilities $(0 \leq p \leq 1)$ of, respectively:

- Taking all objects in the first available row when the number of active rows is even
- Taking all objects in the first available row when the number of active rows is odd

The crossover chosen is a one-point crossover, while the fitness is the winning rate of the strategy against a random one over 100 games. A mutation increases or decreases a random probability by 0.05.

The results of training the algorithm with a population size of 150, an offspring size of 100, 98 generations, with 10,000 fitness evaluations were a genome consisting of $(0.002, 0.991)$, which shows that the algorithm never takes all objects when there is an even number of rows (opting for leaving one behind) and always takes all when there is an odd number of rows.

This shows me that out of the possible actions under the specified conditions, the ones I had chosen by myself were the highest-winning ones, and the algorithm came to the same conclusion. The strategy achieves a 95% winrate against a random chance player. 

Interestingly, by pitting my strategy against the evolved one, whoever starts first loses, because they are not able to reverse the even-odd row situation.

When $k$ is introduced, whoever starts first has a small chance of winning.
