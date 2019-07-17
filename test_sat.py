import random
from ga import GeneticAlgorithm

def readsat(filename):
    f = open(filename)

    txt = f.read()
    f.close()

    txt = txt.split("\n")
    txt.pop()
    n = int(txt.pop(0))
    formula = []
    for line in txt:
        line = line.split(" ")
        formula.append((int(line[0]), int(line[1]), int(line[2])))

    return (formula, n)

def var(value, table):
    if value > 0:
        return table[value-1]

    return not table[-(value+1)]

def trueclauses(table, formula):
    n = 0
    for (x, y, z) in formula:
        if var(x, table) or var(y, table) or var(z, table):
            n += 1

    return n

def fitness(table, formula):
    n = 0
    for (x, y, z) in formula:
        if var(x, table) or var(y, table) or var(z, table):
            n += 1

    return pow(n, 5)
    #return n

def gtop(genome):
    phenome = []
    for i in genome:
        phenome.append(bool(i))

    return phenome

def ptog(phenome):
    genome = []
    for i in phenome:
        genome.append(int(i))

    return genome

def solve(formula, table):
    return trueclauses(formula, table) == len(formula)

def randtable(n):
    table = []

    for i in range(n):
        table.append(bool(random.randint(0,1)))

    return table

def randomsearch(popsize, epochs, formula, n):
    randsearch = 0
    
    for epoch in range(epochs):
        local = 0

        for i in range(popsize):
            table = randtable(n)
            tc = trueclauses(table, formula)
            if tc > local:
                local = tc

        if local > randsearch:
            randsearch = local
        print(randsearch)

    return randsearch


formula, n = readsat("uf100-01.cnf")
#print(formula, len(formula))
popsize = 60
epochs = 10000

print("# Global Optimum:", len(formula))
#print("randsearch", randomsearch(popsize, epochs, formula, n))
ga = GeneticAlgorithm(n, crossoverrate = 0.99, mutationrate = (0.05, 0.01), popsize = popsize, elitism = 5, epochs = epochs)
ga.setfitness(fitness, formula)
ga.setgenometophenome(gtop)
ga.setphenometogenome(ptog)
solucao = ga.evolve()
print(solucao)
