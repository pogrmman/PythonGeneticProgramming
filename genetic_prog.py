import random
import copy
import math

FUNCS = ["+", "-", "*", "/"]
TERMS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class BinaryTree(object):
    def __init__(self, node, left, right):
        self.node = node
        self.left = left
        self.right = right

    def __str__(self):
        return "(" + str(self.node) + " " + str(self.left) + " " + str(self.right) + ")"

class Individual(object):
    def __init__(self, maxdepth):
        self.tree = BinaryTree(random.choice(FUNCS),
                               buildtree(maxdepth), buildtree(maxdepth))

    def mutate(self, probability):
        self.mutate_terms(probability)
        self.mutate_funcs(probability)

    def eval(self, fitness_func):
        self.fitness = fitness_func(self.tree)
        
    def insert(self, probability, depth, tree = "start"):
        if tree == "start":
            tree = self.tree
        if tree:
            if isinstance(tree, BinaryTree):
                if random.random() < probability:
                    if random.random() < 0.5:
                        tree.right = BinaryTree(random.choice(FUNCS),
                                                buildtree(depth),
                                                buildtree(depth))
                        self.insert(probability, depth, tree.left)
                    else:
                        tree.left = BinaryTree(random.choice(FUNCS),
                                               buildtree(depth),
                                               buildtree(depth))
                        self.insert(probability, depth, tree.right)
                else:
                    self.insert(probability, depth, tree.left)
                    self.insert(probability, depth, tree.right)
                             
    def prune(self, probability, tree = "start"):
        if tree == "start":
            tree = self.tree
        if tree:
            if isinstance(tree, BinaryTree):
                if random.random() < probability:
                    if random.random() < 0.5:
                        tree.right = random.choice(TERMS)
                    else:
                        tree.left = random.choice(TERMS)
                self.prune(probability, tree.left)
                self.prune(probability, tree.right)
                
    def mutate_terms(self, probability, tree = "start"):
        if tree == "start":
            tree = self.tree
        if tree:
            if isinstance(tree, BinaryTree):
                if not isinstance(tree.left, BinaryTree):
                    if random.random() < probability:
                        tree.left = random.choice(TERMS)
                if not isinstance(tree.right, BinaryTree):
                    if random.random() < probability:
                       tree.right = random.choice(TERMS)
                self.mutate_terms(probability, tree.left)
                self.mutate_terms(probability, tree.right)
                
    def mutate_funcs(self, probability, tree = "start"):
        if tree == "start":
            tree = self.tree
        if tree:
            if isinstance(tree, BinaryTree):
                if random.random() < probability:
                    tree.node = random.choice(FUNCS)
                self.mutate_funcs(probability, tree.left)
                self.mutate_funcs(probability, tree.right)

    def crossover(self, other):
        tree1 = copy.copy(self.tree)
        tree2 = copy.copy(other.tree)
        crossover_side = random.choice(["l", "r"])
        if crossover_side == "l":
            subtree1 = self.tree.left
            subtree2 = other.tree.left
            tree1.left = subtree2
            tree2.left = subtree1
        elif crossover_side == "r":
            subtree1 = self.tree.right
            subtree2 = other.tree.right
            tree1.right = subtree2
            tree2.right = subtree1
        return [NewIndividual(tree1), NewIndividual(tree2)]

    def __str__(self):
        return str(self.tree)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __le__(self, other):
        return self.fitness <= other.fitness

    def __gt__(self, other):
        return self.fitness > other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness
    
class NewIndividual(Individual):
    def __init__(self, tree):
        self.tree = tree

class Population(object):
    def __init__(self, n_individuals, max_depth):
        self.individuals = []
        self.n_individuals = n_individuals
        for i in range(0, n_individuals):
            self.individuals.append(Individual(max_depth))

    def eval(self, fitness_func):
        for individual in self.individuals:
            individual.eval(fitness_func)
        self.individuals.sort()
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
        next_gen_individuals = copy.copy(parents)
        while len(next_gen_individuals) < self.n_individuals:
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)
            child = random.choice(parent1.crossover(parent2))
            child.mutate_funcs(mutation_percent)
            child.mutate_terms(mutation_percent)
            child.prune(mutation_percent)
            child.insert(mutation_percent, 3)
            next_gen_individuals.append(child)
        return NewPopulation(self.n_individuals, next_gen_individuals)

class NewPopulation(Population):
    def __init__(self, n_individuals, individuals):
        self.individuals = individuals
        self.n_individuals = n_individuals

class Queue(object):
    def __init__(self, length):
        self.queue = [0 for i in range(0, length)]
        self.length = length
        
    def append(self, item):
        self.queue.append(item)
        self.queue = self.queue[1:]

    def __iter__(self):
        for item in self.queue:
            yield item

    def __str__(self):
        return str(self.queue)

    def __getitem__(self, index):
        return self.queue[index]

    def __len__(self):
        return self.length

    def __contains__(self, item):
        return item in self.queue
    
def buildtree(maxdepth, curdepth = 0):
    if curdepth >= maxdepth:
        return random.choice(TERMS)
    else:
        if random.random() > 0.5:
            return random.choice(TERMS)
        else:
            return BinaryTree(random.choice(FUNCS),
                              buildtree(maxdepth, curdepth + 1),
                              buildtree(maxdepth, curdepth + 1))

def evolve(n_individuals, max_depth, fitness_func, preserve_percent, non_optimal = 0, mutation_percent = 0.05):
    generation = Population(n_individuals, max_depth)
    fitnesses = Queue(5)
    for i in range(0, 5):
        fitnesses.append(generation.eval(fitness_func))
        generation = generation.new_population(preserve_percent, non_optimal, mutation_percent)
    sum = 0
    for item in fitnesses:
        sum += item
    avg = sum / 5
    next_fitness = generation.eval(fitness_func)
    while next_fitness < avg:
        generation = generation.new_population(preserve_percent, non_optimal, mutation_percent)
        fitnesses.append(generation.eval(fitness_func))
        sum = 0
        for item in fitnesses:
            sum += item
        avg = sum / 5
    print("Fittest individual has a fitness of " + str(generation.individuals[0].fitness))
    print("Population has an average fitness of " + str(fitnesses[-1]))
    return generation

def tostring(tree):
    if isinstance(tree, BinaryTree):
        return tostring(tree.left) + " " + str(tree.node) + " " + tostring(tree.right)
    else:
        return str(tree)

def fitness(tree):
    try:
        result = eval(tostring(tree))
        ret_val = abs(10 - result) / 10
    except:
        ret_val = 1000000
    return ret_val
