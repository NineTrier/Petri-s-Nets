import Pos


class Link:
    id: int
    pos_start: Pos
    pos_end: Pos
    start_elem_id: tuple
    end_elem_id: tuple

    def __init__(self, id: int, pos_start: Pos, pos_end: Pos, start_elem_id: tuple, end_elem_id: tuple):
        self.id = id
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.start_elem_id = start_elem_id
        self.end_elem_id = end_elem_id

    def clicked(self, pos: Pos) -> bool:
        if self.pos_start.x > self.pos_end.x:
            if self.pos_start.y > self.pos_end.y:
                if self.pos_end.x <= pos.x <= self.pos_start.x and self.pos_end.y <= pos.y <= self.pos_start.y:
                    return True
            else:
                if self.pos_end.x <= pos.x <= self.pos_start.x and self.pos_end.y >= pos.y >= self.pos_start.y:
                    return True
        else:
            if self.pos_start.y > self.pos_end.y:
                if self.pos_end.x >= pos.x >= self.pos_start.x and self.pos_end.y <= pos.y <= self.pos_start.y:
                    return True
            else:
                if self.pos_end.x >= pos.x >= self.pos_start.x and self.pos_end.y >= pos.y >= self.pos_start.y:
                    return True
        return False
