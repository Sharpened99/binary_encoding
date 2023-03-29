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


def count_tokens(num: int) -> int:
    tokens = 0
    while num != 0:
        tokens += num & 1
        num >>= 1

    return tokens


def rotate_left(x: int, max_bits: int, n = 1) -> int:
    while n > 0:
        x <<= 1
        if x & 2 ** max_bits != 0:
            x &= 2 ** max_bits - 1
            x |= 1
        n -= 1
    return x


def rotate_right(x: int, max_bits: int, n = 1) -> int:
    while n > 0:
        if x & 1 != 0:
            x |= 2 ** max_bits
        x >>= 1
        n -= 1
    return x


def zero_pad_to_len(s: str, length: int) -> str:
    while len(s) < length:
        s = "0" + s
    return s
