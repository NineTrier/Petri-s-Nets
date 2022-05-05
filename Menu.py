from pygame_widgets.button import Button
import pygame as pg
import Pos


class Menu:
    sc: pg.display
    buttons: list
    width: int
    height: int
    pos: Pos
    y_for_button: int
    x_for_button: int
    width_button: int
    height_button: int

    def __init__(self, sc: pg.display, width: int, height: int, pos: Pos):
        self.sc = sc
        self.width = width
        self.height = height
        self.pos = pos
        self.buttons = []
        pg.draw.rect(self.sc, (200, 200, 20), (self.pos.x, self.pos.y, width, height))
        self.y_for_button = self.pos.y + 20
        self.x_for_button = int(self.pos.x + 0.1 * self.width)
        self.width_button = int(self.width - (0.1 * self.width)*2)
        self.height_button = 50

    def add_button(self, text, inactive_color, hover_color, pressed_color, on_click):
        button = Button(
            self.sc,
            self.x_for_button,
            self.y_for_button,
            self.width_button,
            self.height_button,

            text=text,
            fontSize=20,
            margin=20,
            inactiveColour=inactive_color,
            hoverColour=hover_color,
            pressedColour=pressed_color,
            radius=5,
            onClick=on_click,
            shadowDistance=5,
            shadowColour=(180, 180, 180),
            textColour=(255, 255, 255)
        )
        self.buttons.append(button)
        self.y_for_button += self.height_button + 10
