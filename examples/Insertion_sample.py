import sys
sys.path.append("../")
from TSPSolver.Insertion import RandomInsertion, NearestInsertion, FarthestInsertion


if __name__ == "__main__":
    random_insert = FarthestInsertion("./kroA100.tsp")
    random_insert.search()