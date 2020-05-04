from AntColonyOptimization import AntSystem, MaxMinAntSystem


if __name__ == "__main__":
    ant_system = MaxMinAntSystem("./kroA100.tsp", 10)
    ant_system.search(iteration=10)