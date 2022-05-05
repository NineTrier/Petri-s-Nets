import pygame.font
from pygame_widgets.button import Button
import pygame as pg
import Pos


# Класс Меню для приложения
class Menu:
    sc: pg.display # Дислпей пайгейма, на котором рисуем
    buttons: list # Список кнопок
    width: int # Ширина меню
    height: int # Высота меню
    pos: Pos # Позиция меню
    y_for_button: int # На каком y ставить кнопку
    x_for_button: int # На каком x ставить кнопку
    width_button: int # Ширина кнопки
    height_button: int # Высота кнопки

    # Конструктор
    def __init__(self, sc: pg.display, width: int, height: int, pos: Pos):
        self.sc = sc
        self.width = width
        self.height = height
        self.pos = pos
        self.buttons = []
        pg.draw.rect(self.sc, (200, 200, 200), (self.pos.x, self.pos.y, width, height))
        self.y_for_button = self.pos.y + 20
        self.x_for_button = int(self.pos.x + 0.1 * self.width)
        self.width_button = int(self.width - (0.1 * self.width)*2)
        self.height_button = 50

    def add_button(self, text, inactive_color, hover_color, pressed_color, on_click):
        """Функция добавляет кнопку в меню
        text - Текст внутри кнопки
        inactive-color - цвет кнопки, когда она неактивна
        hover_color - цвет кнопки, при наведении на неё мыши
        pressed-color - цвет кнопки, при нажатии на неё
        on-click - функция, которую будет выполнять кнопка"""
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
            textColour=(255, 255, 255),
            font=pygame.font.Font("Roboto-regular.ttf", 14)
        )
        self.buttons.append(button)
        self.y_for_button += self.height_button + 10
