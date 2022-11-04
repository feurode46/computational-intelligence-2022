# Lab 2: Set Covering with Evolutionary Algorithms

## Task

Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$,
determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$
such that each number between $0$ and $N-1$ appears in at least one list

$$\\forall n \\in [0, N-1] \\ \\exists i : n \\in L_{s_i}$$

and that the total numbers of elements in all $L_{s_i}$ is minimum.
