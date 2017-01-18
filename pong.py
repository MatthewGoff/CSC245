import pygame
import objects
import util


class PongGame:

    def __init__(self):

        print "Seed = "+str(util.get_seed())
        pygame.init()
        self.window = pygame.display.set_mode((util.WINDOW_WIDTH, util.WINDOW_HEIGHT))

        self.paddle1 = objects.Paddle(util.Vec2D(50, int(util.WINDOW_HEIGHT/2)),
                                      util.Vec2D(0, 0),
                                      util.PADDLE_HEIGHT,
                                      util.PADDLE_WIDTH,
                                      pygame.Color("white"),
                                      "paddle1")
        self.paddle2 = objects.Paddle(util.Vec2D(util.WINDOW_WIDTH-50, int(util.WINDOW_HEIGHT / 2)),
                                      util.Vec2D(0, 0),
                                      util.PADDLE_HEIGHT,
                                      util.PADDLE_WIDTH,
                                      pygame.Color("white"),
                                      "paddle2")
        self.left_wall = objects.Wall(util.Vec2D(0, util.WINDOW_HEIGHT/2),
                                      util.Vec2D(0, 0),
                                      util.Vec2D(1, 0),
                                      util.WINDOW_HEIGHT,
                                      0,
                                      "left wall",
                                      self.collision)
        self.top_wall = objects.Wall(util.Vec2D(util.WINDOW_WIDTH/2, 0),
                                     util.Vec2D(0, 0),
                                     util.Vec2D(0, 1),
                                     util.WINDOW_WIDTH,
                                     0,
                                     "top wall",
                                     self.collision)
        self.bottom_wall = objects.Wall(util.Vec2D(util.WINDOW_WIDTH/2, util.WINDOW_HEIGHT),
                                        util.Vec2D(0, 0),
                                        util.Vec2D(0, -1),
                                        util.WINDOW_WIDTH,
                                        0,
                                        "bottom wall",
                                        self.collision)
        self.right_wall = objects.Wall(util.Vec2D(util.WINDOW_WIDTH, util.WINDOW_HEIGHT / 2),
                                       util.Vec2D(0, 0),
                                       util.Vec2D(-1, 0),
                                       util.WINDOW_HEIGHT,
                                       0,
                                       "right wall",
                                       self.collision)

        self.walls = self.paddle1.get_walls() + self.paddle2.get_walls() + [self.top_wall,
                                                                            self.bottom_wall,
                                                                            self.right_wall,
                                                                            self.left_wall]

        self.balls = []
        for i in range(0, util.NUM_BALLS):
            radius = util.RandGen.randint(util.RADIUS_RANGE[0], util.RADIUS_RANGE[1])
            position = util.Vec2D(util.RandGen.uniform(0 + radius, util.WINDOW_WIDTH - radius),
                                  util.RandGen.uniform(0 + radius, util.WINDOW_HEIGHT - radius))
            velocity = util.random_velocity()
            color = util.random_color()
            identifier = i

            self.balls += [objects.Ball(position, velocity, color, radius, identifier)]

        self.quadtree = util.Quadtree(util.Rectangle(0, util.WINDOW_HEIGHT, 0, util.WINDOW_WIDTH))

        self.score1 = 0
        self.score2 = 0

    def run_game(self):
        # The game loop starts here.
        keep_going = True
        while keep_going:

            advance = util.CONTINUOUS

            # 1. Handle events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    keep_going = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    advance = True

            if advance:

                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP]:
                    self.paddle2.set_velocity(util.Vec2D(0, -1*util.PADDLE_SPEED))
                elif keys[pygame.K_DOWN]:
                    self.paddle2.set_velocity(util.Vec2D(0, util.PADDLE_SPEED))
                else:
                    self.paddle2.set_velocity(util.Vec2D(0, 0))

                if keys[pygame.K_w]:
                    self.paddle1.set_velocity(util.Vec2D(0, -1*util.PADDLE_SPEED))
                elif keys[pygame.K_s]:
                    self.paddle1.set_velocity(util.Vec2D(0, util.PADDLE_SPEED))
                else:
                    self.paddle1.set_velocity(util.Vec2D(0, 0))

                # 2. Apply rules of game world
                self.quadtree.insert_many(self.balls)
                self.quadtree.insert_many(self.walls)

                for ball in self.balls:
                    neighbors = self.quadtree.get_neighbors(ball)
                    for neighbor in neighbors:
                        test_collision(ball, neighbor)

                # 3. Simulate the world
                for ball in self.balls:
                    ball.simulate()
                self.paddle1.simulate()
                self.paddle2.simulate()

                # 4. Draw
                self.window.fill(util.WINDOW_COLOR)

                draw_text(self.window, str(self.score1), (100, 100), 100)
                draw_text(self.window, str(self.score2), (util.WINDOW_WIDTH-100, 100), 100)

                draw_paddle(self.window, self.paddle1)
                draw_paddle(self.window, self.paddle2)

                for ball in self.balls:
                    draw_ball(self.window, ball)

                if util.DRAW_QUADTREE:
                    draw_quadtree(self.window, self.quadtree)

                if util.LABEL_OBJECTS:
                    for ball in self.balls:
                        draw_text(self.window, ball.__str__(), ball.get_position().to_tuple(), 24)

                        draw_text(self.window, self.paddle1.__str__(), self.paddle1.get_position().to_tuple(), 24)
                        draw_text(self.window, self.paddle2.__str__(), self.paddle2.get_position().to_tuple(), 24)

                    for wall in self.walls:
                        draw_text(self.window, wall.__str__(), wall.get_position().to_tuple(), 24)

                # 5. Takedown
                self.quadtree.clear()

                # Swap display
                pygame.display.update()


        #  The game loop ends here.

        pygame.quit()

    def collision(self, wall, other):
        if wall == self.left_wall:
            self.score2 += 1
            self.balls.remove(other)

        if wall == self.right_wall:
            self.score1 += 1
            self.balls.remove(other)


def test_collision(object2, object1):
    '''
    Any wall object must be second parameter: "object1"

    :param object2:
    :param object1:
    :return:
    '''

    if object1 == object2:
        return

    distance = object2.get_position()-object1.get_position()  # towards object 2

    if type(object1) is objects.Wall:
        unit_norm = object1.get_norm()
        unit_tang = object1.get_tang()
    else:
        unit_norm = distance.unit()
        unit_tang = unit_norm.perp()

    if type(object1) is objects.Wall:
        if abs(distance.dot(unit_norm)) > object2.get_radius() \
                or abs(distance.dot(unit_tang)) > (object1.get_width()/2+object2.get_radius()):
            return
    elif distance.mag() > (object1.get_radius() + object2.get_radius()):
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

    if m1 == float("inf"):
        v1norm_mag_f = v1norm_mag_i
        v1tang_mag_f = v1tang_mag_i
        v2norm_mag_f = -1*v2norm_mag_i
        v2tang_mag_f = v2tang_mag_i+v1tang_mag_i
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


def draw_paddle(window, paddle):
    pygame.draw.rect(window,
                     paddle.get_color(),
                     pygame.Rect(paddle.get_left(),
                                 paddle.get_top(),
                                 paddle.get_width(),
                                 paddle.get_height()),
                     0)


def draw_ball(window, ball):
    pos = ball.get_position()
    color = ball.get_color()

    if util.COLOR_SCHEME == "gradient" or util.COLOR_SCHEME == "speed":
        r = int(255 * pos.to_tuple()[0] / util.WINDOW_WIDTH)
        g = int(255 * pos.to_tuple()[1] / util.WINDOW_HEIGHT)
        b = int(255 * ball.get_radius() / util.RADIUS_RANGE[1])

        r = min(max(0, r), 255)  # encase it shoots over
        g = min(max(0, g), 255)
        b = min(max(0, b), 255)

        color = pygame.Color(r, g, b)

        if util.COLOR_SCHEME == "speed":
            s = pygame.Surface((ball.get_radius() * 2, ball.get_radius() * 2))
            s.fill((0, 0, 0))
            s.set_colorkey((0, 0, 0))
            pygame.draw.circle(s, color, (ball.get_radius(), ball.get_radius()), ball.get_radius())
            s.set_alpha(int((ball.get_velocity().mag() * 500) % 255))

            window.blit(s, (int(pos.to_tuple()[0] - ball.get_radius()),int(pos.to_tuple()[1] - ball.get_radius())))

    if util.COLOR_SCHEME != "speed":
        pygame.draw.circle(window,
                           color,
                           (int(pos.to_tuple()[0]), int(pos.to_tuple()[1])),
                           ball.get_radius())

    if util.DRAW_VELOCITY:
        vec = pos+ball.get_velocity()*50
        pygame.draw.line(window, pygame.Color("white"), pos.to_tuple(), vec.to_tuple(), 1)


def draw_text(window, text_param, center, size):
    basic_font = pygame.font.SysFont(None, size)
    text = basic_font.render(text_param, True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = center[0]
    text_rect.centery = center[1]
    window.blit(text, text_rect)

# Start game
my_pong_game = PongGame()
my_pong_game.run_game()
