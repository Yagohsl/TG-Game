import pygame
from manager.run_game import run_game

pygame.init()
pygame.display.set_caption("Star Jedi Battleforce")
pygame.display.set_icon(pygame.image.load("assets/images/icon/icone.ico"))
run_game()