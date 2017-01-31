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
from sheep import Sheep
from levels import Levels


class AngryBirds:
    WINDOW_COLOR = pygame.Color("lightblue")
    LAUNCH_SPEED = .05  # active

    def __init__(self, window_width, window_height):
        print "Seed = " + str(util.get_seed())
        pygame.init()
        pygame.mixer.init()

        self.wood = pygame.mixer.Sound("audio/wood.wav")
        self.stone = pygame.mixer.Sound("audio/stone.wav")
        self.ice = pygame.mixer.Sound("audio/ice.wav")
        self.bleep = pygame.mixer.Sound("audio/bleep.wav")
        self.moss = pygame.mixer.Sound("audio/moss.wav")

        self.mute = False

        self.score = 0;
        self.currentLevel = 0;

        self.shootingBird = []

        self.birdType = 1

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
            self.score += 100;
            if (issubclass(arbiter.shapes[0].body.__class__, Crate)) or (issubclass(arbiter.shapes[1].body.__class__, Crate)):
                self.wood.play(0,400)
            elif(issubclass(arbiter.shapes[0].body.__class__, Ice)) or (issubclass(arbiter.shapes[1].body.__class__, Ice)):
                self.ice.play(0,400)
            elif (issubclass(arbiter.shapes[0].body.__class__, Stone)) or (issubclass(arbiter.shapes[1].body.__class__, Stone)):
                self.stone.play(0, 400)
            elif (issubclass(arbiter.shapes[0].body.__class__, Moss)) or (issubclass(arbiter.shapes[1].body.__class__, Moss)):
                self.moss.play(0, 400)

            if (issubclass(arbiter.shapes[0].body.__class__, Bird)
                and issubclass(arbiter.shapes[1].body.__class__, Block)
                and not issubclass(arbiter.shapes[1].body.__class__, Moss)):
                bird = arbiter.shapes[0]
                block = arbiter.shapes[1]
            elif (issubclass(arbiter.shapes[0].body.__class__, Block)
                and issubclass(arbiter.shapes[1].body.__class__, Bird)
                and not issubclass(arbiter.shapes[0].body.__class__, Moss)):
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
        self.enemies = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        self.slingshots = pygame.sprite.Group()

        self.slingshot = Slingshot(util.Vec2D(300, self.window_height - 300),
                                   50, "slingshot")
        self.slingshots.add(self.slingshot)

        self.levels = Levels(window_width, window_height)

    def clear_space(self):
        for bird in self.birds:
            self.space.remove(bird.poly)
        for enemy in self.enemies:
            self.space.remove(enemy.poly)
        for block in self.blocks:
            self.space.remove(block.poly)

    def init_level(self, i):
        level = self.levels.get_level(i-1)

        self.clear_space()
        self.birds = pygame.sprite.Group()
        self.enemies = level.get_enemies()
        self.blocks = level.get_blocks()

        for enemy in self.enemies:
            print str(enemy.identifier)
            self.space.add(enemy, enemy.poly)

        for block in self.blocks:
            print str(block.identifier)
            self.space.add(block, block.poly)

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
                elif event.key == pygame.K_1:
                    self.instructions = False
                    self.init_level(1)
                elif event.key == pygame.K_2:
                    self.instructions = False
                    self.init_level(2)
                elif event.key == pygame.K_3:
                    self.instructions = False
                    self.init_level(3)

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

        if len(self.enemies) == 0:
            self.instructions = False
            self.currentLevel += 1
            self.init_level(self.currentLevel)

        if self.pulling:
            bird = stoneBird(self.slingshot.position.to_tuple(),
                             self.launch_velocity.to_tuple(),
                             "new")
            self.score -= 5
            if self.birdType == 1:
                bird = stoneBird(self.slingshot.position.to_tuple(),
                                 self.launch_velocity.to_tuple(),
                                 "new")
                self.birdType = 2
            elif self.birdType == 2:
                bird = iceBird(self.slingshot.position.to_tuple(),
                                 self.launch_velocity.to_tuple(),
                                 "new")
                self.birdType = 3
            elif self.birdType == 3:
                bird = crateBird(self.slingshot.position.to_tuple(),
                                 self.launch_velocity.to_tuple(),
                                 "new")
                self.birdType = 4
            elif self.birdType == 4:
                bird = BasicBird(self.slingshot.position.to_tuple(),
                                 self.launch_velocity.to_tuple(),
                                 "new")
                self.birdType = 1

            self.birds.add(bird)
            self.shootingBird.append(bird)
            self.pulling = False

        if len(self.shootingBird) != 0:
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
                           "Press '1-3' to start a level",
                           (self.window_width/2, 400),
                           50,
                           text_color)
        else:
            self.window.fill(AngryBirds.WINDOW_COLOR)
            util.draw_text(self.window,
                           "Score: " + str(self.score),
                           (250, 50),
                           50,
                           pygame.Color("Black"))
            self.slingshots.draw(self.window)
            self.birds.update(self.window)
            self.enemies.draw(self.window)
            self.blocks.draw(self.window)

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

angry_birds = AngryBirds(640*2, 480*2)
angry_birds.run_game()
