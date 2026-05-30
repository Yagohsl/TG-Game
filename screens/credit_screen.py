import pygame, sys

from buttons.button import Button
from data.colors import COR_HOVER, COR_TEXTO
from data.screen import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.draw import draw_text
from utils.fonts import get_font

def credit_screen():
    background = pygame.image.load("assets/images/menu/FUNDO MENU.png")
    exit_button = Button(text="SAIR", pos=(1280 // 2, 525),font=get_font(30), base_color=COR_TEXTO, hover_color=COR_HOVER)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        SCALED_BACKGROUND = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        SCREEN.blit(SCALED_BACKGROUND, (0, 0))

        draw_text("Autores", get_font(32), COR_TEXTO, SCREEN_WIDTH//2, 50, center=True)

        draw_text("Yago Henrique dos Santos Lima", get_font(25), COR_TEXTO, SCREEN_WIDTH//2, 150, center=True)
        draw_text("Amon Lucena", get_font(25), COR_TEXTO, SCREEN_WIDTH//2, 200, center=True)
        
        draw_text("Controles", get_font(32), COR_TEXTO, SCREEN_WIDTH//2, 290, center=True)

        draw_text("Movimentos:", get_font(25), COR_TEXTO, 100, 340) 
        draw_text("A   D", get_font(25), COR_TEXTO, 420, 340)

        draw_text("Pular:", get_font(25), COR_TEXTO, 100, 390)
        draw_text("Espaço", get_font(25), COR_TEXTO, 420, 390)

        draw_text("Ataques:", get_font(25), COR_TEXTO, 700, 340)
        draw_text("J   K", get_font(25), COR_TEXTO, 1020, 340)

        draw_text("Esquiva:", get_font(25), COR_TEXTO, 700, 390)
        draw_text("L", get_font(25), COR_TEXTO, 1020, 390)



        exit_button.update_color(mouse_pos)
        exit_button.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button.check_for_input(mouse_pos):
                        return
        pygame.display.update()