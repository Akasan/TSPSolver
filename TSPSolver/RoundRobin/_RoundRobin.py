from ..utils.DataLoader import load_dataset
from ..utils.DataWriter import DataWriter
from itertools import permutations
import numpy as np
from math import factorial
from pprint import pprint


class RoundRobin:
    """ Round-Robin method for TSP

    Notes:
    ------
        You should not use this method beacause this'll take astronomical time.

    Examples:
    ---------
        >>> rr = RoundRobin(dataset_filename="kroA100.tsp")     # You can download the benchmark problem
        >>> rr.search()

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
        self.best_distance = np.inf

    def search(self):
        """ search path"""
        for route in list(permutations([i for i in range(self.CITY_NUM)])):
            distance = self._calculate_distance(route)
            if distance < self.best_distance:
                self.best_distance = distance

    def _calculate_distance(self, route):
        """ calculate distance

        Returns:
        --------
            distance {float} -- distance
        """
        distance = 0
        for i in range(self.CITY_NUM):
            city1 = route[i]
            city2 = route[(i+1) % self.CITY_NUM]
            distance += self.distance_arr[city1, city2]

        return distance