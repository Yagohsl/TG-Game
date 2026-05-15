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
        # 1. Exibe o menu
        menu_screen = MenuScreen()
        menu_screen.run()

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

        # 5. A tela de batalha
        battle_screen = BattleScreen(game_state)
        battle_screen.run()
