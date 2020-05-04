import numpy as np
from tqdm import tqdm
from .src.Logger import *
from .src.Agent import Agent, AgentRank
from ..utils.DataLoader import load_dataset
from ..utils.DataWriter import DataWriter


class AntSystem:
    def __init__(self, dataset_filename, agent_num,
                 alpha=1.0, beta=5.0, rho=0.5, init_pheromone=1.0, pheromone_q=1.0):
        """
        Arguments:
            dataset_filename {str} -- dataset file name
            agent_num {int} -- the number of agents

        Keyword Arguments:
            alpha {float} -- weight of pheromone (default: 1.0)
            beta {float} -- weight of hueristics (default: 5.0)
            rho {float} -- rate of reducing pheromone (default: 0.98)
            init_pheromone {float} -- initial pheromone concentration (default: 1.0)
            pheromone_q {float} --  numerator of calculating pheromone increase(default: 1.0)
        """
        city_num, distance = load_dataset(dataset_filename)
        self.CITY_NUM = city_num
        self.AGENT_NUM = agent_num
        self.ALPHA = alpha
        self.BETA = beta
        self.RHO = rho
        self.INIT_PHEROMONE = init_pheromone
        self.PHEROMONE_Q = pheromone_q

        self.agent = Agent(self.CITY_NUM, self.AGENT_NUM)
        self.pheromone = np.ones((self.CITY_NUM, self.CITY_NUM)) * init_pheromone
        self.distance = distance
        self.distance_inv = 1.0 / distance
        self.best_distance = np.inf

        self.writer = DataWriter()

    def search(self, iteration):
        """ start searching best route

        Arguments:
            iteration {int} -- the number of iterations
        """
        for i in tqdm(range(iteration)):
            self.agent.reset_agent()
            self.generate_route()
            self.agent.find_best()
            self.update_pheromone()
            if self.agent.best_distance < self.best_distance:
                self.best_distance = self.agent.best_distance

            info(str(self.best_distance))
            self.writer.write(self.agent.get_distance_as_arr())

        self.writer.save()

    def generate_route(self):
        """ generate route"""
        for agent in self.agent:
            start = np.random.randint(0, self.CITY_NUM, 1)[0]
            prob_arr = np.zeros(self.CITY_NUM)
            agent.set_next_city(start)

            for i in range(self.CITY_NUM-1):
                prob_arr *= 0
                for city in range(self.CITY_NUM):
                    if not agent.is_already_visit(city):
                        prob = pow(self.pheromone[city, agent.current_city], self.ALPHA) * pow(self.distance_inv[city, agent.current_city], self.BETA)
                        prob_arr[city] = prob

                rand = np.random.rand()
                for city in range(self.CITY_NUM):
                    if prob_arr[city] == 0:
                        continue

                    prob = prob_arr[:city+1].sum() / prob_arr.sum()
                    if prob > rand:
                        agent.set_next_city(city)
                        break

            self.calculate_distance(agent)

    def calculate_distance(self, agent):
        """ calculate distance

        Arguments:
            agent {Agent} -- agent instance which has already route information
        """
        distance = 0
        for i in range(self.CITY_NUM):
            city1 = agent.route[i]
            city2 = agent.route[(i+1) % self.CITY_NUM]
            distance += self.distance[city1, city2]

        agent.distance = distance

    def update_pheromone(self):
        """ update pheromone"""
        self.pheromone *= self.RHO

        for agent in self.agent:
            inc = self.PHEROMONE_Q / agent.distance
            for base_city, next_city in agent.get_city_pair():
                self.pheromone[base_city, next_city] += inc
                self.pheromone[next_city, base_city] += inc

class MaxMinAntSystem(AntSystem):
    def __init__(self, dataset_filename, agent_num,
                 alpha=1.0, beta=5.0, rho=0.5, init_pheromone=1.0, pheromone_q=1.0, p_best=0.05):
        """
        Arguments:
            dataset_filename {str} -- dataset file name
            agent_num {int} -- the number of agents

        Keyword Arguments:
            alpha {float} -- weight of pheromone (default: 1.0)
            beta {float} -- weight of hueristics (default: 5.0)
            rho {float} -- rate of reducing pheromone (default: 0.98)
            init_pheromone {float} -- initial pheromone concentration (default: 1.0)
            pheromone_q {float} --  numerator of calculating pheromone increase(default: 1.0)
            p_best {float} -- parameter for calculating minimum of pheromone (default: 0.05)
        """
        super(MaxMinAntSystem, self).__init__(dataset_filename, agent_num,
                                              alpha, beta, rho, init_pheromone, pheromone_q)

        self.PHEROMONE_MIN_COEF = pow(p_best, 1.0/self.CITY_NUM)

    def update_pheromone(self):
        """ update pheromone(There're maimum and minimum value of pheromone)"""
        self.pheromone *= self.RHO
        pheromone_max = 1.0 / ((1 - self.RHO) * self.agent.best_distance)
        pheromone_min = pheromone_max * (1-self.PHEROMONE_MIN_COEF) / ((self.CITY_NUM / 2 - 1)*self.PHEROMONE_MIN_COEF)
        inc = self.PHEROMONE_Q / self.agent.best_distance
        for base_city, next_city in self.agent.get_best_route_pair():
            self.pheromone[base_city, next_city] += inc
            self.pheromone[next_city, base_city] += inc

        self.pheromone[self.pheromone > pheromone_max] = pheromone_max
        self.pheromone[self.pheromone < pheromone_min] = pheromone_min


class AntSystemElite(AntSystem):
    def __init__(self, dataset_filename, agent_num,
                 alpha=1.0, beta=5.0, rho=0.98, init_pheromone=1.0, pheromone_q=1.0, p_best=0.05):
        """
        Arguments:
            dataset_filename {str} -- dataset file name
            agent_num {int} -- the number of agents

        Keyword Arguments:
            alpha {float} -- weight of pheromone (default: 1.0)
            beta {float} -- weight of hueristics (default: 5.0)
            rho {float} -- rate of reducing pheromone (default: 0.98)
            init_pheromone {float} -- initial pheromone concentration (default: 1.0)
            pheromone_q {float} --  numerator of calculating pheromone increase(default: 1.0)
        """
        super(AntSystemElite, self).__init__(dataset_filename, agent_num,
                                             alpha, beta, rho, init_pheromone, pheromone_q)

        self.agent = AgentRank(self.CITY_NUM, self.AGENT_NUM)