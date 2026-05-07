import pygame, sys

from buttons.button import Button
from data.colors import WHITE
from data.screen import SCREEN, SCREEN_WIDTH
from utils.draw import draw_text
from utils.fonts import get_font

def credit_screen():
    background = pygame.image.load("assets/images/menu/FUNDO CREDITO.png")
    exit_button = Button(image=pygame.image.load("assets/images/menu/sair.png"), pos=(SCREEN_WIDTH//2, 450))
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.blit(background, (0, 0))
        draw_text("joão vitor branco colombo", get_font(28), WHITE, 245, 55)
        draw_text("gustavo neves buzois", get_font(28), WHITE, 245, 95)
        exit_button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.checkForInput(mouse_pos):
                        return
        pygame.display.update()