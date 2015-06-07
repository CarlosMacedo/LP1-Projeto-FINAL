import os, pygame, math, random
from pygame.locals import *
from pygame import font

#inicializar
pygame.init()
pygame.mixer.init()
size = width, height = 800, 600
tela = pygame.display.set_mode(size)
cor = 114, 115, 118
clock = pygame.time.Clock()
pygame.display.set_caption('Projeto FINAL de P1/LP1: Bomberman')
tempo_posição = 0  ##########################################
tempo_posiçãoF = 120
direção = 1

class Objetos:
    def __init__( self, imagem, posicao_inicial ):
        self.posicao = list( posicao_inicial )
        ''' Carregar Imagens '''
        diretorio_foto = os.path.join('images', imagem)
        self.imagem = pygame.image.load( diretorio_foto ).convert_alpha()
        
    def colidiu(self , obj2, obj2Px, obj2Py):
        return self.imagem.get_rect( center= (self.posicao[0] + self.imagem.get_size()[0]/2, self.posicao[1] + self.imagem.get_size()[1]/2) ).colliderect( obj2.get_rect(center= (obj2Px + obj2.get_size()[0]/2, obj2Py +obj2.get_size()[1]/2)))

    def colidiu_bloco( self , lista_blocos ):
        for x in lista_blocos:  #blocos indestrutiveis      
            if self.imagem.get_rect(center= (self.posicao[0] + self.imagem.get_size()[0]/2, self.posicao[1] + self.imagem.get_size()[1]/2) ).colliderect(blocoIn.imagem.get_rect(center=(x[0]+50, x[1]+50))):
                if self.imagem == explosao_H.imagem or self.imagem == explosao_V.imagem:
                    blocos_madeira.remove( x )
                return True
        return False

class Textos:
    def __init__( self, mensagem ):
        self.fonte = font.SysFont("ARIAL", 50, True, False)
        self.texto = self.fonte.render(mensagem, 0, (255, 255, 255))

class Audio:
    def __init__( self, audio ):
        self.diretorio_audio = os.path.join('audio', audio)
        self.audio = pygame.mixer.Sound( self.diretorio_audio )


#funções
def desenharMapa():
    for x in range( 7 ):
        for y in range( 5 ):
            posX = x*100+50
            posY = y*100+50
            if not (posY in (150,350) and posX in (150,350,550,150,350)):
                tela.blit(grama.imagem, (posX, posY))

                
def desenharBomba():
    global cont_bomba_explosao_v, cont_bomba_explosao_h
    
    if ativar_bomba:
        tela.blit(bomba.imagem, bomba.posicao)
        cont_bomba_explosao_v += 1
        cont_bomba_explosao_h += 1

        
def desenharExplosao():
    global cont_bomba_explosao_v, cont_bomba_explosao_h, ativar_bomba, cont_explosao_desaparecer, cont_explosao_desaparecer
      
    if cont_bomba_explosao_v == 110 and cont_bomba_explosao_h == 110:                 
        ativar_bomba = False

        explosao_V.posicao[0], explosao_V.posicao[1] = bomba.posicao[0], bomba.posicao[1] -105
        explosao_H.posicao[0], explosao_H.posicao[1] = bomba.posicao[0] -105, bomba.posicao[1]
        
        tela.blit( explosao_V.imagem, explosao_V.posicao )
        tela.blit( explosao_H.imagem, explosao_H.posicao )

        if cont_explosao_desaparecer == 0:
            som_explosao.audio.play(0)
        
        cont_explosao_desaparecer += 1
        if cont_explosao_desaparecer == 10:
            cont_bomba_explosao_v = 0
            cont_explosao_desaparecer = 0
            
            explosao_V.posicao[0], explosao_V.posicao[1] = -300, -300
            explosao_H.posicao[0], explosao_H.posicao[1] = -300, -300

            
def vitoriaDerrota():
    global nivel_fase, qnt_vida
    
    if len(lista_inimigos) == 0:
        som_lvl1.audio.stop()
        som_vitoria.audio.play()
        
        tela.blit(ganhou.imagem, ganhou.posicao)
        nivel_fase += 1
        
        pygame.display.flip()
        pygame.time.wait(4000)

        pygame.mixer.fadeout(500)
        som_vitoria.audio.stop()
        
    elif qnt_vida <= 0:
        som_lvl1.audio.stop()
        som_derrota.audio.play()
        
        tela.blit(perdeu.imagem, perdeu.posicao)
        qnt_vida = 3
        
        pygame.display.flip()
        pygame.time.wait(2000)

        som_derrota.audio.stop()
        
        carregarFuncionalidadesMapa1()
        mapa1()

    
def eventosMapa():
    global teclas, menu, ativar_bomba, cont_bomba_explosao_v, cont_bomba_explosao_h, qnt_vida
    
    for evento in pygame.event.get():
        if evento.type == pygame.KEYDOWN:
            #andar
            if evento.key == K_w or evento.key == K_UP:
                teclas[0] = True

            elif evento.key == K_s or evento.key == K_DOWN:
                teclas[2] = True

            if evento.key == K_a or evento.key == K_LEFT:
                teclas[1] = True

            elif evento.key == K_d or evento.key == K_RIGHT:
                teclas[3] = True
            #bomba
            if evento.key == K_SPACE and not ativar_bomba :
                ativar_bomba = True
                bomba.posicao = person.posicao[0] + 10, person.posicao[1] + 10

                cont_bomba_explosao_v = 0
                cont_bomba_explosao_h = 0

                
                som_clicar.audio.play()
                
            #racker
            if evento.key == K_PAGEUP:
                qnt_vida = 10

            if evento.key == K_ESCAPE:
                som_lvl1.audio.stop()
                carregarFuncionalidadesMapa1()
                menu = True
                
        if evento.type == pygame.KEYUP:#parar_andar
            if evento.key == pygame.K_w or evento.key == K_UP:
                teclas[0] = False
                
            elif evento.key == pygame.K_s or evento.key == K_DOWN:
                teclas[2] = False

            if evento.key == pygame.K_a or evento.key == K_LEFT:
                teclas[1] = False

            elif evento.key == pygame.K_d or evento.key == K_RIGHT:
                teclas[3] = False
                
        if evento.type == pygame.QUIT:#sair
            pygame.quit()
            exit()

            
def MoverBomberman():
    if teclas[0] and person.posicao[1] > 50:
        person.posicao[1] -= velocidadeP
        if person.colidiu_bloco(blocos_indestrutiveis) or person.colidiu_bloco(blocos_madeira) :
            person.posicao[1] += velocidadeP
        
    if teclas[1] and person.posicao[0] > 50:
        person.posicao[0] -= velocidadeP
        if person.colidiu_bloco(blocos_indestrutiveis) or person.colidiu_bloco(blocos_madeira) :
            person.posicao[0] += velocidadeP
        
    if teclas[2] and person.posicao[1] + person_size[1] < 550:
        person.posicao[1] += velocidadeP
        if person.colidiu_bloco(blocos_indestrutiveis) or person.colidiu_bloco(blocos_madeira) :
            person.posicao[1] -= velocidadeP
        
    if teclas[3] and person.posicao[0] + person_size[0] < 750:
        person.posicao[0] += velocidadeP
        if person.colidiu_bloco(blocos_indestrutiveis) or person.colidiu_bloco(blocos_madeira) :
            person.posicao[0] -= velocidadeP


def carregarFuncionalidadesMapa1():
    global continuar, tracoP, l_traco_posicao, person_size, qnt_vida, qnt_habi, blocos_madeira, blocos_indestrutiveis, lista_inimigos, teclas, ativar_bomba, velocidadeP, lista_habilidades, nivel_fase, menu, cont_bomba_explosao_v, cont_bomba_explosao_h, cont_explosao_desaparecer

    #Carregar Objetos
    person.posicao = [50,50]
    bomba.posicao = [50,50]
    coelho1.posicao = [270,270]
    coelho2.posicao = [360,65]
    coelho3.posicao = [560,270]
    coelho4.posicao = [465,475]
    rato1.posicao = [665,85]
    rato2.posicao = [165,485]
    explosao_V.posicao = [-300, -300 ]
    explosao_H.posicao = [-300, -300 ]
    ganhou.posicao = (200,200)
    perdeu.posicao = (200,200)
    fundo_menu.posicao = (0,0)
    person_size = person.imagem.get_size()
    coelho1_size = coelho1.imagem.get_size() ###################################
    #Carregar variaveis
    continuar = True
    qnt_vida = 3
    qnt_habi = 0
    blocos_madeira = [ (250, 50),(450, 50),(550, 50),(250, 150),(650, 150),(50, 250),(650, 250),(450, 350),(250, 450),(350, 450),(550, 450),(650, 450) ]
    blocos_indestrutiveis = (150,150), (350,150), (550,150), (150,350), (350,350), (550,350)
    lista_inimigos = [coelho1, coelho2, coelho3, coelho4, rato1, rato2]
    teclas = [False, False, False, False] #w/a/s/d
    ativar_bomba = False
    velocidadeP = 2
    lista_habilidades = []
    nivel_fase = 1
    menu = True
    l_traco_posicao = (526,406), (526,491), (526,568)
    tracoP = 0
    
    while qnt_habi != 3:#carregandos habilidades
        hab = random.choice( blocos_madeira )
        if hab not in lista_habilidades:
            lista_habilidades.append( hab )
            qnt_habi += 1

    #contadores de tempo
    cont_bomba_explosao_v = 0
    cont_bomba_explosao_h = 0
    cont_explosao_desaparecer = 0

############################################################################\/
def tempos_finais():
    lista = [500,1000]
    return random.choice(lista)

def direção_aleatoria():
    direção = random.randrange(1,5)
    return direção

    
def mov_aleatorio(mob):
    global tempo_posição,tempo_posiçãoF,direção
    tempo_posição += 1
    
    if tempo_posição > tempo_posiçãoF:
        tempo_posiçãoF = tempos_finais()
        direção = direção_aleatoria()
        tempo_posição = 0

    if direção == 1:
        if not(mob.posicao[1]) < 50:
            mob.posicao[1] -= 1
            if mob.colidiu_bloco(blocos_indestrutiveis) or mob.colidiu_bloco(blocos_madeira):
                mob.posicao[1] += 1
                direção = direção_aleatoria()
                
    if direção == 2:
        if not(mob.posicao[0]) < 50:
            mob.posicao[0] -= 1
            if mob.colidiu_bloco(blocos_indestrutiveis) or mob.colidiu_bloco(blocos_madeira):
                mob.posicao[0] += 1
                direção = direção_aleatoria()
                
    if direção == 3:
        if not(mob.posicao[1])  > 550:
            mob.posicao[1] += 1
            if mob.colidiu_bloco(blocos_indestrutiveis) or mob.colidiu_bloco(blocos_madeira):
                mob.posicao[1] -= 1
                direção = direção_aleatoria()
                
    if direção == 4:
        if not(mob.posicao[0]) > 750:
            mob.posicao[0] += 1
            if mob.colidiu_bloco(blocos_indestrutiveis) or mob.colidiu_bloco(blocos_madeira):
                mob.posicao[0] -= 1
                direção = direção_aleatoria()
     




"""def direção_perseguir(n):
    if person.posicao[n] > coelho1.posicao[n] - 15:
        return 2

    else:
        return 1

def mover_mob():
    global direcao1_coelho1,direcao2_coelho1,coelho1_size

    direcao1_coelho1 = direção_perseguir(1)
    direcao2_coelho1 = direção_perseguir(0)
    
    if direcao1_coelho1 == 1:
        if not(coelho1.posicao[1]) < 50:
            coelho1.posicao[1] -= 1
            if coelho1.colidiu_bloco(blocos_indestrutiveis) or coelho1.colidiu_bloco(blocos_madeira):
                coelho1.posicao[1] += 1
                
    if direcao2_coelho1 == 1:
        if not(coelho1.posicao[0]) < 50:
            coelho1.posicao[0] -= 1
            if coelho1.colidiu_bloco(blocos_indestrutiveis) or coelho1.colidiu_bloco(blocos_madeira):
                coelho1.posicao[0] += 1
                
    if direcao1_coelho1 == 2:
        if not(coelho1.posicao[1])  > 550:
            coelho1.posicao[1] += 1
            if coelho1.colidiu_bloco(blocos_indestrutiveis) or coelho1.colidiu_bloco(blocos_madeira):
                coelho1.posicao[1] -= 1
                
    if direcao2_coelho1 == 2:
        if not(coelho1.posicao[0]) > 750:
            coelho1.posicao[0] += 1
            if coelho1.colidiu_bloco(blocos_indestrutiveis) or coelho1.colidiu_bloco(blocos_madeira):
                coelho1.posicao[0] -= 1"""

tempo_posição = 0              
#################################################################/\
def mapa1():
    global qnt_vida, lista_habilidades, velocidadeP, lista_inimigos
    
    tela.blit(HP.texto, (50, -2)) #hp           
    for x in range( qnt_vida ):
        tela.blit(vida.imagem, (125+x*50, 10))
        
    for habilidade in lista_habilidades:#habilidades
        if person.colidiu( hab_vel.imagem, *habilidade ):
            lista_habilidades.remove(habilidade)
            velocidadeP += 1
        tela.blit( hab_vel.imagem, (habilidade[0]+5, habilidade[1]+5) )        
    
    for bloco in blocos_madeira:#BlocosMadeira
        tela.blit( blocoM.imagem, bloco )
        
    #desenhar inimigos na tela
    tela.blit(person.imagem, person.posicao)
    for objeto in lista_inimigos:
        if person.colidiu( objeto.imagem, *objeto.posicao):#colisao
            qnt_vida -= 1
            person.posicao = [50,50]
        if explosao_V.colidiu( objeto.imagem, *objeto.posicao ) or explosao_H.colidiu( objeto.imagem, *objeto.posicao ):
            lista_inimigos.remove(objeto)
        tela.blit(objeto.imagem, objeto.posicao)
    if (explosao_V.colidiu( person.imagem, *person.posicao ) or explosao_H.colidiu( person.imagem, *person.posicao )) and person.posicao != [50,50]:#Gambiarra_ajeitar
        person.posicao = [50,50]
        qnt_vida -= 1
    #colisao
    explosao_H.colidiu_bloco( blocos_madeira )
    explosao_V.colidiu_bloco( blocos_madeira )

    if qnt_vida == 1 and len(lista_inimigos) != 0:
        som_tensao.audio.play()

#Carregar Objetos
person = Objetos('p.png', (50,50))
bomba = Objetos('bomba.png', (50,50))
coelho1 = Objetos('dude2.png', (270,270))
coelho2 = Objetos('dude2.png', (360,65))
coelho3 = Objetos('dude.png', (560,270))
coelho4 = Objetos('dude.png', (465,475))
rato1 = Objetos('ini.png', (665,85))
rato2 = Objetos('ini.png', (165,485))
explosao_V = Objetos('ex_bombaV.png', (-300, -300 ))
explosao_H = Objetos('ex_bombaH2.png',(-300, -300 ))
vida = Objetos('vida.png', (50,50))
grama = Objetos('grama.png', (50,50))
blocoIn = Objetos('blocoindestrutivel.png', (50,50))
blocoM = Objetos('blocomadeira.png', (50,50))
hab_vel = Objetos('hab_velocidade.png', (50,50))
ganhou = Objetos('Ganhou.png', (200,200))
perdeu = Objetos('perdeu.png', (200,200))
fundo_menu = Objetos('MENU.png', (0,0))
traco_selecao = Objetos('traco_selecao.png', (526,407))
queosjogoscomecem = Objetos('queosjogoscomecem.png', (0,0))

#Carregar Textos
HP = Textos('HP')

#Carregar Audios
som_clicar = Audio('clicar.wav')
som_explosao = Audio('explode.wav')
som_menu = Audio('menu.wav')
som_tensao = Audio('tensao.wav')
som_vitoria = Audio('Vitoria.wav')
som_lvl1 = Audio('lv1.wav')
som_derrota = Audio('derrota.wav')

som_menu.audio.set_volume(0.1)
som_lvl1.audio.set_volume(0.05)
som_tensao.audio.set_volume(0.1)
som_vitoria.audio.set_volume(0.1)
som_derrota.audio.set_volume(0.1)

#carregar
carregarFuncionalidadesMapa1()


while continuar:
    tela.fill(cor)
    clock.tick(120)
    
    if menu:
        som_menu.audio.play()
        tela.blit( fundo_menu.imagem, fundo_menu.posicao )
        try:
            tela.blit( traco_selecao.imagem, l_traco_posicao[ tracoP ] )
        except:
            tracoP = 0
            tela.blit( traco_selecao.imagem, l_traco_posicao[ tracoP ] )

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:#parar_andar
                if evento.key == pygame.K_w or evento.key == K_UP:
                    tracoP -= 1
                if evento.key == pygame.K_s or evento.key == K_DOWN:
                    tracoP += 1
                    
                if evento.key == pygame.K_RETURN:
                    if l_traco_posicao[ tracoP ] == l_traco_posicao[ 0 ]:
                        pygame.mixer.fadeout(500)
                        som_clicar.audio.stop()
                        som_menu.audio.stop()
                        
                        tela.blit( queosjogoscomecem.imagem, queosjogoscomecem.posicao )
                        pygame.display.flip()
                        pygame.time.wait(2100)
                        
                        nivel_fase = 1
                        menu = False
                    elif l_traco_posicao[ tracoP ] == l_traco_posicao[ 1 ]:
                        pass
                    elif l_traco_posicao[ tracoP ] == l_traco_posicao[ 2 ]:
                        pygame.quit()
                        exit()
                              
            if evento.type == pygame.QUIT:#sair
                pygame.quit()
                exit()
        
    elif nivel_fase == 1:
        som_lvl1.audio.play()         
        
        desenharMapa()
        desenharBomba()
        
        mapa1()
        'mover_mob()' ##############################################
        mov_aleatorio(coelho1)
        mov_aleatorio(coelho2)
        mov_aleatorio(coelho3)
        mov_aleatorio(rato1)
        mov_aleatorio(rato2)
        
        desenharExplosao()    
        vitoriaDerrota()
        eventosMapa()
        MoverBomberman()
        
    elif nivel_fase == 2:
        pygame.quit()
        exit()

    pygame.display.flip()
