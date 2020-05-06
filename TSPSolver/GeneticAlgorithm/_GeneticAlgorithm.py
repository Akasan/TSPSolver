from .src.Population import Population
from ..utils.DataLoader import load_dataset


class GeneticAlgorithm:
    def __init__(self, dataset_filename, population_size, mutation_rate):
        city_num, distance = load_dataset(dataset_filename)
        self.CITY_NUM = city_num
        self.MUTATION_RATE = mutation_rate
        self.distance = distance
        self.population = Population(population_size, self.CITY_NUM, distance)

    def search(self, iteration):
        for i in range(iteration):
            self.population.evaluate()
