from itertools import chain, groupby
from operator import attrgetter
import random as random_mod


def weighted_pick(x, key_weight=None):
    """Returns one element from the sequence x.
    A "heavy" element is more likely to be picked.
    The `key_weight` argument can be used to define how to access the element's weight.
    By default, we assume x to be a sequence of (element, weight) tuples.
    """
    if key_weight is None:
        key_weight = lambda t: t[1]
    
    total_weights = sum(key_weight(e) for e in x)
    target = random_mod.randint(0, total_weights)
    for e in x:
        target -= e[1]
        if target <= 0:
            return e[0]


def weighted_shuffle(x, key_weight=None):
    """Shuffles the sequence x in place.
    Elements that are "heavier" will be more likely to be at the beginning.
    The `key_weight` argument can be used to define how to access the element's weight.
    By default, we assume x to be a sequence of (element, weight) tuples.
    """
    if key_weight is None:
        key_weight = lambda t: t[1]
    
    weights = [(i, key_weight(e)) for e in enumerate(x)]
    
    for i in reversed(xrange(1, len(x))):
        j = weighted_pick(weights[:i+1])
        x[i], x[j] = x[j], x[i]


def shuffled(iterable, weight=None):
    """
    Return a shuffled copy of the given iterable.
    If a callable is passed for `weight`, then a weighted_shuffle will be used.
    If not, a plain random.shuffle will be used.
    """
    l = list(iterable)  # copy
    if weight is None:
        random_mod.shuffle(l)
    else:
        weighted_shuffle(l, key_weight=weight)
    return l


def sequential(elements, key=attrgetter('position')):
    return sorted(elements, key=key)


def random(elements):
    return shuffled(elements)


def weighted_random(elements, key=attrgetter('position')):
    l = list(elements)
    weighted_shuffle(l, key_weight=key)
    return l


def cluster_random(elements, key=attrgetter('position')):
    ordered = sorted(elements, key=key)
    grouped = groupby(ordered, key=key)
    clustered = chain.from_iterable(shuffled(elements) for _, elements in grouped)
    return list(clustered)
