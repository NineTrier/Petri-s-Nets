# Класс, содержащий различные флаги и функции для кнопок в меню
class Spawner:
    # Различные флаги
    spawn_link: bool # Флаг, разрешающий ставить соединение
    spawn_tr: bool # Флаг, разрешающий ставить переход
    spawn_pt: bool # Флаг, разрешающий ставить поинт
    spawn_mark: bool # Флаг, разрешающий изменять маркеры
    change_pos: bool # Флаг, разрешающий перемещение элементов

    def __init__(self):
        self.spawn_pt = False
        self.spawn_tr = False
        self.spawn_link = False
        self.spawn_mark = False
        self.change_pos = True

    def func_add_point(self):
        self.spawn_pt = True
        self.spawn_tr = False
        self.spawn_link = False
        self.spawn_mark = False
        self.change_pos = True

    def func_add_trans(self):
        self.spawn_pt = False
        self.spawn_tr = True
        self.spawn_link = False
        self.spawn_mark = False
        self.change_pos = True

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

