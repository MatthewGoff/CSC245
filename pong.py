import pygame
import objects
import util


def run_game():

    # Initialize pygame and set up the display window.
    pygame.init()

    my_win = pygame.display.set_mode((util.WINDOW_WIDTH, util.WINDOW_HEIGHT))

    # Initialize balls
    my_balls = []

    for i in range(0, util.NUM_BALLS):
        radius = util.RandGen.randint(util.RADIUS_RANGE[0], util.RADIUS_RANGE[1])
        position = util.Vec2D(util.RandGen.uniform(0 + radius, util.WINDOW_WIDTH - radius),
                              util.RandGen.uniform(0 + radius, util.WINDOW_HEIGHT - radius))
        velocity = util.Vec2D(util.RandGen.uniform(-util.INITIAL_SPEED, util.INITIAL_SPEED),
                              util.RandGen.uniform(-util.INITIAL_SPEED, util.INITIAL_SPEED))
        color = util.random_color()

        my_balls += [objects.Ball(position, velocity, color, radius)]

    # The game loop starts here.
    keep_going = True
    while keep_going:

        # 1. Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

        # 2. Apply rules of game world
        for i in range(0,len(my_balls)):
            collide_walls(my_balls[i])
            for j in range(i+1,len(my_balls)):
                test_collision(my_balls[i], my_balls[j])

        # 3. Simulate the world
        for ball in my_balls:
            ball.simulate()

        # 4. Draw
        my_win.fill(pygame.color.Color("black"))

        for ball in my_balls:
            pos = ball.get_position()
            color = ball.get_color()

            if util.COLOR_SCHEME == "gradient" or util.COLOR_SCHEME == "speed":
                if util.COLOR_SCHEME == "speed":
                    r = int((ball.get_velocity().mag() * 50) % 255)
                    g = r
                    b = g
                else:
                    r = int(255 * pos.get_x() / util.WINDOW_WIDTH)
                    g = int(255 * pos.get_y() / util.WINDOW_HEIGHT)
                    b = int(255 * ball.get_radius() / util.RADIUS_RANGE[1])
                    #b = int((ball.get_velocity().mag() * 500) % 255)

                r = min(max(0, r), 255)  # encase it shoots over
                g = min(max(0, g), 255)
                b = min(max(0, b), 255)

                color =  pygame.color.Color(r, g, b, 1)

            pygame.draw.circle(my_win, color, (int(ball.get_position().get_x()), int(ball.get_position().get_y())), ball.get_radius())

            if util.DRAW_VELOCITY:
                vel = ball.get_velocity().scale(50)
                vec = pos.add(vel)
                pygame.draw.line(my_win, pygame.color.Color("white"), (pos.get_x(), pos.get_y()), (vec.get_x(),vec.get_y()), 3)

        # Swap display
        pygame.display.update()

    # The game loop ends here.

    pygame.quit()


def test_collision(ball1, ball2):
    # see if these two balls have collided and if so calc result

    normal = ball2.get_position().sub(ball1.get_position())  # towards ball2

    if normal.mag() < (ball1.get_radius() + ball2.get_radius()) and\
            (normal.dot(ball1.get_next_velocity()) > 0 or normal.dot(ball2.get_next_velocity()) < 0):

        m1 = ball1.get_mass()
        m2 = ball2.get_mass()
        v1 = ball1.get_next_velocity()
        v2 = ball2.get_next_velocity()

        unit_norm = normal.unit()
        unit_tang = unit_norm.perp()

        v1norm_mag = v1.dot(unit_norm)
        v1tang_mag = v1.dot(unit_tang)
        v2norm_mag = v2.dot(unit_norm)
        v2tang_mag = v2.dot(unit_tang)

        v1norm_mag_f = (v1norm_mag * (m1 - m2) + 2 * m2 * v2norm_mag) / (m1 + m2)
        v1tang_mag_f = v1tang_mag
        v2norm_mag_f = (v2norm_mag * (m2 - m1) + 2 * m1 * v1norm_mag) / (m1 + m2)
        v2tang_mag_f = v2tang_mag

        v1norm = unit_norm.scale(v1norm_mag_f)
        v1tang = unit_tang.scale(v1tang_mag_f)
        v2norm = unit_norm.scale(v2norm_mag_f)
        v2tang = unit_tang.scale(v2tang_mag_f)

        ball1.collide(v1norm.add(v1tang))
        ball2.collide(v2norm.add(v2tang))


def collide_walls(ball1):
    # see if the ball has collided with any walls and if so calc result
    if ball1.get_position().get_x() <= 0 + ball1.get_radius():
        collision_vec = util.Vec2D(-1, 0)
        if collision_vec.dot(ball1.get_next_velocity()) > 0:
            ball1.collide(ball1.get_next_velocity().add(util.Vec2D(-2 * ball1.get_next_velocity().get_x(), 0)))
    elif ball1.get_position().get_x() >= util.WINDOW_WIDTH - ball1.get_radius():
        collision_vec = util.Vec2D(1, 0)
        if collision_vec.dot(ball1.get_next_velocity()) > 0:
            ball1.collide(ball1.get_next_velocity().add(util.Vec2D(-2 * ball1.get_next_velocity().get_x(), 0)))
    if ball1.get_position().get_y() <= 0 + ball1.get_radius():
        collision_vec = util.Vec2D(0, -1)
        if collision_vec.dot(ball1.get_next_velocity()) > 0:
            ball1.collide(ball1.get_next_velocity().add(util.Vec2D(0, -2 * ball1.get_next_velocity().get_y())))
    elif ball1.get_position().get_y() >= util.WINDOW_HEIGHT - ball1.get_radius():
        collision_vec = util.Vec2D(0, 1)
        if collision_vec.dot(ball1.get_next_velocity()) > 0:
            ball1.collide(ball1.get_next_velocity().add(util.Vec2D(0, -2 * ball1.get_next_velocity().get_y())))


# Start game
run_game()
