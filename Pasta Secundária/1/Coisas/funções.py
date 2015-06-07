import os, pygame
from pygame.locals import *
def loadImage( nome ):
    ''' Carregar Imagens '''
    nome = os.path.join('image', nome)
    imagem = pygame.image.load( nome ).convert_alpha()

    return imagem, imagem.get_rect()
