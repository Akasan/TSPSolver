import random


def _make_rank(fitness):
    """ make ranking according to fitness

    Arguments:
    ----------
        fitness {list[float]} -- each indivisuals' fitness

    Returns:
    --------
        rank {list[int]} -- rank

    Examples:
    ---------
        >>> fitness = [5, 3, 4, 1, 2]
        >>> rank = _make_rank(fitness)
        >>> rank
        [3, 4, 1, 2, 0]
    """
    rank_dict = {i: _fitness for i, _fitness in enumerate(fitness)}
    rank = []
    for k, _ in sorted(rank_dict.items(), key=lambda x: x[1]):
        rank.append(k)

    return rank


def _calculate_probability(fitness):
    """ calculate probability.

    Arguments:
    ----------
        fitness {list[float]} -- each indivisuals' fitness

    Returns:
    --------
        prob {list[float]} -- each indivisuals' probability for selecting

    Examples:
    ---------
        >>> fitness = [1, 2, 3, 4]
        >>> prob = _calculate_probability(fitness)
        >>> prob
        [0.1, 0.2, 0.3, 0.4]
    """
    prob_sum = sum(fitness)
    prob = []
    for _fitness in fitness:
        prob.append(_fitness/prob_sum)

    return prob


def elite_selection(fitness, num):
    """ select according elite strategy

    Arguments:
    ----------
        fitness {list[float]} -- list of each indivisual's fitness
        num {int} -- the number of indivisuals which will be selected

    Returns:
    --------
        rank {list[int]} -- selected indivisuals' id
    """
    rank = _make_rank(fitness)
    return rank[:num]


def roulette_selection(fitness, num):
    prob = _calculate_probability(fitness)


def ranking_selection(fitness, num):
    pass


def tournament_selection(fitness, num, tournament_size):
    base = [i for i in range(len(fitness))]
    result = []

    for i in range(num):
        cand = random.sample(base, tournament_size)
        cand_value = [fitness[_cand] for _cand in cand]
        max_value = max(cand_value)
        max_idx = cand_value.index(max_value)
        result.append(max_idx)

    return result