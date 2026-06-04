import pygame, os

# Defina o diretório base do jogo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Pega o diretório do script atual
ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters')  # Caminho para as imagens

# Dados dos personagens
AVAILABLE_CHARACTERS = {

    #Placeholder Personagem Principal
    "Mestre Diogo": {
                "name": "Mestre Diogo Robles",
                "animation_steps": [1, 5, 1, 1, 1, 1, 1, 1, 1, 1],
                "sheet_path": pygame.image.load("assets/images/jogo/fighters/hero.png"),
                "icon": pygame.image.load("assets/images/jogo/fighters/icons/mestre_diogo_icon.png"),
                "data": [64, 3, [22, 13]]
            },
    "Hero": {
        "name": "Herói",
        "animation_steps": [1, 5, 2, 1, 1, 1, 1, 1, 1, 1],
        "sheet_path": pygame.image.load(os.path.join(ASSETS_DIR, 'hero.png')),
        "icon": pygame.image.load(os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters', 'icons', 'mestre_diogo_icon.png')),
        "data": [64, 3, [22, 8]]
    },
    "Anxiety": {
        "name": "Ansiedade",
        "animation_steps": [4, 4, 3, 2, 3, 2, 1, 1, 1, 1],
        "sheet_path": pygame.image.load(os.path.join(ASSETS_DIR, 'ansiedade.png')),
        "icon": pygame.image.load(os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters', 'icons', 'general_grevious_icon.png')),
        "data": [64, 4, [22, 13]]
    }
}
