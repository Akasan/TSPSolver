def float_range(_min, _max, step_size=None, step_num=None, round_pos=5, is_ascending=True):
    """ iterator for providing range that data-type is float

    Arguments:
    ----------
        _min {float} -- minimum boundary value
        _max {float} -- maximum boundary value

    Keyword Arguments:
    ------------------
        step_size {int} -- how much you want to step (default: None)
        step_num {float} -- the number of dicision (default: None)
        round_pos {int} -- which position to round error (default: 5)
        is_ascending {bool} -- if you want to sort in ascending order, set this as True (default: True)

    Returns:
    --------
        value {list[float]} -- value list

    Examples:
    ---------
        >>> ...
    """
    if step_size is not None:
        step_num = int((_max - _min) / step_size) + 1

    elif step_num is not None:
        step_size = (_max - _min) / step_num

    if is_ascending:
        value = [round(_min + step_size * i, round_pos) for i in range(step_num)]
    else:
        value = [round(_max - step_size * i, round_pos) for i in range(step_num)]

    return value