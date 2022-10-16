# Lab 1: Set Covering

## Task

Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$,
determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$
such that each number between $0$ and $N-1$ appears in at least one list

$$\\forall n \\in [0, N-1] \\ \\exists i : n \\in L_{s_i}$$

and that the total numbers of elements in all $L_{s_i}$ is minimum.

## 1st version using simple Dijkstra's algorithm:

This algorithm uses a frontier in which the state with the lowest cost (total length of lists) is extracted first.
The states are inserted in the frontier in an ordered way based on cost.
To map the costs to the states, a hash is generated for each new state and a dictionary is kept for the associations. Then, a hash-to-cost dictionary is used to effectively have a list of costs indexed by their state.
The frontier is a simple list of state-cost pairs (two-element lists).

Below is the solution using a simple priority queue based on lowest cost for the frontier:

(full solution can be viewed in the file `raw_output_1st_ver.txt`)

    Solution for N=5: w=5 (bloat=0%)
    Solution for N=10: w=13 (bloat=30%)
    Solution for N=20: w=46 (bloat=130%)
    Solution for N=30: w=70 (bloat=133%)
    Solution for N=50: w=137 (bloat=174%)
    Solution for N=100: w=332 (bloat=232%)

The search function was based on professor's Squillero's template from _Lecture 02 - Searching for paths_.
