import random
from EA import EvolutionaryModel

def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]


if __name__ == "__main__":
    Ns = [5, 10, 20, 100, 500, 1000]
    for N in Ns:
        ls = problem(N, 42)
        print(f"working on N={N}...")
        ea = EvolutionaryModel(ls, N=N, pop_size=150, offspring_size=100, epochs=1000, fitness_evaluations_threshold=50000, mutation_chance=0.2)
        ea.simulate()
        solution = ea.get_solution()
        print(
            f"Solution for N={N}: w={sum(len(_) for _ in solution)} (bloat={(sum(len(_) for _ in solution) - N) / N * 100:.0f}%)"
        )
        if N <= 20:
            print(f"{solution}")
        print("---------")

