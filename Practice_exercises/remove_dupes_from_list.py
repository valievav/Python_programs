# TASK 1 - https://leetcode.com/explore/interview/card/top-interview-questions-easy/92/array/727/
# Given a sorted array nums, remove the duplicates in-place such that each element appear only once
# and return the new length. Do not allocate extra space for another array, you must do this
# by modifying the input array in-place with O(1) extra memory.
# CLARIFICATION: you should PUSH elements to the end, not remove (Leetcode task desc is misleading to what they expect).
#
# Example 1:
# Given nums = [1,1,2],
# Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively.
# It doesn't matter what you leave beyond the returned length.
#
# TASK 2 - same task as above but need to remove elements.

from typing import List, Tuple


# TASK 1
def remove_duplicates_with_appending(nums: List[int]) -> Tuple[int, List[int]]:
    moved = 0
    for i in reversed(range(1, len(nums))):
        if nums[i] == nums[i-1]:
            nums.append(nums.pop(i-1))
            moved += 1
    return len(nums[:-moved]), nums[:-moved]


# TASK 2
def remove_duplicates_with_set(nums: List[int]) -> Tuple[int, List[int]]:
    deduped = list(set(nums))
    return len(deduped), deduped


# TASK 2
def remove_duplicates_with_reversed(nums: List[int]) -> Tuple[int, List[int]]:
    # can be optimized to exclude 0 element - reversed(range(1, len(nums))) or range(len(nums)-1, 0, -1)
    for i in reversed(range(len(nums))):  # same as range(len(nums)-1, -1, -1)
        if nums[i] == nums[i-1]:
            del nums[i]
    return len(nums), nums


if __name__ == "__main__":
    l = [0,1,2,2,2]
    solutions = [
        remove_duplicates_with_set,
        remove_duplicates_with_reversed,
        remove_duplicates_with_appending,
    ]

    print(solutions[1](l))
