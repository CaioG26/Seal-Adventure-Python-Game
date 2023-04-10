# SEAL ADVENTURE - JOGO 1º SEMESTRE


import time

import pygame
from pygame.locals import* #
import math, random, sys, os
from os import path


class Game():
    def __init__(self):

        pygame.init()
        pygame.display.set_caption("Seal Adventure")
        self.running, self.playing = True, False
        self.ataque=False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 600 # Tamanho da tela
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = 'fonte/PressStart2P-vaV7.ttf'
        self.BLACK,self. BLUE = (0, 0, 0), (63, 255, 223) #Definindo cores
        self.main_menu = MainMenu(self) #Classes
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        self.kills= 0
        self.ultimakills=0
        self.highkills=0


    #def load_data(self):
        # load high score
        #self.dir = path.dirname(__file__)
       # with open(path.join(self.dir, HS_FILE), 'r') as f:
            #try:
                #self.highkills = int(f.read())
            #except:
                #self.highkills = 0



    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
#INICIO
            # # #  CONFIGURAÇÕES DE TELA ------------------------------------------------------------------
            larguraTela, alturaTela = 1000, 500
            metadeLargura = larguraTela / 2
            metadeAltura = alturaTela / 2
            areaTela = larguraTela * alturaTela
            tela = pygame.display.set_mode((larguraTela, alturaTela))
            bg = pygame.image.load("Cenario/cenariogelo.jpeg")
            background = pygame.transform.scale(bg, (larguraTela, alturaTela))
            pygame.display.set_caption("Seal Adventure")

            pygame.init()
            CLOCK = pygame.time.Clock()
            FPS = 60
            BLACK = (0, 0, 0)


            # # # MUSICA DO JOGO -----------------------------------------------------------------------------------

            pygame.mixer.music.load('Musicas/Snow02.ogg')
            pygame.mixer.music.play(-1)

            # # # PERSONAGEM ---------------------------------------------------------------------------------
            scale_hero=[100,100]
            left = [pygame.transform.scale(pygame.image.load(os.path.join('Personagens', 'desenhoesquerda.png')),(scale_hero)),
                    pygame.transform.scale(pygame.image.load(os.path.join('Personagens', 'correndo 2.0.png')),(scale_hero)),
                    pygame.transform.scale(pygame.image.load(os.path.join('Personagens', 'correndo 3.0.png')),(scale_hero)),
                    pygame.transform.scale(pygame.image.load(os.path.join('Personagens', 'pertras1.png')),(scale_hero))
                    ]
            right = [pygame.transform.scale(pygame.image.load(os.path.join('Personagens', 'desenho.png')),(scale_hero)),
                     pygame.transform.scale(pygame.image.load(os.path.join('Personagens', 'correndo 2.png')),(scale_hero)),
                     pygame.transform.scale(pygame.image.load(os.path.join('Personagens', 'correndo 3.png')),(scale_hero)),
                     pygame.transform.scale(pygame.image.load(os.path.join('Personagens', 'perfren1.png')),(scale_hero))
                     ]

            scale_bullet=[35,35]
            bullet_img =  pygame.transform.scale(pygame.image.load(os.path.join('Bullets', 'poder.png')), (scale_bullet))

            x = 100
            y = 395
            radius = 80
            vel = 5
            move_left = False
            move_right = False
            stepIndex = 0

            class Hero:
                def __init__(self, x, y):
                    # walk
                    self.x = x
                    self.y = y
                    self.velx = 6
                    self.vely = 15
                    self.face_right = True
                    self.face_left = False
                    self.ataque= False
                    self.stepIndex = 0
                    # Jump
                    self.jump = False
                    # Bullet
                    self.bullets = []
                    self.cool_down_count = 0
                    # Health
                    self.hitbox = (self.x, self.y, 64, 64)
                    self.health = 40
                    self.lives = 1
                    self.alive = True



                def move_hero(self, userInput):
                    if userInput[pygame.K_RIGHT] and self.x <= larguraTela - radius :
                        self.x += self.velx
                        self.face_right = True
                        self.face_left = False
                    elif userInput[pygame.K_LEFT] and self.x >= 0 :
                        self.x -= self.velx
                        self.face_right = False
                        self.face_left = True
                    else:
                        self.stepIndex = 0

                def draw(self, tela):
                    self.hitbox = (self.x, self.y, 78, 90)
                    pygame.draw.rect(tela, (255, 0, 0), (self.x + 30, self.y - 10, 40, 10))
                    if self.health >= 0:
                        pygame.draw.rect(tela, (0, 255, 0), (self.x + 30, self.y - 10, self.health, 10))
                    if self.stepIndex >= 16:
                        self.stepIndex = 0
                    if self.face_left and self.ataque == False:
                        tela.blit(left[self.stepIndex // 4], (self.x, self.y))
                        self.stepIndex += 1
                    if self.face_right and self.ataque == False:
                        tela.blit(right[self.stepIndex // 4], (self.x, self.y))
                        self.stepIndex += 1

                def jump_motion(self, userInput):
                    if userInput[pygame.K_SPACE] and self.jump is False:
                        jumpvar = pygame.mixer.Sound('Musicas/SFX_Jump_17.wav')
                        jumpvar.play()
                        self.jump = True
                    if self.jump:
                        self.y -= self.vely * 2
                        self.vely -= 1
                    if self.vely < -15:
                        self.jump = False
                        self.vely = 15

                def direction(self):
                    if self.face_right:
                        return 1
                    if self.face_left:
                        return -1

                def cooldown(self):
                    if self.cool_down_count >= 20:
                        self.cool_down_count = 0
                    elif self.cool_down_count > 0:
                        self.cool_down_count += 1

                def shoot(self):
                    self.hit()
                    self.cooldown()
                    self.tempo = 30
                    if (userInput[pygame.K_f] and self.cool_down_count == 0  ):

                        self.ataque = True
                        shootvar=pygame.mixer.Sound('Musicas/fogo.wav')
                        shootvar.play()

                        ataque =  pygame.image.load(os.path.join('Personagens', 'ataque.png'))

                        tela.blit(ataque,(100,100))

                        bullet = Bullet(self.x, self.y, self.direction())
                        self.bullets.append(bullet)
                        self.cool_down_count = 1

                    else:
                        if self.tempo> 0:
                            self.tempo-=1

                        else:
                            self.ataque= False
                            self.tempo= 30

                    for bullet in self.bullets:
                        bullet.move()

                        if bullet.off_screen():
                            self.bullets.remove(bullet)

                def hit(self):
                    for enemy in enemies:
                        for bullet in self.bullets:
                            if enemy.hitbox[0] < bullet.x < enemy.hitbox[0] + enemy.hitbox[2] and enemy.hitbox[
                                1] < bullet.y < enemy.hitbox[1] + enemy.hitbox[3]:

                                enemy.health -= 25
                                player.bullets.remove(bullet)



            class Bullet:
                def __init__(self, x, y, direction):

                    self.direction = direction
                    self.ataque=False

                    if direction ==1:
                        self.x = x + 60
                        self.y = y + 30

                    if direction ==-1:
                        self.x = x + 10
                        self.y = y + 30



                def draw_bullet(self):



                        tela.blit(bullet_img, (self.x, self.y))


                def move(self):
                    if self.direction == 1 :
                        self.x += 15
                    if self.direction == -1 :
                        self.x -= 15

                def off_screen(self):
                    return not (self.x >= 0 and self.x <= larguraTela)

            # INIMIGO ----------------------------------------------------------------------------------------
            scale_enimy=[100,100]
            left_enemy = [pygame.transform.scale(pygame.image.load(os.path.join('Inimigos', 'PINGUIM1.png')),(scale_enimy)),
                          pygame.transform.scale(pygame.image.load(os.path.join('Inimigos', 'PINGUIMATAQUE1.png')),(scale_enimy)),
                          pygame.transform.scale(pygame.image.load(os.path.join('Inimigos', 'PINGUIM1.png')),(scale_enimy)),
                          pygame.transform.scale(pygame.image.load(os.path.join('Inimigos', 'PINGUIMATAQUE1.png')),(scale_enimy))
                          ]
            right_enemy = [pygame.transform.scale(pygame.image.load(os.path.join('Inimigos', 'PINGUIM1.0.png')),(scale_enimy)),
                           pygame.transform.scale(pygame.image.load(os.path.join('Inimigos', 'PINGUIMATAQUE1.0.png')),(scale_enimy)),
                           pygame.transform.scale(pygame.image.load(os.path.join('Inimigos', 'PINGUIM1.0.png')),(scale_enimy)),
                           pygame.transform.scale(pygame.image.load(os.path.join('Inimigos', 'PINGUIMATAQUE1.0.png')),(scale_enimy))
                           ]

            class Enemy:
                def __init__(self, x, y, direction):
                    self.x = x
                    self.y = y
                    self.direction = direction
                    self.stepIndex = 0
                    # Health
                    self.hitbox = (self.x, self.y, 64, 64)
                    self.health = 40



                def step(self):
                    if self.stepIndex >= 32:
                        self.stepIndex = 0

                def draw(self, tela):
                    self.hitbox = (self.x, self.y, 78, 90)
                    pygame.draw.rect(tela, (255, 0, 0), (self.x + 20, self.y - 10, 40, 10))
                    if self.health >= 0:
                        pygame.draw.rect(tela, (0, 255, 0), (self.x + 20, self.y - 10, self.health, 10))
                    self.step()
                    if self.direction == left:
                        tela.blit(left_enemy[self.stepIndex // 8], (self.x, self.y))
                    if self.direction == right:
                        tela.blit(right_enemy[self.stepIndex // 8], (self.x, self.y))
                    self.stepIndex += 1

                def move(self):
                    self.hit()
                    if self.direction == left :
                        self.x -= 9
                    if self.direction == right :
                        self.x += 9

                def hit(self):
                    if player.hitbox[0] < enemy.x + 32 < player.hitbox[0] + player.hitbox[2] and player.hitbox[1] < enemy.y + 32 < player.hitbox[1] + player.hitbox[3]:
                        if player.health > 0:
                            player.health -= 1
                            if player.health == 0 and player.lives > 0:
                                player.lives -= 1
                                player.health = 40
                            elif player.health == 0 and player.lives == 0:
                                player.alive = False

                def off_screen(self):
                    return not (self.x >= -80 and self.x <= larguraTela + 30)

            # # # FUNÇÃO TELA ------------------------------------------------------------------------------
            def draw_game():

                tela.fill(BLACK)
                tela.blit(background, (0, 0))
                # Draw Playerf
                player.draw(tela)

                # Draw Bullets
                for bullet in player.bullets:
                    bullet.draw_bullet()
                # Draw Enemies
                for enemy in enemies:
                    enemy.draw(tela)
                # Player Health


                tempo= False
                if player.alive == False and tempo== False :


                    self.ultimakills= self.kills
                    tela.fill((0, 0, 0))
                    SCALE_FUNDO=[1000,500]
                    SCALE_FUNDO= pygame.transform.scale(pygame.image.load(os.path.join('Cenario/menu.jpeg')), (SCALE_FUNDO))
                    tela.blit(SCALE_FUNDO, (0,0))



                    font = pygame.font.Font('Fonte/PressStart2P-vaV7.ttf', 32)
                    text = font.render('GAME OVER! pressione R', True, (138, 47, 47))
                    textRect = text.get_rect()
                    textRect.center = (metadeLargura, metadeAltura)
                    tela.blit(text, textRect)
                    gameover = pygame.mixer.Sound('Musicas/gameover.wav')
                    gameover.play()
                    tempo = True

                    if gameover.play() == True and player.alive == False:
                        gameover.stop()


                    if self.kills > self.highkills:
                        self.highkills = self.kills
                        #self.draw_text('Novo Score de Recorde de mortes: ' + str(self.highkills), True,
                                            #(63, 255, 223))
                        #with open(path.join(self.dir, HS_FILE), 'w') as f:
                           # f.write(str(self.kills))


                font = pygame.font.Font('Fonte/PressStart2P-vaV7.ttf', 27)
                text = font.render('Mortos: ' + str(self.kills) + '  Vidas: ' + str(player.lives), True, (63, 255, 223))

                text2 = font.render('Última pontuação de mortes: ' + str(self.ultimakills) , True, (63, 255, 223))
                text3 = font.render('Recorde de mortes: ' + str(self.highkills), True,
                                    (63, 255, 223))



                tela.blit(text, (180, 20))
                tela.blit(text2, (180, 55))
                tela.blit(text3, (180, 90))


                if userInput[pygame.K_r]:
                    player.alive = True
                    player.lives = 1
                    player.health = 40
                    self.kills= 0



                pygame.display.update()

                CLOCK.tick(FPS)


            # ultimakills=0
            #highkills=kills
            #contador = kills
            player = Hero(250, 320)
            #kills = 0
            enemies = []







            # # # LOOP ------------------------------------------------------------------------
            run = True
            while run:

                # # # FECHAR TELA ------------------------------------------------------------
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                        if self.kills > self.highkills:
                            self.highkills = self.kills
                            text3 = font.render('Novo Score de Recorde de mortes: ' + str(self.highkills), True,
                                                (63, 255, 223))
                            with open('score.txt', 'w') as file:
                                file.write(str(self.highkills))
                # Input
                userInput = pygame.key.get_pressed()

                # shoot
                player.shoot()

                # Movement
                player.move_hero(userInput)
                player.jump_motion(userInput)

                # # # CONTROLE INIMIGOS
                if len(enemies) == 0:
                    rand_nr = random.randint(0, 1)
                    if rand_nr == 1:
                        enemy = Enemy(1010, 320, left)
                        enemies.append(enemy)
                    if rand_nr == 0:
                        enemy = Enemy(0, 320, right)
                        enemies.append(enemy)
                for enemy in enemies:
                    enemy.move()


                    if enemy.off_screen() or enemy.health <= 0:
                        enemies.remove(enemy)
                    if enemy.health <= 0:
                        self.kills += 1



                # Draw game in windows
                draw_game()

    #FIM


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y ): #Cor da letra, tamanho
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.BLUE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 130, 130)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('▶', 20, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Iniciar"
        self.startx, self.starty = self.mid_w, self.mid_h+80
        self.tutorialx, self.tutorialy = self.mid_w, self.mid_h + 120
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 160
        self.exitx, self.exity = self.mid_w, self.mid_h + 200
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):  # Aparência do Menu
        self.run_display = True

        menuprincipal = pygame.image.load('Cenario/menu.jpeg')
        menuprincipal2 = pygame.transform.scale(menuprincipal, (800, 600))


        pygame.mixer.music.load('Musicas/prologue.mp3')
        pygame.mixer.music.play(-1)

        while self.run_display:

            self.game.check_events()
            self.check_input()
            self.game.display.blit(menuprincipal2,(0,0)) # Preenchendo tela com imagem

            self.game.draw_text("Jogar", 20, self.startx, self.starty)
            self.game.draw_text("Como Jogar?", 20, self.tutorialx, self.tutorialy)
            self.game.draw_text("Créditos", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Sair", 20, self.exitx, self.exity)
            self.game.draw_text("Voltar: ESC", 10, self.mid_w - 200, self.mid_h + 260)
            self.game.draw_text("Avançar: Enter", 10, self.mid_w + 200, self.mid_h + 260)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):  # Movimentação do Cursor (Setinha)
        if self.game.DOWN_KEY:  # Usando seta pra baixo
            if self.state == 'Iniciar':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = 'Como Jogar?'
            elif self.state == 'Como Jogar?':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Créditos'
            elif self.state == 'Créditos':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Sair'
            elif self.state == 'Sair':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Iniciar'
        elif self.game.UP_KEY:  # Usando ceta pra cima
            if self.state == 'Iniciar':
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = 'Sair'
            elif self.state == 'Sair':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Créditos'
            elif self.state == 'Como Jogar?':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Iniciar'
            elif self.state == 'Créditos':
                self.cursor_rect.midtop = (self.tutorialx + self.offset, self.tutorialy)
                self.state = 'Como Jogar?'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Iniciar':
                self.game.playing = True
            elif self.state == 'Como Jogar?':
                self.game.curr_menu = self.game.options
            elif self.state == 'Créditos':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Sair':
                self.game.exiting = sys.exit()
            self.run_display = False


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.arrowx, self.arrowy = self.mid_w, self.mid_h + 0
        self.rightx, self.righty = self.mid_w, self.mid_h + 60
        self.leftx, self.lefty = self.mid_w, self.mid_h + 90
        self.shotx, self.shoty = self.mid_w, self.mid_h + 120
        self.shotz, self.shoth = self.mid_w, self.mid_h + 150

    def display_menu(self):

        self.run_display = True

        menuprincipal = pygame.image.load('Cenario/menu.jpeg')
        menuprincipal2 = pygame.transform.scale(menuprincipal, (800, 600))
        self.game.display.blit(menuprincipal2, (0, 0))  # Preenchendo tela com imagem

        while self.run_display:

            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.display.blit(menuprincipal2, (0, 0))  # Preenchendo tela com imagem
            self.game.draw_text('Tutorial', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 120)
            self.game.draw_text("Teclado", 30, self.arrowx, self.arrowy)
            self.game.draw_text("Andar para Direita:  →", 15, self.rightx, self.righty)
            self.game.draw_text("Andar para Esquerda: ←", 15, self.leftx, self.lefty)
            self.game.draw_text("Disparar Tiro:  F", 15, self.shotx, self.shoty)
            self.game.draw_text("Pular:  Barra de Espaço", 15, self.shotz, self.shoth)
            self.game.draw_text("Voltar: ESC", 10, self.mid_w - 200, self.mid_h + 260)
            self.game.draw_text("Avançar: Enter", 10, self.mid_w + 200, self.mid_h + 260)
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.START_KEY:
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        menuprincipal = pygame.image.load('Cenario/menu.jpeg')
        menuprincipal2 = pygame.transform.scale(menuprincipal, (800, 600))

        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(menuprincipal2, (0, 0))  # Preenchendo tela com imagem
            self.game.draw_text('CRIADORES DO SEAL ADVENTURE', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4 - 20)
            self.game.draw_text('CAIO GUIMARÃES SA SILVA', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('MARCO AURÉLIO SODRÉ', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.game.draw_text('SAMIRA DE BARROS CAVALCANTE FIGUEIREDO', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 50)
            self.game.draw_text('TAIGUARA TALES DA SILVA VITORINO', 15, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 70)
            self.game.draw_text("Voltar: ESC", 10, self.mid_w - 200, self.mid_h + 260)
            self.game.draw_text("Avançar: Enter", 10, self.mid_w + 200, self.mid_h + 260)
            self.blit_screen()

def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_ESCAPE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.UP_KEY = True

# INICIALIZADOR DO JOGO

g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
