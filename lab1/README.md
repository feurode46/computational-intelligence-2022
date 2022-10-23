# Lab 1: Set Covering

## Task

Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$,
determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$
such that each number between $0$ and $N-1$ appears in at least one list

$$\\forall n \\in [0, N-1] \\ \\exists i : n \\in L_{s_i}$$

and that the total numbers of elements in all $L_{s_i}$ is minimum.

## 1st version using simple ~~Dijkstra's~~ algorithm:

This algorithm uses a frontier in which the state with the lowest cost (total length of lists) is extracted first.
The states are inserted in the frontier in an ordered way based on cost.
To map the costs to the states, a hash is generated for each new state and a dictionary is kept for the associations. Then, a hash-to-cost dictionary is used to effectively have a list of costs indexed by their state.
The frontier is a simple list of state-cost pairs (two-element lists).

Below is the solution using a simple priority queue based on lowest cost for the frontier:

(full solution can be viewed in the file `raw_output_1st_ver.txt`)

    Solution for N=5: w=5 (bloat=0%), nodes=36
    Solution for N=10: w=13 (bloat=30%), nodes=472
    Solution for N=20: w=46 (bloat=130%), nodes=841
    Solution for N=100: w=332 (bloat=232%), nodes=68546

The search function was based on professor's Squillero's template from _Lecture 02 - Searching for paths_.

## 2nd ver. - Beam search with improvements and reflections on peer feedback

I made some fundamental changes to the program structure.

Namely, I made the solution and the state one and the same, implemented the frontier with PriorityQueue() found in gx_utils by prof. Squillero, found a better way to hash states, and generally refactored some code.

The hash for a state is now calculated from its string representation, and it's not kept in a dictionary anymore. Instead, the state_cost dictionary maps the state's hash (calculated on the fly) to its cost.

I also limited the frontier's size, effectively implementing a beam search. This limit is not fixed for all values of N, but instead changes with a ratio of 1000/N, so that solutions can be found in a timely manner even for big sizes. Further optimization will eventually remove the need for limiting the frontier.

This new solutions is much faster than the last one, able to generate at least _some_ results for higher values of N, up to 1000.

Here are the results: 

    N=5, visited: 2423
    Solution for N=5: w=5 (bloat=0%)
    ----
    N=10, visited: 29810
    Solution for N=10: w=18 (bloat=80%)
    ----
    N=20, visited: 17957
    Solution for N=20: w=58 (bloat=190%)
    ----
    N=30, visited: 48117
    Solution for N=30: w=77 (bloat=157%)
    ----
    N=50, visited: 68594
    Solution for N=50: w=156 (bloat=212%)
    ----
    N=100, visited: 127838
    Solution for N=100: w=575 (bloat=475%)
    ----
    N=500, visited: 109420
    Solution for N=500: w=2804 (bloat=461%)
    ----
    N=1000, visited: 151138
    Solution for N=1000: w=7570 (bloat=657%)
    
This search performs generally worse than the last one, but is at least able to produce solutions for higher values of N. Further work is needed, but the program structure and size is much better now.
