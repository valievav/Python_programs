'''
Write a recursive function to count the number of items in a list.
'''


def count_recursion(l:list)-> int:
    def no_index_1():
        try:
            l[1]
        except IndexError:
            return True
        else:
            return False

    if not l:
        return 0

    if l[0] and no_index_1():  # base case - if only index 0 exists
        return 1

    return 1 + count_recursion(l[1:])


l = [1,1,5,8]
print(count_recursion(l))


assert count_recursion([1,1])  == 2
assert count_recursion([1,1,4,1,3,5]) == 6
assert count_recursion([]) == 0
assert count_recursion([5]) == 1
