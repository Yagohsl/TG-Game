import pygame, sys
from data.screen import SCREEN
from buttons.button import Button
from data.colors import COR_HOVER, COR_TEXTO
from utils.fonts import get_font
from screens.credit_screen import credit_screen
from data.screen import SCREEN_HEIGHT, SCREEN_WIDTH

class MenuScreen:
    def __init__(self):
        self.menu_font = get_font(30)
        background = pygame.image.load("assets/images/menu/FUNDO MENU.png")
        self.background = pygame.transform.smoothscale(background, (1280,720))
        pygame.mixer.music.load("assets/audio/musicmenu.mp3")
        pygame.mixer.music.play(-1)


        self.play_button = Button(
            text="JOGAR", pos=(SCREEN_WIDTH // 2, 325), 
            font=self.menu_font, base_color=COR_TEXTO, hover_color=COR_HOVER
        )
        self.credits_button = Button(
            text="CRÉDITOS", pos=(SCREEN_WIDTH // 2, 425), 
            font=self.menu_font, base_color=COR_TEXTO, hover_color=COR_HOVER
        )
        self.exit_button = Button(
            text="SAIR", pos=(SCREEN_WIDTH // 2, 525), 
            font=self.menu_font, base_color=COR_TEXTO, hover_color=COR_HOVER
        )
      

    def run(self):
        clock = pygame.time.Clock()
        SCALED_BACKGROUND = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        while True:
            SCREEN.blit(SCALED_BACKGROUND, (0, 0))
            mouse_pos = pygame.mouse.get_pos()

            for button in [self.play_button, self.credits_button, self.exit_button]:
                button.update_color(mouse_pos)
                button.draw(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.check_for_input(mouse_pos):
                        return 
                    if self.credits_button.check_for_input(mouse_pos):
                        credit_screen()
                    if self.exit_button.check_for_input(mouse_pos):
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()


            pygame.display.update()
            clock.tick(60)  # controla 60 FPS