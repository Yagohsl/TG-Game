import pygame
import random
import math
from bosses.boss import Boss

class BossAnxiety(Boss):
    def __init__(self, name, animation_steps, sprite_sheet, icon, data, player, x, y, flip):
        super().__init__(name, animation_steps, sprite_sheet, icon, data, player, x, y, flip)
       
   
        self.projectiles = []
        self.projectile_cooldown = 0
        self.shoot_interval = 200 
        self.animation_cooldown = 120

        #checa se projetil foi lançado
        self.fired_this_cycle = False
        
        self.dash_max_distance = 500
        self.dash_distance_left = 0
        self.dash_speed = 40
        self.dash_direction = 0
        self.dash_hit = False
        self.dash_prep_timer = 0

        self.teleport_count = 0
        self.teleport_timer = 0
        self.teleport_stage = "idle"  # "idle", "warning", "stay"
        self.teleport_target_pos = (0, 0)
        self.teleport_warning_duration = 700  
        self.teleport_stay_duration = 300     
        self.min_teleport_distance = 250      

        self.animation_map = {
            "idle": 0,
            "run": 1,
            "thoughts": 2,  
            "thought_explosion": 5,
            "thought_explosion_prep": 5,
            "teleport": 5, 
            "dash_prep": 3,
            "dash": 3,
            "death": 4
}
        self.explosion_prep_timer = 0
        self.health = 150
    
    def reset(self):
        super().reset()
        
        self.current_action = "idle"  
        
        if hasattr(self, 'action_start_time'):
            self.action_start_time = pygame.time.get_ticks()
        if hasattr(self, 'projectiles'):
            self.projectiles.clear()

    def fire_preoccupation(self, target):
        """Calcula a rota até o jogador e aplica desvios imprevisíveis (angulares e de velocidade)."""
        start_x = self.rect.centerx
        start_y = self.rect.centery
        
        dx = target.rect.centerx - start_x
        dy = target.rect.centery - start_y
        base_angle = math.atan2(dy, dx)
        
        #trajetória irregular com desvio aleatório
        irregular_angle = base_angle + random.uniform(-0.2, 0.2)
        
        #velocidades variadas
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

    def fire_explosion(self):
        start_x = self.rect.centerx
        start_y = self.rect.centery

        num_projectiles = 12
        speed = 18

        for i in range(num_projectiles):
            angle = (2 * math.pi / num_projectiles) *i

            projectile = {
                "x": start_x,
                "y": start_y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "radius": random.randint(12, 15),
                "spawn_time": pygame.time.get_ticks(),
                "wave_speed": random.uniform(10, 18),
                "wave_amplitude": random.uniform(2, 4)  #mantém o efeito ondulatório 
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
                if hasattr(target, 'dashing') and target.dashing:
                    continue  # Passa direto sem causar dano ou sumir com o projétil

                if hasattr(target, 'health'):
                    target.health -= 5  # Dano baixo e focado em exaustão psicológica
                    target.hit = True
                self.projectiles.remove(proj)
                continue
                
            # Limpeza preventiva de memória (Fora da tela HD 1280x720)
            if proj["x"] < -50 or proj["x"] > 1330 or proj["y"] < -50 or proj["y"] > 770:
                self.projectiles.remove(proj)

    def draw_projectiles(self, surface):
        """Desenha graficamente as esferas na arena."""
        for proj in self.projectiles:
            # Aura externa laranja
            pygame.draw.circle(surface, (255, 114, 13), (int(proj["x"]), int(proj["y"])), proj["radius"] + 2)
            # Aura interna preta
            pygame.draw.circle(surface, (0, 0, 0), (int(proj["x"]), int(proj["y"])), int(proj["radius"] / 2))

        # Efeito visual de aviso no local de destino do teletransporte
        if self.current_action == "teleport" and self.teleport_stage == "warning":
            center_x = self.teleport_target_pos[0] + self.rect.width // 2
            center_y = self.teleport_target_pos[1] + self.rect.height // 2
            
            # Gera 6 círculos
            for _ in range(6):
                offset_x = random.randint(-25, 25)
                offset_y = random.randint(-40, 40)
                radius = random.randint(6, 14)
                # Faísca externa laranja 
                pygame.draw.circle(surface, (255, 114, 13), (center_x + offset_x, center_y + offset_y), radius)
                # Centro preto
                pygame.draw.circle(surface, (0, 0, 0), (center_x + offset_x, center_y + offset_y), radius // 2)

    def update_ai(self, target, round_over):
        dx = 0

        if not self.alive:
            self.current_action = "death"
            return dx
        current_time = pygame.time.get_ticks()

        if not self.attacking and self.alive and not round_over:
            distancia_x = target.rect.centerx - self.rect.centerx

            # Dano por contato direto 
            if self.rect.colliderect(target.rect) and self.attack_cooldown == 0 and self.current_action != "dash":
                target.hit = True
                if hasattr(target, 'dashing') and target.dashing:
                    pass 
                else:
                    target.hit = True
                    if hasattr(target, 'health'):
                        target.health -= 10
                    self.attack_cooldown = 60

            # Cronômetro de tomada de decisão
            if self.current_action not in ["dash","dash_prep", "teleport", "thought_explosion_prep", "thought_explosion"]:
                self.animation_cooldown = 120
                self.decision_timer += 1
                if self.decision_timer >= self.decision_cooldown:
                    self.decision_timer = 0

                    self.fired_this_cycle = False

                    #IA escolhe aleatoriamente qual ação irá fazer
                    self.current_action = random.choice(["run","dash_prep","thoughts", "thought_explosion_prep", "teleport", "run"])
                 

            # --- EXECUÇÃO DOS ESTADOS EXCLUSIVOS DO BOSS ---
            if self.current_action == "run":
                self.running = True
                dx = self.speed if distancia_x > 0 else -self.speed

            elif self.current_action == "thoughts":
                self.running = False
                if not self.fired_this_cycle:
                    self.fire_preoccupation(target)
                    self.fired_this_cycle = True

            # === PREPARO DA EXPLOSÃO ===
            elif self.current_action == "thought_explosion_prep":
                self.running = False
                
                # Inicializa um temporizador
                if not hasattr(self, 'explosion_prep_timer') or self.explosion_prep_timer == 0:
                    self.explosion_prep_timer = current_time

                # Aguarda 500ms carregando o golpe no Frame 0
                if current_time - self.explosion_prep_timer >= 500:
                    self.explosion_prep_timer = current_time # Reaproveita o timer para a pose do disparo
                    self.current_action = "thought_explosion" # Transiciona para o ataque real

            # === REALIZAÇÃO DA EXPLOSÃO ===
            elif self.current_action == "thought_explosion":
                self.running = False
                if not self.fired_this_cycle:
                    self.fire_explosion() # Dispara os projéteis 360
                    self.fired_this_cycle = True

                # Mantém o Boss travado na pose de disparo por mais 400ms antes de voltar ao idle
                if current_time - self.explosion_prep_timer >= 400:
                    self.explosion_prep_timer = 0 # Reseta o timer
                    self.current_action = "idle" # Libera o Boss

            # === TELEPORTE ===
            elif self.current_action == "teleport":
                self.running = False
                self.gravity = 0
                
                # Inicializa o ciclo completo do ataque
                if self.teleport_stage == "idle":
                    self.teleport_count = 0
                    self.teleport_stage = "warning"
                    self.teleport_timer = current_time
                    
                    # Define o primeiro ponto aleatório 
                    rand_x = random.randint(100, 1180)
                    while abs(rand_x - self.rect.x) < self.min_teleport_distance:
                        rand_x = random.randint(100, 1180)
                    rand_y = random.randint(720 - 110 - self.rect.height- 150, 720 - 110 - self.rect.height)
                    

                    self.teleport_target_pos = (rand_x, rand_y)

                # aviso visual na tela
                elif self.teleport_stage == "warning":
                    if current_time - self.teleport_timer >= self.teleport_warning_duration:
                        # Estourou os 500ms de aviso muda o Boss para a posição 
                        self.rect.x = self.teleport_target_pos[0]
                        self.rect.y = self.teleport_target_pos[1]
                        self.teleport_count += 1

                        # Checa se ja realizou os 3 teletransportes
                        if self.teleport_count >= 3:
                            self.teleport_stage = "idle"
                            self.current_action = "idle"
                            self.gravity = 2
                        else:
                            # Entra em janela curta de permanencia antes do próximo sumiço
                            self.teleport_stage = "stay"
                            self.teleport_timer = current_time

                # Boss pousou e aguarda um instante antes de saltar novamente
                elif self.teleport_stage == "stay":
                    if current_time - self.teleport_timer >= self.teleport_stay_duration:
                        # Sorteia um novo lugar e volta para o modo de aviso 
                        self.teleport_stage = "warning"
                        self.teleport_timer = current_time

                        rand_x = random.randint(100, 1180)
                        while abs(rand_x - self.rect.x) < self.min_teleport_distance:
                            rand_x = random.randint(100, 1180)

                        rand_y = random.randint(720 - 110 - self.rect.height- 150, 720 - 110 - self.rect.height)
                        self.teleport_target_pos = (rand_x, rand_y)

            # === DASH ===
            elif self.current_action == "dash_prep":
                self.running = False  # Fica estático
                
                if self.dash_prep_timer == 0:
                    self.dash_prep_timer = current_time  # Marca o início do preparo

                # Se passou 500ms transiciona para o ataque real
                if current_time - self.dash_prep_timer >= 500:
                    self.dash_prep_timer = 0  
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

                # Detecção de dano
                if self.rect.colliderect(target.rect) and not self.dash_hit:
                    if hasattr(target, 'dashing') and target.dashing:
                        pass 
                    else:
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
        if self.current_action in self.animation_map and not self.attacking:
            visual_id = self.animation_map[self.current_action]
            self.update_action(visual_id)

        return dx
    
    def update(self):
        """Bloqueia e protege a animação customizada para impedir o reset automático do Fighter."""
        if self.current_action == "death":
            self.update_action(self.animation_map["death"])

            if self.frame_index >= len(self.animation_list[self.action]) -1:
                self.frame_index = len(self.animation_list[self.action]) -1
            else:
                if pygame.time.get_ticks() -self.update_time > self.animation_cooldown:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()
            self.image = self.animation_list[self.action][self.frame_index]
            return

        # Se estiver vivo, não estiver tomando dano e nem atacando fisicamente corpo-a-corpo
        if self.alive and not self.hit and not self.attacking:

            # CONTROLADOR DO PREPARO DA EXPLOSÃO 
            if self.current_action == "thought_explosion_prep":
                self.update_action(5) 
                self.frame_index = 0  #frame preparo
                self.image = self.animation_list[self.action][self.frame_index]
                return

            # CONTROLADOR DO ATAQUE REAL DA EXPLOSÃO 
            elif self.current_action == "thought_explosion":
                self.update_action(5)
                self.frame_index = 1  #frame realização
                self.image = self.animation_list[self.action][self.frame_index]
                return
            
            if self.current_action == "thoughts":
                self.update_action(2)  
                
                if pygame.time.get_ticks() - self.update_time > self.animation_cooldown:
                    self.frame_index += 1
                    self.update_time = pygame.time.get_ticks()
                
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0
                    self.current_action = "idle"  
                    
                self.image = self.animation_list[self.action][self.frame_index]
                return  
            
            elif self.current_action == "teleport":
                self.update_action(5)
                self.frame_index = 1
                self.image = self.animation_list[self.action][self.frame_index]
                return
            
            elif self.current_action == "dash_prep":
                self.update_action(3)
                self.frame_index = 1
                self.image = self.animation_list[self.action][self.frame_index]
                return  

            # Se já estiver executando o dash, exibe apenas o frame 1
            elif self.current_action == "dash":
                self.update_action(3)
                self.frame_index = 0
                self.image = self.animation_list[self.action][self.frame_index]
                return

        super().update()

    def move(self, screen_width, screen_height, surface, target, round_over):
        self.update_projectiles(target)
        super().move(screen_width, screen_height, surface, target, round_over)
        