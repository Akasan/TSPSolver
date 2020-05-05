import sys
sys.path.append("../")
from TSPSolver.AntColonyOptimization import AntSystem, MaxMinAntSystem


if __name__ == "__main__":
    ant_system = AntSystem("./kroA100.tsp", 10)
    ant_system.search(iteration=100, is_judge_convergence=True, convergence_iteration=100)
