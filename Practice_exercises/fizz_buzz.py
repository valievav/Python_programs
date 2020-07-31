# Write a program that prints the numbers from 1 to 100.
# But for multiples of three print “Fizz” instead of the number and for the multiples of five print “Buzz”.
# For numbers which are multiples of both three and five print “FizzBuzz”


def fizz_buzz_if_else(max_num: int) -> None:
    for num in range(1, max_num+1):
        if (num % 3 == 0) and (num % 5 == 0):
            print('FizzBuzz')
        elif num % 3 == 0:
            print('Fizz')
        elif num % 5 == 0:
            print("Buzz")
        else:
            print(num)


def fizz_buzz_ternary(max_num: int) -> None:
    for num in range(1, max_num+1):
        result = 'Fizz' if num % 3 == 0 else ''
        result += 'Buzz' if num % 5 == 0 else ''

        print(result or num)


def fizz_buzz_ternary_one_liner(max_num: int) -> None:
    for num in range(1, max_num+1):
        print('Fizz' * (num % 3 == 0) + 'Buzz' * (num % 5 == 0) or num)  # Fizz * False => Fizz*0 => empty str ''


if __name__ == "__main__":
    max_num = 100
    # fizz_buzz_if_else(max_num)
    # fizz_buzz_ternary(max_num)
    fizz_buzz_ternary_one_liner(max_num)
