def fact(n: int) -> int:
    prod = 1
    for i in range(1, n + 1):
        prod *= i
    return prod


def n_choose_k(n: int, k: int) -> int:
    if n < k:
        raise AttributeError("n must be smaller or equal to k;", n, k)
    return int(
        fact(n) /
        (fact(k) * fact(n - k)
         )
    )
