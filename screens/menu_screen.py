import pygame, sys
from data.screen import SCREEN
from buttons.button import Button
from screens.credit_screen import credit_screen
from data.screen import SCREEN_HEIGHT, SCREEN_WIDTH

class MenuScreen:
    def __init__(self):
        self.play_button = Button(image=pygame.image.load("assets/images/menu/jogar.png"), pos=(850, 200))
        self.credits_button = Button(image=pygame.image.load("assets/images/menu/creditos.png"), pos=(850, 325))
        self.exit_button = Button(image=pygame.image.load("assets/images/menu/sair.png"), pos=(850, 450))
        background = pygame.image.load("assets/images/menu/FUNDO MENU.png")
        self.background = pygame.transform.smoothscale(background, (1000,600))
        pygame.mixer.music.load("assets/audio/musicmenu.mp3")
        pygame.mixer.music.play(-1)

      

    def run(self):
        clock = pygame.time.Clock()
        SCALED_BACKGROUND = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        while True:
            SCREEN.blit(SCALED_BACKGROUND, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            for button in [self.play_button, self.credits_button, self.exit_button]:
                button.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.checkForInput(mouse_pos):
                        return 
                    if self.credits_button.checkForInput(mouse_pos):
                        credit_screen()
                    if self.exit_button.checkForInput(mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()


            pygame.display.update()
            clock.tick(60)  # controla 60 FPS