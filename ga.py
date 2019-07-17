import random
import math
from copy import copy

class GeneticAlgorithm:

    def __init__(self, numchrom, popsize = 50, crossoverrate = 0.3, mutationrate = 0.3, epochs = 100, elitism = 0):
        self.setparameters(popsize, crossoverrate, mutationrate, epochs, elitism)
        self.numchrom = numchrom
        self.fitfunc = None
        self.extradata = None
        self.selectmethod = "roulette"
        self.population = []
        self.__initpop__()

    def __initpop__(self):
        for i in range(self.popsize):
            individual = []
            for j in range(self.numchrom):
                individual.append(random.randint(0,1))
            self.population.append(individual)

    def roulette(self):
        fitted = []

        for i in range(self.popsize):
            genome = copy(self.population[i])
            phenome = self.genometophenome(genome)
            fitted.append((genome, self.fitfunc(phenome, self.extradata)))

        fitted.sort(key = lambda x : x[1])
        sumfitness = sum(x[1] for x in fitted)
        fitted[0] = (fitted[0][0], fitted[0][1], fitted[0][1] / sumfitness)
        for i in range(1, self.popsize):
            fitted[i] = (fitted[i][0], fitted[i][1], (fitted[i][1] / sumfitness) + fitted[i-1][2])

        return fitted

    def setparameters(self, popsize, crossoverrate, mutationrate, epochs, elitism):
        self.popsize = popsize
        self.crossoverrate = crossoverrate
        self.epochs = epochs
        self.elitism = elitism
        if elitism > popsize:
            self.elitism = 0
        if isinstance(mutationrate, tuple):
            self.mutationrate = mutationrate[0]
            self.mutationratefinal = mutationrate[1]
        else:
            self.mutationrate = mutationrate
            self.mutationratefinal = mutationrate

    def setfitness(self, fitfunc, extradata):
        self.fitfunc = fitfunc
        self.extradata = extradata

    def setselection(self, selectmethod):
        self.selectmethod = selectmethod

    def setgenometophenome(self, func):
        self.genometophenome = func

    def setphenometogenome(self, func):
        self.phenometogenome = func

    def __nextgeneration__(self):
        fitted = self.roulette()
        offspring = []

        #for ind in fitted:
        #    print(ind)

        # Elitism
        e = self.popsize - 1
        for i in range(self.elitism):
            offspring.append(fitted[e][0])
            e -= 1

        #print(offspring)
        while len(offspring) < self.popsize:
            # Selection
            parents = []
            p = random.random()
            for i in range(self.popsize):
                if p < fitted[i][2]:
                    parents.append(copy(fitted[i][0]))
                    break

            done = False
            while not done:
                p = random.random()
                for j in range(self.popsize):
                    if i != j and p < fitted[j][2]:
                        parents.append(copy(fitted[j][0]))
                        done = True
                        break

            # Crossover
            children = parents
            p = random.random()
            if p < self.crossoverrate:
                cut = random.randint(1, self.numchrom - 1)
                for i in range(cut):
                    aux = children[0][i]
                    children[0][i] = children[1][i]
                    children[1][i] = aux

            # Mutation
            for child in range(2):
                for i in range(self.numchrom):
                    p = random.random()
                    if p < self.mutationrate:
                        children[child][i] = int(not children[child][i])

            offspring.append(children[0])
            if len(offspring) != self.popsize:
                offspring.append(children[1])

        return offspring

    def evolve(self):
        for epoch in range(self.epochs):
            if self.epochs // 4 == epoch:
                print("mutation change")
                self.mutationrate = self.mutationratefinal
            self.population = self.__nextgeneration__()
            fitted = self.roulette()
            #print(round(math.pow(fitted[len(fitted)-1][1], 1/5)))

        return fitted[len(fitted)-1][0]

