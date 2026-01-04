import pgzrun
import random
from pygame import Rect  # Importa a classe Rect para a detecção de colisões

# Definições do jogo
WIDTH = 800
HEIGHT = 600
TITLE = 'Crazy Piramide'

# Definições de cores
black = (0, 0, 0)
white = (255, 255, 255)
orange = (225, 118, 40)

# Botões do menu
button_start = Actor('button_start')
button_start.x = WIDTH // 2
button_start.y = 180

button_sound_on = Actor('button_sounds_on')
button_sound_on.x = WIDTH // 2
button_sound_on.y = 270

button_sound_off = Actor('button_sounds_off')
button_sound_off.x = WIDTH // 2
button_sound_off.y = 270

button_exit = Actor('button_quit')
button_exit.x = WIDTH // 2
button_exit.y = 360

button_restart = Actor('button_restart')
button_restart.x = WIDTH // 2
button_restart.y = 260

you_win = Actor ('you_win') 
you_win.x = WIDTH // 2
you_win.y = 130

you_lose = Actor ('you_lose') 
you_lose.x = WIDTH // 2
you_lose.y = 150

board = Actor('board')
board.x = 300
board.y = 450

# Variáveis de controle do jogo
score = 0
game_On = False
sound_on = True
game_win = False
game_over = False
gravity = 0.7  # Ajuste a gravidade
jump_velocity = -15  # Ajuste a força do pulo
current_scene = 1

# CLASSE Plataforma
class Platform(Actor):
    def __init__(self, image, x, y):
        super().__init__(image)
        self.x = x
        self.y = y
        self.rect = Rect((self.x, self.y), (self.width, self.height)) #define a area ao redor, a area de colisao

    def draw(self):
        super().draw() #Desenha a plataforma

#CLASSE JOGADOR
class Player(Actor):
    def __init__(self, images_idle, images_move, x, y):
        super().__init__(images_idle[0])
        self.x = x
        self.y = y
        self.images_idle = images_idle #Imagem para o jogador parado
        self.images_move = images_move #Imagem para o jogador se movendo
        self.images = self.images_idle #Inicia com a imagem dele parado
        self.speed = 5
        self.frame_counter = 0 #cotna os quadros para a animação
        self.frame_delay = 15 #Intervalo de tempo entra os frames
        self.current_image = 0 #Imagem Atual
        self.on_the_floor = False #Informa se o jogador esta no chão
        self.velocity_y = 0 #Velocidade dele na coordenada y
        self.rect = Rect((self.x, self.y), (40, 40))  # Essa e a area de colisão do jogador

    def updateAnimation(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0000
            self.image = self.images[self.current_image]
            self.current_image = (self.current_image + 1) % len(self.images)

    def move(self, ex, ey):
        self.x += ex
        self.y += ey
        self.rect.topleft = (self.x, self.y)
        

    def jump(self):
        if self.on_the_floor:
            self.velocity_y = -13
            self.on_the_floor = False
            sounds.sfx_jump.play()

            

    def verify_collision_with_platforms(self):
        platforms = [platform_a, platform_b, platform_c]
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.y = platform.rect.top - self.height + 30
                self.velocity_y = 0
                self.on_the_floor = True
                break

    def update(self):
        self.rect.topleft = (self.x, self.y)
        if self.on_the_floor:
            if keyboard.space:
                self.jump()        
        self.velocity_y += 0.5
        self.y += self.velocity_y
        
        if self.y >= 460:  #Se estiver nesta posição ele não ultrapaça o chão e significa que ele esta no chão.
            self.y = 460
            self.velocity_y = 0
            self.on_the_floor = True
        else:  #se não esta na posição x 460 entao verifica se ele esta colidindo com a plataforma. 
            self.verify_collision_with_platforms()
            if not any(self.rect.colliderect(platform.rect) for platform in [platform_a, platform_b, platform_c]): #se não esta colidindo com nenhuma plataforma, significa que ele tambem não esta no "chão"
                self.on_the_floor = False
        
        if keyboard.left:    #move o jogador
            self.move(-self.speed, 0)
            self.images = self.images_move  
        elif keyboard.right:          #move o jogador
            self.move(self.speed, 0)
            self.images = self.images_move  
        else: #se não ha teclas precionadas significa que ele esta parado, exibi a animação do personagem parado.
            self.images = self.images_idle

        self.updateAnimation()

    def draw(self):
        super().draw()

class Enemy(Actor):
    def __init__(self, images, x, y, speed=2):
        super().__init__(images[0])
        self.x = x
        self.y = y
        self.speed = speed
        self.images = images
        self.frame_counter = 0
        self.frame_delay = 15
        self.current_image = 0

    def updateAnimation(self): #animação do inimigo
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.image = self.images[self.current_image]
            self.current_image = (self.current_image + 1) % len(self.images)

    def update(self): 
        self.x -= self.speed  #sempre movendo-se para a esquerda
        if self.x  <= 0:  #ao chegar nesta posição ele é realocado, criando ilusao de novo inimigo.
            self.x = random.randint(800, 900)
            self.y = random.randint(450, 470)
        self.updateAnimation()

    def check_collision(self, player): #função que será chamada em update para verificar se o inimigo colide com o jogador.
        if self.colliderect(player):
            sounds.sfx_die.play()
            return True
        return False

    def draw(self):
        super().draw()

# Função para exibir o menu
def show_menu():
    screen.blit('background', (0, 0))
    button_start.draw()
    if sound_on:
        button_sound_on.draw()
        sounds.music_cp.play()
    else:
        button_sound_off.draw()
        sounds.music_cp.stop()
    button_exit.draw()

# Função para exibir a tela de derrota
def show_game_over():
    screen.blit('background', (0,0))
    you_lose.draw()
    button_restart.draw()
    button_exit.draw()
    sounds.music_lose.play()
    sounds.music_cp.stop()


def show_win():
    screen.blit('background', (0,0))
    you_win.draw()
    button_restart.draw()
    button_exit.draw()
    sounds.music_cp.stop()
    sounds.music_win.play()
    

def update():
    global game_over, game_win, score, current_scene, game_On

    if game_On:
        moises.update()
        mummy.update()
        bat.update()

        if mummy.check_collision(moises) or bat.check_collision(moises):
            game_over = True
        
        if score >= 2:
            game_win = True
            game_On = False
        
        # Troca de cenário
        if moises.x >= 800 and current_scene == 1:
            current_scene = 2
            moises.x = 50
        
        if moises.x <= 0 and current_scene == 2:
            current_scene = 1
            moises.x = 790

        #impede que ele saia da tela de jogo
        if current_scene == 1:
            if moises.x <= 5:
                moises.x = 5

        if current_scene == 2:
            if moises.x >=795:
                moises.x = 795

    if game_win:
        show_win()
        game_On = False
        
    if game_over:
        show_game_over()
        game_On = False

    #chamando as funções de controle do jogador.
    if keyboard.space:
        moises.jump()

    #move a placa de madeira que o moises deve coletar.
    board.x = board.x-3
    if board.x < -100:
        board.x = random.randint(900, 2000)
        board.y = random.randint(350, 440)

    #Quando moises colide com a placa o score aumenta
    if moises.colliderect(board):
        score += 1
        board.x = random.randint(900, 2000)
        board.y = random.randint(350, 440 )
        sounds.sfx_colect.play()
        sounds.sfx_colect.set_volume(1.0)

def on_mouse_down(pos):
    global game_On, game_win, sound_on, game_over, score, current_scene, sound_on
    # Verifica se o Start foi clicado.
    if button_start.collidepoint(pos):  
        game_On = True
        score = 0
        game_over = False
        game_win = False
    
    #Sai do jogo
    if button_exit.collidepoint(pos):
        exit()

    #Reinicia o jogo
    if button_restart.collidepoint(pos):
        game_On = True
        score = 0
        game_over = False
        game_win = False 
        moises.x = 50
        moises.y = 460
        mummy.x = 800
        bat.x = 900
        sounds.music_lose.stop()  # Para a música de derrota
        sounds.music_win.stop()   # Para a música de vitória
        if sound_on:
            sounds.music_cp.play()    # Inicia a música normal do jogo
        current_scene = 1    
    
    #Altera o estado do som
    if button_sound_on.collidepoint(pos) or button_sound_off.collidepoint(pos):
        sound_on = not sound_on
        if sound_on:
            sounds.music_cp.play()
            button_sound_on.image = 'button_sounds_on'
        else:
            sounds.music_cp.stop()
            button_sound_off.image = 'button_sounds_off'

def draw():
    
    if game_over:
        show_game_over()

    elif game_win:
        show_win()

    elif not game_On:
        show_menu()
    
    elif game_On:
         # Alterando o fundo com base no cenario_atual
        if current_scene == 1:
            screen.blit('background_1', (0, 0))
        elif current_scene == 2:
            screen.blit('background_2', (0, 0))

        #Exibindo Score e Plataformas
        screen.draw.text(f"Score: {score}", topleft=(700, 10), fontsize=30, color=white)
        screen.draw.text("Colete 2 tábuas enquanto desvia dos inimigos.", topleft=(20, 10), fontsize=30, color=white)
        platform_a.draw()
        platform_b.draw()
        platform_c.draw()
        
        #exibindo Actors
        moises.draw()
        mummy.draw()
        bat.draw()
        board.draw()


# intanciando as plataformas, jogador e inimigos.
images_move = ['wolk1', 'wolk2', 'wolk3', 'wolk4', 'wolk5', 'wolk6', 'wolk7']
images_idle = ['player_idle2', 'player_idle3', 'player_idle4', 'player_idle5', 'player_idle6', 'player_idle7', 'player_idle8']
moises = Player(images_idle, images_move, 50, 460)

mummy = Enemy(['mummy1.png', 'mummy2.png', 'mummy3.png'], 600, 460, 2)
bat = Enemy(['bat1.png', 'bat2.png', 'bat3.png'], 900, 400, 3)

platform_a = Platform('plataforma_a', 300, 400,)
platform_a.rect = Rect((platform_a.x - 0, platform_a.y, platform_a.width - 50, platform_a.height))
platform_b = Platform('plataforma_a', 470, 350)
platform_b.rect = Rect((platform_b.x - 0, platform_b.y, platform_b.width - 50, platform_b.height))
platform_c = Platform('plataforma_a', 650, 370)
platform_c.rect = Rect((platform_c.x - 0, platform_c.y, platform_c.width - 50, platform_c.height))

pgzrun.go()