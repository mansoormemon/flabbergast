import arcade as arc


class Direction:
    UP = 1
    DOWN = 2
    LEFT = 4
    RIGHT = 8


class Player(arc.SpriteSolidColor):
    def __init__(self, grid, spawn_point, *args, **kwargs):
        super().__init__(64, 64, arc.color.RED, *args, **kwargs)

        self.speed = 3
        self.center_x, self.center_y = spawn_point
        self.scale = grid.scale

    # def update(self):
    #     self.center_x += self.c
    #     self.center_y += self.delta_y
    #     print(self.center_x, self.center_y)

    def move_up(self):
        self.change_y = self.speed

    def move_down(self):
        self.change_y = -self.speed

    def move_right(self):
        self.change_x = self.speed

    def move_left(self):
        self.change_x = -self.speed
