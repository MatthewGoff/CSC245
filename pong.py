import pygame
import objects
import util


def run_game():

    # Initialize pygame and set up the display window.
    pygame.init()

    window = pygame.display.set_mode((util.WINDOW_WIDTH, util.WINDOW_HEIGHT))

    # Initialize balls
    my_balls = []
    for i in range(0, util.NUM_BALLS):
        radius = util.RandGen.randint(util.RADIUS_RANGE[0], util.RADIUS_RANGE[1])
        position = util.Vec2D(util.RandGen.uniform(0 + radius, util.WINDOW_WIDTH - radius),
                              util.RandGen.uniform(0 + radius, util.WINDOW_HEIGHT - radius))
        velocity = util.Vec2D(util.RandGen.uniform(-util.INITIAL_SPEED, util.INITIAL_SPEED),
                              util.RandGen.uniform(-util.INITIAL_SPEED, util.INITIAL_SPEED))
        color = util.random_color()
        name = i

        my_balls += [objects.Ball(position, velocity, color, radius, name)]

    quadtree = util.Quadtree(util.Rectangle(0, util.WINDOW_HEIGHT, 0, util.WINDOW_WIDTH))

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

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            print "up"

        if keys[pygame.K_DOWN]:
            print "down"

        if advance:

            # 2. Apply rules of game world
            for ball in my_balls:
                quadtree.insert(ball)

            for ball in my_balls:
                collide_walls(ball)
                neighbors = quadtree.get_neighbors(ball)
                for neighbor in neighbors:
                    test_collision(ball, neighbor)

            # 3. Simulate the world
            for ball in my_balls:
                ball.simulate()

            # 4. Draw
            window.fill(util.WINDOW_COLOR)

            for ball in my_balls:
                draw_ball(window, ball)

            if util.DRAW_QUADTREE:
                draw_quadtree(window, quadtree)

            if util.LABEL_OBJECTS:
                for ball in my_balls:
                    draw_text(window, ball.__str__(), ball.get_position())

            # 5. Takedown
            quadtree.clear()

            # Swap display
            pygame.display.update()


    #  The game loop ends here.

    pygame.quit()


def test_collision(ball_1, ball_2):
    # see if these two balls have collided and if so calc result

    if ball_1 == ball_2:
        return

    normal = ball_2.get_position().sub(ball_1.get_position())  # towards ball_2

    if normal.mag() > (ball_1.get_radius() + ball_2.get_radius()):
        return

    m1 = ball_1.get_mass()
    m2 = ball_2.get_mass()
    v1 = ball_1.get_velocity()
    v2 = ball_2.get_velocity()

    unit_norm = normal.unit()
    unit_tang = unit_norm.perp()

    v1norm_mag = v1.dot(unit_norm)
    v1tang_mag = v1.dot(unit_tang)
    v2norm_mag = v2.dot(unit_norm)
    v2tang_mag = v2.dot(unit_tang)

    if v1norm_mag - v2norm_mag < 0:
        return

    v1norm_mag_f = (v1norm_mag * (m1 - m2) + 2 * m2 * v2norm_mag) / (m1 + m2)
    v1tang_mag_f = v1tang_mag
    v2norm_mag_f = (v2norm_mag * (m2 - m1) + 2 * m1 * v1norm_mag) / (m1 + m2)
    v2tang_mag_f = v2tang_mag

    v1norm = unit_norm.scale(v1norm_mag_f)
    v1tang = unit_tang.scale(v1tang_mag_f)
    v2norm = unit_norm.scale(v2norm_mag_f)
    v2tang = unit_tang.scale(v2tang_mag_f)

    ball_1.collide(v1norm.add(v1tang))
    ball_2.collide(v2norm.add(v2tang))


def collide_walls(ball1):
    # see if the ball has collided with any walls and if so calc result
    if ball1.get_position().get_x() <= 0 + ball1.get_radius():
        collision_vec = util.Vec2D(-1, 0)
        if collision_vec.dot(ball1.get_velocity()) > 0:
            ball1.collide(ball1.get_velocity().add(util.Vec2D(-2 * ball1.get_velocity().get_x(), 0)))
    elif ball1.get_position().get_x() >= util.WINDOW_WIDTH - ball1.get_radius():
        collision_vec = util.Vec2D(1, 0)
        if collision_vec.dot(ball1.get_velocity()) > 0:
            ball1.collide(ball1.get_velocity().add(util.Vec2D(-2 * ball1.get_velocity().get_x(), 0)))
    if ball1.get_position().get_y() <= 0 + ball1.get_radius():
        collision_vec = util.Vec2D(0, -1)
        if collision_vec.dot(ball1.get_velocity()) > 0:
            ball1.collide(ball1.get_velocity().add(util.Vec2D(0, -2 * ball1.get_velocity().get_y())))
    elif ball1.get_position().get_y() >= util.WINDOW_HEIGHT - ball1.get_radius():
        collision_vec = util.Vec2D(0, 1)
        if collision_vec.dot(ball1.get_velocity()) > 0:
            ball1.collide(ball1.get_velocity().add(util.Vec2D(0, -2 * ball1.get_velocity().get_y())))


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
        for i in range(0,4):
            draw_quadtree(window, quadtree.get_nodes()[i])

    draw_text(window, str(quadtree.get_population()), quadtree.get_bounds().get_center())


def draw_ball(window, ball):
    pos = ball.get_position()
    color = ball.get_color()

    if util.COLOR_SCHEME == "gradient" or util.COLOR_SCHEME == "speed":
        r = int(255 * pos.get_x() / util.WINDOW_WIDTH)
        g = int(255 * pos.get_y() / util.WINDOW_HEIGHT)
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

            window.blit(s, (int(pos.get_x() - ball.get_radius()),int(pos.get_y() - ball.get_radius())))

    if util.COLOR_SCHEME != "speed":
        pygame.draw.circle(window,
                           color,
                           (int(pos.get_x()), int(pos.get_y())),
                           ball.get_radius())

    if util.DRAW_VELOCITY:
        vel = ball.get_velocity().scale(50)
        vec = pos.add(vel)
        pygame.draw.line(window, pygame.Color("white"), (pos.get_x(), pos.get_y()), (vec.get_x(), vec.get_y()), 1)


def draw_text(window, text_param, center):
    basic_font = pygame.font.SysFont(None, 24)
    text = basic_font.render(text_param, True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = center.get_x()
    text_rect.centery = center.get_y()
    window.blit(text, text_rect)

# Start game
run_game()
