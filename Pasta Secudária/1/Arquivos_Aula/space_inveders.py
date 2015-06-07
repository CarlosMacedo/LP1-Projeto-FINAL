import sys, os, random, pygame
from pygame.locals import *
from threading import Thread

clock = pygame.time.Clock()

pygame.init()

running = True
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 500
stop = 0

#offsets do sprite alien3 width = 24, height = 16
#alien2: width = 22, height = 16
#alien1: width = 16, height = 16

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.get_surface()

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
pygame.display.set_caption("SPACE INVADERS!")


class Shot:
    shot = pygame.Surface((2, 8))
    shot = shot.convert()
    shot.fill((255, 255, 255))

    ready = 0
    y = 350
    x = 0
    dx = 12
    def shoot(self):
        key = pygame.key.get_pressed()
        if (key[K_SPACE]) & (self.y > 10):
            self.ready = 1

    def reset(self):
        self.ready = 0
        self.y = 350

    def blit(self, x):
        if (self.ready == 0):
            self.x = x
        if (self.ready == 1) & (self.y > 10):
            screen.blit(self.shot, (self.x + 15, self.y))
            self.y -= self.dx
        if (self.y <= 10):
            self.reset()

class Aliens:
    alien1 = []
    alien2 = []
    alien3 = []
    show = [[], [], [], [], []]
    hit = []
    points = [40, 20, 20, 10, 10]
    score = 0
    alien_shot = pygame.Surface((2, 8))
    alien_shot = alien_shot.convert()
    alien_shot.fill((255, 255, 255))
    increment = 0
    down = 0 #1 = desce, 0 = anda
    move = 1 #1 = move, 0 = nao move
    left_or_right = 1 #1 = right, -1 = left
    x_shot = 0
    y_shot = 0
    n_hits = 0
    ready = 0
    level = 1
    chance = 300 #30%
    r = 10
    l = 0
    x = 20
    y = 100
    frame = 0
    k = 0
    dx = 25
    dx_shot = 5
    def init(self):
        self.alien3 += [pygame.image.load(os.path.join("invaders", "alien31.bmp"))]
        self.alien3 += [pygame.image.load(os.path.join("invaders", "alien32.bmp"))]
        self.alien3[0].set_colorkey((0, 255, 255))
        self.alien3[1].set_colorkey((0, 255, 255))

        self.alien2 += [pygame.image.load(os.path.join("invaders", "alien21.bmp"))]
        self.alien2 += [pygame.image.load(os.path.join("invaders", "alien22.bmp"))]
        self.alien2[0].set_colorkey((0, 255, 255))
        self.alien2[1].set_colorkey((0, 255, 255))

        self.alien1 += [pygame.image.load(os.path.join("invaders", "alien11.bmp"))]
        self.alien1 += [pygame.image.load(os.path.join("invaders", "alien12.bmp"))]
        self.alien1[0].set_colorkey((0, 255, 255))
        self.alien1[1].set_colorkey((0, 255, 255))


        for i in range(5):
            for k in range(11):
                self.show[i] += [0]

        for i in range(11):
            self.hit += [4]

    def blit(self, x, y, x_target, stop, lives, ready):
        for i in range(self.level):
            th = Thread(target = self.shot, args = (x_target, stop))
            th.start()
        #Calcula o movimento
        if (frames%self.dx == 0) & (frames != 0):
            if (self.frame == 0):
                self.frame = 1
            else: self.frame = 0

            if (self.down == 0):
                self.x += 5*self.left_or_right
                #print self.x

            if (((self.x + 30*(self.r+1) >= 490) | (self.x + self.l*30 <= 10)) & (self.down == 1)):
                if self.dx > 6:
                    self.dx -= 5
                self.y += 10
                self.move = 1

            if (self.x + 30*(self.r+1) >= 490) & (self.down == 0):
                self.left_or_right = -1
                self.down = 1

            if (self.x + self.l*30 <= 10) & (self.down == 0):
                self.left_or_right = 1
                self.down = 1

        #Controle de movimento
            if (self.move == 1):
                self.move = 0
                self.down = 0

        if (ready != 0):
            for i in range(11):
                if self.hit[i] >= 0: #caso nao tenha matado todos de uma coluna
                    collide(x, y, self.x + 30*i, self.y + 30*(self.hit[i] + 1), i)
                    if self.show[self.hit[i]][i] == 1:
                        self.n_hits += 1
                        self.score += self.points[self.hit[i]]
                        self.hit[i] -= 1
                        self.increment = 0
                        #arrumar o movimento depois de matar os extremos
                        if (self.l != self.r):
                            if (self.hit[i] == -1) & (i == self.l):
                                k = self.l
                                while (self.show[0][k] == 1) & (k <= 10):
                                    self.l += 1
                                    k += 1
                            elif (self.hit[i] == -1) & (i == self.r):
                                k = self.r
                                while (self.show[0][k] == 1) & (k >= 0):
                                    self.r -= 1
                                    k -= 1
                        break
        if (self.n_hits%7 == 0) & (self.increment == 0) & (self.n_hits != 0):
            if self.dx >= 5:
                self.increment = 1
                self.dx -= 2

        if self.n_hits == 55:
            self.reset()

        #Imprime
        for i in range(11):
            if self.show[self.k][i] == 0:
                screen.blit(self.alien3[self.frame], (self.x + 30*i, self.y))


        self.k = 1
        for k in range(self.k, 3):
            for i in range(11):
                if self.show[k][i] == 0:
                    screen.blit(self.alien2[self.frame], (self.x + 30*i, self.y + 30*k))

        self.k = 3
        for k in range(self.k, 5):
            for i in range(11):
                if self.show[k][i] == 0:
                    screen.blit(self.alien1[self.frame], (self.x + 30*i, self.y + 30*k))

        self.k = 0

        for i in range(11):
            if self.y + self.hit[i]*30 >= 350:
                lives = 0

    def shot(self, x_target, stop):
        shot = random.randint(0, 1000)
        if (shot <= self.chance) & (self.ready == 0):
            i = random.randint(0,10)
            k = random.randint(0, 3)
            while (self.show[k][i] == 1):
                i = random.randint(0,10)
                k = random.randint(0, 3)
            self.x_shot = self.x + 15*i
            self.y_shot = self.y + 15 + 30*k
            self.ready = 1
        if (self.ready == 1) & (self.y_shot <= 370) & (stop == 0):
            collide_def(self.x_shot, self.y_shot, x_target)
            screen.blit(self.alien_shot, (self.x_shot, self.y_shot))
            self.y_shot += self.dx_shot
        else: self.ready = 0

    def reset(self):
        self.left_or_right = 1
        self.x = 20
        self.y = 100
        self.dx = 25 - 5*self.level
        self.dx_shot -= 1
        self.level += 1
        self.chance += 100
        self.n_hits = 0
        self.l = 0
        self.r = 10
        for k in range(5):
            for i in range(11):
                self.show[k][i] = 0
                self.hit[i] = 4




class Defender:
    x = 10
    y = 350
    lives = 3
    stop = 0
    destroyed = pygame.image.load(os.path.join("invaders", "destroyed.bmp"))
    destroyed.set_colorkey((0,255,255))
    defensor = pygame.image.load(os.path.join("invaders", "defender.bmp"))
    defensor.set_colorkey((0,255,255))

    def move(self):
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if ((key[K_RIGHT]) & (self.x < 465) & (self.stop == 0)):
            self.x += 5
        if ((key[K_LEFT]) & (self.x > 8) & (self.stop == 0)):
            self.x -= 5
    def blit(self):
        if (self.stop == 0):
            screen.blit(self.defensor, (self.x, self.y))
        else:
            screen.blit(self.destroyed, (self.x, self.y))
            if self.stop > 0:
                self.stop -= 1
            if self.stop == 0:
                self.reset()

    def reset(self):
        self.x = 10


defender = Defender()
shot = Shot()
aliens = Aliens()

aliens.init()

frames = 0

def collide(x_shot, y_shot, x_target, y_target, i): #otimo!, 0 para aliens, 1 para defender
    if (y_shot <= y_target):
        if ((x_shot + 10 >= x_target) & (x_shot + 1 < (x_target + 20))):
                aliens.show[aliens.hit[i]][i] = 1
                shot.reset()
                return 1
    return 0

def collide_def(x_shot, y_shot, x_def):
    if (y_shot >= defender.y):
        if ((x_shot + 10 >= x_def) & (x_shot + 1 < x_def + 30)):
            defender.stop = 20
            defender.lives -= 1
            return 1

font = pygame.font.Font(None, 20)
def blit_font():
    surface_font_score = font.render("Score = " + str(aliens.score), True, (255, 255, 255))
    screen.blit(surface_font_score, (10, 10))
    surface_font_live = font.render("Lives = " + str(defender.lives), True, (255, 255, 255))
    screen.blit(surface_font_live, (280, 10))
    surface_font_level = font.render("Level = " + str(aliens.level), True, (255, 255, 255))
    screen.blit(surface_font_level, (370, 10))

lose = pygame.font.Font(None, 100)
def lose_blit():
    surface_font_lose = lose.render("YOU LOSE!", True, (0, 139, 0))
    screen.blit(surface_font_lose, (80, 100))

def handle():
    global running
    if defender.lives == 0:
        lose_blit()
        defender.stop = 20
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            shot.shoot()

while (running):
    clock.tick(30)
    screen.blit(background, (0, 0))
    defender.move()
    shot.blit(defender.x)
    #aliens.shot(defender.x)
    aliens.blit(shot.x, shot.y, defender.x, defender.stop, defender.lives, shot.ready)
    defender.blit()
    blit_font()
    handle()
    pygame.display.flip()
    frames += 1

pygame.display.quit()