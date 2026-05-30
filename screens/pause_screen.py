import pygame
import sys
from buttons.button import Button
from utils.draw import draw_text
from utils.fonts import get_font
from data.colors import WHITE  # Utilizando WHITE como base, altere para COR_TEXTO se preferir
from data.screen import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT

class PauseScreen:
    def __init__(self):
        # Configura o botão de Sair centralizado
        self.exit_button = Button(
            text="SAIR DO JOGO", 
            pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), 
            font=get_font(25), 
            base_color=WHITE, 
            hover_color=(255, 100, 0) # Laranja de alerta para o hover
        )

    def draw(self):
        """Renderiza a sobreposição semitransparente e os elementos de texto/botões."""
        # 1. Cria uma camada de sombra semitransparente por cima do frame congelado da batalha
        pausa_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pausa_overlay.fill((0, 0, 0, 160))
        SCREEN.blit(pausa_overlay, (0, 0))
        
        # 2. Desenha o Título de Pausa
        draw_text("JOGO PAUSADO", get_font(35), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
        draw_text("Pressione ESC para Retornar", get_font(20), WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, center=True)

        # 3. Atualiza a cor e desenha o botão de Sair
        mouse_pos = pygame.mouse.get_pos()
        self.exit_button.update_color(mouse_pos)
        self.exit_button.draw(SCREEN)

    def handle_event(self, event, battle_screen):
        """Gerencia os eventos específicos da tela de pausa."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # Despausa o jogo e retoma a música
                battle_screen.paused = False
                pygame.mixer.music.unpause()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique com o botão esquerdo
                if self.exit_button.rect.collidepoint(event.pos):
                    return "EXIT"  # Sinaliza que o jogador escolheu sair
                    
        return None