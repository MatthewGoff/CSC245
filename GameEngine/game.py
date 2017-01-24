import pygame

import game_objects
import util


class Game:

    def __init__(self, window_width, window_height):

        print "Seed = "+str(util.get_seed())
        pygame.init()
        pygame.mixer.init()
        self.bounce_sound = pygame.mixer.Sound("bounce.wav")
        self.mute = True

        self.running = False

        self.window_width = window_width
        self.window_height = window_height
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        self.left_wall = game_objects.Wall(util.Vec2D(0, self.window_height / 2),
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

        self.objects = [self.walls]

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
        pass

    def apply_rules(self):
        for obj_class in self.objects:
            self.quadtree.insert_many(obj_class)

        for ball in self.balls:
            neighbors = self.quadtree.get_neighbors(ball)
            for neighbor in neighbors:
                self.resolve_collision(neighbor, ball)

    def simulate(self):
        for obj_class in self.objects:
            for obj in obj_class:
                obj.simulate()

    def takedown(self):
        self.quadtree.clear()

    def update_display(self):
        pass

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

        if (type(object2) is game_objects.Wall
            or type(object2) is game_objects.Block):
            temp = object2
            object2 = object1
            object1 = temp

        distance = object2.get_position()-object1.get_position()  # towards object 2

        if issubclass(object2.__class__, game_objects.Block):
            for wall in object2.get_walls():
                self.resolve_collision(wall, object1)
            return
        elif type(object1) is game_objects.Wall:
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
        for obj_class in self.objects:
            for obj in obj_class:
                util.draw_text(self.window,
                               obj.__str__(),
                               obj.get_position().to_tuple(),
                               24)

