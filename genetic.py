#!/bin/python3

##### Importing Modules #####
### Builtin Modules ###
import random
import math

class Population(object):
    def __init__(self, n_individuals, individual_length, gene_max, fitness_func):
        self.n_individuals = n_individuals
        self.individuals = [Individual(individual_length, gene_max, fitness_func) for i in range(0, self.n_individuals)]
        self.individuals.sort(reverse = True)
        
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

    def get_fittest(self):
        return self.individuals[0]

    def get_best_fitness(self):
        return self.individuals[0].fitness
    
class New_Population(Population):
    def __init__(self, n_individuals, individuals):
        self.n_individuals = n_individuals
        self.individuals = individuals
        self.individuals.sort(reverse = True)
        
class Individual(object):
    def __init__(self, individual_length, gene_max, fitness_func):
        self.max = gene_max
        self.length = individual_length
        self.chromosome = [random.randint(0, self.max) for i in range(0, self.length)]
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

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness

    def __ne__(self, other):
        return self.fitness != other.fitness

class NewIndividual(Individual):
    def __init__(self, chromosome, gene_max, fitness_func):
        self.chromosome = chromosome
        self.length = len(self.chromosome)
        self.max = gene_max
        self.fitness_func = fitness_func
        self.fitness = self.fitness_func(self.chromosome)

def evolve(n_individuals, individual_length, gene_max, fitness_func, preserve_percent, non_optimal = 0, mutation_percent = 0.05):
    generation = Population(n_individuals, individual_length, gene_max, fitness_func)
    last_fitness = 0
    next_fitness = generation.get_best_fitness()
    while last_fitness < next_fitness:
        generation = generation.new_population(preserve_percent, non_optimal, mutation_percent)
        last_fitness = next_fitness
        next_fitness = generation.get_best_fitness()
    print("Fittest individual has a fitness of " + str(next_fitness))
    return generation.get_fittest()
