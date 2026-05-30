import pygame
from data.screen import SCREEN

class DialogueBox:
    def __init__ (self, screen, font, x= 50, y = 520, width = 1180, height = 160):
        self.screen = screen
        self.font = font

        self.rect = pygame.Rect(x,y, width, height)

        self.dialogues = []
        self.current_index = 0
        self.active = False

    def start_dialogue(self, dialogue_list):
        self.dialogues = dialogue_list
        self.current_index = 0
        self.active = True

    def next_dialogue(self):
        self.current_index += 1
        if self.current_index >= len(self.dialogues):
            self.active = False
            return False
        return True
    
    def _wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "

            if self.font.size(test_line)[0] <max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines

    def draw(self):
        if not self.active:
            return

        # 1. Desenhar o fundo do retângulo (Preto com borda branca pixel art)
        pygame.draw.rect(self.screen, (20, 20, 20), self.rect)  # Fundo escuro
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect, 4)  # Borda branca

        # Pegar os dados do diálogo atual
        speaker_icon, text = self.dialogues[self.current_index]

        # 2. Desenhar a imagem do locutor na esquerda (dentro do balão)
        icon_x = self.rect.x + 20
        icon_y = self.rect.y + 15
        
        # Redimensiona o ícone se ele for maior que o espaço disponível (ex: 128x128)
        if speaker_icon.get_height() > (self.rect.height - 30):
            speaker_icon = pygame.transform.scale(speaker_icon, (130, 130))
            
        self.screen.blit(speaker_icon, (icon_x, icon_y))

        # 3. Renderizar o texto com quebra de linha à direita da imagem
        # O texto começará após a imagem (X do ícone + largura + margem)
        text_start_x = icon_x + speaker_icon.get_width() + 20
        text_start_y = self.rect.y + 25
        max_text_width = self.rect.width - speaker_icon.get_width() - 60

        # Aplica a quebra automática
        lines = self._wrap_text(text, max_text_width)

        # Desenha linha por linha com espaçamento vertical
        for i, line in enumerate(lines):
            line_surface = self.font.render(line.strip(), True, (255, 255, 255))
            self.screen.blit(line_surface, (text_start_x, text_start_y + (i * 30)))
            
        # Pequeno indicador piscante/aviso no canto inferior direito para "Avançar"
        adv_text = self.font.render("[ESPAÇO]", True, (255, 165, 0)) # Laranja (cor de alerta)
        self.screen.blit(adv_text, (self.rect.right - 130, self.rect.bottom - 35))