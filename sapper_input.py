"""Functionality for user input data"""

import os

def initialize():
    """
    Set initial parameters for game.

    Takes number of rows, columns and bombs from user. Check 
    correctness of input data.
    
    Arguments: None
    Returns:
        - config: tuple of input values
    """

    while True:
        print('Enter number of rows, columns and bombs separated by space')
        try:
            config = tuple(map(int, input().split()))
            if 0 in config:
                os.system('cls')
                print('Each argument must be > 0. Try again!')
                continue

            if len(config) != 3:
                os.system('cls')
                print('Enter exactly 3 numbers. Try again!')
                continue

            if config[0] * config[1] < config[2]:
                os.system('cls')
                print('Too much bombs. Try again!')
                continue

        except ValueError as ve:
            os.system('cls')
            print('Enter only integers. Try again!')
            continue

        return config


def game_input(rows, columns):
    """
    Ask for coordinates and action, then check correctness of user input.

    Arguments:
        - rows: number of rows in game field
        - columns: number of columns in game field
    Returns:
        - row: chosen row
        - column: chosen column
        - action: chosen action
    """

    while True:
        print(f"Enter coordinates and action in next format: X Y Action\n"
              f"('Flag' to set a flag, 'Open' to open a cell)")

        try:
            column, row, action = input().split()
            column, row = int(column) - 1, rows - int(row)

            if column < 0 or column > columns \
                or row < 0 or row > rows:
                print('Your coordinates is out of limits. Try again!')
                continue
            
            if action not in ('Open', 'Flag'):
                print('Enter only valid Action. Try again!')
                continue

        except ValueError as ve:
            print('Enter only valid values. Try again!')
            continue

        return row, column, action

    