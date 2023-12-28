from guizero import App, Text, PushButton, Box, Window
from gui.constants import *

class Tile:
    def __init__(self, tile: Box):
        self.tile = tile

        # state variables #
        self.properties = {
            'letter': None,
            'color': IDLE
        }

        self.top_padding = Box(tile, width=52, height=10, align="top")
        self.text = Text(tile, bg=IDLE, color=WHITE, size=24)
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

    def __set_custom_color(self, red: int, green: int, blue: int):
        desired_rgb = f"#{hex(red)[2:4]}{hex(green)[2:4]}{hex(blue)[2:4]}"
        self.tile.bg = desired_rgb
        self.properties['color'] = desired_rgb

    def fade(self, color: str):
        current_color = self.properties.get('color')
        desired_rgb = [self.__get_color_field(color, 'red'),
                       self.__get_color_field(color, 'green'),
                       self.__get_color_field(color, 'blue')]
        current_rgb = [self.__get_color_field(current_color, 'red'),
                       self.__get_color_field(current_color, 'green'),
                       self.__get_color_field(current_color, 'blue')]
        
        while((desired_rgb[0] != current_rgb[0]) or (desired_rgb[1] != current_rgb[1]) or (desired_rgb[2] != current_rgb[2])):
            # set red field #
            if current_rgb[0] < desired_rgb[0]:
                current_rgb[0] = current_rgb[0] + 1
            elif current_rgb[0] > desired_rgb[0]:
                current_rgb[0] = current_rgb[0] - 1
                
            # set green field #
            if current_rgb[1] < desired_rgb[1]:
                current_rgb[1] = current_rgb[1] + 1
            elif current_rgb[1] > desired_rgb[1]:
                current_rgb[1] = current_rgb[1] - 1

            # set blue field #
            if current_rgb[2] < desired_rgb[2]:
                current_rgb[2] = current_rgb[2] + 1
            elif current_rgb[2] > desired_rgb[2]:
                current_rgb[2] = current_rgb[2] - 1

            # set the tile color #
            self.__set_custom_color(current_rgb[0], current_rgb[1], current_rgb[2])