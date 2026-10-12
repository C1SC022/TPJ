class Paddle:
    def __init__(self, x, y, width, height, window_width, window_height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window_width = window_width
        self.window_height = window_height

    def move(self, delta_y):
        self.y = max(0, min(self.window_height - self.height, self.y + delta_y))

    def position(self):
        # return the percentage of the paddle that the ball hits
        pass

    