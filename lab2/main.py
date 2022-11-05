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
        random.shuffle(ls)
        # print(ls)
        print(f"working on N={N}...")
        ea = EvolutionaryModel(ls, pop_size=100, offspring_size=2, epochs=10000)
        # print(ea.population, sep="\n")
        ea.simulate()
        solution = ea.converted_solution()
        print(
            f"Solution for N={N}: w={sum(len(_) for _ in solution)} (bloat={(sum(len(_) for _ in solution) - N) / N * 100:.0f}%)"
        )
        print(f"{solution}")
        print("---------")

