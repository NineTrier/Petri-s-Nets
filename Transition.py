import Point
import Pos


class Transition:
    id: int
    pos: Pos
    points_in: list
    points_out: list

    def __init__(self, id, pos):
        self.id = id
        self.pos = pos
        self.points_in = []
        self.points_out = []

    def addLink(self, pt: Point, in_out: bool):
        if in_out:
            if pt not in self.points_in:
                self.points_in.append(pt)
                return True
            else:
                return False
        else:
            if pt not in self.points_out:
                self.points_out.append(pt)
                return True
            else:
                return False
