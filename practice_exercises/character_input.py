# https://www.practicepython.org/exercise/2014/01/29/01-character-input.html
# Create a program that asks the user to enter their name and their age.
# Print out a message addressed to them that tells them the year that they will turn 100 years old.

import datetime


def ask_age():
    current_year = datetime.datetime.now().year
    name = input('Please enter your name.\n')

    while True:
        try:
            age = int(input('Please enter your age.\n'))
        except ValueError:
            print('Age should be an integer.')
        else:
            if age <= 0:
                print('Age should be a positive integer > 0.')
            else:
                break

    if age > 100:
        print('You already older than 100 years. Congratulations! :)')
    elif age == 100:
        print('You already 100. Congratulations ! :)')
    else:
        result_year = current_year + (100 - age)

        print(f'Hi {name}. You are going to turn 100 in {result_year} years.')


if __name__ == "__main__":
    ask_age()
