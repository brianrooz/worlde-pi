from guizero import App, Text, PushButton, Box, Window
from gui.constants import *
from find_wordle import find_wordle
from solver import solver

class Board:
    def __init__(self, answer: str = 'hello'):
        self.timer = 0
        self.state = CLEARED
        self.app, self.rows = self.__create_board(solver(answer))
        self.app.display()

    def __event_handler(self):
        if self.state == CLEARED:
            self.state = BEGIN_FADE
        elif self.state == FADED:
            self.timer = 0
            self.state = BEGIN_REVEAL
        elif self.state == REVEALED:
            self.state = BEGIN_FULL_CLEAR

    def __state_machine(self):
        if self.state == BEGIN_FADE:
            if self.rows[0].state != FADED:
                self.rows[0].fade('on')
            elif self.rows[1].state != FADED:
                self.rows[1].fade('on')
            elif self.rows[2].state != FADED:
                self.rows[2].fade('on')
            elif self.rows[3].state != FADED:
                self.rows[3].fade('on')
            elif self.rows[4].state != FADED:
                self.rows[4].fade('on')
            elif self.rows[5].state != FADED:
                self.rows[5].fade('on')
            else:
                self.state = FADED
        elif self.state == FADED:
            self.timer += ONE_TICK
            if self.timer == 5 * ONE_SECOND:
                self.state = BEGIN_CLEAR
                self.timer = 0
        elif self.state == BEGIN_REVEAL:
            if self.rows[0].state != REVEALED:
                self.rows[0].reveal()
            elif self.rows[1].state != REVEALED:
                self.rows[1].reveal()
            elif self.rows[2].state != REVEALED:
                self.rows[2].reveal()
            elif self.rows[3].state != REVEALED:
                self.rows[3].reveal()
            elif self.rows[4].state != REVEALED:
                self.rows[4].reveal()
            elif self.rows[5].state != REVEALED:
                self.rows[5].reveal()
            else:
                self.state = REVEALED
        elif self.state == REVEALED:
            self.timer += ONE_TICK
            if self.timer == 10 * ONE_SECOND:
                self.state = BEGIN_FULL_CLEAR
                self.timer = 0
        elif self.state == BEGIN_CLEAR:
            if self.rows[0].state != CLEARED:
                self.rows[0].fade('off')
            elif self.rows[1].state != CLEARED:
                self.rows[1].fade('off')
            elif self.rows[2].state != CLEARED:
                self.rows[2].fade('off')
            elif self.rows[3].state != CLEARED:
                self.rows[3].fade('off')
            elif self.rows[4].state != CLEARED:
                self.rows[4].fade('off')
            elif self.rows[5].state != CLEARED:
                self.rows[5].fade('off')
            else:
                self.state = CLEARED
        elif self.state == BEGIN_FULL_CLEAR:
            if self.rows[0].state != CLEARED:
                self.rows[0].fade('all')
            elif self.rows[1].state != CLEARED:
                self.rows[1].fade('all')
            elif self.rows[2].state != CLEARED:
                self.rows[2].fade('all')
            elif self.rows[3].state != CLEARED:
                self.rows[3].fade('all')
            elif self.rows[4].state != CLEARED:
                self.rows[4].fade('all')
            elif self.rows[5].state != CLEARED:
                self.rows[5].fade('all')
            else:
                self.state = CLEARED

    def __create_board(self, results: list):
        board = []
        app = App(title="Wordle", width=500, height=360, bg=IDLE)
        app.when_clicked = self.__event_handler                       # create a callback function to reveal tiles/letter on click
        app.repeat(ONE_TICK, self.__state_machine)                    # create a callback that is called every 100 ms 
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

        return app, board


class Row:
    def __init__(self, tiles: list, word):
        self.tiles = tiles
        self.word = word
        self.state = CLEARED 

    def fade(self, mode: str):
        for tile in self.tiles:
            tile.fade(mode)
        
        if mode == 'on':
            if (self.tiles[0].state == self.tiles[1].state == self.tiles[2].state == self.tiles[3].state == self.tiles[4].state == FADED):
                self.state = FADED
        else:
            if (self.tiles[0].state == self.tiles[1].state == self.tiles[2].state == self.tiles[3].state == self.tiles[4].state == CLEARED):
                self.state = CLEARED

    def reveal(self):
        for tile in self.tiles:
            tile.reveal()

        if (self.tiles[0].state == self.tiles[1].state == self.tiles[2].state == self.tiles[3].state == self.tiles[4].state == REVEALED):
            self.state = REVEALED

    def get_word(self):
        return self.word
    
    def set_word(self, word: str):
        self.word = word
        for letter in range(5):
            self.tiles[letter].set_letter(word[letter])

        return self.word

class Tile:
    def __init__(self, tile: Box, color: str, letter: str):
        self.tile = tile

        # state variables #
        self.properties = {
            'letter': None,
            'letter_color': None,
            'color': IDLE
        }
        self.word_decode = {
            '0': ABSENT,
            '1': YELLOW,
            '2': GREEN
        }
        self.state = CLEARED
        self.letter_initialized = False
        self.fade_color = self.word_decode.get(color, IDLE)
        self.properties['letter_color'] = self.fade_color
        self.fade_letter = letter

        self.top_padding = Box(tile, width=52, height=10, align="top")
        self.text = Text(tile, bg=IDLE, color=self.fade_color, size=24)
        self.tile.set_border(THICKNESS, ABSENT)

    def __get_color_field(self, color: str, field: str):
        code = 0
        if field == 'red':
            code = int(color[1:3], 16)
        elif field == 'green':
            code = int(color[3:5], 16)
        else:
            code = int(color[5:7], 16)
        return code

    def __set_custom_color(self, target: str, red: int, green: int, blue: int):
        desired_rgb = f"#{hex(red)[2:4]}{hex(green)[2:4]}{hex(blue)[2:4]}"
        if target == 'tile': 
            self.tile.bg = desired_rgb
            self.properties['color'] = desired_rgb
        else:
            self.text.text_color = desired_rgb
            self.properties['letter_color'] = desired_rgb

    def __calculate_rgb(self, current, desired):
            # set red field #
            if current[0] < desired[0]:
                current[0] = current[0] + 1
            elif current[0] > desired[0]:
                current[0] = current[0] - 1
                
            # set green field #
            if current[1] < desired[1]:
                current[1] = current[1] + 1
            elif current[1] > desired[1]:
                current[1] = current[1] - 1

            # set blue field #
            if current[2] < desired[2]:
                current[2] = current[2] + 1
            elif current[2] > desired[2]:
                current[2] = current[2] - 1

            return (current[0], current[1], current[2])

    def __get_target_color(self, mode: str):
        if mode == 'on':
            desired_rgb = [self.__get_color_field(self.fade_color, 'red'),
                        self.__get_color_field(self.fade_color, 'green'),
                        self.__get_color_field(self.fade_color, 'blue')]
        elif (mode == 'off') or (mode == 'all'):
            desired_rgb = [self.__get_color_field(IDLE, 'red'),
                        self.__get_color_field(IDLE, 'green'),
                        self.__get_color_field(IDLE, 'blue')]
        else:
            desired_rgb = [self.__get_color_field(WHITE, 'red'),
                        self.__get_color_field(WHITE, 'green'),
                        self.__get_color_field(WHITE, 'blue')]
        return desired_rgb

    def __get_current_color(self, target):
        current_color = self.properties.get(target)
        current_rgb = [self.__get_color_field(current_color, 'red'),
                       self.__get_color_field(current_color, 'green'),
                       self.__get_color_field(current_color, 'blue')]
        return current_rgb

    def __fade(self, mode: str):
        current_rgb = self.__get_current_color('color')
        desired_rgb = self.__get_target_color(mode)

        if ((desired_rgb[0] != current_rgb[0]) or (desired_rgb[1] != current_rgb[1]) or (desired_rgb[2] != current_rgb[2])):
            r, g, b = self.__calculate_rgb(current_rgb, desired_rgb)

            # set the tile color #
            self.__set_custom_color('tile', r, g, b)
            if mode == 'all':
                self.__set_custom_color('letter', r, g, b)
        else:
            self.tile.cancel(self.__fade)
            if mode == 'on': 
                self.state = FADED
            else:
                self.text.clear()
                self.letter_initialized = False
                self.text.text_color = self.fade_color
                self.properties['letter_color'] = self.fade_color
                self.state = CLEARED

    def __reveal(self):
        current_rgb = self.__get_current_color('letter_color')
        desired_rgb = self.__get_target_color('reveal')
        
        if ((desired_rgb[0] != current_rgb[0]) or (desired_rgb[1] != current_rgb[1]) or (desired_rgb[2] != current_rgb[2])):
            r, g, b = self.__calculate_rgb(current_rgb, desired_rgb)

            # set the tile color #
            self.__set_custom_color('letter', r, g, b)
        else:
            self.tile.cancel(self.__reveal)
            self.state = REVEALED

    def fade(self, mode: str):
        self.tile.repeat(10, self.__fade, args=[mode])

    def reveal(self):
        if self.fade_letter:
            if not self.letter_initialized:
                self.text.append(self.fade_letter.upper())
                self.letter_initialized = True
            self.tile.repeat(10, self.__reveal)
        else:
            self.state = REVEALED

    def get_letter(self):
        return self.properties.get('letter', None)
    
    def set_letter(self, letter: str):
        self.properties['letter'] = letter
        return self.properties.get('letter')

