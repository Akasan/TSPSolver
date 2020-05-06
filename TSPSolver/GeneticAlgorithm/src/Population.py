from .Gene import Gene
from .Select import roulette_selection
from .Mutation import mutate



class Population:
    """
    Attributes:
    -----------
        population_size {int} -- the number of population
        city_num {int} -- the number of cities
    """

    def __init__(self, population_size, city_num, distance):
        """
        Arguments:
        ----------
            population_size {int} -- the number of population
            city_num {int} -- the number of cities
        """
        self.POPULATION_SIZE = population_size
        self.CITY_NUM = city_num
        self.distance = distance
        self.gene = [Gene(self.POPULATION_SIZE, self.CITY_NUM) for _ in range(self.POPULATION_SIZE)]
        self.fitness = np.array([0.0 for _ in range(self.POPULATION_SIZE)])

    def evaluate(self):
        for i, gene in enumerate(self.gene):
            self.fitness[i] = 0.0
            for city1, city2 in gene.get_route_pair():
                self.fitness[i] += self.distance[city1, city2]

    def select(self):
        pass