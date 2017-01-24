import pygame

from GameEngine import game_objects, util, game


class PongGame(game.Game):
    WINDOW_COLOR = pygame.Color("Black")

    # Ball parameters
    NUM_BALLS = 20
    SPEED_RANGE = (0.5, 1)  # pixels per "tick"
    RADIUS_RANGE = (10, 50)  # in pixels

    # Play parameters
    PADDLE_SPEED = 3
    PADDLE_HEIGHT = 300
    PADDLE_WIDTH = 20

    # Display parameters
    DRAW_VELOCITY = False
    DRAW_QUADTREE = False
    LABEL_OBJECTS = False

    def __init__(self, window_width, window_height):
        game.Game.__init__(self, window_width, window_height)

        window_bounds = util.Rectangle(0,
                                       self.window_height,
                                       0,
                                       self.window_width)
        self.paddle1 = game_objects.VerticalPaddle(util.Vec2D(50, int(self.window_height / 2)),
                                                   util.Vec2D(0, 0),
                                                   PongGame.PADDLE_HEIGHT,
                                                   PongGame.PADDLE_WIDTH,
                                                   window_bounds,
                                                   pygame.Color("white"),
                                                   "paddle1")
        self.paddle2 = game_objects.VerticalPaddle(util.Vec2D(self.window_width - 50, int(self.window_height / 2)),
                                                   util.Vec2D(0, 0),
                                                   PongGame.PADDLE_HEIGHT,
                                                   PongGame.PADDLE_WIDTH,
                                                   window_bounds,
                                                   pygame.Color("white"),
                                                   "paddle2")

        self.balls = []
        for i in range(0, PongGame.NUM_BALLS):
            radius = util.RandGen.randint(PongGame.RADIUS_RANGE[0], PongGame.RADIUS_RANGE[1])
            position = util.Vec2D(util.RandGen.uniform(0 + radius, self.window_width - radius),
                                  util.RandGen.uniform(0 + radius, self.window_height - radius))
            velocity = util.random_velocity(PongGame.SPEED_RANGE)
            color_scheme = game_objects.PongBall.RANDOM
            identifier = i

            self.balls += [game_objects.PongBall(position, velocity, color_scheme, radius, identifier)]

        self.objects += [self.balls]
        self.objects += [[self.paddle1, self.paddle2]]

        self.score1 = 0
        self.score2 = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.mute = not self.mute

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.paddle2.set_velocity(util.Vec2D(0, -1 * PongGame.PADDLE_SPEED))
        elif keys[pygame.K_DOWN]:
            self.paddle2.set_velocity(util.Vec2D(0, PongGame.PADDLE_SPEED))
        else:
            self.paddle2.set_velocity(util.Vec2D(0, 0))

        if keys[pygame.K_w]:
            self.paddle1.set_velocity(util.Vec2D(0, -1 * PongGame.PADDLE_SPEED))
        elif keys[pygame.K_s]:
            self.paddle1.set_velocity(util.Vec2D(0, PongGame.PADDLE_SPEED))
        else:
            self.paddle1.set_velocity(util.Vec2D(0, 0))

    def simulate(self):
        for ball in self.balls:
            ball.simulate()
        self.paddle1.simulate()
        self.paddle2.simulate()

    def update_display(self):
        self.window.fill(PongGame.WINDOW_COLOR)

        util.draw_text(self.window,
                       str(self.score1),
                       (100, 100),
                       100)
        util.draw_text(self.window,
                       str(self.score2),
                       (self.window_width - 100, 100),
                       100)

        self.paddle1.draw(self.window)
        self.paddle2.draw(self.window)

        if self.score1 >= PongGame.NUM_BALLS / 2 + 1:
            util.draw_text(self.window,
                           "Player 1 Wins!",
                           (self.window_width / 2, self.window_height / 2),
                           200)
        elif self.score2 >= PongGame.NUM_BALLS / 2 + 1:
            util.draw_text(self.window,
                           "Player 2 Wins!",
                           (self.window_width / 2, self.window_height / 2),
                           200)

        for ball in self.balls:
            ball.draw(self.window, PongGame.DRAW_VELOCITY)

        if PongGame.DRAW_QUADTREE:
            util.draw_quadtree(self.window, self.quadtree)

        if PongGame.LABEL_OBJECTS:
            self.label_objects()

        # Swap display
        pygame.display.update()

    def notify_collision(self, wall, other):
        if wall == self.left_wall:
            self.score2 += 1
            self.balls.remove(other)

        if wall == self.right_wall:
            self.score1 += 1
            self.balls.remove(other)

# Start game
my_pong_game = PongGame(640*2, 480*2)
my_pong_game.run_game()
