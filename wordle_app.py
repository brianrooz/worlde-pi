from guizero import App, Text, PushButton, Box, Window
from time import sleep, time
from gui.constants import *
from gui.objects import *
import sys

board = []
timer = 0
state = CLEARED

def main():
    # month = None
    # day = None
    # year = None

    # try:
    #     month = sys.argv[1]
    #     day = sys.argv[2]
    #     year = sys.argv[3]
    #     print(f'using wordle from: {month}-{day}-{year}')
    # except:
    #     print(f"using wordle from today")

    # word, difficulty = find_wordle(month, day, year)
    # results = solver(word)
    board = Board()

main()
