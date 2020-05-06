from ..utils.DataLoader import load_dataset
from ..utils.DataWriter import DataWriter
from pprint import pprint


class Greedy:
    """ Greedy method

    Attributes:
    -----------
        CITY_NUM {int} -- the number of cities
        distance_arr {np.ndarray} -- distance between cities
        writer {DataWriter} -- writer of saving scores
        route {dict} -- route which starts from each cities

    Examples:
    ---------
        >>> from TSPSolver.Greedy import Greedy
        >>> greedy = Greedy("kroA100.tsp")
        >>> greedy.search()
    """

    def __init__(self, dataset_filename):
        """
        Arguments:
        ----------
            dataset_filename {str} -- dataset file name
        """
        city_num, distance = load_dataset(dataset_filename)
        self.CITY_NUM = city_num
        self.distance_arr = distance
        self.writer = DataWriter()

    def search(self):
        """ search path"""
        self.generate_route()
        self.calculate_distance()

        for k, v in self.distance.items():
            print(f"Start: {k}\tDistance: {v:.4f}")

    def generate_route(self):
        """ gnerate route"""
        self.route = {}
        for i in range(self.CITY_NUM):
            self.route[i] = [i]

            for next_city in range(self.CITY_NUM):
                if next_city == i:
                    continue

                distance = self.distance_arr[self.route[i][-1]]
                distance_dict = {k: v for k, v in zip(range(self.CITY_NUM), distance)}
                distance_dict_sorted = dict(sorted(distance_dict.items(), key=lambda x: x[1]))

                for k, v in distance_dict_sorted.items():
                    if v == -1 or k in self.route[i]:
                        continue
                    self.route[i].append(k)
                    break

    def calculate_distance(self):
        """ calculate distance"""
        self.distance = {}

        for k, v in self.route.items():
            self.distance[k] = 0
            for i in range(self.CITY_NUM):
                city1 = v[i]
                city2 = v[(i+1) % self.CITY_NUM]
                self.distance[k] += self.distance_arr[city1, city2]