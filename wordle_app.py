from guizero import App, Text, PushButton, Box, Window
from time import sleep, time
from gui.constants import *
from gui.objects import *

from find_wordle import find_wordle
from solver import solver
import sys

board = []
timer = 0
state = CLEARED

def event():
    global state
    global timer

    if state == CLEARED:
        state = BEGIN_FADE
    elif state == FADED:
        timer = 0
        state = BEGIN_REVEAL
    elif state == REVEALED:
        state = BEGIN_FULL_CLEAR
    
def state_machine():
    global state
    global timer

    if state == BEGIN_FADE:
        if board[0].state != FADED:
            board[0].fade('on')
        elif board[1].state != FADED:
            board[1].fade('on')
        elif board[2].state != FADED:
            board[2].fade('on')
        elif board[3].state != FADED:
            board[3].fade('on')
        elif board[4].state != FADED:
            board[4].fade('on')
        elif board[5].state != FADED:
            board[5].fade('on')
        else:
            state = FADED
    elif state == FADED:
        timer += ONE_TICK
        if timer == 5 * ONE_SECOND:
            state = BEGIN_CLEAR
            timer = 0
    elif state == BEGIN_REVEAL:
        if board[0].state != REVEALED:
            board[0].reveal()
        elif board[1].state != REVEALED:
            board[1].reveal()
        elif board[2].state != REVEALED:
            board[2].reveal()
        elif board[3].state != REVEALED:
            board[3].reveal()
        elif board[4].state != REVEALED:
            board[4].reveal()
        elif board[5].state != REVEALED:
            board[5].reveal()
        else:
            state = REVEALED
    elif state == REVEALED:
        timer += ONE_TICK
        if timer == 10 * ONE_SECOND:
            state = BEGIN_FULL_CLEAR
            timer = 0
    elif state == BEGIN_CLEAR:
        if board[0].state != CLEARED:
            board[0].fade('off')
        elif board[1].state != CLEARED:
            board[1].fade('off')
        elif board[2].state != CLEARED:
            board[2].fade('off')
        elif board[3].state != CLEARED:
            board[3].fade('off')
        elif board[4].state != CLEARED:
            board[4].fade('off')
        elif board[5].state != CLEARED:
            board[5].fade('off')
        else:
            state = CLEARED
    elif state == BEGIN_FULL_CLEAR:
        if board[0].state != CLEARED:
            board[0].fade('all')
        elif board[1].state != CLEARED:
            board[1].fade('all')
        elif board[2].state != CLEARED:
            board[2].fade('all')
        elif board[3].state != CLEARED:
            board[3].fade('all')
        elif board[4].state != CLEARED:
            board[4].fade('all')
        elif board[5].state != CLEARED:
            board[5].fade('all')
        else:
            state = CLEARED

def create_board(results):
    global board

    app = App(title="Wordle", width=500, height=360, bg='#121213')
    app.when_clicked = event                       # create a callback function to reveal tiles/letter on click
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
    app.repeat(ONE_TICK, state_machine)
    app.display()

main()
