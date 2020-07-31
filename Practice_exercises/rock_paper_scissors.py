# https://www.practicepython.org/exercise/2014/03/26/08-rock-paper-scissors.html
# Make a two-player Rock-Paper-Scissors game.
# (Hint: Ask for player plays (using input), compare them, print out a message of congratulations to the winner,
# and ask if the players want to start a new game)
#
# Remember the rules:
# Rock beats scissors
# Scissors beats paper
# Paper beats rock

from typing import Tuple


def rock_paper_scissors() -> None:

    def get_input(choice: tuple) -> Tuple[str, str]:
        user_name = input("Hi! Let's play rock-paper-scissors. What's you'r name?\n")

        while True:
            user_choice = input(f'Hi {user_name}. Please enter "rock", "paper" or "scissors".\n')
            if user_choice not in choice:
                print('This choice is not possible.')
                continue
            return user_name, user_choice

    def determine_winner(user1_name: str, user1_choice: str, user2_name: str, user2_choice: str) -> None:
        if user1_choice == beats[user2_choice]:
            print(f"Yey! {user1_name} has won - {user1_choice} beats {user2_choice}. Congrats!")
        elif user2_choice == beats[user1_choice]:
            print(f"Yey! {user2_name} has won - {user2_choice} beats {user1_choice}. Congrats!")
        else:
            print("It's a tie!")

    choice = ('rock', 'paper', 'scissors')
    beats = {'rock': 'scissors',
             'scissors': 'paper',
             'paper': 'rock'}

    user1_name, user1_choice = get_input(choice)
    user2_name, user2_choice = get_input(choice)
    determine_winner(user1_name, user1_choice, user2_name, user2_choice)


if __name__ == '__main__':
    rock_paper_scissors()

