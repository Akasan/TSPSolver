from itertools import product
from ..utils.FloatRange import float_range
from ._AntColonyOptimization import AntSystem, MaxMinAntSystem


class GridSearch:
    """ Grid Search(GS) method for AntColonyOptimization.
    You can use GS for testing parameters combination which is suit for particular problem.

    Attributes:
    -----------
        __MODE {dict} -- dictionary for selecting mode (which ACO method will be used)
        param_grid {dict} -- parameter grid
        alpha_range {list[float]} -- list of value for ALPHA
        beta_range {list[float]} -- list of value for BETA
        rho_range {list[float]} -- list of value for RHO
        agent_num_range {list[float]} -- list of value for AGENT_NUM

    Examples:
    ---------
        >>> param_grid = {"alpha": {"min": 1.0, "max": 3.0, "interval": 0.5},
        ...               "beta": {"min": 1.0, "max": 5.0, "interval": 0.5},
        ...               "rho": {"min": 0.5, "max": 0.98, "interval": 0.25},
        ...               "agent_num": {"value": 100}}
        >>> gs = GridSearch(param_grid)
        >>> gs.search(iteration=1, dataset_filename="./kroA100.tsp", mode="AntSystem")
        alpha: 1.0, beta: 1.0, rho: 0.5, agent: 100
        0        94056.455
        alpha: 1.0, beta: 1.0, rho: 0.75, agent: 100
        0        94598.195
        alpha: 1.0, beta: 1.5, rho: 0.5, agent: 100
        0        68395.391
        alpha: 1.0, beta: 1.5, rho: 0.75, agent: 100
        0        70948.872
    """

    __MODE = {"AntSystem": AntSystem, "MaxMinAntSystem": MaxMinAntSystem}

    def __init__(self, param_grid):
        """
        Arguments:
        ----------
            param_grid {dict} -- parameter grid
        """
        self.param_grid = param_grid
        self._parse_param_grid()

    def _parse_param_grid(self):
        """ parse param_grid"""
        alpha_info = self.param_grid["alpha"]
        beta_info = self.param_grid["beta"]
        rho_info = self.param_grid["rho"]
        agent_num_info = self.param_grid["agent_num"]

        self.alpha_range = self._get_range(alpha_info)
        self.beta_range = self._get_range(beta_info)
        self.rho_range = self._get_range(rho_info)
        self.agent_num_range = self._get_range(agent_num_info)

    def search(self, iteration, dataset_filename, mode="AntSystem"):
        """ start searching

        Arguments:
        ----------
            iteration {int} -- the number of iteration
            dataset_filename {str} -- dataset file name

        Keyword Arguments:
        ------------------
            mode {str} -- ACO mode (default: "AntSystem")
        """
        param_list = product(self.alpha_range, self.beta_range, self.rho_range, self.agent_num_range)
        for alpha, beta, rho, agent_num in param_list:
            print(f"alpha: {alpha}, beta: {beta}, rho: {rho}, agent: {agent_num}")
            system = self.__MODE[mode](dataset_filename, agent_num, alpha, beta, rho)
            system.search(iteration)

    @staticmethod
    def _get_range(info):
        """ get range from param_grid

        Returns:
        --------
            {list[float]} -- value list
        """
        if "value" in info:
            return [info["value"]]
        else:
            if "interval" in info:
                return float_range(_min=info["min"], _max=info["max"], step_size=info["interval"])
            elif "num" in info:
                return float_range(_min=info["min"], _max=info["max"], step_num=info["num"])