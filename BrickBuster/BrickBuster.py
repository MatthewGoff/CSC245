import pygame

from GameEngine import game_objects, util, game


class BrickBuster(game.Game):
    WINDOW_COLOR = pygame.Color("Black")

    # Play parameters
    PADDLE_SPEED = 6
    PADDLE_HEIGHT = 20
    PADDLE_WIDTH = 300
    NUM_BRICKS = 10
    NUM_ROWS = 2
    ROW_HEIGHT = 50
    TOP_MARGIN = 100

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
        self.paddle = game_objects.HorizontalPaddle(util.Vec2D(int(self.window_width/2),
                                                               self.window_height - 50),
                                                    util.Vec2D(0, 0),
                                                    BrickBuster.PADDLE_HEIGHT,
                                                    BrickBuster.PADDLE_WIDTH,
                                                    window_bounds,
                                                    pygame.Color("white"),
                                                    "paddle")

        radius = 20
        position = util.Vec2D(self.window_width/2, self.window_height-100)
        velocity = util.Vec2D(1, -5)
        color_scheme = game_objects.PongBall.RANDOM
        identifier = "ball"

        self.balls = [game_objects.PongBall(position,
                                            velocity,
                                            color_scheme,
                                            radius,
                                            identifier)]

        self.bricks = []
        for row in range(0, BrickBuster.NUM_ROWS):
            brick_width = self.window_width/BrickBuster.NUM_BRICKS
            brick_height = BrickBuster.ROW_HEIGHT
            position = util.Vec2D(brick_width/2, brick_height/2 + BrickBuster.TOP_MARGIN + (brick_height * row))
            for i in range(0, BrickBuster.NUM_BRICKS):
                self.bricks += [game_objects.Brick(position,
                                                   brick_height,
                                                   brick_width,
                                                   i)]
                position += util.Vec2D(brick_width, 0)

        self.objects += [[self.paddle]] + [self.balls] + [self.bricks]

        self.lives = 3

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.mute = not self.mute

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.paddle.set_velocity(
                util.Vec2D(BrickBuster.PADDLE_SPEED, 0))
        elif keys[pygame.K_LEFT]:
            self.paddle.set_velocity(util.Vec2D(BrickBuster.PADDLE_SPEED, 0) * (-1))
        else:
            self.paddle.set_velocity(util.Vec2D(0, 0))

    def apply_rules(self):
        game.Game.apply_rules(self)
        for brick in self.bricks:
            if brick.get_lives() == 0:
                self.bricks.remove(brick)

    def update_display(self):
        self.window.fill(BrickBuster.WINDOW_COLOR)

        if self.lives <= 0:
            util.draw_text(self.window,
                           "You lose!",
                           (self.window_width / 2, self.window_height / 2),
                           200)

        util.draw_text(self.window,
                       "lives: "+str(self.lives),
                       (self.window_width - 200, self.window_height-100),
                       80)

        self.paddle.draw(self.window)

        for ball in self.balls:
            ball.draw(self.window, BrickBuster.DRAW_VELOCITY)

        for brick in self.bricks:
            brick.draw(self.window)

        if BrickBuster.DRAW_QUADTREE:
            util.draw_quadtree(self.window, self.quadtree)

        if BrickBuster.LABEL_OBJECTS:
            for object in self.objects:
                util.draw_text(self.window,
                               object.__str__(),
                               object.get_position().to_tuple(),
                               24)

        # Swap display
        pygame.display.update()

    def notify_collision(self, wall, other):
        if wall == self.bottom_wall:
            #self.balls.remove(other)
            self.lives -= 1

# Start game
my_pong_game = BrickBuster(640 * 2, 480 * 2)
my_pong_game.run_game()
