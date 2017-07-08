#!/bin/python3

##### Importing Modules #####
### Builtin Modules ###
import math
### Package Modules ###
import genetic

class FitPoints(object):
    def __init__(self, points):
        self.points = points

    def sum_of_squares(self, chromosome):
        sum = 0
        slope = chromosome[0]
        y_int = chromosome[1]
        vals = [(i[0], slope * i[0] + y_int) for i in self.points]
        for p1, p2 in zip(vals, self.points):
            sum += self.dist(p1, p2)
        return sum

    def evolve(self, *args, **kwargs):
        self.best = genetic.evolve(*args, **kwargs)
        self.slope = self.best[0]
        self.y_int = self.best[1]
        
    @staticmethod
    def dist(p1, p2):
        return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
