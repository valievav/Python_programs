'''
Write sum function for list with recursion.
'''


from typing import Optional


def sum_recursion(l:list)->Optional[int]:
    if not l:
        return None

    if len(l) == 1:
        return l[0]

    return l[0] + sum_recursion(l[1:])


l = [2,5,7]
print(sum_recursion(l))


assert sum_recursion([1,2,3,4]) == 10
assert sum_recursion([]) == None
assert sum_recursion([0,0,0]) == 0
assert sum_recursion([10,100,0]) == 110
