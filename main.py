from math_helper import *


def maximum_all_perm_tokens() -> int:
    usable_codes = 0
    items_filter = 0
    tokens = 1

    while tokens <= BITS and items_filter + n_choose_k(BITS - 1, tokens - 1) <= FILTER_SIZE:
        usable_codes += n_choose_k(BITS, tokens)
        items_filter += n_choose_k(BITS - 1, tokens - 1)
        # print("Every permutation of a code with ", tokens, " tokens is usable")
        tokens += 1

    return tokens - 1


def find_rotations(tokens: int, items_filter: int) -> int:
    rotations = 0

    while items_filter + tokens <= NUMBER_CONTAINERS * CONTAINER_SIZE:
        items_filter += tokens
        rotations += 1

    return rotations


def print_attr():
    global BITS
    global NUMBER_CONTAINERS
    global CONTAINER_SIZE
    global FILTER_SIZE

    # Get inputs
    BITS = int(input("Input the number of bits: "))
    NUMBER_CONTAINERS = int(input("Input the number of containers per \"filter\": "))
    CONTAINER_SIZE = int(input("Input the size of the container (5/9/27/54): "))
    FILTER_SIZE = NUMBER_CONTAINERS * CONTAINER_SIZE
    print("\n")

    usable_codes = 0
    items_filter = 0
    THEORETICAL_LIMIT = 2 ** BITS - 1

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
        rotations = find_rotations(rotation_tokens, items_filter)

        usable_codes += rotations * BITS
        items_filter += rotations * rotation_tokens

        print("---Rotations---")
        print("There are ", rotations, "rotations with", rotation_tokens, "tokens that are usable")
        print("Now at", usable_codes, "usable codes and", items_filter, "items / filter\n")

    ###########################################################################################
    # find number of individual codes with leftover space
    if usable_codes < THEORETICAL_LIMIT:
        leftover_space = FILTER_SIZE - items_filter

        print("---Leftover space filling---")
        print("There are ", leftover_space, "spaces left in the chests to fill with individual codes")
        active_ratio = rotation_tokens / BITS

        individual_codes = int(leftover_space / active_ratio)

        print("There are", individual_codes, "individual codes (I think)")

        usable_codes += individual_codes

    ###########################################################################################

    ratio_percent = (usable_codes / THEORETICAL_LIMIT) * 100

    print("\n---RESULTS---")
    print("theoretical limit of codes: ", THEORETICAL_LIMIT)
    print("number of usable codes: ", usable_codes)
    print("ratio of usable / theoretical limit: ", '{:.2f}'.format(ratio_percent))
    print("min items / container: ", '{:.2f}'.format(items_filter / NUMBER_CONTAINERS), "of", CONTAINER_SIZE)


def do_math():
    while True:
        nums = input("Give n and k: ")
        nums_array = nums.split(" ")
        n = int(nums_array[0])
        k = int(nums_array[1])
        print(n, ";", k, ":", n_choose_k(n, k), ";", n_choose_k(n - 1, k - 1))


if __name__ == '__main__':
    while True:
        opt = input("What to do? [c] for code_attr / [m] for math: ")
        if opt.lower()[0] == 'c':
            print_attr()
            break
        elif opt.lower()[0] == 'm':
            do_math()
            break
