class AgentBase:
    def __init__(self, city_num):
        """
        Arguments:
            city_num {int} -- the number of cities
        """
        self.CITY_NUM = city_num
        self.reset_values()

    def reset_values(self):
        """reset all variables"""
        self.distance = 0
        self.route = []

    @property
    def current_city(self):
        return self.route[-1]

    def get_current_city(self):
        """ get agent's current city

        Returns:
            {int} -- agent's curent city
        """
        return self.route[-1]

    def set_next_city(self, city):
        """ go to next city

        Arguments:
            city {int} -- next city
        """
        self.route.append(city)

    def is_already_visit(self, city):
        """ check whether specified city is already visited

        Returns:
            {bool} -- True when specified city is already visited
        """
        return True if city in self.route else False

    def get_city(self):
        """ yield each city

        Yields:
            {int} -- city
        """
        for city in route:
            yield city

    def get_city_pair(self):
        """ yield city pair

        Yields:
            {int} -- base city
            {int} -- city next to base city
        """
        for i in range(self.CITY_NUM):
            city1 = self.route[i]
            city2 = self.route[(i+1)%self.CITY_NUM]
            yield city1, city2


class Agent:
    def __init__(self, city_num, agent_num):
        """
        Arguments:
            city_num {int} -- the number of cities
            agent_num {int} -- the number of agents
        """
        self.CITY_NUM = city_num
        self.agent = [AgentBase(city_num) for _ in range(city_num)]

    def __iter__(self):
        """ iterator for getting each agent's instance

        Returns:
            {iter(AgentBase)} -- each agent's instance
        """
        return iter(self.agent)

    def __getitem__(self, idx):
        """ return agent instance spcified index

        Arguments:
            idx {int} -- agent id

        Returns:
            [type] -- [description]
        """
        return self.agent[idx]

    def reset_agent(self):
        """reset all agents' instance"""
        for agent in self.agent:
            agent.reset_values()

    def find_best(self):
        """ find the best result"""
        distance = [agent.distance for agent in self.agent]
        self.best_distance = min(distance)
        best_idx = distance.index(self.best_distance)
        self.best_route = self.agent[best_idx].route

    def get_best_route_pair(self):
        """ get pair of the best route

        Yields:
            {int} -- base city
            {int} -- city next to base city
        """
        for i in range(self.CITY_NUM):
            city1 = self.best_route[i]
            city2 = self.best_route[(i+1)%self.CITY_NUM]
            yield city1, city2

    def get_distance_as_arr(self):
        """ get array of distance"""
        return [agent.distance for agent in self.agent]


class AgentRank(Agent):
    def __init__(self, city_num, agent_num):
        """
        Arguments:
            city_num {int} -- the number of cities
            agent_num {int} -- the number of agents
        """
        super(AgentRank, self).__init__(city_num, agent_num)
        self.rank = [-1 for _ in range(agent_num)]

    def get_rank(self):
        """ calculate agents' rank"""
        rank_dict = {k: agent.distance for k, agent in zip(range(self.CITY_NUM), self.agent)}
        rank_dict_sorted = dict(sorted(rank_dict.items(), key=lambda x: x[1]))

        self.rank = {}
        rank = 0
        for i, (k, v) in enumerate(rank_dict_sorted.items()):
            if i == 0:
                self.rank[rank] = {"VALUE": v, "ID": [k]}
                continue

            if v == self.rank[rank]["VALUE"]:
                self.rank[rank]["ID"].append(k)

            else:
                rank += 1
                self.rank[rank] = {"VALUE": v, "ID": [k]}

    def get_rank_base(self):
        """ get agent's ID according to ranking made by get_rank function

        Yields:
            {list[int]} -- ID list which has same distance
        """
        for k, v in self.rank.item():
            yield v["ID"]