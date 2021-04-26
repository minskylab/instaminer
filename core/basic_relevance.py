from math import log


def basic_relevance(likes: int, comments: int) -> float:
    return _consume(likes, comments)


def _consume(l: int, c: int) -> float:
    l += 1  # not zero
    c += 1
    alpha_l = 0.32
    alpha_c = 0.18
    delta = 0.98
    nl = log(l)/log(7)
    nc = log(c)/log(10)
    v = alpha_l * nl + alpha_c * nc
    v *= delta
    v += 0.99 - delta
    if v > 1.0:
        v = 0.99
    return v
