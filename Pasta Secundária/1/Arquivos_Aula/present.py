import pygame, sys,os, time
from pygame.locals import *

#inicia os modulos
pygame.init()

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

#Impressao do fundo branco e do arquivo carregado
screen.blit(background, (0,0))
screen.blit(ball_surface, (50,50))
pygame.display.flip()

time.sleep(6)

pygame.display.quit()