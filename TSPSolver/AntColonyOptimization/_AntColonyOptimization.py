import numpy as np
from tqdm import tqdm

from ..utils.DataLoader import load_dataset
from ..utils.DataWriter import DataWriter
# from .src.Logger import *
from .src.Agent import Agent, AgentRank


class AntSystem:
    """ The implementation of the most simple Ant Colony Optimization's method, named Ant System(AS).
    AS is the first method which is proposed first.

    Attributes:
    -----------
        ALPHA {float} -- weight of pheromone (default: 1.0)
        BETA {float} -- weight of hueristics (default: 5.0)
        RHO {float} -- rate of reducing pheromone (default: 0.98)
        INIT_PHEROMONE {float} -- initial pheromone concentration (default: 1.0)
        PHEROMONE_Q {float} --  numerator of calculating pheromone increase(default: 1.0)
        IS_SAVE {bool} -- wehther save results or not (default: True)
        CITY_NUM {float} -- the number of cities
        AGENT_NUM {float} -- the number of agents
        agent {Agent} -- each agents' information
        pheromone {np.ndarray} -- pheromone concentration
        distance {np.ndarray} -- distance between cities
        distance_inv {np.ndarray} -- inverse of distance
        best_distance {float} -- the best score
        pre_best_distance {float} -- the best score of previous iteration
        writer {DataWriter} -- writer for saving scores

    Examples:
    ---------
        >>> from TSPSolver.AntColonyOptimization import AntSystem
        >>> ant_system = AntSystem("./kroA100.tsp", 100)            # You can download benchmark problem
        >>> ant_system.search(5)                                    # The search will be run the specified number of times
        >>> ant_system.best_distance
        0      27681.669
        1      27681.669
        2      27570.186
        3      27570.186
        4      27207.674
        >>> ant_system.best_distance
        26277.257
    """

    def __init__(self, dataset_filename, agent_num,
                 alpha=1.0, beta=5.0, rho=0.5, init_pheromone=1.0, pheromone_q=1.0, is_save=True, save_filename="result.csv"):
        """
        Arguments:
        ----------
            dataset_filename {str} -- dataset file name
            agent_num {int} -- the number of agents

        Keyword Arguments:
        ------------------
            alpha {float} -- weight of pheromone (default: 1.0)
            beta {float} -- weight of hueristics (default: 5.0)
            rho {float} -- rate of reducing pheromone (default: 0.98)
            init_pheromone {float} -- initial pheromone concentration (default: 1.0)
            pheromone_q {float} --  numerator of calculating pheromone increase(default: 1.0)
            is_save {bool} -- wehther save results or not (default: True)
            save_filename {str} -- file name of results (default: result.csv)
        """
        city_num, distance = load_dataset(dataset_filename)
        self.CITY_NUM = city_num
        self.AGENT_NUM = agent_num
        self.ALPHA = alpha
        self.BETA = beta
        self.RHO = rho
        self.INIT_PHEROMONE = init_pheromone
        self.PHEROMONE_Q = pheromone_q
        self.IS_SAVE = is_save
        if is_save:
            self.writer = DataWriter(save_filename)

        self.agent = Agent(self.CITY_NUM, self.AGENT_NUM)
        self.pheromone = np.ones((self.CITY_NUM, self.CITY_NUM)) * init_pheromone
        self.distance = distance
        self.distance_inv = 1.0 / pow(distance, self.BETA)
        self.best_distance = np.inf
        self.pre_best_distance = np.inf

    def search(self, iteration, is_judge_convergence=False, convergence_iteration=None):
        """ start searching best route

        Arguments:
        ----------
            iteration {int} -- the number of iterations

        Keyword Arguments:
        ------------------
            is_judge_convergence {bool} -- whether check convergence or not (default: False)
            convergence_iteration {int} -- threshold to consider as converged (default: None)
        """
        if is_judge_convergence and convergence_iteration is None:
            raise Exception("Please set argument: convergence_iteration")

        converge_cnt = 0

        for i in range(iteration):
            self.agent.reset_agent()
            self._generate_route()
            self.agent.find_best()
            self._update_pheromone()

            if self.agent.best_distance < self.best_distance:
                self.best_distance = self.agent.best_distance
                converge_cnt = 0
            elif self.best_distance == self.pre_best_distance:
                converge_cnt += 1
                if converge_cnt == convergence_iteration:
                    print("Converted")
                    break

            print(f"{str(i).rjust(len(str(iteration)))} \t{self.best_distance: .3f}")
            if self.IS_SAVE:
                self.writer.write(self.agent.get_distance_as_arr())

            self.pre_best_distance = self.best_distance

        self.writer.save()

    def _generate_route(self):
        """ generate route"""
        for agent in self.agent:
            start = np.random.randint(0, self.CITY_NUM, 1)[0]
            prob_arr = np.zeros(self.CITY_NUM)
            agent.set_next_city(start)

            for i in range(self.CITY_NUM-1):
                prob_arr *= 0
                for city in range(self.CITY_NUM):
                    if not agent.is_already_visit(city):
                        prob = pow(self.pheromone[city, agent.current_city], self.ALPHA) * self.distance_inv[city, agent.current_city]
                        prob_arr[city] = prob

                rand = np.random.rand()
                for city in range(self.CITY_NUM):
                    if prob_arr[city] == 0:
                        continue

                    prob = prob_arr[:city+1].sum() / prob_arr.sum()
                    if prob > rand:
                        agent.set_next_city(city)
                        break

            self._calculate_distance(agent)

    def _calculate_distance(self, agent):
        """ calculate distance

        Arguments:
        ----------
            agent {Agent} -- agent instance which has already route information
        """
        distance = 0
        for i in range(self.CITY_NUM):
            city1 = agent.route[i]
            city2 = agent.route[(i+1) % self.CITY_NUM]
            distance += self.distance[city1, city2]

        agent.distance = distance

    def _update_pheromone(self):
        """ update pheromone"""
        self.pheromone *= self.RHO

        for agent in self.agent:
            inc = self.PHEROMONE_Q / agent.distance
            for base_city, next_city in agent.get_city_pair():
                self.pheromone[base_city, next_city] += inc
                self.pheromone[next_city, base_city] += inc


class MaxMinAntSystem(AntSystem):
    """ The implementation of one of the best method of ACO, named Max-Min Ant System(MMAS)

    Attributes:
    -----------
        ALPHA {float} -- weight of pheromone (default: 1.0)
        BETA {float} -- weight of hueristics (default: 5.0)
        RHO {float} -- rate of reducing pheromone (default: 0.98)
        INIT_PHEROMONE {float} -- initial pheromone concentration (default: 1.0)
        PHEROMONE_Q {float} --  numerator of calculating pheromone increase(default: 1.0)
        IS_SAVE {bool} -- wehther save results or not (default: True)
        CITY_NUM {float} -- the number of cities
        AGENT_NUM {float} -- the number of agents
        PHEROMONE_MIN_COEF {float} -- coefficient which is used at calculating minimum of pheromone concentration
        agent {Agent} -- each agents' information
        pheromone {np.ndarray} -- pheromone concentration
        distance {np.ndarray} -- distance between cities
        distance_inv {np.ndarray} -- inverse of distance
        best_distance {float} -- the best score
        pre_best_distance {float} -- the best score of previous iteration
        writer {DataWriter} -- writer for saving scores


    Examples:
    ---------
        >>> from TSPSolver.AntColonyOptimization import MaxMinAntSystem
        >>> mmas = MaxMinAntSystem("./kroA100.tsp", 100)            # You can download benchmark problem
        >>> mmas.search(5)                                          # The search will be run the specified number of times
        0      26294.189
        1      26294.189
        2      26294.189
        3      26294.189
        4      26277.257
        >>> ant_system.best_distance
        26277.257
    """

    def __init__(self, dataset_filename, agent_num,
                 alpha=1.0, beta=5.0, rho=0.5, init_pheromone=1.0, pheromone_q=1.0, p_best=0.05, is_save=True, save_filename="result.csv"):
        """
        Arguments:
        ----------
            dataset_filename {str} -- dataset file name
            agent_num {int} -- the number of agents

        Keyword Arguments:
        ------------------
            alpha {float} -- weight of pheromone (default: 1.0)
            beta {float} -- weight of hueristics (default: 5.0)
            rho {float} -- rate of reducing pheromone (default: 0.98)
            init_pheromone {float} -- initial pheromone concentration (default: 1.0)
            pheromone_q {float} --  numerator of calculating pheromone increase(default: 1.0)
            p_best {float} -- parameter for calculating minimum of pheromone (default: 0.05)
            is_save {bool} -- wehther save results or not (default: True)
            save_filename {str} -- file name of results (default: result.csv)
        """
        super(MaxMinAntSystem, self).__init__(dataset_filename, agent_num,
                                              alpha, beta, rho, init_pheromone, pheromone_q,
                                              is_save, save_filename)

        self.PHEROMONE_MIN_COEF = pow(p_best, 1.0/self.CITY_NUM)

    def _update_pheromone(self):
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
    """ The implementation of one of the best method of ACO, named Max-Min Ant System(MMAS)

    Attributes:
    -----------
        ALPHA {float} -- weight of pheromone (default: 1.0)
        BETA {float} -- weight of hueristics (default: 5.0)
        RHO {float} -- rate of reducing pheromone (default: 0.98)
        INIT_PHEROMONE {float} -- initial pheromone concentration (default: 1.0)
        PHEROMONE_Q {float} --  numerator of calculating pheromone increase(default: 1.0)
        IS_SAVE {bool} -- wehther save results or not (default: True)
        CITY_NUM {float} -- the number of cities
        AGENT_NUM {float} -- the number of agents
        PHEROMONE_MIN_COEF {float} -- coefficient which is used at calculating minimum of pheromone concentration
        agent {AgentRank} -- each agents' information with rank information
        pheromone {np.ndarray} -- pheromone concentration
        distance {np.ndarray} -- distance between cities
        distance_inv {np.ndarray} -- inverse of distance
        best_distance {float} -- the best score
        pre_best_distance {float} -- the best score of previous iteration
        writer {DataWriter} -- writer for saving scores


    Examples:
    ---------
        >>> from TSPSolver.AntColonyOptimization import AntSystemElute
        >>> as_elite = AntSystemElite("./kroA100.tsp", 100)             # You can download benchmark problem
        >>> as_elite.search(5)                                          # The search will be run the specified number of times
        0      26294.189
        1      26294.189
        2      26294.189
        3      26294.189
        4      26277.257
        >>> ant_system.best_distance
        26277.257
    """
    def __init__(self, dataset_filename, agent_num,
                 alpha=1.0, beta=5.0, rho=0.5, init_pheromone=1.0, pheromone_q=1.0, is_save=True, save_filename="result.csv"):
        """
        Arguments:
        ----------
            dataset_filename {str} -- dataset file name
            agent_num {int} -- the number of agents

        Keyword Arguments:
        ------------------
            alpha {float} -- weight of pheromone (default: 1.0)
            beta {float} -- weight of hueristics (default: 5.0)
            rho {float} -- rate of reducing pheromone (default: 0.98)
            init_pheromone {float} -- initial pheromone concentration (default: 1.0)
            pheromone_q {float} --  numerator of calculating pheromone increase(default: 1.0)
        """
        super(AntSystemElite, self).__init__(dataset_filename, agent_num, alpha, beta, rho, init_pheromone, pheromone_q)
        self.agent = AgentRank(self.CITY_NUM, self.AGENT_NUM)