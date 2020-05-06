import random


def mutate(gene, threshold):
    """ mutate gene

    Arguments:
    ----------
        gene {list[int]} -- gene
        threshold {float} -- threshold for mutating

    Returns:
    --------
        new_gene {list[int]} -- new gene

    Examples:
    ---------
        >>> gene = [4, 3, 2, 1, 0]
        >>> for _ in range(5):
        ...     new_gene = mutate(gene, 0.5)
        ...     print(new_gene)
        [0, 3, 2, 1, 0]
        [4, 3, 2, 1, 0]
        [4, 3, 2, 1, 0]
        [2, 3, 2, 1, 0]
        [4, 0, 2, 1, 0]
        >>> for _ in range(5):
        ...     new_gene = mutate(gene, 0.1)        # change thresold to 0.1
        ...     print(new_gene)
        [4, 2, 2, 1, 0]
        [4, 3, 0, 1, 0]
        [4, 1, 2, 1, 0]
        [4, 0, 2, 1, 0]
        [2, 3, 2, 1, 0]
        >>> for _ in range(5):
        ...     new_gene = mutate(gene, 0.9)        # change thresold to 0.9
        ...     print(new_gene)
        [2, 3, 2, 1, 0]
        [4, 3, 2, 1, 0]
        [4, 3, 2, 1, 0]
        [4, 3, 2, 1, 0]
        [4, 3, 2, 1, 0]]
    """
    mutate_prob = random.random()
    if mutate_prob < threshold:
        new_gene = gene

    else:
        length = len(gene)
        mutate_pos = random.randint(0, length-2)

        new_gene = gene.copy()
        while True:
            new_value = random.randint(0, length-mutate_pos-1)
            if not new_value == gene[mutate_pos]:
                new_gene[mutate_pos] = new_value
                break

    return new_gene