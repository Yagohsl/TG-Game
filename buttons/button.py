import pygame

class Button():
    def __init__(self, text, pos, font, base_color, hover_color):
        self.text = text
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        
        # Renderiza o texto inicial e cria a hitbox perfeita baseada no tamanho das letras
        self.image = self.font.render(self.text, True, self.base_color)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def draw(self, surface):
        """Desenha o texto do botão na tela."""
        surface.blit(self.image, self.rect)

    def check_for_input(self, position):
        """Verifica se o mouse está em cima da hitbox usando o método nativo."""
        return self.rect.collidepoint(position)

    def update_color(self, position):
        """Muda a cor do texto caso o mouse esteja passando por cima (Efeito Hover)."""
        if self.rect.collidepoint(position):
            self.image = self.font.render(self.text, True, self.hover_color)
        else:
            self.image = self.font.render(self.text, True, self.base_color)