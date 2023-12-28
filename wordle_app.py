from guizero import App, Text, PushButton, Box, Window
from time import sleep
from gui.constants import *
from gui.objects import *

tiles = []
app = ""

def test2():
    print("clicked again!")
    app.when_clicked = test

def test():
    print("hello world!")
    app.when_clicked = test2

def create_board():
    global app

    rows = []
    app = App(title="Wordle", width=500, height=360, bg='#121213')
    app.when_clicked = test
    board = Box(app, width=300, height=360)
    top_padding = Box(board, width=300, height=10)

    for row in range(6):
        line = Box(board, width=280, height=52.5)
        row_padding = Box(board, width=300, height=5)
        rows.append(line)

    for row in rows:
        for box in range(5):
            tile = Box(row, width=52, height=52.5, align="left")
            tile_padding = Box(row, width=5, height=52.5, align="left")
            tiles.append(Tile(tile))

    return app


create_board()
app.display()
