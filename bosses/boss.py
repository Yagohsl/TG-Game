import pygame
import random
from fighters.fighterPlayer import FighterPlayer


class Boss(FighterPlayer):
    def __init__(self, name, animation_steps, sprite_sheet, icon, data, player, x, y, flip):
        # Repassa todos os parâmetros para o FighterPlayer
        super().__init__(name, animation_steps, sprite_sheet, icon, data, player, x, y, flip)

        # Configurações de física adaptáveis
        self.speed = 6
        self.gravity = 2

        # Variáveis de controle da IA
        self.decision_timer = 0
        self.decision_cooldown = 30  # O Boss "pensa" a cada 30 frames
        self.current_action = "idle"

    def update_ai(self, target, round_over):
        """Gerencia exclusivamente a máquina de estados e decisões da IA."""
        dx = 0

        # Só toma decisões se não estiver no meio de um ataque, estiver vivo e o round rolando
        if not self.attacking and self.alive and not round_over:
            distancia_x = target.rect.centerx - self.rect.centerx

            # Incrementa o relógio de decisão
            self.decision_timer += 1
            if self.decision_timer >= self.decision_cooldown:
                self.decision_timer = 0

                # Decisão por distância
                if abs(distancia_x) > 130:
                    self.current_action = "run"
                else:
                    opcoes = ["attack1", "attack2"]
                    if hasattr(self, 'special_energy') and hasattr(self, 'special_cost'):
                        if self.special_energy >= self.special_cost:
                            opcoes.append("special")
                    self.current_action = random.choice(opcoes)

            # Execução da ação escolhida
            if self.current_action == "run":
                self.running = True
                dx = self.speed if distancia_x > 0 else -self.speed

            elif self.current_action == "attack1":
                self.attack_type = 1
                self.attack(target)
                self.current_action = "idle"

            elif self.current_action == "attack2":
                self.attack_type = 2
                self.attack(target)
                self.current_action = "idle"

            elif self.current_action == "special":
                self.special_attack(target)
                self.current_action = "idle"

        return dx

    def move(self, screen_width, screen_height, surface, target, round_over):
        """Aplica a movimentação física, gravidade, limites de tela e rotação do Boss."""
        self.running = False
        self.attack_type = 0

        # Obtém o deslocamento horizontal calculado pela IA
        dx = self.update_ai(target, round_over)
        dy = 0

        # Aplica gravidade
        self.vel_y += self.gravity
        dy += self.vel_y

        # Mantém o Boss dentro dos limites horizontais da tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        # Mantém o Boss no chão da arena
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # Vira para olhar sempre na direção do alvo (Herói)
        self.flip = target.rect.centerx <= self.rect.centerx

        # Aplica cooldown de ataque de forma contínua
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Atualiza a posição física no retângulo do Pygame
        self.rect.x += dx
        self.rect.y += dy