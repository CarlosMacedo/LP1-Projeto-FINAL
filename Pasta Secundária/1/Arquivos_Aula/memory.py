import sys, os, random, pygame
from pygame.locals import *

clock = pygame.time.Clock()
pygame.init()

running = True
N_CARDS = 32
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CARD_HEIGHT = 122
CARD_WIDTH = 167
p_turn = 0 #0 para p1, 1 para p2
p1_score = 0
p2_score = 0

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))
pygame.display.set_caption("Memory")

def isIn(x, n):
    for i in range(n):
        if x[i] == x[n]: return 1
    return 0

def selected_ones():
    x = []
    j = 0
    for i in range(4):
        for k in range(4):
            if selector.selected_check[i][k] == 1:
                x.append((i,k))
                j+= 1
    return x

class Selector:
    selector = pygame.Surface((CARD_WIDTH + 10, CARD_HEIGHT + 10))
    selector = selector.convert()
    selector.fill((34, 139, 34))

    selected = pygame.Surface((CARD_WIDTH + 6, CARD_HEIGHT + 6))
    selected = selected.convert()
    selected.fill((139, 0, 0))

    selected_check = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
    match = [ [0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0] ]
    two_selected = 0

    score = 0
    x = 0
    y = 0

    def blit(self):
        screen.blit(self.selector, (20 + (CARD_WIDTH + 25)* self.x, 20 + (CARD_HEIGHT + 25)*self.y))
        for i in range(4):
            for k in range(4):
                if (self.match[i][k] == 1) | (self.selected_check[i][k] == 1):
                    screen.blit(self.selected, (22 + (CARD_WIDTH + 25)*i, 22 + (CARD_HEIGHT + 25)*k))

    def button(self):
        global p_turn
        pygame.event.pump()
        key = pygame.key.get_pressed()
        if key[K_UP]:
            if self.y > 0: self.y += -1
            if self.two_selected > 1:
                self.reset(self.selected_check)
        if key[K_DOWN]:
            if self.y < 3: self.y += 1
            if self.two_selected > 1:
                self.reset(self.selected_check)
        if key[K_LEFT]:
            if self.x > 0: self.x += -1
            if self.two_selected > 1:
                self.reset(self.selected_check)
        if key[K_RIGHT]:
            if self.x < 3: self.x += 1
            if self.two_selected > 1:
                self.reset(self.selected_check)
        if key[K_RETURN]:
            if (self.selected_check[self.x][self.y] == 0) & (self.match[self.x][self.y] == 0):
                self.selected_check[self.x][self.y] = 1
                self.two_selected += 1
                if self.two_selected > 1:
                    x = selected_ones()
                    self.check(x[0][0], x[0][1], x[1][0], x[1][1])



    def mouse(self):
        pygame.event.pump()
        mouse = pygame.mouse.get_pos()
        for i in range(4):
            if (mouse[0] > 25 + (25 + CARD_WIDTH)*i):
                self.x = i
        for j in range(4):
            if mouse[1] > 25+ (25 + CARD_HEIGHT)*j:
                self.y = j
        if self.two_selected > 1:
            self.reset(self.selected_check)

    def check(self, i, k, x, y):
        global p_turn, p1_score, p2_score
        print "hash map",card.hash_map[i][k], card.hash_map[x][y]
        if card.hash_map[i][k] == card.hash_map[x][y]:
            if p_turn == 0:
                p1_score += 1
            else: p2_score +=1
            print "score",self.score
            self.match[i][k] = 1
            self.match[x][y] = 1
        else:
            if p_turn == 0:
                p_turn = 1
            else: p_turn = 0



    def reset(self, x):
        self.two_selected = 0
        for i in range(4):
            for k in range(4):
                x[i][k] = 0

class Card:
    cards = []
    choice = []
    back = []

    hash_map = [[0,0,0,0], [0,0,0,0],[0,0,0,0],[0,0,0,0]]

    def load(self, n):
        for i in range(n):
            self.cards += [pygame.image.load(os.path.join("coisas", "WWK", str(i) + ".jpg"))]
        for i in range (5):
            self.back += [pygame.image.load(os.path.join("coisas", "WWK", "back" + str(i) + ".jpg"))]

    def choose(self):

        y = [random.randint(0, N_CARDS -1)]

        for i in range(N_CARDS/2-1):
            y.append(random.randint(0, N_CARDS - 1))
            while isIn(y, i+1):
                y[i+1] = random.randint(0, N_CARDS - 1)

        for i in range(N_CARDS/4):
            self.choice += [self.cards[y[i]]]

        x = [random.randint(0, N_CARDS/4 -1)]

        for i in range(N_CARDS/4-1):
            x.append(random.randint(0, N_CARDS/4 - 1))
            while isIn(x, i+1):
                x[i+1] = random.randint(0, N_CARDS/4 - 1)
        return x

    def hash(self, r):
        x = r
        random.shuffle(r)
        random.shuffle(x)
        r += x
        y = 0
        random.shuffle(r)

        for i in range(4):
            for k in range(4):
                self.hash_map[i][k] = r[y]
                y += 1

    def blit(self, n):
        x = 0
        for i in range(4):
            for k in range(4):
                screen.blit(self.back[back], (25 + (25 + CARD_WIDTH)*i, 25+ (25 + CARD_HEIGHT)*k))
                if (selector.match[i][k] == 1) | (selector.selected_check[i][k] == 1):
                    screen.blit(self.choice[self.hash_map[i][k]], (25 + (25 + CARD_WIDTH)*i, 25+ (25 + CARD_HEIGHT)*k))


def handle():
    global running
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            selector.button()
        elif event.type == MOUSEBUTTONDOWN:
            selector.mouse()

card = Card()
card.load(N_CARDS)
r = card.choose()
card.hash(r)
print card.hash_map

back = random.randint(0, 4)
selector = Selector()

font = pygame.font.Font(None, 30)
def score_blit():
    global p1_score, p2_score, p_turn
    scores = font.render("Scores:", True, (255, 255, 255))
    score_p1 = font.render("P1 = " + str(p1_score), True, (0, 0, 205))
    score_p2 = font.render("P2 = " + str(p2_score), True, (192, 0, 0))
    turn = font.render("Turn:", True, (255, 255, 255))
    p1 = font.render("P1", True, (0, 0, 205))
    p2 = font.render("P2", True, (192, 0, 0))
    win = font.render("WINS!", True, (255, 255, 255))
    draw = font.render("DRAW!", True, (255, 255, 255))

    screen.blit(turn, (800, 20))
    if (p_turn == 0):
        screen.blit(p1, (880, 20))
    else: screen.blit(p2, (880, 20))
    screen.blit(scores, (800, 160))
    screen.blit(score_p1, (800, 200))
    screen.blit(score_p2, (800, 240))
    if (p1_score + p2_score) == 8:
        screen.blit(win, (840, 280))
        if p1_score > p2_score:
            screen.blit(p1, (800, 280))
        elif p1_score < p2_score:
            screen.blit(p2, (800, 280))
        else: screen.blit(drawm (800, 280))

while running:
    clock.tick(30)
    handle()
    screen.blit(background, (0, 0))
    selector.blit()
    card.blit(N_CARDS)
    score_blit()
    pygame.display.flip()

pygame.display.quit()
