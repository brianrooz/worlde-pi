from guizero import App, Text, PushButton, Box, Window

tiles = []

class Tile:
    def __init__(self, tile: Box):
        self.tile = tile

        # constants #
        self.white = "#f8f8f8"
        self.green = "#538d4e"
        self.yellow = "#b59f3b"
        self.absent = "#3a3a3c"
        self.idle = "#121213"

        # state variables #
        self.properties = {
            'letter': None,
            'color': None
        }

        self.top_padding = Box(tile, width=52, height=10, align="top")
        self.text = Text(tile, bg=self.idle, color=self.white, size=24, text='B')
        self.tile.set_border(1.7, self.absent)

def create_board():
    rows = []
    app = App(title="Wordle", width=500, height=360, bg='#121213')
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

def main():
    app = create_board()
    app.display()

main()