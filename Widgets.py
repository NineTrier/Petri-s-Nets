import pygame as pg
import Pos
pg.font.init()


class Table:
    sc: pg.display # Дислпей пайгейма, на котором рисуем
    matr: list
    width: int
    height: int
    headers: list
    index: list
    item_w: int
    item_h: int

    def __init__(self, sc: pg.display, matr: list, headers: list, index: list):
        self.sc = sc
        self.headers = headers
        self.index = index
        self.matr = []
        self.item_w = 30
        self.item_h = 30
        self.width = (len(headers)+1) * self.item_w
        self.height = (len(index)+1) * self.item_h
        for i in range(len(matr)):
            row = []
            for j in range(len(matr[i])):
                row.append(matr[i][j])
            self.matr.append(row)

    def draw(self, pos: Pos):
        font = pg.font.Font("Roboto-regular.ttf", 14)
        y = pos.y
        x = pos.x
        for i in range(-1, len(self.index)):
            pg.draw.line(self.sc, (0, 0, 0), (x, y), (x + self.width, y))
            for j in range(-1, len(self.headers)):
                pg.draw.line(self.sc, (0, 0, 0), (x, y), (x, y + self.item_h))
                if i == -1 and j > -1:
                    text = font.render(str(self.headers[j]), True, (0, 0, 0))
                    self.sc.blit(text, (x + text.get_size()[0]/2, y))
                elif i > -1 and j == -1:
                    text = font.render(str(self.index[i]), True, (0, 0, 0))
                    self.sc.blit(text, (x + text.get_size()[0]/2, y))
                elif i > -1 and j > -1:
                    text = font.render(str(self.matr[i][j]), True, (0, 0, 0))
                    self.sc.blit(text, (x + text.get_size()[0]/2, y))
                x += self.item_w
            pg.draw.line(self.sc, (0, 0, 0), (x, y), (x, y + self.item_h))
            y += self.item_h
            x = pos.x
        pg.draw.line(self.sc, (0, 0, 0), (x, y), (x + self.width, y))



