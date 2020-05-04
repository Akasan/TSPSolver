from ..utils.DataLoader import load_dataset
from ..utils.DataWriter import DataWriter
import numpy as np
from random import shuffle


class InsertionBase:
    def __init__(self, dataset_filename):
        """
        Arguments:
            dataset_filename {str} -- dataset file name
        """
        city_num, distance = load_dataset(dataset_filename)
        self.CITY_NUM = city_num
        self.distance = distance
        self.writer = DataWriter()
        self.best_distance = np.inf

    def select_next(self):
        """ function for selecting next city (this function is implemented in each Child Class)"""
        pass

    def generate_route(self):
        """ generate route"""
        for i in range(self.CITY_NUM-1):
            next_city = self.select_next()
            self.append_city(next_city)

    def append_city(self, next_city):
        """ append next city to route

        Arguments:
            next_city {int} -- next city
        """
        length = len(self.route)

        if length <= 2:
            self.route.append(next_city)
        else:
            best_distance = np.inf
            best_route = None
            for pos in range(length):
                route_cp = self.route.copy()
                route_cp.insert(pos, next_city)
                distance = self.calculate_distance(route_cp)

                if distance < best_distance:
                    best_distance = distance
                    best_route = route_cp

            self.route = best_route

    def calculate_distance(self, route):
        """ calculate distance

        Arguments:
            route {list[int]} -- route

        Returns:
            {float} -- distance of route
        """
        distance = 0
        length = len(route)
        for i in range(length):
            city1 = route[i]
            city2 = route[(i+1) % length]
            distance += self.distance[city1, city2]

        return distance


class RandomInsertion(InsertionBase):
    def __init__(self, dataset_filename):
        """
        Arguments:
            dataset_filename {str} -- dataset file name
        """
        super(RandomInsertion, self).__init__(dataset_filename)

    def search(self, iteration):
        """ start searching

        Arguments:
            iteration {int} -- the number of iterations
        """
        for i in range(iteration):
            self.route = [np.random.randint(0, self.CITY_NUM, 1)[0]]
            self.generate_route()

            distance = self.calculate_distance(self.route)
            if distance < self.best_distance:
                self.best_distance = distance

            print(i, self.best_distance)

    def select_next(self):
        """ select next city

        Returns:
            {int} -- id of next city
        """
        city_list = [i for i in range(self.CITY_NUM)]
        shuffle(city_list)
        for city in city_list:
            if not city in self.route:
                return city


class NearestInsertion(InsertionBase):
    def search(self):
        """ start searching"""
        for i in range(self.CITY_NUM):
            self.route = [i]
            self.generate_route()

            distance = self.calculate_distance(self.route)
            if distance < self.best_distance:
                self.best_distance = distance

            print(i, self.best_distance)

    def select_next(self):
        """ select the next city

        Returns:
            {int} -- id of next city
        """
        distance_min = np.inf
        idx = None
        for city in self.route:
            distance_dict = {k: v for k, v in zip(range(self.CITY_NUM), self.distance[city, :]) if v > 0}
            for k, v in sorted(distance_dict.items(), key=lambda x: x[1]):
                if v < distance_min and not k in self.route:
                    distance_min = v
                    idx = k
                    break

        return idx


class FarthestInsertion(NearestInsertion):
    def select_next(self):
        """ select the next city

        Returns:
            {int} -- id of next city
        """
        distance_min = 0
        idx = None
        for city in self.route:
            distance_dict = {k: v for k, v in zip(range(self.CITY_NUM), self.distance[city]) if v > 0}
            for k, v in sorted(distance_dict.items(), key=lambda x: -x[1]):
                if v > distance_min and not k in self.route:
                    distance_min = v
                    idx = k
                    break

        return idx

class CheapestInsertion(InsertionBase):
    pass