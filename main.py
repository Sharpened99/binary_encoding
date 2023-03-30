import sys

from helpers import *

global BITS
global NUMBER_CONTAINERS
global CONTAINER_SIZE
global FILTER_SIZE
global THEORETICAL_LIMIT
global code_index


def get_inputs():
    global BITS, NUMBER_CONTAINERS, CONTAINER_SIZE

    # Get inputs
    BITS = int(input("Input the number of bits: "))
    NUMBER_CONTAINERS = int(input("Input the number of containers per \"filter\": "))
    CONTAINER_SIZE = int(input("Input the size of the container (5/9/27/54): "))
    print()


def generate_constants():
    global FILTER_SIZE, THEORETICAL_LIMIT
    FILTER_SIZE = NUMBER_CONTAINERS * CONTAINER_SIZE
    THEORETICAL_LIMIT = 2 ** BITS - 1


def maximum_all_perm_tokens() -> tuple[int, int]:
    usable_codes = 0
    items_filter = 0
    tokens = 1

    while tokens <= BITS and items_filter + n_choose_k(BITS - 1, tokens - 1) <= FILTER_SIZE:
        usable_codes += n_choose_k(BITS, tokens)
        items_filter += n_choose_k(BITS - 1, tokens - 1)
        tokens += 1

    return tokens - 1, items_filter


def get_number_rotations(tokens: int) -> tuple[int, int]:
    rotations = 0
    items_filter = maximum_all_perm_tokens()[1]

    while items_filter + tokens <= NUMBER_CONTAINERS * CONTAINER_SIZE:
        items_filter += tokens
        rotations += 1

    return rotations, items_filter


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
    if len(args) == 5:
        global BITS, NUMBER_CONTAINERS, CONTAINER_SIZE
        BITS = int(args[2])
        NUMBER_CONTAINERS = int(args[3])
        CONTAINER_SIZE = int(args[4])
    else:
        BITS = 0
        get_inputs()

    generate_constants()

    usable_codes = 0
    ###########################################################################################
    # Find max tokens where every permutation is a valid code
    max_tokens, items_filter = maximum_all_perm_tokens()
    for i in range(1, max_tokens + 1):
        usable_codes += n_choose_k(BITS, i)

    print("---Token filling---")
    print("Max tokens where every perm is valid code:", max_tokens)
    print("Now at", usable_codes, "usable codes and", items_filter, "items / filter\n")
    ###########################################################################################
    # find rotations
    rotation_tokens = max_tokens + 1

    if max_tokens < BITS and items_filter + rotation_tokens <= FILTER_SIZE:
        rotations, items_filter = get_number_rotations(rotation_tokens)

        usable_codes += rotations * BITS

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
        print("There are ", leftover_space, "spaces left in the chests to fill with individual codes"
                                            " that have", rotation_tokens, "tokens")
        print("There are", leftover_codes, "individual codes (I think)")
    ###########################################################################################
    # Results
    print_stats(items_filter, usable_codes)

    return usable_codes


def generate_permutations_list(max_tokens: int):
    numbers = [*range(1, 2 ** BITS)]

    i = 2 ** max_tokens - 1
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


def write_all_perm_codes() -> str:
    s = ""
    max_all_perm_tokens: int = maximum_all_perm_tokens()[0]
    max_token_numbers = generate_permutations_list(max_all_perm_tokens)
    for i in range(len(max_token_numbers)):
        num = max_token_numbers[i]
        if i > 0 and count_tokens(num) > count_tokens(max_token_numbers[i - 1]):
            s += get_separator_line()
        global code_index
        s += format_code_line(num, BITS, code_index)
        code_index += 1
    return s


def write_all_rotation_codes() -> tuple[str, list[int]]:
    rotation_tokens = maximum_all_perm_tokens()[0] + 1
    s = ""
    number_of_rotations = get_number_rotations(rotation_tokens)[0]

    n_token_numbers = get_n_token_numbers(rotation_tokens, BITS)

    # BE or LE sorting, comment out the following line if you want LE sorting
    n_token_numbers.sort(reverse = True)

    no_rotational_dup = remove_rot_dup(n_token_numbers)

    ########################################
    used_codes = []

    for i in range(number_of_rotations):
        val = no_rotational_dup[i]
        for rot in range(BITS):
            rotated = rotate_right(val, BITS, rot)
            global code_index
            s += format_code_line(rotated, BITS, code_index)
            code_index += 1
        if i < number_of_rotations - 1:
            s += get_separator_line()
        used_codes.append(val)

    return s, used_codes


def remove_rot_dup(n_token_numbers):
    no_rotational_dup = []
    for new_val in n_token_numbers:
        counter = 0
        for rot in range(BITS):
            rotated = rotate_right(new_val, BITS, rot)
            if no_rotational_dup.__contains__(rotated):
                counter += 1
        if counter == 0:
            no_rotational_dup.append(new_val)
    return no_rotational_dup


def sort_to_overlap(to_sort):
    new_list = []
    new_list.insert(0, to_sort.pop(0))

    while len(to_sort) > 0:
        collective_overlap = []
        for i in range(len(to_sort)):
            collective_overlap.insert(i, 0)
            for to_compare in new_list:
                collective_overlap[i] += get_overlap(to_sort[i], to_compare)

        lowest_overlap_index = 0
        for i in range(len(collective_overlap)):
            if collective_overlap[i] < collective_overlap[lowest_overlap_index]:
                lowest_overlap_index = i

        new_list.append(to_sort.pop(lowest_overlap_index))

    return new_list


def write_individual_codes(used_codes) -> str:
    max_all_perm_tokens = maximum_all_perm_tokens()[0]
    rotation_tokens = max_all_perm_tokens + 1
    number_of_rotations, items_filter = get_number_rotations(rotation_tokens)
    leftover_space = FILTER_SIZE - items_filter

    usable_codes = 0
    for i in range(1, max_all_perm_tokens):
        usable_codes += n_choose_k(BITS, i)
    usable_codes += number_of_rotations * BITS

    leftover_codes = get_number_leftover_codes(leftover_space, rotation_tokens, usable_codes)
    s = ""

    n_token_numbers_wo_rot = get_n_token_numbers(rotation_tokens, BITS)
    for n in used_codes:
        n_token_numbers_wo_rot.remove(n)

    free_codes = remove_rot_dup(n_token_numbers_wo_rot)

    # BE or LE sorting: Comment out the following line if you want LE sorting
    free_codes.sort(reverse = True)
    ###########################################
    free_codes = sort_to_overlap(free_codes)

    bin_nums = []
    for n in free_codes:
        bin_nums.append(bin(n))

    print(bin_nums)

    individual_codes = free_codes[0: leftover_codes]
    for num in individual_codes:
        global code_index
        s += format_code_line(num, BITS, code_index)
        code_index += 1

    return s


def get_separator_line() -> str:
    length = get_max_dec_len(BITS) * 2 + BITS + 5
    s = ""
    for i in range(length):
        s += "-"
    return s + "\n"


def write_codes_to_file(number_usable_codes):
    file = open("usable_codes.csv", "w")
    global code_index
    code_index = 1
    content: str = get_starter_line(BITS)
    ###########################################################################################
    codes = []

    content += write_all_perm_codes()
    if code_index < number_usable_codes:
        content += get_separator_line()
        rots, codes = write_all_rotation_codes()
        content += rots
    if code_index < number_usable_codes:
        content += get_separator_line()
        content += write_individual_codes(codes)

    ###########################################################################################
    file.write(content)
    file.close()


if __name__ == '__main__':
    args = sys.argv
    print(args)

    if len(args) < 2 or len(args) > 5:
        print("Incorrect number of arguments")
        exit(0)

    if args[1].startswith("-c"):
        usable = find_usable_codes()
        if args[1].__contains__("w"):
            write_codes_to_file(usable)
    elif args[1] == "-i":
        pass
