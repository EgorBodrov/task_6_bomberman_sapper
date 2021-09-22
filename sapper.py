"""
Script imitates pure console version of Sapper.
According to Wikipedia, you win only when all bombs are marked with a flag.

Copyright by Bodrov Egor, 20.09.2021.
"""

import os
import sys
import random
import datetime
import time

from sapper_input import game_input

# The signs, which are used in field presentation
flag_sign = '?'     # Marked cells
boomed_sign = '!'   # If you picked a bomb

class Sapper:
    """
    Class contains all initial data and provides game functions.
    
    Attributes:
        - rows (int): Number of rows in game field
        - columns (int): Number of columns in game field
        - bombs_number (int): Number of bombs number
        - field: 2D-list that is shown for user
        - bombs: 2D-list that contains bombs location and number of neighbors
        - start_time: starting timer
        - result_file: file with match data
        - original_stdout: save stdout to choose between console and file

    Methods:
        - generate_bombs(): 
            Randomly generate bombs on the field.
        - win_condition() -> bool:
            Check are all bombs were marked with a flag.
        - show():
            Print field as convinient table.
        - count_bombs():
            Count the number of neibors-bombs for each cell.
        - open(row, column):
            Open cell in specific row and column.
        - set_flag(row, column):
            Set flag in specific row and column.
        - save_step(text=None):
            Save text or field in file
        - play():
            Main method, calls other methods.
    """

    def __init__(self, rows, columns, bombs_number):
        self.rows = rows
        self.columns = columns
        self.bombs_number = bombs_number

        self.field = [['x'] * self.columns for x in range(self.rows)]
        self.bombs = [[0] * self.columns for x in range(self.rows)]

        self.start_time = time.time()
        self.result_file = open(
            f'{datetime.datetime.now().strftime(r"%d-%m-%y_%H-%M-%S_match.txt")}',
            mode='a+'
        )
        self.original_stdout = sys.stdout

    def generate_bombs(self) -> None:
        generated = 0
        while generated < self.bombs_number:
            row = random.randint(0, self.rows - 1)
            column = random.randint(0, self.columns - 1)
            if self.bombs[row][column] == 0:
                self.bombs[row][column] = -1
                generated += 1

    def win_condition(self) -> bool:
        pairs = list(zip(sum(self.field, []), sum(self.bombs, [])))
        if pairs.count((flag_sign, -1)) == self.bombs_number:
            return True
        return False

    def show(self):
        print('\n Y')
        for i in range(self.rows, 0, -1):
            print(f' {i} ', end=' ') if i < 10 else print(f'{i} ', end=' ')
            print(*self.field[self.rows - i], sep='  ')

        print('\n   ', end='')
        for i in range(1, self.columns + 1):
            print(f' {i}', end=' ') if i < 10 else print(f'{i}', end=' ') 
        print('X\n')

    def count_bombs(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.bombs[i][j] > -1:
                    if i > 0 and self.bombs[i - 1][j] == -1:
                        self.bombs[i][j] += 1
                    if i > 0 and j < self.columns - 1 and self.bombs[i - 1][j + 1] == -1:
                        self.bombs[i][j] += 1
                    if j < self.columns - 1 and self.bombs[i][j + 1] == -1:
                        self.bombs[i][j] += 1
                    if j < self.columns - 1 and i < self.rows - 1 and self.bombs[i + 1][j + 1] == -1:
                        self.bombs[i][j] += 1
                    if i < self.rows - 1 and self.bombs[i + 1][j] == -1:
                        self.bombs[i][j] += 1
                    if i < self.rows - 1 and j > 0 and self.bombs[i + 1][j - 1] == -1:
                        self.bombs[i][j] += 1
                    if j > 0 and self.bombs[i][j - 1] == -1:
                        self.bombs[i][j] += 1
                    if i > 0 and j > 0 and self.bombs[i - 1][j - 1] == -1:
                        self.bombs[i][j] += 1

    def open(self, row, column):
        if row >= self.rows or column >= self.columns or row < 0 or column < 0 or \
           self.field[row][column] != 'x':
            return
        
        if self.bombs[row][column] > 0:
            self.field[row][column] = str(self.bombs[row][column])
        elif self.bombs[row][column] == 0:
            self.field[row][column] = '0'

            self.open(row, column - 1)
            self.open(row + 1, column - 1)
            self.open(row + 1, column)
            self.open(row + 1, column + 1)
            self.open(row, column + 1)
            self.open(row - 1, column + 1)
            self.open(row - 1, column)
            self.open(row - 1, column - 1)

    def set_flag(self, row, column):
        if self.field[row][column] == 'x':
            self.field[row][column] = flag_sign
        elif self.field[row][column] == flag_sign:
            self.field[row][column] = 'x'

    def save_step(self, text=''):
        sys.stdout = self.result_file
        if text == '':
            self.show()
        else:
            self.result_file.write(text + '\n')

        sys.stdout = self.original_stdout

    def play(self) -> bool:
        os.system('cls')
        self.generate_bombs()
        self.count_bombs()

        while self.win_condition() is False:
            self.show()
            self.save_step()

            row, column, action = game_input(self.rows, self.columns)
            self.save_step(text=f'{column + 1} {self.rows - row} {action}\n')

            if action == 'Open':
                if self.bombs[row][column] == -1:
                    self.field[row][column] = boomed_sign
                    self.show()
                    print('YOU LOST!')
                    self.save_step(text='YOU LOST!\n')
                    break
                
                self.open(row, column)
            else:
                self.set_flag(row, column)     
        else:
            self.show()
            self.save_step()
            print('YOU WON!\n')
            self.save_step(text='YOU WON!\n')
        
        self.result_file.write(f'match duration: {time.time() - self.start_time}\n')
        self.result_file.close()
        print('\nWant to play one more time? (Y/n)')
        answer = input()
        if answer.lower() in ('y', 'yes', 'да'):
            return True
        else:
            return False
