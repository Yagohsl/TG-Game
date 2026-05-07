import pygame
from data.available_characters import AVAILABLE_CHARACTERS  # Certifique-se de importar o dicionário AVAILABLE_CHARACTERS
from screens.menu_screen import MenuScreen
from screens.character_select import character_select
from screens.map_select import map_select_screen
from screens.battle_screen import BattleScreen
from bosses.boss import Boss

def run_game():
    game_state = {
        "player1": None,
        "player2": None,
        "selected_map": None
    }

    while True:
        # 1. Exibe o menu e verifica se o personagem secreto foi desbloqueado
        menu_screen = MenuScreen()
        secret_character_enabled = menu_screen.run()

        # 2. Se o cheat foi ativado, adiciona o personagem secreto (somente uma vez)
        if secret_character_enabled and "Mestre Diogo" not in AVAILABLE_CHARACTERS:
            AVAILABLE_CHARACTERS["Mestre Diogo"] = {
                "name": "Mestre Diogo Robles",
                "animation_steps": [5, 12, 1, 8, 8, 3, 7, 5, 3, 8],
                "sheet_path": pygame.image.load("assets/images/jogo/fighters/mestre_diogo.png"),
                "icon": pygame.image.load("assets/images/jogo/fighters/icons/mestre_diogo_icon.png"),
                "data": [162, 3, [72, 40]]
            }

        # 3. Vai para a seleção de personagens
        character_select(game_state)

        # 4. Forçar o Player 2 a ser o Boss (Exemplo usando o General como Boss)
        boss_data = AVAILABLE_CHARACTERS["General"]
        game_state["player2"] = Boss(
            boss_data["name"],
            boss_data["animation_steps"],
            boss_data["sheet_path"],
            boss_data["icon"],
            boss_data["data"],
            2, 700, 310, True
        )


        # 5. Seleção do mapa
        map_select_screen(game_state)

        # 6. A tela de batalha
        battle_screen = BattleScreen(game_state)
        battle_screen.run()
