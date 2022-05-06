import math

import Point
import Transition
import Pos
import Link
from Widgets import Table
import pygame as pg

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 127)
blue = (0, 0, 255)
black = (0, 0, 0)
yellow = (222, 184, 135)
dark_yellow = (210, 180, 140)
orange = (218, 165, 32)
dark_green = (46, 139, 87)
pg.font.init()


class Petri:
    sc: pg.display
    points: dict
    transitions: dict
    links: dict
    ptRadius: int
    trLength: int
    trWidth: int

    def __init__(self, sc, ptRadius=10, trLength=20, trWidth=6):
        self.sc = sc
        self.points = {}
        self.transitions = {}
        self.links = {}
        self.ptRadius = ptRadius
        self.trLength = trLength
        self.trWidth = trWidth

    def draw_point(self, pos: Pos, idPt: int, color):
        pg.draw.circle(self.sc, (200, 200, 200), (pos.x + 5, pos.y + 5), self.ptRadius)
        pg.draw.circle(self.sc, dark_yellow, (pos.x, pos.y), self.ptRadius + 1)
        pg.draw.circle(self.sc, color, (pos.x, pos.y), self.ptRadius)

        font = pg.font.Font("CaviarDreams.ttf", int(self.ptRadius / 1.2))
        text = font.render(f"P{idPt}", True, black)
        self.sc.blit(text, (pos.x - (self.ptRadius / 2), pos.y - self.ptRadius - text.get_size()[0] - 5))

        text = font.render("oo" if self.points[idPt].markers == -1 else f"{self.points[idPt].markers}", True, white)
        self.sc.blit(text, (
            self.points[idPt].pos.x - text.get_size()[0] / 2, self.points[idPt].pos.y - text.get_size()[1] / 2))

    def draw_transition(self, pos, idTr: int, color):
        pg.draw.rect(self.sc, (200, 200, 200),
                     (pos.x - self.trWidth / 2 + 1, pos.y - self.trLength / 2 + 1, self.trWidth + 5, self.trLength + 5))
        pg.draw.rect(self.sc, (0, 100, 0),
                     (pos.x - self.trWidth / 2 - 1, pos.y - self.trLength / 2 - 1, self.trWidth + 2, self.trLength + 2))
        pg.draw.rect(self.sc, color,
                     (pos.x - (self.trWidth / 2), pos.y - (self.trLength / 2), self.trWidth, self.trLength))

        font = pg.font.Font("CaviarDreams.ttf", int(self.ptRadius / 1.2))
        text = font.render(f"T{idTr}", True, black)
        self.sc.blit(text, (pos.x - text.get_size()[0] / 2, pos.y - self.trLength / 2 - text.get_size()[1]))

    def draw_link_tr_pt(self, trId: int, ptId: int, lnId: int, color):
        tr = self.transitions[trId]
        pt = self.points[ptId]
        mark = self.links[lnId].markers
        font = pg.font.Font("CaviarDreams.ttf", int(self.ptRadius / 1.2))
        text = font.render(f"{mark}", True, black)
        width_line = 1
        if pt.pos.x > tr.pos.x:
            pg.draw.line(self.sc, color, (tr.pos.x + (self.trWidth / 2), tr.pos.y),
                         (pt.pos.x - self.ptRadius * 1.2 - 1, pt.pos.y), width_line)
            rad = math.pi / 180
            trirad = 5
            start = (tr.pos.x + (self.trWidth / 2), tr.pos.y)
            end = (pt.pos.x - self.ptRadius * 1.2, pt.pos.y)
            pg.draw.rect(self.sc, white, ((start[0] + end[0]) / 2, ((start[1] + end[1]) / 2) + 20, 20, 15))
            self.sc.blit(text, ((start[0] + end[0]) / 2, ((start[1] + end[1]) / 2) + 20))
            rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
            pg.draw.polygon(self.sc, color, ((end[0] + trirad * math.sin(rotation),
                                              end[1] + trirad * math.cos(rotation)),
                                             (end[0] + trirad * math.sin(rotation - 120 * rad),
                                              end[1] + trirad * math.cos(rotation - 120 * rad)),
                                             (end[0] + trirad * math.sin(rotation + 120 * rad),
                                              end[1] + trirad * math.cos(rotation + 120 * rad))))
        elif pt.pos.x < tr.pos.x:
            pg.draw.line(self.sc, color, (tr.pos.x - (self.trWidth / 2), tr.pos.y),
                         (pt.pos.x + self.ptRadius + 1, pt.pos.y), width_line)

            rad = math.pi / 180
            trirad = 5
            start = (tr.pos.x - (self.trWidth / 2), tr.pos.y)
            end = (pt.pos.x + self.ptRadius * 1.2, pt.pos.y)
            pg.draw.rect(self.sc, white, ((start[0] + end[0]) / 2, ((start[1] + end[1]) / 2) + 20, 20, 15))
            self.sc.blit(text, ((start[0] + end[0]) / 2, ((start[1] + end[1]) / 2) + 20))
            rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
            pg.draw.polygon(self.sc, color, ((end[0] + trirad * math.sin(rotation),
                                              end[1] + trirad * math.cos(rotation)),
                                             (end[0] + trirad * math.sin(rotation - 120 * rad),
                                              end[1] + trirad * math.cos(rotation - 120 * rad)),
                                             (end[0] + trirad * math.sin(rotation + 120 * rad),
                                              end[1] + trirad * math.cos(rotation + 120 * rad))))

    def draw_link_pt_tr(self, ptId, trId, lnId, color):
        tr = self.transitions[trId]
        pt = self.points[ptId]
        mark = self.links[lnId].markers
        font = pg.font.Font("CaviarDreams.ttf", int(self.ptRadius / 1.2))
        text = font.render(f"{mark}", True, black)
        width_line = 1
        if pt.pos.x > tr.pos.x:
            trirad = 5
            pg.draw.line(self.sc, color, (pt.pos.x - self.ptRadius - 1, pt.pos.y),
                         (tr.pos.x + (self.trWidth / 2) + trirad, tr.pos.y), width_line)

            rad = math.pi / 180
            start = (pt.pos.x - self.ptRadius - 1, pt.pos.y)
            end = (tr.pos.x + (self.trWidth / 2) + trirad, tr.pos.y)
            pg.draw.rect(self.sc, white, ((start[0] + end[0]) / 2, ((start[1] + end[1]) / 2) - 20, 20, 15))
            self.sc.blit(text, ((start[0] + end[0]) / 2, ((start[1] + end[1]) / 2) - 20))
            rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
            pg.draw.polygon(self.sc, color, ((end[0] + trirad * math.sin(rotation),
                                              end[1] + trirad * math.cos(rotation)),
                                             (end[0] + trirad * math.sin(rotation - 120 * rad),
                                              end[1] + trirad * math.cos(rotation - 120 * rad)),
                                             (end[0] + trirad * math.sin(rotation + 120 * rad),
                                              end[1] + trirad * math.cos(rotation + 120 * rad))))

        elif pt.pos.x < tr.pos.x:
            trirad = 5
            pg.draw.line(self.sc, color, (pt.pos.x + self.ptRadius + 1, pt.pos.y),
                         (tr.pos.x - (self.trWidth / 2) - trirad, tr.pos.y), width_line)

            rad = math.pi / 180
            start = (pt.pos.x + self.ptRadius + 1, pt.pos.y)
            end = (tr.pos.x - (self.trWidth / 2) - trirad, tr.pos.y)
            pg.draw.rect(self.sc, white, ((start[0] + end[0]) / 2, ((start[1] + end[1]) / 2) - 20, 20, 15))
            self.sc.blit(text, ((start[0] + end[0]) / 2, ((start[1] + end[1]) / 2) - 20))
            rotation = (math.atan2(start[1] - end[1], end[0] - start[0])) + math.pi / 2
            pg.draw.polygon(self.sc, color, ((end[0] + trirad * math.sin(rotation),
                                              end[1] + trirad * math.cos(rotation)),
                                             (end[0] + trirad * math.sin(rotation - 120 * rad),
                                              end[1] + trirad * math.cos(rotation - 120 * rad)),
                                             (end[0] + trirad * math.sin(rotation + 120 * rad),
                                              end[1] + trirad * math.cos(rotation + 120 * rad))))

    def new_point(self, pos: Pos):
        pt = Point.Point(max(self.points.keys()) + 1 if len(self.points) > 0 else 1, pos)
        self.points[pt.id] = pt
        self.draw_point(pos, pt.id, yellow)

    def new_transition(self, pos: Pos):
        tr = Transition.Transition(max(self.transitions.keys()) + 1 if len(self.transitions) > 0 else 1, pos)
        self.transitions[tr.id] = tr
        self.draw_transition(pos, tr.id, green)

    def new_link_transition_to_point(self, trId: int, ptId: int):
        tr = self.transitions[trId]
        pt = self.points[ptId]

        add = True
        if tr.addLink(pt, 0):
            self.transitions[trId] = tr
        else:
            add = False
        if pt.addLink(tr, 1):
            self.points[ptId] = pt
        else:
            add = False
        print(add)
        if add:
            ln = Link.Link(max(self.links.keys())+1 if len(self.links) > 0 else 1, tr.pos, pt.pos, (trId, "Transition"), (ptId, "Point"))
            self.links[ln.id] = ln
        else:
            ln = None
            for i in self.links.values():
                if i.start_elem_id[0] == tr.id and i.start_elem_id[1] == "Transition" and i.end_elem_id[0] == pt.id and \
                        i.end_elem_id[1] == "Point":
                    i.markers += 1
                    ln = i
        self.draw_link_tr_pt(trId, ptId, ln.id, black)

    def new_link_point_to_transition(self, ptId: int, trId: int):
        tr = self.transitions[trId]
        pt = self.points[ptId]

        add = True
        if tr.addLink(pt, 1):
            self.transitions[trId] = tr
        else:
            add = False
        if pt.addLink(tr, 0):
            self.points[ptId] = pt
        else:
            add = False
        print(add)
        if add:
            ln = Link.Link(max(self.links.keys())+1 if len(self.links) > 0 else 1, pt.pos, tr.pos, (ptId, "Point"), (trId, "Transition"))
            self.links[ln.id] = ln
        else:
            ln = None
            for i in self.links.values():
                if i.start_elem_id[0] == pt.id and i.start_elem_id[1] == "Point" and i.end_elem_id[0] == tr.id and \
                        i.end_elem_id[1] == "Transition":
                    i.markers += 1
                    ln = i
        self.draw_link_pt_tr(ptId, trId, ln.id, black)

    def activate_pt(self, ptId: int, newPos: Pos):
        pt = self.points[ptId]
        pt.pos = newPos
        self.points[ptId] = pt
        self.draw_point(newPos, pt.id, orange)

    def inactivate_pt(self, ptId: int, newPos: Pos):
        pt = self.points[ptId]
        pt.pos = newPos
        self.points[ptId] = pt
        self.draw_point(newPos, pt.id, yellow)

    def activate_tr(self, trId: int, newPos: Pos):
        tr = self.transitions[trId]
        tr.pos = newPos
        self.transitions[trId] = tr
        self.draw_transition(newPos, tr.id, dark_green)

    def inactivate_tr(self, trId: int, newPos: Pos):
        tr = self.transitions[trId]
        tr.pos = newPos
        self.transitions[trId] = tr
        self.draw_transition(newPos, tr.id, green)

    def activate_ln(self, lnId: int):
        ln = self.links[lnId]
        if ln.start_elem_id[1] == "Transition":
            self.draw_link_tr_pt(ln.start_elem_id[0], ln.end_elem_id[0], ln.id, red)
        else:
            self.draw_link_pt_tr(ln.start_elem_id[0], ln.end_elem_id[0], ln.id, red)

    def inactivate_ln(self, lnId: int):
        ln = self.links[lnId]
        if ln.start_elem_id[1] == "Transition":
            self.draw_link_tr_pt(ln.start_elem_id[0], ln.end_elem_id[0], ln.id, black)
        else:
            self.draw_link_pt_tr(ln.start_elem_id[0], ln.end_elem_id[0], ln.id, black)

    def redraw_links(self):
        for i in self.links.values():
            if i.start_elem_id[1] == "Transition":
                i.pos_start = self.transitions[i.start_elem_id[0]].pos
                i.pos_end = self.points[i.end_elem_id[0]].pos
                self.draw_link_tr_pt(i.start_elem_id[0], i.end_elem_id[0], i.id, black)
            else:
                i.pos_start = self.points[i.start_elem_id[0]].pos
                i.pos_end = self.transitions[i.end_elem_id[0]].pos
                self.draw_link_pt_tr(i.start_elem_id[0], i.end_elem_id[0], i.id, black)

    def delete_transition(self, trId):
        tr = self.transitions[trId]
        for i in self.points.values():
            if tr in i.trans_in:
                i.trans_in.remove(tr)
            if tr in i.trans_out:
                i.trans_out.remove(tr)
        list_to_del = []
        for i in self.links.values():
            if i.start_elem_id[1] == "Transition" and i.start_elem_id[0] == tr.id and i not in list_to_del:
                list_to_del.append(i)
            if i.end_elem_id[1] == "Transition" and i.end_elem_id[0] == tr.id and i not in list_to_del:
                list_to_del.append(i)
        for i in list_to_del:
            self.links.pop(i.id)
        self.transitions.pop(tr.id)

    def delete_point(self, ptId):
        pt = self.points[ptId]
        for i in self.transitions.values():
            if pt in i.points_in:
                i.points_in.remove(pt)
            if pt in i.points_out:
                i.points_out.remove(pt)
        list_to_del = []
        for i in self.links.values():
            if i.start_elem_id[1] == "Point" and i.start_elem_id[0] == pt.id and i not in list_to_del:
                list_to_del.append(i)
            if i.end_elem_id[1] == "Point" and i.end_elem_id[0] == pt.id and i not in list_to_del:
                list_to_del.append(i)
        for i in list_to_del:
            self.links.pop(i.id)
        self.points.pop(pt.id)

    def delete_link(self, lnId):
        ln = self.links[lnId]
        if ln.start_elem_id[1] == "Point":
            tr = self.transitions[ln.end_elem_id[0]]
            pt = self.points[ln.start_elem_id[0]]
            tr.points_in.remove(pt)
            pt.trans_out.remove(tr)
        else:
            tr = self.transitions[ln.start_elem_id[0]]
            pt = self.points[ln.end_elem_id[0]]
            tr.points_out.remove(pt)
            pt.trans_in.remove(tr)
        self.links.pop(ln.id)

    def matr_incident(self, pos: Pos):
        headers = [f"P{i.id}" for i in self.points.values()]
        index = [f"T{i.id}" for i in self.transitions.values()]
        matr = []
        for i in self.transitions.values():
            row = []
            for j in self.points.values():
                go_in = 1 if j in i.points_out else 0
                go_out = 1 if j in i.points_in else 0
                row.append(0 + go_in - go_out)
            matr.append(row)

        table = Table(self.sc, matr, headers, index)
        table.draw(pos)

    def PTIO(self):
        P = [f"P{i.id}" for i in self.points.values()]
        T = [f"T{i.id}" for i in self.transitions.values()]
        I = []
        O = []
        for i in self.transitions.values():
            i.points_in.sort(key=Transition.key)
            i.points_out.sort(key=Transition.key)
            row = []
            for j in i.points_in:
                row.append(f"p{j.id}")
            I.append(row)
            row = []
            for j in i.points_out:
                row.append(f"p{j.id}")
            O.append(row)
        print(P)
        print(T)
        print(I)
        print(O)
