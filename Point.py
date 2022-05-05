import Transition
import Pos


class Point:
    id: int
    pos: Pos
    markers: int
    trans_in: list
    trans_out: list

    def __init__(self, id, pos, markers=-1):
        self.id = id
        self.pos = pos
        self.markers = markers
        self.trans_out = []
        self.trans_in = []

    def addLink(self, tr: Transition, in_out: bool) -> bool:
        if in_out:
            if tr not in self.trans_in:
                self.trans_in.append(tr)
                return True
            else:
                return False
        else:
            if tr not in self.trans_out:
                self.trans_out.append(tr)
                return True
            else:
                return False


