import pygame
from data.colors import BLUE, RED,WHITE, YELLOW

SCREEN_WIDTH = 1000
SCREEN_HEIGHT =  600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60

VERSUS_IMAGE = pygame.image.load("assets/images/jogo/icons/versus.png").convert_alpha()
VERSUS_IMAGE= pygame.transform.scale(VERSUS_IMAGE, (VERSUS_IMAGE.get_width() // 3, VERSUS_IMAGE.get_height() // 3))
VICTORY_IMAGE = pygame.image.load("assets/images/jogo/icons/victory.png").convert_alpha()


def draw_health_bar(health, x, y, player):
    ratio = health / 100
    pygame.draw.rect(SCREEN, WHITE, (x - 4, y - 4, 408, 38))  # Borda
    pygame.draw.rect(SCREEN, RED, (x, y, 400, 30))            # Fundo vermelho

    if player == 1:
        # Barra de vida invertida (direita para esquerda)
        width = 400 * ratio
        pygame.draw.rect(SCREEN, YELLOW, (x + 400 - width, y, width, 30))
    else:
        # Barra de vida normal (esquerda para direita)
        pygame.draw.rect(SCREEN, YELLOW, (x, y, 400 * ratio, 30))

def draw_power_bar(power, x, y, player):
    ratio = power / 100
    pygame.draw.rect(SCREEN, WHITE, (x - 4, y - 4, 308, 33))
    pygame.draw.rect(SCREEN, (134, 207, 248), (x, y, 300, 25))
    if player == 1:
        # Barra de vida invertida (direita para esquerda)
        width = 300 * ratio
        pygame.draw.rect(SCREEN, BLUE, (x + 300 - width, y, width, 25))
    else:
        # Barra de vida normal (esquerda para direita)
        pygame.draw.rect(SCREEN, BLUE, (x, y, 300 * ratio, 25))