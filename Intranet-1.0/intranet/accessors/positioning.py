# -*- coding: utf-8 -*-


def calc_places(existing_places, position, item_count=1, distance=1024.0):
    """
    Calculate the places of new items in order to insert them after a given position.

    Insert exactly at the position (or distance if position is ``None``):

    >>> calc_places([], 0)
    [0.0]
    >>> calc_places([], 100)
    [100.0]
    >>> calc_places([], -100)
    [-100.0]
    >>> calc_places([], None)
    [1024.0]
    >>> calc_places([], None, item_count=3, distance=100)
    [100.0, 200.0, 300.0]

    Insert after the position or before if the position is negative:

    >>> calc_places([0], 0)
    [1024.0]
    >>> calc_places([0], 100)
    [1024.0]
    >>> calc_places([0], -100)
    [-1024.0]
    >>> calc_places([0], None)
    [1024.0]
    >>> calc_places([0], None, item_count=3, distance=100)
    [100.0, 200.0, 300.0]
    >>> calc_places([1024], None, item_count=3)
    [2048.0, 3072.0, 4096.0]
    >>> calc_places([1024, 2048], None)
    [3072.0]

    Insert in the interval:

    >>> calc_places([1, 2], 1)
    [1.5]
    >>> calc_places([1, 2], 1.25)
    [1.5]
    >>> calc_places([1, 2], 1.5)
    [1.5]
    >>> calc_places([1, 2], 1.75)
    [1.5]
    >>> calc_places([1, 2], 2)
    [1026.0]
    >>> calc_places([1, 2], 1, item_count=3)
    [1.25, 1.5, 1.75]
    >>> calc_places([1, 14], 1, item_count=12)
    [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0]

    :type existing_places: list[int or float]
    :param existing_places: list of existing positions.
    :type position: int or float or None
    :param position: Insertion point, after the last position if ``None``.
    :type item_count: int
    :param item_count: Number of items to insert, at least one.
    :type distance: int or float
    :param distance: minimum distance between two consecutive items for insterting at start or end position.
    :rtype: list[int or float]
    :return: list of new positions.
    """
    origin = distance if position is None else position
    last = max(existing_places) if existing_places else origin
    position = last if position is None else origin
    before = [p for p in existing_places if p <= position]
    after = [p for p in existing_places if p > position]
    if after and before:
        # -- insert between
        start = max(before)
        end = min(after)
    elif before:
        # -- insert after
        start = max(before)
        end = start + distance * (item_count + 1)
    elif after:
        # -- insert before
        end = min(after)
        start = end - distance * (item_count + 1)
    else:
        # -- create new places from origin
        start = position - distance
        end = start + distance * (item_count + 1)
    k = 1.0 * (end - start) / (item_count + 1)
    return [start + k * (idx + 1) for idx in range(item_count)]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
