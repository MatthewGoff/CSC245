# An Angry Birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
import pymunk
from GameEngine import util, game_objects
from BasicBird import BasicBird
from iceBird import iceBird
from crateBird import crateBird
from stoneBird import stoneBird
from slingshot import Slingshot
from crate import Crate
from ice import Ice
from stone import Stone
from moss import Moss


class AngryBirds:
    WINDOW_COLOR = pygame.Color("lightblue")
    LAUNCH_SPEED = .05  # active

    def __init__(self, window_width, window_height):
        print "Seed = " + str(util.get_seed())
        pygame.init()
        pygame.mixer.init()
        self.bounce_sound = pygame.mixer.Sound("bounce.wav")
        self.mute = True

        self.running = False
        self.instructions = True
        self.firing = False
        self.mouse_origin = util.Vec2D(0, 0)
        self.launch_velocity = util.Vec2D(0, 0)

        self.window_width = window_width
        self.window_height = window_height
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        self.space = pymunk.Space()
        self.space.gravity = 0, 1
        self.space.damping = 1

        self.birds = pygame.sprite.Group()
        self.slingshots = pygame.sprite.Group()
        self.crates = pygame.sprite.Group()

        self.slingshot = Slingshot(util.Vec2D(200, self.window_height - 100),
                                   50, "slingshot")
        self.slingshots.add(self.slingshot)

        self.floor = pymunk.Body(mass=100, moment=100, body_type=pymunk.Body.STATIC)
        self.floorpoly = pymunk.Segment(self.floor, (0, window_height),
                                        (window_width, window_height), 5)
        self.space.add(self.floor, self.floorpoly)

        self.init_objects()

    def init_objects(self):
        self.birds = pygame.sprite.Group()
        self.crates = pygame.sprite.Group()

        crate = Crate(util.Vec2D(500, 500),
                      util.Vec2D(0, 0),
                      100,
                      100,
                      self.notify_collision,
                      "crate")
        self.space.add(crate, crate.poly)
        self.crates.add(crate)

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

    def handle_events(self):
        #bird = BasicBird(self.slingshot.position,
         #                0,
          #               self.physics_environment,
           #              "new")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.mute = not self.mute
                elif event.key == pygame.K_SPACE:
                    self.firing = True
                elif event.key == pygame.K_r:
                    self.instructions = False
                    self.init_objects()
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #print "Button pressed:", event.dict['button'], "@", event.dict['pos']
                button_pressed = event.dict['button']
                target = event.dict['pos']
                if button_pressed == 1: # Left click targets
                    self.mouse_origin = util.Vec2D(target[0], target[1])
                #    self.birds.add(bird)
                elif button_pressed == 3: # Right click fires
                    pass

            elif event.type == pygame.MOUSEBUTTONUP:

                #print "Button released:", event.dict['button'], "@", event.dict['pos']
                button_pressed = event.dict['button']
                target = event.dict['pos']

                if button_pressed == 1: # Left click targets
                    self.firing = True
                    mouse_end = util.Vec2D(target[0], target[1])
                    self.launch_velocity = self.mouse_origin - mouse_end
                    self.launch_velocity *= AngryBirds.LAUNCH_SPEED
                    #bird.velocity = self.launch_velocity
                    #print self.launch_velocity



                elif button_pressed == 3: # Right click fires
                    pass

        keys = pygame.key.get_pressed()

    def apply_rules(self):
        if self.firing:
            bird = BasicBird(self.slingshot.position,
                             self.launch_velocity,
                             "new")
            self.space.add(bird, bird.poly)
            self.birds.add(bird)
            self.firing = False

    def simulate(self):
        self.space.step(0.02)
        for body in self.space.bodies:
            if issubclass(body.__class__, pygame.sprite.Sprite):
                body.update_rect()

    def update_display(self):

        if self.instructions:
            self.window.fill(pygame.Color("green"))
            text_color = pygame.Color("black")
            util.draw_text(self.window,
                           "Angry Birds",
                           (self.window_width/2, 100),
                           100,
                           text_color)
            util.draw_text(self.window,
                           "By: Matt & Nik",
                           (self.window_width/2, 200),
                           50,
                           text_color)
            util.draw_text(self.window,
                           "Drag to shoot",
                           (self.window_width/2, 300),
                           50,
                           text_color)
            util.draw_text(self.window,
                           "Press 'R' to start/restart",
                           (self.window_width/2, 400),
                           50,
                           text_color)
        else:
            self.window.fill(AngryBirds.WINDOW_COLOR)

            self.slingshots.draw(self.window)
            self.birds.update(self.window)
            self.crates.draw(self.window)

        pygame.display.update()

    def notify_collision(self, block, bird):
        bird.kill()
        self.crates.remove(block)

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


class PhysicsEnvironment:

    def __init__(self, gravity, drag):
        self.gravity = gravity
        self.drag = drag

angry_birds = AngryBirds(640*2, 480*2)
angry_birds.run_game()
