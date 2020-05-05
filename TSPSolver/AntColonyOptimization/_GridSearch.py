from itertools import product
from ..utils.FloatRange import float_range
from ._AntColonyOptimization import AntSystem, MaxMinAntSystem


class GridSearch:
    __MODE = {"AntSystem": AntSystem, "MaxMinAntSystem": MaxMinAntSystem}

    def __init__(self, param_grid):
        """[summary]

        Arguments:
            param_grid {[type]} -- [description]
        """
        self.param_grid = param_grid
        self._parse_param_grid()

    def _parse_param_grid(self):
        alpha_info = self.param_grid["alpha"]
        beta_info = self.param_grid["beta"]
        rho_info = self.param_grid["rho"]
        agent_num_info = self.param_grid["agent_num"]

        self.alpha_range = self._get_range(alpha_info)
        self.beta_range = self._get_range(beta_info)
        self.rho_range = self._get_range(rho_info)
        self.agent_num_range = self._get_range(agent_num_info)

    def search(self, iteration, dataset_filename, mode="AntSystem"):
        for alpha, beta, rho, agent_num in product(self.alpha_range, self.beta_range, self.rho_range, self.agent_num_range):
            print(f"alpha: {alpha}, beta: {beta}, rho: {rho}, agent: {agent_num}")
            system = self.__MODE[mode](dataset_filename,
                                       agent_num,
                                       alpha, beta, rho)
            system.search(iteration)

    @staticmethod
    def _get_range(info):
        if "value" in info:
            return [info["value"]]
        else:
            if "interval" in info:
                return float_range(_min=info["min"], _max=info["max"], step_size=info["interval"])
            elif "num" in info:
                return float_range(_min=info["min"], _max=info["max"], step_num=info["num"])