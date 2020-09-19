# Related read
# https://realpython.com/python-coding-interview-tips/#select-the-right-built-in-function-for-the-job
# https://docs.python.org/3/library/functions.html#built-in-functions

section_sep = ''

# EVEN numbers
x = [11,1,3,4,5,6,8,9,10,1,3]
even_only = [i for i in x if i %2==0]
print(even_only)

print(section_sep)
##################################

# get COUNT of particular element in list
one_cnt = x.count(1)
print(one_cnt)

# get COUNT of ALL elements in a list
list_elem_cnt = {i: x.count(i) for i in x}
print(list_elem_cnt, type(list_elem_cnt))

# COUNT number of each letter in a word
from collections import Counter
word = "tomatoes, potatoes, brokkoli"
print({i: word.count(i) for i in word})
print(Counter(word))

# COUNT words in sentence
sentence = "It was a really great trip"
print(len(sentence.split()))

print(section_sep)
###################################

# FIND DUPES in array
from collections import Counter
dupes = [k for k, v in Counter(x).items() if v > 1]
print(dupes)

dupes = [k for k, v in list_elem_cnt.items() if v > 1]
print(dupes)

# REMOVE DUPES
deduped = list(set(x))
print(deduped)

# REMOVE DUPES option for ordered list
print(list(dict.fromkeys(x)))

print(section_sep)
#####################################

# SORT list
char = ['d', 'K', 'd', 'c', 'a']
char.sort(key=str.lower)  # in-place
print(char)
print(sorted(char, key=str.lower))  # copy and sort

print(section_sep)
#####################################

# REVERSE list order with slicing
l = [1,2,3,4,5,6,7]
print(l[::-1])

# REVERSE list order with reverse iter
print(list(reversed(l)))

# REVERSE list order with reverse method
l.reverse()
print(l, )

print(section_sep)
######################################

# get LENGTH for each element in a list
words = ['asd', 'zxcvb', 'a', 'qwerty']
print(list(map(len, words)))

print(section_sep)
#######################################

# UPDATE each element of a list to upper
print(list(map(lambda x: x.upper(), words)))

# ADD 2 lists
x1 = [1,2,3,4,5]
x2 = [6,7,8,9,10]
print(list(map(lambda x,y: x+y, x1, x2)))

print(section_sep)
#######################################

# get EVERY 2nd element in a list
x = [1,2,3,4,5,6]
print(x[::2])
print(section_sep)

print(section_sep)
####################################

# Generate every possible COMBINATION between elements of a list (order doesn't matter)
import itertools

people = ['Mary', 'Jake', 'Sandy', 'Becca', 'Robin']
print(list(itertools.combinations(people, r=4)))

print(section_sep)
##################################

# Generate every possible PERMUTATIONS between elements of a list (order does matter)
print(list(itertools.permutations(people, r=2)))

print(section_sep)
##################################
