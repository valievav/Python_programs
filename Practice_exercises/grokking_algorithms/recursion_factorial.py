# Factorial 1,   1,   2,   6,   24,  120,  720
#           0,   1,   2,   3,   4,   5,    6       i
#           0*1, 0*1, 1*2, 2*3, 6*4, 24*5, 120*6  (i * prev factorial)

# 6! => 720 (1 -> 1 -> 2 -> 6 -> 24 -> 120 -> 720)

def get_factorial_for_loop(n):
    f = 1
    for i in range(1, n+1):
        f = f*i
    return f


x = 6
print(get_factorial_for_loop(x))

assert get_factorial_for_loop(0) == 1
assert get_factorial_for_loop(1) == 1
assert get_factorial_for_loop(2) == 2
assert get_factorial_for_loop(3) == 6
assert get_factorial_for_loop(4) == 24
assert get_factorial_for_loop(5) == 120
assert get_factorial_for_loop(6) == 720


def get_factorial_recursion(n):
    if n == 1:
        return 1

    return n * get_factorial_recursion(n-1)


x = 3
print(get_factorial_recursion(x))

