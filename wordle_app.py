from guizero import App, Text, PushButton, Box, Window
from time import sleep
from gui.constants import *
from gui.objects import *

from find_wordle import find_wordle
from solver import solver
import sys

board = []

def test():
    print("starting fade...")
    board[0].fade()
    print("done!")

def create_board(results):
    global board

    app = App(title="Wordle", width=500, height=360, bg='#121213')
    app.when_clicked = test                       # create a callback function to reveal tiles/letter on click
    area = Box(app, width=300, height=360)
    top_padding = Box(area, width=300, height=10)

    rows = []
    for row in range(6):
        line = Box(area, width=280, height=52.5)
        row_padding = Box(area, width=300, height=5)
        rows.append(line)

    tiles = []
    for row in range(MAX_ROWS):
        for box in range(TILES_PER_ROW):
            tile = Box(rows[row], width=52, height=52.5, align="left")
            tile_padding = Box(rows[row], width=5, height=52.5, align="left")

            # parse the results #
            try:
                letter = results[row][0][box]
                color = results[row][1][box]
            except IndexError: 
                letter = None
                color = IDLE

            tiles.append(Tile(tile, color, letter))

        try:
            word = results[row][0]
        except IndexError:
            word = None
        board.append(Row(tiles, word))
        tiles = []

    return app

def main():
    month = None
    day = None
    year = None

    try:
        month = sys.argv[1]
        day = sys.argv[2]
        year = sys.argv[3]
        print(f'using wordle from: {month}-{day}-{year}')
    except:
        print(f"using wordle from today")

    word, difficulty = find_wordle(month, day, year)
    results = solver(word)
    app = create_board(results)
    app.display()

main()
