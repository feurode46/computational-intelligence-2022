import random
from nim import Nim, Nimply


class EvolutionaryModel:

    def __init__(self, nim_size=5, k=None, pop_size=150, offspring_size=100, epochs=1000, fitness_evaluations_threshold=10000, mutation_chance = 0.2, num_matches=100):
        self.N = nim_size
        self.k = k
        self.num_matches = num_matches
        self.population_size = pop_size
        self.offspring_size = offspring_size
        self.epochs = epochs
        self.population = list()
        self.fitness_evaluations = 0
        self.fitness_evaluations_threshold = fitness_evaluations_threshold
        self.mutation_chance = mutation_chance

        # generate initial population
        for i in range(self.population_size):
            self.population.append(self.generate_individual())
            self.sort_population()

    def generate_individual(self):
        # for Nim: an individual is a (genome, fitness) tuple
        # genome: probability threshold of choosing all / all but one matches
        # from arbitrary row, in case of even or odd number of rows

        genome = tuple([random.random(), random.random()])
        fitness = self.fitness_eval(genome)
        individual = tuple([genome, fitness])
        # print(individual)
        return individual

    def cook_status(self, state: Nim) -> dict:
        cooked = dict()
        cooked["active_rows"] = list([o for o in enumerate(state.rows) if o[1] > 0])
        cooked["n_active_rows"] = len(cooked["active_rows"])
        cooked["rows_2_or_more"] = list([o for o in cooked["active_rows"] if o[1] > 1])

        return cooked

    def evolved_strategy(self, genome, state: Nim) -> Nimply:
        data = self.cook_status(state)
        probs = [random.random() for i in range(2)]
        if data["n_active_rows"] % 2 == 0:
            if len(data["rows_2_or_more"]) > 0:
                row = data["rows_2_or_more"][0][0]
                if probs[0] > genome[0]:
                    if self.k is not None:
                        n_objects = min(self.k, data["rows_2_or_more"][0][1])  # take all
                    else:
                        n_objects = data["rows_2_or_more"][0][1]  # take all
                else:
                    if self.k is not None:
                        n_objects = min(self.k, data["rows_2_or_more"][0][1] - 1)  # leave one
                    else:
                        n_objects = data["rows_2_or_more"][0][1] - 1
            else:
                # forced move: take one from arbitrary row
                row = data["active_rows"][0][0]
                n_objects = 1
        else:
            if len(data["rows_2_or_more"]) > 0:
                row = data["rows_2_or_more"][0][0]
                if probs[1] > genome[1]:
                    if self.k is not None:
                        n_objects = min(self.k, data["rows_2_or_more"][0][1])  # take all
                    else:
                        n_objects = data["rows_2_or_more"][0][1]  # take all
                else:
                    if self.k is not None:
                        n_objects = min(self.k, data["rows_2_or_more"][0][1] - 1)  # leave one
                    else:
                        n_objects = data["rows_2_or_more"][0][1] - 1
            else:
                # forced move: take one
                row = data["active_rows"][0][0]
                n_objects = 1

        return Nimply(row, n_objects)

    def random_strategy(self, state: Nim) -> Nimply:
        row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
        if self.k is not None:
            num_objects = min(self.k, random.randint(1, state.rows[row]))
        else:
            num_objects = random.randint(1, state.rows[row])

        return Nimply(row, num_objects)

    def fitness_eval(self, genome):
        # win rate over 100 matches
        self.fitness_evaluations += 1
        won = 0
        for m in range(self.num_matches):
            nim = Nim(self.N)
            player = 0
            while nim:
                if player == 0:
                    ply = self.evolved_strategy(genome, nim)
                else:
                    ply = self.random_strategy(nim)
                nim.nimming(ply)
                player = 1 - player
            if player == 1:
                won += 1
        return won / self.num_matches

    def select_parent(self, tournament_size=2):
        return max(random.choices(self.population, k=tournament_size), key=lambda i: i[1])

    def cross_over(self, g1, g2):
        return tuple([g1[0], g2[1]])

    def mutate(self, genome):
        # increment or decrement a random probability by 0.05
        r1 = random.random()
        r2 = random.random()
        p1 = genome[0]
        p2 = genome[1]
        if r1 > 0.5:
            if r2 > 0.5:
                p1 -= 0.05
                if p1 < 0:
                    p1 = 0
            else:
                p1 += 0.05
                if p1 > 1:
                    p1 = 1
        else:
            if r2 > 0.5:
                p2 -= 0.05
                if p2 < 0:
                    p2 = 0
            else:
                p2 += 0.05
                if p2 > 1:
                    p2 = 1
        new_genome = tuple([p1, p2])
        return new_genome

    def evolve(self):
        for i in range(self.offspring_size):
            if random.random() < self.mutation_chance:
                offspring_genome = self.mutate(random.choice(self.population)[0])
            else:
                p1 = self.select_parent()
                p2 = self.select_parent()
                offspring_genome = self.cross_over(p1[0], p2[0])
            self.population.append(tuple([offspring_genome, self.fitness_eval(offspring_genome)]))
        # then sort and trim
        self.sort_population()
        self.population = self.population[:self.population_size]

    def simulate(self):
        for i in range(self.epochs):
            self.evolve()
            if self.fitness_evaluations % (self.fitness_evaluations_threshold/10) == 0:
                print(f"{int(self.fitness_evaluations/self.fitness_evaluations_threshold*100)}%")
            if self.fitness_evaluations > self.fitness_evaluations_threshold:
                print(f"Maximum number of evaluations ({self.fitness_evaluations}) reached. Trained for {i} generations.")
                break
        print("100% Done!")

    def sort_population(self):
        self.population = sorted(self.population, key=lambda i: i[1], reverse=True)

    def best_genome(self):
        return self.population[0][0]
