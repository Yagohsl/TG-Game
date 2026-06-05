import pygame, os

# Defina o diretório base do jogo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Pega o diretório do script atual
ASSETS_DIR = os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters')  # Caminho para as imagens

# Dados dos personagens
AVAILABLE_CHARACTERS = {

    #Placeholder Personagem Principal

    "Hero": {
        "name": "Herói",
        "animation_steps": [1, 5, 2, 1, 4, 4, 1, 1, 1, 1],
        "sheet_path": pygame.image.load(os.path.join(ASSETS_DIR, 'hero.png')),
        "icon": pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters', 'icons', 'hero_icon.png')), (512, 512)),       
        "data": [64, 3, [22, 8]]
    },
    "Anxiety": {
        "name": "Ansiedade",
        "animation_steps": [4, 4, 3, 2, 3, 2, 1, 1, 1, 1],
        "sheet_path": pygame.image.load(os.path.join(ASSETS_DIR, 'ansiedade.png')),
        "icon": pygame.transform.scale(pygame.image.load(os.path.join(BASE_DIR, '..', 'assets', 'images', 'jogo', 'fighters', 'icons', 'ansiedade_icon.png')), (512, 512)),       
        "data": [64, 4, [22, 13]]
    }
}
