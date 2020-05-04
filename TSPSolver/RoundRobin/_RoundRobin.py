from ..utils.DataLoader import load_dataset
from ..utils.DataWriter import DataWriter
from itertools import permutations
import numpy as np
from math import factorial
from pprint import pprint


class RoundRobin:
    def __init__(self, dataset_filename):
        """

        Arguments:
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
            distance = calculate_distance(route)
            if distance < self.best_distance:
                self.best_distance = distance

    def calculate_distance(self, route):
        """ calculate distance"""
        distance = 0
        for i in range(self.CITY_NUM):
            city1 = route[i]
            city2 = route[(i+1) % self.CITY_NUM]
            distance += self.distance_arr[city1, city2]

        return distance