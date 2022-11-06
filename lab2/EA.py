import random

class EvolutionaryModel:

    def __init__(self, problem, N=5, pop_size=150, offspring_size=100, epochs=1000, fitness_evaluations_threshold=10000, mutation_chance = 0.2):
        self.problem = problem
        self.N = N
        self.problem_size = len(self.problem)
        self.population_size = pop_size
        self.offspring_size = offspring_size
        self.epochs = epochs
        self.population = list()
        self.total_length = sum(len(i) for i in self.problem)
        self.fitness_evaluations = 0
        self.fitness_evaluations_threshold = fitness_evaluations_threshold
        self.mutation_chance = mutation_chance

        # generate initial population
        for i in range(self.population_size):
            self.population.append(self.generate_individual())
            self.sort_population()


    def generate_individual(self):
        genome = tuple([random.choice([0, 1]) for _ in range(self.problem_size)])
        fitness = self.fitness_eval(genome)
        individual = tuple([genome, fitness])
        return individual
    

    def fitness_eval(self, genome):
    # tuple with: 1) number of digits included, 2) number of total elements
    #                higher is better              lower is better
        all_values = list()
        for i in range(len(genome)):
            if genome[i] == 1:
                all_values.extend(self.problem[i])
        digit_range = list(range(self.N))
        count = 0
        for i in digit_range:
            if i in all_values:
                count += 1
        self.fitness_evaluations += 1
        return tuple([count, -len(all_values)]) # negative since we want the min
    
    def select_parent(self, tournament_size=2):
        return max(random.choices(self.population, k=tournament_size), key=lambda i: i[1])
    
    def cross_over(self, g1, g2):
        # gene-by-gene crossover
        g3 = list()
        g3.extend([random.choice([g1[i], g2[i]]) for i in range(self.problem_size)])
        return tuple(g3)

    def mutate(self, genome):
        # flip two random bits
        new_genome = list(genome)
        for i in range(2):
            idx = random.randint(0, len(genome)-1)
            new_genome[idx] = not new_genome[idx]
        return tuple(new_genome)

    def evolve(self):
        for i in range(self.offspring_size):
            if random.randint(1, 10) < 10*self.mutation_chance:
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
            if (self.fitness_evaluations > self.fitness_evaluations_threshold):
                print(f"Maximum number of evaluations ({self.fitness_evaluations}) reached. Trained for {i} generations.")
                break
        print("100% Done!")
    
    def sort_population(self):
        self.population = sorted(self.population, key=lambda i: i[1], reverse=True)

    def get_solution(self):
        if (self.population[0][1][0] < self.N):
            print("No solution has been found!")
            return list()
        solution = list()
        genome = self.population[0][0]
        for i in range(len(genome)):
            if genome[i] == 1:
                solution.append(self.problem[i])
        return solution
