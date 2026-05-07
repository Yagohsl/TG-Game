import pygame, sys
from data.screen import SCREEN
from buttons.button import Button
from screens.credit_screen import credit_screen

class MenuScreen:
    def __init__(self):
        self.play_button = Button(image=pygame.image.load("assets/images/menu/jogar.png"), pos=(850, 200))
        self.credits_button = Button(image=pygame.image.load("assets/images/menu/creditos.png"), pos=(850, 325))
        self.exit_button = Button(image=pygame.image.load("assets/images/menu/sair.png"), pos=(850, 450))
        background = pygame.image.load("assets/images/menu/FUNDO MENU.png")
        self.background = pygame.transform.smoothscale(background, (1000,600))
        pygame.mixer.music.load("assets/audio/musicmenu.mp3")
        pygame.mixer.music.play(-1)

        self.cheat_code = [pygame.K_UP, pygame.K_UP, pygame.K_DOWN, pygame.K_DOWN,
                           pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_RIGHT,
                           pygame.K_b, pygame.K_a]
        self.cheat_input = []
        self.secret_unlocked = False

        # Variáveis para o efeito de piscar
        self.blinking = False
        self.blink_alpha = 0
        self.blink_direction = 1  # 1 = aumentando alpha, -1 = diminuindo
        self.blink_duration = 60  # total de frames para o piscar (~1 segundo se 60 FPS)
        self.blink_timer = 0

        # Superfície para efeito de brilho (preta com alpha variável)
        self.blink_surface = pygame.Surface(SCREEN.get_size())
        self.blink_surface.fill((255, 255, 255))  # branco para efeito de claridade (pode mudar)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            SCREEN.blit(self.background, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            for button in [self.play_button, self.credits_button, self.exit_button]:
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.checkForInput(mouse_pos):
                        return self.secret_unlocked  # Retorna se o personagem secreto foi desbloqueado
                    if self.credits_button.checkForInput(mouse_pos):
                        credit_screen()
                    if self.exit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.cheat_input.append(event.key)
                    if len(self.cheat_input) > len(self.cheat_code):
                        self.cheat_input.pop(0)
                    if self.cheat_input == self.cheat_code:
                        self.secret_unlocked = True
                        self.blinking = True  # ativa o efeito piscar
                        self.blink_alpha = 0
                        self.blink_direction = 1
                        self.blink_timer = 0

            # Se estiver piscando, atualiza o efeito
            if self.blinking:
                self.blink_alpha += self.blink_direction * 10  # velocidade do fade
                if self.blink_alpha >= 150:
                    self.blink_alpha = 150
                    self.blink_direction = -1
                elif self.blink_alpha <= 0:
                    self.blink_alpha = 0
                    self.blink_direction = 1
                    self.blink_timer += 1

                self.blink_surface.set_alpha(self.blink_alpha)
                SCREEN.blit(self.blink_surface, (0, 0))

                if self.blink_timer >= 3:  # piscar 3 vezes
                    self.blinking = False

            pygame.display.update()
            clock.tick(60)  # controla 60 FPS