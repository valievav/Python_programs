'''
Given an unsorted list of integers, find a pair which add up to a given value.
Identify the indices of the values which sum to the target.
These indices must be distinct (i.e. you can't use a value in the same position twice).
'''


# Big O (log n)
def two_sum(l: list, target: int)-> tuple:
    l.sort()

    for index1, value1 in enumerate(l):
        value2 = target - value1

        low = 0
        high = len(l)-1

        while low <= high:
            mid = (low+high) // 2   # splits each search volume on 2

            if value2 == l[mid]:
                return index1, mid
            if value2 > l[mid]:
                low = mid + 1
            if value2 < l[mid]:
                high = mid - 1


l = [6,7,8,1,2,3]  # [1,2,3,6,7,8]
target = 10
print(two_sum(l, target))


assert two_sum(l, 10) == (1,5)
assert two_sum(l, 7) == (0,3)
assert two_sum(l, 15) == (4,5)
assert two_sum(l, 3) == (0,1)
assert two_sum(l, 20) == None
