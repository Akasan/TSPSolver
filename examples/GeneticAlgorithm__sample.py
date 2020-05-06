import sys
sys.path.append("../")
from TSPSolver.GeneticAlgorithm import GeneticAlgorithm


if __name__ == "__main__":
    ga = GeneticAlgorithm("./kroA100.tsp", 100, 0.1)
    ga.search(1)
