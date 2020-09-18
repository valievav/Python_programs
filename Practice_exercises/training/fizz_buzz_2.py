'''
Write a Python program which iterates the integers from 1 to 50.
For multiples of three print "Fizz" instead of the number and for the multiples of five print "Buzz".
For numbers which are multiples of both three and five print "FizzBuzz".
'''


def solution_loop():
    for i in range(1, 51):
        if i%3 == 0 and i%5 ==0:
            print('Fizzbuzz')
        elif i%3 == 0:
            print('Fizz')
        elif i%5 == 0:
            print('Buzz')
        else:
            print(i)


def solution_str_concat():
    for i in range(1, 51):
        fizzbuzz = "Fizz" if i%3==0 else ''
        fizzbuzz += "Buzz" if i%5==0 else ''

        print(fizzbuzz or i)


def solution_bool_eval_concat():
    # print('zzz' * True + 'ddd' * False + 'ccc' * True)
    for i in range(1, 51):
        print('Fizz' * (i%3==0) + 'Buzz' * (i%5==0) or i)
