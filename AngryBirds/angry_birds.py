# An Angry Birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from GameEngine import util, game_objects
from bird import Bird
from slingshot import Slingshot


class AngryBirds:
    WINDOW_COLOR = pygame.Color("lightblue")

    def __init__(self, window_width, window_height):
        print "Seed = " + str(util.get_seed())
        pygame.init()
        pygame.mixer.init()
        self.bounce_sound = pygame.mixer.Sound("bounce.wav")
        self.mute = True

        self.running = False
        self.firing = False

        self.window_width = window_width
        self.window_height = window_height
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        self.left_wall = game_objects.Wall(
            util.Vec2D(0, self.window_height / 2),
            util.Vec2D(0, 0),
            util.Vec2D(1, 0),
            self.window_height,
            float("inf"),
            pygame.Color("white"),
            "left wall",
            self.notify_collision)
        self.top_wall = game_objects.Wall(util.Vec2D(self.window_width / 2, 0),
                                          util.Vec2D(0, 0),
                                          util.Vec2D(0, 1),
                                          self.window_width,
                                          float("inf"),
                                          pygame.Color("white"),
                                          "top wall",
                                          self.notify_collision)
        self.bottom_wall = game_objects.Wall(util.Vec2D(self.window_width / 2,
                                                        self.window_height),
                                             util.Vec2D(0, 0),
                                             util.Vec2D(0, -1),
                                             self.window_width,
                                             float("inf"),
                                             pygame.Color("white"),
                                             "bottom wall",
                                             self.notify_collision)
        self.right_wall = game_objects.Wall(util.Vec2D(self.window_width,
                                                       self.window_height / 2),
                                            util.Vec2D(0, 0),
                                            util.Vec2D(-1, 0),
                                            self.window_height,
                                            float("inf"),
                                            pygame.Color("white"),
                                            "right wall",
                                            self.notify_collision)

        self.walls = [self.top_wall,
                      self.bottom_wall,
                      self.right_wall,
                      self.left_wall]

        self.birds = pygame.sprite.Group()
        self.bird = Bird(util.Vec2D(50, 50), util.Vec2D(0, 0), 50, 0, "bird")
        self.birds.add(self.bird)

        self.slingshots = pygame.sprite.Group()
        self.slingshot = Slingshot(util.Vec2D(200, 200), 50, "slingshot")
        self.slingshots.add(self.slingshot)

        self.quadtree = util.Quadtree(util.Rectangle(0,
                                                     self.window_height,
                                                     0,
                                                     self.window_width))

    def run_game(self):
        self.running = True
        while self.running:
            self.tick()
        pygame.quit()

    def tick(self):
        self.handle_events()
        self.apply_rules()
        self.simulate()
        self.update_display()
        self.takedown()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.mute = not self.mute
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.firing = True
            else:
                self.firing = False

        keys = pygame.key.get_pressed()

    def apply_rules(self):
        if self.firing:
            print "firing"
            bird = Bird(self.slingshot.position,
                        util.Vec2D(1, 1),
                        50,
                        0,
                        "new")
            self.birds.add(bird)

    def simulate(self):
        for bird in self.birds:
            bird.simulate()

    def takedown(self):
        self.quadtree.clear()

    def update_display(self):
        self.window.fill(AngryBirds.WINDOW_COLOR)

        self.slingshots.draw(self.window)
        self.birds.draw(self.window)

        pygame.display.update()

    def notify_collision(self, wall, other):
        pass

    def resolve_collision(self, object2, object1):
        '''
        Cannot collide two walls
        :param object2:
        :param object1:
        :return:
        '''

        if object1 == object2:
            return

        if issubclass(object2.__class__, game_objects.Block):
            for wall in object2.get_walls():
                self.resolve_collision(wall, object1)
            return

        if type(object2) is game_objects.Wall:
            temp = object2
            object2 = object1
            object1 = temp

        distance = object2.get_position()-object1.get_position()  # towards object 2

        if type(object1) is game_objects.Wall:
            unit_norm = object1.get_norm()
            unit_tang = unit_norm.perp()
            if (abs(distance.dot(unit_norm)) <= object2.get_radius()
                and abs(distance.dot(unit_tang)) <= (object1.get_radius() + object2.get_radius())):
                if distance.dot(unit_tang) > object1.get_radius():
                    corner = object1.get_position() + unit_tang * object1.get_radius()
                    normal = object2.get_position()-corner
                    if normal.mag() <= object2.get_radius():
                        unit_norm = normal.unit()
                        unit_tang = unit_norm.perp()
                    else:
                        return
                elif distance.dot(unit_tang) < object1.get_radius() * (-1):
                    corner = object1.get_position() - unit_tang * object1.get_radius()
                    normal = object2.get_position() - corner
                    if normal.mag() <= object2.get_radius():
                        unit_norm = normal.unit()
                        unit_tang = unit_norm.perp()
                    else:
                        return
                else:
                    unit_norm = object1.get_norm()
                    unit_tang = unit_norm.perp()
            else:
                #No collision
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

        v1norm_i = v1.dot(unit_norm)
        v1tang_i = v1.dot(unit_tang)
        v2norm_i = v2.dot(unit_norm)
        v2tang_i = v2.dot(unit_tang)

        if v1norm_i - v2norm_i < 0:
            return

        if m1 == m2:
            v1norm_f = v2norm_i
            v1tang_f = v1tang_i
            v2norm_f = v1norm_i
            v2tang_f = v2tang_i
        elif m1 == float("inf"):
            v1norm_f = v1norm_i
            v1tang_f = v1tang_i
            v2norm_f = v1norm_i-v2norm_i
            v2tang_f = v2tang_i + v1tang_i
        elif m2 == float("inf"):
            v1norm_f = v2norm_i-v1norm_i
            v1tang_f = v1tang_i + v2tang_i
            v2norm_f = v2norm_i
            v2tang_f = v2tang_i
        else:
            v1norm_f = (v1norm_i * (m1 - m2) + 2 * m2 * v2norm_i) / (m1 + m2)
            v1tang_f = v1tang_i
            v2norm_f = (v2norm_i * (m2 - m1) + 2 * m1 * v1norm_i) / (m1 + m2)
            v2tang_f = v2tang_i

        v1norm = unit_norm * v1norm_f
        v1tang = unit_tang * v1tang_f
        v2norm = unit_norm * v2norm_f
        v2tang = unit_tang * v2tang_f

        object1.collide(v1norm + v1tang, object2)
        object2.collide(v2norm + v2tang, object1)

        if not self.mute:
            self.bounce_sound.play(0, 250)

    def label_objects(self):
        for bird in self.birds:
            util.draw_text(self.window,
                           bird.__str__(),
                           bird.get_position().to_tuple(),
                           24)

angry_birds = AngryBirds(640*2, 480*2)
angry_birds.run_game()
