import random

from config import TrainingConfig
from neural_network import NeuralNetwork


class GeneticAlgorithm:
    def __init__(self, selection_method=None):
        self.population_size = TrainingConfig.POPULATION_SIZE
        self.tournament_size = TrainingConfig.TOURNAMENT_SIZE
        self.mutation_rate = TrainingConfig.MUTATION_RATE
        self.mutation_amount = TrainingConfig.MUTATION_AMOUNT
        self.selection_method = (
            selection_method or TrainingConfig.SELECTION_METHOD
        )

    def calculate_fitness(self, bird):
        # Fitness = thời gian tồn tại (số frame sống sót)
        return bird.frames_alive

    def tournament_selection(self, birds):
        tournament = random.sample(birds, self.tournament_size)
        winner = max(tournament, key=self.calculate_fitness)
        return winner

    def roulette_wheel_selection(self, birds):
        fitnesses = [self.calculate_fitness(b) for b in birds]
        # Xử lý fitness âm (dù hiện tại fitness >= 0)
        min_f = min(fitnesses)
        if min_f < 0:
            fitnesses = [f - min_f for f in fitnesses]
        total = sum(fitnesses)
        if total == 0:
            return random.choice(birds)
        pick = random.uniform(0, total)
        current = 0
        for bird, f in zip(birds, fitnesses):
            current += f
            if current >= pick:
                return bird
        return birds[-1]

    def select_parent(self, birds):
        if self.selection_method == "roulette":
            return self.roulette_wheel_selection(birds)
        return self.tournament_selection(birds)

    def crossover(self, parent1, parent2):
        genome1 = parent1.brain.genome
        genome2 = parent2.brain.genome

        child_genome = []
        for i in range(len(genome1)):
            if random.random() < 0.5:
                child_genome.append(genome1[i])
            else:
                child_genome.append(genome2[i])
        return child_genome

    def mutate(self, genome):
        mutated_genome = genome.copy()
        for i in range(len(mutated_genome)):
            if random.random() < self.mutation_rate:
                mutated_genome[i] += random.uniform(
                    -self.mutation_amount,
                    self.mutation_amount
                )
        return mutated_genome

    def create_next_generation(self, birds):
        birds = sorted(
            birds,
            key=self.calculate_fitness,
            reverse=True
        )

        new_birds = []

        if TrainingConfig.ELITISM:
            elite = birds[0]
            new_birds.append(
                self.create_bird_from_genome(elite.brain.genome)
            )

        while len(new_birds) < self.population_size:
            parent1 = self.select_parent(birds)
            parent2 = self.select_parent(birds)

            child_genome = self.crossover(parent1, parent2)
            child_genome = self.mutate(child_genome)

            child = self.create_bird_from_genome(child_genome)
            new_birds.append(child)

        return new_birds

    def create_bird_from_genome(self, genome):
        from bird import Bird
        brain = NeuralNetwork(genome=genome)
        return Bird(brain=brain)
