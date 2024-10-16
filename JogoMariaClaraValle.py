import turtle
import math
import time
import random

################# CRIA TURTLE #####################
t = turtle
t.hideturtle()
t.tracer(0, 0)  # tira animação


###################### ROTINAS DE PRIMITIVAS DE DESENHO ##########################

def square(t, length):
    """Draws a square with sides of the given length.
    Returns the Turtle to the starting position and location.
    """
    for i in range(4):
        t.fd(length)
        t.lt(90)


def polyline(t, n, length, angle):
    """Draws n line segments.
    t: Turtle object
    n: number of line segments
    length: length of each segment
    angle: degrees between segments
    """
    for i in range(n):
        t.fd(length)
        t.lt(angle)


def polygon(t, n, length):
    """Draws a polygon with n sides.
    t: Turtle
    n: number of sides
    length: length of each side.
    """
    angle = 360.0 / n
    polyline(t, n, length, angle)


def arc(t, r, angle):
    """Draws an arc with the given radius and angle.
    t: Turtle
    r: radius
    angle: angle subtended by the arc, in degrees
    """
    arc_length = 2 * math.pi * r * abs(angle) / 360
    n = int(arc_length / 4) + 3
    step_length = arc_length / n
    step_angle = float(angle) / n

    # making a slight left turn before starting reduces
    # the error caused by the linear approximation of the arc
    t.lt(step_angle / 2)
    polyline(t, n, step_length, step_angle)
    t.rt(step_angle / 2)


def curve(turtle, tamanho):
    '''
    Desenha uma curva
    :param turtle: turtle que vai desenhar
    :param tamanho: tamanho da curva
    :return:
    '''
    for i in range(200):
        turtle.pu()
        turtle.right(1)
        turtle.forward(tamanho)


def heart(turtle, tamanho):
    '''
    Desenha um coração
    :param turtle: turtle que vai desenhar
    :param tamanho: tamanho do coração
    :return:
    '''
    turtle.fillcolor('red')
    turtle.begin_fill()
    turtle.left(140)
    turtle.pu()
    #tamanho*120 -> proporção pro coração ficar correto
    turtle.forward(tamanho * 120)
    turtle.pd()
    curve(turtle, tamanho)
    turtle.left(120)
    curve(turtle, tamanho)
    turtle.pu()
    turtle.forward(tamanho * 120)
    turtle.pd()
    turtle.end_fill()


############## ESTRUTURA DE DADOS  ###########################
def reset_fase():
    '''
    Inicializa todas as estruturas de dados, quando carrega a fase
    '''
    global jogador
    global inimigos1
    global inimigos2
    global tiro_inimigos2
    global tiro

    # JOGADOR
    jogador = {
        'x': 0,
        'y': -260,
        'speed': 15,
        'vida': 3}

    # INIMIGOS
    #########inimigos1###########
    inimigos1 = []
    linha = []
    x, y = -250, 200
    for i in range(2):  # QUANTIDADE DE LINHAS DE INIMIGOS
        for i in range(9):  # quantidade de inimigos por linha
            inimigo = {
                'x': x,
                'y': y,
                'speed': 1,
                'size': 25,
            }
            linha.append(inimigo)
            x += 60
        inimigos1.append(linha)
        y -= 40
        x = -250

    #########inimigos2###########
    inimigos2 = [{'x': 0, 'y': 200, 'speed': 2, 'size': 25, 'vida': 5}]

    # TIROS
    #######tiro jogador##########
    tiro = {'status': 'ready', 'x': -400, 'y': -400, 'speed': 50}
    #######tiro inimigo2##########
    tiro_inimigos2 = {'status': 'ready', 'x': -400, 'y': -400, 'speed': 25}

    # DADOS DA FASE 2
    if fase == 2:
        # tipo 2
        inimigos2 = [{'x': 0, 'y': 230, 'speed': 5, 'size': 25, 'vida': 5}]
        tiro_inimigos2 = {'status': 'ready', 'x': -400, 'y': -400, 'speed': 25}


############## REGISTRANDO AS IMAGENS #####################

t.register_shape('fundo.gif')
t.register_shape('jogador.gif')
t.register_shape('inimigo4.gif')
t.register_shape('iniatira.gif')
t.register_shape('fundo2.gif')

############## ROTINAS GRAFICAS ###########

# variáveis iniciais
escrita = 'SpaceWar'
legenda = 'Iniciar: P'
sublegenda1 = 'ESPAÇO para atirar'
sublegenda2 = 'SETAS para mexer'
fase = 1


def telas():
    '''
    Desenha todas telas de passagem do jogo
    :return:
    '''
    global fase
    global escrita
    global legenda
    global sublegenda1
    global sublegenda2

    if jogador['vida'] == 0:
        escrita = 'GAME OVER'
        legenda = 'Para tentar novamente, clique P'
        sublegenda2, sublegenda1 = '',''
        fase = 1
        # reinicia os contadores usados para descontar as vidas
    elif len(inimigos1[0]) == 0 and len(inimigos2) == 0:
        escrita = 'Você ganhou'
        legenda = 'Para sair, clique Q'
        sublegenda2, sublegenda1 = '', ''
    elif len(inimigos1[0]) == 0:
        escrita = 'Parabéns'
        legenda = 'Para iniciar próxima fase, clique P'
        sublegenda2, sublegenda1 = '', ''
        fase = 2

    # Características da escrita
    t.pencolor('Red')
    t.bgcolor('Black')
    t.pu()
    t.goto(0, 0)
    t.write(escrita, move=False, align='center', font=('Impact', 50, 'bold'))
    t.goto(0, -50)
    t.pencolor('White')
    t.write(legenda, move=False, align='center', font=('Questrial', 20,'bold'))
    t.goto(0, -90)
    t.write(sublegenda1, move=False, align='center', font=('Questrial', 15))
    t.goto(0, -110)
    t.write(sublegenda2, move=False, align='center', font=('Questrial', 15))


def desenha_arena():
    '''
    Desenha as bordas da arena
    :return: nada
    '''

    t.pensize(3)
    t.pu()
    t.goto(0, 0)
    t.pd()
    if fase == 1:
        t.shape('fundo.gif')
    if fase ==2:
        t. shape('fundo2.gif')
    t.stamp()


    # Limitações da arena
    t.pencolor('white')
    t.pensize(0.5)
    t.pu()
    t.goto(-300, -300)
    t.pd()
    # desenha quadrado
    for lado in range(4):
        t.fd(600)
        t.left(90)
    t.pu()
    t.hideturtle()

def desenha_jogador():
    '''
    Desenha o jogador
    :param jogador:
    :return:
    '''
    x, y = jogador['x'], jogador['y']
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.shape('jogador.gif')
    t.stamp()


def desenha_inimigos():
    '''
    desenha os inimigos do jogo
    :return: nada
    '''
    global inimigos1

    # desenha inimigos1
    if jogador['vida'] > 0:  # só desenha inimigos se jogador ainda tem vidas
        for linha in inimigos1:
            for ini in linha:
                t.up()
                t.goto(ini['x'], ini['y'])
                t.down()
                t.shape('inimigo4.gif')
                t.stamp()

    # desenha inimigos2
    if fase == 2:
        if len(inimigos2) != 0:
            t.up()
            t.goto(inimigos2[0]['x'], inimigos2[0]['y'])
            t.down()
            t.shape('iniatira.gif')
            t.stamp()

            # desenha vidas do inimigo2
            x, y = inimigos2[0]['x'] - 20, inimigos2[0]['y']
            t.goto(x, y)
            for _ in range(inimigos2[0]['vida']):
                heart(t, 0.03)
                x += 10
                t.pu()
                t.setheading(0)
                t.goto(x, y)


def desenha_tiro():
    '''
    Desenha o tiro do jogador
    :return: nada
    '''
    global tiro
    # só desenha o tiro quando já estiver clicado espaço
    if tiro['status'] == 'not ready':
        t.pu()
        t.setheading(90)
        t.goto(tiro['x'], tiro['y'])
        t.pd()
        t.pensize(4)
        t.fillcolor('white')
        t.pencolor('white')
        t.begin_fill()
        polyline(t, 1, 10, 20)
        t.end_fill()


def desenha_placar():
    '''
    Desenha as vidas do jogador no topo da arena
    :return:
    '''
    global jogador
    t.setheading(0)
    t.pu()
    x, y = -280, 280
    t.goto(x, y)
    t.pd()
    for _ in range(jogador['vida']):
        heart(t, 0.1)
        x += 50
        t.pu()
        t.setheading(0)
        t.goto(x, y)


def desenha_tiro_inimigos2():
    '''
    Desenha o tiro. Dá aspectos visuais
    :return:
    '''
    global tiro_inimigos2
    # só desenha o lista quando já estiver atirando
    if len(inimigos2) != 0:
        if tiro_inimigos2['status'] == 'not ready':
            t.pu()
            t.setheading(90)
            t.goto(tiro_inimigos2['x'], tiro_inimigos2['y'])
            t.pd()
            t.pensize(3)
            t.fillcolor('red')
            t.pencolor('red')
            t.begin_fill()
            polyline(t, 1, 10, 20)
            t.end_fill()


def desenha_jogo():
    '''
    Chama todas as outras funções de desenho
    :return: nada
    '''
    global fase
    global jogador
    t.reset()
    t.hideturtle()
    if fase == 1:
        # checa se o jogador ainda tem vidas e se inimigos estão vivos
        if jogador['vida'] > 0 and len(inimigos1[0]) > 0:
            desenha_arena()
            desenha_jogador()
            desenha_placar()
            desenha_inimigos()
            # desenha_obstáculo()
    if fase == 2:
        # checa se o jogador tem vida e se algum dos inimigos ainda tem vida
        if jogador['vida'] > 0 and (len(inimigos1[0]) > 0 or len(inimigos2) > 0):
            desenha_arena()
            desenha_jogador()
            desenha_placar()
            desenha_inimigos()
    desenha_tiro()
    desenha_tiro_inimigos2()
    t.update()


############## LOGICA DE ANIMACAO ###################
###### rotinas atreladas ao teclado
def direita():
    '''
    Faz jogador andar pra direita
    :return: nada
    '''
    global jogador
    # checando limites da arena
    if jogador['x'] > 280:
        jogador['x'] += 0
    else:
        # coordenada x do jogaor muda conforme a "velocidade"
        jogador['x'] += jogador['speed']


def esquerda():
    '''
    Faz jogador andar para esquerda
    :return: nada
    '''
    global jogador
    # checando limites da arena
    if jogador['x'] < -280:
        jogador['x'] += 0
    else:
        jogador['x'] -= jogador['speed']


def atirar():
    '''
    Posiciona e muda status do tiro do inimigo
    :return: nada
    '''
    global tiro
    if tiro['status'] == 'ready':
        tiro['x'] = jogador['x'] + 4
        tiro['y'] = jogador['y'] + 15
        tiro['status'] = 'not ready'  # dai função desenha_tiro inicia


def atirar_inimigos2():
    '''
    Posiciona e muda status do tiro do inimigo
    :return: nada
    '''
    global tiro_inimigos2
    if len(inimigos2) != 0:
        if tiro_inimigos2['status'] == 'ready':
            tiro_inimigos2['x'] = inimigos2[0]['x'] + 4
            tiro_inimigos2['y'] = inimigos2[0]['y'] - 15
            tiro_inimigos2['status'] = 'not ready'


#### demais rotinas de animação
def anima_inimigos():
    '''
    Muda coordenadas x e y dos inimigos tipo 1 e tipo 2'
    :return: nada
    '''
    global inimigos1
    global jogador
    for linha in inimigos1:
        for ini in linha:
            # speed é acrescentada na coordenada x do inimigo
            ini['x'] += ini['speed']
            # se um inimigo bate na parede direita da arena
            if ini['x'] > 280:
                # todos os inimigos mudam de direção e descem
                for enemy in linha:
                    # inimigos descem
                    enemy['y'] += -30
                    enemy['speed'] *= -1
            # se um inimigo bate na parede esquerda da arena
            if ini['x'] < -280:
                # todos os inimigos mudam de direção e descem
                for enemy in linha:
                    # inimigos descem
                    enemy['y'] += -10
                    enemy['speed'] *= -1
            # checando se chegaram no limite inferior da barreira
            if ini['y'] < -300:
                del inimigos1[:]
                jogador['vida'] = 0
    if fase == 2:
        if len(inimigos2) != 0:
            if 3 < inimigos2[0]['vida'] <= 5:
                inimigos2[0]['x'] += inimigos2[0]['speed']
            #quando inimigo fica com 3 vidas, dobra a velocidade
            elif 1<inimigos2[0]['vida'] <= 3:
                inimigos2[0]['x'] += inimigos2[0]['speed']*2
            #com uma vida, inimigo segue jogador
            if inimigos2[0]['vida'] == 1:
                inimigos2[0]['x'] = jogador['x']

            # checando limites da arena
            if inimigos2[0]['x'] > 270:
                inimigos2[0]['speed'] *= -1
            if inimigos2[0]['x'] < -270:
                inimigos2[0]['speed'] *= -1


def anima_tiro():
    '''
    Muda as coordenadas x e y do tiro do jogador
    :return:
    '''
    global tiro
    # se a barra de espaço já tiver sido clicada
    if tiro['status'] == 'not ready':
        tiro['y'] += tiro['speed']
        # checando topo da arena
        if tiro['y'] > 280:
            tiro['status'] = 'ready'  # quando atinge o topo da arena, o tiro está pronto para ser atirado novamente


def anima_tiroinimigos2():
    '''
    Muda as coordenadas do tiro do inimigo, fazendo-o se mexer
    :return: nada
    '''
    global tiro_inimigos2
    # se a barra de espaço já tiver sido clicada
    if len(inimigos2) != 0:
        if tiro_inimigos2['status'] == 'not ready':
            tiro_inimigos2['y'] -= tiro_inimigos2['speed']
            # checando topo da arena
            if tiro_inimigos2['y'] < -300:
                tiro_inimigos2['status'] = 'ready'  # quando atira limite inferior, pode atirar novamente



def isColision_ini_tiro(tiro, inimigos):
    '''
    Checa se há colisão entre o tiro do jogador e algum inimigo
    :param tiro: tiro do jogador
    :param inimigos1: inimigos
    :return: nada
    '''
    global inimigos2
    for linha in inimigos1:
        for i, ini in enumerate(linha):
            distancia = math.sqrt((tiro['x'] - ini['x']) ** 2 + (tiro['y'] - ini['y']) ** 2)
            if distancia < 27:
                # deleta dicionário do inimigo atingido
                del linha[i]
                # ajustando posição do tiro
                tiro['x'], tiro['y'] = jogador['x'], jogador['y']
                tiro['status'] = 'ready'
    if fase == 2:  # na fase 2 tbm começa a checar pela colisão com inimigos2
        if len(inimigos2) != 0:
            distancia = math.sqrt((tiro['x'] - inimigos2[0]['x']) ** 2 + (tiro['y'] - inimigos2[0]['y']) ** 2)
            if distancia < 27:
                if inimigos2[0]['vida'] == 1:
                    del inimigos2[0]

                else:
                    inimigos2[0]['vida'] -= 1
                    tiro['x'], tiro['y'] = jogador['x'], jogador['y']
                    tiro['status'] = 'ready'


                # deleta dicionário do inimigo atingido



def isColision_ini_jogador(inimigos1, jogador):
    '''
    Checa se há colisão entre os inimigos e o jogador
    :param inimigos1: inimigo2
    :param jogador: jogador
    :return: nada
    '''
    for linha in inimigos1:
        for i, ini in enumerate(linha):
            distancia = math.sqrt((jogador['x'] - ini['x']) ** 2 + (jogador['y'] - ini['y']) ** 2)
            if jogador['vida'] > 0:
                if distancia < 30:
                    # inimigo some
                    del linha[i]
                    # jogador perde uma vida
                    jogador['vida'] -= 1


def isColision_tiroini_player(tiro_ini, jogador):
    '''
    Checa se há colisão entre o tiro do inimigo2 e o jogador

    :param tiro_ini: tiros do inimigo2
    :param player: jogador
    :return: Nada
    '''
    distancia = math.sqrt((jogador['x'] - tiro_ini['x']) ** 2 + (jogador['y'] - tiro_ini['y']) ** 2)
    # se jogador ainda tem vida, checa por colisões
    if jogador['vida'] > 0:
        if distancia < 30:  # checa distancia entre o tiro do inimigo e o jogador
            tiro_inimigos2['x'], tiro_inimigos2['y'] = inimigos2[0]['x'], inimigos2[0]['y']
            tiro_inimigos2['status'] = 'ready'
            # jogador perde uma vida
            jogador['vida'] -= 1


############### LOOP PRINCIPAL ##################

def roda_jogo():
    '''
    Chama as rotinas de desenho e de animação, num While True, dando movimento ao jogo
    :return: nada
    '''
    global fase
    reset_fase()
    while True:
        anima_inimigos()
        isColision_ini_tiro(tiro, inimigos1)
        isColision_ini_jogador(inimigos1, jogador)
        isColision_tiroini_player(tiro_inimigos2, jogador)
        anima_tiro()
        desenha_jogo()
        anima_tiroinimigos2()
        # para inimigos2 atirar a em "tempo" aleatório
        a = random.randint(1, 15)  # escolhe um número aleatório
        if fase == 2 and a == 10:
            atirar_inimigos2()
        time.sleep(0.01)
        # checa se o jogador ta sem vidas, e chama uma tela de Game Over
        if jogador['vida'] == 0:
            telas()
            break
        # checa se todos os inimigos foram mortos e chama a tela de parabéns
        if len(inimigos1[0]) == 0 and len(inimigos2) == 0:
            telas()
            break
        # checa se está na fase 1 e se todos os inimigos1 foram mortos, para chamar tela de Próxima fase
        if fase == 1:
            if len(inimigos1[0]) == 0:
                telas()
                break

############## COMANDOS PELO TECLADO#############

t.listen()
# teclas do jogador
t.onkeypress(direita, "Right")
t.onkeypress(esquerda, "Left")
t.onkeypress(atirar, 'space')
# teclas do game
t.onkeypress(t.bye, 'q')  # fecha a window do turtle
t.onkeypress(roda_jogo, 'p')  # inicia loop principal

############# PROGRAMA PRINCIPAL ########################

reset_fase() #chama a estrutura de dados
telas()  # chama tela inicial
t.done()  # mantem window do turtle aberta

#Maria Clara Castro Valle - 26/09/2021