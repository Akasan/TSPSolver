import numpy as np


class Gene:
    """ Gene class

    Attributes:
    -----------
        CITY_NUM {int} -- the number of cities
        GENE_SIZE {int} -- gene size
        gene {np.ndarray} -- gene representation
        route {list[int]} -- route converted from gene
    """

    def __init__(self, gene_size, city_num):
        """
        Arguments:
        ----------
            gene_size {int} -- size of gene
            city_num {int} -- the number of cities
        """
        self.CITY_NUM = city_num
        self.GENE_SIZE = gene_size
        self._initialize_gene()

    def _initialize_gene(self):
        """ initialize gene information"""
        self.gene = np.zeros(self.GENE_SIZE, dtype=np.int32)

        for i in range(self.GENE_SIZE):
            gene = np.random.randint(0, self.GENE_SIZE-i, 1)[0]
            self.gene[i] = int(gene)

    def get_route_pair(self):
        self._convert_to_route()
        for i in range(self.CITY_NUM):
            city1 = self.route[i]
            city2 = self.route[(i+1)%self.CITY_NUM]
            yield city1, city2

    def _convert_to_route(self):
        city = [i for i in range(self.CITY_NUM)]
        self.route = []
        for g in self.gene:
            next_city = city[g]
            del city[g]
            self.route.append(next_city)