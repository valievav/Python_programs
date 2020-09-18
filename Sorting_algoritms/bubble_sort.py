def bubble_sort_init_solution(test_list):
    while True:
        temp = None
        for n in range(len(test_list)-1):
            if test_list[n] > test_list[n+1]:
                temp = test_list[n + 1]
                test_list[n + 1] = test_list[n]
                test_list[n] = temp
            else:
                continue
        if not temp:
            break

    return test_list


def bubble_sort_after_solution_lookup(test_list):
    values_swapped = True
    while values_swapped:
        values_swapped = False
        for n in range(len(test_list)-1):
            if test_list[n] > test_list[n+1]:
                test_list[n], test_list[n + 1] = test_list[n + 1], test_list[n]
                values_swapped = True

    return test_list


test_list = [3,6,1,4,7,9,0,22,45,100,3, -1]

print(bubble_sort_init_solution(test_list))
print(bubble_sort_after_solution_lookup(test_list))

