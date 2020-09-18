'''
Given an unsorted list of integers, find a pair which add up to a given value.
Identify the indices of the values which sum to the target.
These indices must be distinct (i.e. you can't use a value in the same position twice).
'''
from typing import Optional, Tuple


def two_sum_naive_approach(x: list, value: int)->Optional[Tuple]:
    x.sort()

    # index iter approach
    # for index_1 in range(len(x)-1):  # no sense to run last loop because there's no value_2 to compare it to
    #     for index_2 in range(index_1+1, len(x)):
    #         sum = x[index_1] + x[index_2]
    #         if sum == value:
    #             return index_1, index_2

    # value iter approach
    for index, value_1 in enumerate(x[:-1]):  # no sense to run last loop because there's no value_2 to compare it to
        for value_2 in x[index+1:]:
            if value_1 + value_2 == value:
                return x.index(value_1), x.index(value_2)


def two_sum_binary_search(x: list, value: int) -> Optional[Tuple]:
    l = sorted(x)

    for ind, value_1 in enumerate(l[:-1]):
        value_2 = value - value_1
        low = 0
        high = len(l)-1

        while low <= high:
            mid = (low + high) // 2
            if value_2 == l[mid]:
                return ind, mid
            elif value_2 > l[mid]:
                low = mid + 1
            else:
                high = mid - 1


def two_sum_dict(x: list, value: int) -> Optional[Tuple]:
    x.sort()
    hash = {item: x.index(item) for item in x}

    for index_1, value_1 in enumerate(x):
        value_2 = value - value_1
        if index_2:= hash.get(value_2):
            return index_1, index_2


# two_sum = two_sum_naive_approach
# two_sum = two_sum_binary_search
two_sum = two_sum_dict

# TESTS
x = [1, 5, 2, 3, 6]  # [1,2,3,5,6]
assert two_sum(x, 7) == (0,4)
assert two_sum(x, 3) == (0,1)
assert two_sum(x, 11) == (3,4)
assert two_sum(x, 20) == None   # negative case
