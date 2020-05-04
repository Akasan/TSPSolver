import numpy as np
import re
from pprint import pprint


def load_dataset(dataset_filename):
    """ load dataset

    Arguments:
        dataset_filename {str} -- dataset file name

    Returns:
        {int} -- the number of city
        {np.ndarray} -- distance array
    """
    city_cnt = 0
    with open(dataset_filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f.readlines()):
            if i <= 2:
                continue

            elif i == 3:
                CITY_NUM = int(line.strip().split(" ")[-1])
                distance = np.zeros((CITY_NUM, CITY_NUM))
                city_info = np.zeros((CITY_NUM, 2))

            elif 6 <= i <= CITY_NUM + 5:
                split = re.sub(r"\s+", " ", line.strip()).split(" ")
                city_info[city_cnt][0] = int(split[-2])
                city_info[city_cnt][1] = int(split[-1])
                city_cnt += 1

    for i in range(CITY_NUM):
        for j in range(i+1, CITY_NUM):
            dis = pow(pow(city_info[i][0] - city_info[j][0], 2.0) + pow(city_info[i][1] - city_info[j][1], 2.0), 0.5)
            distance[i, j] = dis
            distance[j, i] = dis

        distance[i, i] = -1

    return CITY_NUM, distance