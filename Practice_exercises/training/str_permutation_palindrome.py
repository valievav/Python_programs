'''
Given a string write a function to determine if it's a permutation or a palindrome permutation.
Permutation - arrangement of letters like pot->top.
Palindrome - work which is written the same forwards and backwards like madam, racecar.
'''


def is_palindrome(word):
    word = word.lower()
    word = word.replace(' ', '')

    word_reversed = ''.join(list(reversed(word)))
    print(word_reversed)
    return True if word == word_reversed else False


def is_palindrome_permutation(word):
    """
    Word either palindrome or palindrome permutation.
    Palindrome - has symmetrical letters + only 1 letter occurs at most once, all others occur even number of times (madam).
    Permutation of palindrome - asymmetrical + only 1 letter occurs at most once, all others even number of times (mmaad).
    """
    word = word.lower().replace(' ', '')
    char_set = {}

    for i in word:
        if i in char_set:
            char_set[i] += 1
        else:
            char_set[i] = 1

    odd_chars = 0
    for v in char_set.values():
        if v%2 != 0 and not odd_chars:
            odd_chars += 1
        elif v%2 != 0 and odd_chars:
            return False
        else:
            pass

    return True


text = 'kkaya'
print(is_palindrome(text))
print(is_palindrome_permutation(text))
