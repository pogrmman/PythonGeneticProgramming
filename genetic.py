#!/bin/python3

##### Importing Modules #####
### Builtin Modules ###
import random
import math
import collections.abc

class Population(collections.abc.Sequence):
    def __init__(self, n_individuals, individual_length, gene_max, fitness_func):
        self.individuals = [Individual(individual_length, gene_max, fitness_func) for i in range(0, n_individuals)]
        self._finish_init(n_individuals)
        
    def _finish_init(self, n_individuals):
        self.n_individuals = n_individuals
        self.individuals.sort()
        self.fittest = self.individuals[0]
        self.best_fitness = self.individuals[0].fitness
        self.avg_fitness = self._calc_avg_fitness()

    def _calc_avg_fitness(self):
        sum = 0
        for individual in self.individuals:
            sum += individual.fitness
        return sum / self.n_individuals
    
    def new_population(self, preserve_percent, non_optimal = 0, mutation_percent = .05):
        n_parents = math.floor(self.n_individuals * preserve_percent)
        n_non_optimal = math.floor(self.n_individuals * non_optimal)
        parents = self.individuals[:n_parents]
        for i in range(0, n_non_optimal):
            parents.append(random.choice(self.individuals))
        next_gen_individuals = parents.copy()
        while len(next_gen_individuals) < self.n_individuals:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = parent1.crossover(parent2)
            child.mutate(mutation_percent)
            next_gen_individuals.append(child)
        return New_Population(self.n_individuals, next_gen_individuals)

    # Container emulation methods
    def __getitem__(self, index):
        return self.individuals[index]

    def __len__(self):
        return self.n_individuals

    def __iter__(self):
        for item in self.individuals:
            yield item

    def __contains__(self, individual):
        matched = False
        for indiv in self.individuals:
            if individual == indiv:
                matched = True
                break
        return matched
    
class New_Population(Population):
    def __init__(self, n_individuals, individuals):
        self.individuals = individuals
        self._finish_init(n_individuals)
        
class Individual(collections.abc.Sequence):
    def __init__(self, individual_length, gene_max, fitness_func):
        self.chromosome = [random.randint(0, gene_max) for i in range(0, individual_length)]
        self._finish_init(individual_length, gene_max, fitness_func)
        
    def _finish_init(self, individual_length, gene_max, fitness_func):
        self.max = gene_max
        self.length = individual_length
        self.fitness_func = fitness_func
        self.fitness = self.fitness_func(self.chromosome)

    def mutate(self, probability):
        for index, item in enumerate(self.chromosome):
            if random.random() < probability:
                self.chromosome[index] = random.randint(0, self.max)

    def crossover(self, other):
        chromosome = [0 for i in range(0, self.length)]
        for index, gene in enumerate(self.chromosome):
            num = random.random()
            if num < .5:
                chromosome[index] = gene
            else:
                chromosome[index] = other.chromosome[index]
        return NewIndividual(chromosome, self.max, self.fitness_func)

    # Container emulation methods
    def __getitem__(self, index):
        return self.chromosome[index]

    def __len__(self):
        return self.length

    def __iter__(self):
        for item in self.chromosome:
            yield item

    def __contains__(self, item):
        return item in self.chromosome

    # Methods to allow comparison (for sorting)
    def __eq__(self, other):
        identical_chromosomes = True
        for index, item in self.chromosome:
            if other[index] != item:
                identical_chromosomes = False
        if len(other) != self.length:
            identical_chromosomes = False
        return (self.max == other.max and self.fitness == other.fitness
                                      and identical_chromosomes)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __ne__(self, other):
        return not self.__eq__(other)

class NewIndividual(Individual):
    def __init__(self, chromosome, gene_max, fitness_func):
        self.chromosome = chromosome
        self._finish_init(len(self.chromosome), gene_max, fitness_func)

def evolve(n_individuals, individual_length, gene_max, fitness_func, preserve_percent,
           non_optimal = 0, mutation_percent = 0.05):
    generation = Population(n_individuals, individual_length, gene_max, fitness_func)
    last_fitness = 0
    next_fitness = generation.avg_fitness
    while last_fitness < next_fitness:
        generation = generation.new_population(preserve_percent, non_optimal, mutation_percent)
        last_fitness = next_fitness
        next_fitness = generation.avg_fitness
    print("Fittest individual has a fitness of " + str(generation.best_fitness))
    return generation.fittest
