from turtle import window_height, window_width


class ball:
    def __init__(self, velocity_x, velocity_y, window_width, window_height):
        self.x = window_width // 2
        self.y = window_height // 2
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.window_width = window_width
        self.window_height = window_height

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    def restart(self):
        self.x, self.y = self.window_width // 2, self.window_height // 2