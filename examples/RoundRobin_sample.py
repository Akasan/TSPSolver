import sys
sys.path.append("../")
from TSPSolver.RoundRobin import RoundRobin


if __name__ == "__main__":
    rr = RoundRobin("./kroA100.tsp")
    rr.search()