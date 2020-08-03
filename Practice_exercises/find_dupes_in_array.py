# Task 1 -  find duplicates in an array of positive numbers
# Task 2 - https://leetcode.com/problems/find-all-duplicates-in-an-array/
# Given an array of integers, 1 ≤ a[i] ≤ n (n = size of array), some elements appear twice and others appear once.
# Find all the elements that appear twice in this array.
# Could you do it without extra space and in O(n) runtime?
#
# Example:
# Input:
# [4,3,2,7,8,2,3,1]
#
# Output:
# [2,3]

from collections import Counter
from time import perf_counter
from typing import List, Set


# TASK 1
def solution_for_loop_and_2_lists(values: list) -> List[list]:
    """
    Use for loop and 2 lists to store unique and dupe values.
    """
    unique = []  # creates extra space, so does not follow exercise condition
    dupes = set()

    for value in values:
        if value not in unique:
            unique.append(value)
        else:
            dupes.add(value)

    return list(dupes)


# TASK 1
def solution_sorting(values: list) -> Set[int]:
    # order list with bubble sort
    while True:
        values_swapped = False
        for i in range(len(values) - 1):
            if values[i] > values[i + 1]:
                values[i], values[i + 1] = values[i + 1], values[i]
                values_swapped = True
        if not values_swapped:
            break

    # find neighbour dupes
    dupes = set()
    for i in range(len(values) - 1):
        if values[i] == values[i + 1]:
            dupes.add(values[i])
    return dupes


# TASK 1
def solution_list_count(values: list) -> List[int]:
    """
    Use list comprehension with set to evaluate only unique elements and count() method of lists.
    """
    return [v for v in set(values) if values.count(v) > 1]


# TASK 2 - PASSES LEETCODE SPEED TEST (372 ms, faster than 91.01% of submissions)
def solution_counter(values: list) -> List[int]:
    """
    Use Counter form collections to get {value: count,..}.
    """
    return [item for item, count in Counter(values).items() if count > 1]


# TASK 2 - LEETCODE SOLUTION (400 ms, faster than 67.83% of submissions)
def solution_negative_value_using_index(values: list) -> List[int]:
    """
    Based on idea that if list has dupes then dupe elements will lead to the same index withing a list
    (e.g., 3 will lead to 3-1=2 no matter where in a list it is located).

    Take each element -> calc index from it (elem - 1) -> use it to find value in a list -> check if it's negative.
    IF positive -> make it negative (mark value that lead to it as seen),
    IF negative -> it means it already seen -> record value that leads to it as dupe.
    """
    dupes = []
    for v in values:
        if values[abs(v) - 1] < 0:  # -1 is required to reach first/last index for list 1 ≤ a[i] ≤ n
            dupes.append(abs(v))
        else:
            values[abs(v) - 1] *= -1
    return dupes


if __name__ == "__main__":
    solutions = [
        solution_for_loop_and_2_lists,
        solution_sorting,
        solution_list_count,
        solution_counter,
        solution_negative_value_using_index,
    ]
    values_list = [3, 3, 4, 4, 5, 1, 2, 9, 8]

    start = perf_counter()
    solution_used = solutions[4](values_list)
    print(f'Dupes are {solution_used}.')

    time_spent = perf_counter() - start
    print(f'Time spent {time_spent}')

