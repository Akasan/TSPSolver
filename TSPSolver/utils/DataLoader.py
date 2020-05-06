import numpy as np
import re
from pprint import pprint


def load_dataset(dataset_filename):
    """ load dataset

    Arguments:
    ----------
        dataset_filename {str} -- dataset file name

    Returns:
    --------
        city_num {int} -- the number of city
        distance {np.ndarray} -- distance array

    Examples:
    ---------
        >>> city_num, distasnce = load_dataset("kroA100.tsp")
        >>> city_num
        100
        >>> type(distance)
        <class 'numpy.ndarray'>
        >>> distance.shape
        (100, 100)
    """
    city_cnt = 0
    with open(dataset_filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines()):
            if i <= 2:
                continue

            elif i == 3:
                city_num = int(line.strip().split(" ")[-1])
                distance = np.zeros((city_num, city_num))
                city_info = np.zeros((city_num, 2))

            elif 6 <= i <= city_num + 5:
                split = re.sub(r"\s+", " ", line.strip()).split(" ")
                city_info[city_cnt][0] = int(split[-2])
                city_info[city_cnt][1] = int(split[-1])
                city_cnt += 1

    for i in range(city_num):
        for j in range(i+1, city_num):
            dis = pow(pow(city_info[i][0] - city_info[j][0], 2.0) + pow(city_info[i][1] - city_info[j][1], 2.0), 0.5)
            distance[i, j] = dis
            distance[j, i] = dis

        distance[i, i] = -1

    return city_num, distance