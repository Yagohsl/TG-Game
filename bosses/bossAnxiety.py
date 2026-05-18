import pygame
import random
import math
from bosses.boss import Boss

class BossAnxiety(Boss):
    def __init__(self, name, animation_steps, sprite_sheet, icon, data, player, x, y, flip):
        super().__init__(name, animation_steps, sprite_sheet, icon, data, player, x, y, flip)
       
        # Controle exclusivo do Bombardeio de Preocupações
        self.projectiles = []
        self.projectile_cooldown = 0
        self.shoot_interval = 200  # Corrigido para 200 milissegundos para criar um bombardeio real
        self.animation_cooldown = 120

        #checa se projetil foi lançado
        self.fired_this_cycle = False
        
        self.dash_max_distance = 500
        self.dash_distance_left = 0
        self.dash_speed = 40
        self.dash_direction = 0
        self.dash_hit = False
        self.dash_prep_timer = 0

        self.animation_map = {
            "idle": 0,
            "run": 1,
            "thoughts": 2,  
            "dash_prep": 3,
            "dash": 3
      
}
    
    def fire_preoccupation(self, target):
        """Calcula a rota até o jogador e aplica desvios imprevisíveis (angulares e de velocidade)."""
        start_x = self.rect.centerx
        start_y = self.rect.centery
        
        dx = target.rect.centerx - start_x
        dy = target.rect.centery - start_y
        base_angle = math.atan2(dy, dx)
        
        # Trajetória irregular com desvio aleatório
        irregular_angle = base_angle + random.uniform(-0.2, 0.2)
        
        # Velocidades variadas simulando pensamentos acelerados
        speed = 18
        
        projectile = {
            "x": start_x,
            "y": start_y,
            "vx": math.cos(irregular_angle) * speed,
            "vy": math.sin(irregular_angle) * speed,
            "radius": random.randint(14, 17),
            "spawn_time": pygame.time.get_ticks(),
            "wave_speed": random.uniform(15, 25),
            "wave_amplitude": random.uniform(2, 5)
        }
        
        self.projectiles.append(projectile)

    def update_projectiles(self, target):
        """Gerencia a movimentação ondulatória dos projéteis e colisões com o Herói."""
        current_time = pygame.time.get_ticks()
        
        for proj in self.projectiles[:]:
            time_alive = (current_time - proj["spawn_time"]) / 1000.0
            
            # Efeito senoidal para fazer o projétil serpentear de forma instável
            wave = math.sin(time_alive * proj["wave_speed"]) * proj["wave_amplitude"]
            
            proj["x"] += proj["vx"]
            proj["y"] += proj["vy"] + wave
            
            # Hitbox virtual do projétil
            proj_rect = pygame.Rect(
                proj["x"] - proj["radius"], 
                proj["y"] - proj["radius"], 
                proj["radius"] * 2, 
                proj["radius"] * 2
            )
            
            # Verificação de impacto
            if proj_rect.colliderect(target.rect):
                if hasattr(target, 'health'):
                    target.health -= 5  # Dano baixo e focado em exaustão psicológica
                self.projectiles.remove(proj)
                continue
                
            # Limpeza preventiva de memória (Fora da tela HD 1280x720)
            if proj["x"] < -50 or proj["x"] > 1330 or proj["y"] < -50 or proj["y"] > 770:
                self.projectiles.remove(proj)

    def draw_projectiles(self, surface):
        """Desenha graficamente as esferas de pensamentos intrusivos na arena."""
        for proj in self.projectiles:
            # Aura externa laranja
            pygame.draw.circle(surface, (255, 114, 13), (int(proj["x"]), int(proj["y"])), proj["radius"] + 2)
            # Aura interna preta
            pygame.draw.circle(surface, (0, 0, 0), (int(proj["x"]), int(proj["y"])), int(proj["radius"] / 2))

    def update_ai(self, target, round_over):
        """Sobrescreve apenas as regras de decisão e ataques da Ansiedade."""
        dx = 0
        current_time = pygame.time.get_ticks()

        if not self.attacking and self.alive and not round_over:
            distancia_x = target.rect.centerx - self.rect.centerx

            # Dano por contato direto por aproximação excessiva
            if self.rect.colliderect(target.rect) and self.attack_cooldown == 0 and self.current_action != "dash":
                target.hit = True
                if hasattr(target, 'health'):
                    target.health -= 10
                self.attack_cooldown = 60

            # Cronômetro de tomada de decisão
            if self.current_action not in ["dash","dash_prep"]:
                self.animation_cooldown = 120
                self.decision_timer += 1
                if self.decision_timer >= self.decision_cooldown:
                    self.decision_timer = 0

                    self.fired_this_cycle = False

                    # Longe: Persegue ou ativa Bombardeio de Preocupações ("thoughts")
                    if abs(distancia_x) > 130:
                        self.current_action = random.choice(["run","dash_prep","thoughts"])
                    # Perto: Ataques tradicionais ou recuo tático de pânico ("retreat")
                    else:
                        opcoes = ["attack1", "attack2"]
                        if hasattr(self, 'special_energy') and hasattr(self, 'special_cost'):
                            if self.special_energy >= self.special_cost:
                                opcoes.append("special")
                        self.current_action = random.choice(opcoes)

            # --- EXECUÇÃO DOS ESTADOS EXCLUSIVOS DA ANSIEDADE ---
            if self.current_action == "run":
                self.running = True
                dx = self.speed if distancia_x > 0 else -self.speed

            elif self.current_action == "thoughts":
                self.running = False
                if not self.fired_this_cycle:
                    self.fire_preoccupation(target)
                    self.fired_this_cycle = True

            elif self.current_action == "dash_prep":
                self.running = False  # Fica estático acumulando energia
                
                if self.dash_prep_timer == 0:
                    self.dash_prep_timer = current_time  # Marca o início do preparo

                # Se passou 500ms, transiciona para o ataque real
                if current_time - self.dash_prep_timer >= 500:
                    self.dash_prep_timer = 0  # Reseta o cronômetro para o próximo uso
                    self.current_action = "dash"
                    
                    # Inicializa os dados de movimento imediatamente no arranque
                    self.dash_direction = 1 if distancia_x > 0 else -1
                    self.dash_distance_left = self.dash_max_distance
                    self.dash_hit = False
            
            elif self.current_action == "dash":
                self.running = True
                self.animation_cooldown = 20  

                # O passo é de 40px, pega o que restar para cravar a distância final
                passo_atual = min(self.dash_speed, self.dash_distance_left)
                
                dx = passo_atual * self.dash_direction
                self.dash_distance_left -= passo_atual  

                # Detecção de dano por atropelamento
                if self.rect.colliderect(target.rect) and not self.dash_hit:
                    target.hit = True
                    if hasattr(target, 'health'):
                        target.health -= 15  
                    self.dash_hit = True  

                # Condição de término do movimento
                if self.dash_distance_left <= 0:
                    self.dash_direction = 0       
                    self.current_action = "idle"


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

        # --- APLICADOR DINÂMICO DE ANIMAÇÃO ---
        # Se a ação atual da IA está no nosso mapa visual, nós a aplicamos!
        if self.current_action in self.animation_map and not self.attacking:
            visual_id = self.animation_map[self.current_action]
            self.update_action(visual_id)

        return dx
    
    def update(self):
        """Bloqueia e protege a animação customizada para impedir o reset automático do Fighter."""
        # Se estiver vivo, não estiver tomando dano e nem atacando fisicamente corpo-a-corpo
        if self.alive and not self.hit and not self.attacking:
            if self.current_action == "thoughts":
                self.update_action(2)  # Força e mantém o índice 2 da folha ativo
                
                # Avança o índice de frames manualmente respeitando o tempo
                if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()
                
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0
                    self.current_action = "idle"  # Força o estado a virar IDLE na hora!
                    
                self.image = self.animation_list[self.action][self.frame_index]
                return  # RETORNA ANTECIPADAMENTE
            
            elif self.current_action == "dash_prep":
                self.update_action(3)
                self.frame_index = 1
                self.image = self.animation_list[self.action][self.frame_index]
                return  # Ignora o super().update() para não rodar a animação sozinho

            # Se já estiver executando o dash, exibe apenas o frame 1
            elif self.current_action == "dash":
                self.update_action(3)
                self.frame_index = 0
                self.image = self.animation_list[self.action][self.frame_index]
                return

        # Se não estiver no estado especial, executa os comportamentos padrões herdados (idle, run, hit, death)
        super().update()

    def move(self, screen_width, screen_height, surface, target, round_over):
        """Atualiza a física dos projéteis e aproveita toda a física base do Boss."""
        self.update_projectiles(target)
        # Delega gravidade, limites, inversão e movimentação final para a classe base
        super().move(screen_width, screen_height, surface, target, round_over)
        