import pygame, os

# Defina o diretório base do jogo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Pega o diretório do script atual
ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters')  # Caminho para as imagens

# Dados dos personagens
AVAILABLE_CHARACTERS = {
    #Placeholder Personagem Principal
    "Anakin": {
        "name": "Anakin Skywalker",
        "animation_steps": [10, 8, 1, 8, 8, 3, 7, 5, 3, 8],
        "sheet_path": pygame.image.load(os.path.join(ASSETS_DIR, 'fighterAnakin.png')),
        "icon": pygame.image.load(os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters', 'icons', 'anakin.png')),
        "data": [162, 3, [72, 40]]
    },
    #Placeholder Boss1
    "General": {
        "name": "General Grievous",
        "animation_steps": [3, 8, 1, 8, 8, 3, 7, 5, 3, 8],
        "sheet_path": pygame.image.load(os.path.join(ASSETS_DIR, 'general.png')),
        "icon": pygame.image.load(os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters', 'icons', 'general_grevious_icon.png')),
        "data": [162, 3, [72, 40]]
    },
    "Anxiety": {
        "name": "Anxiety",
        "animation_steps": [4, 4, 3, 2, 1, 1, 1, 1, 1, 1],
        "sheet_path": pygame.image.load(os.path.join(ASSETS_DIR, 'ansiedade.png')),
        "icon": pygame.image.load(os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters', 'icons', 'general_grevious_icon.png')),
        "data": [64, 4, [22, 19]]
    }
}