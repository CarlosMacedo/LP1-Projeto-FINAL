import sys, os, random, pygame
from math import *
from pygame.locals import *
from threading import Thread

clock = pygame.time.Clock()
pygame.init()

running = True
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 600

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
pygame.display.set_caption("Hit It")

def distance(x1, y1, x2, y2):
    return sqrt((x2-x1)** 2 + (y2-y1)**2)

def circular_collision(x1, y1, x2, y2, raio1, raio2):
    if (distance(x1, y1, x2, y2) < (raio1 + raio2)):
        return True
    else:
        return False



class Target_Control:
    targets = []
    images = []

    def __init__(self):
        self.images += [pygame.image.load(os.path.join("hitit", "marble.bmp"))]
        self.images[0].set_colorkey((0,255,255))
        self.images += [pygame.image.load(os.path.join("hitit", "red_marble_50.bmp"))]
        self.images[1].set_colorkey((0,255,255))
        self.images += [pygame.image.load(os.path.join("hitit", "white_marble_50.bmp"))]
        self.images[2].set_colorkey((0,255,255))

    def add(self, x, y, xvel, yvel):
        r = random.randint(0,2)
        if (r == 0): raio = 10
        else: raio = 25
        t = Target(x, y,self.images[r],raio)
        t.set_speed(xvel,yvel)
        self.targets.append(t)

    def remove(self, i):
        self.targets.remove(i)

    def size(self):
        return len(self.targets)

    def blit(self):
        for i in range(len(self.targets)):
            self.targets[i].blit()

    def move(self):
        for i in range(len(self.targets)):
            self.targets[i].speed()

#raio das marbles = 10

class Target:
    x = 0
    y = 0
    xvel = 0
    yvel = 0
    raio = 0

    def __init__(self, x, y, image, raio):
        self.x = x
        self.y = y
        self.image = image
        self.raio = raio

    def set_speed(self, xvel, yvel):
        self.xvel = xvel
        self.yvel = yvel

    def speed(self):
        self.x += self.xvel
        if (self.x - self.raio < 0):
            self.x = self.raio
            self.xvel = -1*self.xvel
        if (self.x + self.raio > SCREEN_WIDTH):
            self.x = SCREEN_WIDTH - self.raio
            self.xvel = -1*self.xvel

        self.y += self.yvel
        if (self.y - self.raio < 0):
            self.y = self.raio
            self.yvel = -1*self.yvel
        if (self.y + self.raio > SCREEN_HEIGHT):
            self.y = SCREEN_HEIGHT - self.raio
            self.yvel = -1*self.yvel

    def blit(self):
        screen.blit(self.image, (self.x - self.raio, self.y - self.raio))


class Ball:
    x = SCREEN_WIDTH/2
    y = SCREEN_HEIGHT/2
    xvel = 0
    yvel = 0
    raio = 10
    score = 0
    ball_image = pygame.image.load(os.path.join("hitit", "cannonball.bmp"))
    ball_image.set_colorkey((0,255,255))

    def move(self):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        self.yvel += 1*(key[pygame.K_DOWN] - key[pygame.K_UP])
        self.xvel += 1*(key[pygame.K_RIGHT] - key[pygame.K_LEFT])
        self.y += 5*(key[pygame.K_s] - key[pygame.K_w])
        self.x += 5*(key[pygame.K_d] - key[pygame.K_a])

    def speed(self, targets):
        #self.yvel += 1

        self.x += self.xvel
        if (self.x - self.raio < 0):
            self.x = self.raio
            self.xvel = -0.5*self.xvel
        if (self.x + self.raio > SCREEN_WIDTH):
            self.x = SCREEN_WIDTH - self.raio
            self.xvel = -0.5*self.xvel
        if (self.detect_collision(targets) == True):
            self.x -= self.xvel
            self.xvel = -0.5*self.xvel

        self.y += self.yvel
        if (self.y - self.raio < 0):
            self.y = self.raio
            self.yvel = -0.5*self.yvel
        if (self.y + self.raio > SCREEN_HEIGHT):
            self.y = SCREEN_HEIGHT - self.raio
            self.yvel = -0.5*self.yvel
            self.xvel = 0.9*self.xvel
        if (self.detect_collision(targets) == True):
            self.y -= self.yvel
            self.yvel = -0.5*self.yvel

    def detect_collision(self,targets):
        for i in range(len(targets)):
            x2 = targets[i].x
            y2 = targets[i].y
            raio2 = targets[i].raio
            if (circular_collision(self.x, self.y, x2, y2, self.raio, raio2) == True):
                if raio2 == 25: self.score += 50
                elif raio2 == 10: self.score += 100
                del targets[i]
                return True
        return False

    def blit(self):
        screen.blit(self.ball_image, (self.x - self.raio, self.y - self.raio))

class Event_Control:
    target_control = Target_Control()
    ball = Ball()
    level = 1
    timer1 = 0
    timer2 = 30

    def blit(self):
        self.target_control.move()
        self.ball.blit()
        self.target_control.blit()

    def level_control(self):
        if self.level == 1:
            t = pygame.time.get_ticks()
            if ((t - self.timer1 >= 1000) & (self.target_control.size() <= 10)):
                self.timer1 = pygame.time.get_ticks()
                self.target_control.add(random.randint(25,575),random.randint(25,575),
                random.randint(-2,2),(random.randint(-2,2)))


font = pygame.font.Font(None, 20)
def blit_font():
    surface_font_score = font.render("Score = " + str(event.ball.score), True, (0,0,0))
    screen.blit(surface_font_score, (10,10))

def handle():
    global running
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

pygame.key.set_repeat(1)

event = Event_Control()
event.timer1 = pygame.time.get_ticks()

while running:
    clock.tick(60)
    handle()
    screen.blit(background, (0, 0))
    event.ball.move()
    event.ball.speed(event.target_control.targets)
    event.level_control()
    event.blit()
    blit_font()
    pygame.display.flip()

pygame.display.quit()