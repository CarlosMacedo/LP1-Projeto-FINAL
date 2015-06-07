import pygame
pygame.init()

size = largura, altura = 840, 360
velocidade = [1, 1]
v = [-1,-1]
cor = 0, 0, 0

tela = pygame.display.set_mode(size)

bola = pygame.image.load("image/ball.gif").convert_alpha()
bolarect = bola.get_rect()

bola2 = pygame.image.load("image/bola.bmp").convert_alpha()
bolap = bola2.get_rect()


while True:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: exit()

    bolarect = bolarect.move(velocidade)
    if bolarect.left < 0 or bolarect.right > largura:
        velocidade[0] = -velocidade[0]
    if bolarect.top < 0 or bolarect.bottom > altura:
        velocidade[1] = -velocidade[1]

    
    

    tela.fill(cor)
    tela.blit(bola2, bolap)
    tela.blit(bola, bolarect)
    tela.blit(bola2,(250,0))
    
    pygame.display.flip()
    pygame.time.delay(10)
