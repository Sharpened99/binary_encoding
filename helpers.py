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
    """
    count bits set to one in num.
    """
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


def get_overlap(x: int, y: int) -> int:
    """
    count the bits to set to one in (x & y).
    """
    count = 0
    while x > 0 and y > 0:
        count += (x & 1) & (y & 1)
        x >>= 1
        y >>= 1

    return count


def zero_pad_to_len(s: str, length: int) -> str:
    """
    leftpads s to given length with zero.
    """
    while len(s) < length:
        s = "0" + s
    return s


def get_max_dec_len(bits) -> int:
    return len(str(2 ** bits))


def get_n_token_numbers(rotation_tokens: int, bits: int) -> list:
    min_num = 2 ** rotation_tokens - 1
    n_token_numbers = [*range(min_num, 2 ** bits)]
    i = 0
    while i < len(n_token_numbers):
        if count_tokens(n_token_numbers[i]) != rotation_tokens:
            n_token_numbers.pop(i)
        else:
            i += 1
    return n_token_numbers


def get_starter_line(bits) -> str:
    s = ""
    for i in range(get_max_dec_len(bits) - 2):
        s += " "
    s += "no;"
    for i in range(get_max_dec_len(bits) - 2):
        s += " "
    s += "dec;"
    for i in range(bits - 2):
        s += " "
    s += "bin;\n"
    return s


def format_code_line(num: int, bits, code_index) -> str:
    max_dec_len = get_max_dec_len(bits)

    padded_code_no = zero_pad_to_len(str(code_index), max_dec_len)
    padded_dec_num = zero_pad_to_len(str(num), max_dec_len)
    padded_bin_num = zero_pad_to_len(str(bin(num))[2:], bits)

    return padded_code_no + "; " + padded_dec_num + "; " + padded_bin_num + ";\n"
