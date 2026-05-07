import pygame
import sys
from data.screen import SCREEN, SCREEN_HEIGHT, SCREEN_WIDTH
from data.colors import WHITE, YELLOW
from data.available_characters import AVAILABLE_CHARACTERS
from fighters.fighterPlayer import FighterPlayer
from utils.fonts import get_font
from utils.draw import draw_text

def draw_text_centered(text, font, color, y):
    img = font.render(text, True, color)
    x = (SCREEN_WIDTH - img.get_width()) // 2
    SCREEN.blit(img, (x, y))

def character_select(game_state):
    selected = []

    background_original = pygame.image.load("assets/images/menu/tela_fundo.jpg")
    background = pygame.transform.scale(background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))
    positions = [
        (170, 200), (500, 200),(800, 200),
        (320, 400), (670, 400)
    ]

    while True:
        SCREEN.blit(background, (0, 0))
        draw_text_centered("Selecione os Personagens (Clique nos dois)", get_font(25), WHITE, 40)
        mouse_pos = pygame.mouse.get_pos()

        rects = []  # Para armazenar posições clicáveis com chave

        for idx, (key, data) in enumerate(AVAILABLE_CHARACTERS.items()):
            if idx >= len(positions):
                break

            x, y = positions[idx]
            image_scaled = pygame.transform.scale(data["icon"], (150, 175))
            rect = image_scaled.get_rect(center=(x, y))
            SCREEN.blit(image_scaled, rect.topleft)

            name_text = get_font(20).render(data["name"], True, WHITE)
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
                        selected.append(key)
                        pygame.time.wait(300)


        if len(selected) == 2:
            # Construindo lutadores
            char_config = AVAILABLE_CHARACTERS[selected[0]]
            game_state["player1"] = FighterPlayer(
                name=char_config["name"], animation_steps=char_config["animation_steps"],
                sprite_sheet=char_config["sheet_path"], icon=char_config["icon"],
                data=char_config["data"], player=1, x=200, y=310, flip=False)

            char_config = AVAILABLE_CHARACTERS[selected[1]]
            game_state["player2"] = FighterPlayer(
                name=char_config["name"], animation_steps=char_config["animation_steps"],
                sprite_sheet=char_config["sheet_path"], icon=char_config["icon"],
                data=char_config["data"], player=2, x=700, y=310, flip=True)

            return  # Avança para a próxima tela

        pygame.display.update()
