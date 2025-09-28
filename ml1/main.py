import numpy as np
import matplotlib.pyplot as plt
import random

   # Количество полей
CROPS = ["Wheat", "Corn", "Barley", "Soybean", "Sunflower", "Beet"]
crop_costs = np.array([30, 45, 25, 50, 40, 35])  
field_yields = np.array([
    [1.72, 4.13, 2.95, 3.47, 1.59, 4.88],
    [2.34, 3.21, 1.87, 4.45, 2.76, 3.99],
    [4.67, 1.98, 2.43, 3.88, 4.12, 1.34],
    [3.56, 2.67, 4.21, 1.76, 2.91, 3.44],
    [1.88, 4.55, 3.12, 2.34, 1.99, 4.01],
    [2.77, 3.89, 1.45, 4.67, 2.18, 3.22],
    [4.33, 2.12, 3.76, 1.54, 4.88, 2.65],
    [3.11, 1.67, 4.44, 2.23, 3.55, 1.88],
    [2.56, 4.22, 3.33, 1.99, 2.77, 4.66],
    [1.45, 3.88, 2.12, 4.55, 3.01, 2.34]
])
N_FIELDS = field_yields.shape[0]
K = len(CROPS)

ALPHA, BETA = 0.6, 0.4
MUTATION_PROBABILITY = 0.5
CROSSOVER_PROBABILITY = 0.7

# класс особи 
class Individual:
    def __init__(self, genome):
        self.genome = genome
        self.fitness, self.total_yield, self.total_cost = self.calculate_fitness()

    def calculate_fitness(self):
        total_yield = np.sum(field_yields[np.arange(N_FIELDS), self.genome])
        total_cost = np.sum(crop_costs[self.genome])
        max_yield = np.sum(np.max(field_yields, axis=1))
        max_cost = N_FIELDS * np.max(crop_costs)
        norm_yield = total_yield / max_yield
        norm_cost = total_cost / max_cost
        score = ALPHA * norm_yield - BETA * norm_cost
        return score, total_yield, total_cost

#создание популяции 
def create_random_individual():
    genome = np.random.randint(0, K, size=N_FIELDS)
    return Individual(genome)

# Отбор 
def select_parents(population):
    candidates = random.sample(population, 5)
    candidates.sort(key=lambda x: x.fitness, reverse=True)
    return candidates[:2]

#скрещивание 
def single_point_crossover(parent1, parent2):
    point = np.random.randint(1, N_FIELDS)
    child1 = np.concatenate([parent1.genome[:point], parent2.genome[point:]])
    child2 = np.concatenate([parent2.genome[:point], parent1.genome[point:]])
    return Individual(child1), Individual(child2)

def two_point_crossover(parent1, parent2):
    p1, p2 = sorted(np.random.randint(1, N_FIELDS, size=2))
    child1 = parent1.genome.copy(); child2 = parent2.genome.copy()
    child1[p1:p2], child2[p1:p2] = parent2.genome[p1:p2], parent1.genome[p1:p2]
    return Individual(child1), Individual(child2)

def uniform_crossover(parent1, parent2):
    mask = np.random.randint(0, 2, size=N_FIELDS).astype(bool)
    child1 = np.where(mask, parent1.genome, parent2.genome)
    child2 = np.where(mask, parent2.genome, parent1.genome)
    return Individual(child1), Individual(child2)

# Мутации 
def random_reset(ind):
    genome = ind.genome.copy()
    pos = np.random.randint(N_FIELDS)
    genome[pos] = np.random.randint(K)
    return Individual(genome)

def swap_mutation(ind):
    genome = ind.genome.copy()
    i, j = np.random.choice(N_FIELDS, 2, replace=False)
    genome[i], genome[j] = genome[j], genome[i]
    return Individual(genome)

def inversion_mutation(ind):
    genome = ind.genome.copy()
    i, j = sorted(np.random.choice(N_FIELDS, 2, replace=False))
    genome[i:j+1] = genome[i:j+1][::-1]
    return Individual(genome)

# Эволбция
def evolve_population(population, crossover, mutation):
    new_pop = []
    while len(new_pop) < len(population):
        p1, p2 = select_parents(population)
        if random.random() < CROSSOVER_PROBABILITY:
            c1, c2 = crossover(p1, p2)
        else:
            c1, c2 = p1, p2
        if random.random() < MUTATION_PROBABILITY:
            c1 = mutation(c1)
        if random.random() < MUTATION_PROBABILITY:
            c2 = mutation(c2)
        new_pop.extend([c1, c2])
    return new_pop[:len(population)]

#Эксперимент
def run_experiment(crossover, mutation, label, color):
    population = [create_random_individual() for _ in range(20)]
    best_over_time = []
    for g in range(50):
        population = evolve_population(population, crossover, mutation)
        best_fitness = max(ind.fitness for ind in population)
        best_over_time.append(best_fitness)
    plt.plot(best_over_time, label=label, color=color)
    best = max(population, key=lambda ind: ind.fitness)
    print(f"{label}: Урожай={best.total_yield:.2f}, Стоимость={best.total_cost:.2f}, Фитнес={best.fitness:.4f}")
    print("Назначение:", best.genome)

 
plt.figure(figsize=(10,8))
run_experiment(single_point_crossover, random_reset, "Single-point + Reset", "red")
run_experiment(two_point_crossover, random_reset, "Two-point + Reset", "green")
run_experiment(uniform_crossover, random_reset, "Uniform + Reset", "blue")

run_experiment(single_point_crossover, swap_mutation, "Single-point + Swap", "orange")
run_experiment(two_point_crossover, swap_mutation, "Two-point + Swap", "purple")
run_experiment(uniform_crossover, swap_mutation, "Uniform + Swap", "brown")

run_experiment(single_point_crossover, inversion_mutation, "Single-point + Inversion", "pink")
run_experiment(two_point_crossover, inversion_mutation, "Two-point + Inversion", "cyan")
run_experiment(uniform_crossover, inversion_mutation, "Uniform + Inversion", "gray")

plt.title("Эволюция функции приспособленности (поля-культуры)")
plt.xlabel("Поколение")
plt.ylabel("Лучшая приспособленность")
plt.legend()
plt.grid(True)
plt.show()
