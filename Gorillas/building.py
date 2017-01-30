# A simple building class
# Author: Matthew Anderson
# Winter 2017

import pygame
from bumper import Bumper


class Building(pygame.sprite.Sprite):

    def __init__(self,x,y,width,height,windows,floors):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.color.Color("DarkGrey"))

        self.bumpers = [Bumper(x, y, x + width, y, pygame.color.Color("Blue")),
                        Bumper(x + width, y, x + width, y + height, pygame.color.Color("Blue")),
                        Bumper(x, y + height, x + width, y + height, pygame.color.Color("Blue")),
                        Bumper(x, y, x, y + height, pygame.color.Color("Blue"))]

        self.width = width/float(windows)
        self.height = height/float(floors)

        for i in range(floors):
            for j in range(windows):
                pygame.draw.rect(self.image,pygame.color.Color("LightGrey"),
                                 pygame.Rect(j*self.width+3,i*self.height+3,self.width-6,self.height-6))

        self.rect = self.image.get_rect()
        self.rect.move_ip(x,y)


    def draw(self,window):
        for bumper in self.bumpers:
            bumper.draw(window)
