# Write a program that asks the user for a long string containing multiple words.
# Print back to the user the same string, except with the words in backwards order.
# For example 'My name is Michele' -> 'Michele is name My'


def reverse_with_reverse_method(sentence: str) -> str:
    words = sentence.split()
    words.reverse()
    return ' '.join(words)


def reverse_with_slicing(sentence: str) -> str:
    words = sentence.split()
    return ' '.join(words[::-1])  # [start: end: step]


def reverse_with_reversed_iterator(sentence: str) -> str:
    words = sentence.split()
    return ' '.join(list(reversed(words)))  # yields elements


user_input = input('Please enter a sentence.\n')
solutions = [
    reverse_with_reverse_method,
    reverse_with_slicing,
    reverse_with_reversed_iterator,
]
print(solutions[0](user_input))
