import sys

from helpers import *

global BITS
global NUMBER_CONTAINERS
global CONTAINER_SIZE
global FILTER_SIZE
global THEORETICAL_LIMIT
global code_index


def get_inputs():
    global BITS
    global NUMBER_CONTAINERS
    global CONTAINER_SIZE
    global FILTER_SIZE
    global THEORETICAL_LIMIT

    # Get inputs
    BITS = int(input("Input the number of bits: "))
    NUMBER_CONTAINERS = int(input("Input the number of containers per \"filter\": "))
    CONTAINER_SIZE = int(input("Input the size of the container (5/9/27/54): "))
    FILTER_SIZE = NUMBER_CONTAINERS * CONTAINER_SIZE
    THEORETICAL_LIMIT = 2 ** BITS - 1
    print()


def maximum_all_perm_tokens() -> int:
    usable_codes = 0
    items_filter = 0
    tokens = 1

    while tokens <= BITS and items_filter + n_choose_k(BITS - 1, tokens - 1) <= FILTER_SIZE:
        usable_codes += n_choose_k(BITS, tokens)
        items_filter += n_choose_k(BITS - 1, tokens - 1)
        tokens += 1

    return tokens - 1


def find_rotations(tokens: int) -> int:
    rotations = 0
    items_filter = 0
    for i in range(1, tokens):
        items_filter += n_choose_k(BITS - 1, i - 1)

    while items_filter + tokens <= NUMBER_CONTAINERS * CONTAINER_SIZE:
        items_filter += tokens
        rotations += 1

    return rotations


def get_number_leftover_codes(leftover_space: int, rotation_tokens: int, usable_codes: int) -> int:
    individual_codes = 0
    if usable_codes < THEORETICAL_LIMIT:
        active_ratio = rotation_tokens / BITS
        individual_codes = int(leftover_space / active_ratio)

    return individual_codes


def print_stats(items_filter, usable_codes):
    ratio_percent = (usable_codes / THEORETICAL_LIMIT) * 100
    print("\n---RESULTS---")
    print("theoretical limit of codes: ", THEORETICAL_LIMIT)
    print("number of usable codes: ", usable_codes)
    print("ratio of usable / theoretical limit: ", '{:.2f}'.format(ratio_percent))
    print("min items / container: ", '{:.2f}'.format(items_filter / NUMBER_CONTAINERS), "of", CONTAINER_SIZE)


def find_usable_codes():
    get_inputs()

    usable_codes = 0
    items_filter = 0
    ###########################################################################################
    # Find max tokens where every permutation is a valid code
    max_tokens = maximum_all_perm_tokens()

    for i in range(1, max_tokens + 1):
        usable_codes += n_choose_k(BITS, i)
        items_filter += n_choose_k(BITS - 1, i - 1)

    print("---Token filling---")
    print("Max tokens where every perm is valid code:", max_tokens)
    print("Now at", usable_codes, "usable codes and", items_filter, "items / filter\n")
    ###########################################################################################
    # find rotations
    rotation_tokens = max_tokens + 1

    if max_tokens < BITS and items_filter + rotation_tokens <= FILTER_SIZE:
        rotations = find_rotations(rotation_tokens)

        usable_codes += rotations * BITS
        items_filter += rotations * rotation_tokens

        print("---Rotations---")
        print("There are ", rotations, "rotations with", rotation_tokens, "tokens that are usable")
        print("Now at", usable_codes, "usable codes and", items_filter, "items / filter\n")
    ###########################################################################################
    # find number of individual codes with leftover space
    leftover_space = FILTER_SIZE - items_filter
    leftover_codes = get_number_leftover_codes(leftover_space, rotation_tokens, usable_codes)
    usable_codes += leftover_codes

    if leftover_codes > 0:
        print("---Leftover space filling---")
        print("There are ", leftover_space, "spaces left in the chests to fill with individual codes\n"
                                            "that have", rotation_tokens, "tokens")
        print("There are", leftover_codes, "individual codes (I think)")
    ###########################################################################################
    # Results
    print_stats(items_filter, usable_codes)


def generate_permutations_list(max_tokens: int):
    numbers = [*range(1, 2 ** BITS)]

    i = 0
    while i < len(numbers):
        if count_tokens(numbers[i]) > max_tokens:
            numbers.pop(i)
        else:
            i += 1

    # BE or LE Sorting, comment out the following line if you want LE Ordering
    numbers.sort(key = None, reverse = True)
    ########################################
    numbers.sort(key = lambda x: count_tokens(x))
    return numbers


def format_code_line(num: int) -> str:
    max_dec_len = get_max_dec_len()
    padded_bin_num = zero_pad_to_len(str(bin(num))[2:], BITS)
    padded_dec_num = zero_pad_to_len(str(num), max_dec_len)
    global code_index
    padded_file_line = zero_pad_to_len(str(code_index), max_dec_len)
    return padded_file_line + "; " + padded_dec_num + "; " + padded_bin_num + ";\n"


def get_max_dec_len():
    return len(str(2 ** BITS))


def write_all_perm_codes() -> str:
    s = ""
    max_all_perm_tokens: int = maximum_all_perm_tokens()
    max_token_numbers = generate_permutations_list(max_all_perm_tokens)
    for num in max_token_numbers:
        s += format_code_line(num)
        global code_index
        code_index += 1
    return s


def write_all_rotation_codes() -> str:
    rotation_tokens = maximum_all_perm_tokens() + 1
    s = ""
    min_num = 2 ** rotation_tokens - 1
    number_of_rotations = find_rotations(rotation_tokens)
    for i in range(BITS):
        num = rotate_left(min_num, BITS, i)
        s += format_code_line(num)
        global code_index
        code_index += 1
    # TODO
    return s


def get_separator_line():
    length = get_max_dec_len() * 2 + BITS + 5
    s = ""
    for i in range(length):
        s += "-"
    return s + "\n"


def write_codes_to_file():
    file = open("usable_codes.csv", "w")
    global code_index
    code_index = 1
    content: str = ""
    ###########################################################################################

    content += write_all_perm_codes()
    content += get_separator_line()
    content += write_all_rotation_codes()
    # TODO

    ###########################################################################################
    file.write(content)
    file.close()


def do_math():
    while True:
        nums = input("Give n and k: ")
        nums_array = nums.split(" ")
        n = int(nums_array[0])
        k = int(nums_array[1])
        print(n, ";", k, ":", n_choose_k(n, k), ";", n_choose_k(n - 1, k - 1))


if __name__ == '__main__':
    args = sys.argv

    if len(args) < 2 or len(args) > 3:
        print("Incorrect number of arguments")
        exit(0)

    if args[1].startswith("-c"):
        find_usable_codes()
        if args[1].__contains__("w"):
            write_codes_to_file()
    elif args[1] == "-m":
        do_math()
    elif args[1] == "-i":
        pass
