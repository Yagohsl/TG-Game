import pygame, sys
from data.Maps import MAPS
from data.colors import WHITE, YELLOW
from data.screen import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH

from utils.fonts import get_font
from utils.draw import draw_text

def draw_text_centered(text, font, color, y):
    img = font.render(text, True, color)
    x = (SCREEN_WIDTH - img.get_width()) // 2
    SCREEN.blit(img, (x, y))

def map_select_screen(game_state):
    background_original = pygame.image.load("assets/images/menu/tela_fundo.jpg")
    background = pygame.transform.scale(background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
    map_images = {key: pygame.image.load(data["imagem"]) for key, data in MAPS.items()}
    
    pygame.time.wait(300)  # Espera curta para evitar cliques anteriores

    # Posições fixas para exibir os mapas
    positions = [
        (230, SCREEN_HEIGHT-400), (770, SCREEN_HEIGHT-400),(SCREEN_WIDTH//2, 450)
    ]

    while True:
        SCREEN.blit(background, (0, 0))
        draw_text_centered("Selecione o Mapa", get_font(30), WHITE, 50)
        mouse_pos = pygame.mouse.get_pos()

        rects = []
        for idx, (key, data) in enumerate(MAPS.items()):
            if idx >= len(positions):
                break  # Evita ultrapassar o número de posições disponíveis

            x, y = positions[idx]
            image_scaled = pygame.transform.scale(map_images[key], (400, 200))
            rect = image_scaled.get_rect(center=(x, y))
            SCREEN.blit(image_scaled, rect.topleft)

            name_text = get_font(20).render(data["nome"], True, WHITE)
            name_rect = name_text.get_rect(center=(rect.centerx, rect.bottom + 15))
            SCREEN.blit(name_text, name_rect)

            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(SCREEN, YELLOW, rect, 3)

            rects.append((rect, key))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, key in rects:
                    if rect.collidepoint(event.pos):
                        pygame.time.wait(300)
                        game_state["selected_map"] = map_images[key]
                        return

        pygame.display.update()


