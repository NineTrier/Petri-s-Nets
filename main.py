from Petri import *
import sys


sc = pg.display.set_mode((1000, 500))
sc.fill((255, 255, 255))
pg.display.update()
petr = Petri(sc, 20, 60, 10)

active_elem = None

spawn_pt = False
spawn_tr = False

spawn_link = False
link = []

spawn_mark = False
leftmouseclick = False
while True:
    for i in pg.event.get():
        if i.type == pg.QUIT:
            sys.exit()
        elif i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                leftmouseclick = True
        elif i.type == pg.KEYDOWN:
            if i.key == pg.K_SPACE:
                spawn_link = True
                spawn_tr = False
                spawn_pt = False
                spawn_mark = False
            elif i.key == pg.K_p:
                spawn_pt = True
                spawn_tr = False
                spawn_link = False
                spawn_mark = False
            elif i.key == pg.K_t:
                spawn_tr = True
                spawn_pt = False
                spawn_link = False
                spawn_mark = False
            elif i.key == pg.K_m:
                spawn_mark = True
                spawn_pt = False
                spawn_tr = False
                spawn_link = False
            elif i.key == pg.K_DELETE:
                if active_elem[1] == "Transition":
                    petr.delete_transition(active_elem[0])
                elif active_elem[1] == "Point":
                    petr.delete_point(active_elem[0])
                elif active_elem[1] == "Link":
                    petr.delete_link(active_elem[0])
                sc.fill((255, 255, 255))
                for j in petr.transitions:
                    petr.inactivate_tr(j.id, j.pos)
                for j in petr.points:
                    petr.inactivate_pt(j.id, j.pos)
                petr.redraw_links()
                pg.display.flip()
                active_elem = None
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
                pg.display.flip()
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
                pg.display.flip()
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
                pg.display.flip()
        if spawn_pt:
            if not activate:
                petr.new_point(pos)
            pg.display.flip()
        elif spawn_tr:
            if not activate:
                petr.new_transition(pos)
            pg.display.flip()
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
                    pg.display.flip()
                    link = []
        elif spawn_mark:
            if activate and active_elem[1] == "Point":
                petr.points[active_elem[0]].markers += 1
                pt = petr.points[active_elem[0]]
                petr.draw_point(pt.pos, pt.id, orange)
        leftmouseclick = False

    pressed = pg.mouse.get_pressed()
    if pressed[0] and not spawn_link:
        if type(active_elem) == tuple:
            if active_elem[1] == "Point":
                pt = petr.points[active_elem[0]]
                pos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                if pt.pos.x - petr.ptRadius < pos.x < pt.pos.x + petr.ptRadius and pt.pos.y - petr.ptRadius < pos.y < pt.pos.y + petr.ptRadius:
                    newPos = Pos.Pos(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
                    sc.fill((255, 255, 255))
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
                    sc.fill((255, 255, 255))
                    for i in petr.transitions:
                        if i.id != active_elem[0]:
                            petr.inactivate_tr(i.id, i.pos)
                    for i in petr.points:
                        petr.inactivate_pt(i.id, i.pos)
                    petr.activate_tr(active_elem[0], newPos)
                    petr.redraw_links()
        pg.display.flip()

