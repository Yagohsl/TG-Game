import pygame
import random
import math
from bosses.boss import Boss

class BossAnxiety(Boss):
    def __init__(self, name, animation_steps, sprite_sheet, icon, data, player, x, y, flip):
        super().__init__(name, animation_steps, sprite_sheet, icon, data, player, x, y, flip)
       
        # Controle do Bombardeio de Preocupações
        self.projectiles = []
        self.projectile_cooldown = 0
        self.shoot_interval = 3000 #Dispara um novo projétil a cada 200 milissegundos
    
    def fire_preoccupation(self, target):
        """Calcula a rota até o jogador e aplica desvios imprevisíveis."""
        start_x = self.rect.centerx
        start_y = self.rect.centery
        
        # 1. Descobre a distância horizontal e vertical até o centro do Herói
        dx = target.rect.centerx - start_x
        dy = target.rect.centery - start_y
        base_angle = math.atan2(dy, dx)
        
        # 2. Torna a trajetória irregular: adiciona um desvio aleatório no ângulo original [cite: 1, 8]
        # O valor entre -0.5 e 0.5 garante que o tiro saia um pouco torto, espalhando o bombardeio
        irregular_angle = base_angle + random.uniform(-0.5, 0.5)
        
        # 3. Torna a velocidade imprevisível: alguns pensamentos são mais rápidos que outros [cite: 1, 8]
        speed = random.uniform(7, 12)
        
        # Criamos o dicionário do projétil com comportamento próprio de onda
        projectile = {
            "x": start_x,
            "y": start_y,
            "vx": math.cos(irregular_angle) * speed,
            "vy": math.sin(irregular_angle) * speed,
            "radius": random.randint(14, 17), # Projéteis pequenos [cite: 1, 12]
            "spawn_time": pygame.time.get_ticks(),
            "wave_speed": random.uniform(15, 25), # Frequência da oscilação
            "wave_amplitude": random.uniform(2, 5) # Força do desvio vertical
        }
        
        self.projectiles.append(projectile)

    def update_projectiles(self, target):
        """Gerencia a física ondulatória e o impacto com o Herói."""
        current_time = pygame.time.get_ticks()
        
        # Percorre uma cópia da lista [:] para permitir a remoção segura de itens durante o loop 
        for proj in self.projectiles[:]:
            # Calcula há quantos segundos o projétil existe
            time_alive = (current_time - proj["spawn_time"]) / 1000.0
            
            # Efeito ondulatório: cria uma perturbação baseada no Seno do tempo ativo
            # Isso faz o projétil "vibrar" ou serpentear pelo ar de forma instável
            wave = math.sin(time_alive * proj["wave_speed"]) * proj["wave_amplitude"]
            
            # Atualiza a posição X e Y
            proj["x"] += proj["vx"]
            proj["y"] += proj["vy"] + wave
            
            # Cria um retângulo virtual (Rect) temporário para usar o sistema de colisões do Pygame 
            proj_rect = pygame.Rect(
                proj["x"] - proj["radius"], 
                proj["y"] - proj["radius"], 
                proj["radius"] * 2, 
                proj["radius"] * 2
            )
            
            # Verifica impacto com o Herói 
            if proj_rect.colliderect(target.rect):
                if hasattr(target, 'health'):
                    target.health -= 2 # Causa pouco dano por projétil, focando no cansaço mental [cite: 6, 8]
                self.projectiles.remove(proj)
                continue
                
            # Limpa da memória caso saia dos limites de uma tela HD (1280x720) [cite: 8, 158]
            if proj["x"] < -50 or proj["x"] > 1330 or proj["y"] < -50 or proj["y"] > 770:
                self.projectiles.remove(proj)

    def draw_projectiles(self, surface):
        """Desenha as esferas de pensamentos intrusivos na arena."""
        for proj in self.projectiles:
            # Camada externa: Aura do pensamento negativo (Roxo/Violeta) 
            pygame.draw.circle(surface, (140, 20, 180), (int(proj["x"]), int(proj["y"])), proj["radius"] + 2)
            # Camada interna: Núcleo brilhante de energia 
            pygame.draw.circle(surface, (240, 220, 255), (int(proj["x"]), int(proj["y"])), int(proj["radius"] / 2))

    def move(self, screen_width, screen_height, surface, target, round_over):

        speed = 6 
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        current_time = pygame.time.get_ticks()


        # Garante que os projéteis continuem voando de forma independente na arena
        self.update_projectiles(target)

        # Condições de execução de movimentos (vivos e durante a partida)
        if self.attacking == False and self.alive == True and round_over == False:
            distancia_x = target.rect.centerx - self.rect.centerx

            #Se encostar no player, da dano
            if abs(distancia_x) < 85 and self.attack_cooldown == 0:
                target.hit = True
                target.health -= 10
                self.attack_cooldown = 60

            # Sistema de decisão a cada 30 frames
            self.decision_timer += 1
            if self.decision_timer >= 30:
                self.decision_timer = 0

                # 2. Quando estiver longe, escolhe entre avançar ou usar o Bombardeio ("thoughts")
                if abs(distancia_x) > 130:
                    self.current_action = random.choice(["run", "thoughts"])

                # 3. Combate de Curto Alcance
                else:
                    opcoes = ["attack1", "attack2"]
                    if self.special_energy >= self.special_cost:
                        opcoes.append("special")
                    self.current_action = random.choice(opcoes)

            # --- EXECUÇÃO DAS AÇÕES DA MÁQUINA DE ESTADOS ---

            if self.current_action == "retreat":
                self.running = True
                dx = -speed if distancia_x > 0 else speed

            elif self.current_action == "run":
                self.running = True
                dx = speed if distancia_x > 0 else -speed

            # EXECUÇÃO DO NOVO ATAQUE: Bombardeio de Preocupações
            elif self.current_action == "thoughts":
                self.running = True
                # O boss recua lentamente (metade da velocidade) enquanto atira para manter distância
                dx = -(speed * 0.5) if distancia_x > 0 else (speed * 0.5)
                
                # Controla a cadência de tiro usando o relógio interno do Pygame
                if current_time - self.projectile_cooldown > self.shoot_interval:
                    self.fire_preoccupation(target)
                    self.projectile_cooldown = current_time

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

        # --- REGRAS DE GRAVIDADE E LIMITES DE TELA ---
        self.vel_y += gravity
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # Alinha a direção do sprite para encarar o alvo
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # Atualização de posicionamento final
        self.rect.x += dx
        self.rect.y += dy
     