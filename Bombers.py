'''
Equipe: Adriano Alves dos Santos
        Carlos Henrique de Macêdo
        Pedro Bandeira Milfont
'''
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
menu = True
salvar_jogo = False
atirar = False
nivel_fase = 1

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
    global cont_bomba_explosao_v, cont_bomba_explosao_h, ativar_bomba, cont_explosao_desaparecer, cont_explosao_desaparecer, indestrutivel, chefe_indestrutivel
      
    if cont_bomba_explosao_v == 110 and cont_bomba_explosao_h == 110:                 
        ativar_bomba = False

        explosao_V.posicao[0], explosao_V.posicao[1] = bomba.posicao[0], bomba.posicao[1] -105
        explosao_H.posicao[0], explosao_H.posicao[1] = bomba.posicao[0] -105, bomba.posicao[1]
        
        tela.blit( explosao_V.imagem, explosao_V.posicao )
        tela.blit( explosao_H.imagem, explosao_H.posicao )

        if cont_explosao_desaparecer == 0:
            som_explosao.audio.play(0)
        
        cont_explosao_desaparecer += 1
        if cont_explosao_desaparecer == 65:
            cont_bomba_explosao_v = 0
            cont_explosao_desaparecer = 0
            
            explosao_V.posicao[0], explosao_V.posicao[1] = -300, -300
            explosao_H.posicao[0], explosao_H.posicao[1] = -300, -300
            
            indestrutivel = False
            chefe_indestrutivel = False

            
def vitoriaDerrota():
    global nivel_fase, qnt_vida, salvar_jogo
    
    if len(lista_inimigos) == 0:
        som_lvl1.audio.stop()
        som_lvl2.audio.stop()
        som_tensao.audio.stop()
        som_vitoria.audio.play()
        
        tela.blit(ganhou.imagem, ganhou.posicao)
        nivel_fase += 1
        
        pygame.display.flip()
        pygame.time.wait(4000)

        pygame.mixer.fadeout(500)
        som_vitoria.audio.stop()

        salvar_jogo = True
        
        if nivel_fase == 1:
            carregarFuncionalidadesMapa1()
        elif nivel_fase == 2:
            carregarFuncionalidadesMapa2()
        elif nivel_fase == 3:
            carregarFuncionalidadesMapa3()
        
    elif qnt_vida <= 0:
        som_lvl1.audio.stop()
        som_tensao.audio.stop()
        som_derrota.audio.play()
        
        tela.blit(perdeu.imagem, perdeu.posicao)
        qnt_vida = 3
        nivel_fase = 1
        
        pygame.display.flip()
        pygame.time.wait(2000)

        som_derrota.audio.stop()
        
        carregarFuncionalidadesMapa1()

    
def eventosMapa():
    global teclas, menu, ativar_bomba, cont_bomba_explosao_v, cont_bomba_explosao_h, qnt_vida,lista_inimigos
    
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
       
            if evento.key == K_ESCAPE:
                som_lvl1.audio.stop()
                som_lvl2.audio.stop()
                nivel_fase = 1
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


def tempos_finais():
    return random.randrange(120,500)

def direção_aleatoria():
    return random.randrange(1,5)

def mov_aleatorio(mob,direção):#principal
    global tempo_posição,tempo_posiçãoF
    tempo_posição += 1
    
    if tempo_posição > tempo_posiçãoF: #Onde muda
        tempo_posiçãoF = tempos_finais()
        direção = direção_aleatoria()
        tempo_posição = 0


    if direção == 1:#Para cima
        if not(mob.posicao[1]) < 50 and not(mob.posicao[0] < 150 and mob.posicao[1] < 150):#Parede/bloco invisivel
            mob.posicao[1] -= 1

            if mob.imagem == coelho1.imagem or mob.imagem == coelho2.imagem or mob.imagem == coelho3.imagem or mob.imagem == coelho4.imagem:
                mob.imagem = coelho2_cima.imagem    #Olhar para cima
            if mob.imagem == rato1.imagem or mob.imagem == rato2.imagem:
                mob.imagem = rato_cima.imagem
            
            if ( mob.colidiu_bloco(blocos_indestrutiveis) or mob.colidiu_bloco(blocos_madeira) ) and mob.imagem != chefe_final.imagem:
                mob.posicao[1] += 1
                direção = direção_aleatoria()
        else: #para parede
            direção = direção_aleatoria()
            
    elif direção == 2:#Para esquerda
        if not(mob.posicao[0]) < 50 and not(mob.posicao[0] < 150 and mob.posicao[1] < 150):
            mob.posicao[0] -= 1
            
            if mob.imagem == coelho1.imagem or mob.imagem == coelho2.imagem or mob.imagem == coelho3.imagem or mob.imagem == coelho4.imagem:
                mob.imagem = coelho2_esquerda.imagem    #Olhar para esquerda
            if mob.imagem == rato1.imagem or mob.imagem == rato2.imagem:
                mob.imagem = rato_esquerda.imagem
                
            if ( mob.colidiu_bloco(blocos_indestrutiveis) or mob.colidiu_bloco(blocos_madeira) ) and mob.imagem != chefe_final.imagem:
                mob.posicao[0] += 1
                direção = direção_aleatoria()
        else:
            direção = direção_aleatoria()
            
    elif direção == 3:#Para baixo
        if not(mob.posicao[1])  > 550 - mob.imagem.get_size()[1]:
            mob.posicao[1] += 1

            if mob.imagem == coelho1.imagem or mob.imagem == coelho2.imagem or mob.imagem == coelho3.imagem or mob.imagem == coelho4.imagem:
                mob.imagem = coelho2_baixo.imagem    #Olhar para baixo
            if mob.imagem == rato1.imagem or mob.imagem == rato2.imagem:
                mob.imagem = rato_baixo.imagem
            
            if ( mob.colidiu_bloco(blocos_indestrutiveis) or mob.colidiu_bloco(blocos_madeira) ) and mob.imagem != chefe_final.imagem:
                mob.posicao[1] -= 1
                direção = direção_aleatoria()
        else:
            direção = direção_aleatoria()
            
    elif direção == 4:#para direita
        if not(mob.posicao[0]) > 750 - mob.imagem.get_size()[0]:
            mob.posicao[0] += 1

            if mob.imagem == coelho1.imagem or mob.imagem == coelho2.imagem or mob.imagem == coelho3.imagem or mob.imagem == coelho4.imagem:
                mob.imagem = coelho2_direita.imagem    #Olhar para direita
            if mob.imagem == rato1.imagem or mob.imagem == rato2.imagem:
                mob.imagem = rato_direita.imagem
            
            if ( mob.colidiu_bloco(blocos_indestrutiveis) or mob.colidiu_bloco(blocos_madeira) ) and mob.imagem != chefe_final.imagem:
                mob.posicao[0] -= 1
                direção = direção_aleatoria()
        else:
            direção = direção_aleatoria()
    
    return direção

def tiro_boss(boss,direção): 
    global atirar,direção_tiro
    
    if atirar == False:
        tiro.posicao = [boss.posicao[0]+45,boss.posicao[1]+45]
        atirar = True
        direção_tiro = direção
        som_bomba_chefe2.audio.play()

    if atirar == True:
        
        if direção_tiro == 1:
            tiro.posicao[1] -= 3
            if not(-100 <= tiro.posicao[1]) or (tiro.posicao[0] < 151 and tiro.posicao[1] < 151):
                atirar = False

        if direção_tiro == 2:
            tiro.posicao[0] -= 3
            if not(-100 <= tiro.posicao[0]) or (tiro.posicao[0] < 151 and tiro.posicao[1] < 151):
                atirar = False

        if direção_tiro == 3:
            tiro.posicao[1] += 3
            if not(tiro.posicao[1] <= 600):
                atirar = False

        if direção_tiro == 4:
            tiro.posicao[0] += 3
            if not(tiro.posicao[0] <= 800):
                atirar = False

def carregarFuncionalidadesMapa1():
    global l_traco_posicao2,tempo_posição,tempo_posiçãoF, direção1,direção2,direção3,direção4,direção5,direção6,continuar, indestrutivel, tracoP, l_traco_posicao, person_size, qnt_vida, qnt_habi, blocos_madeira, blocos_indestrutiveis, lista_inimigos, teclas, ativar_bomba, velocidadeP, lista_habilidades, nivel_fase, menu, cont_bomba_explosao_v, cont_bomba_explosao_h, cont_explosao_desaparecer
    tempo_posição = 0  
    tempo_posiçãoF = 120
    direção1,direção2,direção3,direção4,direção5,direção6 = 1,1,1,1,1,1
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
    l_traco_posicao = (526,406), (526,491), (526,568)
    l_traco_posicao2 = (129,432), (591,442)
    tracoP = 0
    indestrutivel = False
    chefe.posicao = [450,250]
    
    while qnt_habi != 3:#carregandos habilidades
        hab = random.choice( blocos_madeira )
        if hab not in lista_habilidades:
            lista_habilidades.append( hab )
            qnt_habi += 1

    #contadores de tempo
    cont_bomba_explosao_v = 0
    cont_bomba_explosao_h = 0
    cont_explosao_desaparecer = 0

def carregarFuncionalidadesMapa2():
    global l_traco_posicao2,tempo_posição,tempo_posiçãoF, direção1,direção2,direção3,direção4,direção5,direção6,vida_chefe_lvl2, chefe_indestrutivel, indestrutivel, cont_hab_chefe, continuar, tracoP, l_traco_posicao, person_size, qnt_vida, qnt_habi, blocos_madeira, blocos_indestrutiveis, lista_inimigos, teclas, ativar_bomba, velocidadeP, lista_habilidades, nivel_fase, menu, cont_bomba_explosao_v, cont_bomba_explosao_h, cont_explosao_desaparecer

    tempo_posição = 0  
    tempo_posiçãoF = 120
    direção1,direção2,direção3,direção4,direção5,direção6 = 1,1,1,1,1,1

    #Carregar Objetos
    person.posicao = [50,50]
    bomba.posicao = [50,50]
    coelho1.posicao = [665,175]
    coelho2.posicao = [265,380]
    rato1.posicao = [570,87]
    rato2.posicao = [165,485]
    explosao_V.posicao = [-300, -300 ]
    explosao_H.posicao = [-300, -300 ]
    ganhou.posicao = (200,200)
    perdeu.posicao = (200,200)
    fundo_menu.posicao = (0,0)
    person_size = person.imagem.get_size()
    #Carregar variaveis
    continuar = True
    qnt_vida = 3
    qnt_habi = 0
    blocos_madeira = [ (250, 50),(50, 250),(250, 150),(450, 150),(250, 250),(650, 250),(50, 350),(450, 350),(650, 350),(350, 450),(350, 450),(650, 450) ]
    blocos_indestrutiveis = (150,150), (350,150), (550,150), (150,350), (350,350), (550,350)
    lista_inimigos = [coelho1, coelho2, rato1, rato2, chefe]
    teclas = [False, False, False, False] #w/a/s/d
    ativar_bomba = False
    velocidadeP = 2
    lista_habilidades = []
    l_traco_posicao = (526,406), (526,491), (526,568)
    l_traco_posicao2 = (129,432), (591,442)
    tracoP = 0
    vida_chefe_lvl2 = 3
    cont_hab_chefe = 0
    indestrutivel = False
    chefe_indestrutivel = False
    
    while qnt_habi != 3:#carregandos habilidades
        hab = random.choice( blocos_madeira )
        if hab not in lista_habilidades:
            lista_habilidades.append( hab )
            qnt_habi += 1

    #contadores de tempo
    cont_bomba_explosao_v = 0
    cont_bomba_explosao_h = 0
    cont_explosao_desaparecer = 0

def carregarFuncionalidadesMapa3():
    global l_traco_posicao2,tempo_posição,tempo_posiçãoF, direção1,direção2,direção3,direção4,direção5,direção6,vida_chefe_lvl3, chefe_indestrutivel, indestrutivel, cont_hab_chefe, continuar, tracoP, l_traco_posicao, person_size, qnt_vida, qnt_habi, blocos_madeira, blocos_indestrutiveis, lista_inimigos, teclas, ativar_bomba, velocidadeP, lista_habilidades, nivel_fase, menu, cont_bomba_explosao_v, cont_bomba_explosao_h, cont_explosao_desaparecer

    tempo_posição = 0  
    tempo_posiçãoF = 120
    direção1,direção2,direção3,direção4,direção5,direção6 = 1,1,1,1,1,1
    
    #Carregar Objetos
    person.posicao = [50,50]
    bomba.posicao = [50,50]
    explosao_V.posicao = [-300, -300 ]
    explosao_H.posicao = [-300, -300 ]
    ganhou.posicao = (200,200)
    perdeu.posicao = (200,200)
    fundo_menu.posicao = (0,0)
    person_size = person.imagem.get_size()
    chefe_final.posicao = [350,250]
    tiro.posicao = [-300,-300]
    
    #Carregar variaveis
    continuar = True
    qnt_vida = 3
    blocos_indestrutiveis = (150,150), (350,150), (550,150), (150,350), (350,350), (550,350)
    lista_inimigos = [chefe_final]
    teclas = [False, False, False, False] #w/a/s/d
    ativar_bomba = False
    velocidadeP = 2
    l_traco_posicao = (526,406), (526,491), (526,568)
    l_traco_posicao2 = (129,432), (591,442)
    tracoP = 0
    vida_chefe_lvl3 = 5
    cont_hab_chefe = 0
    indestrutivel = False
    chefe_indestrutivel = False

    #contadores de tempo
    cont_bomba_explosao_v = 0
    cont_bomba_explosao_h = 0
    cont_explosao_desaparecer = 0



def mapa1():
    global tempo_posição,tempo_posiçãoF, direção1,direção2,direção3,direção4,direção5,direção6, qnt_vida, lista_habilidades, velocidadeP, lista_inimigos, vida_chefe_lvl2, cont_hab_chefe, indestrutivel, chefe_indestrutivel, blocos_madeira, vida_chefe_lvl3
    
    tela.blit(HP.texto, (50, -2)) #hp           
    for x in range( qnt_vida ):
        tela.blit(vida.imagem, (125+x*50, 10))

    if nivel_fase == 3:
        lista_habilidades = []
        blocos_madeira = []
        
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
            som_morteP.audio.play()
            person.posicao = [50,50]
        if explosao_V.colidiu( objeto.imagem, *objeto.posicao ) or explosao_H.colidiu( objeto.imagem, *objeto.posicao ):
            if chefe.imagem != objeto.imagem and chefe_final.imagem != objeto.imagem:
                som_morte_monstro.audio.play()
                lista_inimigos.remove(objeto)
                
            elif not chefe_indestrutivel and objeto.imagem == chefe.imagem:
                vida_chefe_lvl2 -= 1
                chefe_indestrutivel = True
                som_monstrolvl3.audio.play()
                
                if vida_chefe_lvl2 <= 0:
                    som_monstrolvl3.audio.play()
                    lista_inimigos.remove(objeto)
            
            elif not chefe_indestrutivel and objeto.imagem == chefe_final.imagem:
                vida_chefe_lvl3 -= 1                
                chefe_indestrutivel = True
                som_monstrolvl3.audio.play()
                
                if vida_chefe_lvl3 <= 0:
                    som_monstrolvl3.audio.play()
                    lista_inimigos.remove(objeto)
                    
                    
        tela.blit(objeto.imagem, objeto.posicao)
    if (explosao_V.colidiu( person.imagem, *person.posicao ) or explosao_H.colidiu( person.imagem, *person.posicao )) and not indestrutivel:
        indestrutivel = True
        qnt_vida -= 1
        som_morteP.audio.play()
        
    #colisao
    explosao_H.colidiu_bloco( blocos_madeira )
    explosao_V.colidiu_bloco( blocos_madeira )

    if qnt_vida == 1 and len(lista_inimigos) != 0:
        som_tensao.audio.play()

    if nivel_fase == 2:
        tela.blit(texto_chefe.texto, (450, -2)) #hp do chefe lvl2         
        for x in range( vida_chefe_lvl2 ):
            tela.blit(caveira.imagem, (565+x*50, 15))

        if vida_chefe_lvl2 > 0: #habilidade do chefe
            x = random.randint(50, 750 - 177)
            y = random.randint(50, 550 - 153)
            luz.posicao = [x,y]


            if cont_hab_chefe == 150:
                tela.blit(luz.imagem, luz.posicao)
                som_bomba_chefe.audio.play()
                cont_hab_chefe = 0

                if person.colidiu( luz.imagem, *luz.posicao ):
                    qnt_vida -= 1
                    som_morteP.audio.play()
            else:
                luz.posicao = [-x,-y]
                cont_hab_chefe += 1
                
    elif nivel_fase == 3:
        tela.blit(texto_chefe.texto, (450, -2)) #hp do chefe lvl3         
        for x in range( vida_chefe_lvl3 ):
            tela.blit(caveira.imagem, (565+x*50, 15))

        if vida_chefe_lvl3 > 0: #habilidade do chefe
            x = random.randint(50, 750 - 177)
            y = random.randint(50, 550 - 153)
            luz.posicao = [x,y]

            if person.colidiu(tiro.imagem,*tiro.posicao):
                qnt_vida -= 1
                person.posicao = [50,50]
            tela.blit(tiro.imagem, tiro.posicao)
            
            if cont_hab_chefe == 150:
                tela.blit(luz.imagem, luz.posicao)
                som_bomba_chefe.audio.play()
                cont_hab_chefe = 0

                if person.colidiu( luz.imagem, *luz.posicao ):
                    qnt_vida -= 1
                    som_morteP.audio.play()
            else:
                luz.posicao = [-x,-y]
                cont_hab_chefe += 1
        
            


#Carregar Objetos
person = Objetos('p.png', (50,50))
bomba = Objetos('bomba.png', (50,50))

coelho2_baixo = Objetos('dudeBaixo.png', (0,0))
coelho2_esquerda = Objetos('dudeEsquerda.png', (0,0))
coelho2_direita = Objetos('dudeDireita.png', (0,0))
coelho2_cima = Objetos('dudeCima.png', (0,0))

coelho1 = Objetos('dude2.png', (270,270))
coelho2 = Objetos('dude2.png', (360,65))
coelho3 = Objetos('dude.png', (560,270))
coelho4 = Objetos('dude.png', (465,475))

rato1 = Objetos('ini.png', (665,85))
rato2 = Objetos('ini.png', (165,485))

rato_baixo = Objetos('iniBaixo.png', (0,0))
rato_esquerda = Objetos('ini.png', (0,0))
rato_direita = Objetos('iniDireita.png', (0,0))
rato_cima = Objetos('iniCima.png', (0,0))

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
traco_selecao2 = Objetos('traco_salvar.png', (526,407))
queosjogoscomecem = Objetos('queosjogoscomecem.png', (0,0))
chefe = Objetos('chefe.png', (450,250))
chefe_final = Objetos('chefefinal.png' , (250,250) )
caveira = Objetos('caveira1.png', (50,50))
luz = Objetos('explosaoMonstro.png', (50,50))
menu_salvar_jogo = Objetos('desejasalvar.png',(0,0))
credito = Objetos('creditos.png', (0,0))
dica = Objetos('dica.png', (0,0))
bomberXleopold = Objetos('bomberxleopold.png', (0,0))
tiro = Objetos('bola.png', (-300,-300))


#Carregar Textos
HP = Textos('HP')
texto_chefe = Textos('Boss')

#Carregar Audios
som_clicar = Audio('clicar.wav')
som_explosao = Audio('explode2.wav')
som_menu = Audio('menu.wav')
som_tensao = Audio('tensao.wav')
som_vitoria = Audio('Vitoria.wav')
som_lvl1 = Audio('lv1.wav')
som_lvl2 = Audio('lv2.wav')
som_derrota = Audio('derrota.wav')
som_bomba_chefe = Audio('bombachefe2.wav')
som_morteP = Audio('morte.wav')
som_loading = Audio('loading.wav')
som_creditos = Audio('creditos.wav')
som_monstrolvl3 = Audio('monstro.wav')
som_morte_monstro = Audio('morte2.wav')
som_bomba_chefe2 = Audio('bombachefe2.wav')

som_menu.audio.set_volume(0.1)
som_lvl1.audio.set_volume(0.05)
som_lvl2.audio.set_volume(0.05)
som_tensao.audio.set_volume(0.5)
som_vitoria.audio.set_volume(0.5)
som_derrota.audio.set_volume(0.5)


#carregar
if nivel_fase == 1:
    carregarFuncionalidadesMapa1()
elif nivel_fase == 2:
    carregarFuncionalidadesMapa2()
elif nivel_fase == 3:
    carregarFuncionalidadesMapa3()


while continuar:
    tela.fill(cor)
    clock.tick(125)
    
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
                        som_loading.audio.play()
                        pygame.display.flip()
                        pygame.time.wait(2100)
                        
                        nivel_fase = 1
                        carregarFuncionalidadesMapa1()
                        menu = False
                    elif l_traco_posicao[ tracoP ] == l_traco_posicao[ 1 ]:
                        som_menu.audio.stop()
                        try:
                            save_game = open('savegame.dat','r')
                            nivel_fase = int(save_game.read())
                            save_game.close()
                        except:
                            salve_game = open('savegame.dat','w')
                            salve_game.write( '1' )
                            salve_game.close()
                            
                        #carregar
                        if nivel_fase == 1:
                            carregarFuncionalidadesMapa1()
                        elif nivel_fase == 2:
                            carregarFuncionalidadesMapa2()
                        elif nivel_fase == 3:
                            carregarFuncionalidadesMapa3()
    
                        menu = False
                        
                    elif l_traco_posicao[ tracoP ] == l_traco_posicao[ 2 ]:
                        pygame.quit()
                        exit()
                              
            if evento.type == pygame.QUIT:#sair
                pygame.quit()
                exit()
                
    elif salvar_jogo:
        
        tela.blit( menu_salvar_jogo.imagem, menu_salvar_jogo.posicao )
        try:
            tela.blit( traco_selecao2.imagem, l_traco_posicao2[ tracoP ] )
        except:
            tracoP = 0
            tela.blit( traco_selecao2.imagem, l_traco_posicao2[ tracoP ] )

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:#parar_andar
                if evento.key == pygame.K_a or evento.key == K_LEFT:
                    tracoP -= 1
                if evento.key == pygame.K_d or evento.key == K_RIGHT:
                    tracoP += 1
                    
                if evento.key == pygame.K_RETURN:
                    if l_traco_posicao[ tracoP ] == l_traco_posicao[ 0 ]:
                        salve_game = open('savegame.dat','w')
                        salve_game.write( str(nivel_fase) )
                        salve_game.close()

                        #carregar
                        if nivel_fase == 1:
                            carregarFuncionalidadesMapa1()
                        elif nivel_fase == 2:
                            carregarFuncionalidadesMapa2()
                        elif nivel_fase == 3:
                            carregarFuncionalidadesMapa3()
                        
                        salvar_jogo = False

                        if nivel_fase == 2:#dica
                            tela.blit( dica.imagem, dica.posicao )
                            pygame.display.flip()
                            pygame.time.wait(2100)
                        elif nivel_fase == 3:#dica
                            tela.blit( bomberXleopold.imagem, bomberXleopold.posicao )
                            pygame.display.flip()
                            pygame.time.wait(2100)
                        
                    elif l_traco_posicao[ tracoP ] == l_traco_posicao[ 1 ]:
                        salvar_jogo = False

                        if nivel_fase == 2:#dica
                            tela.blit( dica.imagem, dica.posicao )
                            pygame.display.flip()
                            pygame.time.wait(2100)
                        elif nivel_fase == 3:#dica
                            tela.blit( bomberXleopold.imagem, bomberXleopold.posicao )
                            pygame.display.flip()
                            pygame.time.wait(2100)

            if evento.type == pygame.QUIT:#sair
                pygame.quit()
                exit()
                
            
    elif nivel_fase == 1:
                
        desenharMapa()
        desenharBomba()
        
        mapa1()

        direção1 = mov_aleatorio(coelho1,direção1)
        direção2 = mov_aleatorio(coelho2,direção2)
        direção3 = mov_aleatorio(coelho3,direção3)
        direção4 = mov_aleatorio(coelho4,direção4)
        direção5 = mov_aleatorio(rato1,direção5)
        direção6 = mov_aleatorio(rato2,direção6)
        
        desenharExplosao()    
        vitoriaDerrota()
        eventosMapa()
        MoverBomberman()
        
    elif nivel_fase == 2:
        
        desenharMapa()
        desenharBomba()
        
        mapa1()

        direção1 = mov_aleatorio(coelho1,direção1)
        direção2 = mov_aleatorio(coelho2,direção2)
        direção3 = mov_aleatorio(chefe,direção3)
        direção5 = mov_aleatorio(rato1,direção5)
        direção6 = mov_aleatorio(rato2,direção6)

        desenharExplosao()    
        vitoriaDerrota()
        eventosMapa()
        MoverBomberman()
    
    elif nivel_fase == 3:
        desenharMapa()
        desenharBomba()

        mapa1()

        tiro_boss(chefe_final,direção3)
        direção3 = mov_aleatorio(chefe_final,direção3)        
        
        desenharExplosao()
        vitoriaDerrota()
        eventosMapa()
        MoverBomberman()
        
    elif nivel_fase == 4:#zeramento
        som_creditos.audio.play()
        tela.blit( credito.imagem, credito.posicao )
        pygame.display.flip()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:#sair
                pygame.quit()
                exit()
                
        pygame.time.wait(2100)
        menu = True
    else:
        nivel_fase = 1
        carregarFuncionalidadesMapa1()
        menu = True
    
    pygame.display.flip()
