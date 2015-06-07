import pygame, sys,os, time
from pygame.locals import *

pygame.init()

window = pygame.display.set_mode((800, 600))

screen = pygame.display.get_surface()
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
screen.blit(background, (0,0))
pygame.display.flip()

pygame.display.set_caption("Teste")

time.sleep(3)

pygame.display.quit()