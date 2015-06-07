import pygame, sys,os, time, random
from pygame.locals import *

#relogio interno
clock = pygame.time.Clock()

#inicia os modulos
pygame.init()

#Varialvel que indica que o jogo esta rodando
running = True;

#Janela principal
window = pygame.display.set_mode((800, 600))

#Tela para impressao das imagens
screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
pygame.display.set_caption("Exemplo")

#Arquivo para ser impresso na tela
ball_file = os.path.join("hitit", "cannonball.bmp")
ball_surface = pygame.image.load(ball_file)
ball_surface.set_colorkey((0, 0xFF, 0xFF))

screen.blit(background, (0,0))
screen.blit(ball_surface, (50,50))
pygame.display.flip()

def new_ball():
    pygame.event.pump()
    key = pygame.key.get_pressed()
    if key[pygame.K_a]:
        x = random.randint(10,790)
        y = random.randint(10,590)
        screen.blit(ball_surface, (x,y))
        pygame.display.flip()

def handle():
    global running
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            new_ball()

while running:
    clock.tick(30)
    handle()


pygame.display.quit()