# Convert a number, represented as a sequence of digits in one base, to any other base.
# from decimal to binary

# 7 => 0111 => 8421

import timeit


def decimal_to_binary_list_fip(dec):
    binary = ""

    while dec:
        binary += str(dec%2)
        dec = dec//2

    return binary[::-1]


def decimal_to_binary_reverse(dec):
    binary = ""

    while dec:
        binary += str(dec%2)
        dec = dec//2

    return ''.join(list(reversed(binary)))


def decimal_to_binary_wo_reverse(dec):
    binary = ""

    while dec:
        binary = str(dec%2) + binary
        dec = dec//2

    return binary

dec = 14

print(decimal_to_binary_list_fip(dec))
print(timeit.timeit(decimal_to_binary_reverse(dec), number=100000))

print(decimal_to_binary_reverse(dec))
print(timeit.timeit(decimal_to_binary_reverse(dec), number=100000))

print(decimal_to_binary_wo_reverse(dec))
print(timeit.timeit(decimal_to_binary_wo_reverse(dec), number=100000))
