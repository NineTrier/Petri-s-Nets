class Spawner:

    spawn_link: bool
    spawn_tr: bool
    spawn_pt: bool
    spawn_mark: bool
    change_pos: bool

    def __init__(self):
        self.spawn_pt = False
        self.spawn_tr = False
        self.spawn_link = False
        self.spawn_mark = False
        self.change_pos = False

    def func_add_point(self):
        self.spawn_pt = True
        self.spawn_tr = False
        self.spawn_link = False
        self.spawn_mark = False
        self.change_pos = False

    def func_add_trans(self):
        self.spawn_pt = False
        self.spawn_tr = True
        self.spawn_link = False
        self.spawn_mark = False
        self.change_pos = False

    def func_add_link(self):
        self.spawn_pt = False
        self.spawn_tr = False
        self.spawn_link = True
        self.spawn_mark = False
        self.change_pos = False

    def func_add_mark(self):
        self.spawn_pt = False
        self.spawn_tr = False
        self.spawn_link = False
        self.spawn_mark = True
        self.change_pos = False

    def func_change_pos(self):
        self.spawn_pt = False
        self.spawn_tr = False
        self.spawn_link = False
        self.spawn_mark = False
        self.change_pos = True
