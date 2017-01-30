# An Angry Birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
import pymunk
from GameEngine import util, game_objects
from block import Block
from bird import Bird
from BasicBird import BasicBird
from iceBird import iceBird
from crateBird import crateBird
from stoneBird import stoneBird
from slingshot import Slingshot
from crate import Crate
from ice import Ice
from stone import Stone
from moss import Moss
from Levels import Level


class AngryBirds:
    WINDOW_COLOR = pygame.Color("lightblue")
    LAUNCH_SPEED = .05  # active

    def __init__(self, window_width, window_height):
        print "Seed = " + str(util.get_seed())
        pygame.init()
        pygame.mixer.init()
        self.bounce_sound = pygame.mixer.Sound("audio/wood.wav")
        self.mute = True

        self.shootingBird = []

        self.running = False
        self.instructions = True
        self.firing = False
        self.pulling = False
        self.mouse_origin = util.Vec2D(0, 0)
        self.launch_velocity = util.Vec2D(0, 0)

        self.window_width = window_width
        self.window_height = window_height
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        self.space = pymunk.Space()
        self.space.gravity = 0, 1
        self.space.damping = 1

        def collision(arbiter, space, data):
            if (issubclass(arbiter.shapes[0].body.__class__, Bird)
                and issubclass(arbiter.shapes[1].body.__class__, Block)):
                bird = arbiter.shapes[0]
                block = arbiter.shapes[1]
            elif (issubclass(arbiter.shapes[0].body.__class__, Block)
                and issubclass(arbiter.shapes[1].body.__class__, Bird)):
                bird = arbiter.shapes[1]
                block = arbiter.shapes[0]
            else:
                return True

            space.remove(bird, bird.body)
            space.remove(block, block.body)
            bird.body.kill()
            block.body.kill()
            return False

        h = self.space.add_default_collision_handler()
        h.begin = collision

        self.birds = pygame.sprite.Group()
        self.slingshots = pygame.sprite.Group()
        #self.crates = pygame.sprite.Group()
        self.blocks = []

        self.slingshot = Slingshot(util.Vec2D(300, self.window_height - 300),
                                   50, "slingshot")
        self.slingshots.add(self.slingshot)

        self.floor = pymunk.Body(mass=100, moment=100, body_type=pymunk.Body.STATIC)
        self.floorpoly = pymunk.Segment(self.floor, (0, window_height),
                                        (window_width, window_height), 5)
        self.space.add(self.floor, self.floorpoly)

        self.init_objects()

    def init_objects(self):

        self.birds = pygame.sprite.Group()
        '''
        self.crates = pygame.sprite.Group()

        crate = Crate(util.Vec2D(500, 500),
                      util.Vec2D(0, 0),
                      100,
                      100,
                      "crate")
        self.space.add(crate, crate.poly)

        self.crates.add(crate)
        '''
        currentBlocks = Level()
        self.blocks = currentBlocks.setup(0)

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
                    self.pulling = True
                    self.mouse_origin = util.Vec2D(target[0], target[1])
                    mouse_end = util.Vec2D(target[0], target[1])
                    self.launch_velocity = self.mouse_origin - mouse_end
                    self.launch_velocity *= AngryBirds.LAUNCH_SPEED

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

            elif event.type == pygame.MOUSEMOTION:
                target = event.dict['pos']
                mouse_end = util.Vec2D(target[0], target[1])
                self.launch_velocity = self.mouse_origin - mouse_end
                self.launch_velocity *= AngryBirds.LAUNCH_SPEED

        keys = pygame.key.get_pressed()

    def apply_rules(self):

        if self.pulling:
            bird = BasicBird(self.slingshot.position,
                             self.launch_velocity,
                             "new")
            self.birds.add(bird)
            self.shootingBird.append(bird)
            self.pulling = False

        if len(self.shootingBird) != 0:
            print self.launch_velocity
            self.shootingBird[0].pullSpot(self.slingshot.position - self.launch_velocity)

        if self.firing and len(self.shootingBird) != 0:
            self.shootingBird[0].setVel(self.launch_velocity)
            self.space.add(self.shootingBird[0], self.shootingBird[0].poly)
            self.shootingBird = []
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
            for group in self.blocks:
                group.draw()

        pygame.display.update()

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

angry_birds = AngryBirds(1920, 1080)
angry_birds.run_game()
