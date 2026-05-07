import pygame, sys
from data.screen import SCREEN, VERSUS_IMAGE, VICTORY_IMAGE, draw_health_bar, SCREEN_WIDTH, SCREEN_HEIGHT, draw_power_bar
from utils.draw import draw_text
from utils.fonts import get_font
from data.colors import WHITE

class BattleScreen:
    def __init__(self, game_state):
        context = game_state
        self.fighter1 = context["player1"]
        self.fighter2 = context["player2"]
        self.background = context["selected_map"]
        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]
        self.round_over = False
        self.round_over_cooldown = 2000
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.play(-1)
        
    def run(self):
        SCALED_BACKGROUND = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()
        while True:
            SCREEN.blit(SCALED_BACKGROUND, (0, 0))

            clock.tick(70)

            #icones
            SCREEN.blit(self.fighter1.icon, (20, 5))
            SCREEN.blit(self.fighter2.icon, (890, 5))
            SCREEN.blit(VERSUS_IMAGE, (410, 40))

            #status dos jogadores
            draw_health_bar(self.fighter1.health, 20, 100, 1)
            draw_health_bar(self.fighter2.health, 580, 100, 2)

            #status dos jogadores
            draw_power_bar(self.fighter1.special_energy, 20, 120, 1)
            draw_power_bar(self.fighter2.special_energy, 680, 120, 2)

            #inserindo nomes
            draw_text(self.fighter1.name, get_font(25), WHITE, 110, 50)
            draw_text(self.fighter2.name, get_font(25), WHITE, 580, 50)
            draw_text("p1: " + str(self.score[0]), get_font(25), WHITE, 350, 130)
            draw_text("p2: " + str(self.score[1]), get_font(25), WHITE, 580, 130)

            #recontagem
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
                SCREEN.blit(VICTORY_IMAGE, (360, 150))

                #acaba jogo
                if self.score[0] == 2 or self.score[1] == 2:
                    if pygame.time.get_ticks() - self.round_over_time > self.round_over_cooldown:
                        self.round_over = True
                        self.round_over_time = pygame.time.get_ticks()
                        SCREEN.blit(VICTORY_IMAGE, (360, 150))
                        return

                if pygame.time.get_ticks() - self.round_over_time > self.round_over_cooldown:
                    self.round_over = False
                    self.intro_count = 3
                    self.fighter1.reset()
                    self.fighter2.reset()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.pause()
                        return
                    if event.key == pygame.K_e:
                        self.fighter1.defense_key_held = True
                    if event.key == pygame.K_KP_3:
                        self.fighter2.defense_key_held = True
                        #defesa
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_e:
                        self.fighter1.defense_key_held = False
                    if event.key == pygame.K_KP_3:
                        self.fighter2.defense_key_held = False

            pygame.display.update()
