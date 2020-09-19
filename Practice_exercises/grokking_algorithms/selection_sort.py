'''
Find smallest element in array.
'''


# Big O (n*2) very slow
def selection_sort(l:list)->list:
    new_l = []   # creates new data structure

    for k in range(len(l)):  # iter over each elem once
        smallest = l[0]
        smallest_i = 0

        for i in range(1, len(l)):  # and twice
            if l[i] < smallest:
                smallest = l[i]
                smallest_i = i
        new_l.append(l.pop(smallest_i))

    return new_l


l = [3,1,5,2]
print(selection_sort(l))

assert selection_sort([1,2,3,4,6,5]) == [1,2,3,4,5,6]
assert selection_sort([5,2,3,1]) == [1,2,3,5]
assert selection_sort([3,0,1,2]) == [0,1,2,3]
