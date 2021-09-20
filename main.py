"""Example of set up and usage"""

import os

from sapper_input import initialize
from sapper import Sapper

def main():
    """Creates object Sapper, receive initial parameters and starts the game."""

    replay = True
    while replay:
        os.system('cls')
        print('WELCOME TO SAPPER!\nVersion: 1.0.0\nMade by: Bodrov Egor\n')
        game = Sapper(*initialize())
        replay = game.play()

    print('Thanks for playing!')

if __name__ == '__main__':
    main()
