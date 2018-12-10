def manhattan_distance(x: list, y: tuple) -> int:
    '''
    This is simply the Manhattan distance, which makes the most sense since our areas are just basically squares and
    pollinator_types can only move in an ordinal diretion. For this application, these should  be integers, in order
    to give a proper integer answer, though in true manhattan distance this doesn't have to be the case, necessarily.
    As such, I will assert that they are integers just to be complete
    :param x: the current position in the form of a list
    :param y: the current position in the form of a tuple, The only reason this is a tuple and not a list is because
    that's how I set it up in the indices list in the pollinator's class. This would work perfectly fine as a list
    too, since the only thing returned is an integer.
    :return: an integer giving the manhattan distance. Since these are square areas basically it's the number of
    'moves' it takes to get from point x to point y.
    >>> manhattan_distance([5, 0], (-1, 3))
    9
    '''
    # assert type(x[0]) is int and type(x[1]) is int and type(y[0]) is int and type(y[1]) is int
    return abs(x[0] - y[0]) + abs(x[1] - y[1])