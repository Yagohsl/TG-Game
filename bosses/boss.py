import pygame
import random
from fighters.fighterPlayer import FighterPlayer


class Boss(FighterPlayer):
    def __init__(self, name, animation_steps, sprite_sheet, icon, data, player, x, y, flip):
        # Repassa todos os parâmetros para o FighterPlayer
        super().__init__(name, animation_steps, sprite_sheet, icon, data, player, x, y, flip)

        # Variáveis exclusivas da IA
        self.decision_timer = 0
        self.current_action = "idle"

    def move(self, screen_width, screen_height, surface, target, round_over):
        speed = 6
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # Só toma decisões se não estiver no meio de um ataque, estiver vivo e o round rolando
        if self.attacking == False and self.alive == True and round_over == False:

            # Calcula a distância entre o Boss e o Jogador
            distancia_x = target.rect.centerx - self.rect.centerx

            # O Boss "pensa" a cada 30 frames
            self.decision_timer += 1
            if self.decision_timer >= 300:
                self.decision_timer = 0

                # --- NOVA MÁQUINA DE ESTADOS ---

                # 2. Se não está em perigo e está longe, persegue
                if abs(distancia_x) > 130:
                    self.current_action = "run"

                # 3. Se está perto, combate
                else:
                    opcoes = ["attack1", "attack2"]
                    if self.special_energy >= self.special_cost:
                        opcoes.append("special")
                    self.current_action = random.choice(opcoes)

            # --- EXECUTA A AÇÃO ESCOLHIDA ---

            

            if self.current_action == "run":
                self.running = True
                # Anda na direção do jogador
                if distancia_x > 0:
                    dx = speed
                else:
                    dx = -speed

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



        # Aplica gravidade
        self.vel_y += gravity
        dy += self.vel_y

        # Mantém na tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # Vira para olhar para o alvo
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Aplica cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Atualiza a posição
        self.rect.x += dx
        self.rect.y += dy