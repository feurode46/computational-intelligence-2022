# Lab 2: Set Covering with Evolutionary Algorithms

## Task

Given a number $N$ and some lists of integers $P = (L_0, L_1, L_2, ..., L_n)$,
determine, if possible, $S = (L_{s_0}, L_{s_1}, L_{s_2}, ..., L_{s_n})$
such that each number between $0$ and $N-1$ appears in at least one list

$$\\forall n \\in [0, N-1] \\ \\exists i : n \\in L_{s_i}$$

and that the total numbers of elements in all $L_{s_i}$ is minimum.

## Solution

As for the representation, I decided to go with a binary one: the genome is as long as the list of lists ($P$) and each gene denotes whether a list is chosen (1) or not (0). The initial population is chosen at random, so each list has a 50/50 chance of being included in a solution. A weighted approach was also tried, which skewed towards shorter or longer lists for the initial population selection, but ultimately it didn't make any difference.

The fitness function is a tuple consisting of:

1) the number of digits included in the solution (our objective function) - must be maximized
2) The total length of the solution - must be minimized

The crossover function is a gene-by-gene crossover, choosing at random for each gene which parent's to keep. A mutation function was introduced as well, which just flips two bits in the genome. I chose a mutation rate of 20%, so an offspring is either born by two parents with 80% chance, or a mutation of a random existing individual with 20% chance.

I decided to go with a steady-state approach, because it seemed to yield better results in initial runs. This means that the parents are not replaced every generation, but instead the individuals with highest fitness are kept, regardless of age.

Here are my best results, using a population size of 150, an offspring size of 100, and a total of 100,000 evaluations:


|   N  | Weight | Bloat |
|:----:|:------:|:-----:|
| 5    | 5      | 0%    |
| 10   | 10     | 0%    |
| 20   | 24     | 20%   |
| 100  | 199    | 99%   |
| 500  | 3902   | 680%  |
| 1000 | 66834  | 6583% |


Another run was performed with a $(\mu, \lambda)$ evolution strategy, with $\mu=150$ and $\lambda=1000$ and it provided better results for N=100 and N=500, however the solution for N=1000 was much worse so I decided not to make it the final version of the code, and I'll just include the results below.

### Run with $(150, 1000)$-ES
|   N  | Weight | Bloat |
|:----:|:------:|:-----:|
| 5    | 5      | 0%    |
| 10   | 10     | 0%    |
| 20   | 27     | 35%   |
| 100  | 186    | 86%   |
| 500  | 2518   | 404%  |
| 1000 | 89272  | 8827% |

In the end I wasn't able to understand why it couldn't find a good solution for N=1000 and up, having tried different crossover strategies, fitness functions and population and offspring sizes. I will keep adding to this to get to the bottom of it.
