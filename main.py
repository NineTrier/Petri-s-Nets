import pygame_widgets
from Petri import *
import sys
from Menu import Menu
from FunctionsForButton import Spawner
from Widgets import *


# Создаём экран
sc = pg.display.set_mode((1500, 750))
# Рабочая область, где будут двигаться элементы
rect = (10, 10, sc.get_size()[0] - 200-20, sc.get_size()[1]-20)
# ПОдготовка окна
sc.fill((220, 220, 220))
pg.draw.rect(sc, (255, 255, 255), rect)
# Создаём переменные необходимых классов
petr = Petri(sc, 20, 60, 10) # Класс сетей Петри, весь бэкенд в этом классе
sp = Spawner() # Класс, который нужен, чтобы создать кнопки
# Цвета для кнопок
button_color = (119, 136, 153)
button_color_hover = (105, 105, 105)
button_color_pressed = (192, 192, 192)
# Создаём меню
menu = Menu(sc, 200, sc.get_size()[1], Pos.Pos(sc.get_size()[0] - 200, 0))
menu.add_button("Переместить", button_color, button_color_hover, button_color_pressed, sp.func_change_pos)
menu.add_button("Добавить Point", button_color, button_color_hover, button_color_pressed, sp.func_add_point)
menu.add_button("Добавить Transition", button_color, button_color_hover, button_color_pressed, sp.func_add_trans)
menu.add_button("Добавить Link", button_color, button_color_hover, button_color_pressed, sp.func_add_link)
menu.add_button("Добавить Marker", button_color, button_color_hover, button_color_pressed, sp.func_add_mark)
menu.add_button("Матрица инцидентности", button_color, button_color_hover, button_color_pressed, lambda: petr.matr_incident(Pos.Pos(500, 100)))
# Обновляем окно
pg.display.update()
# Вспомогательные инструменты
active_elem = None # Активный элемент, сюда будут заносится активные элементы в формате (id, "Type")
link = [] # Массив, нужный для создания соединений между элементами
leftmouseclick = False # Для отслеживания одинарного левого клика мыши
while True:
    events = pg.event.get()
    for i in events:
        if i.type == pg.QUIT:
            sys.exit()
        # Если была нажата мышь
        elif i.type == pg.MOUSEBUTTONDOWN:
            # Левая кнопка мыши
            if i.button == 1:
                # Флаг делаем True
                leftmouseclick = True
        # Здесь горячие клавиши(Пока только удаление)
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_DELETE:
                # Удаляем выделенный элемент
                if active_elem[1] == "Transition":
                    petr.delete_transition(active_elem[0])
                elif active_elem[1] == "Point":
                    petr.delete_point(active_elem[0])
                elif active_elem[1] == "Link":
                    petr.delete_link(active_elem[0])
                # Очищаем рабочую область
                pg.draw.rect(sc, (255, 255, 255), rect)
                # Отрисовываем элементы обратно
                for j in petr.transitions:
                    petr.inactivate_tr(j.id, j.pos)
                for j in petr.points:
                    petr.inactivate_pt(j.id, j.pos)
                petr.redraw_links()
                # Обновляем рабочую область
                pg.display.update(rect)
                # Активный элемент обнуляем
                active_elem = None
    # Получаем позицию мыши в пространстве
    mouse_pos = pg.mouse.get_pos()
    # Ограничиваем окно, в котором можем работать
    if 10 + petr.ptRadius < mouse_pos[0] < sc.get_size()[0] - 235 and petr.trLength < mouse_pos[1] < sc.get_size()[1] - petr.trLength:
        # Если было нажатие на левую кнопку мыши
        if leftmouseclick:
            # Переводим mouse_pos в свой собственный класс Pos
            pos = Pos.Pos(mouse_pos[0], mouse_pos[1])
            # Флаг, который обозначает, что элемент был активирован, а не добавлен
            activate = False
            # Пройдём по всем поинтам
            for i in petr.points:
                # Если мы кликнули на какой-то из них
                if i.pos.x - petr.ptRadius < pos.x < i.pos.x + petr.ptRadius and i.pos.y - petr.ptRadius < pos.y < i.pos.y + petr.ptRadius:
                    # Проверяем есть ли уже активный элемент
                    if type(active_elem) == tuple:
                        # Если есть, то смотрим что это за элемент
                        if active_elem[1] == "Point":
                            # И дезактивируем его
                            petr.inactivate_pt(active_elem[0], petr.points[active_elem[0]].pos)
                        elif active_elem[1] == "Transition":
                            petr.inactivate_tr(active_elem[0], petr.transitions[active_elem[0]].pos)
                        elif active_elem[1] == "Link":
                            petr.inactivate_ln(active_elem[0])
                    # Флаг ставим в True
                    activate = True
                    # Заполняем переменную активный элемент
                    active_elem = (i.id, 'Point')
                    # Активируем поинт
                    petr.activate_pt(active_elem[0], i.pos)
                    pg.display.update(rect)
            # То же самое, что в верхнем, только объект другой и функции соответственно для этого объекта
            for i in petr.transitions:
                if i.pos.x - petr.trWidth/2 < pos.x < i.pos.x + petr.trWidth/2 and i.pos.y - petr.trLength/2 < pos.y < i.pos.y + petr.trLength/2:
                    if type(active_elem) == tuple:
                        if active_elem[1] == "Point":
                            petr.inactivate_pt(active_elem[0], petr.points[active_elem[0]].pos)
                        elif active_elem[1] == "Transition":
                            petr.inactivate_tr(active_elem[0], petr.transitions[active_elem[0]].pos)
                        elif active_elem[1] == "Link":
                            petr.inactivate_ln(active_elem[0])
                    activate = True
                    active_elem = (i.id, "Transition")
                    petr.activate_tr(active_elem[0], i.pos)
                    pg.display.update(rect)
            # То же самое, что в верхнем, только объект другой и функции соответственно для этого объекта
            for i in petr.links:
                if i.clicked(pos):
                    if type(active_elem) == tuple:
                        if active_elem[1] == "Point":
                            petr.inactivate_pt(active_elem[0], petr.points[active_elem[0]].pos)
                        elif active_elem[1] == "Transition":
                            petr.inactivate_tr(active_elem[0], petr.transitions[active_elem[0]].pos)
                        elif active_elem[1] == "Link":
                            petr.inactivate_ln(active_elem[0])
                    activate = True
                    active_elem = (i.id, "Link")
                    petr.activate_ln(active_elem[0])
                    pg.display.update(rect)
            # Далее спавним объекты, если стоят соответствующие флаги
            if sp.spawn_pt:
                if not activate:
                    petr.new_point(pos)
            elif sp.spawn_tr:
                if not activate:
                    petr.new_transition(pos)
            elif sp.spawn_link:
                # Для соединения необходимо 2 элемента
                if activate and active_elem[1] != "Link":
                    print(active_elem)
                    # Если элементов меньше чем 2
                    if len(link) < 2:
                        # То добавляем их в массив
                        link.append((petr.points[active_elem[0]], "Point") if active_elem[1] == "Point" else (petr.transitions[active_elem[0]], "Transition"))
                    # Если элементов 2
                    if len(link) == 2:
                        print(link)
                        # То соединяем в зависимости от того как расположены элементы
                        if link[0][1] == "Point" and link[1][1] == "Transition":
                            petr.new_link_point_to_transition(link[0][0].id, link[1][0].id)
                        elif link[0][1] == "Transition" and link[1][1] == "Point":
                            petr.new_link_transition_to_point(link[0][0].id, link[1][0].id)
                        # Обнуляем массив
                        link = []
            # Если спавним маркеры
            elif sp.spawn_mark:
                # Смотрим на активный элемент, если он является поинтом
                if activate and active_elem[1] == "Point":
                    # То при клике увеличиваем кол-во маркеров на 1
                    petr.points[active_elem[0]].markers += 1
                    pt = petr.points[active_elem[0]]
                    # Перерисовываем с новым кол-во маркеров
                    petr.draw_point(pt.pos, pt.id, orange)
            pg.display.update(rect)
            # Убираем флаг, чтобы всё не продолжало выполнятся повторно
            leftmouseclick = False
        # Получаем кортеж из того, какие кнопки мыши зажаты
        pressed = pg.mouse.get_pressed()
        # Если зажата левая кнопка и стоит флаг переноса
        if pressed[0] and sp.change_pos:
            # Ищем активный элемент
            if type(active_elem) == tuple:
                if active_elem[1] == "Point":
                    pt = petr.points[active_elem[0]]
                    pos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                    if pt.pos.x - petr.ptRadius < pos.x < pt.pos.x + petr.ptRadius and pt.pos.y - petr.ptRadius < pos.y < pt.pos.y + petr.ptRadius:
                        # Получаем позицию мышки
                        newPos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                        # Очищаем экран
                        pg.draw.rect(sc, (255, 255, 255), rect)
                        # Заново отрисовываем элементы
                        for i in petr.points:
                            if i.id != active_elem[0]:
                                petr.inactivate_pt(i.id, i.pos)
                        for i in petr.transitions:
                            petr.inactivate_tr(i.id, i.pos)
                        # Перерисовываем элемент в новую позицию (К мышке)
                        petr.activate_pt(active_elem[0], newPos)
                        petr.redraw_links()
                # То же самое, что и поинтами, только теперь переходы
                elif active_elem[1] == "Transition":
                    pt = petr.transitions[active_elem[0]]
                    pos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                    if pt.pos.x - petr.trWidth/2 < pos.x < pt.pos.x + petr.trWidth/2 and pt.pos.y - petr.trLength/2 < pos.y < pt.pos.y + petr.trLength/2:
                        newPos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                        pg.draw.rect(sc, (255, 255, 255), rect)
                        for i in petr.transitions:
                            if i.id != active_elem[0]:
                                petr.inactivate_tr(i.id, i.pos)
                        for i in petr.points:
                            petr.inactivate_pt(i.id, i.pos)
                        petr.activate_tr(active_elem[0], newPos)
                        petr.redraw_links()
            # Обновляем рабочую область
            pg.display.update(rect)
    else:
        leftmouseclick = False
    pygame_widgets.update(events)
    pg.display.update()
