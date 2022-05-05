import pygame.event
import pygame_widgets

from Petri import *
import sys
from Menu import Menu

from FunctionsForButton import Spawner

sc = pg.display.set_mode((1000, 500))
rect = (10, 10, 800-20, sc.get_size()[1]-20)
sc.fill((220, 220, 220))
pg.draw.rect(sc, (255, 255, 255), rect)
petr = Petri(sc, 20, 60, 10)
sp = Spawner()

button_color = (119, 136, 153)
button_color_hover = (105, 105, 105)
button_color_pressed = (192, 192, 192)
menu = Menu(sc, 200, 500, Pos.Pos(sc.get_size()[0] - 200, 0))
menu.add_button("Переместить", button_color, button_color_hover, button_color_pressed, sp.func_change_pos)
menu.add_button("Добавить Point", button_color, button_color_hover, button_color_pressed, sp.func_add_point)
menu.add_button("Добавить Transition", button_color, button_color_hover, button_color_pressed, sp.func_add_trans)
menu.add_button("Добавить Link", button_color, button_color_hover, button_color_pressed, sp.func_add_link)
menu.add_button("Добавить Marker", button_color, button_color_hover, button_color_pressed, sp.func_add_mark)

pg.display.update()
active_elem = None

link = []

leftmouseclick = False
while True:
    events = pg.event.get()
    for i in events:
        if i.type == pg.QUIT:
            sys.exit()
        elif i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                leftmouseclick = True
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_DELETE:
                if active_elem[1] == "Transition":
                    petr.delete_transition(active_elem[0])
                elif active_elem[1] == "Point":
                    petr.delete_point(active_elem[0])
                elif active_elem[1] == "Link":
                    petr.delete_link(active_elem[0])
                pg.draw.rect(sc, (255, 255, 255), rect)
                for j in petr.transitions:
                    petr.inactivate_tr(j.id, j.pos)
                for j in petr.points:
                    petr.inactivate_pt(j.id, j.pos)
                petr.redraw_links()
                pg.display.update(rect)
                active_elem = None
    spawn_pt = sp.spawn_pt
    spawn_tr = sp.spawn_tr
    spawn_link = sp.spawn_link
    spawn_mark = sp.spawn_mark
    change_pos = sp.change_pos
    mouse_pos = pg.mouse.get_pos()
    if 10 + petr.ptRadius < mouse_pos[0] < sc.get_size()[0] - 235 and petr.trLength < mouse_pos[1] < sc.get_size()[1] - petr.trLength:
        if leftmouseclick:
            pos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            activate = False
            for i in petr.points:
                if i.pos.x - petr.ptRadius < pos.x < i.pos.x + petr.ptRadius and i.pos.y - petr.ptRadius < pos.y < i.pos.y + petr.ptRadius:
                    if type(active_elem) == tuple:
                        if active_elem[1] == "Point":
                            petr.inactivate_pt(active_elem[0], petr.points[active_elem[0]].pos)
                        elif active_elem[1] == "Transition":
                            petr.inactivate_tr(active_elem[0], petr.transitions[active_elem[0]].pos)
                        elif active_elem[1] == "Link":
                            petr.inactivate_ln(active_elem[0])
                    activate = True
                    active_elem = (i.id, 'Point')
                    petr.activate_pt(active_elem[0], i.pos)
                    pg.display.update(rect)
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
            if spawn_pt:
                if not activate:
                    petr.new_point(pos)
            elif spawn_tr:
                if not activate:
                    petr.new_transition(pos)
            elif spawn_link:
                if activate and active_elem[1] != "Link":
                    print(active_elem)
                    if len(link) < 2:
                        link.append((petr.points[active_elem[0]], "Point") if active_elem[1] == "Point" else (petr.transitions[active_elem[0]], "Transition"))
                    if len(link) == 2:
                        print(link)
                        if link[0][1] == "Point" and link[1][1] == "Transition":
                            petr.new_link_point_to_transition(link[0][0].id, link[1][0].id)
                        elif link[0][1] == "Transition" and link[1][1] == "Point":
                            petr.new_link_transition_to_point(link[0][0].id, link[1][0].id)
                        link = []
            elif spawn_mark:
                if activate and active_elem[1] == "Point":
                    petr.points[active_elem[0]].markers += 1
                    pt = petr.points[active_elem[0]]
                    petr.draw_point(pt.pos, pt.id, orange)
            pg.display.update(rect)
            leftmouseclick = False
        pressed = pg.mouse.get_pressed()
        if pressed[0] and change_pos:
            if type(active_elem) == tuple:
                if active_elem[1] == "Point":
                    pt = petr.points[active_elem[0]]
                    pos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                    if pt.pos.x - petr.ptRadius < pos.x < pt.pos.x + petr.ptRadius and pt.pos.y - petr.ptRadius < pos.y < pt.pos.y + petr.ptRadius:
                        newPos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                        pg.draw.rect(sc, (255, 255, 255), rect)
                        for i in petr.points:
                            if i.id != active_elem[0]:
                                petr.inactivate_pt(i.id, i.pos)
                        for i in petr.transitions:
                            petr.inactivate_tr(i.id, i.pos)
                        petr.activate_pt(active_elem[0], newPos)
                        petr.redraw_links()
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
            pg.display.update(rect)
    else:
        leftmouseclick = False
    pygame_widgets.update(events)
    pg.display.update()
