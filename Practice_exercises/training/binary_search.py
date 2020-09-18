'''
Find certain value in unordered list. Return index of such value.
'''


def binary_search(list, value):
    list.sort()

    start = 0
    end = len(list)-1  # last index

    while start <= end:
        mid = (start + end) // 2
        if list[mid] == value:
            return mid
        elif list[mid] > value:
            end = mid - 1
        else:
            start = mid + 1


list = [2,4,5,6,1]  # [1,2,4,5,6]
value = 5  # index 3
print(binary_search(list, value))

assert binary_search([3,4,5,6,1], 6) == 4
assert binary_search([2,4,1,2,3], 10) == None
assert binary_search([1,2,3,4,5], 1) == 0
