import pygame

from GameEngine import objects, util


class PongGame:
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

        print "Seed = "+str(util.get_seed())
        pygame.init()
        pygame.mixer.init()
        self.bounce_sound = pygame.mixer.Sound("bounce.wav")
        self.mute = True

        self.score1 = 0
        self.score2 = 0

        self.window_width = window_width
        self.window_height = window_height
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

        window_bounds = util.Rectangle(0, self.window_height, 0, self.window_width)
        self.paddle1 = objects.VerticalPaddle(util.Vec2D(50, int(self.window_height / 2)),
                                              util.Vec2D(0, 0),
                                              PongGame.PADDLE_HEIGHT,
                                              PongGame.PADDLE_WIDTH,
                                              window_bounds,
                                              pygame.Color("white"),
                                              "paddle1")
        self.paddle2 = objects.VerticalPaddle(util.Vec2D(self.window_width - 50, int(self.window_height / 2)),
                                              util.Vec2D(0, 0),
                                              PongGame.PADDLE_HEIGHT,
                                              PongGame.PADDLE_WIDTH,
                                              window_bounds,
                                              pygame.Color("white"),
                                              "paddle2")
        self.left_wall = objects.Wall(util.Vec2D(0, self.window_height / 2),
                                      util.Vec2D(0, 0),
                                      util.Vec2D(1, 0),
                                      self.window_height,
                                      float("inf"),
                                      pygame.Color("white"),
                                      "left wall",
                                      self.notify_collision)
        self.top_wall = objects.Wall(util.Vec2D(self.window_width / 2, 0),
                                     util.Vec2D(0, 0),
                                     util.Vec2D(0, 1),
                                     self.window_width,
                                     float("inf"),
                                     pygame.Color("white"),
                                     "top wall",
                                     self.notify_collision)
        self.bottom_wall = objects.Wall(util.Vec2D(self.window_width / 2, self.window_height),
                                        util.Vec2D(0, 0),
                                        util.Vec2D(0, -1),
                                        self.window_width,
                                        float("inf"),
                                        pygame.Color("white"),
                                        "bottom wall",
                                        self.notify_collision)
        self.right_wall = objects.Wall(util.Vec2D(self.window_width, self.window_height / 2),
                                       util.Vec2D(0, 0),
                                       util.Vec2D(-1, 0),
                                       self.window_height,
                                       float("inf"),
                                       pygame.Color("white"),
                                       "right wall",
                                       self.notify_collision)

        self.walls = self.paddle1.get_walls() + self.paddle2.get_walls() + [self.top_wall,
                                                                            self.bottom_wall,
                                                                            self.right_wall,
                                                                            self.left_wall]

        self.balls = []
        for i in range(0, PongGame.NUM_BALLS):
            radius = util.RandGen.randint(PongGame.RADIUS_RANGE[0], PongGame.RADIUS_RANGE[1])
            position = util.Vec2D(util.RandGen.uniform(0 + radius, self.window_width - radius),
                                  util.RandGen.uniform(0 + radius, self.window_height - radius))
            velocity = util.random_velocity(PongGame.SPEED_RANGE)
            color_scheme = objects.PongBall.SPEED
            identifier = i

            self.balls += [objects.PongBall(position, velocity, color_scheme, radius, identifier)]

        self.quadtree = util.Quadtree(util.Rectangle(0, self.window_height, 0, self.window_width))

    def run_game(self):
        # The game loop starts here.
        keep_going = True
        while keep_going:

            # 1. Handle events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
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

            # 2. Apply rules of game world
            self.quadtree.insert_many(self.balls)
            self.quadtree.insert_many(self.walls)

            for ball in self.balls:
                neighbors = self.quadtree.get_neighbors(ball)
                for neighbor in neighbors:
                    self.resolve_collision(neighbor, ball)

            # 3. Simulate the world
            for ball in self.balls:
                ball.simulate()
            self.paddle1.simulate()
            self.paddle2.simulate()

            # 4. Draw
            self.window.fill(PongGame.WINDOW_COLOR)

            draw_text(self.window, str(self.score1), (100, 100), 100)
            draw_text(self.window, str(self.score2), (self.window_width-100, 100), 100)

            self.paddle1.draw(self.window)
            self.paddle2.draw(self.window)

            if self.score1 >= PongGame.NUM_BALLS/2+1:
                draw_text(self.window, "Player 1 Wins!", (self.window_width / 2, self.window_height / 2), 200)
            elif self.score2 >= PongGame.NUM_BALLS/2+1:
                draw_text(self.window, "Player 2 Wins!", (self.window_width / 2, self.window_height / 2), 200)

            for ball in self.balls:
                ball.draw(self.window, PongGame.DRAW_VELOCITY)

            if PongGame.DRAW_QUADTREE:
                draw_quadtree(self.window, self.quadtree)

            if PongGame.LABEL_OBJECTS:
                for ball in self.balls:
                    draw_text(self.window, ball.__str__(), ball.get_position().to_tuple(), 24)

                    draw_text(self.window, self.paddle1.__str__(), self.paddle1.get_position().to_tuple(), 24)
                    draw_text(self.window, self.paddle2.__str__(), self.paddle2.get_position().to_tuple(), 24)

                for wall in self.walls:
                    draw_text(self.window, wall.__str__(), wall.get_position().to_tuple(), 24)

            # Swap display
            pygame.display.update()

            # 5. Takedown
            self.quadtree.clear()

        #  The game loop ends here.

        pygame.quit()

    def notify_collision(self, wall, other):
        if wall == self.left_wall:
            self.score2 += 1
            self.balls.remove(other)

        if wall == self.right_wall:
            self.score1 += 1
            self.balls.remove(other)

    def resolve_collision(self, object2, object1):
        '''
        Cannot collide b
        :param object2:
        :param object1:
        :return:
        '''

        if object1 == object2:
            return

        if type(object2) is objects.Wall:
            temp = object2
            object2 = object1
            object1 = temp

        distance = object2.get_position()-object1.get_position()  # towards object 2

        if type(object1) is objects.Wall:
            unit_norm = object1.get_norm()
            unit_tang = unit_norm.perp()
            if abs(distance.dot(unit_norm)) > object2.get_radius() \
                    or abs(distance.dot(unit_tang)) > (object1.get_radius()+object2.get_radius()):
                return
        else:
            unit_norm = distance.unit()
            unit_tang = unit_norm.perp()
            if distance.mag() > (object1.get_radius() + object2.get_radius()):
                return

        m1 = object1.get_mass()
        m2 = object2.get_mass()
        v1 = object1.get_velocity()
        v2 = object2.get_velocity()

        v1norm_mag_i = v1.dot(unit_norm)
        v1tang_mag_i = v1.dot(unit_tang)
        v2norm_mag_i = v2.dot(unit_norm)
        v2tang_mag_i = v2.dot(unit_tang)

        if v1norm_mag_i - v2norm_mag_i < 0:
            return

        if m1 == m2:
            v1norm_mag_f = v2norm_mag_i
            v1tang_mag_f = v1tang_mag_i
            v2norm_mag_f = v1norm_mag_i
            v2tang_mag_f = v2tang_mag_i
        elif m1 == float("inf"):
            v1norm_mag_f = v1norm_mag_i
            v1tang_mag_f = v1tang_mag_i
            v2norm_mag_f = -1 * v2norm_mag_i
            v2tang_mag_f = v2tang_mag_i + v1tang_mag_i
        elif m2 == float("inf"):
            v1norm_mag_f = -1 * v1norm_mag_i
            v1tang_mag_f = v1tang_mag_i + v2tang_mag_i
            v2norm_mag_f = v2norm_mag_i
            v2tang_mag_f = v2tang_mag_i
        else:
            v1norm_mag_f = (v1norm_mag_i * (m1 - m2) + 2 * m2 * v2norm_mag_i) / (m1 + m2)
            v1tang_mag_f = v1tang_mag_i
            v2norm_mag_f = (v2norm_mag_i * (m2 - m1) + 2 * m1 * v1norm_mag_i) / (m1 + m2)
            v2tang_mag_f = v2tang_mag_i

        v1norm = unit_norm * v1norm_mag_f
        v1tang = unit_tang * v1tang_mag_f
        v2norm = unit_norm * v2norm_mag_f
        v2tang = unit_tang * v2tang_mag_f

        object1.collide(v1norm + v1tang, object2)
        object2.collide(v2norm + v2tang, object1)

        if not self.mute:
            self.bounce_sound.play(0, 250)


def draw_quadtree(window, quadtree):
    if quadtree.is_split():
        bounds = quadtree.get_bounds()
        pygame.draw.line(window,
                         pygame.color.Color("white"),
                         (bounds.get_h_median(), bounds.get_top()),
                         (bounds.get_h_median(), bounds.get_bottom()),
                         1)
        pygame.draw.line(window,
                         pygame.color.Color("white"),
                         (bounds.get_left(), bounds.get_v_median()),
                         (bounds.get_right(), bounds.get_v_median()),
                         1)
        for i in range(0, 4):
            draw_quadtree(window, quadtree.get_nodes()[i])

    draw_text(window, str(quadtree.get_population()), quadtree.get_bounds().get_center().to_tuple(), 24)


def draw_text(window, text_param, center, size):
    basic_font = pygame.font.SysFont(None, size)
    text = basic_font.render(text_param, True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = center[0]
    text_rect.centery = center[1]
    window.blit(text, text_rect)

# Start game
my_pong_game = PongGame(640*2, 480*2)
my_pong_game.run_game()
