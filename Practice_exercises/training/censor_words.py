'''
Create a function that takes a string txt and censors any word from a given list lst.
The text removed must be replaced by the given character char.
'''


def censor_string(txt:str, lst:list)-> str:
    for word in lst:
        txt = txt.replace(word, '*'*len(word))
    return txt

txt = "Today is Wednesday! Hey all!"
lst = ["Today", 'all']

print(censor_string(txt, lst))


assert censor_string('All people run away', ['Cheer', 'all', 'run']) == "All people *** away"
assert censor_string('Cheer all and run!', ['Cheer', 'all', 'run']) == '***** *** and ***!'
assert censor_string('Nothing to replace at ALL', ['Cheer', 'all', 'run']) == 'Nothing to replace at ALL'
