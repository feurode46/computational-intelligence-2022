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

This strategy, albeit being extremely simple and deduced by playing some games by myself, is able to beat an opponent using random moves around 90-95% of the time.

## Task 3.2 - Evolved rules
