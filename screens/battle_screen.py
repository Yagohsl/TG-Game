import pygame, sys
from data.screen import SCREEN, VICTORY_IMAGE, draw_health_bar, SCREEN_WIDTH, SCREEN_HEIGHT, draw_power_bar
from utils.draw import draw_text
from utils.fonts import get_font
from data.colors import WHITE
from screens.dialog_screen import DialogueBox
from screens.pause_screen import PauseScreen

class BattleScreen:
    def __init__(self, game_state):
        context = game_state
        self.fighter1 = context["player1"]
        self.fighter2 = context["player2"]
        self.background = pygame.image.load("assets/images/jogo/maps/background6.png") #escolhendo mapa
        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]
        self.round_over = False
        self.round_over_cooldown = 2000
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.play(-1)
        
        self.paused = False
        self.pause_screen = PauseScreen()


        self.font_dialogo = get_font(28) 
        self.dialogue_box = DialogueBox(SCREEN, self.font_dialogo)

        self.player_icon = game_state["player1"].icon
        self.boss_icon = game_state["player2"].icon

        # Configurar a lista de falas da introdução da batalha
        self.dialogos_da_luta = [
            (self.player_icon, "Eu consigo fazer isso... Só preciso manter o foco e respirar fundo."),
            (self.boss_icon, "E se tudo der errado? Você não se preparou o suficiente. Desista!"),
            (self.player_icon, "Não vou me render aos pensamentos intrusivos. Vamos resolver isso agora!")
        ]
        self.dialogue_box.start_dialogue(self.dialogos_da_luta)
        
    def run(self):
        SCALED_BACKGROUND = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()
        sombra = pygame.Surface(SCALED_BACKGROUND.get_size(), pygame.SRCALPHA)
        sombra.fill((0,0,0,150))
        while True:
            SCREEN.blit(SCALED_BACKGROUND, (0, 0))
            SCREEN.blit(sombra, (0,-100))

            clock.tick(70)

            #icone
            SCREEN.blit(self.fighter1.icon, (40, 5))

            #status dos jogadores
            draw_health_bar(self.fighter1.health, 40, 100, 1)
            draw_health_bar(self.fighter2.health, 240, 680, 2)

            #status dos jogadores
            draw_power_bar(self.fighter1.special_energy, 40, 120, 1)
            #draw_power_bar(self.fighter2.special_energy, 680, 120, 2)

            #inserindo nomes
            draw_text(self.fighter1.name, get_font(25), WHITE, 130, 50)
            draw_text(self.fighter2.name, get_font(25), WHITE, SCREEN_WIDTH//2, 650, center = True)

            if not self.paused:
                if hasattr(self.fighter2, 'draw_projectiles'):
                    self.fighter2.draw_projectiles(SCREEN)

                    
                #recontagem
                if not self.dialogue_box.active:
                    if self.intro_count <= 0:
                        self.fighter1.move(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN, self.fighter2, self.round_over)
                        self.fighter2.move(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN, self.fighter1, self.round_over)
                    else:
                        #temporizador de contagem
                        draw_text(str(self.intro_count), get_font(40), WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                        if (pygame.time.get_ticks() - self.last_count_update) >= 1000:
                            self.intro_count -= 1
                            self.last_count_update = pygame.time.get_ticks()

                # Atualiza lógica dos personagens aqui (a implementar)
                self.fighter1.update()
                self.fighter2.update()

            self.fighter1.draw(SCREEN)
            self.fighter2.draw(SCREEN)
                  # 4. Desenha o balão de diálogo POR CIMA de tudo (se ele estiver ativo)
            if self.dialogue_box.active:
                self.dialogue_box.draw()

            if not self.paused:
                #verificando derrota
                if self.round_over == False:
                    if self.fighter1.alive == False:
                        self.score[1] += 1
                        self.round_over = True
                        self.round_over_time = pygame.time.get_ticks()
                    elif self.fighter2.alive == False:
                        self.score[0] += 1
                        self.round_over = True
                        self.round_over_time = pygame.time.get_ticks()
                else:
                    #exibir vitoria
                    SCREEN.blit(VICTORY_IMAGE, ((SCREEN_WIDTH - VICTORY_IMAGE.get_width())//2, 150))

                    #acaba jogo
                    if self.score[0] == 1:
                        if pygame.time.get_ticks() - self.round_over_time > self.round_over_cooldown:
                            self.round_over = True
                            self.round_over_time = pygame.time.get_ticks()
                            #exibir vitoria
                            SCREEN.blit(VICTORY_IMAGE, ((SCREEN_WIDTH - VICTORY_IMAGE.get_width())//2, 150))  
                            return

                    if pygame.time.get_ticks() - self.round_over_time > self.round_over_cooldown:
                        self.round_over = False
                        self.intro_count = 3
                        self.fighter1.reset()
                        self.fighter2.reset()

            if self.paused:
                self.pause_screen.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Se o jogo ESTIVER pausado, repassa o evento para a PauseScreen tratar
                if self.paused:
                    acao = self.pause_screen.handle_event(event, self)
                    if acao == "EXIT":
                        return  # Interrompe a luta e retorna ao run_game.py (Menu Inicial)

                # Se o jogo NÃO estiver pausado, processa as teclas de combate normalmente
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.paused = True
                            pygame.mixer.music.pause() # Pausa a música de fundo de forma limpa
                        
                        if self.dialogue_box.active and event.key == pygame.K_SPACE:
                            self.dialogue_box.next_dialogue()
                        if event.key == pygame.K_e:
                            self.fighter1.defense_key_held = True
                        if event.key == pygame.K_KP_3:
                            self.fighter2.defense_key_held = True

                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_e:
                            self.fighter1.defense_key_held = False
                        if event.key == pygame.K_KP_3:
                            self.fighter2.defense_key_held = False

            pygame.display.update()
