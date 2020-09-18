'''
Implement an algorithm to determine whether a string has all unique characters.
What if you cannot use additional data structures?
'''


def is_unique_chars_set(l: str)-> bool:
    l = l.lower().replace(' ', '')
    return False if len(set(l)) != len(l) else True


def is_unique_chars_compar(l: str)-> bool:
    l = l.lower().replace(' ', '')

    for i, char in enumerate(l):
        if char in l[i+1:]:
            return False

    return True


text = "Some rando"

print(is_unique_chars_set(text))
print(is_unique_chars_compar(text))

