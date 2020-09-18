'''
Write three functions:

boolean_and
boolean_or
boolean_xor
These functions should evaluate a list of True and False values, starting from the leftmost element and evaluating pairwise.
'''


def boolean_and(l: list)-> bool:
    if not l:
        return False

    result=l[0]
    for item in l[1:]:
        result = result and item

    return result


def boolean_or(l: list)-> bool:
    if not l:
        return False

    result=l[0]
    for item in l[1:]:
        result = result or item

    return result


def boolean_xor(l: list)-> bool:
    """
    Like OR but excludes [True, True] => False
    """
    if not l:
        return False

    result=l[0]
    for item in l[1:]:
        result = (result or item) and not (result and item)

    return result


l = []
print(boolean_and(l))

# TESTS
assert boolean_and([False, False]) == False
assert boolean_and([False, True]) == False
assert boolean_and([True, False]) == False
assert boolean_and([True, True]) == True
assert boolean_and([True, True, True, True]) == True
assert boolean_and([True, True, True, False]) == False

assert boolean_or([False, False]) == False
assert boolean_or([False, True]) == True
assert boolean_or([True, False]) == True
assert boolean_or([True, True]) == True
assert boolean_or([False, False, False, True]) == True
assert boolean_or([False, False, False, False]) == False

assert boolean_xor([False, False]) == False
assert boolean_xor([False, True]) == True
assert boolean_xor([True, False]) == True
assert boolean_xor([True, True]) == False

# SOLUTION with short circuit evaluation


def boolean_and(l: list) -> bool:
    if not l:
        return False

    # short circuit evaluation
    return not(False in l)


def boolean_or(l: list)-> bool:
    if not l:
        return False

    # short circuit evaluation
    return True in l


def boolean_xor(l: list)-> bool:
    if not l:
        return False

    return True in l and not all(l)

# TESTS
assert boolean_and([False, False]) == False
assert boolean_and([False, True]) == False
assert boolean_and([True, False]) == False
assert boolean_and([True, True]) == True
assert boolean_and([True, True, True, True]) == True
assert boolean_and([True, True, True, False]) == False

assert boolean_or([False, False]) == False
assert boolean_or([False, True]) == True
assert boolean_or([True, False]) == True
assert boolean_or([True, True]) == True
assert boolean_or([False, False, False, True]) == True
assert boolean_or([False, False, False, False]) == False

assert boolean_xor([False, False]) == False
assert boolean_xor([False, True]) == True
assert boolean_xor([True, False]) == True
assert boolean_xor([True, True]) == False
