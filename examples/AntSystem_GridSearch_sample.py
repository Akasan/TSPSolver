import sys
sys.path.append("../")
from TSPSolver.AntColonyOptimization import GridSearch


if __name__ == "__main__":
    param_grid = {"alpha": {"min": 1.0, "max": 3.0, "interval": 0.5},
                  "beta": {"min": 1.0, "max": 5.0, "interval": 0.5},
                  "rho": {"min": 0.5, "max": 0.98, "interval": 0.25},
                  "agent_num": {"value": 100}}

    gs = GridSearch(param_grid)
    gs.search(iteration=1, dataset_filename="./kroA100.tsp")