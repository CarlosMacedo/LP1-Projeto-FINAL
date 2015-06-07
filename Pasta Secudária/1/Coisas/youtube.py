import pygame
import math

from pygame.locals import *

#Iniciar o jogo
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

#Carregar imagens
player = pygame.image.load('resources/images/dude.png')
grass = pygame.image.load('resources/images/grass.png')
castle = pygame.image.load('resources/images/castle.png')
arrow = pygame.image.load('resources/images/bullet.png')
badguyimg1 = pygame.image.load('resources/images/badguy.png')
badguyimg = badguyimg1

keys = [False, False, False, False] #w/a/s/d
playerpos = [100, 100]
acc = [0,0]
arrows = []
badtimer = 100
badtimer1 = 0
badguys = [[640,100]]
healthvalue = 194

while True:
    #limpar a tela
    screen.fill(0)

    #plotar o cenario
    for x in range( int( width/ grass.get_width() ) + 1):
        for y in range( int( height/ grass.get_height() ) + 1):
            screen.blit(grass, (x*100, y*100))
    for x in range(30, 346, 105):
        screen.blit(castle, (0,x))


    #desenhar alguns elementos na tela
    #screen.blit(player, playerpos)
    position = pygame.mouse.get_pos()
    
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]+26)
    playerrot = pygame.transform.rotate(player, 360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)

    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index+=1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(arrow1, (projectile[1], projectile[2]))
  
            
    #update na tela
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False
            elif event.key == pygame.K_d:
                keys[3] = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32),position[0]-(playerpos1[0]+26)),playerpos1[0]+32,playerpos1[1]+32])
            
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    #movimentar jogador
    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    if keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5

     
    
        
        
