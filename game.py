import ball

class game:
    def __init__(self, window_width, window_height):
        self.ball = ball(200, 200, window_width, window_height)
        self.ball.restart()

    def update(self, dt):
        self.ball.update(dt)
