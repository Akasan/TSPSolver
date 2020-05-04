import sys
sys.path.append("../")
from TSPSolver.Greedy import Greedy


if __name__ == "__main__":
    greedy = Greedy("./kroA100.tsp")
    greedy.search()