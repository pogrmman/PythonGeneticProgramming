#!/bin/python3

##### Importing Modules #####
### Builtin Modules ###
import random
import math
import collections.abc

##### Classes #####
### Population Classes ###
## Generic Population Class ##
class Population(collections.abc.Sequence):
    """Class to create a population of individuals for a given fitness function.

    Provides the following public methods:
    new_population -- Create the next generation's population.

    Provides the following attributes:
    individuals -- A list containing the individuals in the population, sorted by fitness.
    n_individuals -- The number of individuals in the population.
    fittest -- The most fit individual.
    avg_fitness -- The average fitness of the population.
    best_fitness -- The fitness of the fittest individual.

    This class provides the methods to be used as a sequence.
    """
    def __init__(self, n_individuals, individual_length, gene_max, fitness_func):
        """Initialize the population.

        Usage:
        __init__(n_individuals, individual_length, gene_max, fitness_func)

        Parameters:
        n_individuals -- The number of individuals in the population.
        individual_length -- The length of an individual's chromosome.
        gene_max -- The maximum value for any spot in an individual's chromosome.
        fitness_func -- A function that takes a chromosome and returns its fitness.
        """
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
        """Create the next generation's population.

        Usage:
        new_population(preserve_percent[, non_optimal, mutation_percent])
        
        Parameters:
        preserve_percent -- The proportion of best performing individuals to use as the parents.
        non_optimal -- The proportion of randomly selected individuals to use as parents. Defaults to 0.
        mutation_percent -- The probability of a location on a chromosome mutating. Defaults to 0.05.
        """
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

## New Population Class ##    
class New_Population(Population):
    """Class to create a population from a list of individuals.

    Provides all public methods and attributes of the Population class.
    """
    def __init__(self, n_individuals, individuals):
        """Initialize a population from a list of individuals.

        Usage:
        __init__(n_individuals, individuals)

        Parameters:
        n_individuals -- The number of individuals in the population.
        individuals -- A list of individuals.
        """
        self.individuals = individuals
        self._finish_init(n_individuals)

### Individual Classes ###
## Basic Individual Class ##
class Individual(collections.abc.Sequence):
    """Class to create a single individual.

    Provides the following public methods:
    mutate -- Mutate the individual.
    crossover -- Create a child from this individual and another one.
    fitness_func -- The fitness function for this individual.
    
    Provides the following public attributes:
    chromosome -- A list of integers, representing the chromosome of the individual.
    max -- The maximum possible value of a location on the chromosome.
    length -- The length of the chromosome.
    fitness -- The fitness of this individual.
    
    This class provides the methods to be used as a sequence.
    """
    def __init__(self, individual_length, gene_max, fitness_func):
        """Initialize an individual.

        Usage:
        __init__(individual_length, gene_max, fitness_func)

        Parameters:
        individual_length -- The length of the chromosome of the individual.
        gene_max -- The maximum integer to use at any location along the chromosome.
        fitness_func -- A function that takes a chromosome and returns its fitness.
        """
        self.chromosome = [random.randint(0, gene_max) for i in range(0, individual_length)]
        self._finish_init(individual_length, gene_max, fitness_func)
        
    def _finish_init(self, individual_length, gene_max, fitness_func):
        self.max = gene_max
        self.length = individual_length
        self.fitness_func = fitness_func
        self.fitness = self.fitness_func(self.chromosome)

    def mutate(self, probability):
        """Mutate the individual.

        Usage:
        mutate(probability)

        Parameters:
        probability -- The probability that a given location on the chromosome will mutate.
        """
        for index, item in enumerate(self.chromosome):
            if random.random() < probability:
                self.chromosome[index] = random.randint(0, self.max)

    def crossover(self, other):
        """Create a child from this individual and another one.

        Usage:
        crossover(other)

        Parameters:
        other -- Another individual.
        """
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

## New Individual Class ##
class NewIndividual(Individual):
    """Class to create a new individual from a given chromosome.

    Provides all the public methods and attributes of the Individual class.
    """
    def __init__(self, chromosome, gene_max, fitness_func):
        """Initialize a new individual from a given chromosome.
        
        Usage:
        __init__(chromosome, gene_max, fitness_func)

        Parameters:
        chromosome -- A list of integers, this individual's chromosome.
        gene_max -- The maximum possible value of any location on the chromosome.
        fitness_func -- A function that takes a chromosome and returns its fitness.
        """
        self.chromosome = chromosome
        self._finish_init(len(self.chromosome), gene_max, fitness_func)

##### Functions #####
### Evolve Function ###
def evolve(n_individuals, individual_length, fitness_func, preserve_percent,
           non_optimal = 0, mutation_percent = 0.05, gene_max = 100):
    """Evolve a solution to a fitness function.

    Usage:
    evolve(n_individuals, individual_length, fitness_func, preserve_percent[, non_optimal, mutation_percent, gene_max])

    Parameters:
    n_individuals -- The number of individuals in each generation.
    individual_length -- The length of the chromosome of each individual.
    fitness_func -- A function that takes a chromosome and returns its fitness.
    preserve_percent -- The proportion of best performers to use as the parents of the next generation.
    non_optimal -- The proportion of randomly selected individuals to add to the pool of parents. Defaults to 0.
    mutation_percent -- The probability of a given location on a chromosome mutating. Defaults to 0.05.
    gene_max -- The maximum value to use on any location of a chromosome. Defaults to 100.
    """
    generation = Population(n_individuals, individual_length, gene_max, fitness_func)
    last_fitness = 0
    next_fitness = generation.avg_fitness
    while last_fitness < next_fitness:
        generation = generation.new_population(preserve_percent, non_optimal, mutation_percent)
        last_fitness = next_fitness
        next_fitness = generation.avg_fitness
    print("Fittest individual has a fitness of " + str(generation.best_fitness))
    return generation.fittest
