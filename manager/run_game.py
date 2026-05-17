import pygame
from data.available_characters import AVAILABLE_CHARACTERS 
from screens.menu_screen import MenuScreen
from screens.battle_screen import BattleScreen
from bosses.bossAnxiety import BossAnxiety
from fighters.fighterPlayer import FighterPlayer
from data.screen import SCREEN_HEIGHT, SCREEN_WIDTH


def run_game():
    game_state = {
        "player1": None,
        "player2": None,
        "selected_map": None
    }

    while True:
        #Exibe o menu
        menu_screen = MenuScreen()
        menu_screen.run()

        #Personagem Principal
        player_data = AVAILABLE_CHARACTERS["Anakin"]
        game_state["player1"] = FighterPlayer(
            player_data["name"],
            player_data["animation_steps"],
            player_data["sheet_path"],
            player_data["icon"],
            player_data["data"],
            1, 380, 430, False
        )

        #Forçar o Player 2 a ser o Boss (Exemplo usando o General como Boss)
        boss_data = AVAILABLE_CHARACTERS["Anxiety"]
        game_state["player2"] = BossAnxiety(
            boss_data["name"],
            boss_data["animation_steps"],
            boss_data["sheet_path"],
            boss_data["icon"],
            boss_data["data"],
            2, 1000, 430, True
        )

        #Tela de batalha
        battle_screen = BattleScreen(game_state)
        battle_screen.run()
