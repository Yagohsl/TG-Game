import pygame
from fighters.fighter import Fighter

class FighterPlayer (Fighter):
    def __init__(self,name, animation_steps, sprite_sheet, icon, data, player, x, y, flip):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps)
        self.name = name
        icon = pygame.transform.scale(icon, (icon.get_width() // 5, icon.get_height() // 5))
        self.icon = icon


    def getName(self):
        return self.name
   
    def getIcon(self):
        return self.icon