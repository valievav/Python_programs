# EVEN numbers
x = [11,1,3,4,5,6,8,9,10,1,3]
even_only = [i for i in x if i %2==0]
print(even_only)

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

#####################################

# SORT list
char = ['d', 'K', 'd', 'c', 'a']
char.sort(key=str.lower)  # in-place
print(char)
print(sorted(char, key=str.lower))  # copy and sort

#####################################

# REVERSE list order with slicing
l = [1,2,3,4,5,6,7]
print(l[::-1])

# REVERSE list order with reverse iter
print(list(reversed(l)))
